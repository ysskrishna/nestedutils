import pytest
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
            PathErrorCode.NON_NAVIGABLE_TYPE,
            PathErrorCode.OPERATION_DISABLED,
        ]
        assert len(codes) == 7
    
    def test_error_code_values(self):
        """Verify error code string values."""
        assert PathErrorCode.INVALID_INDEX.value == "INVALID_INDEX"
        assert PathErrorCode.MISSING_KEY.value == "MISSING_KEY"
        assert PathErrorCode.EMPTY_PATH.value == "EMPTY_PATH"
        assert PathErrorCode.IMMUTABLE_CONTAINER.value == "IMMUTABLE_CONTAINER"
        assert PathErrorCode.INVALID_PATH.value == "INVALID_PATH"
        assert PathErrorCode.NON_NAVIGABLE_TYPE.value == "NON_NAVIGABLE_TYPE"
        assert PathErrorCode.OPERATION_DISABLED.value == "OPERATION_DISABLED"


class TestComplexIntegrationScenarios:
    """Complex integration scenarios combining multiple operations."""
    
    def test_round_trip_operations(self):
        """Multiple operations in sequence."""
        d = {}
        set_at(d, "a.b.c", 1, create=True)
        assert get_at(d, "a.b.c") == 1
        set_at(d, "a.b.d", 2, create=True)
        assert get_at(d, "a.b.d") == 2
        val = delete_at(d, "a.b.c")
        assert val == 1
        with pytest.raises(PathError):
            get_at(d, "a.b.c")
        assert get_at(d, "a.b.d") == 2
    
    def test_mixed_numeric_and_string_keys(self):
        """Mixed numeric and string keys."""
        d = {}
        # Build structure sequentially - first create index 0, then index 1
        set_at(d, "a.0.b.0.c", 10, create=True)  # Create list at a[0]["b"] with first element
        set_at(d, "a.0.b.1.c", 42, create=True)  # Now can append to list
        assert isinstance(d["a"], list)
        assert isinstance(d["a"][0], dict)
        assert isinstance(d["a"][0]["b"], list)
        assert d["a"][0]["b"][0]["c"] == 10
        assert d["a"][0]["b"][1]["c"] == 42


class TestLargeStructures:
    """Tests for large data structures."""
    
    def test_very_deep_nesting(self):
        """Very deeply nested structure."""
        d = {}
        path = ".".join(["level" + str(i) for i in range(20)])
        set_at(d, path, "deep", create=True)
        assert get_at(d, path) == "deep"
    
    def test_many_keys_in_dict(self):
        """Dict with many keys."""
        d = {}
        for i in range(100):
            set_at(d, f"key{i}", i, create=True)
        for i in range(100):
            assert get_at(d, f"key{i}") == i


class TestListPathTypeHandling:
    """Tests for type coercion and conversion."""
    
    def test_list_path_with_string_numbers(self):
        """List form path with string numbers."""
        d = {"a": [1, 2, 3]}
        assert get_at(d, ["a", "0"]) == 1
        assert get_at(d, ["a", "1"]) == 2

    def test_mixed_path_types(self):
        """Mixed path types in list form."""
        d = {"a": {"0": [1, 2, 3]}}
        assert get_at(d, ["a", "0", 1]) == 2


class TestSpecialCharacters:
    """Tests for special characters in keys."""
    
    def test_keys_with_special_chars(self):
        """Keys with special characters."""
        d = {}
        set_at(d, "a-b.c_d.e@f", 42, create=True)
        assert get_at(d, "a-b.c_d.e@f") == 42
    
    def test_keys_with_spaces_in_list_form(self):
        """Keys with spaces using list form."""
        d = {}
        set_at(d, ["key with spaces", "another key"], 1, create=True)
        assert get_at(d, ["key with spaces", "another key"]) == 1
    
    def test_keys_with_newlines_in_list_form(self):
        """Keys with newlines using list form."""
        d = {}
        set_at(d, ["key\nwith\nnewlines"], 1, create=True)
        assert get_at(d, ["key\nwith\nnewlines"]) == 1


class TestNegativeIndexEdgeCases:
    """Edge cases for negative indices not covered in operation-specific tests."""

    def test_negative_index_very_large_negative(self):
        """Very large negative numbers should be out of bounds."""
        d = {"a": [1, 2, 3]}
        with pytest.raises(PathError):
            get_at(d, "a.-1000")
        with pytest.raises(PathError):
            get_at(d, "a.-999999")
        # With default, returns default
        assert get_at(d, "a.-1000", default="missing") == "missing"

    def test_negative_index_after_list_mutation(self):
        """Negative index behavior after list mutations."""
        d = {"items": [1, 2, 3, 4, 5]}
        # Delete using positive index
        delete_at(d, "items.1", allow_list_mutation=True)
        assert d["items"] == [1, 3, 4, 5]
        # Negative indices should still work correctly
        assert get_at(d, "items.-1") == 5
        assert get_at(d, "items.-2") == 4
        assert get_at(d, "items.-4") == 1
        # -5 should now be out of bounds
        with pytest.raises(PathError):
            get_at(d, "items.-5")


class TestMissingEdgeCases:
    """Additional edge cases for comprehensive coverage."""

    def test_get_empty_path_raises(self):
        """Empty path should raise EMPTY_PATH error."""
        with pytest.raises(PathError) as exc:
            get_at({}, "")
        assert exc.value.code == PathErrorCode.EMPTY_PATH

    def test_set_empty_path_raises(self):
        """Empty path should raise EMPTY_PATH error for set_at."""
        with pytest.raises(PathError) as exc:
            set_at({}, "", 1)
        assert exc.value.code == PathErrorCode.EMPTY_PATH

    def test_delete_empty_path_raises(self):
        """Empty path should raise EMPTY_PATH error for delete_at."""
        with pytest.raises(PathError) as exc:
            delete_at({}, "")
        assert exc.value.code == PathErrorCode.EMPTY_PATH

    def test_set_non_container_root_raises(self):
        """Setting on non-container root should raise NON_NAVIGABLE_TYPE."""
        with pytest.raises(PathError) as exc:
            set_at(42, "a", 1)
        assert exc.value.code == PathErrorCode.NON_NAVIGABLE_TYPE

    def test_get_non_container_root_raises(self):
        """Getting from non-container root should raise NON_NAVIGABLE_TYPE."""
        with pytest.raises(PathError) as exc:
            get_at(42, "a")
        assert exc.value.code == PathErrorCode.NON_NAVIGABLE_TYPE

    def test_delete_non_container_root_raises(self):
        """Deleting from non-container root should raise NON_NAVIGABLE_TYPE."""
        with pytest.raises(PathError) as exc:
            delete_at(42, "a")
        assert exc.value.code == PathErrorCode.NON_NAVIGABLE_TYPE

    def test_get_from_set_raises(self):
        """Accessing set elements should raise NON_NAVIGABLE_TYPE."""
        with pytest.raises(PathError) as exc:
            get_at({"a": {1, 2, 3}}, "a.0")
        assert exc.value.code == PathErrorCode.NON_NAVIGABLE_TYPE

    def test_get_from_frozenset_raises(self):
        """Accessing frozenset elements should raise NON_NAVIGABLE_TYPE."""
        with pytest.raises(PathError) as exc:
            get_at({"a": frozenset([1, 2, 3])}, "a.0")
        assert exc.value.code == PathErrorCode.NON_NAVIGABLE_TYPE

    def test_set_into_string_raises(self):
        """Setting into a string should raise NON_NAVIGABLE_TYPE."""
        with pytest.raises(PathError) as exc:
            set_at({"a": "hello"}, "a.0", "x")
        assert exc.value.code == PathErrorCode.NON_NAVIGABLE_TYPE

