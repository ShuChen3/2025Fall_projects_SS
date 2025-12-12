import matplotlib.pyplot as plt
import numpy as np
from strategy_examples import RandomStrategy, GreedyStrategy, SimpleRuleStrategy, HumanLikeStrategy, AdvancedHumanLikeStrategy
from simulator import Simulator
from game_rules import GameRules


def run_simulation(rules: GameRules, num_games: int = 2000):

    print(f"Current Game Rule: {rules}")

    # Initialize the Strategies
    strategies = {
        "Random": RandomStrategy(),
        "Greedy": GreedyStrategy(),
        "SimpleRule": SimpleRuleStrategy(),
        "HumanLike": HumanLikeStrategy(),
        'AdvancedHumanLike': AdvancedHumanLikeStrategy()
    }

    results = {}

    # Simulation
    print(f"start simulation for {num_games} games")

    for name, strat in strategies.items():
        print(f"  Current strategy {name}...")

        # Initialize the simulator
        sim = Simulator(rules)

        # Run simulation
        sim.simulate_many(strat, n=num_games)

        # Record all scores for visualization
        results[name] = sim.stats.total_scores

    # Create the plot
    plt.figure(figsize=(12, 7))

    for name, scores in results.items():
        cumsum = np.cumsum(scores)
        running_avg = cumsum / (np.arange(len(scores)) + 1)

        plt.plot(running_avg, label=f"{name} (Final Avg: {running_avg[-1]:.1f})", linewidth=2)

    plt.xlabel("Number of Games Played", fontsize=12)
    plt.ylabel("Average Score", fontsize=12)

    title_str = (f"Yahtzee Strategy Comparison\n"
                 f"Rules: {rules.num_dice} Dice, {rules.num_faces} Faces, "
                 f"{rules.max_category_fills}x Fill(s), {rules.max_rerolls} Reroll time(s)")
    plt.title(title_str, fontsize=12, fontweight='bold')

    plt.legend(fontsize=10, loc='upper right', frameon=0.5)
    plt.grid(True, linestyle='--', alpha=0.6)

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    # Set custom game rule
    Game_rules = GameRules(
        num_dice=5,
        num_faces=6,
        max_category_fills=1,
        max_rerolls=2
    )

    # Run the simulation
    run_simulation(Game_rules, num_games=2000)