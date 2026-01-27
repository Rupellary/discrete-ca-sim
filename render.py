# Code for rendering the simulation in the terminal
import numpy as np
from typing import Dict, Any


def display_grid_state(
    grid: np.array, 
    symbols: Dict[Any, str] = {1: 'X', 0: '_', 'sep': '|'}
) -> None:
    """
    Takes in a 2D numpy array and prints a text visual of the array.

    Parameters:
    ----------
    grid : np.array
        2D numpy array containing the grid state to be visualized
    symbols : dict
        Dictionary with the keys 0, 1, and 'sep' used to determine the characters used for the visual

    Returns:
    ----------
    None
    """

    # --- Printing grid "roof" ---
    # Compute line length to know how many characters to have in the first row
    line_length: int = len(grid[0]) * (len(symbols[0]) + len(symbols['sep'])) + len(symbols['sep'])
    # Concatenate underscores into "roof" of grid
    print(' _'*int(line_length/2))

    # --- Displaying Matrix ---
    # Loop through rows in the grid
    for row in grid:
        # Convert numbers into symbols from the symbols dict for displaying
        line: list[str] = [symbols[cell] for cell in row]
        # Concatenate cell symbols with separator
        line: str = symbols['sep'] + symbols['sep'].join(line) + symbols['sep']
        # Print row
        print(line)