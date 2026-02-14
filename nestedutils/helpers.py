from typing import Any, List, Union, Optional
from nestedutils.exceptions import PathError
from nestedutils.enums import PathErrorCode
from nestedutils.constants import MAX_DEPTH, MAX_LIST_SIZE


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


MISSING = object()


def navigate_dict_key(
    current: dict,
    key: Union[str, int],
    *,
    default: Any = MISSING,
    raise_on_missing: bool = True
) -> Any:
    """Navigate into a dictionary using a key.
    
    Args:
        current: The dictionary to navigate into.
        key: The key to access.
        default: Value to return if key is missing (when not MISSING).
        raise_on_missing: Whether to raise PathError on missing key.
    
    Returns:
        The value at the key, or default if provided and key is missing.
    
    Raises:
        PathError: If key is missing and raise_on_missing is True and default is MISSING.
    """
    if key not in current:
        if default is not MISSING:
            return default
        if raise_on_missing:
            raise PathError(
                f"Key '{key}' not found",
                PathErrorCode.MISSING_KEY
            )
        return None
    return current[key]


def navigate_sequence_index(
    current: Union[list, tuple],
    key: Union[str, int],
    *,
    default: Any = MISSING,
    raise_on_missing: bool = True
) -> Any:
    """Navigate into a list or tuple using an index.
    
    Args:
        current: The list or tuple to navigate into.
        key: The index to access.
        default: Value to return if index is out of bounds (when not MISSING).
        raise_on_missing: Whether to raise PathError on out-of-bounds index.
    
    Returns:
        The value at the index, or default if provided and index is out of bounds.
    
    Raises:
        PathError: If key is not a valid integer, or index is out of bounds and
            raise_on_missing is True and default is MISSING.
    """
    if not is_int_key(key):
        if default is not MISSING:
            return default
        if raise_on_missing:
            raise PathError(
                f"Expected numeric index, got '{key}'",
                PathErrorCode.INVALID_INDEX
            )
        return None
    
    idx = resolve_read_index(current, key)
    if idx is None:
        if default is not MISSING:
            return default
        if raise_on_missing:
            raise PathError(
                f"Index '{key}' out of bounds in path",
                PathErrorCode.INVALID_INDEX
            )
        return None
    
    return current[idx]


def navigate_one_step(
    current: Any,
    key: Union[str, int],
    *,
    default: Any = MISSING,
    raise_on_missing: bool = True
) -> Any:
    """Navigate one step into a nested structure.
    
    Handles dict, list, tuple, and other types.
    
    Args:
        current: The current value in the nested structure.
        key: The key or index to navigate with.
        default: Value to return if navigation fails (when not MISSING).
        raise_on_missing: Whether to raise PathError on navigation failure.
    
    Returns:
        The next value in the navigation path, or default if provided and navigation fails.
    
    Raises:
        PathError: If navigation fails and raise_on_missing is True and default is MISSING.
    """
    if isinstance(current, dict):
        return navigate_dict_key(current, key, default=default, raise_on_missing=raise_on_missing)
    
    elif isinstance(current, (list, tuple)):
        return navigate_sequence_index(current, key, default=default, raise_on_missing=raise_on_missing)
    
    else:
        if default is not MISSING:
            return default
        if raise_on_missing:
            raise PathError(
                f"Cannot navigate into {type(current).__name__} at '{key}'",
                PathErrorCode.NON_NAVIGABLE_TYPE
            )
        return None


def navigate_to_parent(
    data: Any,
    intermediate_keys: List[Union[str, int]],
    final_key: Union[str, int],
    *,
    create: bool = False
) -> Any:
    """Navigate to the parent container of the final key.
    
    For intermediate keys, creates containers if create=True. When create=True,
    this function will also replace None values with appropriate containers (dict
    or list) based on the next key type, allowing navigation through None values.
    
    Args:
        data: The root data structure.
        intermediate_keys: List of intermediate keys to navigate through.
        final_key: The final key (used to determine container type for last intermediate).
        create: If True, automatically create missing intermediate containers and
            replace None values with containers.
    
    Returns:
        The parent container of the final key.
    
    Raises:
        PathError: If path doesn't exist and create=False, or if attempting
            to modify tuple, or other navigation errors.
    """
    current = data
    
    # Navigate intermediate keys
    for i, key in enumerate(intermediate_keys):
        next_key = intermediate_keys[i + 1] if i + 1 < len(intermediate_keys) else final_key
        
        if isinstance(current, dict):
            if key not in current:
                if not create:
                    raise PathError(
                        f"Key '{key}' does not exist. Use create=True to auto-create path.",
                        PathErrorCode.MISSING_KEY
                    )
                # Create intermediate container based on next key type
                current[key] = create_intermediate_container(next_key)
            elif current[key] is None:
                if not create:
                    raise PathError(
                        f"Key '{key}' is None. Use create=True to replace with container.",
                        PathErrorCode.MISSING_KEY
                    )
                current[key] = create_intermediate_container(next_key)
            
            current = current[key]
        
        elif isinstance(current, list):
            if not is_int_key(key):
                raise PathError(
                    f"Expected numeric index for list, got '{key}'",
                    PathErrorCode.INVALID_INDEX
                )
            
            idx = resolve_write_index(current, key)
            
            # Extend list if needed (only for append, not gaps)
            if idx == len(current):
                if not create:
                    raise PathError(
                        f"Index {idx} does not exist. Use create=True to append.",
                        PathErrorCode.INVALID_INDEX
                    )
                current.append(create_intermediate_container(next_key))
            elif current[idx] is None:
                if not create:
                    raise PathError(
                        f"Index {idx} is None. Use create=True to replace with container.",
                        PathErrorCode.MISSING_KEY
                    )
                current[idx] = create_intermediate_container(next_key)
            
            current = current[idx]
        
        elif isinstance(current, tuple):
            raise PathError(
                "Cannot modify tuple (immutable container)",
                PathErrorCode.IMMUTABLE_CONTAINER
            )
        
        else:
            raise PathError(
                f"Cannot navigate into {type(current).__name__}",
                PathErrorCode.NON_NAVIGABLE_TYPE
            )
    
    return current


def set_final_value(
    parent: Union[dict, list],
    key: Union[str, int],
    value: Any,
    *,
    create: bool = False
) -> None:
    """Set the final value at the given key in parent container.
    
    Handles dict assignment and list append/modify logic.
    
    Args:
        parent: The parent container (dict or list).
        key: The key or index to set.
        value: The value to set.
        create: If True, allow appending to lists.
    
    Raises:
        PathError: If setting fails (e.g., out of bounds, immutable container).
    """
    if isinstance(parent, dict):
        parent[key] = value
    
    elif isinstance(parent, list):
        if not is_int_key(key):
            raise PathError(
                f"Expected numeric index for list, got '{key}'",
                PathErrorCode.INVALID_INDEX
            )
        
        idx = resolve_write_index(parent, key)
        
        # Extend list if appending
        if idx == len(parent):
            if not create:
                raise PathError(
                    f"Index {idx} does not exist. Use create=True to append.",
                    PathErrorCode.INVALID_INDEX
                )
            parent.append(value)
        else:
            parent[idx] = value
    
    elif isinstance(parent, tuple):
        raise PathError(
            "Cannot modify tuple (immutable container)",
            PathErrorCode.IMMUTABLE_CONTAINER
        )
    
    else:
        raise PathError(
            f"Cannot set value in {type(parent).__name__}",
            PathErrorCode.NON_NAVIGABLE_TYPE
        )


def navigate_to_parent_for_delete(
    data: Any,
    keys: List[Union[str, int]]
) -> Any:
    """Navigate to the parent container of the final key for deletion.
    
    Raises PathError if any intermediate key is missing.
    
    Args:
        data: The root data structure.
        keys: List of keys to navigate through (excluding final key).
    
    Returns:
        The parent container of the final key.
    
    Raises:
        PathError: If any intermediate key is missing or navigation fails.
    """
    current = data
    
    for key in keys:
        if isinstance(current, dict):
            if key not in current:
                raise PathError(
                    f"Key '{key}' not found",
                    PathErrorCode.MISSING_KEY
                )
            current = current[key]
        
        elif isinstance(current, (list, tuple)):
            if not is_int_key(key):
                raise PathError(
                    f"Expected numeric index, got '{key}'",
                    PathErrorCode.INVALID_INDEX
                )
            
            idx = resolve_read_index(current, key)
            if idx is None:
                raise PathError(
                    f"Index '{key}' out of bounds",
                    PathErrorCode.INVALID_INDEX
                )
            current = current[idx]
        
        else:
            raise PathError(
                f"Cannot navigate through {type(current).__name__}",
                PathErrorCode.NON_NAVIGABLE_TYPE
            )
    
    return current


def delete_from_container(
    parent: Union[dict, list],
    key: Union[str, int],
    *,
    allow_list_mutation: bool = False
) -> Any:
    """Delete and return value from parent container.
    
    Handles dict.pop() and list.pop() with validation.
    
    Args:
        parent: The parent container (dict or list).
        key: The key or index to delete.
        allow_list_mutation: If True, allows deletion from lists.
    
    Returns:
        The deleted value.
    
    Raises:
        PathError: If deletion fails (e.g., key not found, immutable container,
            list mutation disabled).
    """
    if isinstance(parent, dict):
        if key not in parent:
            raise PathError(
                f"Key '{key}' not found",
                PathErrorCode.MISSING_KEY
            )
        return parent.pop(key)
    
    elif isinstance(parent, list):
        if not allow_list_mutation:
            raise PathError(
                "List deletion disabled. Set allow_list_mutation=True",
                PathErrorCode.OPERATION_DISABLED
            )
        
        if not is_int_key(key):
            raise PathError(
                f"Expected numeric index, got '{key}'",
                PathErrorCode.INVALID_INDEX
            )
        
        idx = resolve_read_index(parent, key)
        if idx is None:
            raise PathError(
                f"Index '{key}' out of bounds",
                PathErrorCode.INVALID_INDEX
            )
        return parent.pop(idx)
    
    elif isinstance(parent, tuple):
        raise PathError(
            "Cannot delete from tuple (immutable)",
            PathErrorCode.IMMUTABLE_CONTAINER
        )
    
    else:
        raise PathError(
            f"Cannot delete from {type(parent).__name__}",
            PathErrorCode.NON_NAVIGABLE_TYPE
        )