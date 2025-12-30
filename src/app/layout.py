"""
Main Dashboard Layout

Integrates all NBA lineup analysis components into a unified 3-column dashboard:
- Left: Player selector + Player profile + Opponent placeholder
- Center: Shot chart heatmap
- Right: Lineup dropdown + Efficiency + Tendency radar
"""

from dash import html, dcc
import pandas as pd
from pathlib import Path

# Import data loaders
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))
from src.data.load_players import load_player_data
from src.data.load_efficiency import load_efficiency_data
from src.data.load_tendencies import load_tendency_data, normalize_metrics, create_lineup_label

# Import components
from src.app.components.efficiency_landscape import create_efficiency_component
from src.app.components.opponent_placeholder import create_opponent_placeholder
from src.app.components.tendency_radar import create_tendency_radar_component


# Styling constants
DARK_BG = '#1E2833'
CARD_BG = '#2A3642'
ACCENT_COLOR = '#008080'
BORDER_COLOR = '#00BFFF'
FONT_FAMILY = 'Calibri, sans-serif'


def create_layout(app):
    """
    Create the main dashboard layout with all integrated components.

    Returns:
        Dash html.Div containing the complete dashboard
    """

    # Load all data
    try:
        df_players = load_player_data('data/raw/allstar_data.csv')
        df_efficiency = load_efficiency_data('data/processed/luka_efficiency_graph_data.csv')
        df_tendencies = load_tendency_data('data/processed/luka_team_tendencies_graph_data.csv')
        df_tendencies = normalize_metrics(df_tendencies)

        # Get player options for dropdown
        player_options = [{'label': name, 'value': name} for name in sorted(df_players['PLAYER'].unique())]
        default_player = 'Luka Dončić' if 'Luka Dončić' in df_players['PLAYER'].values else player_options[0]['value']

        # Create lineup options for DROPDOWN (not checklist)
        lineup_options = []
        for i in range(len(df_efficiency)):
            label = create_lineup_label(df_efficiency.iloc[i])
            lineup_options.append({
                'label': f"#{i+1}: {label}",
                'value': i
            })

    except Exception as e:
        print(f"Error loading data: {e}")
        return html.Div([
            html.H1("Error Loading Dashboard", style={'color': 'red', 'textAlign': 'center', 'fontFamily': FONT_FAMILY}),
            html.P(f"Error: {str(e)}", style={'color': 'white', 'textAlign': 'center', 'fontFamily': FONT_FAMILY})
        ], style={'backgroundColor': DARK_BG, 'padding': '40px', 'minHeight': '100vh'})

    # Create main layout
    return html.Div(
        style={
            'backgroundColor': DARK_BG,
            'minHeight': '100vh',
            'padding': '8px 12px',
            'fontFamily': FONT_FAMILY
        },
        children=[
            # Header
            html.H1(
                "NBA Lineup Analysis Dashboard",
                style={
                    'textAlign': 'center',
                    'color': ACCENT_COLOR,
                    'marginBottom': '5px',
                    'fontSize': '28px',
                    'fontWeight': 'bold',
                    'fontFamily': FONT_FAMILY
                }
            ),

            html.H3(
                "Strategic Insights for Star-Driven Lineups",
                style={
                    'textAlign': 'center',
                    'color': 'rgba(255, 255, 255, 0.7)',
                    'marginBottom': '10px',
                    'fontSize': '14px',
                    'fontWeight': 'normal',
                    'fontFamily': FONT_FAMILY
                }
            ),

            html.Hr(style={'borderColor': BORDER_COLOR, 'margin': '10px 0'}),

            # Main 3-column layout
            html.Div(
                style={
                    'display': 'flex',
                    'gap': '10px',
                    'alignItems': 'flex-start'
                },
                children=[
                    # LEFT COLUMN (flex: 1.5)
                    html.Div(
                        style={'flex': '1.5', 'minWidth': '280px'},
                        children=[
                            # Star Player Selector (moved here)
                            html.Div(
                                style={
                                    'backgroundColor': CARD_BG,
                                    'padding': '10px',
                                    'borderRadius': '8px',
                                    'marginBottom': '10px',
                                    'border': f'2px solid {BORDER_COLOR}'
                                },
                                children=[
                                    html.Label(
                                        "Select Star Player:",
                                        style={
                                            'color': 'white',
                                            'fontWeight': 'bold',
                                            'fontSize': '13px',
                                            'marginBottom': '6px',
                                            'display': 'block',
                                            'fontFamily': FONT_FAMILY
                                        }
                                    ),
                                    dcc.Dropdown(
                                        id='global-star-player-dropdown',
                                        options=player_options,
                                        value=default_player,
                                        clearable=False,
                                        style={'fontFamily': FONT_FAMILY, 'fontSize': '13px'}
                                    )
                                ]
                            ),

                            # Player Profile Card
                            html.Div(
                                style={'marginBottom': '10px'},
                                children=[
                                    html.H2(
                                        "Star Player Profile",
                                        style={
                                            'color': ACCENT_COLOR,
                                            'fontSize': '16px',
                                            'marginBottom': '8px',
                                            'fontWeight': 'bold',
                                            'fontFamily': FONT_FAMILY
                                        }
                                    ),
                                    html.Div(
                                        id='player-profile-container',
                                        children=[]  # Will be populated by callback
                                    )
                                ]
                            ),

                            # Opponent Placeholder
                            html.Div(
                                children=[
                                    html.H2(
                                        "Matchup Analysis",
                                        style={
                                            'color': ACCENT_COLOR,
                                            'fontSize': '16px',
                                            'marginBottom': '8px',
                                            'fontWeight': 'bold',
                                            'fontFamily': FONT_FAMILY
                                        }
                                    ),
                                    create_opponent_placeholder(
                                        component_id='opponent',
                                        height=200,
                                        card_color=CARD_BG,
                                        accent_color=ACCENT_COLOR,
                                        border_color=BORDER_COLOR
                                    )
                                ]
                            )
                        ]
                    ),

                    # CENTER COLUMN (flex: 3)
                    html.Div(
                        style={'flex': '3', 'minWidth': '550px'},
                        children=[
                            html.H2(
                                "Shot Chart",
                                style={
                                    'color': ACCENT_COLOR,
                                    'fontSize': '16px',
                                    'marginBottom': '8px',
                                    'fontWeight': 'bold',
                                    'textAlign': 'center',
                                    'fontFamily': FONT_FAMILY
                                }
                            ),

                            html.Div(
                                style={
                                    'backgroundColor': CARD_BG,
                                    'padding': '8px',
                                    'borderRadius': '8px',
                                    'border': f'2px solid {BORDER_COLOR}',
                                    'display': 'flex',
                                    'justifyContent': 'center',
                                    'width': '100%',
                                    'marginBottom': '10px'
                                },
                                children=[
                                    dcc.Graph(
                                        id='shot-chart-graph',
                                        config={
                                            'displayModeBar': True,
                                            'displaylogo': False,
                                            'toImageButtonOptions': {
                                                'format': 'png',
                                                'filename': 'shot_chart',
                                                'height': 1200,
                                                'width': 1000,
                                                'scale': 2
                                            }
                                        },
                                        style={'fontFamily': FONT_FAMILY, 'width': '100%'}
                                    )
                                ]
                            ),

                            # Efficiency Landscape
                            html.Div(
                                children=[
                                    html.H2(
                                       # "Efficiency Landscape",
                                        style={
                                            'color': ACCENT_COLOR,
                                            'fontSize': '16px',
                                            'marginBottom': '8px',
                                            'fontWeight': 'bold',
                                            'textAlign': 'center',
                                            'fontFamily': FONT_FAMILY
                                        }
                                    ),
                                    create_efficiency_component(
                                        df_efficiency=df_efficiency,
                                        component_id='efficiency',
                                        star_player=default_player,
                                        height=240,
                                        card_color=CARD_BG,
                                        accent_color=ACCENT_COLOR,
                                        border_color=BORDER_COLOR
                                    )
                                ]
                            )
                        ]
                    ),

                    # RIGHT COLUMN (flex: 2.5)
                    html.Div(
                        style={'flex': '2.5', 'minWidth': '340px'},
                        children=[
                            # Lineup Selector - COMPACT DROPDOWN
                            html.Div(
                                style={
                                    'backgroundColor': CARD_BG,
                                    'padding': '10px',
                                    'borderRadius': '8px',
                                    'marginBottom': '10px',
                                    'border': f'2px solid {BORDER_COLOR}'
                                },
                                children=[
                                    html.Label(
                                        "Select Lineups to Compare:",
                                        style={
                                            'color': 'white',
                                            'fontWeight': 'bold',
                                            'fontSize': '13px',
                                            'marginBottom': '6px',
                                            'display': 'block',
                                            'fontFamily': FONT_FAMILY
                                        }
                                    ),

                                    dcc.Dropdown(
                                        id='lineup-comparison-dropdown',
                                        options=lineup_options,
                                        value=[0, 5, 10],  # Default: 3 lineups
                                        multi=True,
                                        searchable=True,
                                        placeholder="Click to select lineups...",
                                        style={
                                            'fontFamily': FONT_FAMILY,
                                            'fontSize': '13px'
                                        },
                                        className='custom-dropdown'
                                    ),

                                    html.Div(
                                        id='lineup-selection-summary',
                                        style={
                                            'color': 'rgba(255, 255, 255, 0.7)',
                                            'fontSize': '11px',
                                            'marginTop': '6px',
                                            'marginBottom': '0',
                                            'fontFamily': FONT_FAMILY
                                        }
                                    )
                                ]
                            ),

                            # Tendency Radar
                            html.Div(
                                children=[
                                    html.H2(
                                       # "Lineup Tendency Profile",
                                        style={
                                            'color': ACCENT_COLOR,
                                            'fontSize': '16px',
                                            'marginBottom': '8px',
                                            'fontWeight': 'bold',
                                            'fontFamily': FONT_FAMILY
                                        }
                                    ),
                                    create_tendency_radar_component(
                                        df_tendencies=df_tendencies,
                                        default_lineups=[0, 5, 10],
                                        component_id='tendency-radar',
                                        star_player=default_player,
                                        external_checklist_id='lineup-comparison-dropdown',
                                        show_internal_checklist=False,
                                        card_color=CARD_BG,
                                        accent_color=BORDER_COLOR,
                                        header_color=ACCENT_COLOR
                                    )
                                ]
                            )
                        ]
                    )
                ]
            ),

            # Footer
            html.Hr(style={'borderColor': BORDER_COLOR, 'margin': '10px 0'}),

            html.P(
                "NBA Lineup Analysis Dashboard | Data from NBA Stats API | Built with Dash & Plotly",
                style={
                    'textAlign': 'center',
                    'color': 'rgba(255, 255, 255, 0.4)',
                    'fontSize': '11px',
                    'marginBottom': '5px',
                    'marginTop': '5px',
                    'fontFamily': FONT_FAMILY
                }
            )
        ]
    )
