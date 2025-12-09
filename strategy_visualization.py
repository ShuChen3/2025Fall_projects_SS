import matplotlib.pyplot as plt
import numpy as np
from strategy_examples import RandomStrategy, GreedyStrategy, SimpleRuleStrategy, HumanLikeStrategy, AdvancedHumanLikeStrategy
from simulator import Simulator
from game_rules import GameRules

# Set game rules
# Number of dices(standard: 5)
NUM_DICE = 5

# Number of faces of each dice(standard: 6)
NUM_FACES = 6

# Times to fill each score category(standard: 1)
MAX_FILLS = 1

# Times of reroll(standard: 2)
MAX_REROLLS = 2

# Number of simulation games played
NUM_GAMES = 2000


# ==========================================

def run_simulation():
    # Create the game rule object
    current_rules = GameRules(
        num_dice=NUM_DICE,
        num_faces=NUM_FACES,
        max_category_fills=MAX_FILLS,
        max_rerolls=MAX_REROLLS
    )

    print(f"Current Game Rule: {current_rules}")

    # Initialize the Strategies
    strategies = {
        "Random": RandomStrategy(),
        "Greedy": GreedyStrategy(),
        "SimpleRule": SimpleRuleStrategy(),
        "HumanLike": HumanLikeStrategy(),
        'Advanced': AdvancedHumanLikeStrategy()
    }

    results = {}

    # Simulation
    print(f"start simulation for {NUM_GAMES} games")

    for name, strat in strategies.items():
        print(f"  Current strategy {name}...")

        # Initialize the simulator
        sim = Simulator(current_rules)

        # Run simulation
        sim.simulate_many(strat, n=NUM_GAMES)

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
                 f"Rules: {NUM_DICE} Dice, {NUM_FACES} Faces, "
                 f"{MAX_FILLS}x Fills, {MAX_REROLLS} Roll time(s)")
    plt.title(title_str, fontsize=12, fontweight='bold')

    plt.legend(fontsize=10)
    plt.grid(True, linestyle='--', alpha=0.6)

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    run_simulation()