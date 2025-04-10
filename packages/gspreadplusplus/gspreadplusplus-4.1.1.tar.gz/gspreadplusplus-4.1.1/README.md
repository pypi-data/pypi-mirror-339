# gspreadplusplus

A Python library that enhances Google Sheets operations with additional functionality and improved data type handling.

## Features

- Transfer Spark DataFrames to Google Sheets with proper type conversion
- Append data to existing sheets while maintaining structure
- Intelligent handling of various data types (numbers, dates, timestamps, etc.)
- Preserve or update sheet headers
- Selective column clearing options
- Automatic date formatting
- Sheet dimension management
- Configuration management with key-value storage

## Installation

```bash
pip install gspreadplusplus
```

## Requirements

- Python 3.7+
- gspread
- pyspark
- google-auth

## Usage

### Basic DataFrame Export

```python
from gspreadplusplus import GPP
from pyspark.sql import SparkSession

# Initialize Spark and create a DataFrame
spark = SparkSession.builder.appName("example").getOrCreate()
df = spark.createDataFrame([
    ("2024-01-01", 100, "Complete"),
    ("2024-01-02", 150, "Pending")
], ["date", "amount", "status"])

# Your Google Sheets credentials
creds_json = {
    "type": "service_account",
    # ... rest of your service account credentials
}

# Export DataFrame to Google Sheets
GPP.df_to_sheets(
    df=df,
    spreadsheet_id="your_spreadsheet_id",
    sheet_name="Sheet1",
    creds_json=creds_json
)
```

### Advanced DataFrame Export Options

```python
# Export with custom options
GPP.df_to_sheets(
    df=df,
    spreadsheet_id="your_spreadsheet_id",
    sheet_name="Sheet1",
    creds_json=creds_json,
    keep_header=True,     # Preserve existing header row
    erase_whole=False,    # Clear only necessary columns
    create_sheet=True     # Create sheet if it doesn't exist
)

# Append data to existing sheet
GPP.df_append_to_sheets(
    df=df,
    spreadsheet_id="your_spreadsheet_id",
    sheet_name="Sheet1",
    creds_json=creds_json,
    keep_header=True,     # Keep existing header
    create_sheet=True     # Create sheet if it doesn't exist
)
```

### Configuration Management

The library provides functionality to store and update configuration values in a Google Sheet. By default, it uses a sheet named "CONFIG" with keys in column A and values in column B.

```python
# Store or update a configuration value
result = GPP.set_config(
    spreadsheet_id="your_spreadsheet_id",
    key="api_endpoint",
    value="https://api.example.com",
    creds_json=creds_json,
    sheet_name="CONFIG"  # Optional, defaults to "CONFIG"
)

if result == 0:
    print("Configuration updated successfully")
else:
    print("Error updating configuration")
```

## Method Reference

### df_to_sheets
Exports a Spark DataFrame to Google Sheets, optionally preserving existing headers.

Parameters:
- `df`: Spark DataFrame containing the data to transfer
- `spreadsheet_id`: The ID of the Google Spreadsheet
- `sheet_name`: Name of the worksheet to update
- `creds_json`: Dictionary containing Google service account credentials
- `keep_header`: If True, preserve the first row of the sheet (default: False)
- `erase_whole`: If True, clear all columns and rows (default: True)
- `create_sheet`: If True, create the sheet if it doesn't exist (default: True)

### df_append_to_sheets
Appends data from a Spark DataFrame to an existing Google Sheet.

Parameters:
- `df`: Spark DataFrame containing the data to append
- `spreadsheet_id`: The ID of the Google Spreadsheet
- `sheet_name`: Name of the worksheet to update
- `creds_json`: Dictionary containing Google service account credentials
- `keep_header`: If True, preserve existing header (default: False)
- `create_sheet`: If True, create the sheet if it doesn't exist (default: True)

### set_config
Stores or updates configuration values in a designated sheet.

Parameters:
- `spreadsheet_id`: The ID of the Google Spreadsheet
- `key`: The key to store/update
- `value`: The value to set
- `creds_json`: Dictionary containing Google service account credentials
- `sheet_name`: Name of the configuration worksheet (default: "CONFIG")

Returns:
- 0 on success
- 1 on error

## Data Type Support

The library automatically handles conversion of various data types:

- Strings
- Integers (regular, long, bigint)
- Floating point numbers (double, float)
- Decimals
- Dates
- Timestamps
- Booleans

Null values are converted to:
- 0 for numeric types
- Empty string for other types

## Error Handling

The library implements comprehensive error handling:
- Returns status codes for operations (0 for success, 1 for failure)
- Prints detailed error messages for debugging
- Gracefully handles missing keys, sheet access issues, and credential problems
- Validates column count when appending with preserved headers

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.