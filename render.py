from sim import CellularAutomaton

import numpy as np
from typing import Dict, Any
from numpy.typing import ArrayLike
from rich.live import Live
from rich.text import Text
import time


def _render_state(
    grid_state: ArrayLike,
    symbols: Dict[Any, str] = {1: "██", 0: "__", "sep": "|"}
) -> Text:
    """
    Turns numpy array into rich.text.Text object to be rendered during animation.
    Helper function for render_rollout().

    Parameters
    ----------
    grid_state : array-like
        Current state of CA grid stored as 1s and 0s in a 2D array.
    symbols : dict
        Dictionary for defining how the grid will be visualized.
        Required keys:
            1: How to represent living cells in text.
            0: How to represent dead cells in text.
            sep: Text element to put between cells.
    
    Returns
    ---------
    Text(state_string) : rich.text.Text
        Rich text object representing grid state for visualization.
    """

    # --- Input Error Handling ---
    # Checking grid_state is valid
    try:
        grid_state = np.asarray(grid_state)
    except (TypeError, ValueError) as e:
        raise TypeError("grid_state must be array-like.") from e
    if grid_state.ndim != 2:
        raise ValueError(f"grid_state must be 2 dimensional. Received shape {grid_state.shape}.")
    # Checking symbols dict is valid
    if not isinstance(symbols, dict):
        raise TypeError("symbols must be a dict.")
    required_keys = {1, 0, "sep"}
    missing_keys = required_keys - symbols.keys()
    if missing_keys:
        raise KeyError(f"symbols dict missing required keys: {missing_keys}")
    for key in required_keys:
        if not isinstance(symbols[key], str):
            raise TypeError(f"symbols[{key}] must be string. Was {type(symbols[key]).__name__}")
    if len(symbols[0]) != len(symbols[1]):
        raise ValueError("symbols[0] and symbols[1] must be of same length to keep grid size constant.")
    if len(symbols[0])==0 or len(symbols[1])==0:
        raise ValueError("symbols[0] and symbols[1] must have at least 1 character.")
    if symbols[0] == symbols[1]:
        raise ValueError("symbols[0] and symbols[1] cannot be the same.")

    # Alias symbols
    dead_str: str = symbols[0]
    sep: str = symbols["sep"]
    state_len: int = len(dead_str)
    sep_len: int = len(sep)
    cell_len: int = state_len + sep_len
    row_len: int = grid_state.shape[0]
    
    # Initialize string for containing text-based visualization of grid
    state_string: str = ""
    
    # --- Generating grid "roof" ---
    # Compute line length to know how many characters to have in the first row
    line_length: int = (row_len * cell_len) + sep_len
    # Concatenate underscores into "roof" of grid (" " between cells, "_" over them)
    grid_roof: str = (" " + "_"*state_len)*row_len
    # Add roof to state string
    state_string += grid_roof 

    # --- Displaying Matrix ---
    # Loop through rows in the grid
    for row in grid_state:
        # Add a line break to start next row
        state_string += "\n"
        # Convert numbers into symbols from the symbols dict for displaying
        line: list[str] = [symbols[cell] for cell in row]
        # Concatenate cell symbols with separator
        line: str = sep + sep.join(line) + sep
        # Add row to state string
        state_string += line
    
    # Add final line break to give visual a bit of space from the bottom of the terminal
    state_string += "\n"

    # Convert to rich.text.Text object and return
    return Text(state_string)


def render_rollout(
    ca: CellularAutomaton,
    steps: int,
    seconds_per_step: float = 0.6
) -> None:
    """
    Renders cellular automaton rollout in the terminal using rich library"s Live objects.
    
    Parameters
    ----------
    ca : CellularAutomaton
        Cellular automaton grid state and update rule.
    steps : int
        Number of steps to rollout the CA in the animation.
    seconds_per_step : float
        Number of seconds between steps of the rollout.
    """
    
    starting_state_render = _render_state(ca.grid_state)

    # --- Creating animation with rich.live.Live ---
    with Live(starting_state_render, screen=True) as live:
        for _ in range(steps):
            # Update grid state
            ca.step()
            # Update Live display with new state
            live.update(_render_state(ca.grid_state))
            # Wait to slow down animation
            time.sleep(seconds_per_step)