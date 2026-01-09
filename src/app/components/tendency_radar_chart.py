"""
Tendency Radar Chart Component for NBA Dashboard
Visualizes play-style tendencies using a radar chart with percentage metrics.
"""

import plotly.graph_objects as go


def create_tendency_radar(row):
    """
    Creates a radar chart showing lineup play-style tendencies.

    Features:
        - Fixed radial axis range [0, 100] to prevent jumping
        - Shows 5 key metrics as percentages
        - Normalized data display

    Args:
        row: Single row (Series or dict) containing tendency data for one lineup

    Returns:
        Plotly figure object
    """
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
