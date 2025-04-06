"""VirtualLanes Web Interface using FastHTML."""

from fasthtml.common import *
import numpy as np
from virtual_lanes import (
    alley, bowler, game, league, tournament, scoring
)

def create_app(debug=False):
    """Create the FastHTML application."""
    app, rt = fast_app(debug=debug)
    
    @rt("/")
    def get():
        return Titled("VirtualLanes", 
            Div(
                H1("Welcome to VirtualLanes"),
                P("A ten-pin bowling simulation library designed to model games, analyze player performance, and explore the effects of different bowling conditions."),
                Grid(
                    Card(
                        H3("Bowlers"),
                        P("Manage bowlers and their statistics."),
                        A("View Bowlers", href="/bowlers"),
                        header=H3("Bowlers")
                    ),
                    Card(
                        H3("Games"),
                        P("Track and analyze bowling games."),
                        A("View Games", href="/games"),
                        header=H3("Games")
                    ),
                    Card(
                        H3("Leagues"),
                        P("Manage bowling leagues and tournaments."),
                        A("View Leagues", href="/leagues"),
                        header=H3("Leagues")
                    )
                )
            )
        )
    
    @rt("/bowlers")
    def get():
        # Example bowlers for demonstration
        example_bowlers = [
            bowler.Bowler("John Doe", 180),
            bowler.Bowler("Jane Smith", 210),
            bowler.Bowler("Bob Johnson", 160)
        ]
        
        return Titled("TrueRoll - Bowlers",
            Div(
                H1("Bowlers"),
                Ul(*[Li(
                    H3(f"{b.name} - Average: {b.average}"),
                    id=f"bowler-{i}"
                ) for i, b in enumerate(example_bowlers)]),
                Button("Add Bowler", hx_get="/bowlers/new", hx_target="#new-bowler-form"),
                Div(id="new-bowler-form")
            )
        )
    
    @rt("/bowlers/new")
    def get():
        return Form(
            Input(id="name", placeholder="Bowler Name"),
            Input(id="average", placeholder="Average Score", type="number"),
            Button("Save", type="submit"),
            hx_post="/bowlers/create",
            hx_target="#bowlers-list"
        )
    
    @rt("/games")
    def get():
        return Titled("TrueRoll - Games",
            Div(
                H1("Games"),
                P("Track and analyze bowling games here.")
            )
        )
    
    @rt("/leagues")
    def get():
        return Titled("TrueRoll - Leagues",
            Div(
                H1("Leagues"),
                P("Manage bowling leagues and tournaments here.")
            )
        )
    
    return app

def run_server(host="127.0.0.1", port=8000, debug=False):
    """Run the FastHTML web server."""
    app = create_app(debug=debug)
    serve(app=app, host=host, port=port)

if __name__ == "__main__":
    run_server(debug=True)