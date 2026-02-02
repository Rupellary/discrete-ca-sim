# Code for running the simulation
import numpy as np
from scipy import convolve2d

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

    def _count_neighbors(self):
        """
        Counts number of active neighbors in the 3x3 neighborhood around each cell.
        Returns a grid of the same size with each cells' count of active neighbors. 
        """
        neighbor_count_kernel: np.ndarray = np.array([
            [1, 1, 1],
            [1, 0, 1],
            [1, 1, 1]
        ])
        neighbor_counts: np.ndarray = convolve2d(self.grid_state, neighbor_count_kernel, mode='same')
        return neighbor_counts


    def update_rule(self):
        neighbor_counts = self._count_neighbors()
        