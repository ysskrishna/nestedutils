from typing import Any, List, Union, Optional
from .exceptions import PathError
from .enums import PathErrorCode
from .constants import MAX_DEPTH, MAX_LIST_SIZE


def normalize_path(path: Union[str, List[Any]]) -> List[Union[str, int]]:
    """Normalize path to list of keys and validate.
    
    Converts path to a list of keys (strings or integers), validating that:
    - Path is not empty
    - No keys in the path are empty strings
    - Path depth does not exceed MAX_DEPTH
    
    For list paths, integer types are preserved to support dictionary keys with integer keys.
    For string paths (dot-notation), all keys are strings.
    
    Args:
        path: Either a dot-notation string (e.g., "a.b.c") or a list of keys.
    
    Returns:
        List of keys representing the path. Elements may be strings or integers.
        - String paths always return List[str]
        - List paths preserve integer types: List[Union[str, int]]
    
    Raises:
        PathError: If path format is invalid, path is empty, contains empty keys,
            or exceeds maximum depth.
    """
    if isinstance(path, list):
        # Preserve integer types from list paths to support dict keys with integer keys
        keys: List[Union[str, int]] = []
        for key in path:
            if isinstance(key, int):
                keys.append(key)
            elif isinstance(key, str):
                if key == "":
                    raise PathError("Path cannot contain empty keys", PathErrorCode.EMPTY_PATH)
                keys.append(key)
            else:
                # Convert other types to strings (e.g., bool, float)
                key_str = str(key)
                if key_str == "":
                    raise PathError("Path cannot contain empty keys", PathErrorCode.EMPTY_PATH)
                keys.append(key_str)
    elif isinstance(path, str):
        keys = path.split(".")
    else:
        raise PathError(
            f"Path must be string or list, got {type(path).__name__}", 
            PathErrorCode.INVALID_PATH
        )
    
    if not keys:
        raise PathError("Path cannot be empty", PathErrorCode.EMPTY_PATH)
    
    if len(keys) > MAX_DEPTH:
        raise PathError(
            f"Path depth exceeds maximum of {MAX_DEPTH}",
            PathErrorCode.INVALID_PATH
        )
    
    # Check for empty strings (integers can't be empty)
    if any(key == "" for key in keys if isinstance(key, str)):
        raise PathError("Path cannot contain empty keys", PathErrorCode.EMPTY_PATH)
    
    return keys


def is_int_key(key: Union[str, int]) -> bool:
    """Check if a key represents a valid integer index.
    
    Accepts both integer types and string representations of integers.
    Rejects: bool, float, complex, or any other type.
    
    Args:
        key: String or integer to check.
    
    Returns:
        True if key is an integer or can be parsed as an integer, False otherwise.
    
    Examples:
        >>> is_int_key("0")
        True
        >>> is_int_key("-1")
        True
        >>> is_int_key(0)
        True
        >>> is_int_key(-1)
        True
        >>> is_int_key("abc")
        False
        >>> is_int_key("")
        False
        >>> is_int_key(True)  # Not int or string
        False
        >>> is_int_key(3.14)  # Not int or string
        False
    """
    if isinstance(key, int):
        return True
    
    if not isinstance(key, str):
        return False
    
    if not key:  # Empty string
        return False
    
    try:
        int(key)
        return True
    except ValueError:
        return False


def parse_int_key(key: Union[str, int]) -> int:
    """Parse a key into an integer index.
    
    Args:
        key: String representation of an index or an integer.
    
    Returns:
        Integer index.
    
    Raises:
        PathError: If key is a string that cannot be parsed as an integer.
    """
    if isinstance(key, int):
        return key
    
    try:
        return int(key)
    except ValueError:
        raise PathError(f"Invalid list index: '{key}'", PathErrorCode.INVALID_INDEX)


def resolve_read_index(container: Union[list, tuple], key: Union[str, int]) -> Optional[int]:
    """Resolve index for read operations (get_at, exists_at).
    
    Read operations are graceful - out-of-bounds indices return None
    to signal "not found" rather than raising errors.
    
    Args:
        container: The list or tuple to index into.
        key: String representation of the index or an integer.
    
    Returns:
        Resolved positive index, or None if out of bounds.
    
    Raises:
        PathError: If the key is not a valid integer.
    """
    idx = parse_int_key(key)
    
    if idx < 0:
        idx = len(container) + idx
    
    if 0 <= idx < len(container):
        return idx
    
    return None


def resolve_write_index(container: list, key: Union[str, int]) -> int:
    """Resolve index for write operations (set_at).
    
    Write operations have strict semantics to prevent sparse lists:
    - Negative indices must reference existing elements (no extension)
    - Positive indices can only extend by 1 (append operation)
    - Index must be <= len(list) (can append, but not create gaps)
    - Index cannot exceed MAX_LIST_SIZE
    
    Args:
        container: The list to index into.
        key: String representation of the index or an integer.
    
    Returns:
        Resolved positive index.
    
    Raises:
        PathError: If index is out of bounds, would create sparse list,
            exceeds MAX_LIST_SIZE, or key is not a valid integer.
    
    Examples:
        >>> lst = [10, 20, 30]
        >>> resolve_write_index(lst, "3")  # Append
        3
        >>> resolve_write_index(lst, 3)  # Append (integer)
        3
        >>> resolve_write_index(lst, "1")  # Modify existing
        1
        >>> resolve_write_index(lst, "-1")  # Modify last
        2
        >>> resolve_write_index(lst, "5")  # Would create gap
        PathError: Index 5 out of bounds for list of length 3 (no sparse lists)
        >>> resolve_write_index(lst, "-5")  # Negative out of bounds
        PathError: Index -5 out of bounds for list of length 3
    """
    idx = parse_int_key(key)
    length = len(container)
    
    # Check maximum size limit first (before any calculations)
    if idx > MAX_LIST_SIZE:
        raise PathError(
            f"List index {idx} exceeds maximum size {MAX_LIST_SIZE}",
            PathErrorCode.INVALID_INDEX
        )
    
    # Handle negative indices
    if idx < 0:
        resolved = length + idx
        if resolved < 0 or resolved >= length:
            raise PathError(
                f"Index {key} out of bounds for list of length {length}",
                PathErrorCode.INVALID_INDEX
            )
        return resolved
    
    # Handle positive indices - NO SPARSE LISTS
    if idx > length:
        raise PathError(
            f"Index {idx} out of bounds for list of length {length} "
            f"(no sparse lists allowed - index must be <= {length})",
            PathErrorCode.INVALID_INDEX
        )
    
    return idx


def create_intermediate_container(next_key: Union[str, int]) -> Union[dict, list]:
    """Create intermediate container based on next key type.
    
    Logic:
    - If next_key is numeric (int or numeric string) → create list
    - Otherwise → create dict
    
    Args:
        next_key: The next key in the path (string or integer).
    
    Returns:
        Empty list or dict.
    
    Examples:
        >>> create_intermediate_container("0")
        []
        >>> create_intermediate_container(0)
        []
        >>> create_intermediate_container("name")
        {}
        >>> create_intermediate_container("-1")
        []
    """
    return [] if is_int_key(next_key) else {}