import pytest
from nestedutils import get_at
from nestedutils.exceptions import PathError, PathErrorCode


class TestGetBasic:
    """Basic get_at functionality tests."""
    
    def test_get_simple(self):
        """Get value from simple dict."""
        d = {"a": 1}
        assert get_at(d, "a") == 1
    
    def test_get_nested_dict(self):
        """Get value from deeply nested dict."""
        d = {"a": {"b": {"c": 5}}}
        assert get_at(d, "a.b.c") == 5
    
    def test_get_missing_returns_default(self):
        """Get missing key returns default value."""
        d = {"a": {"b": 1}}
        assert get_at(d, "a.c", default=99) == 99
        assert get_at(d, "x.y.z") is None
        assert get_at(d, "x.y.z", default="missing") == "missing"
    
    def test_get_list_index(self):
        """Get value from list using index."""
        d = {"a": [10, 20, 30]}
        assert get_at(d, "a.1") == 20
        assert get_at(d, "a.0") == 10
        assert get_at(d, "a.2") == 30
    
    def test_get_negative_list_index(self):
        """Get value using negative list index."""
        d = {"a": [10, 20, 30]}
        assert get_at(d, "a.-1") == 30
        assert get_at(d, "a.-2") == 20
        assert get_at(d, "a.-3") == 10
    
    def test_get_nested_list_dict_mix(self):
        """Get value from mixed nested list and dict."""
        d = {"a": [{"b": 1}, {"b": 2}]}
        assert get_at(d, "a.1.b") == 2
        assert get_at(d, "a.0.b") == 1
    
    def test_get_list_index_out_of_bounds(self):
        """Get from out-of-bounds list index returns default."""
        d = {"a": [10, 20]}
        assert get_at(d, "a.5") is None
        assert get_at(d, "a.5", default=-1) == -1
        assert get_at(d, "a.-10") is None
    
    def test_get_list_index_non_integer(self):
        """Get with non-integer key on list returns default."""
        d = {"a": [1]}
        assert get_at(d, "a.x") is None
        assert get_at(d, "a.x", default="not found") == "not found"


class TestGetPathNormalization:
    """Tests for path normalization (list form, unicode, etc.)."""
    
    def test_path_as_list_form(self):
        """Get using list form path."""
        d = {"a": {"b": {"c": 1}}}
        assert get_at(d, ["a", "b", "c"]) == 1
    
    def test_path_list_mixed_int(self):
        """Get using list form with integer keys."""
        d = {"a": [{"b": 3}]}
        assert get_at(d, ["a", 0, "b"]) == 3
    
    def test_path_list_with_negative_index(self):
        """Get using list form with negative index."""
        d = {"a": [10, 20, 30]}
        assert get_at(d, ["a", -1]) == 30
    
    def test_unicode_keys(self):
        """Get with unicode keys."""
        d = {}
        d["你好"] = {"world": {"🌍": 42}}
        assert get_at(d, "你好.world.🌍") == 42
        assert get_at(d, ["你好", "world", "🌍"]) == 42
    
    def test_keys_with_dots_in_list_form(self):
        """List form allows keys with dots."""
        d = {"a.b": {"c.d": 10}}
        assert get_at(d, ["a.b", "c.d"]) == 10


class TestGetEdgeCases:
    """Edge cases for get_at."""
    
    def test_get_empty_dict(self):
        """Get from empty dict."""
        d = {}
        assert get_at(d, "a") is None
        assert get_at(d, "a.b.c") is None
    
    def test_get_empty_list(self):
        """Get from empty list."""
        d = {"a": []}
        assert get_at(d, "a.0") is None
    
    def test_get_none_value(self):
        """Get None value explicitly stored."""
        d = {"a": None}
        assert get_at(d, "a") is None
    
    def test_get_false_value(self):
        """Get False value (should not be confused with missing)."""
        d = {"a": False}
        assert get_at(d, "a") is False
        assert get_at(d, "a", default=True) is False  # Should return False, not default
    
    def test_get_zero_value(self):
        """Get zero value (should not be confused with missing)."""
        d = {"a": 0}
        assert get_at(d, "a") == 0
    
    def test_get_empty_string_value(self):
        """Get empty string value."""
        d = {"a": ""}
        assert get_at(d, "a") == ""
    
    def test_get_very_deep_nesting(self):
        """Get from very deeply nested structure."""
        d = {"a": {"b": {"c": {"d": {"e": {"f": {"g": 42}}}}}}}
        assert get_at(d, "a.b.c.d.e.f.g") == 42
    
    def test_get_from_dict_with_numeric_keys(self):
        """Get from dict with numeric string keys."""
        d = {"0": {"1": {"2": 5}}}
        assert get_at(d, "0.1.2") == 5
    
    def test_get_mixed_types(self):
        """Get from structure with mixed types."""
        d = {
            "a": [1, "two", {"three": 3}],
            "b": {"list": [10, 20], "dict": {"nested": "value"}}
        }
        assert get_at(d, "a.0") == 1
        assert get_at(d, "a.1") == "two"
        assert get_at(d, "a.2.three") == 3
        assert get_at(d, "b.list.1") == 20
        assert get_at(d, "b.dict.nested") == "value"


class TestGetInvalidPaths:
    """Tests for invalid path types."""
    
    @pytest.mark.parametrize("invalid_path", [
        123,
        None,
        {},
        tuple(),
        set(),
        3.14,
        True,
        False,
    ])
    def test_get_at_invalid_path_types(self, invalid_path):
        """get_at should raise PathError with INVALID_PATH code for invalid path types."""
        d = {"a": 1}
        with pytest.raises(PathError) as exc_info:
            get_at(d, invalid_path)
        assert exc_info.value.code == PathErrorCode.INVALID_PATH
    
    # def test_get_empty_path(self):
    #     """Get with empty path returns the root data."""
    #     d = {"a": 1}
    #     # Empty path should return the root data structure
    #     result = get_at(d, "")
    #     assert result == d
    #     assert result is d  # Should return the same object

