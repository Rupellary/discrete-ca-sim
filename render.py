from sim import CellularAutomaton

import numpy as np
from typing import Dict, Any
from numpy.typing import ArrayLike
from rich.live import Live
from rich.text import Text
import time


# Text symbols for visualization
_CELL_WIDTH = 2
_STATE_TO_TEXT: Dict[int, str] = {
    0: "_"*_CELL_WIDTH,
    1: "█"*_CELL_WIDTH
}
_SEP: str = "|"


def _render_state(
    grid_state: ArrayLike
) -> Text:
    """
    Turns numpy array into rich.text.Text object to be rendered during animation.
    Helper function for render_rollout().

    Parameters
    ----------
    grid_state : array-like
        Current state of CA grid stored as 1s and 0s in a 2D array.
    
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
    if not np.isin(grid_state, (0, 1)).all():
        raise ValueError("All cells in grid_state must be 0 or 1.")
    
    # Initialize list for containing lines of text-based visualization of grid
    lines: list[str] = []
    
    # --- Generating grid "roof" ---
    # Concatenate underscores into "roof" of grid (" "s between cells and "_"s over them)
    grid_roof: str = ((" " * len(_SEP)) + ("_" * _CELL_WIDTH)) * grid_state.shape[1]
    # Add roof to state string
    lines.append(grid_roof)

    # --- Displaying Matrix ---
    # Loop through rows in the grid
    for row in grid_state:
        # Convert numbers into text for displaying
        line: list[str] = [_STATE_TO_TEXT[cell] for cell in row]
        # Concatenate cell symbols with separator
        line: str = _SEP + _SEP.join(line) + _SEP
        # Add row to list of lines
        lines.append(line)
    
    # Combine lines together with line breaks between
    state_string = "\n".join(lines)

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