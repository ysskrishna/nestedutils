"""Custom exceptions for the nestedutils library.

This module defines all custom exceptions used throughout the nestedutils
library. The main exception class is PathError, which includes error codes
for detailed error handling.
"""

from typing import Optional
from nestedutils.enums import PathErrorCode


class PathError(Exception):
    """Raised when a nested path cannot be navigated or modified.
    
    Attributes:
        message: Human-readable error message.
        code: Optional PathErrorCode for programmatic error handling.
    
    Example:
        ```python
        from nestedutils import set_at, PathError, PathErrorCode
        
        data = {"a": {"b": 1}}
        
        # set_at raises when path doesn't exist (create=False is default)
        try:
            set_at(data, "a.c.d", "value")
        except PathError as e:
            if e.code == PathErrorCode.MISSING_KEY:
                print(f"Path doesn't exist: {e.message}")
        
        # get_at raises for missing paths in v2.0 - use default= for optional values
        from nestedutils import get_at
        result = get_at(data, "a.c.d", default="not found")
        print(result)  # "not found"
        ```
    """
    
    def __init__(self, message: str, code: Optional[PathErrorCode] = None) -> None:
        super().__init__(message)
        self.message = message
        self.code = code
