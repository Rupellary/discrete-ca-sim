from sim import CellularAutomaton
from render import render_rollout
from starting_states import get_start, start_options_desc
from validation import validate_inputs

import numpy as np
import typer
import re
from typing import Annotated
from numpy.random import Generator



app = typer.Typer()

@app.command()
def main(
    steps: Annotated[
        int, 
        typer.Option(
            "--steps", "-s",
            help="Number of steps in the rollout."
        )
    ] = 30,
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
    seed: Annotated[
        int | None,
        typer.Option(
            "--seed", "-sd",
            help="For asychronous CA. Random seed to fix randomization for reproducibility. Pass None for nondeterminstic results."
        )
    ] = None,
    seconds_per_step: Annotated[
        float,
        typer.Option(
            "--sec-per-step", "-sps",
            help="Number of seconds between steps of animation. Smaller values speed up the simulation."
        )
    ] = 0.3
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
    seed : int or None
        For asychronous CA. Random seed to fix randomization for reproducibility. If None rng will not be fixed.
    seconds_per_step : float
        Number of seconds between steps of the animation.

    Examples
    ----------
    $ python main.py -s 100 --rule S23B3 --start gliders -sps 0.1
    $ python main.py -s 100 -r S23B3 --start block -ur 0.6 -sd 42 -sps 0.05
    $ python main.py -s 100 -r S23B3 --start oscillator -ur 1.0 -sps 0.1
    """

    # --- Input Error Handling ---
    validate_inputs(
        steps,
        rule_string,
        start_choice,
        update_rate,
        seed,
        seconds_per_step  
    )

    # --- Converting Rule String ---
    # Extract substrings for S and B
    survive_str, birth_str = re.findall(string=rule_string, pattern=r"^S(\d*)B(\d*)$")[0]
    # Convert to sets of integers
    survive_set: set = set(map(int, survive_str))
    birth_set: set = set(map(int, birth_str))

    # --- Retrieving Starting State ---
    # Initialize RNG
    rng: Generator = np.random.default_rng(seed)
    # Retrieve or generate starting state
    start: np.ndarray = get_start(start_choice, rng)

    # --- Initializing CA ---
    ca: CellularAutomaton = CellularAutomaton(
        grid_state=start,
        survive_set=survive_set,
        birth_set=birth_set,
        update_rate=update_rate,
        rng=rng
    )

    # --- Animating Rollout ---
    render_rollout(
        ca=ca, 
        steps=steps, 
        seconds_per_step=seconds_per_step
    )


if __name__ == "__main__":
    app()