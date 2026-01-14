"""
Archetype Profile Component.
Displays archetype information including strengths, weaknesses, and notable players.
"""

from dash import html


def create_archetype_card_dash(archetype_data=None):
    """
    Creates an archetype profile card component.
    
    Args:
        archetype_data: Dictionary or DataFrame row with archetype information
                       Expected keys: 'archetype_name', 'strengths', 'weaknesses', 
                       'similar_players', 'description'
    
    Returns:
        Dash HTML component with archetype profile card
    """
    if archetype_data is None:
        return html.Div(
            style={
                'textAlign': 'center',
                'padding': '20px',
                'color': '#8e9aaf',
                'fontStyle': 'italic'
            },
            children="Select an archetype to view details"
        )
    
    # Extract data (with defaults for template)
    archetype_name = archetype_data.get('archetype_name', 'Unknown Archetype') if isinstance(archetype_data, dict) else getattr(archetype_data, 'archetype_name', 'Unknown Archetype')
    description = archetype_data.get('description', 'No description available') if isinstance(archetype_data, dict) else getattr(archetype_data, 'description', 'No description available')
    strengths = archetype_data.get('strengths', []) if isinstance(archetype_data, dict) else getattr(archetype_data, 'strengths', [])
    weaknesses = archetype_data.get('weaknesses', []) if isinstance(archetype_data, dict) else getattr(archetype_data, 'weaknesses', [])
    similar_players = archetype_data.get('similar_players', []) if isinstance(archetype_data, dict) else getattr(archetype_data, 'similar_players', [])
    
    # Ensure lists
    if isinstance(strengths, str):
        strengths = [s.strip() for s in strengths.split(',') if s.strip()]
    if isinstance(weaknesses, str):
        weaknesses = [w.strip() for w in weaknesses.split(',') if w.strip()]
    if isinstance(similar_players, str):
        similar_players = [p.strip() for p in similar_players.split(',') if p.strip()]
    
    return html.Div(
        style={
            'backgroundColor': '#1a2332',
            'borderRadius': '12px',
            'padding': '20px',
            'border': '1px solid #2d384d',
            'marginTop': '15px'
        },
        children=[
            # Archetype Name
            html.H5(
                archetype_name,
                style={
                    'color': '#00BFFF',
                    'marginTop': '0',
                    'marginBottom': '10px',
                    'fontSize': '18px',
                    'textAlign': 'center',
                    'borderBottom': '1px solid rgba(0, 191, 255, 0.3)',
                    'paddingBottom': '10px'
                }
            ),
            
            # Description
            html.P(
                description,
                style={
                    'color': '#b8c5d6',
                    'fontSize': '16px',
                    'marginBottom': '15px',
                    'fontStyle': 'italic',
                    'textAlign': 'center'
                }
            ),
            
            # Strengths Section
            html.Div([
                html.H6(
                    "✓ Strengths",
                    style={'color': '#4ade80', 'fontSize': '15px', 'marginBottom': '8px', 'fontWeight': 'bold'}
                ),
                html.Ul(
                    [html.Li(strength, style={'color': '#e5e7eb', 'fontSize': '13px', 'marginBottom': '4px'}) 
                     for strength in (strengths if strengths else ['No strengths data available'])],
                    style={'marginTop': '0', 'marginBottom': '15px', 'paddingLeft': '20px'}
                )
            ]),
            
            # Weaknesses Section
            html.Div([
                html.H6(
                    "✕ Limitations",
                    style={'color': '#f87171', 'fontSize': '15px', 'marginBottom': '8px', 'fontWeight': 'bold'}
                ),
                html.Ul(
                    [html.Li(weakness, style={'color': '#e5e7eb', 'fontSize': '13px', 'marginBottom': '4px'}) 
                     for weakness in (weaknesses if weaknesses else ['No limitations data available'])],
                    style={'marginTop': '0', 'marginBottom': '15px', 'paddingLeft': '20px'}
                )
            ]),
            
            # Similar Players Section
            html.Div([
                html.H6(
                    "👥 Key Players",
                    style={'color': '#fbbf24', 'fontSize': '15px', 'marginBottom': '8px', 'fontWeight': 'bold'}
                ),
                html.Div(
                    [html.Span(
                        player,
                        style={
                            'display': 'inline-block',
                            'backgroundColor': 'rgba(0, 191, 255, 0.1)',
                            'color': '#FFFFFF',
                            'padding': '4px 10px',
                            'borderRadius': '12px',
                            'fontSize': '15px',
                            'margin': '2px 4px 2px 0',
                            'border': '1px solid rgba(0, 191, 255, 0.3)'
                        }
                    ) for player in (similar_players if similar_players else ['No player data available'])],
                    style={'marginTop': '0'}
                )
            ])
        ]
    )
