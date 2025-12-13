from dash import Input, Output

def register_callbacks(app):
    @app.callback(
        Output("metrics-view", "children"),
        Input("player-dropdown", "value"),
        Input("archetype-combo-dropdown", "value")
    )
    def update_view(player, combo):
        if not player or not combo:
            return "Select a player and archetype combination."
        return f"Showing metrics for {player} with {combo}"
