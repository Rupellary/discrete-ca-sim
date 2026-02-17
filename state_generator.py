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
        except:
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
        in_prob: str = input("\"Alive\" Probability: ")
        
        try:
            prob: float = float(in_prob)
        except:
            print("I'm sorry, that could not be interpreted as a valid probability. Please input a number between 0 and 1.")
        
        if not (0 < prob < 1):
            print("I'm sorry, that could not be interpreted as a valid probability. Please input a number between 0 and 1.")
        else:
            return prob


def generate_random_state(rng: Generator) -> None:
    """
    Generates randomized grid. Prompts user with questions about the generation first.

    Parameters
    ----------
    rng : np.random.Generator
        Numpy random number generator. Allows for deterministic generation.

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

    # --- Generating Random Grid Using User Specifications ---
    # Generate matrix of random floats between 0-1 using size specifications
    random_matrix: np.ndarray = rng.random((in_width, in_height))
    # The probability of a uniformly sampled float between 0-1 being below the input probability is equal to this probability
    # Using it as a threshold results in a matrix where each cell has this probability of being a 1, i.e. "alive"
    start: np.ndarray = (random_matrix < in_alive_prob).astype(int)
    
    return start