# discrete-ca-sim
Python app for visualizing a parameterized version of Conway's Game of Life. Written for the CAS502: Computation course at ASU.

## Project Description:
This project aims to create a small app for exploring discrete cellular automata dynamics through visualization of a user-controlled update rule. The app will be designed to mimic Conway’s Game of Life while parameterizing aspects of the update rule to allow for exploration of their impacts on the dynamics. 

Cellular Automata are a computational phenomenon used to study a variety of concepts in Complex Adaptive Systems Science including emergence, decentralized coordination, and computation. The most famous Cellular Automata, which this app is based on, is Conway’s Game of Life. It works by first instantiating a grid of binary values, 1s corresponding conceptually with “living cells” and 0s corresponding with “dead cells.” A rule is defined for how cells update their state over time based solely on their current state and the count of living neighbors (the eight neighbors in their 3x3 neighborhood). The rule is then applied iteratively to the grid of values, sometimes resulting in interesting patterns and emergent capabilities as cells interact with their neighbors and turn on and off. 

The update rule for Conway’s Game of Life can be decomposed into two sets:
1. For living cells: which counts (0-8) of living neighbors result in the cell staying alive. This is referred to in the code as the survival_set.
2. For dead cells: which counts (0-8) of living neighbors result in the cell becoming alive. This is referred to in the code as the birth_set.

For Conway's Game of Life the rule is: survival_set={2, 3}, birth_set={3}.
These sets are denoted with the convention S<digits>B<digits>. For example "S23B3".

These two sets are alterable by the user in the CLI, allowing them to probe the system to try to get a sense of the influence these parameters have over the dynamics of the system. 
As the starting state also has a profound effect on the ensuing behavior, the user also has a series of starting states to choose from when running the simulation.
As the CA rolls out over several steps, the state of the grid after each update step is displayed in the terminal to give a window into the system’s dynamics.

## Author
Rockwell Gulassa
