import pytest
from typing import Dict, Any

from validation import validate_inputs, VALID_START_OPTIONS


# Establish base set of valid parameters
# When testing a given parameter, the others will be set to the values in this dict
VALID_BASE: Dict[str, Any] = {
    "steps": 10,
    "rule_string": "S23B3",
    "start_choice": "block",
    "update_rate": 0.8,
    "seed": 1,
    "seconds_per_step": 0.4
}

# --- Testing Values ---
# For each parameter, define lists of inputs that should and should not raise errors

VALID_STEPS: list[int] = [0, 1, 100, 500]
INVALID_STEPS: list[Any] = [-1, 0.5, None]

VALID_RULE_STRINGS: list[str] = ["SB", "S012345678B012345678", "S7B6"]
INVALID_RULE_STRINGS: list[Any] = ["S9B9", "S123", "B123", "B12S32", 123, None, True]

VALID_START_CHOICES: list[str] = VALID_START_OPTIONS
INVALID_START_CHOICES: list[Any] = ["RANDOM", "Randomize", 123, None, True]

VALID_UPDATE_RATES: list[float] = [0.0, 0.1, 0.99, 1.0]
INVALID_UPDATE_RATES: list[Any] = [1.1, -0.2, 10, None, "0.8"]

VALID_SEEDS: list[int|None] = [1, None]
INVALID_SEEDS: list[Any] = [0.5, "None", "42"]

VALID_SECONDS_PER_STEP: list[float] = [0.1, 5.0]
INVALID_SECONDS_PER_STEP: list[Any] = [-0.1, 0.0, None, "0.8"]


# --- Testing Validation Function with Valid and Invalid Inputs ---

# -- Testing Steps Options --
@pytest.mark.parametrize("steps", VALID_STEPS)  # loop through parameter options, testing each
def test_valid_steps(steps):
    test_params: Dict[str, Any] = VALID_BASE.copy()  # create a copy of the valid base...
    test_params.update({"steps": steps})  # and swap in the parameter being tested
    validate_inputs(**test_params)

@pytest.mark.parametrize("steps", INVALID_STEPS)
def test_invalid_steps(steps):
    with pytest.raises((TypeError, ValueError)):
        test_params: Dict[str, Any] = VALID_BASE.copy()
        test_params.update({"steps": steps})
        validate_inputs(**test_params)


# -- Testing Rule String Options --
@pytest.mark.parametrize("rule_string", VALID_RULE_STRINGS)
def test_valid_rule_strings(rule_string):
    test_params: Dict[str, Any] = VALID_BASE.copy()
    test_params.update({"rule_string": rule_string})
    validate_inputs(**test_params)

@pytest.mark.parametrize("rule_string", INVALID_RULE_STRINGS)
def test_invalid_rule_strings(rule_string):
    with pytest.raises((TypeError, ValueError, Warning)):  # warning when 9 in rule
        test_params: Dict[str, Any] = VALID_BASE.copy()
        test_params.update({"rule_string": rule_string})
        validate_inputs(**test_params)


# -- Testing Start Choice Options --
@pytest.mark.parametrize("start_choice", VALID_START_CHOICES)
def test_valid_start_choices(start_choice):
    test_params: Dict[str, Any] = VALID_BASE.copy()
    test_params.update({"start_choice": start_choice})
    validate_inputs(**test_params)

@pytest.mark.parametrize("start_choice", INVALID_START_CHOICES)
def test_invalid_start_choices(start_choice):
    with pytest.raises((TypeError, ValueError)):
        test_params: Dict[str, Any] = VALID_BASE.copy()
        test_params.update({"start_choice": start_choice})
        validate_inputs(**test_params)


# -- Testing Update Rate Options --
@pytest.mark.parametrize("update_rate", VALID_UPDATE_RATES)
def test_valid_update_rates(update_rate):
    test_params: Dict[str, Any] = VALID_BASE.copy()
    test_params.update({"update_rate": update_rate})
    validate_inputs(**test_params)

@pytest.mark.parametrize("update_rate", INVALID_UPDATE_RATES)
def test_invalid_update_rates(update_rate):
    with pytest.raises((TypeError, ValueError)):
        test_params: Dict[str, Any] = VALID_BASE.copy()
        test_params.update({"update_rate": update_rate})
        validate_inputs(**test_params)


# -- Testing Seed Options --
@pytest.mark.parametrize("seed", VALID_SEEDS)
def test_valid_seeds(seed):
    test_params: Dict[str, Any] = VALID_BASE.copy()
    test_params.update({"seed": seed})
    validate_inputs(**test_params)

@pytest.mark.parametrize("seed", INVALID_SEEDS)
def test_invalid_seeds(seed):
    with pytest.raises((TypeError, ValueError)):
        test_params: Dict[str, Any] = VALID_BASE.copy()
        test_params.update({"seed": seed})
        validate_inputs(**test_params)


# -- Testing Seconds Per Step Options --
@pytest.mark.parametrize("seconds_per_step", VALID_SECONDS_PER_STEP)
def test_valid_seconds_per_step(seconds_per_step):
    test_params: Dict[str, Any] = VALID_BASE.copy()
    test_params.update({"seconds_per_step": seconds_per_step})
    validate_inputs(**test_params)

@pytest.mark.parametrize("seconds_per_step", INVALID_SECONDS_PER_STEP)
def test_invalid_seconds_per_step(seconds_per_step):
    with pytest.raises((TypeError, ValueError)):
        test_params: Dict[str, Any] = VALID_BASE.copy()
        test_params.update({"seconds_per_step": seconds_per_step})
        validate_inputs(**test_params)