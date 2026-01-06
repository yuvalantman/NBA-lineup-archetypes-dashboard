"""
Player Profile Component for NBA Dashboard
Creates a 3-column layout with gradient background and special image handling.
"""

import base64
from pathlib import Path
from dash import dcc, html


# --- Image Encoding Utilities ---

def encode_image_to_base64(image_path):
    """
    Encodes a local image file to Base64 for embedding in HTML.
    Returns None if the file doesn't exist.
    """
    if not image_path or not Path(image_path).exists():
        return None

    try:
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
        mime = mime_types.get(ext, 'image/png')

        return f"data:{mime};base64,{encoded}"
    except Exception:
        return None


def find_player_image(player_name):
    """
    Searches for player photo with flexible naming and special cases.

    Handles:
        - Multiple extensions (.png, .jpg, .jpeg, .webp, .avif)
        - Leading/trailing spaces in filenames
        - Special case for "Nikola Jokić" -> "nikola-jokic-2-1.jpg.webp"
    """
    base_dir = Path('assets/images/player_photos')

    if not base_dir.exists():
        return None

    # Special case: Handle Nikola Jokić filename
    if player_name == "Nikola Jokić":
        jokic_path = base_dir / "nikola-jokic-2-1.jpg.webp"
        if jokic_path.exists():
            return str(jokic_path)

    extensions = ['.png', '.jpg', '.jpeg', '.webp', '.avif']

    # Try exact match first
    for ext in extensions:
        path = base_dir / f"{player_name}{ext}"
        if path.exists():
            return str(path)

    # Try with stripped spaces
    for ext in extensions:
        path = base_dir / f"{player_name.strip()}{ext}"
        if path.exists():
            return str(path)

    # Try case-insensitive search
    try:
        for file in base_dir.iterdir():
            if file.stem.lower() == player_name.lower():
                return str(file)
    except Exception:
        pass

    return None


def find_team_logo(team_name):
    """
    Searches for team logo with special cases for specific teams.

    Special cases:
        - Lakers: "Los_Angeles_Lakers_logo.svg.png"
        - Timberwolves: "Minnesota Timberwolves logo.svg"
    """
    base_dir = Path('assets/logos/logo')

    if not base_dir.exists():
        return None

    # Special cases mapping for teams with unusual filenames
    special_cases = {
        'Lakers': 'Los_Angeles_Lakers_logo.svg.png',
        'Timberwolves': 'Minnesota Timberwolves logo.svg',
        'Warriors': 'Golden State Warriors logo.png',
        'Bucks': 'Milwaukee Bucks logo.jpeg',
        'Nuggets': 'Denver Nuggets logo.webp',
        'Thunder': 'Oklahoma City Thunder logo.png'
    }

    # Check if team has a special case
    if team_name in special_cases:
        path = base_dir / special_cases[team_name]
        if path.exists():
            return str(path)

    # Standard naming: "{team_name} logo.{ext}"
    extensions = ['.png', '.jpg', '.jpeg', '.svg', '.webp']

    for ext in extensions:
        path = base_dir / f"{team_name} logo{ext}"
        if path.exists():
            return str(path)

    # Fallback: Try without "logo" suffix
    for ext in extensions:
        path = base_dir / f"{team_name}{ext}"
        if path.exists():
            return str(path)

    return None


# --- Player Profile Component ---

def create_player_profile_component(df_players, component_id='star-profile', default_player=None):
    """
    Creates the player selection dropdown and placeholder for the player card.

    Args:
        df_players: DataFrame with player data (must have 'star_player' or 'PLAYER' column)
        component_id: Base ID for the component elements
        default_player: Optional default player to select

    Returns:
        Dash HTML component with dropdown and card container
    """
    # Determine which column to use for player names
    player_col = 'star_player' if 'star_player' in df_players.columns else 'PLAYER'

    if default_player is None and not df_players.empty:
        default_player = df_players.iloc[0][player_col]

    # Get unique player names for dropdown
    unique_players = sorted(df_players[player_col].unique())
    player_options = [{'label': player, 'value': player} for player in unique_players]

    return html.Div(
        style={'display': 'flex', 'flexDirection': 'column', 'gap': '15px'},
        children=[
            # Player Selection Dropdown
            html.Div(
                style={
                    'backgroundColor': '#2A3642',
                    'padding': '15px',
                    'borderRadius': '10px',
                    'border': '1px solid #00BFFF',
                    'boxShadow': '0 4px 6px rgba(0, 0, 0, 0.3)'
                },
                children=[
                    html.Label(
                        "Select Star Player",
                        style={
                            'color': '#00BFFF',
                            'fontWeight': 'bold',
                            'marginBottom': '10px',
                            'display': 'block',
                            'fontSize': '14px',
                            'textTransform': 'uppercase',
                            'letterSpacing': '1px'
                        }
                    ),
                    dcc.Dropdown(
                        id=f'{component_id}-player-dropdown',
                        options=player_options,
                        value=default_player,
                        clearable=False,
                        style={
                            'color': '#111',
                            'borderRadius': '5px'
                        }
                    )
                ]
            ),

            # Player Card Container (populated by callback)
            html.Div(id=f'{component_id}-card-container')
        ]
    )


def create_player_card_dash(player_data):
    """
    Creates the 3-column player profile card with gradient background.

    Layout:
        Left: Player Photo
        Center: Name, Height, Weight, Position
        Right: Team Logo

    Args:
        player_data: Series or dict with player information

    Returns:
        Dash HTML component with the player card
    """
    # Extract player information (support both column naming conventions)
    name = player_data.get('star_player', player_data.get('PLAYER', 'Unknown'))
    team = player_data.get('CURRENT_TEAM', 'NBA')
    position = player_data.get('Position', 'N/A')
    height = player_data.get('Height', 'N/A')
    weight = player_data.get('Weight', 'N/A')

    # Load images using the specialized functions
    player_img_path = find_player_image(name)
    team_logo_path = find_team_logo(team)

    player_img_encoded = encode_image_to_base64(player_img_path)
    team_logo_encoded = encode_image_to_base64(team_logo_path)

    return html.Div(
        style={
            'display': 'flex',
            'background': 'linear-gradient(135deg, #1e2130 0%, #2a3142 50%, #1e2130 100%)',
            'borderRadius': '15px',
            'border': '2px solid #00BFFF',
            'padding': '25px',
            'color': 'white',
            'alignItems': 'center',
            'minHeight': '220px',
            'boxShadow': '0 8px 16px rgba(0, 191, 255, 0.2)',
            'position': 'relative',
            'overflow': 'hidden'
        },
        children=[
            # Decorative background element
            html.Div(style={
                'position': 'absolute',
                'top': '-50%',
                'right': '-10%',
                'width': '300px',
                'height': '300px',
                'background': 'radial-gradient(circle, rgba(0,191,255,0.1) 0%, transparent 70%)',
                'borderRadius': '50%'
            }),

            # LEFT: Player Photo
            html.Div(
                style={
                    'flex': '1',
                    'textAlign': 'center',
                    'display': 'flex',
                    'flexDirection': 'column',
                    'alignItems': 'center',
                    'justifyContent': 'center',
                    'zIndex': '1'
                },
                children=[
                    html.Img(
                        src=player_img_encoded if player_img_encoded else '',
                        style={
                            'width': '150px',
                            'height': '150px',
                            'borderRadius': '50%',
                            'objectFit': 'cover',
                            'border': '3px solid #00BFFF',
                            'backgroundColor': '#2A3642',
                            'boxShadow': '0 4px 8px rgba(0, 0, 0, 0.4)'
                        }
                    ) if player_img_encoded else html.Div(
                        "No Photo",
                        style={
                            'width': '150px',
                            'height': '150px',
                            'borderRadius': '50%',
                            'backgroundColor': '#2A3642',
                            'border': '3px solid #00BFFF',
                            'display': 'flex',
                            'alignItems': 'center',
                            'justifyContent': 'center',
                            'color': '#666',
                            'fontSize': '12px'
                        }
                    )
                ]
            ),

            # CENTER: Bio Information
            html.Div(
                style={
                    'flex': '1.5',
                    'paddingLeft': '30px',
                    'paddingRight': '20px',
                    'zIndex': '1'
                },
                children=[
                    html.H2(
                        name,
                        style={
                            'color': '#00BFFF',
                            'marginBottom': '15px',
                            'fontSize': '26px',
                            'fontWeight': 'bold',
                            'textShadow': '0 2px 4px rgba(0, 0, 0, 0.5)'
                        }
                    ),
                    html.Div(
                        style={'display': 'flex', 'flexDirection': 'column', 'gap': '8px'},
                        children=[
                            html.P([
                                html.Span("Position: ", style={'color': '#888', 'fontWeight': 'normal'}),
                                html.Span(position, style={'color': 'white', 'fontWeight': 'bold'})
                            ], style={'margin': '0', 'fontSize': '15px'}),
                            html.P([
                                html.Span("Height: ", style={'color': '#888', 'fontWeight': 'normal'}),
                                html.Span(height, style={'color': 'white', 'fontWeight': 'bold'})
                            ], style={'margin': '0', 'fontSize': '15px'}),
                            html.P([
                                html.Span("Weight: ", style={'color': '#888', 'fontWeight': 'normal'}),
                                html.Span(f"{weight} lbs", style={'color': 'white', 'fontWeight': 'bold'})
                            ], style={'margin': '0', 'fontSize': '15px'}),
                            html.P([
                                html.Span("Team: ", style={'color': '#888', 'fontWeight': 'normal'}),
                                html.Span(team, style={'color': '#00BFFF', 'fontWeight': 'bold'})
                            ], style={'margin': '0', 'fontSize': '15px'})
                        ]
                    )
                ]
            ),

            # RIGHT: Team Logo
            html.Div(
                style={
                    'flex': '0.8',
                    'textAlign': 'center',
                    'display': 'flex',
                    'alignItems': 'center',
                    'justifyContent': 'center',
                    'zIndex': '1'
                },
                children=[
                    html.Img(
                        src=team_logo_encoded if team_logo_encoded else '',
                        style={
                            'width': '100px',
                            'height': '100px',
                            'objectFit': 'contain',
                            'filter': 'drop-shadow(0 4px 8px rgba(0, 0, 0, 0.4))'
                        }
                    ) if team_logo_encoded else html.Div(
                        style={'height': '100px'}
                    )
                ]
            )
        ]
    )
