import plotly.graph_objects as go

def draw_nba_court(fig, line_color='#555555', line_width=2):
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
    # 3-Point Line
    fig.add_shape(type="path", path="M -220 92.5 A 237.5 237.5 0 0 1 220 92.5", line=dict(color=line_color, width=line_width))
    fig.add_shape(type="line", x0=-220, y0=-47.5, x1=-220, y1=92.5, line=dict(color=line_color, width=line_width))
    fig.add_shape(type="line", x0=220, y0=-47.5, x1=220, y1=92.5, line=dict(color=line_color, width=line_width))
    return fig