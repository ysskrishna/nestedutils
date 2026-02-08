"""Introspection utilities for nested data structures.

This module provides functions to inspect and analyze nested data structures
without modifying them. All functions are pure and support dict, list, and tuple.
Other container types (set, frozenset, deque, etc.) are treated as leaf values.
"""
from typing import Any, List, Union


def get_depth(data: Any) -> int:
    """Return the maximum nesting depth of a nested structure.

    Supports dict, list, and tuple. Other types are treated as leaves (depth 0).

    Args:
        data: Any nested structure (dict, list, tuple, or primitive).

    Returns:
        Integer depth. Primitives return 0, empty containers return 1.

    Examples:
        >>> get_depth(42)
        0
        >>> get_depth({})
        1
        >>> get_depth({"a": 1})
        1
        >>> get_depth({"a": {"b": 1}})
        2
        >>> get_depth({"a": {"b": {"c": 1}}})
        3
        >>> get_depth([1, [2, [3]]])
        3
    """
    if isinstance(data, dict):
        if not data:
            return 1
        return 1 + max(get_depth(v) for v in data.values())

    elif isinstance(data, (list, tuple)):
        if not data:
            return 1
        return 1 + max(get_depth(item) for item in data)

    return 0


def count_leaves(data: Any) -> int:
    """Count the total number of leaf values in a nested structure.

    A leaf is any value that is not a dict, list, or tuple.
    Empty containers count as 0 leaves.

    Supports dict, list, and tuple. Other container types (set, frozenset, etc.)
    are treated as single leaf values.

    Args:
        data: Any nested structure.

    Returns:
        Integer count of leaf values.

    Examples:
        >>> count_leaves(42)
        1
        >>> count_leaves({})
        0
        >>> count_leaves({"a": 1, "b": 2})
        2
        >>> count_leaves({"a": {"b": 1, "c": 2}, "d": 3})
        3
        >>> count_leaves([1, 2, [3, 4]])
        4
    """
    if isinstance(data, dict):
        return sum(count_leaves(v) for v in data.values())

    elif isinstance(data, (list, tuple)):
        return sum(count_leaves(item) for item in data)

    return 1


def get_all_paths(data: Any) -> List[List[Union[str, int]]]:
    """Return all paths to leaf values in a nested structure.

    Supports dict, list, and tuple. Other container types are treated as leaves.

    Args:
        data: Any nested structure.

    Returns:
        List of paths, where each path is a list of keys/indices.

    Examples:
        >>> get_all_paths({"a": 1, "b": 2})
        [["a"], ["b"]]
        >>> get_all_paths({"a": {"b": 1, "c": 2}})
        [["a", "b"], ["a", "c"]]
        >>> get_all_paths({"users": [{"name": "Alice"}, {"name": "Bob"}]})
        [["users", 0, "name"], ["users", 1, "name"]]
        >>> get_all_paths({})
        []
        >>> get_all_paths(42)
        [[]]
    """
    def recurse(current: Any, prefix: List[Union[str, int]]) -> List[List[Union[str, int]]]:
        if isinstance(current, dict):
            if not current:
                return []
            paths = []
            for key, value in current.items():
                paths.extend(recurse(value, prefix + [key]))
            return paths

        elif isinstance(current, (list, tuple)):
            if not current:
                return []
            paths = []
            for idx, item in enumerate(current):
                paths.extend(recurse(item, prefix + [idx]))
            return paths

        return [prefix]

    return recurse(data, [])
