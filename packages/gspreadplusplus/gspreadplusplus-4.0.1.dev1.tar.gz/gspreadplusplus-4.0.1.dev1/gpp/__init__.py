from .core import GPP

# Create an alias for backward compatibility
import sys
sys.modules['gspreadplusplus'] = sys.modules[__name__]

__version__ = '4.0.1dev1'
__all__ = ['GPP']