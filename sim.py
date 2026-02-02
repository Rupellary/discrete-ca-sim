# Code for running the simulation
import numpy as np

class CellularAutomata:
    """
    Cellular automata, including grid as an attribute and update rule as a method.
    Updates states based on the count of living neighbors.

    Attributes
    ----------
    grid_state : np.ndarray
        Current state of grid of cells, alive cells store 1s, dead cells store 0s.
    surive_set : set
        Set of neighbor counts that result in living cells remaining alive.
    birth_set : set
        Set of neighbor counts that result in dead cells transitioning to alive.    
    """

    def __init__(
        self,
        grid_state: np.ndarray,
        survive_set: set,
        birth_set: set,
    ):
    
        self.grid_state = grid_state
        self.survive_set = survive_set
        self.birth_set = birth_set

    def count_neighbors(self):
        neighbor_count_kernel: np.ndarray = np.array([
            [1, 1, 1],
            [1, 0, 1],
            [1, 1, 1]
        ])
        pass


    def update_rule(self):
        pass