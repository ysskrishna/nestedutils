from typing import Any, List, Union
from .exceptions import PathError
from .enums import PathErrorCode
from .helpers import normalize_path, is_int_key, resolve_write_index, resolve_read_index
from .helpers import create_intermediate_container


_MISSING = object()


def get_at(data: Any, path: Union[str, List[Any]], *, default: Any = _MISSING) -> Any:
    """Retrieve a value from a nested data structure.
    
    Navigates through nested dictionaries, lists, and tuples using a path specified as either
    a dot-notation string or a list of keys/indices. By default, raises PathError if the path
    does not exist. Supports negative indexing for lists and tuples.
    
    This function raises PathError for missing paths by default. Use the `default` parameter
    to return a value instead of raising.
    
    Args:
        data: The data structure to navigate (dict, list, tuple, or nested combinations).
        path: Path to the value. Accepts either a dot-separated string (e.g., "a.b.0.name") or
            a list of keys/indices (e.g., ["a", "b", 0, "name"]). Indices may be integers or
            strings representing integers (including negative indices).
        default: Value to return if the path does not exist. If not provided, raises PathError
            for missing paths.
    
    Returns:
        The value at the specified path, or ``default`` if the path does not exist and
        ``default`` is provided.
    
    Raises:
        PathError: If the path is malformed, empty, contains empty keys, or path doesn't exist
            (when default is not provided).
    
    Examples:
        ```python
        data = {"a": {"b": {"c": 5}}}
        get_at(data, "a.b.c")  # Returns: 5
        
        # Missing paths raise by default
        get_at(data, "a.b.d")  # Raises: PathError
        
        # Explicit default for optional values
        get_at(data, "a.b.d", default=99)  # Returns: 99
        
        data = {"items": [{"name": "apple"}, {"name": "banana"}]}
        get_at(data, "items.1.name")  # Returns: 'banana'
        
        get_at(data, "items.-1.name")  # Returns: 'banana'
        
        get_at(data, "items.-5.name", default="not found")  # Returns: 'not found'
        
        data = (10, 20, 30)
        get_at(data, "-1")  # Returns: 30
        ```
    """
    keys = normalize_path(path)
    current = data
    
    for key in keys:
        if isinstance(current, dict):
            if key not in current:
                if default is not _MISSING:
                    return default
                raise PathError(
                    f"Key '{key}' not found in path",
                    PathErrorCode.MISSING_KEY
                )
            current = current[key]
        
        elif isinstance(current, (list, tuple)):
            if not is_int_key(key):
                if default is not _MISSING:
                    return default
                raise PathError(
                    f"Expected numeric index, got '{key}'",
                    PathErrorCode.INVALID_INDEX
                )
            
            idx = resolve_read_index(current, key)
            if idx is None:
                if default is not _MISSING:
                    return default
                raise PathError(
                    f"Index '{key}' out of bounds in path",
                    PathErrorCode.INVALID_INDEX
                )
            
            current = current[idx]
        
        else:
            if default is not _MISSING:
                return default
            raise PathError(
                f"Cannot navigate into {type(current).__name__} at '{key}'",
                PathErrorCode.NON_NAVIGABLE_TYPE
            )
    
    return current


def exists_at(data: Any, path: Union[str, List[Any]]) -> bool:
    """Check if a path exists in a nested data structure.
    
    Navigates through nested dictionaries, lists, and tuples. Returns True if the full path
    exists and is accessible, False otherwise (including out-of-bounds indices). Supports
    negative indexing for lists and tuples.
    
    This function never raises PathError for missing paths - it returns False instead.
    PathError is only raised for malformed paths.
    
    Args:
        data: The data structure to navigate (dict, list, tuple, or nested combinations).
        path: Path to check. Accepts either a dot-separated string (e.g., "a.b.0.name") or a
            list of keys/indices (e.g., ["a", "b", 0, "name"]).
    
    Returns:
        True if the path exists and is accessible, False otherwise.
    
    Raises:
        PathError: Only if the path format is invalid (empty, malformed, exceeds max depth).
    
    Examples:
        ```python
        data = {"a": {"b": {"c": 5}}}
        exists_at(data, "a.b.c")  # Returns: True
        exists_at(data, "a.b.d")  # Returns: False
        
        data = {"items": [{"name": "apple"}, {"name": "banana"}]}
        exists_at(data, "items.1.name")  # Returns: True
        exists_at(data, "items.-1.name")  # Returns: True
        exists_at(data, "items.-5.name")  # Returns: False
        exists_at(data, "items.10.name")  # Returns: False
        
        data = (10, 20, 30)
        exists_at(data, "2")  # Returns: True
        exists_at(data, "5")  # Returns: False
        
        # Even None values return True if path exists
        data = {"a": {"b": None}}
        exists_at(data, "a.b")  # Returns: True
        exists_at(data, "a.b.c")  # Returns: False (can't navigate into None)
        ```
    """
    try:
        get_at(data, path)  # Uses strict mode internally
        return True
    except PathError as e:
        # Return False for "not found" errors or navigation into non-navigable types
        if e.code in (PathErrorCode.MISSING_KEY, PathErrorCode.INVALID_INDEX, PathErrorCode.NON_NAVIGABLE_TYPE):
            return False
        # Re-raise for path format errors and any other errors
        raise


def set_at(
    data: Any,
    path: Union[str, List[Any]],
    value: Any,
    *,
    create: bool = False
) -> None:
    """Set a value in a nested data structure.
    
    Navigates to the specified path and sets the value. By default (create=False),
    raises PathError if any intermediate key is missing. With create=True, automatically
    creates missing intermediate containers (dicts for string keys, lists for numeric keys).
    
    List indexing rules:
    - Positive indices can append (index == len(list)) but NOT create gaps (index > len(list))
    - Negative indices can only modify existing elements
    - Out-of-bounds negative indices raise PathError
    - Index cannot exceed MAX_LIST_SIZE (10000)
    
    Args:
        data: The mutable data structure to modify (dict or list). The root container
            must already exist and be mutable.
        path: Path where to set the value. Accepts either a dot-separated string (e.g., "a.b.0.name")
            or a list of keys/indices (e.g., ["a", "b", 0, "name"]).
        value: The value to set at the specified path.
        create: If True, automatically create missing intermediate containers.
            If False (default), raise PathError if path doesn't exist.
    
    Returns:
        None. The function modifies ``data`` in place.
    
    Raises:
        PathError: If path is malformed, path doesn't exist (when create=False),
            attempts to modify tuple, uses out-of-bounds negative index, or would
            create sparse list.
    
    Examples:
        ```python
        # create=False (default) - path must exist
        data = {"user": {"profile": {}}}
        set_at(data, "user.profile.name", "Alice")  # OK - path exists
        # data is now: {'user': {'profile': {'name': 'Alice'}}}
        
        data = {}
        set_at(data, "user.name", "Bob")  # PathError - path doesn't exist
        
        # create=True - auto-create missing parts
        data = {}
        set_at(data, "user.profile.name", "Alice", create=True)
        # data is now: {'user': {'profile': {'name': 'Alice'}}}
        
        # List operations - sequential only (no gaps)
        data = {}
        set_at(data, "items.0", "first", create=True)  # OK - creates list
        # data is now: {'items': ['first']}
        
        set_at(data, "items.1", "second", create=True)  # OK - appends
        # data is now: {'items': ['first', 'second']}
        
        set_at(data, "items.5", "x", create=True)  # PathError - would create gap
        
        # Negative indices - modify existing only
        data = {"items": [1, 2, 3]}
        set_at(data, "items.-1", 99)  # OK - modifies last element
        # data is now: {'items': [1, 2, 99]}
        
        set_at(data, "items.-5", 0)  # PathError - out of bounds
        
        # Modifying existing nested structures
        data = {"a": [{"x": 1}]}
        set_at(data, "a.0.y", 2, create=True)  # Adds key to existing dict
        # data is now: {'a': [{'x': 1, 'y': 2}]}
        ```
    """
    keys = normalize_path(path)
    current = data
    
    # Navigate intermediate keys
    for i, key in enumerate(keys[:-1]):
        next_key = keys[i + 1]
        
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
    
    # Set final value
    final_key = keys[-1]
    
    if isinstance(current, dict):
        current[final_key] = value
    
    elif isinstance(current, list):
        if not is_int_key(final_key):
            raise PathError(
                f"Expected numeric index for list, got '{final_key}'",
                PathErrorCode.INVALID_INDEX
            )
        
        idx = resolve_write_index(current, final_key)
        
        # Extend list if appending
        if idx == len(current):
            if not create:
                raise PathError(
                    f"Index {idx} does not exist. Use create=True to append.",
                    PathErrorCode.INVALID_INDEX
                )
            current.append(value)
        else:
            current[idx] = value
    
    elif isinstance(current, tuple):
        raise PathError(
            "Cannot modify tuple (immutable container)",
            PathErrorCode.IMMUTABLE_CONTAINER
        )
    
    else:
        raise PathError(
            f"Cannot set value in {type(current).__name__}",
            PathErrorCode.INVALID_PATH
        )


def delete_at(
    data: Any,
    path: Union[str, List[Any]],
    *,
    allow_list_mutation: bool = False
) -> Any:
    """Delete a value from a nested data structure and return it.
    
    Removes the item at the specified path. For dictionaries, the key-value pair is removed.
    For lists, deletion is disabled by default to prevent accidental index shifting that could
    break subsequent code.
    
    Args:
        data: The mutable data structure to modify (dict or list).
        path: Path to the value to delete. Accepts either a dot-separated string (e.g., "a.b.0")
            or a list of keys/indices (e.g., ["a", "b", 0]).
        allow_list_mutation: If True, allows deletion from lists using ``list.pop()``. Defaults
            to False to prevent unintended side effects.
    
    Returns:
        The deleted value.
    
    Raises:
        PathError: If the path does not exist, is malformed, attempts deletion from a tuple,
            attempts list deletion without ``allow_list_mutation=True``, or uses an out-of-bounds
            index.
    
    Examples:
        ```python
        data = {"a": {"b": 1, "c": 2}}
        delete_at(data, "a.b")  # Returns: 1
        # data is now: {'a': {'c': 2}}
        
        data = {"items": [1, 2, 3]}
        delete_at(data, "items.1", allow_list_mutation=True)  # Returns: 2
        # data is now: {'items': [1, 3]}
        
        delete_at(data, "items.-1", allow_list_mutation=True)  # Returns: 3
        # data is now: {'items': [1]}
        
        # Without allow_list_mutation=True, list deletion raises PathError
        delete_at(data, "items.0")  # Raises: PathError: List deletion disabled...
        ```
    """
    keys = normalize_path(path)
    current = data
    
    # Navigate to parent
    for key in keys[:-1]:
        if isinstance(current, dict):
            if key not in current:
                raise PathError(
                    f"Key not found: '{key}'",
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
                PathErrorCode.INVALID_PATH
            )
    
    # Delete final key
    final_key = keys[-1]
    
    if isinstance(current, dict):
        if final_key not in current:
            raise PathError(
                f"Key not found: '{final_key}'",
                PathErrorCode.MISSING_KEY
            )
        return current.pop(final_key)
    
    elif isinstance(current, list):
        if not allow_list_mutation:
            raise PathError(
                "List deletion disabled. Set allow_list_mutation=True",
                PathErrorCode.INVALID_PATH
            )
        
        if not is_int_key(final_key):
            raise PathError(
                f"Expected numeric index, got '{final_key}'",
                PathErrorCode.INVALID_INDEX
            )
        
        idx = resolve_read_index(current, final_key)
        if idx is None:
            raise PathError(
                f"Index '{final_key}' out of bounds",
                PathErrorCode.INVALID_INDEX
            )
        return current.pop(idx)
    
    elif isinstance(current, tuple):
        raise PathError(
            "Cannot delete from tuple (immutable)",
            PathErrorCode.IMMUTABLE_CONTAINER
        )
    
    else:
        raise PathError(
            f"Cannot delete from {type(current).__name__}",
            PathErrorCode.INVALID_PATH
        )