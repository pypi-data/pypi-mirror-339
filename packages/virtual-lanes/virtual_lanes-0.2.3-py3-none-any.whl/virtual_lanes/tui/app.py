"""VirtualLanes Terminal User Interface using Textual."""

from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Static, Button, DataTable
from textual.containers import Container
import virtual_lanes

class BowlerList(Static):
    """A list of bowlers."""
    
    def compose(self) -> ComposeResult:
        """Compose the bowler list."""
        yield Static("Bowlers", classes="heading")
        table = DataTable()
        table.add_column("Name")
        table.add_column("Average")
        
        # Example data
        table.add_row("John Doe", "180")
        table.add_row("Jane Smith", "210")
        table.add_row("Bob Johnson", "160")
        
        yield table
        yield Button("Add Bowler", id="add-bowler")

class GameList(Static):
    """A list of games."""
    
    def compose(self) -> ComposeResult:
        """Compose the game list."""
        yield Static("Games", classes="heading")
        table = DataTable()
        table.add_column("Date")
        table.add_column("Bowler")
        table.add_column("Score")
        
        # Example data
        table.add_row("2023-05-01", "John Doe", "185")
        table.add_row("2023-05-02", "Jane Smith", "215")
        table.add_row("2023-05-03", "Bob Johnson", "155")
        
        yield table
        yield Button("Add Game", id="add-game")

class LeagueList(Static):
    """A list of leagues."""
    
    def compose(self) -> ComposeResult:
        """Compose the league list."""
        yield Static("Leagues", classes="heading")
        table = DataTable()
        table.add_column("Name")
        table.add_column("Members")
        
        # Example data
        table.add_row("Friday Night League", "12")
        table.add_row("Sunday Afternoon League", "8")
        
        yield table
        yield Button("Add League", id="add-league")

class TrueRollApp(App):
    """The main TrueRoll TUI application."""
    
    TITLE = "TrueRoll"
    CSS = """
    .heading {
        background: $accent;
        color: $text;
        padding: 1 2;
        font-weight: bold;
        margin-bottom: 1;
    }
    
    Screen {
        layout: grid;
        grid-size: 3;
        grid-gutter: 1;
        padding: 1;
    }
    
    BowlerList {
        height: 100%;
        border: solid $accent;
    }
    
    GameList {
        height: 100%;
        border: solid $accent;
    }
    
    LeagueList {
        height: 100%;
        border: solid $accent;
    }
    """
    
    def compose(self) -> ComposeResult:
        """Compose the application layout."""
        yield Header(show_clock=True)
        yield BowlerList()
        yield GameList()
        yield LeagueList()
        yield Footer()

def run_app():
    """Run the TrueRoll TUI application."""
    app = TrueRollApp()
    app.run()

if __name__ == "__main__":
    run_app()