# Nested Utils

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Tests](https://github.com/ysskrishna/nestedutils/actions/workflows/test.yml/badge.svg)
![Python](https://img.shields.io/badge/python-3.8%2B-blue.svg)
[![PyPI](https://img.shields.io/pypi/v/nestedutils)](https://pypi.org/project/nestedutils/)
[![PyPI Downloads](https://static.pepy.tech/personalized-badge/nestedutils?period=total&units=INTERNATIONAL_SYSTEM&left_color=GREY&right_color=BLUE&left_text=downloads)](https://pepy.tech/projects/nestedutils)
[![Documentation](https://img.shields.io/badge/docs-ysskrishna.github.io%2Fnestedutils-blue.svg)](https://ysskrishna.github.io/nestedutils/)
[![Interactive Playground](https://img.shields.io/badge/demo-Try%20it%20now!-green.svg)](https://ysskrishna.github.io/nestedutils/playground/)

The lightweight Python library for safe, simple, dot-notation access to nested dicts and lists. Effortlessly get, set, and delete values deep in your complex JSON, API responses, and config files without verbose error-checking or handling KeyError exceptions.

> 🚀 **Try it interactively in your browser!** Test the library with our [Interactive Playground](https://ysskrishna.github.io/nestedutils/playground/) - no installation required.

![OG Image](https://raw.githubusercontent.com/ysskrishna/nestedutils/main/media/og.png)

## Why nestedutils?

Working with deeply nested data (like JSON API responses) often leads to verbose, error-prone boilerplate:

```python
# The Standard Way: Verbose and hard to read
user_name = None
if data and "users" in data and len(data["users"]) > 0:
    user = data["users"][0]
    if "profile" in user:
        user_name = user["profile"].get("name")

# With nestedutils: Clean, safe, and readable
from nestedutils import get_at

user_name = get_at(data, "users.0.profile.name")
```

## Features

- **Simple Path Syntax**: Use dot-notation strings (`"a.b.c"`) or lists (`["a", "b", "c"]`) to navigate nested structures
- **Mixed Data Types**: Seamlessly work with dictionaries, lists, and tuples (read-only for tuples)
- **List Index Support**: Access list elements using numeric indices, including negative indices
- **Auto-creation**: Automatically create missing intermediate containers when setting values (with `create=True`)
- **Introspection**: Analyze nested structures with `get_depth`, `count_leaves`, and `get_all_paths`
- **Type Safety**: Comprehensive error handling with descriptive error messages and error codes
- **Safety Limits**: Built-in protection against excessive nesting (max depth: 100) and oversized lists (max index: 10,000)
- **Zero Dependencies**: Pure Python implementation with no external dependencies

## Use Cases

- **JSON API Responses**: Safely extract values from complex, unpredictable JSON responses without dozens of checks.
- **Configuration Management**: Easily read and modify deeply nested settings in configuration dictionaries.
- **Data Transformation**: Rapidly remap data from one complex structure to another using `get_at` and `set_at`.

## Terminology

| Term | Definition |
|------|------------|
| **Path** | A navigation string or list that specifies a location in nested data (e.g., `"user.profile.name"` or `["user", "profile", "name"]`) |
| **Key** | An individual dictionary key used to access a value (e.g., `"name"`, `"profile"`) |
| **Index** | A numeric position in a list or tuple (e.g., `0`, `-1` for last element) |

## Installation

```bash
pip install nestedutils
```

## Quick Start

```python
from nestedutils import get_at, set_at, delete_at, exists_at, get_depth, count_leaves, get_all_paths

# Create a nested structure
data = {}

# Set values using dot-notation
set_at(data, "user.name", "John", create=True)
set_at(data, "user.age", 30, create=True)
set_at(data, "user.hobbies.0", "reading", create=True)
set_at(data, "user.hobbies.1", "coding", create=True)

# Access values
name = get_at(data, "user.name")  # "John"
age = get_at(data, "user.age")    # 30
first_hobby = get_at(data, "user.hobbies.0")  # "reading"

# Check if path exists
if exists_at(data, "user.name"):
    print("User name exists!")

# Delete values
delete_at(data, "user.age")
```

## API Reference

### `get_at(data, path, *, default=None)`

Retrieve a value from a nested data structure.

**Parameters:**

- `data`: The data structure to navigate (dict, list, tuple, or nested combinations)
- `path`: Path to the value (string with dot notation or list of keys/indices)
- `default`: Value to return if path doesn't exist (keyword-only parameter, default: `None`)

**Returns:** The value at the path, or `default` if provided and path doesn't exist

**Raises:** `PathError` if the path doesn't exist and `default` is not provided

**Note:** By default, `get_at` raises `PathError` for missing paths. Use the `default` parameter for optional/nullable access.

**Examples:**

```python
data = {"a": {"b": {"c": 5}}}
get_at(data, "a.b.c")  # 5
get_at(data, "a.b.d")  # Raises PathError (path doesn't exist)
get_at(data, "a.b.d", default=99)  # 99 (returns default)

data = {"items": [{"name": "apple"}, {"name": "banana"}]}
get_at(data, "items.1.name")  # "banana"
get_at(data, "items.-1.name")  # "banana" (negative index)
```

### `set_at(data, path, value, *, create=False)`

Set a value in a nested data structure, optionally creating intermediate containers as needed.

**Parameters:**

- `data`: The data structure to modify (must be mutable: dict or list)
- `path`: Path where to set the value (string with dot notation or list of keys/indices)
- `value`: The value to set
- `create`: If `True`, automatically creates missing intermediate containers (default: `False`)

**Note:** 
- By default (`create=False`), `set_at` raises `PathError` if any intermediate key is missing
- With `create=True`, missing containers are automatically created: `{}` for dict keys, `[]` for list indices
- Positive indices can append to lists (index == len(list)) but cannot create gaps (index > len(list))
- Negative indices can only modify existing elements

**Examples:**

```python
# create=True - auto-create missing containers
data = {}
set_at(data, "user.profile.name", "Alice", create=True)
# Creates: {"user": {"profile": {"name": "Alice"}}}

data = {}
set_at(data, "items.0.name", "Item 1", create=True)
# Creates: {"items": [{"name": "Item 1"}]}

# Sequential list appending (no gaps allowed)
data = {}
set_at(data, "items.0", "first", create=True)  # Creates list with first item
set_at(data, "items.1", "second", create=True)  # Appends second item
# Creates: {"items": ["first", "second"]}

# Sparse lists are NOT allowed - this raises PathError
data = [1, 2, 3]
set_at(data, "5", 99, create=True)  # Raises PathError: cannot create gap

# Negative indices - modify existing only
data = [1, 2, 3]
set_at(data, "-1", 100)  # Updates existing last element
# Creates: [1, 2, 100]
```

### `exists_at(data, path)`

Check if a path exists in a nested data structure.

**Parameters:**

- `data`: The data structure to navigate (dict, list, tuple, or nested combinations)
- `path`: Path to check (string with dot notation or list of keys/indices)

**Returns:** `True` if the path exists, `False` otherwise

**Raises:** `PathError` if the path format is invalid

**Examples:**

```python
data = {"a": {"b": {"c": 5}}}
exists_at(data, "a.b.c")  # True
exists_at(data, "a.b.d")  # False

data = {"items": [{"name": "apple"}, {"name": "banana"}]}
exists_at(data, "items.1.name")  # True
exists_at(data, "items.5.name")  # False
exists_at(data, "items.-1.name")  # True (negative index)
```

### `delete_at(data, path, allow_list_mutation=False)`

Delete a value from a nested data structure.

**Parameters:**

- `data`: The data structure to modify
- `path`: Path to the value to delete
- `allow_list_mutation`: If `True`, allows deletion from lists (default: `False`)

**Note:** List deletion is disabled by default to prevent accidental index shifting that could break subsequent code. When you delete an element from a list, all following indices shift down, which can cause unexpected behavior if other parts of your code reference those indices.

**Returns:** The deleted value

**Raises:** `PathError` if the path doesn't exist or deletion is not allowed

**Examples:**

```python
data = {"a": {"b": 1, "c": 2}}
delete_at(data, "a.b")  # Returns 1, data becomes {"a": {"c": 2}}

data = {"items": [1, 2, 3]}
delete_at(data, "items.1", allow_list_mutation=True)  # Returns 2
# data becomes {"items": [1, 3]}
```

### `get_depth(data)`

Get the maximum nesting depth of a data structure.

**Parameters:**

- `data`: Any nested structure (dict, list, tuple, or primitive)

**Returns:** Integer depth. Primitives return 0, empty containers return 1.

**Note:** Only dict, list, and tuple are traversed. Other container types (set, frozenset, etc.) are treated as leaf values.

**Examples:**

```python
get_depth(42)                          # 0 (primitive)
get_depth({})                          # 1 (empty container)
get_depth({"a": 1})                    # 1 (flat dict)
get_depth({"a": {"b": 1}})             # 2 (nested)
get_depth({"a": {"b": {"c": 1}}})      # 3 (deeper nesting)
get_depth([1, [2, [3]]])               # 3 (nested lists)
```

### `count_leaves(data)`

Count the total number of leaf values (non-container values) in a nested structure.

**Parameters:**

- `data`: Any nested structure

**Returns:** Integer count of leaf values. Empty containers return 0.

**Note:** Only dict, list, and tuple are traversed. Other container types (set, frozenset, etc.) count as a single leaf.

**Examples:**

```python
count_leaves(42)                       # 1 (primitive is a leaf)
count_leaves({})                       # 0 (empty container)
count_leaves({"a": 1, "b": 2})         # 2 (two leaf values)
count_leaves({"a": {"b": 1, "c": 2}})  # 2 (nested, still 2 leaves)
count_leaves([1, 2, [3, 4]])           # 4 (four leaf values)
```

### `get_all_paths(data)`

Get all paths to leaf values in a nested structure.

**Parameters:**

- `data`: Any nested structure

**Returns:** List of paths, where each path is a list of keys (strings) and indices (integers).

**Note:** Only dict, list, and tuple are traversed. Other container types are treated as leaves.

**Examples:**

```python
get_all_paths({"a": 1, "b": 2})
# [["a"], ["b"]]

get_all_paths({"a": {"b": 1, "c": 2}})
# [["a", "b"], ["a", "c"]]

get_all_paths({"users": [{"name": "Alice"}, {"name": "Bob"}]})
# [["users", 0, "name"], ["users", 1, "name"]]

get_all_paths({})                      # [] (no leaves)
get_all_paths(42)                      # [[]] (primitive has empty path)
```

## Error Handling

The library uses `PathError` exceptions with error codes for different failure scenarios:

```python
from nestedutils import PathError, PathErrorCode

try:
    set_at(data, "invalid.path", 1)
except PathError as e:
    print(e.message)  # Error message
    print(e.code)     # Error code (PathErrorCode enum)
```

**Error Codes:**

| Error Code | Description |
|------------|-------------|
| `INVALID_PATH` | Invalid path format or type |
| `INVALID_INDEX` | Invalid list index |
| `MISSING_KEY` | Key doesn't exist in dictionary |
| `EMPTY_PATH` | Path is empty |
| `IMMUTABLE_CONTAINER` | Attempted to modify a tuple |
| `NON_NAVIGABLE_TYPE` | Attempted to navigate into a non-container type |
| `OPERATION_DISABLED` | Operation is disabled by configuration (e.g., list deletion without `allow_list_mutation=True`) |

## Advanced Usage

### Using List Paths

List paths are useful when keys contain dots:

```python
data = {}
set_at(data, ["user.name", "first"], "John", create=True)
set_at(data, ["user.name", "last"], "Doe", create=True)
# Creates: {"user.name": {"first": "John", "last": "Doe"}}
```

### Negative List Indices

Negative indices work like Python list indexing for reading and updating existing elements:

```python
data = {"items": [10, 20, 30]}
get_at(data, "items.-1")  # 30 (last item)
set_at(data, "items.-1", 999)  # Updates last item (must exist)
```

**Important**: Negative indices can only reference existing elements. They cannot extend lists - attempting to use a negative index that's out of bounds will raise a `PathError`.

### Working with Tuples

Tuples are read-only. You can read from them but cannot modify:

```python
data = {"items": (1, 2, 3)}
get_at(data, "items.0")  # 1 (works)
set_at(data, "items.0", 9)  # Raises PathError (tuples are immutable)
```

### Handling None Values

The library can navigate through `None` values when setting:

```python
data = {"a": None}
set_at(data, "a.b.c", 10)
# Replaces None with container: {"a": {"b": {"c": 10}}}
```

## Safety Limits

The library includes built-in safety limits to prevent excessive resource usage:

| Limit | Value | Description |
|-------|-------|-------------|
| **Maximum Path Depth** | 100 levels | Prevents deeply nested paths that could cause stack issues |
| **Maximum List Index** | 10,000 | Prevents creating extremely large sparse lists |

These limits help protect against accidental memory exhaustion or performance issues. If you hit these limits, you'll receive a `PathError` with a clear message.


## Migration from v1.x to v2.0

Version 2.0 introduces breaking changes to make the library safer and more predictable. If you're upgrading from v1.x, please see the [Migration Guide](https://ysskrishna.github.io/nestedutils/migration-v1-to-v2/) for detailed upgrade instructions.

## Contributing

Contributions are welcome! Please read our [Contributing Guide](https://github.com/ysskrishna/nestedutils/blob/main/CONTRIBUTING.md) for details on our code of conduct, development setup, and the process for submitting pull requests.

## Support

If you find this library helpful:

- ⭐ Star the repository
- 🐛 Report issues
- 🔀 Submit pull requests
- 💝 [Sponsor on GitHub](https://github.com/sponsors/ysskrishna)

## License

MIT © [Y. Siva Sai Krishna](https://github.com/ysskrishna) - see [LICENSE](https://github.com/ysskrishna/nestedutils/blob/main/LICENSE) file for details.


---

<p align="left">
  <a href="https://github.com/ysskrishna">Author's GitHub</a> •
  <a href="https://linkedin.com/in/ysskrishna">Author's LinkedIn</a> •
  <a href="https://github.com/ysskrishna/nestedutils/issues">Report Issues</a> •
  <a href="https://pypi.org/project/nestedutils/">Package on PyPI</a> •
  <a href="https://ysskrishna.github.io/nestedutils/">Package Documentation</a> •
  <a href="https://ysskrishna.github.io/nestedutils/playground/">Package Playground</a>
</p>
