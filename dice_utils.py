"""
dice_utils.py


"""

import random


def roll_dice(n: int = 5) -> list[int]:
    """
    Roll a fair six-sided dice.

    :param n: number of dice to roll (default 5)
    :return: list of dice value (1 - 6)
    """

    return [random.randint(1, 6) for _ in range(n)]


def get_indices_to_reroll(dice: list[int], keep_indices: list[int]) -> list[int]:
    """
    Based on dice and list of indices to keep, return indices to reroll.
    :param dice: current dice
    :param keep_indices: indices of dice to keep
    :return: indices of dice to reroll
    """
    return [i for i in range(len(dice)) if i not in keep_indices]



def reroll_indices(dice: list[int], indices_to_roll: list[int]) -> list[int]:
    """
    Reroll specific dice based on the indices provided

    :param dice: current dice value
    :param indices_to_roll: list of indices to reroll
    :return: updated dice after rerolling selected indices
    """

    new_dice = dice[:]
    for index in indices_to_roll:
        new_dice[index] = random.randint(1, 6)
    return new_dice

def reroll_with_keep(dice: list[int], keep_indices: list[int]) -> list[int]:
    """
    Re-roll all dice except those at keep_indices
    :param dice: current dice
    :param keep_indices: indices of dice to keep
    :return: updated dice after reroll
    """
    indices_to_reroll = get_indices_to_reroll(dice, keep_indices)
    return reroll_indices(dice, indices_to_reroll)


def count_value(dice: list[int]) -> list[int]:
    """
    count how many times each face (1 - 6) appears in dice
    :param dice: list of dice values
    :return: List[int] counts[0] is count of 1s, ... counts[5] is count of 6s
    """
    counts = [0] * 6
    for value in dice:
        counts[value - 1] += 1
    return counts






