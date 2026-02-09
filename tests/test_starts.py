import pytest
import numpy as np
from numpy.random import Generator
from typing import Any

from starting_states import START_OPTIONS, get_start

VALID_START_CHOICES: list[str] = list(START_OPTIONS.keys()) + ["random_choice", "randomize"]
INVALID_START_CHOICES: list[Any] = ["", None, "hello", "S23B3"]
RANDOM_SEED: int = 42
RNG: Generator = np.random.default_rng(RANDOM_SEED)


# Test that all valid start options work
@pytest.mark.parametrize(
    "start_choice", 
    VALID_START_CHOICES
)
def test_valid_start_retrieval(start_choice):
    get_start(start_choice, rng=RNG)


# Test that all invalid start options don't work
@pytest.mark.parametrize(
    "start_choice", 
    INVALID_START_CHOICES
)
def test_valid_start_retrieval(start_choice):
    with pytest.raises(ValueError):
        get_start(start_choice, RNG)


# Test that all matrices are 2D
@pytest.mark.parametrize(
    "start_choice", 
    VALID_START_CHOICES
)
def test_start_2d(start_choice):
    starting_state: np.ndarray = get_start(start_choice, RNG)
    assert starting_state.ndim == 2

