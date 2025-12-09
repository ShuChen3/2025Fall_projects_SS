"""
strategy.py

Strategies adapted for Dynamic GameRules.
"""
import random
from game_state import GameState
from dice_utils import get_longest_straight

# RandomStrategy: Randomly choose dice to keep and randomly put them in category
class RandomStrategy:
    def choose_dice_to_keep(self, dice: list[int], _roll_index: int, _state: GameState) -> list[int]:
        num_dice = len(dice)
        if num_dice == 0: return []

        k = random.randint(0, num_dice)
        indices = random.sample(range(num_dice), k)
        return indices

    def choose_category(self, _dice: list[int], state: GameState) -> str:
        available = state.available_categories()
        return random.choice(available)

# GreedyStrategy: Keep the dice with most frequent value and put in the highest score category
class GreedyStrategy:
    def choose_dice_to_keep(self, dice: list[int], _roll_index: int, _state: GameState) -> list[int]:
        counts = Counter(dice)
        if not counts: return []
        most_common_val = counts.most_common(1)[0][0]

        return [i for i, x in enumerate(dice) if x == most_common_val]

    def choose_category(self, dice: list[int], state: GameState) -> str:
        available = state.available_categories()
        best_cat = available[0]
        max_score = -1

        for cat in available:
            score = state.score_calc.calculate(cat, dice)
            if score > max_score:
                max_score = score
                best_cat = cat

        return best_cat

# SimpleRuleStrategy: follow simple pre-set rules to choose dice to keep and put score in category
class SimpleRuleStrategy:
    def choose_dice_to_keep(self, dice: list[int], _roll_index: int, _state: GameState) -> list[int]:
        # Check straight
        seq = get_longest_straight(dice)

        if len(seq) >= 3:
            return [i for i, x in enumerate(dice) if x in seq]

        # Keep most frequent value
        counts = Counter(dice)
        if not counts: return []
        most_common_val = counts.most_common(1)[0][0]
        return [i for i, x in enumerate(dice) if x == most_common_val]

    def choose_category(self, dice: list[int], state: GameState) -> str:
        available = state.available_categories()

        # Calculate the scores for all available categories in advance
        scores = {cat: state.score_calc.calculate(cat, dice) for cat in available}

        # Create a dist for categories' priority
        # Highest priority： special values
        priority_list = ['yahtzee', 'large_straight', 'small_straight', 'full_house']

        # Second priority: upper sections from high values to low
        num_faces = state.rules.num_faces
        upper_priority = [f'upper_{i}' for i in range(num_faces, 0, -1)]
        priority_list.extend(upper_priority)

        # last priority: rest of lower section categories
        priority_list.extend(['four_of_a_kind', 'three_of_a_kind', 'chance'])

        for cat in priority_list:
            if cat in available:
                s = scores[cat]
                if cat == 'yahtzee' and s < 50: continue
                if cat == 'large_straight' and s < 40: continue
                if cat == 'small_straight' and s < 30: continue
                if cat == 'full_house' and s < 25: continue

                # for other categories, fill in if it has score
                if s > 0:
                    return cat

        # Sacrifice priority
        dump_order = [f'upper_{i}' for i in range(1, num_faces + 1)]
        dump_order.extend(['yahtzee', 'four_of_a_kind', 'large_straight', 'chance'])


        for cat in dump_order:
            if cat in available: return cat

        return available[0]



# HumanLike Strategy: mimic human player's strategy
class HumanLikeStrategy:

    def _get_upper_cat(self, val: int) -> str:
        return f"upper_{val}"

    def choose_dice_to_keep(self, dice: list[int], _roll_index: int, state: GameState) -> list[int]:
        counts = Counter(dice)
        if not counts: return []

        most_common = counts.most_common(1)
        most_common_val, max_count = most_common[0]

        num_dice = state.rules.num_dice
        num_faces = state.rules.num_faces

        # Keep all if all dices are same
        if max_count == num_dice:
            return list(range(len(dice)))

        consecutive_seq = get_longest_straight(dice)
        consecutive_len = len(consecutive_seq)

        # Check for large straight
        if consecutive_len >= 5:
            return list(range(len(dice)))

        # Try to make straight if there are straight categories available
        if consecutive_len >= 4:
            needs_small = 'small_straight' in state.available_categories()
            needs_large = 'large_straight' in state.available_categories()
            if needs_small or needs_large:
                return [i for i, x in enumerate(dice) if x in consecutive_seq]

        # Try Upper section score. Keep >=2 biggest value
        potential_vals = sorted([v for v, c in counts.items() if c >= 2], reverse=True)

        target_val = 0
        for val in potential_vals:
            cat = self._get_upper_cat(val)
            if cat in state.available_categories():
                target_val = val
                break

        # If no >=2 category available, keep the most common value
        if target_val == 0:
            target_val = most_common_val

        if counts[target_val] >= 2:
            return [i for i, x in enumerate(dice) if x == target_val]

        # Backup strategy: Keep 1 of the largest numbers that correspond to the unoccupied positions in the upper section.
        for val in range(num_faces, 0, -1):
            cat = self._get_upper_cat(val)
            if cat in state.available_categories() and val in dice:
                return [i for i, x in enumerate(dice) if x == val][:1]

        return []

    def choose_category(self, dice: list[int], state: GameState) -> str:
        available = state.available_categories()
        scores = {cat: state.score_calc.calculate(cat, dice) for cat in available}
        counts = Counter(dice)

        num_faces = state.rules.num_faces


        total_slots = len(state.score_calc.get_all_categories()) * state.rules.max_category_fills
        # Calculate filled in times
        filled_count = sum(len(s) for s in state.category_scores.values())
        remaining_slots = total_slots - filled_count
        # Set the rest 30% categories left as late game phase
        is_late_game = remaining_slots <= (total_slots * 0.3)


        # Rules for filling in the category
        # Get directly if satisfied
        if 'yahtzee' in available and scores['yahtzee'] == 50: return 'yahtzee'
        if 'large_straight' in available and scores['large_straight'] == 40: return 'large_straight'
        if 'small_straight' in available and scores['small_straight'] == 30:
            return 'small_straight'
        if is_late_game and 'full_house' in available and scores['full_house'] == 25: return 'full_house'


        # Go through upper section from large value
        for val in range(num_faces, num_faces // 2, -1):
            cat = self._get_upper_cat(val)
            if cat in available:
                # If have more than 4 times
                if counts[val] >= 4: return cat
                # If have more than 3 times
                if counts[val] >= 3 and scores[cat] >= val * 3: return cat

        # Set threshold for lower section categories
        if 'four_of_a_kind' in available and scores['four_of_a_kind'] >= sum(dice) * 0.7:
            return 'four_of_a_kind'
        if 'full_house' in available and scores['full_house'] == 25: return 'full_house'
        if 'three_of_a_kind' in available and scores['three_of_a_kind'] >= sum(dice) * 0.6:
            return 'three_of_a_kind'

        # Get chance when it passed the threshold
        max_chance_score = num_faces * state.rules.num_dice
        if 'chance' in available and scores['chance'] >= max_chance_score * 0.7:
            return 'chance'

        # Get low value upper section score
        for val in range(1, 3):
            cat = self._get_upper_cat(val)
            if cat in available and scores[cat] > 0: return cat

        # Late game strategy
        if is_late_game:
            for val in range(num_faces, num_faces - 3, -1):
                cat = self._get_upper_cat(val)
                if cat in available and counts[val] >= 2: return cat

        # Dump strategy
        dump_cats = [self._get_upper_cat(i) for i in range(1, 4)]
        for cat in dump_cats:
            if cat in available: return cat

        if 'chance' in available: return 'chance'
        if 'yahtzee' in available: return 'yahtzee'
        if 'large_straight' in available: return 'large_straight'
        return available[0]


from collections import Counter
from game_state import GameState


class AdvancedHumanLikeStrategy:

    def _get_upper_cat(self, face: int) -> str:
        """Helper to generate category name like 'upper_1', 'upper_6'"""
        return f"upper_{face}"

    def _needs_upper_bonus(self, state: GameState) -> bool:
        """
        To check if is it still realistic to hit the bonus threshold.
        Optimistic bound: assume we might still get 3 of each remaining face slot.
        """
        target = state.rules.upper_bonus_threshold
        current_upper = state.upper_total

        optimistic_future = 0
        num_faces = state.rules.num_faces
        max_fills = state.rules.max_category_fills

        for face in range(1, num_faces + 1):
            cat = self._get_upper_cat(face)
            current_fills = len(state.category_scores.get(cat, []))
            remaining_slots = max_fills - current_fills

            if remaining_slots > 0:
                optimistic_future += remaining_slots * (face * 3)

        return (current_upper + optimistic_future) >= target


    def choose_dice_to_keep(self, dice: list[int], roll_index: int, state: GameState) -> list[int]:
        counts = Counter(dice)
        available = state.available_categories()

        if not dice: return []

        # get the most frequent face value
        most_common = counts.most_common(1)
        most_common_value, count = most_common[0]

        upper_needed = self._needs_upper_bonus(state)
        num_faces = state.rules.num_faces
        num_dice = state.rules.num_dice

        # First Priority: Yahtzee: if we have greater than n-1 dices, keep for yahtzee
        threshold = max(4, num_dice - 1)
        if 'yahtzee' in available and count >= threshold:
            return [i for i, x in enumerate(dice) if x == most_common_value]

        # Second priority: Strong upper section focus (Dynamic loop: from high value to low)
        for face in range(num_faces, 0, -1):
            cat = self._get_upper_cat(face)
            if cat in available and counts[face] >= 2:
                # Only keep bigger face which is > num_faces / 2
                is_high_face = face > (num_faces / 2)
                if upper_needed or is_high_face:
                    return [i for i, x in enumerate(dice) if x == face]

        # Third priority: Straights
        if 'large_straight' in available or 'small_straight' in available:
            # find longest consecutive run
            max_seq = get_longest_straight(dice)

            # If have 4+ in a run or sufficient for small straight
            if len(max_seq) >= 4:
                # check conditions for strong Upper Section Triple override
                if count >= 3 and most_common_value > (num_faces / 2):
                    cat_name = self._get_upper_cat(most_common_value)
                    if cat_name in available and upper_needed:
                        return [i for i, x in enumerate(dice) if x == most_common_value]

                # otherwise keep the straight
                return [i for i, x in enumerate(dice) if x in max_seq]

            # If we have only 3 in sequence like 2,3,4 -> only worth keeping on the first reroll
            if len(max_seq) == 3 and roll_index == 0:
                return [i for i, x in enumerate(dice) if x in max_seq]

        # Fourth priority: Triples
        if count >= 3:
            return [i for i, x in enumerate(dice) if x == most_common_value]

        # Fifth priority: Pairs, build toward triples, especially of big numbers
        if count == 2:
            is_high_face = most_common_value > (num_faces / 2)
            cat_name = self._get_upper_cat(most_common_value)

            if is_high_face or (upper_needed and cat_name in available):
                return [i for i, x in enumerate(dice) if x == most_common_value]

        # Last priority: keep best single high die for top 3 face values
        start_face = num_faces
        end_face = max(0, num_faces - 3)
        for face in range(start_face, end_face, -1):
            cat = self._get_upper_cat(face)
            if counts[face] >= 1 and (cat in available or 'chance' in available):
                return [i for i, x in enumerate(dice) if x == face]

        # If not hit anything above, reroll all dices
        return []

    def choose_category(self, dice: list[int], state: GameState) -> str:
        available = state.available_categories()
        scores = {cat: state.score_calc.calculate(cat, dice) for cat in available}
        upper_needed = self._needs_upper_bonus(state)
        num_faces = state.rules.num_faces

        # Take Yahtzee if hit it
        if 'yahtzee' in available and scores.get('yahtzee', 0) == 50:
            return 'yahtzee'

        # Take large straight if hit it
        if 'large_straight' in available and scores.get('large_straight', 0) > 0:
            return 'large_straight'

        # Take small straight if hit it
        if 'small_straight' in available and scores.get('small_straight', 0) == 30:
            return 'small_straight'

        # Upper section priority
        for face in range(num_faces, 0, -1):
            cat = self._get_upper_cat(face)
            if cat in available:
                sc = scores[cat]
                if sc >= face * 3:
                    return cat
                # If need for bonus, can take face * 2
                if upper_needed and sc >= face * 2:
                    return cat

        # Take Full house if hit it
        if 'full_house' in available and scores.get('full_house', 0) == 25:
            return 'full_house'

        # 4-of-a-kind, 3-of-a-kind, Chance
        priority_cats = [c for c in ['four_of_a_kind', 'three_of_a_kind', 'chance'] if c in available]
        if priority_cats:
            best_cat = max(priority_cats, key=lambda c: scores[c])
            # Only take if score > 0
            if scores[best_cat] > 0:
                return best_cat

        # Dump Logic
        # Calculate game progress
        total_slots = len(state.score_calc.get_all_categories()) * state.rules.max_category_fills
        filled_count = sum(len(s) for s in state.category_scores.values())
        # Early game definition: < 40% filled is early
        is_early_game = filled_count < (total_slots * 0.4)

        # Dynamically generation dump order
        mid_point = num_faces // 2
        low_upper_cats = [self._get_upper_cat(i) for i in range(1, mid_point + 1)]


        if is_early_game:
            # Early: dump Yahtzee first, then low upper
            dump_order = ['yahtzee'] + low_upper_cats + ['four_of_a_kind', 'large_straight']
        else:
            # Late: dump low upper first
            dump_order = low_upper_cats + ['four_of_a_kind', 'yahtzee', 'large_straight']

        for cat in dump_order:
            if cat in available:
                return cat

        return available[0]