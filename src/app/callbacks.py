"""
Callback Functions for NBA Dashboard
Implements hierarchical filtering with multi-select comparative analysis.
"""

import plotly.graph_objects as go
from dash import Input, Output

# Import component creation functions
from src.app.components.player_profile import create_player_card_dash
from src.app.components.efficiency_landscape import create_efficiency_landscape
from src.app.components.tendency_radar_chart import create_tendency_radar
from src.app.components.shot_chart import create_shot_chart


def register_callbacks(app, df_efficiency, df_tendencies, df_shots):
    """
    Registers all Dash callbacks with hierarchical filtering logic.

    Filtering Hierarchy:
        Level 1: Star Player Selection
            - Updates Player Profile Card
            - Filters Lineup Archetype options

        Level 2: Lineup Archetype Selection (Multi-select)
            - Filters all visualizations (Shot Chart, Radar, Efficiency)
            - Supports comparative analysis with multiple lineups

    Args:
        app: Dash application instance
        df_efficiency: DataFrame with efficiency data
        df_tendencies: DataFrame with tendency data
        df_shots: DataFrame with shot location data
    """

    # --- LEVEL 1 FILTERING: Player Selection ---

    @app.callback(
        [Output('star-profile-card-container', 'children'),
         Output('shot-chart-title', 'children'),
         Output('radar-chart-title', 'children')],
        Input('star-profile-player-dropdown', 'value')
    )
    def update_player_card_and_titles(selected_player):
        """
        Updates the player profile card when a player is selected.

        This is the first level of filtering - updates the UI to show
        the selected player's information and graph titles.

        Args:
            selected_player: Name of the selected star player

        Returns:
            Tuple of (player card, shot chart title, radar chart title)
        """
        if not selected_player or df_efficiency.empty:
            return None, "Shot Chart", "Lineup Tendency Profile"

        # Get the first row for this player (for card display)
        player_data = df_efficiency[df_efficiency['star_player'] == selected_player]

        if player_data.empty:
            return None, "Shot Chart", "Lineup Tendency Profile"

        # Create dynamic titles with player name
        shot_title = f"{selected_player} - Shot Chart"
        radar_title = f"{selected_player} - Lineup Tendency Profile"

        # Use the first lineup's data for the player card
        return (
            create_player_card_dash(player_data.iloc[0]),
            shot_title,
            radar_title
        )


    @app.callback(
        [Output('lineup-dropdown', 'options'),
         Output('lineup-dropdown', 'value')],
        Input('star-profile-player-dropdown', 'value')
    )
    def update_lineup_options(selected_player):
        """
        Updates lineup dropdown options based on selected player.

        This filters the available lineups to only show those that
        include the selected star player.

        Args:
            selected_player: Name of the selected star player

        Returns:
            Tuple of (dropdown options, default selected values)
        """
        if not selected_player or df_efficiency.empty:
            return [], []

        # Filter efficiency data for selected player
        player_df = df_efficiency[df_efficiency['star_player'] == selected_player]

        if 'LINEUP_ARCHETYPE' in player_df.columns:
            unique_lineups = player_df['LINEUP_ARCHETYPE'].unique()
            options = [{'label': lineup, 'value': lineup} for lineup in unique_lineups]

            # For multi-select, default to first lineup only
            default_value = [options[0]['value']] if options else []

            return options, default_value

        return [], []


    # --- LEVEL 2 FILTERING: Lineup Selection (Multi-select) ---

    @app.callback(
        [Output('efficiency-graph', 'figure'),
         Output('tendency-radar-graph', 'figure'),
         Output('shot-chart-graph', 'figure')],
        [Input('star-profile-player-dropdown', 'value'),
         Input('lineup-dropdown', 'value')]
    )
    def update_all_visualizations(selected_player, selected_lineups):
        """
        Updates all three visualization graphs with hierarchical filtering.

        Filtering Logic:
            1. First filters by star_player
            2. Then filters by selected lineup(s) from dropdown
            3. Supports multiple lineup selection for comparison

        Args:
            selected_player: Name of the selected star player
            selected_lineups: List of selected lineup archetypes (multi-select)

        Returns:
            Tuple of (efficiency_fig, radar_fig, shot_fig)
        """
        # Default empty figure
        empty_fig = go.Figure().update_layout(
            template="plotly_dark",
            paper_bgcolor='rgba(0,0,0,0)'
        )

        # If no player selected, return empty figures
        if not selected_player:
            return [empty_fig] * 3

        # Ensure selected_lineups is a list (handle both single and multi-select)
        if not isinstance(selected_lineups, list):
            selected_lineups = [selected_lineups] if selected_lineups else []

        # --- 1. EFFICIENCY LANDSCAPE ---
        # Shows ALL lineups for the selected player
        # Highlights the selected lineup(s)
        player_efficiency = df_efficiency[df_efficiency['star_player'] == selected_player]

        # For efficiency, highlight all selected lineups
        fig_efficiency = create_efficiency_landscape(
            player_efficiency,
            selected_lineups  # Pass list of selected lineups for highlighting
        )

        # If no lineup selected yet, return efficiency graph only
        if not selected_lineups:
            return fig_efficiency, empty_fig, empty_fig

        # --- 2. TENDENCY RADAR CHART ---
        # For comparative analysis: overlay multiple lineups if selected
        # Or show single lineup if only one is selected

        if len(selected_lineups) == 1:
            # Single lineup selected - show standard radar
            player_tendency = df_tendencies[
                (df_tendencies['star_player'] == selected_player) &
                (df_tendencies['LINEUP_ARCHETYPE'] == selected_lineups[0])
            ]

            if player_tendency.empty:
                fig_radar = empty_fig
            else:
                fig_radar = create_tendency_radar(player_tendency.iloc[0])

        else:
            # Multiple lineups selected - create comparative radar
            fig_radar = create_comparative_radar(
                df_tendencies,
                selected_player,
                selected_lineups
            )

        # --- 3. SHOT CHART ---
        # Combine shots from all selected lineups for comparison
        lineup_shots = df_shots[
            (df_shots['star_player'] == selected_player) &
            (df_shots['LINEUP_ARCHETYPE'].isin(selected_lineups))
        ]

        fig_shot = create_shot_chart(lineup_shots)

        return fig_efficiency, fig_radar, fig_shot


def create_comparative_radar(df_tendencies, selected_player, selected_lineups):
    """
    Creates a comparative radar chart overlaying multiple lineups.

    Args:
        df_tendencies: Full tendencies dataframe
        selected_player: Selected star player name
        selected_lineups: List of lineup archetypes to compare

    Returns:
        Plotly figure with overlaid radar charts
    """
    from src.app.components.tendency_radar_chart import create_tendency_radar

    # Define metrics for comparison
    metrics_map = [
        ('3PT Pts', 'pct_pts_3pt'),
        ('Paint Pts', 'pct_pts_paint'),
        ('Fastbreak', 'pct_pts_fb'),
        ('Midrange', 'pct_pts_2pt_mr'),
        ('Assisted FG', 'pct_ast_fgm'),
        ('Unassisted FG', 'pct_uast_fgm')
    ]

    labels = [m[0] for m in metrics_map]

    # Basketball-themed color palette (orange/brown shades)
    colors = ['#E67E22', '#D35400', '#CA6F1E', '#BA4A00', '#935116']

    fig = go.Figure()

    # Add a trace for each selected lineup
    for idx, lineup in enumerate(selected_lineups[:5]):  # Limit to 5 for readability
        lineup_data = df_tendencies[
            (df_tendencies['star_player'] == selected_player) &
            (df_tendencies['LINEUP_ARCHETYPE'] == lineup)
        ]

        if lineup_data.empty:
            continue

        row = lineup_data.iloc[0]

        # Extract values and convert to percentages
        values = []
        for _, col in metrics_map:
            val = row.get(col, 0)
            if isinstance(val, (int, float)):
                values.append(float(val) * 100)
            else:
                values.append(0.0)

        # Close the radar circle
        values_closed = values + [values[0]]
        labels_closed = labels + [labels[0]]

        # Add trace for this lineup
        color = colors[idx % len(colors)]
        fig.add_trace(go.Scatterpolar(
            r=values_closed,
            theta=labels_closed,
            fill='toself',
            name=lineup,
            line=dict(color=color, width=2),
            fillcolor=f'rgba{tuple(list(bytes.fromhex(color[1:])) + [0.2])}',
            hovertemplate=f"<b>{lineup}</b><br>%{{theta}}: %{{r:.1f}}%<extra></extra>"
        ))

    # Update layout
    fig.update_layout(
        template="plotly_dark",
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100],
                showticklabels=True,
                tickvals=[0, 25, 50, 75, 100],
                ticktext=['0%', '25%', '50%', '75%', '100%'],
                gridcolor='rgba(255, 255, 255, 0.1)'
            ),
            angularaxis=dict(
                gridcolor='rgba(255, 255, 255, 0.1)'
            ),
            bgcolor='rgba(0,0,0,0)'
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=40, r=40, t=30, b=30),
        height=350,
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.3,
            xanchor="center",
            x=0.5,
            font=dict(size=10)
        )
    )

    return fig
