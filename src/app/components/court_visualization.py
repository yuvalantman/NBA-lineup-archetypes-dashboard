import plotly.graph_objects as go
import numpy as np

def draw_arc_trace(fig, center_x, center_y, radius, start_angle, end_angle, line_color='#555555', line_width=2, dash='solid'):
    """Helper function to draw arcs using scatter traces."""
    # Convert angles to radians
    start_rad = np.radians(start_angle)
    end_rad = np.radians(end_angle)
    
    # Generate points along the arc
    angles = np.linspace(start_rad, end_rad, 100)
    x = center_x + radius * np.cos(angles)
    y = center_y + radius * np.sin(angles)
    
    # Add as scatter trace (mode='lines')
    fig.add_trace(go.Scatter(
        x=x, y=y,
        mode='lines',
        line=dict(color=line_color, width=line_width, dash=dash),
        hoverinfo='skip',
        showlegend=False
    ))

def draw_nba_court(fig, line_color='white', line_width=2):
    """Adds NBA court markings to a Plotly figure."""
    # Outer Boundary
    fig.add_shape(type="rect", x0=-250, y0=-47.5, x1=250, y1=422.5, 
                  line=dict(color=line_color, width=line_width), fillcolor='rgba(0,0,0,0)')
    # Hoop
    fig.add_shape(type="circle", x0=-7.5, y0=-7.5, x1=7.5, y1=7.5, line=dict(color="#FF4500", width=line_width))
    # Backboard
    fig.add_shape(type="line", x0=-30, y0=-7.5, x1=30, y1=-7.5, line=dict(color=line_color, width=line_width))
    # Paint
    fig.add_shape(type="rect", x0=-80, y0=-47.5, x1=80, y1=142.5, line=dict(color=line_color, width=line_width))
    # Inner Paint
    fig.add_shape(type="rect", x0=-60, y0=-47.5, x1=60, y1=142.5, line=dict(color=line_color, width=line_width))
    
    # Free Throw Top Arc: M -60 142.5 A 60 60 0 0 1 60 142.5 (from -60,142.5 to 60,142.5)
    draw_arc_trace(fig, 0, 142.5, 60, 0, 180, line_color=line_color, line_width=line_width)
    
    # Free Throw Bottom Arc (dashed): M -60 142.5 A 60 60 0 0 0 60 142.5
    draw_arc_trace(fig, 0, 142.5, 60, 180, 360, line_color=line_color, line_width=line_width, dash='dash')

    # Restricted Area: M -40 42.5 A 40 40 0 0 1 40 42.5 (from -40,42.5 to 40,42.5)
    draw_arc_trace(fig, 0, 0, 40, 0, 180, line_color=line_color, line_width=line_width)
    # Center Circle Bottom Arc: M -60 422.5 A 60 60 0 0 0 60 422.5
    draw_arc_trace(fig, 0, 422.5, 60, 180, 360, line_color=line_color, line_width=line_width)
    
    # 3-Point Line Arc: M -220 92.5 A 237.5 237.5 0 1 1 220 92.5
    draw_arc_trace(fig, 0, 0, 237.5, 21, 159, line_color=line_color, line_width=line_width)
    
    # Left corner three
    fig.add_shape(type="line", x0=-220, y0=-47.5, x1=-220, y1=92.5, line=dict(color=line_color, width=line_width))
    # Right corner three
    fig.add_shape(type="line", x0=220, y0=-47.5, x1=220, y1=92.5, line=dict(color=line_color, width=line_width))
    return fig