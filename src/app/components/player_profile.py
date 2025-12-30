"""
Player Profile Component for Dashboard Integration

Provides a reusable player profile card with dropdown selector.
Shows player photo, stats (name, height, weight, position), and team logo.
"""

import sys
from pathlib import Path
import pandas as pd
import base64
from dash import dcc, html, Input, Output


# Helper functions for finding and encoding images

def find_player_image(player_name, images_dir='star_graph_data/player photos'):
    """Find player image file with flexible matching."""
    extensions = ['.png', '.jpg', '.jpeg', '.webp', '.avif']

    # Try exact match
    for ext in extensions:
        exact_path = Path(images_dir) / f"{player_name}{ext}"
        if exact_path.exists():
            return str(exact_path)

    # Try with trailing space
    for ext in extensions:
        space_path = Path(images_dir) / f"{player_name} {ext}"
        if space_path.exists():
            return str(space_path)

    # Try with leading space
    for ext in extensions:
        leading_space_path = Path(images_dir) / f" {player_name}{ext}"
        if leading_space_path.exists():
            return str(leading_space_path)

    # Special case for Nikola Jokić
    if player_name == "Nikola Jokić":
        special_path = Path(images_dir) / "nikola-jokic-2-1.jpg.webp"
        if special_path.exists():
            return str(special_path)

    # Fallback: search by last name
    last_name = player_name.split()[-1]
    for file_path in Path(images_dir).glob('*'):
        if last_name.lower() in file_path.name.lower():
            return str(file_path)

    return None


def find_team_logo(team_name, logos_dir='star_graph_data/logo'):
    """Find team logo file with flexible matching."""
    extensions = ['.png', '.jpg', '.jpeg', '.webp', '.svg']

    # Try standard format
    for ext in extensions:
        logo_path = Path(logos_dir) / f"{team_name} logo{ext}"
        if logo_path.exists():
            return str(logo_path)

    # Special cases for known mismatches
    special_cases = {
        'Los Angeles Lakers': 'Los_Angeles_Lakers_logo.svg.png',
        'Houston Rockets': 'Houston Rockets  logo.png',
        'Minnesota Timberwolves': 'Minnesota Timberwolves logo.svg'
    }

    if team_name in special_cases:
        special_path = Path(logos_dir) / special_cases[team_name]
        if special_path.exists():
            return str(special_path)

    # Fallback: search by team keyword
    team_keywords = team_name.split()[-1]
    for file_path in Path(logos_dir).glob('*'):
        if team_keywords.lower() in file_path.name.lower():
            return str(file_path)

    return None


def encode_image_to_base64(image_path):
    """Convert image file to base64 for embedding in HTML."""
    if not image_path or not Path(image_path).exists():
        return None

    with open(image_path, 'rb') as f:
        encoded = base64.b64encode(f.read()).decode()

    ext = Path(image_path).suffix.lower()
    mime_types = {
        '.png': 'image/png',
        '.jpg': 'image/jpeg',
        '.jpeg': 'image/jpeg',
        '.webp': 'image/webp',
        '.avif': 'image/avif',
        '.svg': 'image/svg+xml'
    }
    mime_type = mime_types.get(ext, 'image/png')

    return f"data:{mime_type};base64,{encoded}"


# Component creation function

def create_player_profile_component(
    df_players: pd.DataFrame,
    component_id: str = 'player-profile',
    default_player: str = None,
    card_color: str = '#2A3642',
    accent_color: str = '#008080',
    border_color: str = '#00BFFF'
) -> html.Div:
    """
    Create player profile component with dropdown selector and card.

    Args:
        df_players: DataFrame with player data
        component_id: Unique ID prefix for component elements
        default_player: Default player to show (uses first if None)
        card_color: Background color for card
        accent_color: Accent color for text highlights
        border_color: Border color

    Returns:
        Dash html.Div containing dropdown and profile card
    """
    if default_player is None:
        default_player = df_players.iloc[0]['PLAYER']

    # Create player dropdown options
    player_options = [
        {'label': row['PLAYER'], 'value': row['PLAYER']}
        for _, row in df_players.iterrows()
    ]

    return html.Div(
        style={'display': 'flex', 'flexDirection': 'column', 'gap': '15px'},
        children=[
            # Player Dropdown Selector
            html.Div(
                style={
                    'backgroundColor': card_color,
                    'padding': '12px',
                    'borderRadius': '8px',
                    'border': f'1px solid {border_color}'
                },
                children=[
                    html.Label(
                        "Select Star Player:",
                        style={
                            'color': 'white',
                            'fontWeight': 'bold',
                            'marginBottom': '8px',
                            'display': 'block',
                            'fontSize': '14px'
                        }
                    ),
                    dcc.Dropdown(
                        id=f'{component_id}-player-dropdown',
                        options=player_options,
                        value=default_player,
                        clearable=False,
                        style={'fontFamily': 'Calibri, sans-serif'}
                    )
                ]
            ),

            # Player Profile Card (will be populated by callback)
            html.Div(
                id=f'{component_id}-card-container',
                children=[
                    # Initial card with default player
                    create_player_card_dash(
                        df_players[df_players['PLAYER'] == default_player].iloc[0],
                        card_color=card_color,
                        accent_color=accent_color,
                        border_color=border_color
                    )
                ]
            )
        ]
    )


def create_player_card_dash(player_data, card_color='#2A3642', accent_color='#008080', border_color='#00BFFF'):
    """
    Create player profile card using native Dash components.

    Args:
        player_data: Dictionary or Series with player information
        card_color: Background color
        accent_color: Accent color for highlights
        border_color: Border color

    Returns:
        Dash html.Div component with 3-column layout
    """
    # Extract player info
    name = player_data['PLAYER']
    height = player_data['Height']
    weight = player_data['Weight']
    position = player_data['Position']
    team = player_data['CURRENT_TEAM']

    # Find and encode images
    player_img_path = find_player_image(name)
    player_img_base64 = encode_image_to_base64(player_img_path)

    team_logo_path = find_team_logo(team)
    team_logo_base64 = encode_image_to_base64(team_logo_path)

    # Create the 3-column card
    return html.Div(
        style={
            'display': 'flex',
            'backgroundColor': card_color,
            'border': f'2px solid {border_color}',
            'borderRadius': '10px',
            'overflow': 'hidden',
            'boxShadow': '0 4px 8px rgba(0, 191, 255, 0.3)',
            'fontFamily': 'Calibri, sans-serif',
            'color': 'white',
            'minHeight': '350px'
        },
        children=[
            # Left Panel: Player Photo
            html.Div(
                style={
                    'flex': '1',
                    'display': 'flex',
                    'alignItems': 'center',
                    'justifyContent': 'center',
                    'background': 'linear-gradient(135deg, rgba(0, 128, 128, 0.1), rgba(0, 191, 255, 0.1))',
                    'padding': '20px'
                },
                children=[
                    html.Img(
                        src=player_img_base64,
                        style={
                            'maxWidth': '100%',
                            'maxHeight': '400px',
                            'objectFit': 'contain',
                            'borderRadius': '5px'
                        }
                    ) if player_img_base64 else html.Div(
                        "No Photo Available",
                        style={'color': 'gray', 'fontSize': '18px'}
                    )
                ]
            ),

            # Middle Panel: Player Stats
            html.Div(
                style={
                    'flex': '1',
                    'padding': '30px',
                    'display': 'flex',
                    'flexDirection': 'column',
                    'justifyContent': 'center'
                },
                children=[
                    html.H2(
                        name,
                        style={
                            'margin': '0 0 25px 0',
                            'color': accent_color,
                            'fontSize': '28px',
                            'fontWeight': 'bold',
                            'borderBottom': f'2px solid {accent_color}',
                            'paddingBottom': '10px'
                        }
                    ),

                    html.Div(
                        style={'fontSize': '16px', 'lineHeight': '2.2'},
                        children=[
                            html.Div([
                                html.Span('Height:', style={'color': accent_color, 'fontWeight': 'bold'}),
                                html.Span(f' {height}', style={'marginLeft': '10px'})
                            ], style={'marginBottom': '10px'}),

                            html.Div([
                                html.Span('Weight:', style={'color': accent_color, 'fontWeight': 'bold'}),
                                html.Span(f' {weight} lbs', style={'marginLeft': '10px'})
                            ], style={'marginBottom': '10px'}),

                            html.Div([
                                html.Span('Position:', style={'color': accent_color, 'fontWeight': 'bold'}),
                                html.Span(f' {position}', style={'marginLeft': '10px'})
                            ], style={'marginBottom': '10px'})
                        ]
                    )
                ]
            ),

            # Right Panel: Team Logo Only
            html.Div(
                style={
                    'flex': '0.8',
                    'display': 'flex',
                    'alignItems': 'center',
                    'justifyContent': 'center',
                    'background': 'rgba(0, 128, 128, 0.05)',
                    'padding': '20px'
                },
                children=[
                    html.Img(
                        src=team_logo_base64,
                        style={
                            'maxWidth': '150px',
                            'maxHeight': '150px',
                            'objectFit': 'contain'
                        }
                    ) if team_logo_base64 else html.Div(
                        "No Logo",
                        style={'color': 'gray', 'fontSize': '14px'}
                    )
                ]
            )
        ]
    )


# Callback registration function

def register_player_profile_callbacks(app, df_players, component_id='player-profile'):
    """
    Register callbacks for player profile component.

    Args:
        app: Dash app instance
        df_players: DataFrame with player data
        component_id: Component ID prefix (must match component creation)
    """

    @app.callback(
        Output(f'{component_id}-card-container', 'children'),
        Input(f'{component_id}-player-dropdown', 'value')
    )
    def update_player_card(selected_player):
        """Update player card when dropdown selection changes."""
        if not selected_player:
            selected_player = df_players.iloc[0]['PLAYER']

        # Get player data
        player_row = df_players[df_players['PLAYER'] == selected_player]

        if player_row.empty:
            return html.Div("Player not found", style={'color': 'red', 'padding': '20px'})

        # Create and return updated card
        return create_player_card_dash(player_row.iloc[0])


# Example usage documentation
INTEGRATION_EXAMPLE = """
# How to integrate into your main dashboard:

## Step 1: Import in your layout file (src/app/__init__.py)

from src.data.load_players import load_player_data
from src.app.components.player_profile import (
    create_player_profile_component,
    register_player_profile_callbacks
)

# Load data
df_players = load_player_data('star_graph_data/allstar_data.csv')

## Step 2: Add to your layout

layout = html.Div([
    # ... your existing components ...

    create_player_profile_component(
        df_players=df_players,
        component_id='star-profile',
        default_player=df_players.iloc[0]['PLAYER']
    ),

    # ... more components ...
])

## Step 3: Register callbacks

register_player_profile_callbacks(
    app,
    df_players=df_players,
    component_id='star-profile'
)

## Done!
The player profile component is now integrated with dropdown selection.
"""

if __name__ == '__main__':
    print("="*60)
    print("Player Profile Component - Integration Guide")
    print("="*60)
    print(INTEGRATION_EXAMPLE)
