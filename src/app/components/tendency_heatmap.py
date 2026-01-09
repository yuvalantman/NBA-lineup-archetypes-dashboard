"""
Tendency Heatmap Component for NBA Dashboard
Visualizes play-style tendencies using a heatmap with color-normalized metrics.
"""

import plotly.graph_objects as go
import pandas as pd
import numpy as np


def create_tendency_heatmap(df_tendencies, selected_player, selected_lineups):
    """
    Creates a heatmap showing lineup play-style tendencies.

    Features:
        - Color normalized per metric across all lineups of the star player
        - Green = highest value for that metric, Red = lowest
        - Rows = metrics
        - Columns = selected lineups (up to 5)
        - Cell annotations show actual values (multiplied by 10 from CSV)

    Args:
        df_tendencies: Full tendencies DataFrame
        selected_player: Name of the star player
        selected_lineups: List of lineup names to display (max 5)

    Returns:
        Plotly figure object
    """
    if df_tendencies is None or df_tendencies.empty or not selected_player:
        return go.Figure().update_layout(
            template="plotly_dark",
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)'
        )

    # Filter data for the selected player
    player_df = df_tendencies[df_tendencies['star_player'] == selected_player].copy()
    
    if player_df.empty:
        return go.Figure().update_layout(
            template="plotly_dark",
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)'
        )

    # Define the metrics to display
    metrics_map = [
        ('EFG %', 'efg_pct'),
        ('TS %', 'ts_pct'),
        ('3PT Pts %', 'pct_pts_3pt'),
        ('Paint Pts %', 'pct_pts_paint'),
        ('Fastbreak %', 'pct_pts_fb'),
        ('Midrange %', 'pct_pts_2pt_mr'),
        ('Assisted FGM %', 'pct_ast_fgm'),
        ('Unassisted FGM %', 'pct_uast_fgm')
    ]

    metric_labels = [m[0] for m in metrics_map]
    metric_columns = [m[1] for m in metrics_map]

    # Handle selected lineups (max 5)
    if not selected_lineups:
        selected_lineups = []
    elif not isinstance(selected_lineups, list):
        selected_lineups = [selected_lineups]
    
    # Limit to 5 lineups
    selected_lineups = selected_lineups[:5]

    if not selected_lineups:
        # Show empty heatmap with message
        fig = go.Figure()
        fig.add_annotation(
            text="Select a lineup to view tendency heatmap",
            xref="paper", yref="paper",
            x=0.5, y=0.5,
            showarrow=False,
            font=dict(size=14, color='#8e9aaf')
        )
        fig.update_layout(
            template="plotly_dark",
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            height=360
        )
        return fig

    # Build the heatmap data matrix
    # Rows = metrics, Columns = lineups
    z_values = []  # For color (normalized per metric across ALL player lineups)
    text_values = []  # For displayed values (x100)
    
    # Create column labels and lineup legend
    lineup_labels = []
    lineup_legend = []
    
    for idx, lineup in enumerate(selected_lineups):
        # Add spaces around dashes for better readability
        formatted_lineup = lineup.replace('-', ' - ')
        
        if idx == 0:
            lineup_labels.append("Main Lineup")
            lineup_legend.append(f"<b>Main Lineup:</b> {formatted_lineup}")
        else:
            lineup_labels.append(f"Lineup {idx}")
            lineup_legend.append(f"<b>Lineup {idx}:</b> {formatted_lineup}")
    
    for metric_col in metric_columns:
        row_z = []
        row_text = []
        
        # Get min/max for this metric across ALL player lineups for normalization
        metric_min = player_df[metric_col].min()
        metric_max = player_df[metric_col].max()
        metric_range = metric_max - metric_min
        
        for lineup in selected_lineups:
            lineup_data = player_df[player_df['LINEUP_ARCHETYPE'] == lineup]
            
            if not lineup_data.empty:
                value = lineup_data[metric_col].iloc[0]
                
                # Normalize for color (0-1 scale) based on ALL player lineups
                if metric_range > 0:
                    normalized = (value - metric_min) / metric_range
                else:
                    normalized = 0.5
                
                # Display value (x100 for percentage)
                display_value = value * 100
                
                row_z.append(normalized)
                row_text.append(f"{display_value:.1f}")
            else:
                row_z.append(0.5)  # Neutral value if not found
                row_text.append("N/A")
        
        z_values.append(row_z)
        text_values.append(row_text)

    # Create more subtle color palette for better text readability
    # Using a blue-to-orange palette instead of red-yellow-green
    subtle_colorscale = [
        [0.0, '#2C3E50'],    # Dark blue-gray (low)
        [0.25, '#34495E'],   # Medium-dark gray
        [0.5, '#7F8C8D'],    # Medium gray
        [0.75, '#E67E22'],   # Orange
        [1.0, '#D35400']     # Dark orange (high)
    ]

    # Create the heatmap
    fig = go.Figure(data=go.Heatmap(
        z=z_values,
        x=lineup_labels,
        y=metric_labels,
        text=text_values,
        texttemplate="%{text}",
        textfont={"size": 13, "color": "white"},
        colorscale=subtle_colorscale,
        showscale=True,
        colorbar=dict(
            title=dict(
                text="Normalized<br>Value",
                side="right"
            ),
            tickmode="array",
            tickvals=[0, 0.5, 1],
            ticktext=["Low", "Mid", "High"],
            len=0.5,
            thickness=15
        ),
        hovertemplate="<b>%{y}</b><br>%{x}<br>Value: %{text}%<extra></extra>"
    ))

    # Create lineup legend text
    legend_text = "<br>".join(lineup_legend)

    # Update layout with bottom margin for legend
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=10, r=10, t=40, b=120),  # Increased bottom margin for legend
        height=460,
        xaxis=dict(
            title="",
            side='top',
            gridcolor='rgba(255, 255, 255, 0.1)'
        ),
        yaxis=dict(
            title="",
            gridcolor='rgba(255, 255, 255, 0.1)'
        )
    )

    # Add lineup legend as annotation below the heatmap
    fig.add_annotation(
        text=legend_text,
        xref="paper", yref="paper",
        x=-0.3, y=-0.22,
        xanchor="left", yanchor="top",
        showarrow=False,
        font=dict(size=11, color='#8e9aaf'),
        align="left"
    )

    return fig


# ============================================================================
# COMMENTED OUT: ORIGINAL RADAR CHART CODE (kept for potential future use)
# ============================================================================
"""
def create_tendency_radar(row):
    '''
    Creates a radar chart showing lineup play-style tendencies.

    Features:
        - Fixed radial axis range [0, 100] to prevent jumping
        - Shows 5 key metrics as percentages
        - Normalized data display

    Args:
        row: Single row (Series or dict) containing tendency data for one lineup

    Returns:
        Plotly figure object
    '''
    # Define the metrics to display on the radar chart
    metrics_map = [
        ('3PT Pts', 'pct_pts_3pt'),
        ('Paint Pts', 'pct_pts_paint'),
        ('Fastbreak', 'pct_pts_fb'),
        ('Midrange', 'pct_pts_2pt_mr'),
        ('Assisted FG', 'pct_ast_fgm'),
        ('Unassisted FG', 'pct_uast_fgm')
    ]

    labels = [m[0] for m in metrics_map]

    # Extract values and convert to percentages (0-100 scale)
    # Values in CSV are decimals (0.0-1.0), so multiply by 100
    values = []
    for _, col in metrics_map:
        val = row.get(col, 0)
        # Convert to percentage
        if isinstance(val, (int, float)):
            values.append(float(val) * 100)
        else:
            values.append(0.0)

    # Close the radar circle by repeating the first value
    values_closed = values + [values[0]]
    labels_closed = labels + [labels[0]]

    # Create the radar chart with basketball-themed colors (orange/brown)
    fig = go.Figure(data=go.Scatterpolar(
        r=values_closed,
        theta=labels_closed,
        fill='toself',
        line=dict(color='#E67E22', width=2),  # Basketball orange
        fillcolor='rgba(230, 126, 34, 0.3)',  # Semi-transparent orange
        hovertemplate="<b>%{theta}</b>: %{r:.1f}%<extra></extra>"
    ))

    # Update layout with STRICT [0, 100] range to prevent jumping
    fig.update_layout(
        template="plotly_dark",
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 75],      # FIXED: Always 0-100%
                showticklabels=True,
                tickvals=[0, 25, 50, 75],
                ticktext=['0%', '25%', '50%', '75%'],
                gridcolor='rgba(255, 255, 255, 0.1)'
            ),
            angularaxis=dict(
                gridcolor='rgba(255, 255, 255, 0.1)'
            ),
            bgcolor='rgba(0,0,0,0)'
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=40, r=40, t=30, b=30),
        height=350
    )

    return fig
"""
