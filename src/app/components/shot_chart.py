"""
Shot Chart Component for NBA Dashboard
Visualizes shot locations on an NBA court for a specific lineup.
"""

# Set matplotlib backend to non-interactive to avoid threading issues in Dash
import matplotlib
matplotlib.use('Agg')

import plotly.graph_objects as go
import numpy as np
import pandas as pd
from src.app.components.court_visualization import draw_nba_court, draw_arc_trace
from src.data.zone_helpers import create_zone_rect, create_zone_with_arc
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap


def create_polygon_path(corners, closed=True):
    """
    Creates an SVG path string for a polygon zone.
    
    Usage:
        # For rectangular zones, use 4 corners:
        corners = [[-80, 0], [80, 0], [80, 90], [-80, 90]]
        path = create_polygon_path(corners)
        
        # For irregular shapes, add more corners as needed:
        corners = [[-100, 0], [100, 0], [100, 80], [50, 100], [-50, 100], [-100, 80]]
        path = create_polygon_path(corners)
    
    Args:
        corners: List of [x, y] coordinates for polygon corners
        closed: If True, closes the path back to start
        
    Returns:
        SVG path string for use with Plotly add_shape(type="path")
    """
    if not corners or len(corners) < 2:
        return ""
    
    # Start at first corner
    path = f"M {corners[0][0]} {corners[0][1]}"
    
    # Line to each subsequent corner
    for corner in corners[1:]:
        path += f" L {corner[0]} {corner[1]}"
    
    # Close path if requested
    if closed:
        path += " Z"
    
    return path


def create_arc_path(center_x, center_y, radius, start_angle, end_angle, large_arc=False):
    """
    Creates an SVG arc path for curved zones (like restricted area circle or three-point line).
    
    Usage:
        # For restricted area semicircle (0° to 180° at bottom of hoop):
        path = create_arc_path(center_x=0, center_y=0, radius=40, start_angle=0, end_angle=180)
        
        # For three-point arc:
        # Center at (0, -47.5), radius ~237.5, from roughly -45° to 225°
        path = create_arc_path(center_x=0, center_y=-47.5, radius=237.5, start_angle=-45, end_angle=225, large_arc=True)
    
    Args:
        center_x, center_y: Center of the arc
        radius: Radius of the arc
        start_angle: Starting angle in degrees (0° = right, 90° = up)
        end_angle: Ending angle in degrees
        large_arc: If True, draws the larger arc (>180°)
        
    Returns:
        SVG path string for use with Plotly add_shape(type="path")
    """
    import math
    
    # Convert degrees to radians
    start_rad = math.radians(start_angle)
    end_rad = math.radians(end_angle)
    
    # Calculate start and end points
    x1 = center_x + radius * math.cos(start_rad)
    y1 = center_y + radius * math.sin(start_rad)
    x2 = center_x + radius * math.cos(end_rad)
    y2 = center_y + radius * math.sin(end_rad)
    
    # Create arc command
    large_arc_flag = 1 if large_arc else 0
    sweep_flag = 1  # Clockwise
    
    path = f"M {x1} {y1} A {radius} {radius} 0 {large_arc_flag} {sweep_flag} {x2} {y2}"
    
    return path


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




def create_zone_shot_chart(df, height=500):
    """
    Creates a zone-based shot chart with 15 NBA court zones.
    
    Zones are defined by coordinates and matched via the ZONE column in the dataframe.
    
    Args:
        df: DataFrame with shot data (LOC_X, LOC_Y, SHOT_MADE_FLAG, ZONE columns)
        height: Height of the figure in pixels (default: 500)
    
    Returns:
        Plotly figure object with zone-based shot chart
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
    
    # Check if ZONE column exists
    if 'ZONE' not in df.columns:
        # If zone column is missing, return empty court
        fig = go.Figure()
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
    
    # Define the 15 zones using coordinates
    zones = [
        # PAINT ZONES
        {
            'name': 'Restricted Area',
            'shape_type': 'arc',
            'center_point': (0, 0),
            'radius': 40,
            'center_label': [0, 5]
        },
        {
            'name': 'Close Paint',
            **create_zone_with_arc(
                corners=[[-80, -47.5], [80, -47.5], [80, 20], [-80, 20]],
                arc_between=(3, 2),
                arc_center=(0, 0),
                arc_radius=80
            ),
            'center_label': [0, 55]
        },
        {
            'name': 'Far Paint',
            **create_zone_with_arc(
                corners=[[-80, 20], [80, 20], [80, 142.5], [-80, 142.5]],
                arc_between=(0, 1),
                arc_center=(0, 0),
                arc_radius=80
            ),
            'center_label': [0, 110]
        },
        
        # LEFT MID-RANGE
        {
            'name': 'Left Midrange Close',
            'shape_type': 'polygon',
            **create_zone_with_arc(
                corners=[[-160, -47.5], [-80, -47.5], [-80, 92.5], [-160, 92.5]],
                arc_between=None,
                arc_center=None,
                arc_radius=None
            ),
            'center_label': [-120, 30]
        },
        {
            'name': 'Left Midrange Far',
            'shape_type': 'polygon',
            **create_zone_with_arc(
                corners=[[-220, -47.5], [-160, -47.5], [-160, 92.5], [-220, 92.5]],
                arc_between=None,
                arc_center=None,
                arc_radius=None
            ),
            'center_label': [-190, 30]
        },
        
        # CENTER MID-RANGE
        {
            'name': 'Center Midrange',
            **create_zone_with_arc(
                corners=[[-80, 142.5], [80, 142.5], [96, 216], [-96, 216]],
                arc_between=(3, 2),
                arc_center=(0, 0),
                arc_radius=237.5
            ),
            'center_label': [0, 170]
        },
        
        # LEFT/CENTER MID-RANGE BLEND
        {
            'name': 'Left Center Midrange',
            'shape_type': 'polygon',
            **create_zone_with_arc(
                corners=[[-80, 92.5], [-80, 142.5], [-96, 216], [-220, 92.5]],
                arc_between=(3, 2),
                arc_center=(0, 0),
                arc_radius=237.5
            ),
            'center_label': [-150, 140]
        },
        
        # RIGHT/CENTER MID-RANGE BLEND
        {
            'name': 'Right Center Midrange',
            'shape_type': 'polygon',
            **create_zone_with_arc(
                corners=[[80, 92.5], [80, 142.5], [96, 216], [220, 92.5]],
                arc_between=(2, 3),
                arc_center=(0, 0),
                arc_radius=237.5
            ),
            'center_label': [150, 140]
        },
        
        # RIGHT MID-RANGE
        {
            'name': 'Right Midrange Close',
            'shape_type': 'polygon',
            **create_zone_with_arc(
                corners=[[80, -47.5], [160, -47.5], [160, 92.5], [80, 92.5]],
                arc_between=None,
                arc_center=None,
                arc_radius=None
            ),
            'center_label': [120, 30]
        },
        {
            'name': 'Right Midrange Far',
            'shape_type': 'polygon',
            **create_zone_with_arc(
                corners=[[160, -47.5], [220, -47.5], [220, 92.5], [160, 92.5]],
                arc_between=None,
                arc_center=None,
                arc_radius=None
            ),
            'center_label': [190, 30]
        },
        
        # 3-POINT CORNERS
        {
            'name': 'Left Corner 3',
            'shape_type': 'path',
            **create_zone_with_arc(
                corners=[[-250, -47.5], [-220, -47.5], [-220, 92.5], [-250, 92.5]],
                arc_between=None,
                arc_center=None,
                arc_radius=None
            ),
            'center_label': [-235, 20]
        },
        {
            'name': 'Right Corner 3',
            'shape_type': 'path',
            **create_zone_with_arc(
                corners=[[220, -47.5], [250, -47.5], [250, 92.5], [220, 92.5]],
                arc_between=None,
                arc_center=None,
                arc_radius=None
            ),
            'center_label': [235, 20]
        },
        
        # 3-POINT WINGS/ABOVE THE BREAK
        {
            'name': 'Above the Break Left 3',
            'shape_type': 'path',
            **create_zone_with_arc(
                corners=[[-250, 92.5], [-220, 92.5], [-96, 216], [-150, 340], [-250, 340]],
                arc_between=(1, 2),
                arc_center=(0, 0),
                arc_radius=237.5
            ),
            'center_label': [-200, 190]
        },
        {
            'name': 'Above the Break Right 3',
            **create_zone_with_arc(
                corners=[[250, 92.5], [250, 340], [150, 340], [96,216], [220, 92.5]],
                arc_between=(3, 4),
                arc_center=(0, 0),
                arc_radius=237.5
            ),
            'center_label': [200, 190]
        },
        {
            'name': 'Above the Break Center 3',
            'shape_type': 'polygon',
            **create_zone_with_arc(
                corners=[[-96, 216], [96, 216], [150, 340], [-150, 340]],
                arc_between=(0, 1),
                arc_center=(0, 0),
                arc_radius=237.5
            ),
            'center_label': [0, 255]
        },
    ]
    
    # Calculate zone statistics from ZONE column
    total_lineup_shots = len(df)
    zone_stats = {}
    
    for zone in zones:
        zone_name = zone['name']
        
        # Get shots for this zone from the ZONE column
        zone_shots = df[df['ZONE'] == zone_name]
        
        zone_stats[zone_name] = {
            'total_shots': len(zone_shots),
            'made_shots': zone_shots['SHOT_MADE_FLAG'].sum() if len(zone_shots) > 0 else 0,
            'fg_pct': zone_shots['SHOT_MADE_FLAG'].mean() if len(zone_shots) > 0 else 0,
            'tendency': len(zone_shots) / total_lineup_shots if total_lineup_shots > 0 else 0,
            'shape_type': zone.get('shape_type', 'rect'),
            'zone_def': zone,
            'center': zone['center_label']
        }
    
    # Normalize opacity by max tendency (most used zone gets ~80% opacity)
    max_tendency = max([s['tendency'] for s in zone_stats.values()]) if zone_stats else 1
    min_opacity = 0.15
    max_opacity = 0.8
    
    # Create shapes for each zone based on shape_type
    for zone_name, stats in zone_stats.items():
        import math
        
        if stats['total_shots'] == 0:
            # No shots in this zone - minimal opacity
            r, g, b = 241, 140, 0  # Basketball orange
            text_label = 'NA'
            text_color = 'rgba(150, 150, 150, 0.5)'
            opacity = 0.1
        else:
            # All zones orange - use alpha for frequency only
            r, g, b = 241, 140, 0  # Basketball orange
            
            # Normalize opacity: scale tendency by max, so highest usage gets max opacity
            normalized_tendency = stats['tendency'] / max_tendency if max_tendency > 0 else 0
            opacity = min_opacity + normalized_tendency * (max_opacity - min_opacity)
            
            # Color text based on FG%
            fg_pct = stats['fg_pct']
            if fg_pct < 0.33:
                text_color = 'rgba(255, 0, 0, 1)'      # Red for poor FG%
            elif fg_pct < 0.66:
                text_color = 'rgba(255, 255, 0, 1)'    # Yellow for medium FG%
            else:
                text_color = 'rgba(0, 255, 0, 1)'      # Green for good FG%
            
            text_label = f"{fg_pct:.0%}"
        
        color = f'rgba({r}, {g}, {b}, {opacity})'
        center = stats['center']
        shape_type = stats['shape_type']
        zone_def = stats['zone_def']
        
        # Add shape based on type
        if shape_type == 'rect':
            bounds = zone_def['bounds']
            fig.add_shape(
                type="rect",
                x0=bounds['x'][0], y0=bounds['y'][0],
                x1=bounds['x'][1], y1=bounds['y'][1],
                line=dict(color="rgba(150, 150, 150, 0.4)", width=1),
                fillcolor=color,
                layer="below"
            )
        
        elif shape_type == 'polygon':
            corners = zone_def['corners']
            path = create_polygon_path(corners)
            fig.add_shape(
                type="path",
                path=path,
                line=dict(color="rgba(150, 150, 150, 0.4)", width=1),
                fillcolor=color,
                layer="below"
            )
        
        elif shape_type == 'arc':
            # Restricted Area - draw as filled circle using scatter
            cx, cy = zone_def['center_point']
            r = zone_def['radius']
            
            # Create filled circle
            angles = np.linspace(0, np.pi, 50)
            circle_x = cx + r * np.cos(angles)
            circle_y = cy + r * np.sin(angles)
            
            fig.add_trace(go.Scatter(
                x=list(circle_x) + list(circle_x[::-1]),
                y=list(circle_y) + [-y for y in circle_y[::-1]],
                fill='toself',
                fillcolor=color,
                line=dict(color="rgba(150, 150, 150, 0.4)", width=1),
                hoverinfo='skip',
                showlegend=False
            ))
        
        elif shape_type == 'path':
            # Path with arcs - use scatter traces like court visualization
            arc_info = zone_def.get('arc_info', {})
            corners = zone_def.get('corners', [])
            
            if arc_info and corners:
                arc_between = arc_info.get('between', (0, 1))
                arc_center = arc_info.get('center', (0, 0))
                arc_radius = arc_info.get('radius', 80)
                
                i, j = arc_between
                corner_i = corners[i]
                corner_j = corners[j]
                
                # Calculate arc angles using atan2
                angle_i = math.degrees(math.atan2(corner_i[1] - arc_center[1], corner_i[0] - arc_center[0]))
                angle_j = math.degrees(math.atan2(corner_j[1] - arc_center[1], corner_j[0] - arc_center[0]))
                
                # Generate arc points
                arc_angles = np.linspace(np.radians(angle_i), np.radians(angle_j), 30)
                arc_x = arc_center[0] + arc_radius * np.cos(arc_angles)
                arc_y = arc_center[1] + arc_radius * np.sin(arc_angles)
                
                # Build complete polygon: arc + straight segments
                poly_x = list(arc_x)
                poly_y = list(arc_y)
                
                # Add remaining corners in order
                for k in range(j + 1, i + len(corners)):
                    corner_idx = k % len(corners)
                    poly_x.append(corners[corner_idx][0])
                    poly_y.append(corners[corner_idx][1])
                
                # Close the polygon
                poly_x.append(arc_x[0])
                poly_y.append(arc_y[0])
                
                # Add filled polygon using scatter
                fig.add_trace(go.Scatter(
                    x=poly_x,
                    y=poly_y,
                    fill='toself',
                    fillcolor=color,
                    line=dict(color="rgba(150, 150, 150, 0.4)", width=1),
                    hoverinfo='skip',
                    showlegend=False
                ))
            else:
                # Fallback to polygon if arc info is missing
                if corners:
                    polygon_path = create_polygon_path(corners)
                    fig.add_shape(
                        type="path",
                        path=polygon_path,
                        line=dict(color="rgba(150, 150, 150, 0.4)", width=1),
                        fillcolor=color,
                        layer="below"
                    )
        
        # Add text annotation for FG% in zone center
        fig.add_annotation(
            x=center[0],
            y=center[1],
            text=text_label,
            showarrow=False,
            font=dict(size=12, color=text_color, family='monospace'),
            bgcolor='rgba(0, 0, 0, 0.5)',
            bordercolor='rgba(255, 255, 255, 0.3)',
            borderwidth=1,
            borderpad=4
        )
    
    # Add a dummy scatter trace with colorbar for opacity/frequency legend
    fig.add_trace(go.Scatter(
        x=[None], y=[None],
        mode='markers',
        marker=dict(
            colorscale=[
                [0.0, 'rgba(241, 140, 0, 0.15)'],   # Low opacity for low frequency
                [1.0, 'rgba(241, 140, 0, 0.8)']    # High opacity for high frequency
            ],
            cmin=0,
            cmax=1,
            colorbar=dict(
                title=dict(text="Shot<br>Frequency", side="right"),
                len=0.4,
                thickness=15,
                x=1.02,
                tickformat=".0%"
            ),
            showscale=True
        ),
        hoverinfo='skip',
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