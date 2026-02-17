import numpy as np
from numpy.typing import ArrayLike
from numpy.random import Generator
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
        Grid state now as an integer numpy array.
    """

    # Convert to integer numpy array if not already. Raise error if not possible.
    try:
        grid_state: np.ndarray = np.asarray(grid_state).astype(int)
    except (TypeError, ValueError) as e:
        raise TypeError("grid_state must be array-like.") from e
    
    # Enforce a 2D discrete grid space
    # Ensure that matrix is rank 2
    if grid_state.ndim != 2:
        raise ValueError(f"grid_state must be 2 dimensional. Received shape {grid_state.shape}.")
    # Ensure that grid is binary
    if not np.isin(grid_state, (0, 1)).all():
        raise ValueError("All cells in grid_state must be 0 or 1.")
    
    return grid_state


class CellularAutomaton:
    """
    Cellular automaton, including grid state as an attribute and update rule as a method.
    Updates states based on the count of "living" neighbors.

    Attributes
    ----------
    grid_state : array-like
        Current state of grid of cells, alive cells store 1s, dead cells store 0s.
    surive_set : set
        Set of neighbor counts that result in living cells remaining alive.
    birth_set : set
        Set of neighbor counts that result in dead cells transitioning to alive. 
    update_rate : float
        For asynchronous updating. Percentage chance of updating each step.
    seed : np.random.Generator
    """

    def __init__(
        self,
        grid_state: ArrayLike,
        survive_set: set = {2, 3},
        birth_set: set = {3},
        update_rate: float = 1.0,
        rng: Generator = None
    ):
        # Checks grid is binary and converts to numpy array if not already
        grid_state: np.ndarray = _normalize_grid_state(grid_state)

        self.grid_state: np.ndarray = grid_state
        self.survive_set: set = survive_set
        self.birth_set: set = birth_set
        self.update_rate: float = update_rate
        self.rng: Generator = rng


    def _count_neighbors(self):
        """
        Counts number of active neighbors in the 3x3 neighborhood around each cell.
        Returns a grid of the same size with each cells" count of active neighbors. 
        Helper function for step() method.
        """

        # Define kernel for counting neighbors in 3x3 (does not count self)
        neighbor_count_kernel: np.ndarray = np.array([
            [1, 1, 1],
            [1, 0, 1],
            [1, 1, 1]
        ])
        # Convolve to count number of active neighbors around each cell
        neighbor_counts: np.ndarray = convolve2d(
            self.grid_state, 
            neighbor_count_kernel, 
            mode="same",
            boundary="wrap"  # results in toroidal topology
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
        would_survive: np.ndarray = np.isin(neighbor_counts, list(self.survive_set)).astype(int)
        would_birth: np.ndarray = np.isin(neighbor_counts, list(self.birth_set)).astype(int)
        # Only apply survival to living cells, only apply birth to dead cells, recombine final states
        new_state: np.ndarray = (currently_alive * would_survive) + (currently_dead * would_birth)

        # --- Asynchronous Updating ---
        # Using is close to avoid any float rounding problems when synchrony is desired
        if not np.isclose(self.update_rate, 1.0):
            # Generate random mask with 1s for cells that will update and 0s for the rest
            update_mask: np.ndarray = self.rng.random(self.grid_state.shape) <= self.update_rate
            # Use new state where mask==1 and previous state where mask==0
            new_state: np.ndarray = (new_state * update_mask) + (self.grid_state * (1-update_mask))

        # Update grid_state
        self.grid_state: np.ndarray = new_state