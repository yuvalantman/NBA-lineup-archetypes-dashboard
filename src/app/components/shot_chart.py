"""
NBA Court Visualization Module

This module provides functions to draw an accurate NBA basketball court
using Plotly shapes. The court can be overlaid with shot data or other visualizations.

Coordinate System:
- Origin (0, 0) = center of the hoop
- X-axis: -250 to 250 (left to right, 50 feet total)
- Y-axis: -47.5 to 422.5 (baseline to half-court, 47 feet total)
- Units are in 1/10 of a foot
"""

import plotly.graph_objects as go
import numpy as np
from typing import Optional, Dict


def get_nba_court_dimensions() -> Dict:
    """
    Returns NBA court dimensions in coordinate units (1/10 foot).

    Returns:
        Dictionary containing all court element dimensions and positions
    """
    return {
        # Court bounds
        'width': 500,           # 50 feet
        'height': 470,          # 47 feet (half-court)
        'x_min': -250,
        'x_max': 250,
        'y_min': -47.5,
        'y_max': 422.5,

        # Hoop and basket
        'hoop_center': (0, 0),
        'hoop_radius': 7.5,      # 0.75 feet
        'backboard_width': 60,   # 6 feet
        'backboard_y': -7.5,     # 0.75 feet behind hoop

        # Paint / Key
        'paint_width': 160,      # 16 feet
        'paint_length': 190,     # 19 feet
        'paint_center_y': 47.5,  # Center of paint relative to hoop

        # Free throw
        'ft_circle_center': (0, 142.5),  # 14.25 feet from hoop
        'ft_circle_radius': 60,           # 6 feet
        'ft_line_length': 160,            # 16 feet (same as paint width)

        # Three-point line
        'three_pt_corner_x': 220,        # 22 feet from center
        'three_pt_arc_radius': 237.5,    # 23.75 feet
        'three_pt_corner_y_start': -47.5,
        'three_pt_corner_y_end': 92.5,   # Where corner meets arc

        # Restricted area
        'restricted_radius': 40,          # 4 feet
    }


def _generate_arc_points(center_x: float, center_y: float, radius: float,
                        start_angle: float, end_angle: float, num_points: int = 50) -> tuple:
    """
    Generate points along an arc.

    Args:
        center_x: X coordinate of arc center
        center_y: Y coordinate of arc center
        radius: Radius of the arc
        start_angle: Starting angle in degrees (0 = right, 90 = up)
        end_angle: Ending angle in degrees
        num_points: Number of points to generate along the arc

    Returns:
        Tuple of (x_coords, y_coords) arrays
    """
    angles = np.linspace(np.radians(start_angle), np.radians(end_angle), num_points)
    x = center_x + radius * np.cos(angles)
    y = center_y + radius * np.sin(angles)
    return x, y


def draw_nba_court(fig: Optional[go.Figure] = None,
                   line_color: str = 'white',
                   line_width: float = 2,
                   court_background: str = 'rgba(0,0,0,0)',
                   show_half_court: bool = True) -> go.Figure:
    """
    Draw an NBA basketball court on a Plotly figure.

    Args:
        fig: Existing Plotly figure to add court to. Creates new if None.
        line_color: Color of court lines (default: white)
        line_width: Width of court lines in pixels (default: 2)
        court_background: Background color for court area (default: transparent)
        show_half_court: If True, show only half court (default: True)

    Returns:
        Plotly Figure object with court drawn

    Example:
        >>> fig = draw_nba_court()
        >>> fig.show()
    """
    if fig is None:
        fig = go.Figure()

    dims = get_nba_court_dimensions()

    # Outer boundary
    fig.add_shape(
        type="rect",
        x0=dims['x_min'], y0=dims['y_min'],
        x1=dims['x_max'], y1=dims['y_max'],
        line=dict(color=line_color, width=line_width),
        fillcolor=court_background,
        layer='below'
    )

    # Hoop
    fig.add_shape(
        type="circle",
        x0=-dims['hoop_radius'], y0=-dims['hoop_radius'],
        x1=dims['hoop_radius'], y1=dims['hoop_radius'],
        line=dict(color=line_color, width=line_width),
        fillcolor='rgba(0,0,0,0)',
        layer='below'
    )

    # Backboard
    backboard_half_width = dims['backboard_width'] / 2
    fig.add_shape(
        type="line",
        x0=-backboard_half_width, y0=dims['backboard_y'],
        x1=backboard_half_width, y1=dims['backboard_y'],
        line=dict(color=line_color, width=line_width),
        layer='below'
    )

    # Paint (outer box)
    paint_half_width = dims['paint_width'] / 2
    paint_top = dims['paint_length'] + dims['y_min']
    fig.add_shape(
        type="rect",
        x0=-paint_half_width, y0=dims['y_min'],
        x1=paint_half_width, y1=paint_top,
        line=dict(color=line_color, width=line_width),
        fillcolor='rgba(0,0,0,0)',
        layer='below'
    )

    # Free throw circle (top arc)
    ft_x, ft_y = _generate_arc_points(
        dims['ft_circle_center'][0],
        dims['ft_circle_center'][1],
        dims['ft_circle_radius'],
        0, 180, 50
    )
    fig.add_trace(go.Scatter(
        x=ft_x, y=ft_y,
        mode='lines',
        line=dict(color=line_color, width=line_width),
        showlegend=False,
        hoverinfo='skip'
    ))

    # Free throw circle (bottom arc - dashed)
    ft_x_bottom, ft_y_bottom = _generate_arc_points(
        dims['ft_circle_center'][0],
        dims['ft_circle_center'][1],
        dims['ft_circle_radius'],
        180, 360, 50
    )
    fig.add_trace(go.Scatter(
        x=ft_x_bottom, y=ft_y_bottom,
        mode='lines',
        line=dict(color=line_color, width=line_width, dash='dash'),
        showlegend=False,
        hoverinfo='skip'
    ))

    # Restricted area arc
    restricted_x, restricted_y = _generate_arc_points(
        0, 0,
        dims['restricted_radius'],
        0, 180, 50
    )
    fig.add_trace(go.Scatter(
        x=restricted_x, y=restricted_y,
        mode='lines',
        line=dict(color=line_color, width=line_width),
        showlegend=False,
        hoverinfo='skip'
    ))

    # Three-point line - left corner
    fig.add_shape(
        type="line",
        x0=-dims['three_pt_corner_x'], y0=dims['three_pt_corner_y_start'],
        x1=-dims['three_pt_corner_x'], y1=dims['three_pt_corner_y_end'],
        line=dict(color=line_color, width=line_width),
        layer='below'
    )

    # Three-point line - right corner
    fig.add_shape(
        type="line",
        x0=dims['three_pt_corner_x'], y0=dims['three_pt_corner_y_start'],
        x1=dims['three_pt_corner_x'], y1=dims['three_pt_corner_y_end'],
        line=dict(color=line_color, width=line_width),
        layer='below'
    )

    # Three-point arc
    # Calculate the angle where the arc meets the corners
    corner_angle_rad = np.arcsin(dims['three_pt_corner_x'] / dims['three_pt_arc_radius'])
    corner_angle_deg = np.degrees(corner_angle_rad)

    three_pt_x, three_pt_y = _generate_arc_points(
        0, 0,
        dims['three_pt_arc_radius'],
        corner_angle_deg, 180 - corner_angle_deg, 100
    )
    fig.add_trace(go.Scatter(
        x=three_pt_x, y=three_pt_y,
        mode='lines',
        line=dict(color=line_color, width=line_width),
        showlegend=False,
        hoverinfo='skip'
    ))

    # Configure axes
    fig.update_xaxes(
        range=[dims['x_min'] - 10, dims['x_max'] + 10],
        showgrid=False,
        zeroline=False,
        showticklabels=False,
        scaleanchor='y',
        scaleratio=1
    )

    y_max_display = dims['y_max'] if show_half_court else dims['y_max'] * 2
    fig.update_yaxes(
        range=[dims['y_min'] - 10, y_max_display + 10],
        showgrid=False,
        zeroline=False,
        showticklabels=False
    )

    return fig


def create_court_figure(width: int = 700, height: int = 650,
                        background_color: str = '#1e1e1e',
                        line_color: str = 'white') -> go.Figure:
    """
    Create a standalone court figure with proper layout configuration.

    Args:
        width: Figure width in pixels
        height: Figure height in pixels
        background_color: Background color for the plot
        line_color: Color for court lines

    Returns:
        Configured Plotly Figure with court drawn
    """
    fig = go.Figure()

    # Draw court
    fig = draw_nba_court(
        fig=fig,
        line_color=line_color,
        line_width=2,
        court_background='rgba(0,0,0,0)'
    )

    # Configure layout
    fig.update_layout(
        width=width,
        height=height,
        plot_bgcolor=background_color,
        paper_bgcolor=background_color,
        margin=dict(l=10, r=10, t=30, b=10),
        font=dict(color='white'),
        xaxis=dict(fixedrange=True),
        yaxis=dict(fixedrange=True)
    )

    return fig
