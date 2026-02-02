# Code for CLI with app, parsing command and running sim and viz
import numpy as np
from render import display_grid_state
from sim import CellularAutomata
import typer
import re

# Hypothetical grid state to be used for various test
test_state: np.array = np.array([
    [0, 0, 0, 0, 0, 1],
    [1, 1, 0, 0, 1, 0],
    [0, 0, 0, 0, 0, 0],
    [0, 0, 0, 1, 0, 0],
    [0, 0, 0, 1, 0, 0],
    [1, 1, 0, 0, 0, 0]
])


# [to team] working off of Typer Docs: https://typer.tiangolo.com/tutorial/arguments/optional/#an-alternative-cli-argument-declaration
app = typer.Typer()

@app.command()
def main(
    steps: int = typer.Option(
        default=3,
        help="""
            Number of steps in the rollout
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
    )
):
    """
    Example Command: $ python main.py --rule-string S23B3
    """

    # Checking that rule string is in valid format
    assert re.match(string=rule_string, pattern=r"^S\d+B\d+$"), """
        Not a valid rule string. 
        Must follow the pattern 'S_B_' with underscores replaced with digits. 
        No other characters are allowed.
    """
    
    # Extract substrings for S and B
    survive_str, birth_str = re.findall(string = rule_string, pattern=r"^S(\d+)B(\d+)$")[0]
    # Convert to sets of integers
    survive_set = set(map(int, survive_str))
    birth_set = set(map(int, birth_str))

    # Initialize CA
    ca = CellularAutomata(
        grid_state=test_state,
        survive_set=survive_set,
        birth_set=birth_set
    )
    print(ca.survive_set)
    print(ca.birth_set)

    # Rollout and display CA
    display_grid_state(ca.grid_state)
    for _ in range(steps):
        ca.step()
        display_grid_state(ca.grid_state)      

if __name__ == "__main__":
    app()