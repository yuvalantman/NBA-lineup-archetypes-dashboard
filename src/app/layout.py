from dash import html, dcc
from src.app.components.player_profile import create_player_profile_component
from src.app.components.team_vs_opp_placeholder import create_team_vs_opp_placeholder

def create_layout(app, df_players):
    """
    Creates the main dashboard layout with hierarchical filtering.

    Args:
        app: Dash application instance
        df_players: DataFrame with player data (efficiency data with star_player column)

    Returns:
        Dash HTML component with complete dashboard layout
    """
    if df_players is None or df_players.empty:
        return html.Div("Error: Data could not be loaded.", style={'color': 'red', 'textAlign': 'center'})

    return html.Div(
        style={
            'backgroundColor': '#0b1019',
            'minHeight': '100vh',
            'padding': '20px',
            'fontFamily': 'Segoe UI, sans-serif',
            'color': 'white'
        },
        children=[
            # --- HEADER ---
            html.Div(
                style={'textAlign': 'center', 'marginBottom': '30px', 'borderBottom': '2px solid rgba(0, 191, 255, 0.3)'},
                children=[
                    html.H1("🏀 NBA Lineup Strategic Analysis Dashboard",
                            style={'color': '#00BFFF', 'fontSize': '32px', 'margin': '0'}),
                    html.P("Strategic Insights for Star-Driven Lineups",
                           style={'color': '#8e9aaf', 'fontSize': '14px'})
                ]
            ),

            # --- MAIN CONTENT AREA ---
            html.Div(
                style={'display': 'flex', 'gap': '25px', 'alignItems': 'flex-start'},
                children=[

                    # ======================
                    # SIDEBAR (Left Column)
                    # ======================
                    html.Div(
                        style={'flex': '0 0 380px', 'display': 'flex', 'flexDirection': 'column', 'gap': '20px'},
                        children=[
                            # Player selection and profile (includes image and bio data)
                            create_player_profile_component(
                                df_players=df_players,
                                component_id='star-profile'
                            ),

                            # Matchup analysis placeholder
                            create_team_vs_opp_placeholder()
                        ]
                    ),

                    # =============================
                    # MAIN VISUALIZATION AREA (Right)
                    # =============================
                    html.Div(
                        style={'flex': '1', 'display': 'flex', 'flexDirection': 'column', 'gap': '20px'},
                        children=[

                            # Top control bar: Graph title + Compact lineup filter
                            html.Div(
                                style={
                                    'display': 'flex',
                                    'justifyContent': 'space-between',
                                    'alignItems': 'center',
                                    'backgroundColor': '#161d2b',
                                    'padding': '12px 20px',
                                    'borderRadius': '12px',
                                    'border': '1px solid #2d384d',
                                    'marginBottom': '10px'
                                },
                                children=[
                                    html.H4(id='shot-chart-title', children="Shot Chart",
                                            style={'color': '#00BFFF', 'margin': '0', 'fontSize': '18px'}),

                                    # Compact lineup selector (Fixed Height, No visible tags)
                                    html.Div(
                                        style={
                                            'width': '280px',
                                            'display': 'flex',
                                            'flexDirection': 'column',
                                            'gap': '4px'
                                        },
                                        children=[
                                            html.Label("Select Lineups:",
                                                       style={'fontSize': '11px', 'color': 'rgba(255,255,255,0.7)', 'fontWeight': 'bold', 'marginBottom': '2px'}),
                                            dcc.Dropdown(
                                                id='lineup-dropdown',
                                                options=[], # Populated by callback
                                                multi=True,
                                                placeholder="Click to select...",
                                                className="custom-clean-dropdown",
                                                style={'fontSize': '13px'}
                                            )
                                        ]
                                    )
                                ]
                            ),

                            # SHOT CHART graph (colors: deep green and red)
                            html.Div(
                                style={'backgroundColor': '#161d2b', 'borderRadius': '15px', 'padding': '20px', 'border': '1px solid #2d384d'},
                                children=[
                                    dcc.Graph(id='shot-chart-graph', style={'height': '500px'})
                                ]
                            ),

                            # Bottom row: Radar (orange-brown) + Efficiency
                            html.Div(
                                style={'display': 'flex', 'gap': '20px'},
                                children=[
                                    # Tendency Radar
                                    html.Div(
                                        style={'flex': '1', 'backgroundColor': '#161d2b', 'borderRadius': '15px', 'padding': '20px', 'border': '1px solid #2d384d'},
                                        children=[
                                            html.H5(id='radar-chart-title', children="Luka Dončić - Lineup Tendency Profile", style={'color': '#00BFFF'}),
                                            dcc.Graph(id='tendency-radar-graph', style={'height': '350px'})
                                        ]
                                    ),
                                    # Efficiency Landscape
                                    html.Div(
                                        style={'flex': '1', 'backgroundColor': '#161d2b', 'borderRadius': '15px', 'padding': '20px', 'border': '1px solid #2d384d'},
                                        children=[
                                            html.H5("Efficiency Landscape", style={'color': '#00BFFF'}),
                                            dcc.Graph(id='efficiency-graph', style={'height': '350px'})
                                        ]
                                    )
                                ]
                            )
                        ]
                    )
                ]
            )
        ]
    )
