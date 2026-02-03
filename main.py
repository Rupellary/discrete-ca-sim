from sim import CellularAutomaton
from render import render_rollout
from starting_states import get_start, start_options_desc

import numpy as np
import typer
import re


# [to team] working off of Typer Docs: https://typer.tiangolo.com/tutorial/arguments/optional/#an-alternative-cli-argument-declaration
app = typer.Typer()

@app.command()
def main(
    steps: int = typer.Option(
        default=5,
        help="""
            Number of steps in the rollout.
        """
    ),
    rule_string: str = typer.Option(
        default="S23B3",
        help="""
            Update rule specified as sets of neighbor counts that result in surival (alive->alive) and those that result in birth (dead->alive)
            Written as S_B_. 
            Example: S23B3 
            The above is the rule for Conway's Game of Life. It means that living cells with 2 or 3 living neighbors stay alive and dead cells with 3 neighbors become alive.
        """
    ),
    start_choice: str = typer.Option(
        default="random_choice",
        help=start_options_desc
    ),
    seconds_per_step: float = typer.Option(
        default=0.6
    )
):
    """
    Example Command: $ python main.py --steps 10 --rule-string S23B3
    """

    # --- Input Error Handling ---
    # Check that number of steps is valid
    if not isinstance(steps, int):
        raise TypeError("--steps must be an integer.")
    if steps < 0:
        raise ValueError("Cannot have negative steps of the simulation.")
    # Check that rule string is in valid format
    if not re.fullmatch(string=rule_string, pattern=r"S\d+B\d+"):
        raise ValueError("--rule-string must follow the pattern S<digits>B<digits>. No other characters are allowed.")
    # [Start state error handling is incorporated into the logic in get_start()]
    # Check that seconds_per_step is a valid type and reasonable value
    if not isinstance(seconds_per_step, (int, float)):
        raise TypeError("--seconds-per-step must be a number.")
    if seconds_per_step <= 0.01:
        raise ValueError("--seconds-per-step must be greater than 0.01.")


    # --- Converting Rule String ---
    # Extract substrings for S and B
    survive_str, birth_str = re.findall(string=rule_string, pattern=r"^S(\d+)B(\d+)$")[0]
    # Convert to sets of integers
    survive_set = set(map(int, survive_str))
    birth_set = set(map(int, birth_str))

    # --- Retrieving Starting State ---
    # Use function and global dictionary from starting_states module
    start = get_start(start_choice)

    # --- Initializing CA ---
    ca = CellularAutomaton(
        grid_state=start,
        survive_set=survive_set,
        birth_set=birth_set
    )

    # --- Animating Rollout ---
    render_rollout(
        ca=ca, 
        steps=steps, 
        seconds_per_step=seconds_per_step
    )  


if __name__ == "__main__":
    app()