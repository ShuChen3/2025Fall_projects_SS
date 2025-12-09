## Monti Carlo Simulation of Strategy Optimization in Yahtzee
IS597PR Fall2025 - Final Project

Team Members: Shu Chen, Sutthana Koo-Anupong

### Project Overview
In traditional Yahtzee, players roll up to five dice three times per round, choosing which dice to keep in pursuit of specific combinations before filling one of the 13 scoring categories. Because the game involves randomness and requires adaptive decision-making, this project uses Monte Carlo simulation to analyze and optimize different strategies for playing Yahtzee.

### Objectives
1. Evaluate the performance of different strategies in a large number of repeated games under standard rules.
2. After modifying the game rules, to study how different rules affect the optimal strategies and average scores.
3. The program can be able to allow users to flexibly change rule of the games freely

### Hypothesis
H1: Under the standard Yahtzee rules, strategy complexity will be positively correlated with average score. 
As strategies incorporate more forward-looking or probabilistic decision-making logic, their average final scores will increase

H2: When the number of faces on the dices increase, achieving the upper-section bonus becomes less feasible. 
Under these conditions, strategies that rely on dynamically assessing bonus feasibility are expected to perform worse

H3: Altering the scoring card in such as removing the “Full House” category or 
doubling the score of “Four of \\a Kind” will change which strategy yields the highest average score 

