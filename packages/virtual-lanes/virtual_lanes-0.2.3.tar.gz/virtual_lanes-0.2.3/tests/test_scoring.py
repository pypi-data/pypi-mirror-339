import pytest
from virtual_lanes import Scoring


# Define a fixture for common sets of frame data
@pytest.fixture
def example_frames():
    return {
        "normal_game": [(6, 3), (7, 2), (3, 7), (10, 0), (8, 0), (2, 8), (1, 9), (10, 0), (10, 0), (6, 4, 5)],
        "perfect_game": [(10, 0) for _ in range(9)] + [(10, 10, 10)],
        "no_strikes_spares": [(8, 1) for _ in range(9)] + [(8, 1, 0)],
        "nine_pin_no_tap": [(9, 0) for _ in range(9)] + [(9, 1, 9)]
    }


def test_traditional_scoring(example_frames):
    assert Scoring.traditional(example_frames["normal_game"]) == 156
    assert Scoring.traditional(example_frames["perfect_game"]) == 300
    assert Scoring.traditional(example_frames["no_strikes_spares"]) == 90


def test_current_frame_scoring(example_frames):
    assert Scoring.current_frame(example_frames["normal_game"]) == 167
    assert Scoring.current_frame(example_frames["perfect_game"]) == 300
    assert Scoring.current_frame(example_frames["no_strikes_spares"]) == 90


def test_nine_pin_no_tap(example_frames):
    # This assumes that knocking down 9 pins counts as a strike in no-tap.
    assert Scoring.nine_pin_no_tap(example_frames["nine_pin_no_tap"]) == 192  # This needs validation for rules
