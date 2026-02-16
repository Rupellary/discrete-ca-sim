import numpy as np
from typing import Dict
from numpy.typing import ArrayLike
from rich.live import Live
from rich.text import Text
import time

from sim import CellularAutomaton, _normalize_grid_state


# Numpy arrays will be converted to rich.text.Text objects for display in the terminal
# These are the symbol choices used for representing the grid state with text.
_CELL_WIDTH: int = 2 # how many times the character is repeated. 2 results in roughly square cells.
_STATE_TO_TEXT: Dict[int, str] = {
    0: "_" * _CELL_WIDTH, # how dead cells will be displayed
    1: "█" * _CELL_WIDTH # how living cells will be displayed
}
_SEP: str = "|" # separator between cells. "|" results in a nice grid look.


def _render_state(
    grid_state: ArrayLike
) -> Text:
    """
    Helper function for render_rollout().
    Turns numpy array into rich.text.Text object to be rendered during animation.

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
    # Checking grid_state is valid and ensuring/converting to numpy array
    grid_state: np.ndarray = _normalize_grid_state(grid_state)
    
    # Initialize list for containing lines of text for state visualization
    lines: list[str] = []
    
    # --- Generating grid "roof" ---
    # Concatenate underscores into "roof" of grid (" "s between cells and "_"s over them)
    num_cols: int = grid_state.shape[1]
    grid_roof: str = ((" " * len(_SEP)) + ("_" * _CELL_WIDTH)) * num_cols
    lines.append(grid_roof)

    # --- Displaying Matrix ---
    # Loop through rows in the grid to convert them each to lines of text
    for row in grid_state:
        # Use dictionary to translate numbers into text for display
        line: list[str] = [_STATE_TO_TEXT[cell] for cell in row]
        # Concatenate cell symbols with separator
        line: str = _SEP + _SEP.join(line) + _SEP
        # Add row to list of lines
        lines.append(line)
    
    # Combine lines together with line breaks between
    state_string: str = "\n".join(lines)

    # Convert to rich.text.Text object before returning
    return Text(state_string)


def render_rollout(
    ca: CellularAutomaton,
    steps: int,
    seconds_per_step: float = 0.6
) -> None:
    """
    Renders cellular automaton rollout in the terminal using rich library's rich.live.Live objects.
    
    Parameters
    ----------
    ca : CellularAutomaton
        Cellular automaton with grid state and update rule.
    steps : int
        Number of steps to rollout the CA in the animation.
    seconds_per_step : float
        Number of seconds to wait between steps of the animation.
    """
    
    # Convert starting CA grid state to rich.text.Text object to display in terminal
    starting_state_render: Text = _render_state(ca.grid_state)

    # --- Creating animation with rich.live.Live ---
    with Live(starting_state_render, refresh_per_second=60, screen=True) as live:
        for _ in range(steps):
            # Update grid state by applying CA update rule
            ca.step()
            # Convert CA grid state to Text object and update Live display with new state
            live.update(_render_state(ca.grid_state))
            # Wait to slow down animation
            time.sleep(seconds_per_step)