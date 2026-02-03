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
    seconds_per_step : float
        Number of seconds between steps of the animation.

    Examples
    ----------
    $ python main.py -s 30 --rule S23B3 --start gliders -sps 0.5 
    """

    # --- Handling Rule String ---
    # Check that rule string is in valid format
    assert re.match(string=rule_string, pattern=r"^S\d+B\d+$"), """
        Not a valid rule string. 
        Must follow the pattern "S_B_" with underscores replaced with digits. 
        No other characters are allowed.
    """
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