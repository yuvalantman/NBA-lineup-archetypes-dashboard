from dash import html, dcc

def create_layout(app):
    return html.Div([
        html.H1("NBA Archetype Lineup Dashboard"),
        dcc.Dropdown(id="player-dropdown", placeholder="Select a star player"),
        dcc.Dropdown(id="archetype-combo-dropdown", placeholder="Select archetype combo"),
        html.Div(id="metrics-view")
    ])
