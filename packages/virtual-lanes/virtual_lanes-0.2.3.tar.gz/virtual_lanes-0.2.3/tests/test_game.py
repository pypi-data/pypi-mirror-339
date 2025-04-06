import pytest
from virtual_lanes import Bowler, Alley, Game


@pytest.fixture
def setup_bowlers_and_alley():
    bowlers = [
        Bowler(name="John Doe", strike_prob=0.5, spare_prob=0.3, handedness='right', technique='single'),
        Bowler(name="Jane Doe", strike_prob=0.4, spare_prob=0.4, handedness='left', technique='double')
    ]
    alley = Alley(name="Main Street Lanes", location="123 Main St", lane_type="Synthetic")
    return bowlers, alley


def test_simulate_regular_frame(setup_bowlers_and_alley):
    bowlers, alley = setup_bowlers_and_alley
    game = Game(bowlers, alley, random_seed=42)
    frame_result = game.simulate_regular_frame(bowlers[0])
    assert isinstance(frame_result, tuple)
    assert len(frame_result) == 2  # Should always return two rolls unless a strike
    assert all(isinstance(pins, int) for pins in frame_result)


def test_simulate_last_frame(setup_bowlers_and_alley):
    bowlers, alley = setup_bowlers_and_alley
    game = Game(bowlers, alley, random_seed=42)
    frame_result = game.simulate_last_frame(bowlers[0])
    print(frame_result)
    assert isinstance(frame_result, tuple)
    assert 2 <= len(frame_result) <= 3  # Last frame can have two or three rolls


def test_frame_by_frame_generator(setup_bowlers_and_alley):
    bowlers, alley = setup_bowlers_and_alley
    game = Game(bowlers, alley, random_seed=42)
    frames = list(game.frame_by_frame_generator())
    assert len(frames) == 10  # There should be exactly 10 frames
    for frame in frames:
        assert isinstance(frame, dict)
        for name, result in frame.items():
            assert isinstance(result, tuple)


def test_simulate_game(setup_bowlers_and_alley):
    bowlers, alley = setup_bowlers_and_alley
    game = Game(bowlers, alley, random_seed=42)
    game_results = game.simulate_game()
    assert isinstance(game_results, dict)
    for name, frames in game_results.items():
        assert len(frames) == 10  # Each bowler should have exactly 10 frames
        for frame in frames:
            assert isinstance(frame, tuple)


def test_randomness_consistency():
    bowlers = [Bowler(name="Test Bowler", strike_prob=0.5, spare_prob=0.3)]
    alley = Alley(name="Strike Zone", lane_type="Wood", location="123 Main Street")
    game1 = Game(bowlers, alley, random_seed=123)
    game2 = Game(bowlers, alley, random_seed=123)
    results1 = game1.simulate_game()
    results2 = game2.simulate_game()
    assert results1 == results2  # Results should be the same due to the same random seed
