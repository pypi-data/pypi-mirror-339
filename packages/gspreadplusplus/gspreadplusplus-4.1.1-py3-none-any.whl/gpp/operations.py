import copy
from typing import Dict, Any, List
from pyspark.sql import DataFrame
from .functions import resolve_function_value


def process_update_config(config: Dict, df: DataFrame, worksheet: Any) -> Dict:
    """
    Process the update configuration and resolve any function references.

    Args:
        config: The update configuration
        df: Source DataFrame
        worksheet: Source worksheet

    Returns:
        Processed configuration with resolved values
    """
    processed_config = copy.deepcopy(config)

    # Get sheet header if needed
    sheet_header = None
    sheet_values = worksheet.get_all_values()
    if sheet_values:
        sheet_header = sheet_values[0]

    for operation in processed_config["operations"]:
        # Check each field that might contain a function reference
        for field in ["value", "start_value", "end_value"]:
            if field in operation and isinstance(operation[field], dict) and "function" in operation[field]:
                operation[field] = resolve_function_value(
                    operation[field], df, worksheet, sheet_header
                )

    return processed_config


def apply_update_operations(config: Dict, worksheet: Any) -> int:
    """
    Apply operations specified in configuration to the worksheet.

    Args:
        config: Processed configuration with resolved values
        worksheet: Target worksheet

    Returns:
        The row index where new data should start (1-based)
    """
    sheet_values = worksheet.get_all_values()
    if not sheet_values:
        return 1  # Empty sheet, start at row 1

    header = sheet_values[0]
    data_rows = sheet_values[1:]

    # Process each operation sequentially
    for operation in config["operations"]:
        op_type = operation["type"].lower()

        if op_type == "sort":
            # Sort data rows by column
            column = operation["column"]
            direction = operation["direction"].lower()

            if column not in header:
                raise ValueError(f"Sort column '{column}' not found in header: {header}")

            col_idx = header.index(column)
            reverse = (direction == "desc")

            data_rows.sort(key=lambda row: row[col_idx], reverse=reverse)

        elif op_type == "delete_from":
            # Delete rows from a specific value
            column = operation["column"]
            value = operation["value"]
            inclusive = operation.get("inclusive", True)

            if column not in header:
                raise ValueError(f"Delete column '{column}' not found in header: {header}")

            col_idx = header.index(column)

            if inclusive:
                data_rows = [row for row in data_rows if row[col_idx] < value]
            else:
                data_rows = [row for row in data_rows if row[col_idx] <= value]

        elif op_type == "delete_range":
            # Delete rows in a value range
            column = operation["column"]
            start_value = operation["start_value"]
            end_value = operation["end_value"]
            inclusive = operation.get("inclusive", True)

            if column not in header:
                raise ValueError(f"Delete column '{column}' not found in header: {header}")

            col_idx = header.index(column)

            if inclusive:
                data_rows = [row for row in data_rows
                             if row[col_idx] < start_value or row[col_idx] > end_value]
            else:
                data_rows = [row for row in data_rows
                             if row[col_idx] <= start_value or row[col_idx] >= end_value]

        elif op_type == "delete_where":
            # Delete rows where a condition is met
            column = operation["column"]
            value = operation["value"]
            operator = operation.get("operator", "eq")  # eq, ne, gt, lt, ge, le

            if column not in header:
                raise ValueError(f"Delete column '{column}' not found in header: {header}")

            col_idx = header.index(column)

            # Define comparison operators
            operators = {
                "eq": lambda x, y: x == y,
                "ne": lambda x, y: x != y,
                "gt": lambda x, y: x > y,
                "lt": lambda x, y: x < y,
                "ge": lambda x, y: x >= y,
                "le": lambda x, y: x <= y
            }

            if operator not in operators:
                raise ValueError(f"Unknown operator: {operator}")

            # Filter rows that don't match the condition
            data_rows = [row for row in data_rows
                         if not operators[operator](row[col_idx], value)]

        else:
            raise ValueError(f"Unknown operation type: {op_type}")

    # Update worksheet with modified data
    worksheet.clear()  # Clear existing data

    # Update with header and filtered data
    if data_rows:
        worksheet.update('A1', [header] + data_rows)
    else:
        worksheet.update('A1', [header])

    # Return the row where new data should start
    return len(data_rows) + 1  # +1 for header row