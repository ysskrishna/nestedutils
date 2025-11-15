import pytest
from nestedutils import get_path, set_path, del_path
from nestedutils.exceptions import PathError


# --------------------------------------------------------------
# BASIC GET
# --------------------------------------------------------------

def test_get_simple():
    d = {"a": 1}
    assert get_path(d, "a") == 1


def test_get_nested_dict():
    d = {"a": {"b": {"c": 5}}}
    assert get_path(d, "a.b.c") == 5


def test_get_missing_returns_default():
    d = {"a": {"b": 1}}
    assert get_path(d, "a.c", default=99) == 99
    assert get_path(d, "x.y.z") is None


def test_get_list_index():
    d = {"a": [10, 20, 30]}
    assert get_path(d, "a.1") == 20


def test_get_negative_list_index():
    d = {"a": [10, 20, 30]}
    assert get_path(d, "a.-1") == 30
    assert get_path(d, "a.-2") == 20


def test_get_nested_list_dict_mix():
    d = {"a": [{"b": 1}, {"b": 2}]}
    assert get_path(d, "a.1.b") == 2


# --------------------------------------------------------------
# BASIC SET
# --------------------------------------------------------------

def test_set_simple():
    d = {}
    set_path(d, "a", 5)
    assert d == {"a": 5}


def test_set_nested_existing():
    d = {"a": {"b": {}}}
    set_path(d, "a.b.c", 9)
    assert d == {"a": {"b": {"c": 9}}}


def test_set_auto_create_dicts():
    d = {}
    set_path(d, "x.y.z", 10)
    assert d == {"x": {"y": {"z": 10}}}


def test_set_auto_create_lists():
    d = {}
    set_path(d, "a.0.b", 1)
    assert d == {"a": [{"b": 1}]}


def test_set_auto_sparse_list():
    d = {"a": []}
    set_path(d, "a.5", 99)
    assert d == {"a": [None, None, None, None, None, 99]}


def test_set_negative_index_write():
    d = {"a": [1, 2, 3]}
    set_path(d, "a.-1", 999)
    assert d["a"] == [1, 2, 999]


def test_set_inside_list_of_dicts():
    d = {"a": [{}]}
    set_path(d, "a.0.x.y", 5)
    assert d == {"a": [{"x": {"y": 5}}]}


# --------------------------------------------------------------
# SET + FILL STRATEGY
# --------------------------------------------------------------

def test_set_fill_strategy_none():
    d = {}
    set_path(d, "a.3", 7, fill_strategy="none")
    assert d == {"a": [None, None, None, 7]}


def test_set_fill_strategy_dict():
    d = {}
    set_path(d, "a.0.b", 1, fill_strategy="dict")
    assert d == {"a": {"0": {"b": 1}}}


def test_set_fill_strategy_list():
    d = {}
    set_path(d, "a.0.1", 42, fill_strategy="list")
    assert d == {"a": [[None, 42]]}


def test_set_invalid_fill_strategy():
    d = {}
    with pytest.raises(PathError):
        set_path(d, "a.b", 1, fill_strategy="unknown")


# --------------------------------------------------------------
# SET INTO TUPLE (READ-ONLY)
# --------------------------------------------------------------

def test_set_into_tuple_fails():
    d = {"a": (1, 2, 3)}
    with pytest.raises(PathError):
        set_path(d, "a.0", 9)


def test_set_navigating_into_tuple_fails():
    d = {"a": ({"x": 1},)}
    with pytest.raises(PathError):
        set_path(d, "a.0.x.y", 1)


# --------------------------------------------------------------
# DELETE
# --------------------------------------------------------------

def test_delete_from_dict():
    d = {"a": {"b": 1}}
    val = del_path(d, "a.b")
    assert val == 1
    assert d == {"a": {}}


def test_delete_missing_key():
    d = {"a": {}}
    with pytest.raises(PathError):
        del_path(d, "a.b")


def test_delete_list_index_disallowed():
    d = {"a": [1, 2, 3]}
    with pytest.raises(PathError):
        del_path(d, "a.1")  # must explicitly allow list deletion


def test_delete_list_index_allowed():
    d = {"a": [1, 2, 3]}
    val = del_path(d, "a.1", allow_list_mutation=True)
    assert val == 2
    assert d == {"a": [1, 3]}


def test_delete_negative_index():
    d = {"a": [10, 20, 30]}
    val = del_path(d, "a.-1", allow_list_mutation=True)
    assert val == 30
    assert d == {"a": [10, 20]}


def test_delete_from_nested_list_dict():
    d = {"a": [{"b": 1}, {"b": 2}]}
    val = del_path(d, "a.0.b")
    assert val == 1
    assert d == {"a": [{}, {"b": 2}]} or d == {"a": [{}, {"b": 2}]}  # acceptable depending on dict emptiness


# --------------------------------------------------------------
# ERROR CASES
# --------------------------------------------------------------

def test_set_list_index_non_integer():
    d = {"a": [1]}
    with pytest.raises(PathError):
        set_path(d, "a.x", 1)


def test_get_list_index_non_integer():
    d = {"a": [1]}
    assert get_path(d, "a.x") is None  # default


def test_delete_non_integer_list_index():
    d = {"a": [1]}
    with pytest.raises(PathError):
        del_path(d, "a.x", allow_list_mutation=True)


def test_set_path_invalid_type():
    d = {"a": 1}
    with pytest.raises(PathError):
        set_path(d, "a.b", 10)


def test_delete_path_invalid_type():
    d = {"a": 5}
    with pytest.raises(PathError):
        del_path(d, "a.b")


# --------------------------------------------------------------
# PATH NORMALIZATION
# --------------------------------------------------------------

def test_path_as_list_form():
    d = {"a": {"b": {"c": 1}}}
    assert get_path(d, ["a", "b", "c"]) == 1


def test_path_list_mixed_int():
    d = {"a": [{"b": 3}]}
    assert get_path(d, ["a", 0, "b"]) == 3


# --------------------------------------------------------------
# COMPLEX CASES
# --------------------------------------------------------------

def test_set_deep_mixed_structure():
    d = {}
    set_path(d, "x.0.y.1.z", 42)
    assert d == {
        "x": [
            {
                "y": [
                    None,
                    {"z": 42}
                ]
            }
        ]
    }


def test_get_after_set_symmetric():
    d = {}
    set_path(d, "a.0.b.0.c", "X")
    assert get_path(d, "a.0.b.0.c") == "X"


def test_delete_leaf_inside_nested_mixed():
    d = {"x": [{"y": {"z": 5}}]}
    val = del_path(d, "x.0.y.z")
    assert val == 5
    assert d == {"x": [{"y": {}}]}


def test_delete_complex_list_item():
    d = {"a": [{"b": 1}, {"b": 2}, {"b": 3}]}
    del_path(d, "a.1", allow_list_mutation=True)
    assert d == {"a": [{"b": 1}, {"b": 3}]}


def test_set_path_creates_correct_types_auto():
    d = {}
    set_path(d, "root.0.child.0", 10)
    assert d == {"root": [{"child": [10]}]}
