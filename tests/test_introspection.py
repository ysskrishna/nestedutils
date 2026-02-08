import pytest
from nestedutils import get_depth, count_leaves, get_all_paths


class TestGetDepth:
    """Tests for get_depth function."""

    def test_primitive_values(self):
        """Primitives have depth 0."""
        assert get_depth(42) == 0
        assert get_depth("string") == 0
        assert get_depth(3.14) == 0
        assert get_depth(True) == 0
        assert get_depth(None) == 0

    def test_empty_containers(self):
        """Empty containers have depth 1."""
        assert get_depth({}) == 1
        assert get_depth([]) == 1
        assert get_depth(()) == 1

    def test_flat_dict(self):
        """Flat dict with primitives has depth 1."""
        assert get_depth({"a": 1}) == 1
        assert get_depth({"a": 1, "b": 2, "c": 3}) == 1

    def test_flat_list(self):
        """Flat list with primitives has depth 1."""
        assert get_depth([1, 2, 3]) == 1
        assert get_depth([1]) == 1

    def test_nested_dict(self):
        """Nested dicts increase depth."""
        assert get_depth({"a": {"b": 1}}) == 2
        assert get_depth({"a": {"b": {"c": 1}}}) == 3
        assert get_depth({"a": {"b": {"c": {"d": 1}}}}) == 4

    def test_nested_list(self):
        """Nested lists increase depth."""
        assert get_depth([[1]]) == 2
        assert get_depth([[[1]]]) == 3
        assert get_depth([1, [2, [3]]]) == 3

    def test_mixed_nesting(self):
        """Mixed dict and list nesting."""
        assert get_depth({"a": [1, 2]}) == 2
        assert get_depth([{"a": 1}]) == 2
        assert get_depth({"a": [{"b": 1}]}) == 3
        assert get_depth({"users": [{"profile": {"name": "Alice"}}]}) == 4

    def test_uneven_depth(self):
        """Returns maximum depth when branches have different depths."""
        data = {
            "shallow": 1,
            "deep": {"nested": {"value": 1}}
        }
        assert get_depth(data) == 3

    def test_tuple_support(self):
        """Tuples are treated like lists."""
        assert get_depth((1, 2, 3)) == 1
        assert get_depth({"a": (1, 2)}) == 2
        assert get_depth(({"a": 1}, {"b": 2})) == 2

    def test_set_treated_as_leaf(self):
        """Sets are treated as leaf values (depth 0)."""
        assert get_depth({1, 2, 3}) == 0
        assert get_depth({"a": {1, 2, 3}}) == 1


class TestCountLeaves:
    """Tests for count_leaves function."""

    def test_primitive_values(self):
        """Primitives count as 1 leaf."""
        assert count_leaves(42) == 1
        assert count_leaves("string") == 1
        assert count_leaves(3.14) == 1
        assert count_leaves(True) == 1
        assert count_leaves(None) == 1

    def test_empty_containers(self):
        """Empty containers have 0 leaves."""
        assert count_leaves({}) == 0
        assert count_leaves([]) == 0
        assert count_leaves(()) == 0

    def test_flat_dict(self):
        """Flat dict counts each value as a leaf."""
        assert count_leaves({"a": 1}) == 1
        assert count_leaves({"a": 1, "b": 2}) == 2
        assert count_leaves({"a": 1, "b": 2, "c": 3}) == 3

    def test_flat_list(self):
        """Flat list counts each element as a leaf."""
        assert count_leaves([1]) == 1
        assert count_leaves([1, 2, 3]) == 3
        assert count_leaves([1, 2, 3, 4, 5]) == 5

    def test_nested_dict(self):
        """Nested dicts still count only leaf values."""
        assert count_leaves({"a": {"b": 1}}) == 1
        assert count_leaves({"a": {"b": 1, "c": 2}}) == 2
        assert count_leaves({"a": {"b": 1}, "d": 2}) == 2

    def test_nested_list(self):
        """Nested lists still count only leaf values."""
        assert count_leaves([[1]]) == 1
        assert count_leaves([[1, 2], [3]]) == 3
        assert count_leaves([1, [2, [3, 4]]]) == 4

    def test_mixed_nesting(self):
        """Mixed dict and list nesting."""
        data = {
            "a": {"b": 1, "c": 2},
            "d": [3, 4, 5],
            "e": 6
        }
        assert count_leaves(data) == 6

    def test_complex_structure(self):
        """Complex nested structure."""
        data = {
            "users": [
                {"name": "Alice", "age": 30},
                {"name": "Bob", "age": 25}
            ],
            "meta": {"count": 2}
        }
        assert count_leaves(data) == 5  # Alice, 30, Bob, 25, 2

    def test_tuple_support(self):
        """Tuples are counted like lists."""
        assert count_leaves((1, 2, 3)) == 3
        assert count_leaves({"a": (1, 2)}) == 2

    def test_set_treated_as_leaf(self):
        """Sets are treated as single leaf values."""
        assert count_leaves({1, 2, 3}) == 1
        assert count_leaves({"a": {1, 2, 3}}) == 1


class TestGetAllPaths:
    """Tests for get_all_paths function."""

    def test_primitive_value(self):
        """Primitive returns empty path."""
        assert get_all_paths(42) == [[]]
        assert get_all_paths("string") == [[]]
        assert get_all_paths(None) == [[]]

    def test_empty_containers(self):
        """Empty containers return no paths."""
        assert get_all_paths({}) == []
        assert get_all_paths([]) == []
        assert get_all_paths(()) == []

    def test_flat_dict(self):
        """Flat dict returns single-key paths."""
        result = get_all_paths({"a": 1, "b": 2})
        assert ["a"] in result
        assert ["b"] in result
        assert len(result) == 2

    def test_flat_list(self):
        """Flat list returns index paths."""
        assert get_all_paths([1, 2, 3]) == [[0], [1], [2]]

    def test_nested_dict(self):
        """Nested dicts produce nested paths."""
        result = get_all_paths({"a": {"b": 1, "c": 2}})
        assert ["a", "b"] in result
        assert ["a", "c"] in result
        assert len(result) == 2

    def test_nested_list(self):
        """Nested lists produce nested index paths."""
        assert get_all_paths([[1, 2], [3]]) == [[0, 0], [0, 1], [1, 0]]

    def test_mixed_dict_list(self):
        """Mixed dict and list nesting."""
        data = {"users": [{"name": "Alice"}, {"name": "Bob"}]}
        result = get_all_paths(data)
        assert ["users", 0, "name"] in result
        assert ["users", 1, "name"] in result
        assert len(result) == 2

    def test_complex_structure(self):
        """Complex nested structure."""
        data = {
            "a": {
                "b": 1,
                "c": [2, 3]
            },
            "d": 4
        }
        result = get_all_paths(data)
        assert ["a", "b"] in result
        assert ["a", "c", 0] in result
        assert ["a", "c", 1] in result
        assert ["d"] in result
        assert len(result) == 4

    def test_tuple_support(self):
        """Tuples are handled like lists."""
        data = {"items": (1, 2)}
        result = get_all_paths(data)
        assert ["items", 0] in result
        assert ["items", 1] in result

    def test_set_treated_as_leaf(self):
        """Sets are treated as leaf values."""
        data = {"a": {1, 2, 3}}
        result = get_all_paths(data)
        assert result == [["a"]]

    def test_deeply_nested(self):
        """Deeply nested structure."""
        data = {"a": {"b": {"c": {"d": {"e": 1}}}}}
        assert get_all_paths(data) == [["a", "b", "c", "d", "e"]]

    def test_path_types(self):
        """Paths contain strings for dict keys and ints for list indices."""
        data = {"key": [1, 2]}
        result = get_all_paths(data)
        assert result == [["key", 0], ["key", 1]]
        # Verify types
        assert isinstance(result[0][0], str)
        assert isinstance(result[0][1], int)
