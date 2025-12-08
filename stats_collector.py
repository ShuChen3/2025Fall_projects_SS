import math
from collections import defaultdict
from game_rules import GameRules



class StatsCollector:
    def __init__(self, rules: GameRules):
        self.rules = rules
        self.total_scores = []

        # lowest game record
        self.min_score = float('inf')
        self.min_score_game_state = None


        self.upper_totals = []
        self.bonus_count = 0


        self.chance_scores = []
        self.yahtzee_hits = 0
        self.small_straight_hits = 0
        self.large_straight_hits = 0
        self.category_usage = defaultdict(int)


    def record_game(self, final_score, upper_total, got_bonus, game_state_copy):
        self.total_scores.append(final_score)
        self.upper_totals.append(upper_total)

        if got_bonus:
            self.bonus_count += 1


        if final_score < self.min_score:
            self.min_score = final_score
            self.min_score_game_state = game_state_copy


    def record_category(self, category, score):
        self.category_usage[category] += 1
        if category == "chance":
            self.chance_scores.append(score)

        if category == "yahtzee" and score == 50:
            self.yahtzee_hits += 1

        if category == "small_straight" and score == 30:
            self.small_straight_hits += 1

        if category == "large_straight" and score == 40:
            self.large_straight_hits += 1

    def report(self):
        n = len(self.total_scores)


        mean = sum(self.total_scores) / n
        min_score = min(self.total_scores)
        max_score = max(self.total_scores)

        variance = sum((x - mean) ** 2 for x in self.total_scores) / n
        std = math.sqrt(variance)

        bonus_rate = self.bonus_count / n
        avg_upper = sum(self.upper_totals) / n

        avg_chance = (
            sum(self.chance_scores) / len(self.chance_scores)
            if self.chance_scores else 0
        )


        print("\n========== strategy statistics ==========")
        print(f"Games played: {n}")
        print(f"Average Score: {mean:.2f}")
        print(f"Min Score: {min_score}")
        print(f"Max Score: {max_score}")
        print(f"Std Dev: {std:.2f}")

        print("\n--- Upper Section ---")
        print(f"Average Upper Total: {avg_upper:.2f}(Target: {self.rules.upper_bonus_threshold})")
        print(f"Bonus Hit Rate: {bonus_rate * 100:.2f}%")

        print("\n--- Special Categories ---")
        print(f"Avg Chance Score: {avg_chance:.2f}")
        print(f"Yahtzee Hit Rate: {self.yahtzee_hits / n * 100:.2f}%")
        print(f"Small Straight Hit Rate: {self.small_straight_hits / n * 100:.2f}%")
        print(f"Large Straight Hit Rate: {self.large_straight_hits / n * 100:.2f}%")

        print("\n--- Category Usage ---")
        for k, v in sorted(self.category_usage.items()):
            print(f"{k:20s} : {v}")

        # lowest game
        if self.min_score_game_state:
            print(f"\n--- Lowest Score Game Analysis (Score: {self.min_score}) ---")
            print("Category Scores Detail:")


            state = self.min_score_game_state
            all_categories = sorted(state.category_scores.keys())

            for cat in all_categories:
                scores = state.category_scores[cat]
                cat_sum = sum(scores)
                print(f"  {cat:20s}: {scores} -> Sum: {cat_sum}")

            print(f"Upper Total: {self.min_score_game_state.upper_total}")
            print(f"Upper Bonus: {self.min_score_game_state.upper_bonus}")
            print(f"TOTAL SCORE: {self.min_score_game_state.total_score}")

