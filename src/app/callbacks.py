"""
Callback Functions for NBA Dashboard
Implements hierarchical filtering with multi-select comparative analysis.
"""

import plotly.graph_objects as go
from dash import Input, Output, no_update, html
import plotly.express as px

# Import component creation functions
from src.app.components.player_profile import create_player_card_dash
from src.app.components.efficiency_landscape import create_efficiency_landscape
# from src.app.components.tendency_radar_chart import create_tendency_radar  # COMMENTED: Radar chart
from src.app.components.tendency_heatmap import create_tendency_heatmap  # NEW: Heatmap
from src.app.components.shot_chart import create_shot_chart, create_zone_shot_chart
from src.app.components.team_vs_opp import create_team_vs_opp_chart
from src.app.components.archetype_profile import create_archetype_card_dash
from src.data.archetype_specs import ARCHETYPE_SPECS


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
         Output('efficiency-landscape-title', 'children'),
         Output('radar-chart-title', 'children'),
         Output('team-vs-opp-title', 'children')],
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
            Tuple of (player card, shot chart title, efficiency landscape title, heatmap chart title, team vs opp title)
        """
        if not selected_player or df_efficiency.empty:
            return None, "Shot Chart", "Efficiency Landscape", "Lineup Tendency Heatmap", "Team vs Opponent Comparison"

        # Get the first row for this player (for card display)
        player_data = df_players[df_players['PLAYER'] == selected_player]

        if player_data.empty:
            return None, "Shot Chart", "Efficiency Landscape", "Lineup Tendency Heatmap", "Team vs Opponent Comparison"

        # Create dynamic titles with player name
        shot_title = f"{selected_player} - Shot Chart"
        efficiency_title = f"{selected_player} - Efficiency Landscape"
        heatmap_title = f"{selected_player} - Lineup Tendency Heatmap"
        team_vs_opp_title = f"{selected_player} - Team vs Opponent Comparison"

        # Use the first lineup's data for the player card
        return (
            create_player_card_dash(player_data.iloc[0]),
            shot_title,
            efficiency_title,
            heatmap_title,
            team_vs_opp_title
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

    @app.callback(
        Output('lineup-specs-content', 'children'),
        Input('star-profile-player-dropdown', 'value'),
        Input('main-lineup-dropdown', 'value')
    )
    def update_main_lineup_specs(selected_player, main_lineup):
        """
        Updates the main lineup specifications section with archetype details and minutes played.
        
        Args:
            selected_player: Currently selected star player
            main_lineup: Selected main lineup archetype
            
        Returns:
            Dash HTML component with lineup specifications
        """
        if not selected_player or not main_lineup or df_efficiency.empty:
            return html.P("Select a lineup to view specifications", style={'color': '#8e9aaf', 'fontStyle': 'italic'})
        
        # Get the main lineup data
        lineup_data = df_efficiency[
            (df_efficiency['star_player'] == selected_player) & 
            (df_efficiency['LINEUP_ARCHETYPE'] == main_lineup)
        ]
        
        if lineup_data.empty:
            return html.P("No data available for selected lineup", style={'color': '#8e9aaf', 'fontStyle': 'italic'})
        
        lineup_row = lineup_data.iloc[0]
        
        # Parse archetypes from LINEUP_ARCHETYPE (separated by "-")
        archetypes = [arch.strip() for arch in main_lineup.split('-')]
        
        # Get minutes played
        min_sum = lineup_row.get('min_sum', 0)
        
        return html.Div([
            # Archetypes section
            html.Div([
                html.H6("Lineup Archetypes:", style={'color': '#00BFFF', 'fontSize': '12px', 'marginBottom': '6px', 'fontWeight': 'bold', 'marginTop': '0'}),
                html.Div(
                    [html.Span(
                        archetype,
                        style={
                            'display': 'inline-block',
                            'backgroundColor': 'rgba(0, 191, 255, 0.15)',
                            'color': '#00BFFF',
                            'padding': '4px 10px',
                            'borderRadius': '6px',
                            'fontSize': '11px',
                            'margin': '2px 6px 2px 0',
                            'border': '1px solid rgba(0, 191, 255, 0.4)',
                            'fontWeight': '500'
                        }
                    ) for archetype in archetypes],
                    style={'marginBottom': '8px'}
                )
            ]),
            
            # Minutes played section
            html.Div([
                html.Span("Total Minutes Played Together: ", style={'color': '#b8c5d6', 'fontSize': '11px', 'fontWeight': 'bold'}),
                html.Span(f"{min_sum:.1f}", style={'color': '#4ade80', 'fontSize': '12px', 'fontWeight': 'bold'})
            ])
        ])


    # --- LEVEL 2 FILTERING: Lineup Selection (Multi-select) ---

    @app.callback(
        Output('efficiency-graph', 'figure'),
        Output('tendency-radar-graph', 'figure'),
        Output('shot-chart-graph', 'figure'),
        Output('team-vs-opp-graph', 'figure'),
        Input('star-profile-player-dropdown', 'value'),
        Input('main-lineup-dropdown', 'value'),
        Input('lineup-dropdown', 'value'),
        Input('shot-chart-type', 'value')
    )
    def update_all_visualizations(selected_player, main_lineup, compare_lineups, shot_chart_type):
        """
        Updates all visualization graphs with hierarchical filtering.

        Filtering Logic:
            1. First filters by star_player
            2. Then filters by selected lineup(s) from dropdown
            3. Supports multiple lineup selection for comparison

        Args:
            selected_player: Name of the selected star player
            main_lineup: Main lineup archetype
            compare_lineups: List of lineup archetypes for comparison (multi-select)
            shot_chart_type: Type of shot chart ('raw' or 'zones')

        Returns:
            Tuple of (efficiency_fig, heatmap_fig, shot_fig, team_vs_opp_fig)
        """
        # Default empty figure
        empty_fig = go.Figure().update_layout(
            template="plotly_dark",
            paper_bgcolor='rgba(0,0,0,0)'
        )

        # If no player selected, return empty figures
        if not selected_player:
            return [empty_fig] * 4  # 4 outputs: efficiency, heatmap, shot, team_vs_opp

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

        # --- 2. TENDENCY HEATMAP ---
        # Shows color-normalized metrics per lineup (max 5 lineups)
        # Green = highest, Red = lowest (normalized per metric across all player lineups)
        
        fig_radar = create_tendency_heatmap(df_tendencies, selected_player, radar_lineups)
        
        # ============================================================================
        # COMMENTED OUT: ORIGINAL RADAR CHART CODE (kept for potential future use)
        # ============================================================================
        # if len(radar_lineups) == 1:
        #     player_tendency = df_tendencies[
        #         (df_tendencies['star_player'] == selected_player) &
        #         (df_tendencies['LINEUP_ARCHETYPE'] == radar_lineups[0])
        #     ]
        #     fig_radar = empty_fig if player_tendency.empty else create_tendency_radar(player_tendency.iloc[0])
        # else:
        #     fig_radar = create_comparative_radar(df_tendencies, selected_player, radar_lineups)


        # --- 3. SHOT CHART ---
        # Combine shots from all selected lineups for comparison
        lineup_shots = df_shots[
            (df_shots['star_player'] == selected_player) &
            (df_shots['LINEUP_ARCHETYPE'] == main_lineup)
        ]
        
        # Choose shot chart type based on user selection
        if shot_chart_type == 'zones':
            fig_shot = create_zone_shot_chart(lineup_shots)
        else:  # 'raw'
            fig_shot = create_shot_chart(lineup_shots)
        
        fig_team_vs_opp = create_team_vs_opp_chart(
            df_team_vs_opponent[df_team_vs_opponent["star_player"] == selected_player],
            lineup_key=main_lineup
        )

        return fig_efficiency, fig_radar, fig_shot, fig_team_vs_opp
    
    @app.callback(
        Output('efficiency-hover-info', 'children'),
        Output('efficiency-hover-info', 'style'),
        Input('efficiency-graph', 'hoverData')
    )
    def update_efficiency_hover(hoverData):
        base_style = {
            'minHeight': '24px',
            'marginBottom': '8px',
            'color': 'rgba(255,255,255,0.85)',
            'fontSize': '14px',
            'padding': '10px 14px',
            'borderRadius': '8px',
            'border': '1px solid #2d384d',
            'backgroundColor': 'transparent'
        }

        # When not hovering (clear_on_unhover=True makes hoverData None)
        if not hoverData or 'points' not in hoverData or not hoverData['points']:
            return (
                html.H5("Hover a point to see lineup details.", style={'color': 'white', 'marginBottom': '5px'}),
                base_style
            )

        p = hoverData['points'][0]
        lineup, off, deff, net, bg = p['customdata']

        # Calculate text color based on background brightness
        # Extract RGB from color string (handle both rgb and rgba formats)
        import re
        match = re.search(r'rgba?\((\d+),\s*(\d+),\s*(\d+)', bg)
        if match:
            r, g, b = int(match.group(1)), int(match.group(2)), int(match.group(3))
            # Calculate luminance (standard formula)
            luminance = (0.299 * r + 0.587 * g + 0.114 * b) / 255
            # Use dark text for bright backgrounds, white for dark backgrounds
            text_color = 'black' if luminance > 0.5 else 'white'
        else:
            text_color = 'white'

        style = dict(base_style)
        style['backgroundColor'] = bg  # this is now a real rgba/rgb string

        return (
            html.Div([
                html.Div(lineup, style={'fontWeight': 'bold', 'fontSize': '14px', 'marginBottom': '6px', 'color': text_color}),
                html.Div(f"OffRtg: {off:.1f}   |   DefRtg: {deff:.1f}   |   Net: {net:+.1f}", style={'color': text_color})
            ]),
            style
        )

    # --- ARCHETYPE EXPLORATION ---
    
    @app.callback(
        Output('archetype-dropdown', 'options'),
        Input('star-profile-player-dropdown', 'value')
    )
    def populate_archetype_dropdown(selected_player):
        """
        Populates archetype dropdown options from ARCHETYPE_SPECS.
        
        Args:
            selected_player: Currently selected player
            
        Returns:
            List of archetype options for dropdown
        """
        # Get all archetype names from ARCHETYPE_SPECS
        archetype_names = sorted(ARCHETYPE_SPECS.keys())
        return [{'label': archetype, 'value': archetype} for archetype in archetype_names]
    
    @app.callback(
        Output('archetype-card-container', 'children'),
        Input('archetype-dropdown', 'value')
    )
    def update_archetype_card(selected_archetype):
        """
        Updates the archetype profile card when an archetype is selected.
        
        Args:
            selected_archetype: Name of the selected archetype
            
        Returns:
            Archetype profile card component
        """
        if not selected_archetype:
            return create_archetype_card_dash()
        
        # Get archetype data from ARCHETYPE_SPECS
        if selected_archetype not in ARCHETYPE_SPECS:
            return create_archetype_card_dash()
        
        archetype_data = ARCHETYPE_SPECS[selected_archetype]
        
        # Format data for the card component
        card_data = {
            'archetype_name': selected_archetype,
            'description': archetype_data.get('description', ''),
            'strengths': archetype_data.get('strengths', []),
            'weaknesses': archetype_data.get('limitations', []),  # 'limitations' key in specs
            'similar_players': archetype_data.get('examples', [])
        }
        
        return create_archetype_card_dash(card_data)
        # Placeholder - will be replaced when archetype data is provided
        # Example structure when data is ready:
        # archetype_row = df_archetypes[df_archetypes['archetype_name'] == selected_archetype].iloc[0]
        # return create_archetype_card_dash(archetype_row)
        
        # For now, return a sample card to show the template
        sample_data = {
            'archetype_name': selected_archetype,
            'description': 'Archetype data will be loaded from DataFrame',
            'strengths': ['Data pending'],
            'weaknesses': ['Data pending'],
            'similar_players': ['Data pending']
        }
        return create_archetype_card_dash(sample_data)


# ============================================================================
# COMMENTED OUT: COMPARATIVE RADAR CHART FUNCTION (kept for potential future use)
# ============================================================================
"""
def create_comparative_radar(df_tendencies, selected_player, selected_lineups):
    '''
    Creates a comparative radar chart overlaying multiple lineups.

    Args:
        df_tendencies: Full tendencies dataframe
        selected_player: Selected star player name
        selected_lineups: List of lineup archetypes to compare

    Returns:
        Plotly figure with overlaid radar charts
    '''
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
"""
