"""Enumerations for nestedutils library.

This module defines error codes used throughout the nestedutils library
for consistent error handling.
"""

from enum import Enum


class PathErrorCode(Enum):
    """Error codes for path-related exceptions.
    
    Example:
        ```python
        from nestedutils import get_at, PathError, PathErrorCode
        
        data = {"a": {"b": 1}}
        try:
            result = get_at(data, "a.c.d")
            # get_at raises PathError for missing paths in v2.0
        except PathError as e:
            if e.code == PathErrorCode.MISSING_KEY:
                print("Key not found")
        ```
    """
    INVALID_INDEX = "INVALID_INDEX"
    """Raised when a list index is invalid (non-numeric, out of bounds, or would create sparse list)."""
    
    MISSING_KEY = "MISSING_KEY"
    """Raised when a required key doesn't exist (in set_at with create=False or delete_at)."""
    
    EMPTY_PATH = "EMPTY_PATH"
    """Raised when path is empty or contains empty keys."""
    
    IMMUTABLE_CONTAINER = "IMMUTABLE_CONTAINER"
    """Raised when attempting to modify an immutable container (tuple)."""
    
    INVALID_PATH = "INVALID_PATH"
    """Raised when path format is invalid (wrong type, exceeds max depth, etc.)."""