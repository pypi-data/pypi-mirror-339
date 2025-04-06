import pytest
from virtual_lanes import Bowler


def test_bowler_creation():
    # Test creating a Bowler instance with expected attributes
    bowler = Bowler("John Doe", strike_prob=0.3, spare_prob=0.5)
    assert bowler.name == "John Doe"
    assert bowler.strike_prob == 0.3
    assert bowler.spare_prob == 0.5
    assert bowler.handedness == 'right'  # Default value
    assert bowler.technique == 'single'  # Default value


def test_bowler_string_representation():
    # Test the string representation of the Bowler
    bowler = Bowler("Jane Doe", strike_prob=0.25, spare_prob=0.6, handedness='left', technique='double')
    expected_string = "Bowler(Name: Jane Doe, Strike Probability: 0.25, Spare Probability: 0.6, Handedness: left, Technique: double)"
    assert str(bowler) == expected_string


def test_bowler_with_invalid_probabilities():
    # Test handling of invalid probability values
    with pytest.raises(ValueError):
        Bowler("Invalid Prob", strike_prob=1.1, spare_prob=-0.1)

    with pytest.raises(ValueError):
        Bowler("Invalid Prob", strike_prob=-0.1, spare_prob=1.1)
