# Code for rendering the simulation in the terminal
import numpy as np
from typing import Dict, Any
from rich.live import Live
from rich.text import Text
from sim import CellularAutomata
import time


def _render_state(
    grid_state: np.ndarray,
    symbols: Dict[Any, str] = {1: "██", 0: "__", "sep": "|"}
) -> Text:
    """
    Turns numpy array into rich.text.Text object to be rendered during animation.
    Helper function for render_rollout().

    Parameters
    ----------
    grid_state : np.ndarray
        Current state of CA grid stored and 1s and 0s in a numpy array.
    symbols : dict
        Dictionary for defining how the grid will be visualized.
        1: How to represent living cells in text.
        0: How to represent dead cells in text.
        sep: Text element to put between cells.
    """    
    
    # Initialize string for containing text-based visualization of grid
    state_string: str = ""
    
    # --- Generating grid "roof" ---
    # Compute line length to know how many characters to have in the first row
    line_length: int = len(grid_state[0]) * (len(symbols[0]) + len(symbols["sep"])) + len(symbols["sep"])
    # Concatenate underscores into "roof" of grid (" " between cells, "_" over them)
    grid_roof: str = (" " + "_"*len(symbols[0]))*int(line_length/3)
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
        line: str = symbols["sep"] + symbols["sep"].join(line) + symbols["sep"]
        # Add row to state string
        state_string += line
    
    # Add final line break to give visual a bit of space from the bottom of the terminal
    state_string += "\n"

    # Convert to rich.text.Text object and return
    return Text(state_string)


def render_rollout(
    ca: CellularAutomata,
    steps: int,
    seconds_per_step: float = 0.6
) -> None:
    """
    Renders cellular automaton rollout in the terminal using rich library's Live objects.
    
    Parameters
    ----------
    ca : CellularAutomata
        Cellular automaton with grid state and update rule.
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