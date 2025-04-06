"""VirtualLanes - A ten-pin bowling simulation library."""

# Version information
__version__ = "0.2.3"

# Import classes to expose them at the package level
from .bowler import Bowler
from .alley import Alley
from .game import Game
from .scoring import Scoring
from .tournament import Tournament
from .league import League
from .bowling_database import BowlingDatabase

# Define an __all__ list to restrict what is exported when someone uses from virtual_lanes import *
__all__ = [
    "Bowler",
    "Alley",
    "Game",
    "Scoring",
    "Tournament",
    "BowlingDatabase",
    "League"
]

# Convenience functions to access different interfaces
def run_cli():
    """Run the command-line interface."""
    from virtual_lanes.cli.commands import app
    app()

def run_tui():
    """Run the terminal user interface."""
    from virtual_lanes.tui.app import run_app
    run_app()

def run_web(host="127.0.0.1", port=8000, debug=False):
    """Run the web interface."""
    from virtual_lanes.web.app import run_server
    run_server(host=host, port=port, debug=debug)
