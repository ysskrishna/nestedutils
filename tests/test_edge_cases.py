from nestedutils import get_at, set_at, delete_at
from nestedutils.exceptions import PathError, PathErrorCode


class TestExceptionHandling:
    """Tests for exception handling and error codes."""
    
    def test_path_error_has_message(self):
        """PathError should have a message."""
        try:
            get_at({}, 123)
        except PathError as e:
            assert e.message is not None
            assert len(str(e)) > 0
    
    def test_path_error_has_code(self):
        """PathError should have a code."""
        try:
            get_at({}, 123)
        except PathError as e:
            assert e.code is not None
            assert e.code == PathErrorCode.INVALID_PATH
    
    def test_exception_inheritance(self):
        """PathError should be an Exception."""
        try:
            get_at({}, 123)
        except PathError as e:
            assert isinstance(e, Exception)
            assert isinstance(e, PathError)
    
    def test_all_error_codes_exist(self):
        """Verify all expected error codes exist."""
        codes = [
            PathErrorCode.INVALID_INDEX,
            PathErrorCode.MISSING_KEY,
            PathErrorCode.EMPTY_PATH,
            PathErrorCode.IMMUTABLE_CONTAINER,
            PathErrorCode.INVALID_PATH,
            PathErrorCode.INVALID_FILL_STRATEGY,
        ]
        assert len(codes) == 6
    
    def test_error_code_values(self):
        """Verify error code string values."""
        assert PathErrorCode.INVALID_INDEX.value == "INVALID_INDEX"
        assert PathErrorCode.MISSING_KEY.value == "MISSING_KEY"
        assert PathErrorCode.EMPTY_PATH.value == "EMPTY_PATH"
        assert PathErrorCode.IMMUTABLE_CONTAINER.value == "IMMUTABLE_CONTAINER"
        assert PathErrorCode.INVALID_PATH.value == "INVALID_PATH"
        assert PathErrorCode.INVALID_FILL_STRATEGY.value == "INVALID_FILL_STRATEGY"


class TestPathNormalizationEdgeCases:
    """Additional edge cases for path normalization."""
    
    def test_path_list_with_negative_index(self):
        """List form path with negative index."""
        d = {"a": [10, 20, 30]}
        assert get_at(d, ["a", -1]) == 30
        set_at(d, ["a", -1], 999)
        assert d["a"][2] == 999
    
    def test_path_list_empty_strings(self):
        """List form with empty strings."""
        d = {}
        set_at(d, ["a", "", "b"], 1)
        assert d == {"a": {"": {"b": 1}}}
        assert get_at(d, ["a", "", "b"]) == 1


class TestComplexIntegrationScenarios:
    """Complex integration scenarios combining multiple operations."""
    
    def test_round_trip_operations(self):
        """Multiple operations in sequence."""
        d = {}
        set_at(d, "a.b.c", 1)
        assert get_at(d, "a.b.c") == 1
        set_at(d, "a.b.d", 2)
        assert get_at(d, "a.b.d") == 2
        val = delete_at(d, "a.b.c")
        assert val == 1
        assert get_at(d, "a.b.c") is None
        assert get_at(d, "a.b.d") == 2
    
    def test_mixed_numeric_and_string_keys(self):
        """Mixed numeric and string keys."""
        d = {}
        set_at(d, "a.0.b.1.c", 42)
        assert isinstance(d["a"], list)
        assert isinstance(d["a"][0], dict)
        assert isinstance(d["a"][0]["b"], list)
        assert d["a"][0]["b"][1]["c"] == 42


class TestEmptyAndNoneValues:
    """Tests for empty and None value handling."""
    
    def test_get_none_vs_missing(self):
        """Distinguish between None value and missing key."""
        d1 = {"a": None}
        d2 = {}
        assert get_at(d1, "a") is None
        assert get_at(d2, "a") is None
        # Both return None, but one has the key, one doesn't
        assert "a" in d1
        assert "a" not in d2


class TestLargeStructures:
    """Tests for large data structures."""
    
    def test_very_deep_nesting(self):
        """Very deeply nested structure."""
        d = {}
        path = ".".join(["level" + str(i) for i in range(20)])
        set_at(d, path, "deep")
        assert get_at(d, path) == "deep"
    
    def test_many_keys_in_dict(self):
        """Dict with many keys."""
        d = {}
        for i in range(100):
            set_at(d, f"key{i}", i)
        for i in range(100):
            assert get_at(d, f"key{i}") == i


class TestTypeCoercion:
    """Tests for type coercion and conversion."""
    
    def test_list_path_with_string_numbers(self):
        """List form path with string numbers."""
        d = {"a": [1, 2, 3]}
        assert get_at(d, ["a", "0"]) == 1
        assert get_at(d, ["a", "1"]) == 2
    
    def test_list_path_with_integers(self):
        """List form path with actual integers."""
        d = {"a": [1, 2, 3]}
        assert get_at(d, ["a", 0]) == 1
        assert get_at(d, ["a", 1]) == 2
    
    def test_mixed_path_types(self):
        """Mixed path types in list form."""
        d = {"a": {"0": [1, 2, 3]}}
        assert get_at(d, ["a", "0", 1]) == 2


class TestSpecialCharacters:
    """Tests for special characters in keys."""
    
    def test_keys_with_special_chars(self):
        """Keys with special characters."""
        d = {}
        set_at(d, "a-b.c_d.e@f", 42)
        assert get_at(d, "a-b.c_d.e@f") == 42
    
    def test_keys_with_spaces_in_list_form(self):
        """Keys with spaces using list form."""
        d = {}
        set_at(d, ["key with spaces", "another key"], 1)
        assert get_at(d, ["key with spaces", "another key"]) == 1
    
    def test_keys_with_newlines_in_list_form(self):
        """Keys with newlines using list form."""
        d = {}
        set_at(d, ["key\nwith\nnewlines"], 1)
        assert get_at(d, ["key\nwith\nnewlines"]) == 1

