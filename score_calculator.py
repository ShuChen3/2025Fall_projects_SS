"""
score_calculator.py

Compute Yahtzee for each category
"""
from collections import Counter


# Upper Section Scoring

def score_aces(dice: list[int]) -> int:
    return sum(d for d in dice if d == 1)

def score_twos(dice: list[int]) -> int:
    return sum(d for d in dice if d == 2)

def score_threes(dice: list[int]) -> int:
    return sum(d for d in dice if d == 3)

def score_fours(dice: list[int]) -> int:
    return sum(d for d in dice if d == 4)

def score_fives(dice: list[int]) -> int:
    return sum(d for d in dice if d == 5)

def score_sixes(dice: list[int]) -> int:
    return sum(d for d in dice if d == 6)

# Lower Section Scoring
def score_three_of_a_kind(dice: list[int]) -> int:
    counts = Counter(dice)
    if any(c >= 3 for c in counts.values()):
        return sum(dice)
    return 0

def score_four_of_a_kind(dice: list[int]) -> int:
    counts = Counter(dice)
    if any(c >= 4 for c in counts.values()):
        return sum(dice)
    return 0

def score_full_house(dice: list[int]) -> int:
    counts = Counter(dice).values()
    if sorted(counts) == [2, 3]:
        return 25
    return 0

def score_small_straight(dice: list[int]) -> int:
    unique = set(dice)
    straights = [
        {1, 2, 3, 4},
        {2, 3, 4, 5},
        {3, 4, 5, 6}
    ]
    if any(straight <= unique for straight in straights):
        return 30
    return 0

def score_large_straight(dice: list[int]) -> int:
    unique = set(dice)
    if unique == {1, 2, 3, 4, 5} or unique == {2, 3, 4, 5, 6}:
        return 40
    return 0

def score_yahtzee(dice: list[int]) -> int:
    if len(set(dice)) == 1:
        return 50
    else:
        return 0

def score_chance(dice: list[int]) -> int:
    return sum(dice)

def is_small_straight(dice: list[int]) -> bool:
    unique = set(dice)
    straights = [
        {1, 2, 3, 4},
        {2, 3, 4, 5},
        {3, 4, 5, 6},
    ]
    return any(straight <= unique for straight in straights)


def is_large_straight(dice: list[int]) -> bool:
    unique = set(dice)
    return unique == {1,2,3,4,5} or unique == {2,3,4,5,6}


# Unified Scoring Interface


CATEGORY_FUNCTIONS = {
    'aces': score_aces,
    'twos': score_twos,
    'threes': score_threes,
    'fours': score_fours,
    'fives': score_fives,
    'sixes': score_sixes,
    'three_of_a_kind': score_three_of_a_kind,
    'four_of_a_kind': score_four_of_a_kind,
    'full_house': score_full_house,
    'small_straight': score_small_straight,
    'large_straight': score_large_straight,
    'yahtzee': score_yahtzee,
    'chance': score_chance,
}

def score_category(category: str, dice: list[int]) -> int:
    if category not in CATEGORY_FUNCTIONS:
        raise ValueError(f'Unknown category: {category}')
    return CATEGORY_FUNCTIONS[category](dice)