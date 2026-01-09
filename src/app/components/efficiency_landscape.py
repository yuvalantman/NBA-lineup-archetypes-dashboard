"""
Efficiency Landscape Component for NBA Dashboard
Visualizes Offensive vs Defensive ratings for all lineups of a selected player.
"""

import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from plotly.colors import sample_colorscale



def create_efficiency_landscape(df, selected_lineups=None):
    """
    Creates a scatter plot comparing offensive and defensive ratings.

    Features:
        - X-axis: Offensive Rating
        - Y-axis: Defensive Rating (inverted - lower is better)
        - Color: Net Rating
        - Fixed axis ranges to prevent graph movement
        - Highlights selected lineup(s) with cyan border
        - Supports multi-select highlighting

    Args:
        df: DataFrame filtered for a specific player with efficiency data
        selected_lineups: Single lineup name or list of lineup names to highlight

    Returns:
        Plotly figure object
    """
    if df is None or df.empty:
        return go.Figure().update_layout(
            template="plotly_dark",
            paper_bgcolor='rgba(0,0,0,0)'
        )
    # Compute an explicit point color per row (so hover callback can use it)
    vals = df['net_rating'].astype(float)

    # Normalize to [0,1] for colorscale sampling
    vmin, vmax = float(vals.min()), float(vals.max())
    if vmax - vmin < 1e-9:
        t = np.full(len(vals), 0.5)
    else:
        t = (vals - vmin) / (vmax - vmin)

    df = df.copy()
    df['_hover_bg'] = sample_colorscale('RdYlGn', t.tolist())

    # Create scatter plot with custom hover data
    fig = px.scatter(
        df,
        x='offensive_rating',
        y='defensive_rating',
        color='net_rating',
        hover_name='LINEUP_ARCHETYPE',
        # hover_data={
        #     'offensive_rating': ':.2f',
        #     'defensive_rating': ':.2f',
        #     'net_rating': ':.2f'
        # },
        color_continuous_scale='RdYlGn',
        labels={
            'offensive_rating': 'Offensive Rating',
            'defensive_rating': 'Defensive Rating',
            'net_rating': 'Net Rating'
        }
    )
    fig.update_traces(
        customdata=df[['LINEUP_ARCHETYPE', 'offensive_rating', 'defensive_rating', 'net_rating', '_hover_bg']],
        hoverinfo="none",
        hovertemplate=" ",
        marker=dict(size=12),
        selector=dict(mode='markers')
    )
    # Highlight the currently selected lineup(s) with cyan rings
    if selected_lineups:
        # Ensure it's a list for consistent handling
        if not isinstance(selected_lineups, list):
            selected_lineups = [selected_lineups]

        # Highlight all selected lineups
        for lineup in selected_lineups:
            highlight = df[df['LINEUP_ARCHETYPE'] == lineup]
            if not highlight.empty:
                fig.add_trace(go.Scatter(
                    x=highlight['offensive_rating'],
                    y=highlight['defensive_rating'],
                    mode='markers',
                    marker=dict(
                        size=15,
                        color='rgba(0,0,0,0)',
                        line=dict(width=3, color='cyan')
                    ),
                    showlegend=False,
                    hoverinfo='skip'
                ))
    x_min, x_max = df['offensive_rating'].min(), df['offensive_rating'].max()
    y_min, y_max = df['defensive_rating'].min(), df['defensive_rating'].max()

    x_pad = max((x_max - x_min) * 0.1, 2)  # At least 2 points padding
    y_pad = max((y_max - y_min) * 0.1, 2)  # At least 2 points padding
    
    # Update layout with fixed ranges to prevent graph movement
    fig.update_layout(
    template="plotly_dark",
    
    # UI REVISION: This is the "Magic" fix for Dash. 
    # It tells the browser to keep the axis state even when data updates.
    uirevision=f'{x_min}_{x_max}_{y_min}_{y_max}',  # Changes when data changes
    hovermode='closest',

    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    margin=dict(l=10, r=10, t=30, b=10),
    height=350,
    #hoverlabel=dict(font_size=11),

    xaxis=dict(
        title="Offensive Rating",
        range=[x_min - x_pad, x_max + x_pad],
        gridcolor='#2d384d'
    ),
    yaxis=dict(
        title="Defensive Rating",
        range=[y_max + y_pad, y_min - y_pad],    # Inverted: better defense at the top
        gridcolor='#2d384d'
    )

)
    # Remove the scaleanchor to allow independent axis scaling
    # fig.update_yaxes(scaleanchor="x", scaleratio=1)
    fig.add_hline(y=df['defensive_rating'].mean(), line_dash='dot', line_color='rgba(255,255,255,0.3)')
    fig.add_vline(x=df['offensive_rating'].mean(), line_dash='dot', line_color='rgba(255,255,255,0.3)')


    return fig