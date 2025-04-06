import pytest
from virtual_lanes import BowlingDatabase
from virtual_lanes import Bowler, Alley

@pytest.fixture
def db():
    """Fixture to create a new database for each test."""
    database = BowlingDatabase('test_bowling.db')
    yield database
    database.close()
    import os
    os.remove('test_bowling.db')

def test_add_bowler(db):
    """Test adding a new bowler to the database."""
    bowler = Bowler(name="John Doe", strike_prob=0.5, spare_prob=0.3, handedness="right", technique="single")
    bowler_id = db.add_bowler(bowler)
    assert bowler_id is not None
    assert isinstance(bowler_id, int)

def test_add_alley(db):
    """Test adding a new alley to the database."""
    alley = Alley(name="Main Street Lanes", location="123 Main St", lane_type="Synthetic")
    alley_id = db.add_alley(alley)
    assert alley_id is not None
    assert isinstance(alley_id, int)

def test_bowler_with_invalid_probabilities():
    """Test handling of invalid probability values."""
    with pytest.raises(ValueError):
        Bowler(name="Invalid Bowler", strike_prob=1.2, spare_prob=0.8)

# Additional tests can include:
# - Test updating an existing bowler.
# - Test adding game results.
# - Test calculating statistics.
# - Test retrieving data to ensure it matches what was inserted.
# - Test deleting data.
# - Test handling of invalid data.
