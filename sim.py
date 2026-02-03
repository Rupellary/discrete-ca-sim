import numpy as np
from np.typing import ArrayLike
from scipy.signal import convolve2d


def _normalize_grid_state(
    grid_state: ArrayLike
) -> np.ndarray:
    """
    Helper function for checking whether grid state is proper binary 2D array.
    Also converts array-like to np.ndarray.

    Parameters
    ----------
    grid_state : array-like
        Grid state array to test and potentially convert.

    Returns
    ----------
    grid_state : np.ndarray
        Grid state now as a numpy array.
    """

    try:
        grid_state: np.ndarray = np.asarray(grid_state)
    except (TypeError, ValueError) as e:
        raise TypeError("grid_state must be array-like.") from e
    if grid_state.ndim != 2:
        raise ValueError(f"grid_state must be 2 dimensional. Received shape {grid_state.shape}.")
    if not np.isin(grid_state, (0, 1)).all():
        raise ValueError("All cells in grid_state must be 0 or 1.")
    
    return grid_state


class CellularAutomaton:
    """
    Cellular automaton, including grid state as an attribute and update rule as a method.
    Updates states based on the count of living neighbors.

    Attributes
    ----------
    grid_state : array-like
        Current state of grid of cells, alive cells store 1s, dead cells store 0s.
    surive_set : set
        Set of neighbor counts that result in living cells remaining alive.
    birth_set : set
        Set of neighbor counts that result in dead cells transitioning to alive.    
    """

    def __init__(
        self,
        grid_state: ArrayLike,
        survive_set: set = {2, 3},
        birth_set: set = {3},
    ):
        # Checks grid is binary and converts to numpy array if not already
        grid_state: np.ndarray = _normalize_grid_state(grid_state)

        self.grid_state: np.ndarray = grid_state
        self.survive_set: set = survive_set
        self.birth_set: set = birth_set


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
        neighbor_counts: np.ndarray = self._count_neighbors()
        # Generate boolean masks for which cells are currently alive and which are currently dead
        currently_alive: np.ndarray = self.grid_state
        currently_dead: np.ndarray = 1 - self.grid_state
        # Check whether neighbor counts meet survival and birth conditions
        would_survive: np.ndarray = np.isin(neighbor_counts, self.survive_set)
        would_birth: np.ndarray = np.isin(neighbor_counts, self.birth_set)
        # Only apply survival to living cells, only apply birth to dead cells, recombine final states
        new_state: np.ndarray = (currently_alive * would_survive) + (currently_dead * would_birth)
        # Update grid state
        self.grid_state: np.ndarray = new_state