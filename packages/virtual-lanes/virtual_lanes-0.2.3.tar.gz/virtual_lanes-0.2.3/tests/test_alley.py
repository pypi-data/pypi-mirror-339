import pytest
from virtual_lanes import Alley


def test_alley_creation():
    # Test the creation of an Alley instance
    alley = Alley(name="Kingpin Alley", location="Springfield", lane_type="Synthetic")
    assert alley.name == "Kingpin Alley"
    assert alley.location == "Springfield"
    assert alley.lane_type == "Synthetic"


def test_alley_name_assignment():
    # Test that the name attribute is set correctly
    alley = Alley(name="Pine Lanes", location="Shelbyville", lane_type="Wood")
    assert alley.name == "Pine Lanes"


def test_alley_location_assignment():
    # Test that the location attribute is set correctly
    alley = Alley(name="Pine Lanes", location="Shelbyville", lane_type="Wood")
    assert alley.location == "Shelbyville"


def test_alley_lane_type_assignment():
    # Test that the lane_type attribute is set correctly
    alley = Alley(name="Pine Lanes", location="Shelbyville", lane_type="Wood")
    assert alley.lane_type == "Wood"


def test_alley_invalid_lane_type():
    # Optionally, test for handling of invalid lane types if such validation is implemented
    with pytest.raises(ValueError):
        Alley(name="Pine Lanes", location="Shelbyville", lane_type="Plastic")

# Additional tests can include:
# - Test updating an existing alley.
# - Test adding games to an alley.
# - Test retrieving data to ensure it matches what was inserted.
# - Test deleting data.
# - Test handling of invalid data.
