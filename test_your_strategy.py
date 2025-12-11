from game_rules import GameRules
from simulator import Simulator
from strategy_examples import *

"""
Before start the simulation, uncomment the self.stats.report() in simulate_many() in the simulator.py
so that it will show the stats result.
"""

# Set rules
rules = GameRules(num_dice=5, num_faces=6, max_category_fills=1, upper_bonus_reward=35, max_rerolls=2)

# Initialize the simulator
sim = Simulator(rules)
# Choose strategy
strategy = HumanLikeStrategy()
avg_score = sim.simulate_many(strategy, n=5000)
