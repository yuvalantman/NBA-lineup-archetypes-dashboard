"""
Shot Chart Component for NBA Dashboard
Visualizes shot locations on an NBA court for a specific lineup.
"""

import plotly.graph_objects as go
from src.app.components.court_visualization import draw_nba_court


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
            range=[-250, 250]
        ),
        yaxis=dict(
            visible=False,
            range=[-47.5, 422.5],
            scaleanchor="x"
        ),
        margin=dict(l=5, r=5, t=5, b=5)
    )

    return fig
