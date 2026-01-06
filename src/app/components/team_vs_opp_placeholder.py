"""
Team vs Opponent Placeholder Component
Displays a "Coming Soon" card for future comparative analysis feature.
"""

from dash import html


def create_team_vs_opp_placeholder():
    """
    Creates a styled placeholder card for the Team vs Opponent comparison feature.

    Returns:
        Dash HTML component with "Coming Soon" message
    """
    return html.Div(
        style={
            'backgroundColor': '#1e2130',
            'borderRadius': '15px',
            'border': '2px solid #2d384d',
            'padding': '30px',
            'textAlign': 'center',
            'minHeight': '200px',
            'display': 'flex',
            'flexDirection': 'column',
            'alignItems': 'center',
            'justifyContent': 'center',
            'boxShadow': '0 4px 8px rgba(0, 0, 0, 0.3)',
            'position': 'relative',
            'overflow': 'hidden'
        },
        children=[
            # Background decoration
            html.Div(style={
                'position': 'absolute',
                'top': '50%',
                'left': '50%',
                'transform': 'translate(-50%, -50%)',
                'width': '200px',
                'height': '200px',
                'background': 'radial-gradient(circle, rgba(0,191,255,0.05) 0%, transparent 70%)',
                'borderRadius': '50%'
            }),

            # Icon/Graphic
            html.Div(
                "🏀 vs 🏀",
                style={
                    'fontSize': '48px',
                    'marginBottom': '15px',
                    'opacity': '0.6',
                    'zIndex': '1'
                }
            ),

            # Title
            html.H4(
                "Matchup Analysis",
                style={
                    'color': '#00BFFF',
                    'marginBottom': '10px',
                    'fontWeight': 'bold',
                    'fontSize': '20px',
                    'zIndex': '1'
                }
            ),

            # Coming Soon Message
            html.P(
                "Coming Soon",
                style={
                    'color': '#888',
                    'fontSize': '16px',
                    'marginBottom': '5px',
                    'fontStyle': 'italic',
                    'zIndex': '1'
                }
            ),

            # Additional info
            html.P(
                "Comparative lineup performance analysis",
                style={
                    'color': '#666',
                    'fontSize': '13px',
                    'margin': '0',
                    'zIndex': '1'
                }
            )
        ]
    )
