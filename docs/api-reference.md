---
title: API Reference

description: "Complete API reference for nestedutils. Documentation for get_at, set_at, delete_at, exists_at, get_depth, count_leaves, and get_all_paths functions with parameters, return values, examples, and error handling."

keywords:
  - nestedutils API
  - API reference
  - get_at
  - set_at
  - delete_at
  - exists_at
  - get_depth
  - count_leaves
  - get_all_paths
  - function documentation
  - nested data functions
  - Python API
  - function parameters
  - examples
  - error codes
---

<!-- ### Core Functions -->

::: nestedutils.access
    options:
      show_root_heading: true
      show_root_toc_entry: false
      members:
        - get_at
        - set_at
        - delete_at
        - exists_at
      heading_level: 3

::: nestedutils.introspection
    options:
      show_root_heading: true
      show_root_toc_entry: false
      members:
        - get_depth
        - count_leaves
        - get_all_paths
      heading_level: 3

::: nestedutils.constants
    options:
      show_root_heading: true
      show_source: false
      heading_level: 3
      members:
        - MAX_DEPTH
        - MAX_LIST_SIZE
      members_order: source

::: nestedutils.enums
    options:
      show_root_heading: true
      show_source: false
      heading_level: 3
      members:
        - PathErrorCode
      members_order: source
      show_if_no_docstring: true

::: nestedutils.exceptions
    options:
      show_root_heading: true
      show_source: false
      heading_level: 3
      members:
        - PathError
      members_order: source

