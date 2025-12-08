"""
score_calculator.py

Compute Yahtzee for each category
"""
from collections import Counter
from game_rules import GameRules


# Upper Section Scoring

# def score_value(dice, value) -> int:
#  return count_value(dice)[value-1]

def score_upper_generic(dice: list[int], target_value: int) -> int:
    """
    Calculate score for specific value of dices for upper section
    :param dice: input list of dices
    :param target_value: The value to calculate score for
    :return: score
    """
    return sum(d for d in dice if d == target_value)

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
def score_n_of_a_kind(dice: list[int], n: int) -> int:
    """
    N_of_a_kind (3 of a kind, 4 of a kind)
    :param dice: input list of dices
    :param n: number of a kind
    :return: score
    """
    counts = Counter(dice)
    if any(c >= n for c in counts.values()):
        return sum(dice)
    return 0

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
    # if sorted(counts) == [2, 3]:
    #     return 25
    # return 0
    c_list = list(counts)
    if 3 in c_list and 2 in c_list:
        return 25
    return 0


def score_straight_generic(dice: list[int], length_needed: int, fixed_score: int) -> int:
    """
    calculate score for straight

    :param dice: input list of dices
    :param length_needed: length of straight
    :param fixed_score: score for straight
    :return: score
    """
    unique_dice = sorted(set(dice))
    if len(unique_dice) < length_needed:
        return 0

    consecutive_count = 1
    max_consecutive = 1

    for i in range(len(unique_dice) - 1):
        if unique_dice[i + 1] == unique_dice[i] + 1:
            consecutive_count += 1
            max_consecutive = max(max_consecutive, consecutive_count)
        else:
            consecutive_count = 1

    if max_consecutive >= length_needed:
        return fixed_score
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


class ScoreCalculator:
    def __init__(self, rules: GameRules):
        self.rules = rules
        self.category_functions = {}
        self.register_functions()

    def register_functions(self):
        # upper section
        for i in range(1, self.rules.num_faces + 1):
            category_name = f"upper_{i}"
            self.category_functions[category_name] = lambda d, val=i: score_upper_generic(d, val)

        # lower section
        self.category_functions['three_of_a_kind'] = lambda d:score_n_of_a_kind(d, 3)
        self.category_functions['four_of_a_kind'] = lambda d:score_n_of_a_kind(d, 4)
        self.category_functions['full_house'] = score_full_house
        self.category_functions['yahtzee'] = score_yahtzee
        self.category_functions['chance'] = score_chance

        # for straight
        self.category_functions['small_straight'] = lambda d: score_straight_generic(d, length_needed= 4, fixed_score=30)
        self.category_functions['large_straight'] = lambda d: score_straight_generic(d, length_needed= 5, fixed_score=40)

    def calculate(self, category: str, dice: list[int]) -> int:

        if category not in self.category_functions:
            raise ValueError(f'Unknown category: {category}')

        return self.category_functions[category](dice)

    def get_all_categories(self) -> list[str]:
        return list(self.category_functions.keys())