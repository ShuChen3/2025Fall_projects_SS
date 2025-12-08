from dataclasses import dataclass


@dataclass
class GameRules:
    """
    Store all variable rule parameters
    """
    # Number of dices (standard rule: 5)
    num_dice: int = 5
    # Number of faces on a die (standard: 6)
    num_faces: int = 6
    # Number of time player can reroll (standard: 2)
    max_rerolls: int = 2
    # The number of times each category can be filled in (standard: 1)
    max_category_fills: int = 1
    # Upper section bonus reward
    upper_bonus_reward: int = 35

    # Calculate the threshold to get upper section bonus for different face of dices
    @property
    def upper_bonus_threshold(self) -> int:
        return sum(range(1, self.num_faces + 1)) * 3

    def __repr__(self):
        """
        Print the rule
        """
        return (f"GameRules(dice={self.num_dice}, faces={self.num_faces}, "
                f"rerolls={self.max_rerolls}, fills={self.max_category_fills}, "
                f"bonus_thresh={self.upper_bonus_threshold})")