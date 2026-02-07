from typing import Any, List, Union, Optional
from .exceptions import PathError
from .enums import PathErrorCode
from .constants import MAX_DEPTH, MAX_LIST_SIZE


def normalize_path(path: Union[str, List[Any]]) -> List[str]:
    """Normalize path to list of strings and validate.
    
    Converts path to a list of string keys, validating that:
    - Path is not empty
    - No keys in the path are empty strings
    - Path depth does not exceed MAX_DEPTH
    
    Args:
        path: Either a dot-notation string (e.g., "a.b.c") or a list of keys.
    
    Returns:
        List of string keys representing the path. All elements are guaranteed to be strings.
    
    Raises:
        PathError: If path format is invalid, path is empty, contains empty keys,
            or exceeds maximum depth.
    """
    if isinstance(path, list):
        # Convert all list elements to strings
        keys = [str(key) for key in path]
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
    
    if any(key == "" for key in keys):
        raise PathError("Path cannot contain empty keys", PathErrorCode.EMPTY_PATH)
    
    return keys


def is_int_key(key: str) -> bool:
    """Check if a key represents a valid integer index.
    
    STRICT CHECKING: Only accepts string representations of integers.
    Rejects: bool, float, complex, or any other type.
    
    Args:
        key: String to check.
    
    Returns:
        True if key can be parsed as an integer, False otherwise.
    
    Examples:
        >>> is_int_key("0")
        True
        >>> is_int_key("-1")
        True
        >>> is_int_key("abc")
        False
        >>> is_int_key("")
        False
        >>> is_int_key(True)  # Not a string
        False
        >>> is_int_key(3.14)  # Not a string
        False
    """
    if not isinstance(key, str):
        return False
    
    if not key:  # Empty string
        return False
    
    try:
        int(key)
        return True
    except ValueError:
        return False


def parse_int_key(key: str) -> int:
    """Parse a string key into an integer index.
    
    Args:
        key: String representation of an index.
    
    Returns:
        Parsed integer index.
    
    Raises:
        PathError: If key cannot be parsed as an integer.
    """
    try:
        return int(key)
    except ValueError:
        raise PathError(f"Invalid list index: '{key}'", PathErrorCode.INVALID_INDEX)


def resolve_read_index(container: Union[list, tuple], key: str) -> Optional[int]:
    """Resolve index for read operations (get_at, exists_at).
    
    Read operations are graceful - out-of-bounds indices return None
    to signal "not found" rather than raising errors.
    
    Args:
        container: The list or tuple to index into.
        key: String representation of the index.
    
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


def resolve_write_index(container: list, key: str) -> int:
    """Resolve index for write operations (set_at).
    
    Write operations have strict semantics to prevent sparse lists:
    - Negative indices must reference existing elements (no extension)
    - Positive indices can only extend by 1 (append operation)
    - Index must be <= len(list) (can append, but not create gaps)
    - Index cannot exceed MAX_LIST_SIZE
    
    Args:
        container: The list to index into.
        key: String representation of the index.
    
    Returns:
        Resolved positive index.
    
    Raises:
        PathError: If index is out of bounds, would create sparse list,
            exceeds MAX_LIST_SIZE, or key is not a valid integer.
    
    Examples:
        >>> lst = [10, 20, 30]
        >>> resolve_write_index(lst, "3")  # Append
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


def navigate(container: Any, key: str, default: Any) -> Any:
    """Navigate one level into a container.
    
    Used by read operations (get_at, exists_at). Returns default
    for any navigation failures rather than raising exceptions.
    
    Args:
        container: Container to navigate into (dict, list, or tuple).
        key: Key or index to access.
        default: Sentinel value to return on failure.
    
    Returns:
        The value at the key, or default if navigation fails.
    """
    if isinstance(container, dict):
        return container.get(key, default)
    
    if isinstance(container, (list, tuple)):
        if not is_int_key(key):
            return default
        
        idx = resolve_read_index(container, key)
        if idx is None:
            return default
        
        return container[idx]
    
    return default


def create_intermediate_container(next_key: str) -> Union[dict, list]:
    """Create intermediate container based on next key type.
    
    Logic:
    - If next_key is numeric → create list
    - Otherwise → create dict
    
    Args:
        next_key: The next key in the path.
    
    Returns:
        Empty list or dict.
    
    Examples:
        >>> create_intermediate_container("0")
        []
        >>> create_intermediate_container("name")
        {}
        >>> create_intermediate_container("-1")
        []
    """
    return [] if is_int_key(next_key) else {}