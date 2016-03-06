import mock
from prefsort import *
from nose.tools import raises

def experiment(expected, actual):
    """Boilerplate testing method. FOR SCIENCE!"""
    assert expected == actual, "Expected {}, got {}".format(expected, actual)

def test_pairs_empty():
    """Test that pairs works for an empty list"""
    expected = []
    actual = list(pairs([]))
    experiment(expected, actual)

def test_pairs_odd():
    """Test that pairs works for odd length lists"""
    expected = [(1, 2), (3, None)]
    actual = list(pairs([1, 2, 3]))
    experiment(expected, actual)

def test_pairs_even():
    """Test that pairs works for even length lists"""
    expected = [(1, 2), (3, 4)]
    actual = list(pairs([1, 2, 3, 4]))
    experiment(expected, actual)

def always_left(a, b):
    """Pretend the user always enters 'left'"""
    return a, b

@raises(ValueError)
def test_sort_negative_length():
    """prefsort should raise an error on negative top_n"""
    PreferenceSort(['foo', 'bar', 'baz']).sort(-1)

@raises(ValueError)
def test_sort_wrong_length():
    """prefsort should raise an error on a top_n that's too large"""
    PreferenceSort(['foo', 'bar', 'baz']).sort(4)

def test_sort_no_data():
    """prefsort should return an empty list if the input data is empty"""
    expected = []
    actual = PreferenceSort([]).sort()
    experiment(expected, actual)

@mock.patch("prefsort.prompt_order")
def test_sort_one_item(prompt_func):
    """prefsort should return the first element without prompting the user"""
    expected = ['foo']
    actual = PreferenceSort(['foo']).sort()
    experiment(expected, actual)
    assert not prompt_func.called

@mock.patch("prefsort.prompt_order", side_effect=always_left)
def test_sort_full(prompt_func):
    """Test a full sort"""
    ps = PreferenceSort(['soup', 'salad', 'pasta', 'chicken', 'rice'])
    expected = ['soup', 'salad', 'pasta', 'chicken', 'rice']
    actual = ps.sort()
    experiment(expected, actual)

@mock.patch("prefsort.prompt_order", side_effect=always_left)
def test_sort_length(prompt_func):
    """Make sure we get the right length back"""
    expected = 2
    ps = PreferenceSort(['foo', 'bar', 'baz'])
    actual = len(ps.sort(2))
    experiment(expected, actual)

@mock.patch("prefsort.prompt_order", side_effect=always_left)
def test_sort_again(prompt_func):
    """If the same sort is done again, the user should not be prompted"""
    ps = PreferenceSort(['foo', 'bar', 'baz', 'qux', 'quux'])
    expected = ps.sort(3)
    actual = ps.sort(3)
    experiment(expected, actual)
