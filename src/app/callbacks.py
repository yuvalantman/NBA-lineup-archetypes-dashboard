"""
Callback Functions for NBA Dashboard
Implements hierarchical filtering with multi-select comparative analysis.
"""

import plotly.graph_objects as go
from dash import Input, Output, no_update
import plotly.express as px

# Import component creation functions
from src.app.components.player_profile import create_player_card_dash
from src.app.components.efficiency_landscape import create_efficiency_landscape
from src.app.components.tendency_radar_chart import create_tendency_radar
from src.app.components.shot_chart import create_shot_chart


def register_callbacks(app, df_players, df_efficiency, df_tendencies, df_shots, df_team_vs_opponent):
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
        player_data = df_players[df_players['PLAYER'] == selected_player]

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
        Output('main-lineup-dropdown', 'options'),
        Output('main-lineup-dropdown', 'value'),
        Output('lineup-dropdown', 'options'),
        Output('lineup-dropdown', 'value'),
        Input('star-profile-player-dropdown', 'value'),
        Input('main-lineup-dropdown', 'value')
    )
    def update_lineup_dropdowns(selected_player, current_main):
        if not selected_player or df_efficiency.empty:
            return [], None, [], []

        player_df = df_efficiency[df_efficiency['star_player'] == selected_player]
        unique_lineups = player_df['LINEUP_ARCHETYPE'].unique().tolist()

        # compare options include main

        options_main = [{'label': l, 'value': l} for l in unique_lineups]
        if current_main in unique_lineups:
            main_value = current_main
        else:
            main_value = unique_lineups[0] if unique_lineups else None

        # compare options exclude main
        compare_lineups = [l for l in unique_lineups if l != main_value]
        options_compare = [{'label': l, 'value': l} for l in compare_lineups]

        return options_main, main_value, options_compare, []


    # --- LEVEL 2 FILTERING: Lineup Selection (Multi-select) ---

    @app.callback(
        Output('efficiency-graph', 'figure'),
        Output('tendency-radar-graph', 'figure'),
        Output('shot-chart-graph', 'figure'),
        Input('star-profile-player-dropdown', 'value'),
        Input('main-lineup-dropdown', 'value'),
        Input('lineup-dropdown', 'value')
    )
    def update_all_visualizations(selected_player, main_lineup, compare_lineups):
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
        if not isinstance(compare_lineups, list):
            compare_lineups = [compare_lineups] if compare_lineups else []
        # Remove duplicates while preserving order
        seen = set()
        seen.add(main_lineup)
        compare_lineups = [x for x in compare_lineups if not (x in seen or seen.add(x))]

        radar_lineups = []
        if main_lineup:
            radar_lineups.append(main_lineup)

        for l in compare_lineups:
            if l and l != main_lineup:
                radar_lineups.append(l)

        # --- 1. EFFICIENCY LANDSCAPE ---
        # Shows ALL lineups for the selected player
        # Highlights the selected lineup(s)
        player_efficiency = df_efficiency[df_efficiency['star_player'] == selected_player]
        fig_efficiency = create_efficiency_landscape(player_efficiency, selected_lineups=main_lineup)


        # For efficiency, highlight all selected lineups
        # fig_efficiency = create_efficiency_landscape(
        #     player_efficiency,
        #     selected_lineups  # Pass list of selected lineups for highlighting
        # )

        # If no lineup selected yet, return efficiency graph only
        # if not selected_lineups:
        #     return fig_efficiency, empty_fig, empty_fig

        # --- 2. TENDENCY RADAR CHART ---
        # For comparative analysis: overlay multiple lineups if selected
        # Or show single lineup if only one is selected

        if len(radar_lineups) == 1:
            player_tendency = df_tendencies[
                (df_tendencies['star_player'] == selected_player) &
                (df_tendencies['LINEUP_ARCHETYPE'] == radar_lineups[0])
            ]
            fig_radar = empty_fig if player_tendency.empty else create_tendency_radar(player_tendency.iloc[0])
        else:
            fig_radar = create_comparative_radar(df_tendencies, selected_player, radar_lineups)


        # --- 3. SHOT CHART ---
        # Combine shots from all selected lineups for comparison
        lineup_shots = df_shots[
            (df_shots['star_player'] == selected_player) &
            (df_shots['LINEUP_ARCHETYPE'] == main_lineup)
        ]
        fig_shot = create_shot_chart(lineup_shots)


        return fig_efficiency, fig_radar, fig_shot
    
    @app.callback(
        Output('efficiency-hover-info', 'children'),
        Input('efficiency-graph', 'hoverData')
    )
    def update_efficiency_hover(hoverData):
        if not hoverData or 'points' not in hoverData or not hoverData['points']:
            return "Hover a point to see lineup details."

        p = hoverData['points'][0]
        lineup = p.get('hovertext') or p.get('customdata', [None])[0]
        x = p.get('x')
        y = p.get('y')
        color = p.get('net_rating')

        return f"Hovered Lineup: {lineup} \n OffRtg: {x:.2f} \n DefRtg: {y:.2f}"



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
    # colors = [
    #     '#00BFFF',  # cyan (main)
    #     '#E74C3C',  # red
    #     '#2ECC71',  # green
    #     '#F1C40F',  # yellow
    #     '#9B59B6',   # purple
    #     '#3498DB',   # blue
    # ]

    colors = px.colors.qualitative.Dark24
    def hex_to_rgba(hex_color, alpha=0.15):
        hex_color = hex_color.lstrip('#')
        r = int(hex_color[0:2], 16)
        g = int(hex_color[2:4], 16)
        b = int(hex_color[4:6], 16)
        return f'rgba({r},{g},{b},{alpha})'


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
            fillcolor=hex_to_rgba(color, 0.15),
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
