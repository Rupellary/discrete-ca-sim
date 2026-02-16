# discrete-ca-sim
Python app for visualizing a parameterized version of [Conway's Game of Life](https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life). Written for the CAS502: Computation course at ASU.

## Project Description
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


# User Guide

## Installation
Follow these steps to set the app up on your local machine:

### 1. Clone the repository
Open your terminal and navigate to the directory where you want to install the app. Then run the following to download it:

```
git clone https://github.com/Rupellary/discrete-ca-sim.git
cd discrete-ca-sim
```

### 2. Create virtual environment
[Conda](https://www.anaconda.com/docs/getting-started/miniconda/install) is recommended for the environment. venv most likely works as well but it has not been tested. Importantly, the program was written in python 3.13, other versions of python have not been tested. To create and activate the environmnet with conda run the following:

```
conda create -n discrete-ca-sim python=3.13
conda activate discrete-ca-sim
```

### 3. Install dependencies
Use the requirements file to install all the dependencies for the project by running the following:
```
pip install -r requirements.txt
```
Now you should be set up to start running the application.

## Usage
From the root directory you can run the app from the command line with the following:
```
python main.py
```
This will run it with the default parameter settings which uses the Game of Life's update rule and randomly selects one of the starting states. However, providing additional arguments in the command allows for much more user control.

### CLI Options

| Argument                 | Type  | Default         | Description |
|--------------------------|-------|-----------------|-------------|
| `-s`, `--steps`          | int   | 30              | Number of steps to rollout for the animation. |
| `-r`, `--rule`           | str   | "S23B3"         | CA update rule. [See below](#### Rule Specification Syntax) for more details on the notation. |
| `--start`                | str   | "random_choice" | Choice of starting state for the simulation. [See below](#### Starting State Options) for more details on the options. |
| `-ur`, `--update_rate`   | float | 1.0             | For asynchronous CA. Values less than 1 result in stochastic updating where cells have this probability of updating at each step. |
| `-sd`, `--seed`          | int   | `None`          | Random seed for determinsitic randomization. Affects randomly generated starting states and asynchronous updating but not start="random_choice" as this can can already be fixed with manual selection. |
| `-sps`, `--sec-per-step` | float | 0.3             | Seconds between steps while animating. Smaller values speed up the animation. |


#### Rule Specification Syntax

As mentioned in the project description, this application keeps the core logic of Conway's Game of Life, namely that cells can either be on or off, "alive" or "dead", and at each step they change their state based solely on:

1. The count of "alive" cells out of the 8 in their 3x3 neighborhood.
2. Their own current state as "alive" or "dead."

But the application generalizes the specific state transition conditions. These transitions can be summarized with 2 sets:

1. The set of alive-neighbor counts that transition "alive" cells to the "alive" state. This is referred to as the "survive set."
2. The set of alive-neighbor counts that transition "dead" cells to the "alive" state. This is referred to as the "birth set."

With these two sets specified, all possible state transitions can be infered.

To set an update rule for the cellular automaton, you can pass in a string that specifies these two sets following the pattern "S<survive-set-digits>B<birth-set-digits>". For example, Conway's Game of Life follows the rule that living cells only survive when they have exactly 2 or 3 living neighbors and dead cells only become alive if they have exactly 2 living neighbors. This can be expressed with this pattern as "S23B3". 

##### Input Validation
* No other characters are allowed, the string must match the regex pattern `"^S\d*B\d*$"`
* Cells only have 8 neighbors so including 9 in your list of digits will raise a warning.
* Double-digit numbers are interpreted as two individual digits. A cell cannot have > 8 neighbors so there is no sense to double-digit numbers anyways.
* Any redundant digits are silently ignored; e.g. "S233B33" == "S23B3"
* Empty sets are allowed; e.g. "SB04"

#### Starting State Options
There are a variety of options that can be selected for the starting state of the CA rollout, each of which provide a different window into the rule's dynamics. 

##### `--start random_choice`
This is the default option, it randomly selects from the other options. 

##### `--start randomize`
Randomly generates the starting state. In the current version, all cells have an equal probability of being on or off. In future versions this probability may be under user control.

![randomize](docs/assets/randomize.svg)

##### `--start block`

![block](docs/assets/block.svg)

##### `--start diamond`

![diamond](docs/assets/diamond.svg)

##### `--start seed`

![seed](docs/assets/seed.svg)

##### `--start nothing`
This will only result in behavior if the birth set includes 0.

![nothing](docs/assets/nothing.svg)

##### `--start classic_shapes`
These shapes have [interesting behavior](https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life#:~:text=edit%20source%5D-,Pattern%20taxonomy,-%5Bedit%20source) under the original Game of Life rule
![classic_shapes](docs/assets/classic_shapes.svg)

##### `--start oscillator`

![oscillator](docs/assets/oscillator.svg)

##### `--start gliders`
The ["Glider"](https://en.wikipedia.org/wiki/Glider_(Conway%27s_Game_of_Life)) is a well-known shape in the Game of Life. It is the simplest pattern that repeats itself translated as though moving through the space.
![gliders](docs/assets/gliders.svg)

##### `--start checkered`

![checkered](docs/assets/checkered.svg)

