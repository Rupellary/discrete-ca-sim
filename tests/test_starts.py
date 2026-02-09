import pytest
from starting_states import START_OPTIONS, get_start

VALID_START_CHOICES = list(START_OPTIONS.keys()) + ["random_choice", "randomize"]
INVALID_START_CHOICES = ["", None, "hello", "S23B3"]

# Test that all valid start options work
@pytest.mark.parametrize(
    "start_choice", 
    VALID_START_CHOICES
)
def test_valid_start_retrieval(start_choice):
    get_start(start_choice)


# Test that all invalid start options don't work
@pytest.mark.parametrize(
    "start_choice", 
    INVALID_START_CHOICES
)
def test_valid_start_retrieval(start_choice):
    with pytest.raises(ValueError):
        get_start(start_choice)


# Test that all matrices are 2D
@pytest.mark.parametrize(
    "start_choice", 
    VALID_START_CHOICES
)
def test_start_2d(start_choice):
    starting_state = get_start(start_choice)
    assert starting_state.ndim == 2

