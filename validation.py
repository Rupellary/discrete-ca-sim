import re
import numpy as np

from starting_states import START_OPTIONS


# Specify valid options so that invalid alternatives can raise errors
VALID_START_OPTIONS: list[str] = list(START_OPTIONS.keys()) + ["randomize", "random_choice"]
MIN_SECONDS_PER_STEP: float = 0.01 # too low of values may stress the FPS and be impossible to see clearly regardless.

def validate_inputs(
    steps: int,
    rule_string: str,
    start_choice: str,
    update_rate: float,
    seed: int,
    seconds_per_step: float
) -> None:
    """
    Checks validity of user inputs, raising errors when invalid. 
    Parameters are the same supplied by the user in the CLI.
    """

    # Check that number of steps is non-negative integer
    if not isinstance(steps, int):
        raise TypeError("--steps must be an integer.")
    if steps < 0:
        raise ValueError("Cannot have negative steps of the simulation.")
    
    # Check that rule string is in valid format S<digits>B<digits>
    if not re.fullmatch(string=rule_string, pattern=r"S\d*B\d*"):
        raise ValueError("--rule-string must follow the pattern S<digits>B<digits>. No other characters are allowed.")
    # Check that rule is possible (a cell can have at maximum 8 living neighbors)
    if "9" in rule_string:
        raise Warning("--rule_string includes 9 but there cannot be more than 8 living neighbors")

    # Check that start state is valid option
    if start_choice not in VALID_START_OPTIONS:
        raise ValueError("--start must be one of the valid options. Use --help to see what options are allowed")

    # Check that update rate is a valid type and probability (0-1)
    if not isinstance(update_rate, (int, float)):
        raise TypeError("--update-rate must be a number.")
    if not (0 <= update_rate <= 1.0):
        raise ValueError("--update-rate must be between 0 and 1")
    
    # Check that seed is valid input for numpy.random.Generator
    try:
        np.random.default_rng(seed)
    except (TypeError, ValueError) as e:
        raise ValueError("--seed must be int int or None") from e
    
    # Check that seconds_per_step is a valid type and reasonable value
    if not isinstance(seconds_per_step, (int, float)):
        raise TypeError("--seconds-per-step must be a number.")
    if seconds_per_step <= MIN_SECONDS_PER_STEP:
        raise ValueError(f"--seconds-per-step must be greater than {MIN_SECONDS_PER_STEP}.")
