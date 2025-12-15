## Monti Carlo Simulation of Strategy Optimization in Yahtzee
IS597PR Fall2025 - Final Project

Team Members: Shu Chen, Sutthana Koo-Anupong

### Project Overview
In traditional Yahtzee, players roll up to five dice three times per round, choosing which dice to keep in pursuit of 
specific combinations before filling one of the 13 scoring categories. Because the game involves randomness 
and requires adaptive decision-making, this project uses Monte Carlo simulation to analyze and optimize different 
strategies for playing Yahtzee.

### Objectives
1. Evaluate the performance of different strategies in a large number of repeated games under standard rules.
2. After modifying the game rules, to study how different rules affect the optimal strategies and average scores.
3. The program is designed to allow users to flexibly adjust the game rules as desired.

### Game Simulation Framework
The program follows standard Yahtzee rules while allowing users to flexibly modify key game parameters including
- Number of dice (standard: 5)
- Number of faces per die (standard: 6)
- Number of rerolls allowed per turn (standard: 2)
- Number of times each scoring category can be filled (standard: 1)

In addition to modifying game rules, users may implement and test custom strategies under any rule configuration. 
To demonstrate the framework, we implemented and evaluated five strategies including
- RandomStrategy: Randomly selects dice to keep and assigns scores to random available categories
- GreedyStrategy: Retains the most frequent dice value and assigns the roll to the category with the highest immediate score
- SimpleRuleStrategy: follow simple pre-set rules to choose dice to keep and put score in category
- HumanLike Strategy: Mimics common human decision-making patterns, balancing risk and reward
- AdvancedHumanLikeStrategy: Extends the HumanLike approach by placing greater emphasis on long-term planning, particularly upper-section bonus feasibility

### Hypothesis
H1: Under the standard Yahtzee rules, strategy complexity will be positively correlated with average score. 
As strategies incorporate more forward-looking or probabilistic decision-making logic, their average final scores will increase
![alt text](https://github.com/ShuChen3/2025Fall_projects_SS/blob/main/H1_result.png)

Result H1: The results support H1. Among the five strategies tested, AdvancedHumanLikeStrategy achieved the highest average score, followed closely by HumanLikeStrategy. Simpler strategies such as Random and Greedy—performed substantially worse.


H2: When the number of faces on the dices increase, achieving the upper-section bonus becomes less feasible. 
Under these conditions, strategies that rely on dynamically assessing bonus feasibility are expected to perform worse
![alt text](https://github.com/ShuChen3/2025Fall_projects_SS/blob/main/H2_result.png)

Result H2: Under increased die-face conditions, AdvancedHumanLikeStrategy no longer clearly outperformed the other non-random strategies. Instead, SimpleRuleStrategy, GreedyStrategy, and HumanLikeStrategy achieved similar average scores, while RandomStrategy remained significantly worse.

H3: When the game allows more scoring opportunities per category by increasing from one fill-in to three, 
the strategic advantages of strategies designed for scarce or restrictive rule settings are expected to diminish.
![alt text](https://github.com/ShuChen3/2025Fall_projects_SS/blob/main/H3_result.png)

Result H3: Under expanded fill-in rules, HumanLikeStrategy and AdvancedHumanLikeStrategy continued to outperform the other strategies, with AdvancedHumanLikeStrategy achieving a slightly higher average score, although the performance gap between strategies was narrower than under standard rules.

## References/Note 
In this project, we utilized AI tools to help organize the overall design logic and assist with the implementation of certain functions,
All final design decisions, code integration, simulation execution, and result validation were completed by the project team members.