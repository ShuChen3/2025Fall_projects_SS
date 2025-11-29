"""
game_state.py

Manage the state of the Yahtzee game
"""
from __future__ import annotations
from copy import deepcopy



from score_calculator import score_category


UPPER_CATEGORIES = ['aces', 'twos', 'threes', 'fours', 'fives', 'sixes']
LOWER_CATEGORIES = ['three_of_a_kind', 'four_of_a_kind', 'full_house',
                    'small_straight', 'large_straight', 'yahtzee', 'chance']

class GameState:
    """
    Represents the state of the Yahtzee game
    """

    def __init__(self):
        # category_scores: dict[str, int | None]
        # None = not yet filled
        self.category_scores = {cat: None for cat in UPPER_CATEGORIES + LOWER_CATEGORIES}

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
        return [cat for cat, score in self.category_scores.items() if score is None]

    def is_complete(self) -> bool:
        """
        Game is complete if all categories are filled
        """
        return all(score is not None for score in self.category_scores.values())

    def copy(self) -> "GameState":
        """
        Return a deep copy for Monte Carlo Branching
        """
        return deepcopy(self)

    # Apply scoring

    def apply_category(self, category: str, dice: list[int]) -> None:
        """
        Assign the dice result to a scoring category
        Update upper section totals, bonus, and total game score
        """

        if category not in self.category_scores:
            raise ValueError(f'Unknown category: {category}')

        if self.category_scores[category] is not None:
            raise ValueError(f"Category'{category} 'already filled")

        # Compute score using the score module
        score = score_category(category, dice)

        # Set the category score
        self.category_scores[category] = score

        # Update upper section tally if needed
        if category in UPPER_CATEGORIES:
            self.upper_total += score

            # Check for bonus (only once)
            if self.upper_total >= 63 and self.upper_bonus == 0:
                self.upper_bonus = 35

        # Update total score
        lower_filled_scores = [
            s for cat, s in self.category_scores.items()
            if cat in LOWER_CATEGORIES and s is not None
        ]
        self.total_score = self.upper_total + self.upper_bonus + sum(lower_filled_scores)

        #  Debug / display
    def __repr__(self):
        return (
            f"GameState(upper_total={self.upper_total}, "
            f"upper_bonus={self.upper_bonus}, "
            f"total_score={self.total_score}, "
            f"filled={[(c, s) for c, s in self.category_scores.items() if s is not None]})"
        )