"""
Efficiency Landscape Component for NBA Dashboard
Visualizes Offensive vs Defensive ratings for all lineups of a selected player.
"""

import plotly.express as px
import plotly.graph_objects as go


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

    # Create scatter plot with custom hover data
    fig = px.scatter(
        df,
        x='offensive_rating',
        y='defensive_rating',
        color='net_rating',
        hover_name='LINEUP_ARCHETYPE',
        hover_data={
            'offensive_rating': ':.2f',
            'defensive_rating': ':.2f',
            'net_rating': ':.2f'
        },
        color_continuous_scale='RdYlGn',
        labels={
            'offensive_rating': 'Offensive Rating',
            'defensive_rating': 'Defensive Rating',
            'net_rating': 'Net Rating'
        }
    )
    fig.update_traces(marker=dict(size=12), selector=dict(mode='markers'))
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

    # Update layout with fixed ranges to prevent graph movement
    fig.update_layout(
    template="plotly_dark",
    
    # UI REVISION: This is the "Magic" fix for Dash. 
    # It tells the browser to keep the axis state even when data updates.
    uirevision='constant_value', 

    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    margin=dict(l=10, r=10, t=30, b=10),
    height=350,
    hoverlabel=dict(font_size=11),

    xaxis=dict(
        title="Offensive Rating",
        range=[70, 143],   # Keep this fixed
        fixedrange=True,    # Disables zoom/pan
        gridcolor='#2d384d'
    ),
    yaxis=dict(
        title="Defensive Rating",
        range=[143, 70],    # Inverted: better defense at the top
        autorange=False,    # Stops automatic scaling
        fixedrange=True,    # Disables zoom/pan
        gridcolor='#2d384d'
    )

)
    fig.update_yaxes(scaleanchor="x", scaleratio=1)
    fig.add_hline(y=df['defensive_rating'].mean(), line_dash='dot', line_color='rgba(255,255,255,0.3)')
    fig.add_vline(x=df['offensive_rating'].mean(), line_dash='dot', line_color='rgba(255,255,255,0.3)')


    return fig