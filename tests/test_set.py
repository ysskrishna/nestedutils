import pytest
from nestedutils import set_at
from nestedutils.exceptions import PathError, PathErrorCode


class TestSetBasic:
    """Basic set_at functionality tests."""
    
    def test_set_simple(self):
        """Set value in simple dict."""
        d = {}
        set_at(d, "a", 5)
        assert d == {"a": 5}
    
    def test_set_nested_existing(self):
        """Set value in existing nested structure."""
        d = {"a": {"b": {}}}
        set_at(d, "a.b.c", 9)
        assert d == {"a": {"b": {"c": 9}}}
    
    def test_set_auto_create_dicts(self):
        """Auto-create nested dicts when setting with create=True."""
        d = {}
        set_at(d, "x.y.z", 10, create=True)
        assert d == {"x": {"y": {"z": 10}}}
    
    def test_set_auto_create_lists(self):
        """Auto-create lists when using numeric keys with create=True."""
        d = {}
        set_at(d, "a.0.b", 1, create=True)
        assert d == {"a": [{"b": 1}]}
    
    def test_set_requires_create_for_missing_path(self):
        """set_at raises PathError for missing paths by default."""
        d = {}
        with pytest.raises(PathError) as exc_info:
            set_at(d, "x.y.z", 10)
        assert exc_info.value.code == PathErrorCode.MISSING_KEY
    
    def test_set_no_sparse_lists(self):
        """Sparse list creation is not allowed."""
        d = {"a": []}
        with pytest.raises(PathError) as exc_info:
            set_at(d, "a.5", 99, create=True)
        assert exc_info.value.code == PathErrorCode.INVALID_INDEX
        assert "no sparse lists" in str(exc_info.value.message).lower()
    
    def test_set_negative_index_write(self):
        """Set value using negative index."""
        d = {"a": [1, 2, 3]}
        set_at(d, "a.-1", 999)
        assert d["a"] == [1, 2, 999]
    
    def test_set_negative_index_modify_existing(self):
        """Modify existing element using negative index (from docstring example)."""
        data = [1, 2, 3]
        set_at(data, "-1", 99)
        assert data == [1, 2, 99]
    
    def test_set_negative_index_out_of_bounds_raises_error(self):
        """Out-of-bounds negative index should raise PathError."""
        data = [1, 2, 3]
        with pytest.raises(PathError) as exc_info:
            set_at(data, "-5", 99)
        assert exc_info.value.code == PathErrorCode.INVALID_INDEX
        # Verify data unchanged
        assert data == [1, 2, 3]
    
    def test_set_negative_index_nested_structure(self):
        """Set value using negative index in nested structure."""
        d = {"items": [{"name": "apple"}, {"name": "banana"}]}
        set_at(d, "items.-1.name", "cherry")
        assert d["items"][-1]["name"] == "cherry"
        assert d["items"][0]["name"] == "apple"
    
    def test_set_negative_index_intermediate_path(self):
        """Set value where intermediate path uses negative index."""
        d = {"data": [[1, 2], [3, 4], [5, 6]]}
        set_at(d, "data.-1.-1", 99)
        assert d["data"][-1][-1] == 99
        assert d["data"][-1] == [5, 99]
    
    def test_set_negative_index_modifies_single_element_list(self):
        """Negative index on short list should still work."""
        d = {"a": [1]}
        set_at(d, "a.-1", 99)
        assert d == {"a": [99]}
    
    def test_set_negative_index_all_valid_indices(self):
        """Test all valid negative indices for a list."""
        d = {"a": [10, 20, 30, 40]}
        set_at(d, "a.-1", 1)
        set_at(d, "a.-2", 2)
        set_at(d, "a.-3", 3)
        set_at(d, "a.-4", 4)
        assert d["a"] == [4, 3, 2, 1]
    
    def test_set_inside_list_of_dicts(self):
        """Set value inside list containing dicts."""
        d = {"a": [{}]}
        set_at(d, "a.0.x.y", 5, create=True)
        assert d == {"a": [{"x": {"y": 5}}]}


class TestSetCreateFlag:
    """Tests for create parameter."""
    
    def test_set_create_true_auto_creates(self):
        """create=True auto-creates missing intermediate containers."""
        d = {}
        set_at(d, "a.b.c", 1, create=True)
        assert d == {"a": {"b": {"c": 1}}}
    
    def test_set_create_false_raises_for_missing(self):
        """create=False (default) raises PathError for missing paths."""
        d = {}
        with pytest.raises(PathError) as exc_info:
            set_at(d, "a.b.c", 1)
        assert exc_info.value.code == PathErrorCode.MISSING_KEY
    
    def test_set_create_true_sequential_list_building(self):
        """create=True allows sequential list building."""
        d = {}
        set_at(d, "items.0", "first", create=True)
        set_at(d, "items.1", "second", create=True)
        assert d == {"items": ["first", "second"]}
    
    def test_set_create_true_no_gaps_allowed(self):
        """create=True does not allow sparse lists."""
        d = {}
        set_at(d, "items.0", "first", create=True)
        with pytest.raises(PathError) as exc_info:
            set_at(d, "items.5", "x", create=True)
        assert exc_info.value.code == PathErrorCode.INVALID_INDEX


class TestSetNoneValues:
    """Tests for handling None values."""
    
    def test_set_through_existing_none_in_list(self):
        """Should replace None with a container when navigating deeper with create=True."""
        d = {"a": [None, None, None]}
        set_at(d, "a.1.x", 5, create=True)
        assert d == {"a": [None, {"x": 5}, None]}
    
    def test_set_through_none_in_dict(self):
        """Should replace None value in dict when navigating deeper with create=True."""
        d = {"a": None}
        set_at(d, "a.b.c", 10, create=True)
        assert d == {"a": {"b": {"c": 10}}}
    
    def test_set_through_none_requires_create(self):
        """Setting through None requires create=True."""
        d = {"a": None}
        with pytest.raises(PathError) as exc_info:
            set_at(d, "a.b.c", 10)
        assert exc_info.value.code == PathErrorCode.MISSING_KEY
    
    def test_set_none_value_explicitly(self):
        """Setting None as a value should work."""
        d = {"a": 1}
        set_at(d, "a", None)
        assert d == {"a": None}
    
    def test_set_none_in_nested_path(self):
        """Setting None deep in path with create=True."""
        d = {}
        set_at(d, "a.b.c", None, create=True)
        assert d == {"a": {"b": {"c": None}}}
    
    def test_set_none_then_replace(self):
        """Set None then replace with container using create=True."""
        d = {}
        set_at(d, "a", None)
        set_at(d, "a.b", 1, create=True)
        assert d == {"a": {"b": 1}}


class TestSetImmutableContainers:
    """Tests for setting into immutable containers."""
    
    def test_set_into_tuple_fails(self):
        """Setting into tuple should fail."""
        d = {"a": (1, 2, 3)}
        with pytest.raises(PathError) as exc_info:
            set_at(d, "a.0", 9)
        assert exc_info.value.code == PathErrorCode.IMMUTABLE_CONTAINER
    
    def test_set_navigating_into_tuple_fails(self):
        """Navigating into tuple should fail."""
        d = {"a": ({"x": 1},)}
        with pytest.raises(PathError) as exc_info:
            set_at(d, "a.0.x.y", 1)
        assert exc_info.value.code == PathErrorCode.IMMUTABLE_CONTAINER


class TestSetErrorCases:
    """Error cases for set_at."""
    
    def test_set_list_index_non_integer(self):
        """Setting with non-integer key on list should fail."""
        d = {"a": [1]}
        with pytest.raises(PathError) as exc_info:
            set_at(d, "a.x", 1)
        assert exc_info.value.code == PathErrorCode.INVALID_INDEX
    
    def test_replace_list_with_dict_key(self):
        """Setting dict key where list exists should fail."""
        d = {"a": [1, 2, 3]}
        with pytest.raises(PathError) as exc_info:
            set_at(d, "a.notanumber", 5)
        assert exc_info.value.code == PathErrorCode.INVALID_INDEX
    
    def test_set_at_invalid_type(self):
        """Setting into non-container type should fail."""
        d = {"a": 1}
        with pytest.raises(PathError) as exc_info:
            set_at(d, "a.b", 10)
        assert exc_info.value.code == PathErrorCode.NON_NAVIGABLE_TYPE
    
    def test_set_negative_index_on_empty_list(self):
        """Can't use negative index on empty list."""
        d = {"a": []}
        with pytest.raises(PathError) as exc_info:
            set_at(d, "a.-1", 5)
        assert exc_info.value.code == PathErrorCode.INVALID_INDEX
    
    def test_set_negative_index_on_empty_dict(self):
        """Can't create list with negative index as first operation."""
        d = {}
        # First, need to create the list with create=True
        # But negative index can't be used to create (must reference existing element)
        with pytest.raises(PathError) as exc_info:
            set_at(d, "a.-1", 5, create=True)
        assert exc_info.value.code == PathErrorCode.INVALID_INDEX
    
    def test_numeric_key_on_existing_dict(self):
        """Setting numeric key on existing dict creates string key."""
        d = {"a": {"b": 1}}
        set_at(d, "a.0", 5)
        assert d == {"a": {"b": 1, "0": 5}}
    
    def test_invalid_negative_format(self):
        """String starting with - but not a valid negative number."""
        d = {}
        set_at(d, "a.-5x", 1, create=True)
        assert d == {"a": {"-5x": 1}}  # Should be dict key
    
    def test_just_minus_sign(self):
        """Just a minus sign should be dict key."""
        d = {}
        set_at(d, "a.-", 1, create=True)
        assert d == {"a": {"-": 1}}
    
    def test_multiple_minus_signs(self):
        """Multiple minus signs."""
        d = {}
        set_at(d, "a.--5", 1, create=True)
        assert d == {"a": {"--5": 1}}


class TestSetPathNormalization:
    """Tests for path normalization in set_at."""
    
    def test_path_as_list_form(self):
        """Set using list form path."""
        d = {}
        set_at(d, ["a", "b", "c"], 1, create=True)
        assert d == {"a": {"b": {"c": 1}}}
    
    def test_keys_with_dots_in_list_form(self):
        """Using list form allows keys with dots."""
        d = {}
        set_at(d, ["a.b", "c.d"], 10, create=True)
        assert d == {"a.b": {"c.d": 10}}
    
    def test_path_list_with_integers(self):
        """List form path with integer keys."""
        d = {}
        set_at(d, ["a", 0, "b"], 1, create=True)
        assert d == {"a": [{"b": 1}]}


class TestSetComplex:
    """Complex set_at scenarios."""
    
    def test_set_deep_mixed_structure(self):
        """Set in deeply nested mixed structure."""
        d = {}
        # Need to build sequentially - first create index 0, then index 1
        set_at(d, "x.0.y.0.z", 10, create=True)  # Create first element
        set_at(d, "x.0.y.1.z", 42, create=True)  # Now can append
        assert d == {
            "x": [
                {
                    "y": [
                        {"z": 10},
                        {"z": 42}
                    ]
                }
            ]
        }
    
    def test_set_at_creates_correct_types_auto(self):
        """create=True creates correct types."""
        d = {}
        set_at(d, "root.0.child.0", 10, create=True)
        assert d == {"root": [{"child": [10]}]}
    
    def test_overwrite_value_with_container(self):
        """Overwrite a value then navigate into it."""
        d = {"a": 5}
        set_at(d, "a", {"b": 1})
        assert d == {"a": {"b": 1}}
        set_at(d, "a.c", 2)
        assert d == {"a": {"b": 1, "c": 2}}
    
    def test_final_key_extends_list_sequentially(self):
        """Final key can only extend list by 1 (append)."""
        d = {"a": []}
        set_at(d, "a.0", "first", create=True)
        set_at(d, "a.1", "second", create=True)
        assert d == {"a": ["first", "second"]}
    
    def test_set_positive_extension_sequential_only(self):
        """Positive index can only append, not create gaps."""
        data = [1, 2, 3]
        set_at(data, "3", 99, create=True)  # Append
        assert data == [1, 2, 3, 99]
        with pytest.raises(PathError):
            set_at(data, "5", 100, create=True)  # Would create gap
    
    def test_set_multiple_values_same_structure(self):
        """Set multiple values in same structure."""
        d = {}
        set_at(d, "a.b.c", 1, create=True)
        set_at(d, "a.b.d", 2, create=True)  # Path exists now, no create needed
        set_at(d, "a.e", 3, create=True)  # Path exists now, no create needed
        assert d == {"a": {"b": {"c": 1, "d": 2}, "e": 3}}
    
    def test_set_overwrite_existing_value(self):
        """Overwrite existing value."""
        d = {"a": {"b": 1}}
        set_at(d, "a.b", 2)
        assert d == {"a": {"b": 2}}
