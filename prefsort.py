#!/usr/bin/env python
import sys
from six.moves import input, range

def prompt_order(left, right):
    """
    Prompt the user to select between
    two options, for now called 'left'
    and 'right'.

    :param any left: the left object
    :param any right: the right object
    :rtype: tuple
    :returns: (winner, loser), where
        the winner is the object the
        user picks (of left, right)
        and the loser is the other one
    """
    while True:
        print("{} or {}?".format(left, right))
        val = input("left/right> ")
        if val == 'left':
            return left, right
        elif val == 'right':
            return right, left

def pairs(data):
    """
    Take a list and generate pairs
    at a time.

    If data has an odd number of elements,
    this yields (item, None)

    :param list data: The list to process
    :rtype: generator of tuple
    :returns: a generator of every pair in
        the iterable.
    """
    #Index of the left element
    i = 0
    while True:
        pair = data[i: i + 2]
        if not pair:
            break
        elif len(pair) == 1:
            yield pair[0], None
        else:
            yield tuple(pair)
        i += 2

class PreferenceSort(object):
    """
    Preference Sort Class
    """
    def __init__(self, data):
        self.rules = {}
        self.data = data

    def sort(self, top_n=None):
        """
        Sort the list.

        :param int top_n: instead of returning the
            whole sorted list, return the top N elements.

        :rtype: list
        :returns: a list of all the elements, sorted
            according to user preference.
        """
        # Sorting the whole list is equvalent to
        # getting the top N elements where N is the
        # length of this list
        if top_n is None:
            top_n = len(self.data)
        return self.__top_n(top_n)

    def __top_n(self, n):
        """
        Get the top N elements,
        sorting partially if needed.

        :param int n: the number of elements to grab
        :rtype: list
        :returns: a list of the top N elements.
        """
        if not 0 <= n <= len(self.data):
            raise ValueError(("The number of elements to fetch should be in "
                "the interval [1, {}]").format(len(self.data)))
        output = []
        data = self.data
        for x in range(n):
            winner, data = self.__sort_round(data)
            output.append(winner)
        return output

    #TODO: Can self.rules store list indices instead of the
    #strings themselves?
    #TODO: Can we memoize winners and pop old rules.
    def __sort_round(self, data):
        """
        Perform one round of Preference sort, selecting
        the top element of the remaining element.

        Elements are sorted with a single-elimination
        tournament where the user gets to decide the winner
        at each step.

        Each choice is memoized so the user doesn't have
        to enter the same choice twice.
        :param list data: the data for use in this round. This is
            a subset of self.data.
        :rtype: (str, [str])
        :returns: (winner, losers) where winner
            is the user's top pick. losers
            is every other element. losers is not
            sorted in any way. If the input list is empty,
            returns (None, []). If the input list is of length
            one, returns (winner, [])
        """
        if not data:
            return (None, [])

        winners = []
        losers = []
        unevaluated = data
        while len(unevaluated) > 1:
            for left, right in pairs(unevaluated):
                if right is None:
                    winners.append(left)
                    continue
                winner, loser = self.__choose_winner(left, right)
                winners.append(winner)
                losers.append(loser)
            unevaluated = winners
            winners = []
        winner = unevaluated[0]
        return winner, losers

    def __choose_winner(self, left, right):
        """
        Have the user choose a winner, memoizing where possible.

        :param str left: left string choice
        :param str right: right string choice
        """
        key = tuple(sorted((left, right)))
        if key in self.rules:
            return self.rules[key]
        else:
            # Memoize the choice
            winner, loser = prompt_order(left, right)
            self.rules[key] = (winner, loser)
            return winner, loser

if __name__ == '__main__':
    #TODO: Argparse arguments
    try:
        fname = sys.argv[1]
        with open(fname, 'rb') as f:
            data = [line.rstrip() for line in f]
        top_3 = PreferenceSort(data).sort(3)
        print("You chose to do these three things:")
        for x in top_3:
            print(x)
    except Exception as e:
        print("Error: {}".format(e))
        print("Usage: ./prefsort.py filename")
