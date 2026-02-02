import numpy as np
from scipy.signal import convolve2d

class CellularAutomaton:
    """
    Cellular automaton, including grid state as an attribute and update rule as a method.
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
        survive_set: set = {2, 3},
        birth_set: set = {3},
    ):
        self.grid_state = grid_state
        self.survive_set = survive_set
        self.birth_set = birth_set


    def _count_neighbors(self):
        """
        Counts number of active neighbors in the 3x3 neighborhood around each cell.
        Returns a grid of the same size with each cells' count of active neighbors. 
        Helper function for step() method.
        """

        neighbor_count_kernel: np.ndarray = np.array([
            [1, 1, 1],
            [1, 0, 1],
            [1, 1, 1]
        ])
        # Convolve to count number of active neighbors around each cell
        neighbor_counts: np.ndarray = convolve2d(
            self.grid_state, 
            neighbor_count_kernel, 
            mode='same', #removes the extra rows and columns that would result from a proper convolution
            boundary='wrap'
        )
        return neighbor_counts


    def step(self):
        """
        Update grid state using survival and birth sets for transition dynamics.
        """

        # Count neighbors to compare with survival and birth conditions
        neighbor_counts = self._count_neighbors()
        # Generate boolean masks for which cells are currently alive and which are currently dead
        currently_alive = self.grid_state
        currently_dead = 1 - self.grid_state
        # Check whether neighbor counts meet survival and birth conditions
        would_survive = np.isin(neighbor_counts, list(self.survive_set))
        would_birth = np.isin(neighbor_counts, list(self.birth_set))
        # Only apply survival to living cells, only apply birth to dead cells, recombine final states
        new_state = (currently_alive * would_survive) + (currently_dead * would_birth)
        # Update grid state
        self.grid_state = new_state