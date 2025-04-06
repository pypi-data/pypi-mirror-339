"""VirtualLanes CLI commands."""

import typer
from typing import Optional, List
import virtual_lanes
from virtual_lanes.tui import app as tui_app
from virtual_lanes.web import app as web_app
import rich
from rich.console import Console
from rich.table import Table

console = Console()
app = typer.Typer(help="VirtualLanes bowling management and simulation.")
bowlers_app = typer.Typer(help="Manage bowlers.")
games_app = typer.Typer(help="Manage games.")
leagues_app = typer.Typer(help="Manage leagues.")
web_app_cmd = typer.Typer(help="Run web interface.")
tui_app_cmd = typer.Typer(help="Run terminal user interface.")

# Register subcommands
app.add_typer(bowlers_app, name="bowlers")
app.add_typer(games_app, name="games")
app.add_typer(leagues_app, name="leagues")
app.add_typer(web_app_cmd, name="web")
app.add_typer(tui_app_cmd, name="tui")

# Main command
@app.callback()
def callback():
    """
    TrueRoll - A ten-pin bowling simulation and management tool.
    """
    pass

# Web interface commands
@web_app_cmd.command("start")
def web_start(
    host: str = typer.Option("127.0.0.1", "--host", "-h", help="Host address to bind to"),
    port: int = typer.Option(8000, "--port", "-p", help="Port to bind to"),
    debug: bool = typer.Option(False, "--debug", help="Enable debug mode"),
):
    """Start the web interface."""
    console.print(f"Starting web server on {host}:{port}...")
    web_app.run_server(host=host, port=port, debug=debug)

# TUI commands
@tui_app_cmd.command("start")
def tui_start():
    """Start the terminal user interface."""
    tui_app.run_app()

# Bowler commands
@bowlers_app.command("list")
def list_bowlers():
    """List all bowlers."""
    # Example data
    bowlers = [
        {"name": "John Doe", "average": 180},
        {"name": "Jane Smith", "average": 210},
        {"name": "Bob Johnson", "average": 160},
    ]
    
    table = Table(title="Bowlers")
    table.add_column("Name")
    table.add_column("Average")
    
    for b in bowlers:
        table.add_row(b["name"], str(b["average"]))
    
    console.print(table)

@bowlers_app.command("add")
def add_bowler(
    name: str = typer.Argument(..., help="Bowler name"),
    average: int = typer.Argument(..., help="Bowler average"),
):
    """Add a new bowler."""
    console.print(f"Added bowler: {name} with average: {average}")

# Game commands
@games_app.command("list")
def list_games():
    """List all games."""
    # Example data
    games = [
        {"date": "2023-05-01", "bowler": "John Doe", "score": 185},
        {"date": "2023-05-02", "bowler": "Jane Smith", "score": 215},
        {"date": "2023-05-03", "bowler": "Bob Johnson", "score": 155},
    ]
    
    table = Table(title="Games")
    table.add_column("Date")
    table.add_column("Bowler")
    table.add_column("Score")
    
    for g in games:
        table.add_row(g["date"], g["bowler"], str(g["score"]))
    
    console.print(table)

@games_app.command("add")
def add_game(
    bowler: str = typer.Argument(..., help="Bowler name"),
    score: int = typer.Argument(..., help="Game score"),
):
    """Add a new game."""
    console.print(f"Added game for {bowler} with score: {score}")

# League commands
@leagues_app.command("list")
def list_leagues():
    """List all leagues."""
    # Example data
    leagues = [
        {"name": "Friday Night League", "members": 12},
        {"name": "Sunday Afternoon League", "members": 8},
    ]
    
    table = Table(title="Leagues")
    table.add_column("Name")
    table.add_column("Members")
    
    for l in leagues:
        table.add_row(l["name"], str(l["members"]))
    
    console.print(table)

@leagues_app.command("add")
def add_league(
    name: str = typer.Argument(..., help="League name"),
):
    """Add a new league."""
    console.print(f"Added league: {name}")

if __name__ == "__main__":
    app()