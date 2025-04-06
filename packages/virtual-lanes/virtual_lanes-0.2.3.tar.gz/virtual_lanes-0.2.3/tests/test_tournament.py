import pytest
from virtual_lanes import Bowler, Alley, Tournament


@pytest.fixture
def sample_bowlers():
    return [Bowler("John Doe", strike_prob=0.3, spare_prob=0.5), Bowler("Jane Smith", strike_prob=0.4, spare_prob=0.4)]

@pytest.fixture
def sample_alley():
    return Alley("Strike Zone", "Medium", "Synthetic")

@pytest.fixture
def sample_tournament(sample_bowlers, sample_alley):
    return Tournament(sample_bowlers, sample_alley, num_games=3)


def test_tournament_initialization(sample_bowlers, sample_alley):
    tournament = Tournament(sample_bowlers, sample_alley, num_games=3)
    assert tournament.num_games == 3
    assert len(tournament.bowlers) == 2
    assert tournament.alley.lane_type == "Synthetic"
    assert all(name in tournament.results for name in ["John Doe", "Jane Smith"])


def test_run_tournament(sample_tournament):
    sample_tournament.run_tournament()
    # Check that results are recorded for each game
    assert all(len(scores) == sample_tournament.num_games for scores in sample_tournament.results.values())


def test_get_results(sample_tournament):
    sample_tournament.run_tournament()
    results = sample_tournament.get_results()
    # Ensure results match expected format and contents
    assert isinstance(results, dict)
    assert all(isinstance(scores, list) for scores in results.values())
    assert all(isinstance(score, int) for scores in results.values() for score in scores)


def test_get_average_scores(sample_tournament):
    sample_tournament.run_tournament()
    averages = sample_tournament.get_average_scores()
    # Check that averages are calculated correctly
    assert isinstance(averages, dict)
    assert all(isinstance(avg, float) for avg in averages.values())
    # Ensure every bowler has an average score calculated
    assert len(averages) == len(sample_tournament.bowlers)
