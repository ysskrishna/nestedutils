from typing import Any
from .enums import PathLike
from .exceptions import PathError
from .enums import PathErrorCode, FillStrategy, FillStrategyType
from .helpers import normalize_path, navigate, create_container, fill_list_gaps, ensure_container_at_index
from .helpers import is_int_key, resolve_write_index


def get_at(data: Any, path: PathLike, default: Any = None) -> Any:
    """Retrieve a value from a nested data structure.
    
    Navigates through nested dictionaries, lists, and tuples using a path
    specified as either a dot-notation string or a list of keys/indices.
    Returns a default value if the path doesn't exist, avoiding KeyError
    or IndexError exceptions.
    
    Args:
        data: The data structure to navigate (dict, list, tuple, or nested
            combinations of these types).
        path: Path to the value. Can be a dot-notation string (e.g., "a.b.c")
            or a list of keys/indices (e.g., ["a", "b", "c"]). For lists,
            use numeric indices (e.g., "items.0.name" or "items.-1" for
            negative indexing).
        default: Value to return if path doesn't exist. Defaults to None.
    
    Returns:
        The value at the specified path, or `default` if the path doesn't exist.
    
    Raises:
        PathError: If the path format is invalid (e.g., non-string/list path,
            empty path, or path contains empty keys).
    
    Examples:
        >>> data = {"a": {"b": {"c": 5}}}
        >>> get_at(data, "a.b.c")
        5
        >>> get_at(data, "a.b.d", default=99)
        99
        >>> data = {"items": [{"name": "apple"}, {"name": "banana"}]}
        >>> get_at(data, "items.1.name")
        'banana'
        >>> get_at(data, "items.-1.name")
        'banana'
        >>> get_at(data, "items.-5.name")
        None
        >>> get_at(data, ["items", "0", "name"])
        'apple'
    """
    keys = normalize_path(path)
    current = data
    MISSING = object()
    
    for key in keys:
        current = navigate(current, key, MISSING)
        if current is MISSING:
            return default
    
    return current


def exists_at(data: Any, path: PathLike) -> bool:
    """Check if a path exists in a nested data structure.
    
    Navigates through nested dictionaries, lists, and tuples using a path
    specified as either a dot-notation string or a list of keys/indices.
    Returns True if the path exists, False otherwise. This function does
    not raise exceptions for missing paths.
    
    Behavior for out-of-bounds indices:
    - Negative out-of-bounds (e.g., -5 in list of length 3): Returns False
    - Positive out-of-bounds (e.g., 10 in list of length 3): Returns False
    
    Args:
        data: The data structure to navigate (dict, list, tuple, or nested
            combinations of these types).
        path: Path to check. Can be a dot-notation string (e.g., "a.b.c")
            or a list of keys/indices (e.g., ["a", "b", "c"]). For lists,
            use numeric indices (e.g., "items.0.name" or "items.-1" for
            negative indexing).
    
    Returns:
        True if the path exists, False otherwise.
    
    Raises:
        PathError: If the path format is invalid (e.g., non-string/list path,
            empty path, or path contains empty keys).
    
    Examples:
        >>> data = {"a": {"b": {"c": 5}}}
        >>> exists_at(data, "a.b.c")
        True
        >>> exists_at(data, "a.b.d")
        False
        >>> data = {"items": [{"name": "apple"}, {"name": "banana"}]}
        >>> exists_at(data, "items.1.name")
        True
        >>> exists_at(data, "items.-1.name")
        True
        >>> exists_at(data, "items.-5.name")
        False
        >>> exists_at(data, "items.5.name")
        False
        >>> exists_at(data, ["items", "0", "name"])
        True
    """
    keys = normalize_path(path)
    current = data
    MISSING = object()
    
    for key in keys:
        current = navigate(current, key, MISSING)
        if current is MISSING:
            return False
    
    return True


def set_at(
    data: Any,
    path: PathLike,
    value: Any,
    fill_strategy: FillStrategyType = "auto"
) -> None:
    """Set a value in a nested data structure, creating intermediate containers as needed.
    
    Navigates to the specified path and sets the value, automatically creating
    any missing intermediate dictionaries or lists. Supports flexible fill
    strategies to control how missing containers are created.
    
    Behavior for list indices:
    - Negative indices must reference existing elements (no extension allowed)
    - Positive indices can extend the list, filling gaps with None or containers
    - Out-of-bounds negative indices raise PathError
    
    Args:
        data: The data structure to modify (must be mutable: dict or list).
            The root container must be mutable, but intermediate containers
            will be created as needed.
        path: Path where to set the value. Can be a dot-notation string
            (e.g., "a.b.c") or a list of keys/indices (e.g., ["a", "b", "c"]).
            For lists, use numeric indices (e.g., "items.0.name").
        value: The value to set at the specified path.
        fill_strategy: How to fill missing containers. Must be one of:
            - "auto": Intelligently creates `{}` for dict keys, `[]` for list
              indices, and `None` for sparse list items.
            - "none": Fills missing list items with `None` when creating
              sparse lists.
            - "dict": Always creates dictionaries for missing containers.
            - "list": Always creates lists for missing containers.
            Defaults to "auto".
    
    Returns:
        None. The function modifies `data` in place.
    
    Raises:
        PathError: If the path format is invalid, path is empty, attempting
            to modify a tuple, fill_strategy is invalid, or using out-of-bounds
            negative index.
    
    Examples:
        >>> data = {}
        >>> set_at(data, "user.profile.name", "Alice")
        >>> data
        {'user': {'profile': {'name': 'Alice'}}}
        
        >>> data = {}
        >>> set_at(data, "items.0.name", "Item 1")
        >>> data
        {'items': [{'name': 'Item 1'}]}
        
        >>> data = {}
        >>> set_at(data, "items.5", "Item 6", fill_strategy="none")
        >>> data
        {'items': [None, None, None, None, None, 'Item 6']}
        
        >>> data = {"a": None}
        >>> set_at(data, "a.b.c", 10)
        >>> data
        {'a': {'b': {'c': 10}}}
        
        >>> data = [1, 2, 3]
        >>> set_at(data, "-1", 99)  # Modify existing element
        >>> data
        [1, 2, 99]
        
        >>> data = [1, 2, 3]
        >>> set_at(data, "5", 99)  # Positive extension
        >>> data
        [1, 2, 3, None, None, 99]
    """
    try:
        strategy = FillStrategy(fill_strategy)
    except ValueError:
        valid = {s.value for s in FillStrategy}
        raise PathError(
            f"Invalid fill_strategy: {fill_strategy}. Valid: {valid}",
            PathErrorCode.INVALID_FILL_STRATEGY
        )
    
    keys = normalize_path(path)
    current = data
    
    # Navigate intermediate keys
    for i, key in enumerate(keys[:-1]):
        next_key = keys[i + 1]
        
        if isinstance(current, dict):
            if key not in current or current[key] is None:
                current[key] = create_container(strategy, next_key)
            current = current[key]
        
        elif isinstance(current, list):
            if not is_int_key(key):
                raise PathError(
                    f"Expected numeric index, got '{key}'",
                    PathErrorCode.INVALID_INDEX
                )
            
            idx = resolve_write_index(current, key, allow_extension=True)
            fill_list_gaps(current, idx, strategy)
            ensure_container_at_index(current, idx, strategy, next_key)
            current = current[idx]
        
        elif isinstance(current, tuple):
            raise PathError(
                "Cannot modify tuple (immutable)",
                PathErrorCode.IMMUTABLE_CONTAINER
            )
        
        else:
            raise PathError(
                f"Cannot navigate into {type(current).__name__}",
                PathErrorCode.INVALID_PATH
            )
    
    # Set final value
    final_key = keys[-1]
    
    if isinstance(current, dict):
        current[final_key] = value
    
    elif isinstance(current, list):
        if not is_int_key(final_key):
            raise PathError(
                f"Expected numeric index, got '{final_key}'",
                PathErrorCode.INVALID_INDEX
            )
        
        idx = resolve_write_index(current, final_key, allow_extension=True)
        
        while len(current) <= idx:
            current.append(None)
        
        current[idx] = value
    
    elif isinstance(current, tuple):
        raise PathError(
            "Cannot modify tuple (immutable)",
            PathErrorCode.IMMUTABLE_CONTAINER
        )
    
    else:
        raise PathError(
            f"Cannot set value in {type(current).__name__}",
            PathErrorCode.INVALID_PATH
        )


def delete_at(
    data: Any,
    path: PathLike,
    *,
    allow_list_mutation: bool = False
) -> Any:
    """Delete a value from a nested data structure.
    
    Removes the value at the specified path from the data structure and returns
    the deleted value. For dictionaries, the key-value pair is removed. For
    lists, deletion is disabled by default to prevent accidental mutations.
    
    Args:
        data: The data structure to modify (must be mutable: dict or list).
        path: Path to the value to delete. Can be a dot-notation string
            (e.g., "a.b.c") or a list of keys/indices (e.g., ["a", "b", "c"]).
            For lists, use numeric indices (e.g., "items.0").
        allow_list_mutation: If True, allows deletion from lists using `pop()`.
            If False (default), raises PathError when attempting to delete
            from a list. This prevents accidental list mutations that shift indices.
    
    Returns:
        The deleted value that was removed from the data structure.
    
    Raises:
        PathError: If the path doesn't exist, path format is invalid, attempting
            to delete from a list without `allow_list_mutation=True`, attempting
            to delete from a tuple, or index is out of bounds.
    
    Examples:
        >>> data = {"a": {"b": 1, "c": 2}}
        >>> delete_at(data, "a.b")
        1
        >>> data
        {'a': {'c': 2}}
        
        >>> data = {"items": [1, 2, 3]}
        >>> delete_at(data, "items.1", allow_list_mutation=True)
        2
        >>> data
        {'items': [1, 3]}
        
        >>> data = {"items": [1, 2, 3]}
        >>> delete_at(data, "items.-1", allow_list_mutation=True)
        3
        >>> data
        {'items': [1, 2]}
        
        >>> data = {"items": [1, 2, 3]}
        >>> delete_at(data, "items.1")
        Traceback (most recent call last):
        ...
        PathError: List deletion disabled. Set allow_list_mutation=True
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
            
            idx = resolve_write_index(current, key, allow_extension=False)
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
        
        idx = resolve_write_index(current, final_key, allow_extension=False)
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