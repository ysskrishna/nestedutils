from typing import Any, Union, List
from .exceptions import PathError

def _normalize(path):
    if isinstance(path, list):
        return [str(x) for x in path]
    if isinstance(path, str):
        return path.split(".")
    raise TypeError("path must be string or list")


def _is_int_key(key):
    if key.startswith("-") and key[1:].isdigit():
        return True
    return key.isdigit()


def _get_list_index(container, key: str):
    """Convert key to index (supports negative indices)."""
    try:
        index = int(key)
    except ValueError:
        raise PathError(f"Invalid list index: {key}")

    if index < 0:
        index = len(container) + index
    return index


def _navigate(container, key, default_marker):
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


def get_path(data: Any, path: Union[str, list], default=None) -> Any:
    keys = _normalize(path)
    current = data
    MISSING = object()

    for key in keys:
        current = _navigate(current, key, MISSING)
        if current is MISSING:
            return default
    return current


def set_path(
    data: Any,
    path: Union[str, list],
    value: Any,
    fill_strategy="auto"
):
    """
    fill_strategy:
      - "auto": {} for dicts, [] for lists
      - "none": fill missing list items with None
      - "dict": always fill with {}
      - "list": always fill with []
    """

    keys = _normalize(path)
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
                elif fill_strategy == "none":
                    current[key] = None
                else:  # auto
                    current[key] = [] if _is_int_key(next_key) else {}
            current = current[key]
            continue

        # list case
        if isinstance(current, list):
            if not _is_int_key(key):
                raise PathError(f"Expected index at '{key}'")
            idx = _get_list_index(current, key)

            while len(current) <= idx:
                if fill_strategy == "none":
                    current.append(None)
                elif fill_strategy == "dict":
                    current.append({})
                elif fill_strategy == "list":
                    current.append([])
                else:
                    # auto mode
                    current.append({} if not _is_int_key(next_key) else [])

            current = current[idx]
            continue

        # tuple case = read-only
        if isinstance(current, tuple):
            raise PathError("Cannot modify inside a tuple")

        raise PathError(f"Cannot navigate into type {type(current)} at {key}")

    # final key
    last = keys[-1]

    if isinstance(current, dict):
        current[last] = value
        return

    if isinstance(current, list):
        if not _is_int_key(last):
            raise PathError(f"Expected index at '{last}'")
        idx = _get_list_index(current, last)
        while len(current) <= idx:
            current.append(None)
        current[idx] = value
        return

    raise PathError("Cannot set value in non-container type")


def del_path(data: Any, path: Union[str, list], allow_list_mutation=False):
    keys = _normalize(path)
    current = data

    for key in keys[:-1]:
        if isinstance(current, dict):
            if key not in current:
                raise PathError(f"Missing key {key}")
            current = current[key]
        elif isinstance(current, list):
            if not _is_int_key(key):
                raise PathError(f"Invalid index {key}")
            idx = _get_list_index(current, key)
            try:
                current = current[idx]
            except IndexError:
                raise PathError(f"Missing index {key}")
        else:
            raise PathError(f"Invalid type in path")

    last = keys[-1]

    if isinstance(current, dict):
        if last in current:
            return current.pop(last)
        raise PathError(f"Missing key {last}")

    if isinstance(current, list):
        if not allow_list_mutation:
            raise PathError("List deletion is disabled. Pass allow_list_mutation=True.")
        idx = _get_list_index(current, last)
        try:
            return current.pop(idx)
        except IndexError:
            raise PathError(f"Missing index {last}")

    raise PathError("Cannot delete from non-container type")
