"""
Efficiency Landscape Component for Dashboard Integration

Scatter plot showing offensive vs defensive rating for lineup comparisons.
Driven by external lineup selection (no internal dropdown).
"""

import sys
from pathlib import Path
import pandas as pd
import plotly.graph_objects as go
from dash import dcc, html, Input, Output


def create_efficiency_component(
    df_efficiency: pd.DataFrame,
    component_id: str = 'efficiency',
    star_player: str = 'Luka Dončić',
    height: int = 400,
    width: int = None,
    card_color: str = '#2A3642',
    accent_color: str = '#008080',
    border_color: str = '#00BFFF'
) -> html.Div:
    """
    Create efficiency landscape component (no internal selector).

    Args:
        df_efficiency: DataFrame with efficiency data
        component_id: Unique ID prefix for component elements
        star_player: Star player name for title
        height: Chart height in pixels
        width: Chart width in pixels (None = auto)
        card_color: Background color for card
        accent_color: Accent color for title
        border_color: Border color

    Returns:
        Dash html.Div containing efficiency landscape graph
    """
    return html.Div(
        style={
            'backgroundColor': card_color,
            'padding': '15px',
            'borderRadius': '8px',
            'border': f'1px solid {border_color}'
        },
        children=[
            html.H3(
                "Efficiency Landscape",
                style={
                    'color': accent_color,
                    'marginTop': 0,
                    'marginBottom': '15px',
                    'fontSize': '18px',
                    'textAlign': 'center'
                }
            ),
            dcc.Graph(
                id=f'{component_id}-graph',
                config={'displayModeBar': True, 'displaylogo': False},
                style={'height': f'{height}px'} if width is None else {'height': f'{height}px', 'width': f'{width}px'}
            )
        ]
    )


def create_efficiency_figure(
    df,
    selected_indices,
    star_player='Luka Dončić',
    height=400,
    dark_theme=True
):
    """
    Create efficiency landscape figure.

    Args:
        df: DataFrame with efficiency data (all lineups)
        selected_indices: List of lineup indices to highlight
        star_player: Star player name
        height: Figure height in pixels
        dark_theme: Use dark theme styling

    Returns:
        Plotly figure
    """
    # Filter to selected lineups
    if not selected_indices:
        # Show all lineups grayed out if none selected
        df_selected = df.copy()
        df_selected['selected'] = False
    else:
        df_selected = df.iloc[selected_indices].copy()
        df_selected['selected'] = True

    # Create lineup labels
    df_selected['lineup_label'] = df_selected.apply(
        lambda row: f"{row['player1_archetype']}, {row['player2_archetype']}, "
                    f"{row['player3_archetype']}, {row['player4_archetype']}",
        axis=1
    )

    # Calculate reference values (using all data, not just selected)
    avg_offensive = df['offensive_rating'].median()
    avg_defensive = df['defensive_rating'].median()

    # Calculate fixed axis ranges from ALL data (not just selected)
    off_min, off_max = df['offensive_rating'].min(), df['offensive_rating'].max()
    def_min, def_max = df['defensive_rating'].min(), df['defensive_rating'].max()

    # Add 5% padding
    off_padding = (off_max - off_min) * 0.05
    def_padding = (def_max - def_min) * 0.05

    x_range = [off_min - off_padding, off_max + off_padding]
    y_range = [def_min - def_padding, def_max + def_padding]

    # Create hover text
    df_selected['hover_text'] = df_selected.apply(
        lambda row: (
            f"<b style='font-family: Calibri; font-size: 13px;'>{star_player}</b><br>"
            f"<b style='font-family: Calibri; font-size: 12px; color: #FF8C00;'>Archetypes:</b><br>"
            f"<span style='font-family: Calibri; font-size: 11px;'>{row['lineup_label']}</span><br><br>"
            f"<b style='font-family: Calibri; font-size: 12px;'>Offensive Rating:</b> {row['offensive_rating']:.1f}<br>"
            f"<b style='font-family: Calibri; font-size: 12px;'>Defensive Rating:</b> {row['defensive_rating']:.1f}<br>"
            f"<b style='font-family: Calibri; font-size: 12px;'>Net Rating:</b> {row['net_rating']:.1f}"
        ),
        axis=1
    )

    # Create figure
    fig = go.Figure()

    # Theme colors
    if dark_theme:
        bg_color = 'rgba(0,0,0,0)'
        font_color = 'white'
        grid_color = 'rgba(255,255,255,0.1)'
        line_color = 'rgba(255,255,255,0.3)'
    else:
        bg_color = 'white'
        font_color = 'black'
        grid_color = 'lightgray'
        line_color = 'gray'

    # Add reference lines (median values)
    fig.add_vline(
        x=avg_offensive,
        line_dash="dash",
        line_color=line_color,
        opacity=0.6,
        line_width=2,
        annotation_text="Median O",
        annotation_position="top",
        annotation_font_color=font_color,
        annotation_font_size=10
    )

    fig.add_hline(
        y=avg_defensive,
        line_dash="dash",
        line_color=line_color,
        opacity=0.6,
        line_width=2,
        annotation_text="Median D",
        annotation_position="right",
        annotation_font_color=font_color,
        annotation_font_size=10
    )

    # Add scatter points
    fig.add_trace(go.Scatter(
        x=df_selected['offensive_rating'],
        y=df_selected['defensive_rating'],
        mode='markers',
        marker=dict(
            size=14,
            color=df_selected['net_rating'],
            colorscale='RdYlGn',  # Red-Yellow-Green
            showscale=True,
            colorbar=dict(
                title=dict(
                    text="Net<br>Rating",
                    font=dict(color=font_color, family='Calibri', size=11)
                ),
                thickness=15,
                len=0.75,
                tickfont=dict(color=font_color, family='Calibri', size=10),
                x=1.02,
                bgcolor='rgba(0,0,0,0.3)',
                yanchor='middle',
                y=0.5
            ),
            line=dict(width=2, color='white'),
            opacity=0.9
        ),
        text=df_selected['hover_text'],
        hovertemplate='%{text}<extra></extra>',
        name=''
    ))

    # Add quadrant annotations
    x_span = df['offensive_rating'].max() - df['offensive_rating'].min()
    y_span = df['defensive_rating'].max() - df['defensive_rating'].min()

    annotations = [
        # Elite quadrant (top-right: good offense, good defense)
        dict(
            x=avg_offensive + x_span * 0.3,
            y=avg_defensive - y_span * 0.3,
            text="<b>ELITE</b>",
            showarrow=False,
            font=dict(size=11, color='#4CAF50', family='Calibri', weight='bold'),
            opacity=0.6,
            bgcolor='rgba(76, 175, 80, 0.15)',
            borderpad=6,
            bordercolor='#4CAF50',
            borderwidth=1
        ),
        # Weak quadrant (bottom-left: poor offense, poor defense)
        dict(
            x=avg_offensive - x_span * 0.3,
            y=avg_defensive + y_span * 0.3,
            text="<b>WEAK</b>",
            showarrow=False,
            font=dict(size=11, color='#F44336', family='Calibri', weight='bold'),
            opacity=0.6,
            bgcolor='rgba(244, 67, 54, 0.15)',
            borderpad=6,
            bordercolor='#F44336',
            borderwidth=1
        ),
    ]

    # Update layout
    fig.update_layout(
        title=dict(
            text=f"<b>{star_player}</b> - Efficiency Landscape",
            x=0.5,
            xanchor='center',
            font=dict(size=16, color='#008080', family='Calibri'),
            y=0.98,
            yanchor='top'
        ),
        xaxis=dict(
            title="<b>Offensive Rating</b> (higher = better)",
            showgrid=True,
            gridcolor=grid_color,
            gridwidth=0.5,
            zeroline=False,
            range=x_range,
            title_font=dict(size=11, color=font_color, family='Calibri'),
            tickfont=dict(color=font_color, family='Calibri', size=10)
        ),
        yaxis=dict(
            title="<b>Defensive Rating</b> (lower = better)",
            showgrid=True,
            gridcolor=grid_color,
            gridwidth=0.5,
            zeroline=False,
            range=[y_range[1], y_range[0]],
            title_font=dict(size=11, color=font_color, family='Calibri'),
            tickfont=dict(color=font_color, family='Calibri', size=10)
        ),
        annotations=annotations,
        plot_bgcolor=bg_color,
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color=font_color, family='Calibri'),
        height=height,
        hovermode='closest',
        showlegend=False,
        margin=dict(l=60, r=80, t=50, b=60),
        hoverlabel=dict(
            bgcolor='rgba(30, 30, 30, 0.95)',
            bordercolor='rgba(255, 140, 0, 0.8)',
            font_size=12,
            font_color='white',
            font_family='Calibri'
        )
    )

    return fig


def register_efficiency_callbacks(
    app,
    df_efficiency,
    lineup_checklist_id: str,
    component_id='efficiency',
    star_player='Luka Dončić'
):
    """
    Register callbacks for efficiency landscape component.

    Args:
        app: Dash app instance
        df_efficiency: DataFrame with efficiency data
        lineup_checklist_id: ID of external lineup checklist to listen to
        component_id: Component ID prefix (must match component creation)
        star_player: Star player name
    """

    @app.callback(
        Output(f'{component_id}-graph', 'figure'),
        Input(lineup_checklist_id, 'value')
    )
    def update_efficiency_landscape(selected_lineups):
        """Update efficiency landscape when lineup selection changes."""
        # Validate input
        if not selected_lineups:
            selected_lineups = []

        # Create and return figure
        fig = create_efficiency_figure(
            df=df_efficiency,
            selected_indices=selected_lineups,
            star_player=star_player,
            height=400,
            dark_theme=True
        )

        return fig


# Example usage documentation
INTEGRATION_EXAMPLE = """
# How to integrate into your main dashboard:

## Step 1: Import in your layout file (src/app/__init__.py)

from src.data.load_efficiency import load_efficiency_data
from src.app.components.efficiency_landscape import (
    create_efficiency_component,
    register_efficiency_callbacks
)

# Load data
df_efficiency = load_efficiency_data('data/processed/luka_efficiency_graph_data.csv')

## Step 2: Add to your layout

layout = html.Div([
    # ... lineup checklist somewhere ...
    dcc.Checklist(
        id='lineup-comparison-checklist',
        options=[...],
        value=[0, 10, 20]
    ),

    # ... efficiency component ...
    create_efficiency_component(
        df_efficiency=df_efficiency,
        component_id='efficiency',
        height=400
    ),
])

## Step 3: Register callbacks

register_efficiency_callbacks(
    app,
    df_efficiency=df_efficiency,
    lineup_checklist_id='lineup-comparison-checklist',  # External checklist ID
    component_id='efficiency',
    star_player='Luka Dončić'
)

## Done!
The efficiency landscape will update when lineup checklist changes.
"""

if __name__ == '__main__':
    print("="*60)
    print("Efficiency Landscape Component - Integration Guide")
    print("="*60)
    print(INTEGRATION_EXAMPLE)
