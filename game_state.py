"""
game_state.py

Manage the state of the Yahtzee game
"""
from __future__ import annotations
from copy import deepcopy
from game_rules import GameRules
from score_calculator import ScoreCalculator

from score_calculator import score_category


# UPPER_CATEGORIES = ['aces', 'twos', 'threes', 'fours', 'fives', 'sixes']
# LOWER_CATEGORIES = ['three_of_a_kind', 'four_of_a_kind', 'full_house',
#                     'small_straight', 'large_straight', 'yahtzee', 'chance']

class GameState:
    """
    Represents the state of the Yahtzee game
    """

    def __init__(self, rules: GameRules, score_calc:ScoreCalculator):
        # category_scores: dict[str, int | None]
        # None = not yet filled
        self.rules = rules
        self.score_calc = score_calc
        # self.category_scores = {cat: None for cat in UPPER_CATEGORIES + LOWER_CATEGORIES}
        all_cats = self.score_calc.get_all_categories()
        self.category_scores: dict[int, list[int]] = {cat: [] for cat in all_cats}

        # Bonus tracking
        self.upper_total = 0
        self.upper_bonus = 0
        self.lower_total = 0
        # total score
        self.total_score = 0

        # Helpers

    def available_categories(self) -> list[int]:
        """
        Return list of categories not filled
        """
        # return [cat for cat, score in self.category_scores.items() if score is None]
        return [
            cat for cat, scores in self.category_scores.items()
            if len(scores) < self.rules.max_category_fills
        ]
    def is_complete(self) -> bool:
        """
        Game is complete if all categories are filled
        """
        # return all(score is not None for score in self.category_scores.values())
        for scores in self.category_scores.values():
            if len(scores) < self.rules.max_category_fills:
                return False
        return True


    def copy(self) -> "GameState":
        """
        Return a deep copy for Monte Carlo Branching
        """
        new_state = GameState(self.rules, self.score_calc)
        new_state.category_scores = deepcopy(self.category_scores)
        new_state.upper_total = self.upper_total
        new_state.upper_bonus = self.upper_bonus
        new_state.lower_total = self.lower_total
        new_state.total_score = self.total_score

        return new_state
        #return deepcopy(self)

    # Apply scoring

    def update_totals(self):
        self.upper_total = 0
        self.lower_total = 0

        for cat, scores in self.category_scores.items():
            cat_sum = sum(scores)

            if cat.startswith('upper_'):
                self.upper_total += cat_sum
            else:
                self.lower_total += cat_sum

        self.upper_bonus = 0
        if self.upper_total >= self.rules.upper_bonus_threshold:
            self.upper_bonus = self.rules.upper_bonus_reward

        self.total_socre = self.upper_total + self.upper_bonus + self.lower_total

    def apply_category(self, category: str, dice: list[int]) -> None:
        """
        Assign the dice result to a scoring category
        Update upper section totals, bonus, and total game score
        """

        if category not in self.category_scores:
            raise ValueError(f'Unknown category: {category}')

        current_fills = self.category_scores[category]

        # check if over the maximum fill in times
        if len(current_fills) < self.rules.max_category_fills:
            raise ValueError(f'Category {category} is full(max {self.rules.max_category_fills})')

        # calculate the score
        score = self.score_calc.calculate(category, dice)

        # record the score
        self.category_scores[category].append(score)

        # update total score
        self.update_totals()




        # if self.category_scores[category] is not None:
        #     raise ValueError(f"Category'{category} 'already filled")

        # # Compute score using the score module
        # score = score_category(category, dice)
        #
        # # Set the category score
        # self.category_scores[category] = score
        #
        # # Update upper section totals if needed
        # if category in UPPER_CATEGORIES:
        #     self.upper_total += score
        #
        #     # Check for bonus (only once)
        #     if self.upper_total >= 63 and self.upper_bonus == 0:
        #         self.upper_bonus = 35
        #
        # # Update total score
        # lower_filled_scores = [
        #     s for cat, s in self.category_scores.items()
        #     if cat in LOWER_CATEGORIES and s is not None
        # ]
        # self.total_score = self.upper_total + self.upper_bonus + sum(lower_filled_scores)

        #  Debug / display
    def __repr__(self):
        filled_count = sum(len(s) for s in self.category_scores.values())
        total_slots = len(self.category_scores) * self.rules.max_category_fills
        return (
            f"GameState(upper_total={self.upper_total}, "
            f"upper={self.upper_total}/{self.rules.upper_bonus_threshold}, "
            # f"total_score={self.total_score}, "
            # 
            f"progress={filled_count}/{total_slots}, "
        )