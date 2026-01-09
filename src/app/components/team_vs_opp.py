"""
Team VS Opponent Comparison Component.
Visualizes performance metrics for the selected lineup vs their opponents side-by-side.
"""

import pandas as pd
import plotly.graph_objects as go
from dash import dcc, html

# def create_team_vs_opp_chart(df=None, selected_lineup_index=None, height=350):
#     """
#     Generates a horizontal grouped bar chart for the layout.
#     Matches the function name imported in layout.py.
#     """
#     # Create an empty figure if no data is provided (for initial load)
#     if df is None or df.empty or selected_lineup_index is None:
#         fig = go.Figure()
#         fig.add_annotation(
#             text="Select a lineup to view comparison",
#             xref="paper", yref="paper", x=0.5, y=0.5, showarrow=False,
#             font=dict(size=14, color='white')
#         )
#         fig.update_layout(
#             paper_bgcolor='rgba(0,0,0,0)',
#             plot_bgcolor='rgba(0,0,0,0)',
#             xaxis=dict(visible=False),
#             yaxis=dict(visible=False),
#             height=height
#         )
#         return fig

#     # Access the specific lineup row
#     try:
#         row = df.iloc[selected_lineup_index]
#     except (IndexError, TypeError):
#         row = df.iloc[0]

#     # Metrics Mapping (Metric Label, Lineup Column, Opponent Column)
#     metrics_map = [
#         ('FG%', 'fg_pct', 'opp_fg_pct'),
#         ('FTA', 'fta', 'opp_fta'),
#         ('Assists', 'ast', 'opp_ast'),
#         ('Off. Reb', 'oreb', 'opp_oreb'),
#         ('Def. Reb', 'dreb', 'opp_dreb'),
#         ('Turnovers', 'tov', 'opp_tov'),
#         ('Steals', 'stl', 'opp_stl'),
#         ('Blocks', 'blk', 'opp_blk'),
#         ('Fouls', 'pf', 'opp_pf')
#     ]

#     categories = [m[0] for m in metrics_map]
#     lineup_vals = [row[m[1]] for m in metrics_map]
#     opp_vals = [row[m[2]] for m in metrics_map]

#     # Helper to format text on bars
#     def format_val(v, label):
#         if 'FG%' in label: return f"{v:.1%}"
#         return f"{v:.1f}"

#     fig = go.Figure()

#     # Team (Lineup) Trace - Teal/Blue
#     fig.add_trace(go.Bar(
#         name='Lineup',
#         y=categories,
#         x=lineup_vals,
#         orientation='h',
#         marker_color='#00BFFF',
#         text=[format_val(v, categories[i]) for i, v in enumerate(lineup_vals)],
#         textposition='outside',
#         cliponaxis=False
#     ))

#     # Opponent Trace - Tomato Red
#     fig.add_trace(go.Bar(
#         name='Opponent',
#         y=categories,
#         x=opp_vals,
#         orientation='h',
#         marker_color='#FF6347', 
#         text=[format_val(v, categories[i]) for i, v in enumerate(opp_vals)],
#         textposition='outside',
#         cliponaxis=False
#     ))

#     fig.update_layout(
#         template="plotly_dark",
#         barmode='group',
#         margin=dict(l=100, r=40, t=20, b=40),
#         paper_bgcolor='rgba(0,0,0,0)',
#         plot_bgcolor='rgba(0,0,0,0)',
#         legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
#         xaxis=dict(
#             title="Value (Per 48 Min)",
#             showgrid=True,
#             gridcolor='rgba(255,255,255,0.05)',
#             zeroline=False
#         ),
#         yaxis=dict(
#             autorange="reversed", # Keeps FG% at the top
#             showgrid=False
#         ),
#         font=dict(family="Calibri", size=12),
#         height=height,
#         bargap=0.2,
#         bargroupgap=0.1
#     )

#     return fig

import plotly.graph_objects as go

def create_team_vs_opp_chart(df=None, lineup_key=None, height=350):
    """
    Dumbbell chart comparing lineup vs opponent metrics.
    lineup_key should identify the selected archetype lineup.
    """

    if df is None or df.empty or lineup_key is None:
        fig = go.Figure()
        fig.add_annotation(
            text="Select a lineup to view matchup comparison",
            xref="paper", yref="paper",
            x=0.5, y=0.5,
            showarrow=False,
            font=dict(size=14, color='white')
        )
        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(visible=False),
            yaxis=dict(visible=False),
            height=height
        )
        return fig

    row = df[df["LINEUP_ARCHETYPE"] == lineup_key]
    if row.empty:
        return go.Figure()

    row = row.iloc[0]

    metrics = [
        # ('FG%', 'fg_pct', 'opp_fg_pct'),
        ('FTA', 'fta', 'opp_fta'),
        ('Assists', 'ast', 'opp_ast'),
        ('Off Reb', 'oreb', 'opp_oreb'),
        ('Def Reb', 'dreb', 'opp_dreb'),
        ('Turnovers', 'tov', 'opp_tov'),
        ('Steals', 'stl', 'opp_stl'),
        ('Blocks', 'blk', 'opp_blk'),
        ('Fouls', 'pf', 'opp_pf')
    ]

    labels = [m[0] for m in metrics]
    lineup_vals = [row[m[1]] for m in metrics]
    opp_vals = [row[m[2]] for m in metrics]

    fig = go.Figure()

    # connecting lines
    for i, label in enumerate(labels):
        fig.add_trace(go.Scatter(
            x=[opp_vals[i], lineup_vals[i]],
            y=[label, label],
            mode='lines',
            line=dict(color='rgba(255,255,255,0.4)', width=3),
            hoverinfo='skip',
            showlegend=False
        ))

    # opponent dots
    fig.add_trace(go.Scatter(
        x=opp_vals,
        y=labels,
        mode='markers',
        name='Opponent',
        marker=dict(
            size=11,
            color='#FF6347',
            symbol='triangle-up'
        )
    ))

    # lineup dots
    fig.add_trace(go.Scatter(
        x=lineup_vals,
        y=labels,
        mode='markers',
        name='Lineup',
        marker=dict(
            size=10,
            color='#00BFFF',
            symbol='circle'
        )
    ))

    fig.update_layout(
        template="plotly_dark",
        height=height,
        margin=dict(l=110, r=40, t=20, b=50),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(
            title="Per 48 Minutes",
            gridcolor='rgba(255,255,255,0.05)',
            zeroline=False
        ),
        yaxis=dict(
            autorange="reversed"
        ),
        legend=dict(
            orientation="h",
            yanchor="top",
            y=-0.2,
            xanchor="center",
            x=0.5
        )
    )

    return fig
