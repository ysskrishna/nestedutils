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
    
    def test_get_intermediate_nested_object(self):
        """Get intermediate path returns complete nested object."""
        data = {
            "user": {
                "profile": {
                    "email": "john@example.com",
                    "address": {"city": "SF", "zip": "94102"}
                }
            }
        }
        # Getting intermediate path should return complete nested structure
        profile = get_at(data, "user.profile")
        assert profile == {
            "email": "john@example.com",
            "address": {"city": "SF", "zip": "94102"}
        }
        # Can also get deeper values
        assert get_at(data, "user.profile.address.city") == "SF"
    
    def test_get_missing_raises_error(self):
        """Get missing key raises PathError by default."""
        d = {"a": {"b": 1}}
        with pytest.raises(PathError) as exc_info:
            get_at(d, "a.c")
        assert exc_info.value.code == PathErrorCode.MISSING_KEY
    
    def test_get_missing_with_default(self):
        """Get missing key returns default when explicitly provided."""
        d = {"a": {"b": 1}}
        assert get_at(d, "a.c", default=99) == 99
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
    
    def test_get_negative_index_nested_structure(self):
        """Get value using negative index in nested list-dict structure."""
        d = {"items": [{"name": "apple"}, {"name": "banana"}]}
        assert get_at(d, "items.-1.name") == "banana"
        assert get_at(d, "items.-2.name") == "apple"
        assert get_at(d, "items.-1") == {"name": "banana"}
    
    def test_get_negative_index_out_of_bounds(self):
        """Get with out-of-bounds negative index raises PathError by default."""
        d = {"items": [{"name": "apple"}, {"name": "banana"}]}
        with pytest.raises(PathError) as exc_info:
            get_at(d, "items.-5.name")
        assert exc_info.value.code == PathErrorCode.INVALID_INDEX
        assert get_at(d, "items.-5.name", default="not found") == "not found"
    
    def test_get_negative_index_deeply_nested(self):
        """Get with negative index in deeply nested structure."""
        d = {"data": [[1, 2, 3], [4, 5, 6], [7, 8, 9]]}
        assert get_at(d, "data.-1.-1") == 9
        assert get_at(d, "data.-1.0") == 7
        assert get_at(d, "data.-2.-1") == 6
    
    def test_get_nested_list_dict_mix(self):
        """Get value from mixed nested list and dict."""
        d = {"a": [{"b": 1}, {"b": 2}]}
        assert get_at(d, "a.1.b") == 2
        assert get_at(d, "a.0.b") == 1
    
    def test_get_list_index_out_of_bounds(self):
        """Get from out-of-bounds list index raises PathError by default."""
        d = {"a": [10, 20]}
        with pytest.raises(PathError) as exc_info:
            get_at(d, "a.5")
        assert exc_info.value.code == PathErrorCode.INVALID_INDEX
        assert get_at(d, "a.5", default=-1) == -1
        with pytest.raises(PathError):
            get_at(d, "a.-10")
        # Test both positive and negative out-of-bounds
        with pytest.raises(PathError):
            get_at(d, "a.100")
        with pytest.raises(PathError):
            get_at(d, "a.-100")
        with pytest.raises(PathError):
            get_at(d, "a.-3")  # Just out of bounds for length 2
    
    def test_get_list_index_non_integer(self):
        """Get with non-integer key on list raises PathError by default."""
        d = {"a": [1]}
        with pytest.raises(PathError) as exc_info:
            get_at(d, "a.x")
        assert exc_info.value.code == PathErrorCode.INVALID_INDEX
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
        assert get_at(d, ["a", -2]) == 20
        assert get_at(d, ["a", -3]) == 10
    
    def test_path_list_with_negative_index_nested(self):
        """Get using list form with negative index in nested structure."""
        d = {"items": [{"name": "apple"}, {"name": "banana"}]}
        assert get_at(d, ["items", -1, "name"]) == "banana"
        assert get_at(d, ["items", -2, "name"]) == "apple"
    
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
    
    def test_integer_vs_string_key_distinction(self):
        """List form handles any key type: special characters, dots, integers (preserved or converted)."""
        # Create data structure with complex keys
        data = {
            "user-info": {
                "first.name": {
                    "123": "string_key_value",  # String key
                    123: "int_key_value"  # Integer key
                }
            }
        }
        
        # Verify each level works independently
        assert get_at(data, ["user-info"]) == {"first.name": {"123": "string_key_value", 123: "int_key_value"}}
        assert get_at(data, ["user-info", "first.name"]) == {"123": "string_key_value", 123: "int_key_value"}
        
        # Integer in path accesses integer key (preserved)
        assert get_at(data, ["user-info", "first.name", 123]) == "int_key_value"
        # String in path accesses string key
        assert get_at(data, ["user-info", "first.name", "123"]) == "string_key_value"
        
        # Test with default for missing path
        assert get_at(data, ["user-info", "first.name", 999], default="not found") == "not found"


class TestGetEdgeCases:
    """Edge cases for get_at."""
    
    def test_get_empty_dict(self):
        """Get from empty dict raises PathError by default."""
        d = {}
        with pytest.raises(PathError):
            get_at(d, "a")
        with pytest.raises(PathError):
            get_at(d, "a.b.c")
        # With default, returns default
        assert get_at(d, "a", default=None) is None
        assert get_at(d, "a.b.c", default="missing") == "missing"
    
    def test_get_empty_list(self):
        """Get from empty list raises PathError by default."""
        d = {"a": []}
        with pytest.raises(PathError):
            get_at(d, "a.0")
        assert get_at(d, "a.0", default=None) is None
    
    def test_get_none_value(self):
        """Get None value explicitly stored."""
        d = {"a": None}
        assert get_at(d, "a") is None
    
    def test_none_blocks_navigation(self):
        """None as intermediate value should block navigation and raise PathError by default."""
        # None at first level blocks further navigation
        d = {"a": None}
        with pytest.raises(PathError):
            get_at(d, "a.b")
        assert get_at(d, "a.b", default="missing") == "missing"
        with pytest.raises(PathError):
            get_at(d, "a.b.c")
        assert get_at(d, "a.b.c", default=99) == 99
        
        # None at deeper level also blocks navigation
        d2 = {"a": {"b": None}}
        with pytest.raises(PathError):
            get_at(d2, "a.b.c")
        assert get_at(d2, "a.b.c", default="not found") == "not found"
        with pytest.raises(PathError):
            get_at(d2, "a.b.c.d.e")
        
        # None in list should also block navigation
        d3 = {"items": [None, {"name": "apple"}]}
        with pytest.raises(PathError):
            get_at(d3, "items.0.name")
        assert get_at(d3, "items.0.name", default="no name") == "no name"
        
        # None in nested structure
        d4 = {"data": {"user": None, "other": {"value": 42}}}
        with pytest.raises(PathError):
            get_at(d4, "data.user.name")
        assert get_at(d4, "data.user.name", default="default") == "default"
        # But other paths should still work
        assert get_at(d4, "data.other.value") == 42
    
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
    
    def test_get_from_dict_with_numeric_keys(self):
        """Get from dict with numeric string keys."""
        d = {"0": {"1": {"2": 5}}}
        assert get_at(d, "0.1.2") == 5
    
    def test_get_dict_with_integer_vs_string_keys(self):
        """Test that integer keys in paths are preserved and can access integer dict keys.
        
        normalize_path() now preserves integer types from list paths, allowing
        dictionaries with integer keys to be accessed using integer values in paths.
        """
        # Dictionary with both integer key and string key
        data = {0: "int_value", "0": "string_value"}
        
        # Integer in path accesses integer key
        assert get_at(data, [0]) == "int_value"  # Preserves int, accesses int key
        # String in path accesses string key
        assert get_at(data, ["0"]) == "string_value"  # String accesses string key
        
        # Verify direct access still distinguishes
        assert data[0] == "int_value"
        assert data["0"] == "string_value"
        
        # List paths now distinguish between integer and string keys
        assert get_at(data, [0]) != get_at(data, ["0"])  # Different keys, different values
    
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

