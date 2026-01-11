from dash import html, dcc
from src.app.components.player_profile import create_player_profile_component
from src.app.components.archetype_profile import create_archetype_card_dash

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
            'color': 'white',
            'overflowX': 'hidden'
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

            # --- HOW TO USE GUIDE ---
            html.Div(
                style={
                    'backgroundColor': 'rgba(0, 191, 255, 0.05)',
                    'border': '1px solid rgba(0, 191, 255, 0.2)',
                    'borderRadius': '8px',
                    'padding': '15px 20px',
                    'marginBottom': '25px',
                    'maxWidth': '1200px',
                    'margin': '0 auto 25px auto'
                },
                children=[
                    html.H3("📖 How to Use This Dashboard", 
                            style={'color': '#00BFFF', 'fontSize': '18px', 'marginTop': '0', 'marginBottom': '10px'}),
                    html.Div(
                        style={'fontSize': '13px', 'color': '#b8c5d6', 'lineHeight': '1.6'},
                        children=[
                            html.P([
                                html.Strong("1. Select a Star Player:", style={'color': '#00BFFF'}),
                                " Choose from the dropdown in the left sidebar to view their profile and statistics."
                            ], style={'margin': '5px 0'}),
                            html.P([
                                html.Strong("2. Choose Main Lineup:", style={'color': '#00BFFF'}),
                                " Each lineup represents 4 player archetypes combination. Select a lineup Archetype to analyze its play style and estimated stats."
                            ], style={'margin': '5px 0'}),
                            html.P([
                                html.Strong("3. Compare Lineups (Optional):", style={'color': '#00BFFF'}),
                                " Multi-select additional lineups to compare tendency patterns on the heatmap."
                            ], style={'margin': '5px 0'}),
                            html.P([
                                html.Strong("4. Analyze Visualizations:", style={'color': '#00BFFF'}),
                                " Efficiency Landscape shows offensive vs defensive ratings. Shot Distribution displays shooting tendencies by location and type. Tendency Heatmap compares playstyle metrics across lineups with color coding (green=high, red=low). Team vs Opponent chart highlights strengths and weaknesses against opponents on the court."
                            ], style={'margin': '5px 0'}),
                            html.P([
                                html.Strong("💡 Tip:", style={'color': '#ffd700'}),
                                " Hover over data points for detailed statistics. Use the graphs to identify optimal lineup combinations and strategic tendencies."
                            ], style={'margin': '5px 0', 'fontStyle': 'italic'})
                        ]
                    )
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
                            # MAIN LINEUP SELECTOR (Step 1)
                            html.Div(
                                style={
                                    'width': '450px',
                                    'display': 'flex',
                                    'flexDirection': 'column',
                                    'gap': '4px'
                                },
                                children=[
                                    html.Label("Main Lineup:",
                                                style={'fontSize': '11px', 'color': '#00BFFF', 'fontWeight': 'bold', 'marginBottom': '2px'}),
                                    dcc.Dropdown(
                                        id='main-lineup-dropdown',
                                        options=[], # Populated by callback
                                        multi=False,
                                        placeholder="Click to select...",
                                        style={'fontSize': '13px', 'color': '#111', 'borderRadius': '5px'}
                                    )
                                ]
                            ),
                            # Compact lineup selector (Fixed Height, No visible tags)
                            # Archetype Specification Section
                            html.Div(
                                style={
                                    'width': '450px',
                                    'display': 'flex',
                                    'flexDirection': 'column',
                                    'gap': '4px',
                                    'marginTop': '18px'
                                },
                                children=[
                                    html.Label("Explore Player Archetypes:",
                                                style={'fontSize': '11px', 'color': '#00BFFF', 'fontWeight': 'bold', 'marginBottom': '2px'}),
                                    dcc.Dropdown(
                                        id='archetype-dropdown',
                                        options=[],  # Populated by callback
                                        placeholder="Select an archetype to explore...",
                                        style={'fontSize': '13px', 'color': '#111', 'borderRadius': '5px'}
                                    ),
                                    # Archetype Profile Card Container
                                    html.Div(id='archetype-card-container', children=create_archetype_card_dash())
                                ]
                            ),

                            # Compare Lineups Section
                            html.Div(
                                style={
                                    'width': '450px',
                                    'display': 'flex',
                                    'flexDirection': 'column',
                                    'gap': '4px',
                                    'marginTop': '20px',
                                    'paddingTop': '20px',
                                    'borderTop': '1px solid rgba(0, 191, 255, 0.2)'
                                },
                                children=[
                                    html.Label("Compare Tendencies with Lineups:",
                                                style={'fontSize': '11px', 'color': '#00BFFF', 'fontWeight': 'bold', 'marginBottom': '2px'}),
                                    dcc.Dropdown(
                                        id='lineup-dropdown',
                                        options=[], # Populated by callback
                                        multi=True,
                                        placeholder="Click to select...",
                                        style={'fontSize': '13px', 'color': '#111', 'borderRadius': '5px'}
                                    )
                                ]
                            )
                        ]
                    ),

                    # =============================
                    # MAIN VISUALIZATION AREA (Right)
                    # =============================
                    html.Div(
                        style={'flex': '1', 'display': 'flex', 'flexDirection': 'column', 'gap': '20px'},
                        children=[

                            # SHOT CHART graph (colors: deep green and red)
                            # html.Div(
                            #     style={'backgroundColor': '#161d2b', 'borderRadius': '15px', 'padding': '20px', 'border': '1px solid #2d384d'},
                            #     children=[
                            #         html.Div(
                            #             style={'flex': '1', 'backgroundColor': '#161d2b', 'borderRadius': '15px', 'padding': '20px', 'border': '1px solid #2d384d'},
                            #             children=[
                            #                 html.H4(id='shot-chart-title', children="Shot Chart",
                            #                     style={'color': '#00BFFF', 'margin': '0', 'fontSize': '18px'}),
                            #                 dcc.Graph(id='shot-chart-graph', style={'height': '500px'})
                            #             ]
                            #         ),
                            #         #dcc.Graph(id='shot-chart-graph', style={'height': '500px'}),
                            #         html.Div(
                            #             style={'flex': '1', 'backgroundColor': '#161d2b', 'borderRadius': '15px', 'padding': '20px', 'border': '1px solid #2d384d'},
                            #             children=[
                            #                 html.H4("Efficiency Landscape", style={'color': '#00BFFF'}),
                            #                 dcc.Graph(id='efficiency-graph', style={'height': '500px'})
                            #             ]
                            #         )
                            #     ]
                            # ),
                            
                            # Main Lineup Specifications Section
                            html.Div(
                                id='main-lineup-specs-container',
                                style={
                                    'backgroundColor': '#161d2b',
                                    'borderRadius': '10px',
                                    'padding': '12px 16px',
                                    'border': '1px solid #2d384d',
                                    'marginBottom': '12px'
                                },
                                children=[
                                    html.H4("Main Lineup Specifications", style={'color': '#00BFFF', 'marginTop': '0', 'marginBottom': '8px', 'fontSize': '15px'}),
                                    html.Div(id='lineup-specs-content', children=[
                                        html.P("Select a lineup to view specifications", style={'color': '#8e9aaf', 'fontStyle': 'italic', 'fontSize': '12px', 'margin': '0'})
                                    ])
                                ]
                            ),
                            
                            html.Div(
                                style={
                                    'display': 'flex',
                                    'gap': '20px',
                                    'backgroundColor': '#161d2b',
                                    'borderRadius': '15px',
                                    'padding': '20px',
                                    'border': '1px solid #2d384d'
                                },
                                children=[

                                    # SHOT CHART
                                    html.Div(
                                        style={
                                            'flex': '1',
                                            'backgroundColor': '#161d2b',
                                            'borderRadius': '15px',
                                            'padding': '20px',
                                            'border': '1px solid #2d384d'
                                        },
                                        children=[
                                            html.Div(
                                                style={
                                                    'display': 'flex',
                                                    'justifyContent': 'space-between',
                                                    'alignItems': 'center',
                                                    'marginBottom': '10px'
                                                },
                                                children=[
                                                    html.H4(
                                                        id='shot-chart-title',
                                                        children="Shot Chart",
                                                        style={'color': '#00BFFF', 'margin': '0', 'fontSize': '18px'}
                                                    ),
                                                    dcc.RadioItems(
                                                        id='shot-chart-type',
                                                        options=[
                                                            {'label': ' Make/Miss', 'value': 'raw'},
                                                            {'label': ' Zones', 'value': 'zones'}
                                                        ],
                                                        value='raw',
                                                        inline=True,
                                                        style={'color': '#8e9aaf', 'fontSize': '12px'},
                                                        labelStyle={'marginLeft': '10px', 'cursor': 'pointer'}
                                                    )
                                                ]
                                            ),
                                            html.P(
                                                "Toggle between Make/Miss (individual shot outcomes) and Zones (FG% by court zones with opacity showing frequency). Red zones = low FG%, green = high FG%.",
                                                style={'color': 'white', 'fontSize': '13px', 'marginTop': '0', 'marginBottom': '12px', 'fontStyle': 'italic'}
                                            ),
                                            dcc.Graph(id='shot-chart-graph', style={'height': '500px'})
                                        ]
                                    ),

                                    # EFFICIENCY LANDSCAPE
                                    html.Div(
                                        style={
                                            'flex': '1',
                                            'backgroundColor': '#161d2b',
                                            'borderRadius': '15px',
                                            'padding': '20px',
                                            'border': '1px solid #2d384d'
                                        },
                                        children=[
                                            html.H4(id='efficiency-landscape-title', children="Efficiency Landscape", style={'color': '#00BFFF', 'marginBottom': '10px'}),
                                            html.Div(
                                                id='efficiency-hover-info',
                                                style={
                                                    'minHeight': '24px',
                                                    'marginBottom': '8px',
                                                    'color': 'rgba(255,255,255,0.85)',
                                                    'fontSize': '14px'
                                                },
                                                children=[
                                                    html.H5("Hover a point to see lineup details.", style={'color': 'white', 'marginBottom' : '5px'})
                                                ]
                                            ),
                                            dcc.Graph(id='efficiency-graph', style={'height': '500px'}, clear_on_unhover=True)
                                        ]
                                    )
                                ]
                            ),
                            # Bottom row: Radar (orange-brown) + Efficiency
                            # html.Div(
                            #     style={'display': 'flex', 'gap': '20px'},
                            #     children=[
                            #         # Tendency Radar
                            #         html.Div(
                            #             style={'flex': '1', 'backgroundColor': '#161d2b', 'borderRadius': '15px', 'padding': '20px', 'border': '1px solid #2d384d'},
                            #             children=[
                            #                 html.H5(id='radar-chart-title', children="Luka Dončić - Lineup Tendency Profile", style={'color': '#00BFFF'}),
                            #                 dcc.Graph(id='tendency-radar-graph', style={'height': '350px'})
                            #             ]
                            #         ),
                            #         # Matchup analysis placeholder
                            #         html.Div(
                            #             style={
                            #                 'flex': '1',
                            #                 'backgroundColor': '#161d2b',
                            #                 'borderRadius': '15px',
                            #                 'padding': '20px',
                            #                 'border': '1px solid #2d384d',
                            #                 'height': '350px'   # ✅ force match radar
                            #             },
                            #             children=[
                            #                 dcc.Graph(
                            #                     id='team-vs-opp-graph',
                            #                     style={'height': '450px'}
                            #                 )

                            #             ]
                            #         )
                            #     ]
                            # )
                            html.Div(
                                style={
                                    'display': 'flex',
                                    'gap': '20px',
                                    'alignItems': 'stretch'
                                },
                                children=[

                                    # Tendency Heatmap (was Radar)
                                    html.Div(
                                        style={
                                            'flex': '1',
                                            'backgroundColor': '#161d2b',
                                            'borderRadius': '15px',
                                            'padding': '20px',
                                            'border': '1px solid #2d384d',
                                            'minHeight': '520px'
                                        },
                                        children=[
                                            html.H5(id='radar-chart-title', style={'color': '#00BFFF', 'marginBottom': '5px'}),
                                            html.P(
                                                "Each metric is independently normalized across all player lineups (darker = below average, brighter = above average)",
                                                style={'color': 'white', 'fontSize': '13px', 'marginTop': '0', 'marginBottom': '15px', 'fontStyle': 'italic'}
                                            ),
                                            dcc.Graph(id='tendency-radar-graph', style={'height': '460px'})
                                        ]
                                    ),

                                    # Team vs Opp
                                    html.Div(
                                        style={
                                            'flex': '1',
                                            'backgroundColor': '#161d2b',
                                            'borderRadius': '15px',
                                            'padding': '20px',
                                            'border': '1px solid #2d384d',
                                            'minHeight': '520px'
                                        },
                                        children=[
                                            html.H5(id='team-vs-opp-title', style={'color': '#00BFFF', 'marginBottom': '5px'}),
                                            html.P(
                                                "Compares lineup performance against opponents. Circles show lineup values, triangles show opponent values. Larger gaps indicate stronger advantages or disadvantages.",
                                                style={'color': 'white', 'fontSize': '13px', 'marginTop': '0', 'marginBottom': '15px', 'fontStyle': 'italic'}
                                            ),
                                            dcc.Graph(id='team-vs-opp-graph', style={'height': '460px'})
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
