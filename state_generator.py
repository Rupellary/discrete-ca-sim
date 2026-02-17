import numpy as np
from numpy.random import Generator


def _reask_dim_size_until_valid(input_prompt: str) -> int:
    """
    Helper function for generate_random_state.
    Asks for user input for height or width. 
    If the input is invalid, notifies user instead of crashing and asks for a new input.

    Parameters
    ----------
    input_prompt : str
        String to prompt user for the information. E.g. "Width: "
    
    Returns
    ----------
    dim_size : int
        The integer form of the final valid input dimension size.
    """
    
    while True:
        # With each repeat of the loop, reask for the user input
        in_dim_size: str = input(input_prompt)

        # Check if input can be interpreted as an integer (dimension sizes must be integers)
        try:
            dim_size: int = int(in_dim_size)
        except ValueError:
            print("I'm sorry, that could not be interpreted as a valid size. Please input an integer.")
            continue

        # Check if input is larger than 0 (dimension sizes cannot be less than 1)
        if dim_size <= 0:
            print("I'm sorry, that could not be interpreted as a valid size. Please input a value above 0.")
            continue
        else:
            return dim_size


def _reask_prob_until_valid() -> float:
    """
    Helper function for generate_random_state.
    Asks for user input for probability of cell being alive. 
    If the input is invalid, notifies user instead of crashing and asks for a new input.
    
    Returns
    ----------
    prob : float
        The float form of the final valid input probability.
    """

    while True:
        # With each repeat of the loop, reask for the user input
        in_prob: str = input("\"Alive\" Probability: ")
        
        # Check if input can be interpreted as a float (probabilities are floats)
        try:
            prob: float = float(in_prob)
        except ValueError:
            print("I'm sorry, that could not be interpreted as a valid probability. Please input a number between 0 and 1.")
        
        # Check if input can be interpreted as a probability (must be between 0 and 1)
        if not (0 < prob < 1):
            print("I'm sorry, that could not be interpreted as a valid probability. Please input a number between 0 and 1.")
        else:
            return prob
        

def _reask_seed_until_valid() -> Generator:
    """
    Helper function for generate_random_state.
    Asks for user input for random seed for reproducibility.
    If the input is invalid, notifies user instead of crashing and asks for a new input.
    
    Returns
    ----------
    rng : np.random.Generator
        The seeded random number generator.
    """

    while True:
        # With each repeat of the loop, reask for the user input
        in_seed: str = input("Seed: ")
        
        # If the user input none, do not seed the RNG (indeterministic)
        if in_seed.lower() == "none":
            return np.random.default_rng(None)

        # Otherwise, try to convert to use input as seed, if invalid repeat the loop and prompt again.
        try:
            seed: int = int(in_seed)
            return np.random.default_rng(seed)
        except ValueError:
            print("I'm sorry, that is not a valid seed. Please either input an integer or \"None\"")


def generate_random_state() -> None:
    """
    Generates randomized grid. Prompts user with questions about the generation first.

    Returns
    ----------
    start : np.ndarray
        Binary 2D numpy array with randomly generated starting state.
    """

    # --- Collecting Additional Specifications from the User ---
    print("In order to generate the randomized grid, please provide additional specifications:")
    # Allow user to control grid size
    print("What size would you like the generated grid to be?")
    # Use while loops to re-ask instead of crashing when user provides invalid input
    in_width: int = _reask_dim_size_until_valid("Width: ")
    in_height: int = _reask_dim_size_until_valid("Height: ")
    # Allow user to choose a probability of each cell being alive
    # This will control the overall ratio of active cells in the generated state
    print("What should the probability of each cell being \"alive\" be?")
    # Use while loop to re-ask instead of crashing when user provides invalid input
    in_alive_prob: float = _reask_prob_until_valid()

    print(
        "If you would like to ensure reproducibility, you may input a random seed. \n"
        "Using the same seed again will allow you to regenerate the exact same randomized starting state. \n"
        "If you do not want reproducibility, you can input \"None\" instead to get different results every time."
    )
    rng: Generator = _reask_seed_until_valid()

    # --- Generating Random Grid Using User Specifications ---
    # Generate matrix of random floats between 0-1 using size specifications
    random_matrix: np.ndarray = rng.random((in_width, in_height))
    # The probability of a uniformly sampled float between 0-1 being below the input probability is equal to this probability
    # Using it as a threshold results in a matrix where each cell has this probability of being a 1, i.e. "alive"
    start: np.ndarray = (random_matrix < in_alive_prob).astype(int)
    
    return start