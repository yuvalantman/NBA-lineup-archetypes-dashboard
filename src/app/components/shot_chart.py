"""
Shot Chart Component for NBA Dashboard
Visualizes shot locations on an NBA court for a specific lineup.
"""

import plotly.graph_objects as go
import numpy as np
import pandas as pd
from src.app.components.court_visualization import draw_nba_court
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap


def create_shot_chart(df, height=500):
    """
    Creates a shot chart visualization on an NBA court.

    Features:
        - Uses LOC_X and LOC_Y coordinates from the shots CSV
        - Made shots (SHOT_MADE_FLAG=1) shown as cyan circles
        - Missed shots (SHOT_MADE_FLAG=0) shown as orange X markers
        - Overlays shots on official NBA court dimensions

    Args:
        df: DataFrame with shot data (LOC_X, LOC_Y, SHOT_MADE_FLAG columns)
        height: Height of the figure in pixels (default: 500)

    Returns:
        Plotly figure object with shot chart
    """
    fig = go.Figure()

    # If the dataframe is empty, return an empty court diagram
    if df is None or df.empty:
        return draw_nba_court(fig)

    # Filter shots by outcome
    made = df[df['SHOT_MADE_FLAG'] == 1]
    missed = df[df['SHOT_MADE_FLAG'] == 0]

    # Add Missed Shots as red 'X' markers
    if not missed.empty:
        fig.add_trace(go.Scatter(
            x=missed['LOC_X'],
            y=missed['LOC_Y'],
            mode='markers',
            name='Missed',
            marker=dict(
                color='#D32F2F',  # Red for missed shots
                size=5,
                opacity=0.5,
                symbol='x'
            )
        ))

    # Add Made Shots as forest green circles
    if not made.empty:
        fig.add_trace(go.Scatter(
            x=made['LOC_X'],
            y=made['LOC_Y'],
            mode='markers',
            name='Made',
            marker=dict(
                color='#2E7D32',  # Deep forest green for made shots
                size=6,
                opacity=0.7,
                symbol='circle'
            )
        ))

    # Apply the NBA court lines
    fig = draw_nba_court(fig)

    # Standardize the court view and aspect ratio
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        height=height,
        xaxis=dict(
            visible=False,
            range=[-260, 260]
        ),
        yaxis=dict(
            visible=False,
            range=[-52.5, 430],
            scaleanchor="x"
        ),
        margin=dict(l=5, r=5, t=5, b=5)
    )

    return fig


def create_hexbin_shot_chart(df, height=500):
    """
    Creates a hexbin shot chart visualization on an NBA court.
    
    Features:
        - Divides court into hexagonal bins using matplotlib-style hexbin
        - Color represents FG% in that hex (using custom blue-to-red colormap)
        - Size represents shot frequency
        - Minimum threshold of shots per hex for display
    
    Args:
        df: DataFrame with shot data (LOC_X, LOC_Y, SHOT_MADE_FLAG columns)
        height: Height of the figure in pixels (default: 500)
    
    Returns:
        Plotly figure object with hexbin shot chart
    """
    
    
    fig = go.Figure()
    
    # If the dataframe is empty, return an empty court diagram
    if df is None or df.empty:
        fig = draw_nba_court(fig)
        fig.update_layout(
            template="plotly_dark",
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            height=height,
            xaxis=dict(visible=False, range=[-260, 260]),
            yaxis=dict(visible=False, range=[-52.5, 430], scaleanchor="x"),
            margin=dict(l=5, r=5, t=5, b=5)
        )
        return fig
    
    # Filter shots to only include half court
    df_filtered = df[df['LOC_Y'] < 425.1].copy()
    
    if df_filtered.empty:
        fig = draw_nba_court(fig)
        fig.update_layout(
            template="plotly_dark",
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            height=height,
            xaxis=dict(visible=False, range=[-260, 260]),
            yaxis=dict(visible=False, range=[-52.5, 430], scaleanchor="x"),
            margin=dict(l=5, r=5, t=5, b=5)
        )
        return fig
    
    x = df_filtered['LOC_X'].values
    y = df_filtered['LOC_Y'].values
    made = df_filtered['SHOT_MADE_FLAG'].values
    
    # Use matplotlib hexbin to calculate hex positions and statistics
    # Calculate total shots hexbin (extent: xmin, xmax, ymin, ymax)
    fig_temp, ax_temp = plt.subplots()
    hb_shots = ax_temp.hexbin(x, y, gridsize=40, extent=(-250, 250, -47.5, 425))
    plt.close(fig_temp)
    
    # Calculate made shots hexbin
    x_made = df_filtered['LOC_X'][df_filtered['SHOT_MADE_FLAG'] == 1].values
    y_made = df_filtered['LOC_Y'][df_filtered['SHOT_MADE_FLAG'] == 1].values
    
    fig_temp2, ax_temp2 = plt.subplots()
    hb_made = ax_temp2.hexbin(x_made, y_made, gridsize=40, extent=(-250, 250, -47.5, 425))
    plt.close(fig_temp2)
    
    # Calculate shooting percentage per hex
    shot_counts = hb_shots.get_array()
    made_counts = hb_made.get_array()
    shooting_pcts = np.divide(made_counts, shot_counts, out=np.zeros_like(made_counts, dtype=float), where=shot_counts > 0)
    
    # Get hex positions
    hex_positions = hb_shots.get_offsets()
    
    # Filter hexes with minimum shot threshold
    min_shots = 3
    valid_hexes = shot_counts >= min_shots
    
    hex_x = hex_positions[valid_hexes, 0]
    hex_y = hex_positions[valid_hexes, 1]
    hex_fg = shooting_pcts[valid_hexes]
    hex_shots = shot_counts[valid_hexes]
    hex_made = made_counts[valid_hexes]
    
    # Calculate frequency for sizing
    total_shots = len(df_filtered)
    hex_freq = hex_shots / total_shots
    
    # Custom colormap matching the notebook style (blue to red)
    custom_colors = ['#2e68b2', '#e5de9c', '#f47623', '#e32b30']
    
    if len(hex_x) > 0:
        # Create scatter plot with hexagons
        fig.add_trace(go.Scatter(
            x=hex_x,
            y=hex_y,
            mode='markers',
            marker=dict(
                size=hex_freq * 1500,  # Scale for visibility
                sizemode='area',
                sizemin=5,
                color=hex_fg,
                colorscale=[
                    [0.0, custom_colors[0]],  # Low FG% - Blue
                    [0.33, custom_colors[1]],  # Below avg - Yellow
                    [0.67, custom_colors[2]],  # Above avg - Orange
                    [1.0, custom_colors[3]]    # High FG% - Red
                ],
                cmin=0,
                cmax=1,
                colorbar=dict(
                    title=dict(text="FG%", side="right"),
                    tickformat='.0%',
                    len=0.5,
                    thickness=15,
                    x=1.02
                ),
                symbol='hexagon',
                line=dict(width=0, color='rgba(0,0,0,0)')
            ),
            hovertemplate='<b>FG%%: %{customdata[2]:.1%}</b><br>' +
                         'Shots: %{customdata[0]:.0f}<br>' +
                         'Made: %{customdata[1]:.0f}<extra></extra>',
            customdata=np.column_stack([hex_shots, hex_made, hex_fg]),
            showlegend=False
        ))
    
    # Apply the NBA court lines
    fig = draw_nba_court(fig)
    
    # Standardize the court view and aspect ratio
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        height=height,
        xaxis=dict(
            visible=False,
            range=[-260, 260]
        ),
        yaxis=dict(
            visible=False,
            range=[-52.5, 430],
            scaleanchor="x"
        ),
        margin=dict(l=5, r=5, t=5, b=5)
    )
    
    return fig
