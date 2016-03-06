#!/usr/bin/env python
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
        print "{} or {}?".format(left, right)
        val = raw_input("left/right> ")
        if val == 'left':
            return left, right
        elif val == 'right':
            return right, left

def pairs(data):
    """
    Take a list and generate pairs
    at a time.

    Note: Each pair is sorted.

    If data has an odd number of elements,
    this yields (item, None)

    :param list data: The list to process
    :rtype: generator of tuple
    :returns: a generator of every pair in
        the iterable.
    """
    #TODO: Can `i` be incremented by 2s instead?
    #TODO: Do the tuples really need to be sorted each time?
    i = 0
    while True:
        pair = data[2 * i: 2 * i + 2]
        if not pair:
            break
        elif len(pair) == 1:
            yield pair[0], None
        else:
            yield tuple(sorted(pair))
        i += 1

#HACK: Make this a class so rules can be a class
#member.
def preference_sort_round(data, rules={}):
    """
    Do one round of Preference Sort. elements
    are entered into a single-elimination tournament
    and the user can decide the winner at each step.
    The winner is returned separately from the rest of
    the data.

    Each choice is memoized in the rules dictionary so
    the user doesn't have to enter the same choice
    twice.

    :param list(str) data: the input elements to sort
    :param dict rules: The rules dictionary for
        memoization. The default one works fine
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
            key = (left, right)
            if key in rules:
                winner, loser = rules[key]
            else:
                winner, loser = prompt_order(left, right)
                rules[key] = (winner, loser)
            winners.append(winner)
            losers.append(loser)
        unevaluated = winners
        winners = []
    winner = unevaluated[0]
    return winner, losers

def preference_sort(data, top_n):
    """
    Let the user sort the list, or at least
    enough to get the top N elements.

    :param list(str) data: input data
    :param int top_n: return only the top N
        elements
    :rtype: list
    :returns: a list of the top N elements, ordered
        by the user's preferences.
    """
    #TODO: top_n should be the length of the list.
    if not 0 < top_n <= len(data):
        raise ValueError("The number of elements to fetch should be in the interval [1, {}]".format(len(data)))
    output = []
    for x in xrange(top_n):
        winner, data = preference_sort_round(data)
        output.append(winner)
    return output

if __name__ == '__main__':
    data = [
        "Read a book",
        "Exercise",
        "Work",
        "Eat",
        "Sleep",
        "Program something",
        "Play video games",
        "Scroll through Facebook",
        "Spend time with friends"
    ]
    top_3 = preference_sort(data, 3)
    print "You chose to do these three things:"
    for x in top_3:
        print x
