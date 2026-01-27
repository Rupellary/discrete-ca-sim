# discrete-ca-sim
Python app for visualizing a parameterized version of Conway's Game of Life. Written for the CAS502: Computation course at ASU.

## Project Description:
This project aims to create a small app for exploring discrete cellular automata dynamics through visualization of a user-controlled update rule. The app will be designed to mimic Conway’s Game of Life while parameterizing aspects of the update rule to allow for exploration of their impacts on the dynamics. 
Cellular Automata are a computational phenomenon used to study a variety of concepts in Complex Adaptive Systems Science including emergence, decentralized coordination, and computation. The most famous Cellular Automata, which this app will be based on, is Conway’s Game of Life. It works by first instantiating a grid of binary values, 1s corresponding conceptually with “living cells” and 0s corresponding with “dead cells.” A rule is defined for how cells update their state over time based solely on their current state and the state of their immediate neighbors (the eight neighbors in their 3x3 neighborhood). The rule is then applied iteratively to the grid of values, sometimes resulting in interesting patterns and emergent capabilities as cells interact with their neighbors and turn on and off. 
The update rule for Conway’s Game of Life can be decomposed into four thresholds; two for determining how “living” cells update and two for determining how “dead” cells update:
1.	If a living cell has less than 2 living neighbors it dies
2.	If a living cell has more than 3 living neighbors it dies
3.	If a dead cell has less than 3 living neighbors it stays dead
4.	If a dead cell has more than 3 living neighbors it stays dead
These four thresholds will be alterable by the user, allowing them to probe the system to try to get a sense of the influence each threshold has over the dynamics of the system. 
As the starting state also has a profound effect on the ensuing behavior, the user will also have a series of starting states to choose from when running the simulation.
As the CA rolls out over several steps, the state of the grid after each update step will be displayed in the terminal for the user to give a window into the system’s dynamics.

## Team Memebers
Rockwell Gulassa

## Anticipated Challenges:
### Technical Challenges: 
I have very little experience with creating apps that can take arguments in the shell which may turn out to be more complicated and/or time-consuming than expected, especially without AI assistance. 
I have no experience creating dynamic visualizations in the terminal. It is possible I will have to pivot to alternatives like generating gif files for instance. 
While the matrix multiplications are straightforward operations, it is easy to get tangled up in the various Boolean masks and update rules all being performed with similar mathematical operations.
### Process Challenges:
(While I will not be working in a team, I can answer as though I were in order to engage with the concept)
Many of the features rely on certain core functionality to be working (update rule and visualization). Should issues arise in developing that functionality, the other team members may be stuck waiting before their code can be properly tested. It will be important to compartmentalize the code in such a way that functionality has some means of being tested even without being “plugged in” to the full application, and to prioritize features not only based on their importance to the project but also their flexibility to the production timelines of others (e.g. having a team member start with the terminal input interface (argparse/typing) - even though shell-level parameterization is not technically required functionality - because it is not dependent on the update rule or visualization code to be already working.)
Time zone and work-schedule differences make rapid communication and collective problem-solving more challenging. It will be important to plan and delegate in a way that does not require synchronous work. It will also be important to make excessive use of comments and docstrings, perhaps beyond what will be included in the final draft, to avoid any challenges interpreting each other’s code while we are unable to ask questions. 
### Teamwork Challenges: 
(While I will not be working in a team, I can answer as though I were in order to engage with the concept)
As a data science teacher, I’ve come to feel most comfortable working in a jupyter notebook where rapid iteration feels easiest, but notebooks don’t mesh well with Git. I will need to adapt and get more comfortable iterating with terminal outputs to make collaboration with Git cleaner.
I also have less experience with object-oriented programming and the shell, but as it makes sense to approach it this way I will have to get more comfortable with this setup. 
In order to effectively collaborate we will both have to step out of our comfort zones to meet each other somewhere where we can both work effectively.
