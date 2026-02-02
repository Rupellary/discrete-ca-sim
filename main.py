# Code for CLI with app, parsing command and running sim and viz
import numpy as np
from render import display_grid_state
from sim import CellularAutomata

# Hypothetical grid state to be used for various test
test_state: np.array = np.array([
    [0, 0, 0, 0, 0, 1],
    [1, 1, 0, 0, 1, 0],
    [0, 0, 0, 0, 0, 0],
    [0, 0, 0, 1, 0, 0],
    [0, 0, 0, 1, 0, 0],
    [1, 1, 0, 0, 0, 0]
])
# Testing display function
display_grid_state(test_state)
ca = CellularAutomata(grid_state=test_state)
ca.step()
display_grid_state(ca.grid_state)