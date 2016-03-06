import mock
from prefsort import *
from nose.tools import raises


def test_pairs_empty():
    """Test that pairs works for an empty list"""
    expected = []
    actual = list(pairs([]))
    assert expected == actual

def test_pairs_odd():
    """Test that pairs works for odd length lists"""
    expected = [(1, 2), (3, None)]
    actual = list(pairs([1, 2, 3]))
    assert expected == actual

def test_pairs_even():
    """Test that pairs works for even length lists"""
    expected = [(1, 2), (3, 4)]
    actual = list(pairs([1, 2, 3, 4]))
    assert expected == actual

def test_pairs_order():
    """Test that each pair is sorted"""
    expected = [(1, 2), (3, 4)]
    actual = list(pairs([2, 1, 4, 3]))
    assert expected == actual

def test_round_empty():
    """Test that a round with no elements returns empty values"""
    expected = (None, [])
    actual = preference_sort_round([], {})
    assert expected == actual

def test_round_single():
    """Test a round with only one element"""
    expected = ("apple", [])
    actual = preference_sort_round(["apple"], {})
    assert expected == actual, "Expected {}, got {}".format(expected, actual)

def always_left(a, b):
    """Pretend the user always enters 'left'"""
    return a, b

@mock.patch("prefsort.prompt_order", side_effect=always_left)
def test_round_simple(prompt_func):
    """Test a round with two elements"""
    expected = ("apple", ["banana"])
    actual = preference_sort_round(["apple", "banana"], {})
    assert expected == actual, "Expected {}, got {}".format(expected, actual)

@mock.patch("prefsort.prompt_order", side_effect=always_left)
def test_round(prompt_func):
    """Test a round with an even number of elements"""
    expected = ("apple", ["banana", "strawberry", "orange", "raspberry", "grape"])
    actual = preference_sort_round(["apple", "banana", "strawberry", "raspberry", "orange", "grape"])
    assert expected == actual, "Expected {}, got {}".format(expected, actual)

@raises(ValueError)
def test_sort_negative_length():
    """prefsort should raise an error on negative top_n"""
    preference_sort(['foo', 'bar', 'baz'], -1)

@raises(ValueError)
def test_sort_wrong_length():
    """prefsort should raise an error on a top_n that's too large"""
    preference_sort(['foo', 'bar', 'baz'], 4)

@raises(ValueError)
def test_sort_empty(prompt_func):
    """prefsort should raise an error on a top_n that's 0"""
    preference_sort(['foo', 'bar', 'baz'], 0)

@mock.patch("prefsort.prompt_order", side_effect=always_left)
def test_sort(prompt_func):
    """Test a full sort"""
    expected = ['chicken', 'pasta', 'rice', 'salad', 'soup']
    actual = preference_sort(['soup', 'salad', 'pasta', 'chicken', 'rice'], 5)
    assert expected == actual, 'Expected {}, got {}'.format(expected, actual)

@mock.patch("prefsort.prompt_order", side_effect=always_left)
def test_sort_length(prompt_func):
    """Make sure we get the right length back"""
    expected = 2
    actual = len(preference_sort(['foo', 'bar', 'baz'], 2))
    assert expected == actual, 'Expected {}, got {}'.format(expected, actual)
