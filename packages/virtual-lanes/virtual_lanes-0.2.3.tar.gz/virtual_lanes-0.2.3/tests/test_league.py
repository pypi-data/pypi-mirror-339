import pytest
from virtual_lanes import Bowler, Alley, League


def test_league_initialisation():
    alley = Alley(name="Pin Palace", location="Suburban", lane_type="Wood")
    league = League("City League", alley, "Medium Oil", 4, 3, 10)
    assert league.name == "City League"
    assert league.alley == alley
    assert league.oil_pattern == "Medium Oil"
    assert league.team_size == 4
    assert league.num_games_per_night == 3
    assert league.season_length == 10


def test_add_team():
    alley = Alley(name="Pin Palace", location="Suburban", lane_type="Wood")
    league = League("City League", alley, "Medium Oil", 2, 3, 10)
    team = [Bowler("John Doe", 0.3, 0.5), Bowler("Jane Doe", 0.25, 0.6)]
    league.add_team(team)
    assert len(league.teams) == 1
    assert league.teams[0] == team


def test_add_team_with_incorrect_size():
    alley = Alley(name="Pin Palace", location="Suburban", lane_type="Wood")
    league = League("City League", alley, "Medium Oil", 3, 3, 10)
    team = [Bowler("John Doe", 0.3, 0.5), Bowler("Jane Doe", 0.25, 0.6)]  # Only 2 bowlers
    with pytest.raises(ValueError):
        league.add_team(team)


def test_run_season():
    alley = Alley(name="Pin Palace", location="Suburban", lane_type="Wood")
    league = League("City League", alley, "Medium Oil", 2, 3, 2)  # A short 2-week season for testing
    team1 = [Bowler("John Doe", 0.3, 0.5), Bowler("Jane Doe", 0.25, 0.6)]
    team2 = [Bowler("Alice Smith", 0.35, 0.55), Bowler("Bob Johnson", 0.28, 0.45)]
    league.add_team(team1)
    league.add_team(team2)
    results = league.run_season()
    assert isinstance(results, dict)
    assert len(results) == 2
    assert all(isinstance(scores, list) for scores in results.values())

# Optional: Further detailed tests can be implemented to check the accuracy of score calculations,
# consistency across games, etc.
# Additional tests can include:
# - Test for handling of invalid team sizes.
# - Test for handling of invalid season lengths.
# - Test for handling of invalid number of games per night.
# - Test for handling of incomplete teams.
# - Test for accurate calculation of average scores.
# - Test for consistent results across multiple runs.
# - Test for handling of edge cases (e.g., empty teams, zero-length season).