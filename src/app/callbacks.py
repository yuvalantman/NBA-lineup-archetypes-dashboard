"""
Dashboard Callbacks

Registers all callbacks for the integrated NBA lineup analysis dashboard:
1. Star player filter → Player profile card + Shot chart
2. Lineup dropdown → Efficiency landscape + Tendency radar
"""

from dash import Input, Output, html
import pandas as pd
from pathlib import Path
import base64

# Import data loaders
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))
from data.load_players import load_player_data
from data.load_efficiency import load_efficiency_data
from data.load_tendencies import load_tendency_data, normalize_metrics

# Import component callback registration
from .components.efficiency_landscape import register_efficiency_callbacks
from .components.tendency_radar import register_tendency_radar_callbacks


# Styling constants (match layout.py)
CARD_BG = '#2A3642'
ACCENT_COLOR = '#008080'
BORDER_COLOR = '#00BFFF'
FONT_FAMILY = 'Calibri, sans-serif'


# Helper functions for finding and encoding images
def find_player_image(player_name, images_dir='assets/images/player_photos'):
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


def find_team_logo(team_name, logos_dir='assets/logos'):
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

    mime = mime_types.get(ext, 'image/png')
    return f"data:{mime};base64,{encoded}"


def create_player_card_dash(player_data, card_color='#2A3642', accent_color='#008080', border_color='#00BFFF'):
    """Create player profile card using native Dash components."""
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
            'alignItems': 'center',
            'justifyContent': 'space-between',
            'backgroundColor': card_color,
            'padding': '12px',
            'borderRadius': '8px',
            'border': f'2px solid {border_color}',
            'gap': '12px',
            'fontFamily': FONT_FAMILY
        },
        children=[
            # Left: Player Photo
            html.Div(
                style={'flex': '1', 'display': 'flex', 'justifyContent': 'center'},
                children=[
                    html.Img(
                        src=player_img_base64 if player_img_base64 else '',
                        style={
                            'width': '100px',
                            'height': '100px',
                            'borderRadius': '50%',
                            'objectFit': 'cover',
                            'border': f'3px solid {accent_color}',
                            'display': 'block' if player_img_base64 else 'none'
                        }
                    ) if player_img_base64 else html.Div(
                        "📷",
                        style={
                            'fontSize': '60px',
                            'opacity': '0.3',
                            'textAlign': 'center'
                        }
                    )
                ]
            ),

            # Middle: Player Stats
            html.Div(
                style={'flex': '2', 'color': 'white'},
                children=[
                    html.H2(
                        name,
                        style={
                            'margin': '0 0 10px 0',
                            'fontSize': '20px',
                            'color': accent_color,
                            'fontWeight': 'bold',
                            'fontFamily': FONT_FAMILY
                        }
                    ),
                    html.Div(
                        [
                            html.Div(f"Height: {height}", style={'fontSize': '14px', 'marginBottom': '5px', 'fontFamily': FONT_FAMILY}),
                            html.Div(f"Weight: {weight}", style={'fontSize': '14px', 'marginBottom': '5px', 'fontFamily': FONT_FAMILY}),
                            html.Div(f"Position: {position}", style={'fontSize': '14px', 'fontFamily': FONT_FAMILY})
                        ]
                    )
                ]
            ),

            # Right: Team Logo
            html.Div(
                style={'flex': '1', 'display': 'flex', 'justifyContent': 'center'},
                children=[
                    html.Img(
                        src=team_logo_base64 if team_logo_base64 else '',
                        style={
                            'maxWidth': '80px',
                            'maxHeight': '80px',
                            'objectFit': 'contain',
                            'display': 'block' if team_logo_base64 else 'none'
                        }
                    ) if team_logo_base64 else html.Div(
                        "🏀",
                        style={
                            'fontSize': '50px',
                            'opacity': '0.3',
                            'textAlign': 'center'
                        }
                    )
                ]
            )
        ]
    )


def register_callbacks(app):
    """
    Register all dashboard callbacks.

    Args:
        app: Dash app instance
    """

    # Load data (needed for callbacks)
    df_players = load_player_data('data/raw/allstar_data.csv')
    df_efficiency = load_efficiency_data('data/processed/luka_efficiency_graph_data.csv')
    df_tendencies = load_tendency_data('data/processed/luka_team_tendencies_graph_data.csv')
    df_tendencies = normalize_metrics(df_tendencies)

    # Load shot data
    df_shots = pd.read_csv('data/raw/allstar_shots_with_lineups.csv')

    # ========================================
    # CALLBACK 1: Star Player → Player Profile Card
    # ========================================
    @app.callback(
        Output('player-profile-container', 'children'),
        Input('global-star-player-dropdown', 'value')
    )
    def update_player_profile(selected_player):
        """Update player profile card when star player changes."""
        if not selected_player:
            return []

        # Get player data
        player_row = df_players[df_players['PLAYER'] == selected_player]

        if player_row.empty:
            return html.Div(
                f"Player '{selected_player}' not found",
                style={'color': 'red', 'padding': '20px', 'fontFamily': FONT_FAMILY}
            )

        player_data = player_row.iloc[0]

        # Create player card
        return create_player_card_dash(
            player_data=player_data,
            card_color=CARD_BG,
            accent_color=ACCENT_COLOR,
            border_color=BORDER_COLOR
        )

    # ========================================
    # CALLBACK 2: Star Player → Shot Chart
    # ========================================
    @app.callback(
        Output('shot-chart-graph', 'figure'),
        Input('global-star-player-dropdown', 'value')
    )
    def update_shot_chart(selected_player):
        """Update shot chart when star player changes."""
        if not selected_player:
            # Return empty figure
            import plotly.graph_objects as go
            fig = go.Figure()
            fig.add_annotation(
                text="Select a star player to view shot chart",
                xref="paper", yref="paper",
                x=0.5, y=0.5, showarrow=False,
                font=dict(size=16, color='white', family=FONT_FAMILY)
            )
            fig.update_layout(
                height=580, width=800,
                plot_bgcolor='#1a2332',  # Dark blue background
                paper_bgcolor='#1a2332',  # Dark blue background
                font=dict(color='white', family=FONT_FAMILY)
            )
            return fig

        # Filter shots for selected player
        player_shots = df_shots[df_shots['PLAYER_NAME'] == selected_player]

        if player_shots.empty:
            # No data - return empty figure
            import plotly.graph_objects as go
            fig = go.Figure()
            fig.add_annotation(
                text=f"No shot data available for {selected_player}",
                xref="paper", yref="paper",
                x=0.5, y=0.5, showarrow=False,
                font=dict(size=16, color='white', family=FONT_FAMILY)
            )
            fig.update_layout(
                height=580, width=800,
                plot_bgcolor='#1a2332',  # Dark blue background
                paper_bgcolor='#1a2332',  # Dark blue background
                font=dict(color='white', family=FONT_FAMILY)
            )
            return fig

        # Create shot chart with POINT-BASED HEATMAP
        import plotly.graph_objects as go
        from src.app.components.court_visualization import draw_nba_court

        # Calculate FG% for coloring
        player_shots['FG_PCT'] = player_shots['SHOT_MADE_FLAG']

        # Create color based on shot result
        colors = player_shots['SHOT_MADE_FLAG'].apply(
            lambda x: '#4CAF50' if x == 1 else '#F44336'  # Green for made, red for missed
        )

        # Create figure
        fig = go.Figure()

        # Draw court first with dark blue background
        fig = draw_nba_court(
            fig=fig,
            line_color='white',
            line_width=2,
            court_background='rgba(0,0,0,0)'
        )

        # Add shot points
        fig.add_trace(go.Scatter(
            x=player_shots['LOC_X'],
            y=player_shots['LOC_Y'],
            mode='markers',
            marker=dict(
                size=8,
                color=colors,
                opacity=0.6,
                line=dict(width=0.5, color='white')
            ),
            text=[
                f"<b>{selected_player}</b><br>" +
                f"Distance: {int(row['SHOT_DISTANCE'])}ft<br>" +
                f"Zone: {row['SHOT_ZONE_BASIC']}<br>" +
                f"Result: {'Made' if row['SHOT_MADE_FLAG'] == 1 else 'Missed'}"
                for _, row in player_shots.iterrows()
            ],
            hovertemplate='%{text}<extra></extra>',
            showlegend=False
        ))

        # Update layout with DARK BLUE background
        fig.update_layout(
            title=dict(
                text=f"<b>{selected_player} - Shot Chart</b>",
                font=dict(size=14, color='white', family=FONT_FAMILY),
                x=0.5,
                xanchor='center'
            ),
            height=340,
            plot_bgcolor='#1a2332',  # Dark blue background
            paper_bgcolor='#1a2332',  # Dark blue background
            font=dict(family=FONT_FAMILY, color='white'),
            xaxis=dict(
                range=[-260, 260],
                showgrid=False,
                zeroline=False,
                showticklabels=False,
                scaleanchor='y',
                scaleratio=1,
                fixedrange=False
            ),
            yaxis=dict(
                range=[-57.5, 432.5],
                showgrid=False,
                zeroline=False,
                showticklabels=False,
                fixedrange=False
            ),
            margin=dict(l=10, r=10, t=30, b=10),
            hoverlabel=dict(
                bgcolor='rgba(0,0,0,0.8)',
                font_size=13,
                font_family=FONT_FAMILY,
                font_color='white'
            )
        )

        return fig

    # ========================================
    # CALLBACK 3: Lineup Dropdown → Efficiency Landscape
    # ========================================
    register_efficiency_callbacks(
        app=app,
        df_efficiency=df_efficiency,
        lineup_checklist_id='lineup-comparison-dropdown',  # Dropdown ID
        component_id='efficiency'
    )

    # ========================================
    # CALLBACK 4: Lineup Dropdown → Selection Summary
    # ========================================
    @app.callback(
        Output('lineup-selection-summary', 'children'),
        Input('lineup-comparison-dropdown', 'value')
    )
    def update_lineup_summary(selected_lineups):
        """Update text showing which lineups are selected."""
        if not selected_lineups or len(selected_lineups) == 0:
            return "No lineups selected"

        count = len(selected_lineups)
        lineup_nums = ", ".join([f"#{i+1}" for i in sorted(selected_lineups)])
        return f"Selected {count} lineup{'s' if count != 1 else ''}: {lineup_nums}"

    # ========================================
    # CALLBACK 5: Lineup Dropdown → Tendency Radar
    # ========================================
    register_tendency_radar_callbacks(
        app=app,
        df_tendencies=df_tendencies,
        component_id='tendency-radar',
        star_player='Luka Dončić',
        external_checklist_id='lineup-comparison-dropdown'  # Dropdown ID
    )
