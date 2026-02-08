# Migration Guide: v1.x to v2.0

This guide helps you upgrade your code from nestedutils v1.x to v2.0. Version 2.0 introduces breaking changes that make the library safer and more predictable.

## Quick Summary of Breaking Changes

| Change | v1.x Behavior | v2.0 Behavior |
|--------|---------------|---------------|
| `get_at` missing path | Returns `None` silently | Raises `PathError` |
| `get_at` default parameter | Could be positional | Must be keyword-only (`default=...`) |
| `set_at` auto-create | `fill_strategy` parameter | `create=False` parameter |
| `set_at` create parameter | N/A (didn't exist) | Must be keyword-only (`create=...`) |
| Sparse lists | Allowed with `None` fill | Not allowed (strict sequential) |
| `FillStrategy` enum | Available | Removed |

---

## 1. `get_at` Now Raises by Default

### The Change

In v1.x, `get_at` silently returned `None` when a path didn't exist. In v2.0, it raises `PathError` by default, making missing data explicit rather than hidden.

### v1.x Code

```python
from nestedutils import get_at

data = {"user": {"name": "Alice"}}

# v1.x: Returns None silently - bugs can hide here!
email = get_at(data, "user.email")  # None
age = get_at(data, "user.profile.age")  # None

# v1.x: default could be passed positionally
value = get_at(data, "missing.path", None)  # None (positional argument)
```

### v2.0 Migration

**Option A: Use `default` parameter for optional values**

```python
from nestedutils import get_at

data = {"user": {"name": "Alice"}}

# Explicit default - clear intent
email = get_at(data, "user.email", default=None)  # None
email = get_at(data, "user.email", default="unknown@example.com")  # fallback value
```

**Option B: Use `exists_at` to check first**

```python
from nestedutils import get_at, exists_at

if exists_at(data, "user.email"):
    email = get_at(data, "user.email")
else:
    email = "default@example.com"
```

**Option C: Use try/except for error handling**

```python
from nestedutils import get_at, PathError

try:
    email = get_at(data, "user.email")
except PathError:
    email = "default@example.com"
```

### Why This Change?

Silent `None` returns masked bugs. Consider:

```python
# v1.x - Bug hidden: typo in path returns None, not an error
user_name = get_at(data, "usr.name")  # None (typo: "usr" vs "user")

# v2.0 - Bug exposed immediately
user_name = get_at(data, "usr.name")  # Raises PathError!
```

---

## 2. `set_at` Parameter Changes

### The Change

The `fill_strategy` parameter has been replaced with a simpler `create` boolean parameter. Sparse list creation is no longer supported. **Important**: Both `get_at`'s `default` and `set_at`'s `create` are now keyword-only parameters (must use `default=...` and `create=...`, not positional arguments).

### v1.x Code

```python
from nestedutils import set_at, FillStrategy

data = {}

# v1.x: Various fill strategies
set_at(data, "user.name", "Alice", fill_strategy=FillStrategy.AUTO)
set_at(data, "items.0", "first", fill_strategy=FillStrategy.AUTO)
set_at(data, "items.5", "sixth", fill_strategy=FillStrategy.NONE)  # Sparse list!

# v1.x: fill_strategy could be passed as string positionally
set_at(data, "user.name", "Alice", "auto")  # Positional argument
```

### v2.0 Migration

```python
from nestedutils import set_at

data = {}

# v2.0: Simple create=True for auto-creation
set_at(data, "user.name", "Alice", create=True)
set_at(data, "items.0", "first", create=True)

# Sparse lists are NO LONGER ALLOWED
# set_at(data, "items.5", "sixth", create=True)  # Raises PathError!

# Must build sequentially
set_at(data, "items.1", "second", create=True)  # OK - appends
```

### FillStrategy Migration Table

| v1.x `fill_strategy` | v2.0 Equivalent |
|----------------------|-----------------|
| `FillStrategy.AUTO` | `create=True` |
| `FillStrategy.NONE` | Not supported (no sparse lists) |
| `FillStrategy.DICT` | `create=True` (inferred from key type) |
| `FillStrategy.LIST` | `create=True` (inferred from key type) |
| Not specified | `create=False` (default, raises on missing) |

### Why This Change?

- Sparse lists (`[None, None, None, "value"]`) caused confusion and bugs
- The `FillStrategy` enum added complexity without proportional benefit
- `create=True/False` is more intuitive and covers most use cases

---

## 3. No More Sparse Lists

### The Change

v1.x allowed creating lists with gaps filled by `None`. v2.0 enforces sequential list building only.

### v1.x Code

```python
from nestedutils import set_at

data = {}
set_at(data, "items.5", "value", fill_strategy=FillStrategy.NONE)
# Result: {"items": [None, None, None, None, None, "value"]}
```

### v2.0 Migration

```python
from nestedutils import set_at

data = {}

# Build lists sequentially
set_at(data, "items.0", "first", create=True)
set_at(data, "items.1", "second", create=True)
set_at(data, "items.2", "third", create=True)
# Result: {"items": ["first", "second", "third"]}

# Or use plain Python for sparse/pre-sized lists
data = {"items": [None] * 6}
set_at(data, "items.5", "value")  # OK - index exists
```

### Why This Change?

Sparse lists often indicate logic errors. If you truly need sparse data, a dict with integer keys is more appropriate:

```python
# Instead of sparse list
data = {"items": {5: "value", 10: "another"}}
```

---

## 4. FillStrategy Enum Removed

### The Change

The `FillStrategy` enum has been removed from the public API.

### v1.x Code

```python
from nestedutils import FillStrategy

strategy = FillStrategy.AUTO
```

### v2.0 Migration

Remove all `FillStrategy` imports and usages. Use `create=True/False` instead.

```python
# v2.0: No FillStrategy import needed
from nestedutils import set_at

set_at(data, "path", value, create=True)
```

---

## 5. New Introspection Functions

v2.0 adds new introspection functions that don't exist in v1.x:

```python
from nestedutils import get_depth, count_leaves, get_all_paths

data = {"a": {"b": 1, "c": 2}, "d": [3, 4]}

get_depth(data)       # 2
count_leaves(data)    # 4
get_all_paths(data)   # [["a", "b"], ["a", "c"], ["d", 0], ["d", 1]]
```

---

## Migration Checklist

- [ ] **Search for `get_at` calls without `default`** - Add `default=None` if silent failure is intended
- [ ] **Update positional `default` arguments** - Change `get_at(data, "path", None)` to `get_at(data, "path", default=None)`
- [ ] **Remove `FillStrategy` imports** - Replace with `create=True/False`
- [ ] **Remove `fill_strategy` parameters** - Replace with `create=True`
- [ ] **Update positional `fill_strategy` arguments** - Change `set_at(data, "path", value, "auto")` to `set_at(data, "path", value, create=True)`
- [ ] **Check for sparse list creation** - Refactor to sequential building or use dicts
- [ ] **Run your test suite** - v2.0's stricter behavior will expose hidden bugs