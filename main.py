# Code for CLI with app, parsing command and running sim and viz
import numpy as np
from render import display_grid_state
from sim import CellularAutomata
import typer

# --------------------
# --- TESTING AREA ---
# --------------------

# # Hypothetical grid state to be used for various test
# test_state: np.array = np.array([
#     [0, 0, 0, 0, 0, 1],
#     [1, 1, 0, 0, 1, 0],
#     [0, 0, 0, 0, 0, 0],
#     [0, 0, 0, 1, 0, 0],
#     [0, 0, 0, 1, 0, 0],
#     [1, 1, 0, 0, 0, 0]
# ])
# # Testing display function
# display_grid_state(test_state)
# ca = CellularAutomata(grid_state=test_state)
# ca.step()
# display_grid_state(ca.grid_state)


# -----------
# --- CLI ---
# -----------

# [to team] working off of Typer Docs: https://typer.tiangolo.com/tutorial/arguments/optional/#an-alternative-cli-argument-declaration

app = typer.Typer()

@app.command()
def main(
    rule_string: str = typer.Option(
        help="""
            Update rule specified as sets of neighbor counts that result in surival (alive->alive) and those that result in birth (dead->alive)
            Written as S_B_. 
            Example: S23B3 
            The above is the rule for Conway's Game of Life. It means that living cells with 2 or 3 living neighbors stay alive and dead cells with 3 neighbors become alive.
        """)
):
    """
    Example Command: $ python main.py --rule-string S23B3
    """
    print(rule_string)

if __name__ == "__main__":
    app()