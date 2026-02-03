from sim import CellularAutomaton
from render import render_rollout
from starting_states import get_start, start_options_desc

from typing import Annotated
import numpy as np
import typer
import re


# [to team] working off of Typer Docs: https://typer.tiangolo.com/tutorial/arguments/optional/#an-alternative-cli-argument-declaration
app = typer.Typer()

@app.command()
def main(
    steps: Annotated[
        int, 
        typer.Option(
            "--steps", "-s",
            help="Number of steps in the rollout."
        )
    ] = 5,
    rule_string: Annotated[
        str,
        typer.Option(
            "--rule", "-r",
            help="""
            Update rule specified as sets of neighbor counts that result in surival (alive->alive) and those that result in birth (dead->alive). \n
            Written as S<digits>B<digits>. E.g. S23B3 \n
            The above is the rule for Conway's Game of Life. It means that living cells with 2 or 3 living neighbors stay alive and dead cells with 3 neighbors become alive.
            """
        )
    ] = "S23B3",
    start_choice: Annotated[
        str,
        typer.Option(
            "--start",
            help=start_options_desc
        )
    ] = "random_choice",
    update_rate: Annotated[
        float,
        typer.Option(
            "--update-rate", "-ur",
            help="For asychronous CA. Probability that a cell will be updated during a step. Values below 1.0 result in stochastic updating."
        )
    ] = 1.0,
    seconds_per_step: Annotated[
        float,
        typer.Option(
            "--sec-per-step", "-sps",
            help="Number of seconds between steps of animation. Smaller values speed up the simulation."
        )
    ] = 0.6
):
    """
    Runs discrete cellular automaton simulation in terminal.

    Parameters
    ----------
    steps : str
        Number of steps of CA rollout to animate.
    rule_string : str
        Update rule specified as sets of neighbor counts with live->live transition (survive) and sets with dead->live transition (birth).
        Expressed as a string following the pattern S<digits>B<digits>. E.g. S23B3.
    start_choice : str
        Choice of starting state. Valid options displayed with --help.
    update_rate : float
        Probability that a cell will update at each step. Values less than 1 result in asynchronous CA.
    seconds_per_step : float
        Number of seconds between steps of the animation.

    Examples
    ----------
    $ python main.py -s 30 --rule S23B3 --start gliders -sps 0.5 
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
    # Check that update rate is a valid type and probability
    if not isinstance(update_rate, (int, float)):
        raise TypeError("--update-rate must be a number.")
    if not (0 <= update_rate <= 1.0):
        raise ValueError("--update-rate must be between 0 and 1")
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
        birth_set=birth_set,
        update_rate=update_rate
    )

    # --- Animating Rollout ---
    render_rollout(
        ca=ca, 
        steps=steps, 
        seconds_per_step=seconds_per_step
    )  


if __name__ == "__main__":
    app()