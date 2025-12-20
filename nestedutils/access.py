from typing import Any, Union, List
from .exceptions import PathError, PathErrorCode

def _normalize(path: Union[str, List[Any]]) -> List[str]:
    if isinstance(path, list):
        return [str(x) for x in path]
    if isinstance(path, str):
        return path.split(".")
    raise PathError(f"path must be string or list, got {type(path).__name__}", PathErrorCode.INVALID_PATH)


def _is_int_key(key: str) -> bool:
    if key.startswith("-") and key[1:].isdigit():
        return True
    return key.isdigit()


def _get_list_index(container: Union[List[Any], tuple], key: str) -> int:
    """Convert key to index (supports negative indices)."""
    try:
        index = int(key)
    except ValueError:
        raise PathError(f"Invalid list index: {key}", PathErrorCode.INVALID_INDEX)

    if index < 0:
        index = len(container) + index
    return index


def _navigate(container: Any, key: str, default_marker: Any) -> Any:
    """Unified navigation for dict/list/tuple."""
    if isinstance(container, dict):
        return container.get(key, default_marker)

    if isinstance(container, (list, tuple)):
        if not _is_int_key(key):
            return default_marker
        idx = _get_list_index(container, key)
        if 0 <= idx < len(container):
            return container[idx]
        return default_marker

    return default_marker


def get_at(data: Any, path: Union[str, List[Any]], default: Any = None) -> Any:
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
        PathError: If the path format is invalid (e.g., non-string/list path).
    
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
        >>> get_at(data, ["items", "0", "name"])
        'apple'
    """
    keys = _normalize(path)
    current = data
    MISSING = object()

    for key in keys:
        current = _navigate(current, key, MISSING)
        if current is MISSING:
            return default
    return current


def set_at(
    data: Any,
    path: Union[str, List[Any]],
    value: Any,
    fill_strategy: str = "auto"
) -> None:
    """Set a value in a nested data structure, creating intermediate containers as needed.
    
    Navigates to the specified path and sets the value, automatically creating
    any missing intermediate dictionaries or lists. Supports flexible fill
    strategies to control how missing containers are created.
    
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
            to modify a tuple, or fill_strategy is invalid.
    
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
    """
    # Validate fill_strategy
    valid_strategies = {"auto", "none", "dict", "list"}
    if fill_strategy not in valid_strategies:
        raise PathError(f"Invalid fill_strategy: {fill_strategy}. Must be one of {valid_strategies}", PathErrorCode.INVALID_FILL_STRATEGY)

    keys = _normalize(path)
    
    # Validate path is not empty
    if not keys or (len(keys) == 1 and keys[0] == ""):
        raise PathError("Path cannot be empty", PathErrorCode.EMPTY_PATH)
    
    current = data

    for i, key in enumerate(keys[:-1]):
        next_key = keys[i + 1]

        # dict case
        if isinstance(current, dict):
            if key not in current:
                if fill_strategy == "dict":
                    current[key] = {}
                elif fill_strategy == "list":
                    current[key] = []
                else:  # auto or none - both intelligently create containers
                    current[key] = [] if _is_int_key(next_key) else {}
            elif current[key] is None:
                # Replace None with appropriate container when navigating deeper
                if fill_strategy == "dict":
                    current[key] = {}
                elif fill_strategy == "list":
                    current[key] = []
                else:  # auto or none
                    current[key] = [] if _is_int_key(next_key) else {}
            current = current[key]
            continue

        # list case
        if isinstance(current, list):
            if not _is_int_key(key):
                raise PathError(f"Expected index at '{key}'", PathErrorCode.INVALID_INDEX)
            idx = _get_list_index(current, key)

            # Fill gaps before the target index
            while len(current) < idx:
                if fill_strategy == "dict":
                    current.append({})
                elif fill_strategy == "list":
                    current.append([])
                else:
                    # auto or none - fill sparse list items with None
                    current.append(None)
            
            # Now create the container at the target index if needed
            if len(current) == idx:
                if fill_strategy == "dict":
                    current.append({})
                elif fill_strategy == "list":
                    current.append([])
                else:
                    # auto or none - create container based on next key
                    current.append([] if _is_int_key(next_key) else {})
            elif current[idx] is None:
                # Replace None with appropriate container when navigating deeper
                if fill_strategy == "dict":
                    current[idx] = {}
                elif fill_strategy == "list":
                    current[idx] = []
                else:  # auto or none
                    current[idx] = [] if _is_int_key(next_key) else {}

            current = current[idx]
            continue

        # tuple case = read-only
        if isinstance(current, tuple):
            raise PathError("Cannot modify inside a tuple", PathErrorCode.IMMUTABLE_CONTAINER)

        raise PathError(f"Cannot navigate into type {type(current)} at {key}", PathErrorCode.INVALID_PATH)

    # final key
    last = keys[-1]

    if isinstance(current, dict):
        current[last] = value
        return

    if isinstance(current, list):
        if not _is_int_key(last):
            raise PathError(f"Expected index at '{last}'", PathErrorCode.INVALID_INDEX)
        idx = _get_list_index(current, last)
        while len(current) <= idx:
            current.append(None)
        current[idx] = value
        return

    if isinstance(current, tuple):
        raise PathError("Cannot modify inside a tuple", PathErrorCode.IMMUTABLE_CONTAINER)

    raise PathError("Cannot set value in non-container type", PathErrorCode.INVALID_PATH)


def delete_at(data: Any, path: Union[str, List[Any]], allow_list_mutation: bool = False) -> Any:
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
            from a list. This prevents accidental list mutations.
    
    Returns:
        The deleted value that was removed from the data structure.
    
    Raises:
        PathError: If the path doesn't exist, path format is invalid, attempting
            to delete from a list without `allow_list_mutation=True`, or
            attempting to delete from a non-container type.
    
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
        >>> delete_at(data, "items.1")
        Traceback (most recent call last):
        ...
        PathError: List deletion is disabled. Pass allow_list_mutation=True.
    """
    keys = _normalize(path)
    current = data

    for key in keys[:-1]:
        if isinstance(current, dict):
            if key not in current:
                raise PathError(f"Missing key {key}", PathErrorCode.MISSING_KEY)
            current = current[key]
        elif isinstance(current, list):
            if not _is_int_key(key):
                raise PathError(f"Invalid index {key}", PathErrorCode.INVALID_INDEX)
            idx = _get_list_index(current, key)
            try:
                current = current[idx]
            except IndexError:
                raise PathError(f"Missing index {key}", PathErrorCode.INVALID_INDEX)
        else:
            raise PathError(f"Invalid type in path", PathErrorCode.INVALID_PATH)

    last = keys[-1]

    if isinstance(current, dict):
        if last in current:
            return current.pop(last)
        raise PathError(f"Missing key {last}", PathErrorCode.MISSING_KEY)

    if isinstance(current, list):
        if not allow_list_mutation:
            raise PathError("List deletion is disabled. Pass allow_list_mutation=True.", PathErrorCode.INVALID_PATH)
        idx = _get_list_index(current, last)
        try:
            return current.pop(idx)
        except IndexError:
            raise PathError(f"Missing index {last}", PathErrorCode.INVALID_INDEX)

    raise PathError("Cannot delete from non-container type", PathErrorCode.INVALID_PATH)
