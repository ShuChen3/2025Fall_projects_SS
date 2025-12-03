"""
simulator.py

Monte Carlo Yahtzee game simulator

The simulator:
- Runs full games using a strategy callback
- Each turn has up to 3 rolls (roll + reroll1 + reroll2)
- Strategy decides which dice to keep and which category to fill
"""

from __future__ import annotations
import random
from dice_utils import roll_dice, reroll_with_keep
from game_state import GameState
################
from stats_collector import StatsCollector
from score_calculator import score_category


class Simulator:
    def __init__(self, num_dice: int = 5, max_rolls: int = 3):
        """
        :param num_dice: normally 5 in standard Yahtzee rule, but adjustable for experiments.
        :param max_rolls: normally 3 (roll + 2 rerolls).
        """
        self.num_dice = num_dice
        self.max_rolls = max_rolls

        ######################
        self.stats = StatsCollector()


    # Simulate for a single turn

    def simulate_turn(self, state: GameState, strategy) -> None:
        """
        Simulate ONE Yahtzee turn using the given strategy.

        strategy must implement:

        1) choose_dice_to_keep(dice: list[int], roll_index: int, state: GameState)
            -> returns a list[int] of indices to keep

        2) choose_category(dice: list[int], state: GameState)
            -> returns a category name string

        The simulator does NOT judge the strategy; it just follows it.
        """
        # 第1次掷骰（必须全掷）
        dice = roll_dice(self.num_dice)

        # 之后最多2次重掷机会
        for roll_index in range(2):  # roll_index=0: 还有2次机会, roll_index=1: 还有1次机会
            keep_indices = strategy.choose_dice_to_keep(dice, roll_index, state)

            if len(keep_indices) == self.num_dice:  # 策略说：我满意了，不掷了
                break

            dice = reroll_with_keep(dice, keep_indices)

        # 最终选类别
        #category = strategy.choose_category(dice, state)
        #state.apply_category(category, dice)

        #############################
        category = strategy.choose_category(dice, state)

        score = score_category(category, dice)
        self.stats.record_category(category, score)

        state.apply_category(category, dice)

    # Simulate for a full game

    def simulate_game(self, strategy) -> int:
        """
        Simulate ONE Yahtzee game using the given strategy.
        :param strategy: chosen strategy
        :return: final score of the game
        """
        state = GameState()

        while not state.is_complete():
            self.simulate_turn(state, strategy)

        #return state.total_score
        ##########################
        final_score = state.total_score
        upper_total = state.upper_total
        got_bonus = upper_total >= 63

        self.stats.record_game(final_score, upper_total, got_bonus)

        return final_score

    # Batch simulation for monte carlo

    def simulate_many(self, strategy, n:int = 1000) -> float:
        """
        Run many games using the given strategy and get the average score.
        :param strategy: chosen strategy
        :param n: number of games to simulate
        :return: average score of the games
        """

        total_score = 0
        for _ in range(n):
            total_score += self.simulate_game(strategy)
        self.stats.report()
        return total_score / n




