"""
NBA Lineup Tendency Spider/Radar Chart Visualization

Creates interactive 8-axis radar charts showing lineup tendency profiles
with multiple lineup overlays for comparison.
"""

import pandas as pd
import numpy as np
import plotly.graph_objects as go
from typing import List, Optional
from pathlib import Path

# Import data utilities
import sys
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from data.load_tendencies import (
    load_tendency_data,
    normalize_metrics,
    prepare_radar_data,
    get_metric_labels,
    format_metric_value,
    DEFAULT_METRICS
)


# Color palette for lineup overlays (supports up to 5 lineups)
LINEUP_COLORS = [
    {'name': 'Teal', 'line': '#008080', 'fill': 'rgba(0, 128, 128, 0.35)'},
    {'name': 'Cyan', 'line': '#00BFFF', 'fill': 'rgba(0, 191, 255, 0.35)'},
    {'name': 'Orange', 'line': '#FF8C00', 'fill': 'rgba(255, 140, 0, 0.35)'},
    {'name': 'Purple', 'line': '#9370DB', 'fill': 'rgba(147, 112, 219, 0.35)'},
    {'name': 'Lime', 'line': '#32CD32', 'fill': 'rgba(50, 205, 50, 0.35)'},
]


def get_lineup_color(index: int) -> dict:
    """
    Get color configuration for a lineup based on its index.

    Args:
        index: Lineup index (0-based)

    Returns:
        Dictionary with 'name', 'line', and 'fill' color values
    """
    return LINEUP_COLORS[index % len(LINEUP_COLORS)]


def create_hover_template(metric_names: List[str]) -> str:
    """
    Create custom hover template for radar chart points.

    Args:
        metric_names: List of metric column names

    Returns:
        Plotly hover template string
    """
    template = (
        '<b style="font-family: Calibri, sans-serif; font-size: 14px;">%{fullData.name}</b><br>'
        '<b style="font-family: Calibri, sans-serif; font-size: 13px; color: #FF8C00;">%{theta}</b><br>'
        '<span style="font-family: Calibri, sans-serif; font-size: 12px;">Value: <b>%{customdata[0]}</b></span><br>'
        '<span style="font-family: Calibri, sans-serif; font-size: 12px;">Normalized: <b>%{r:.2f}</b></span><br>'
        '<span style="font-family: Calibri, sans-serif; font-size: 12px;">Percentile: <b>%{customdata[1]}th</b></span>'
        '<extra></extra>'
    )
    return template


def create_tendency_radar(
    df: pd.DataFrame,
    selected_lineups: List[int],
    star_player: str = 'Luka Dončić',
    metrics: List[str] = None,
    title: str = None,
    height: int = 300,
    width: int = 450,
    background_color: str = '#1E2833'
) -> go.Figure:
    """
    Create an 8-axis spider/radar chart showing lineup tendencies.

    Args:
        df: DataFrame with normalized metrics (from normalize_metrics())
        selected_lineups: List of lineup indices to display (2-5 recommended)
        star_player: Name of star player for title
        metrics: List of metrics to display (defaults to all 8)
        title: Custom chart title (optional)
        height: Chart height in pixels
        width: Chart width in pixels
        background_color: Background color (hex or rgba)

    Returns:
        Plotly Figure object
    """
    if metrics is None:
        metrics = DEFAULT_METRICS

    # Validate lineup count
    if len(selected_lineups) < 1:
        raise ValueError("Must select at least 1 lineup")
    if len(selected_lineups) > 5:
        print(f"WARNING: {len(selected_lineups)} lineups selected. "
              f"Chart may be crowded. Maximum 5 recommended.")

    # Prepare radar data
    radar_data = prepare_radar_data(df, selected_lineups, metrics)
    metric_labels = radar_data['metric_labels']

    # Create figure
    fig = go.Figure()

    # Add trace for each lineup
    for i, lineup in enumerate(radar_data['lineups']):
        color_config = get_lineup_color(i)

        # Prepare custom data for hover (original values + percentiles)
        customdata = list(zip(
            [format_metric_value(m, v) for m, v in zip(metrics, lineup['original_values'])],
            lineup['percentiles']
        ))

        # Add scatterpolar trace
        fig.add_trace(go.Scatterpolar(
            r=lineup['normalized_values'],
            theta=metric_labels,
            fill='toself',
            fillcolor=color_config['fill'],
            line=dict(
                color=color_config['line'],
                width=2
            ),
            name=f"Lineup {lineup['index'] + 1}",
            hovertemplate=create_hover_template(metrics),
            customdata=customdata,
            text=[lineup['label']] * len(metrics),  # Store lineup composition
        ))

    # Configure layout with basketball-themed hexagonal styling
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 1],
                showticklabels=True,
                ticks='',
                gridcolor='rgba(255, 140, 0, 0.4)',  # Basketball orange for grid
                gridwidth=2,
                linewidth=0,
                tickfont=dict(size=11, color='white', family='Calibri'),
                tickvals=[0, 0.25, 0.5, 0.75, 1.0],
                ticktext=['0%', '25%', '50%', '75%', '100%']
            ),
            angularaxis=dict(
                tickfont=dict(size=13, color='white', family='Calibri', weight='bold'),
                linecolor='rgba(255, 140, 0, 0.5)',  # Basketball orange lines
                gridcolor='rgba(255, 140, 0, 0.3)',  # Basketball orange grid
                gridwidth=2,
                rotation=90,  # Start at top
                direction='clockwise'
            ),
            bgcolor='rgba(34, 34, 34, 0.3)'  # Dark court-like background
        ),
        title=dict(
            text=title or f'<b>{star_player} - Lineup Tendency Profiles</b>',
            font=dict(size=20, color='#008080', family='Calibri'),
            x=0.5,
            xanchor='center',
            y=0.98,
            yanchor='top'
        ),
        showlegend=True,
        legend=dict(
            font=dict(color='white', size=10, family='Calibri'),
            bgcolor='rgba(0, 0, 0, 0.6)',
            bordercolor='#008080',
            borderwidth=1,
            orientation='h',
            x=0.5,
            y=1.15,
            xanchor='center',
            yanchor='top'
        ),
        height=height,
        width=width,
        paper_bgcolor=background_color,
        plot_bgcolor=background_color,
        font=dict(color='white', family='Calibri'),
        margin=dict(l=60, r=60, t=80, b=60),
        hoverlabel=dict(
            bgcolor='rgba(30, 30, 30, 0.95)',
            bordercolor='rgba(255, 140, 0, 0.8)',  # Basketball orange border
            font_size=13,
            font_color='white',
            font_family='Calibri'
        )
    )

    return fig


def create_empty_figure(message: str = "No data to display",
                       background_color: str = '#1E2833') -> go.Figure:
    """
    Create an empty figure with a message.

    Args:
        message: Message to display
        background_color: Background color

    Returns:
        Empty Plotly figure
    """
    fig = go.Figure()

    fig.add_annotation(
        text=message,
        xref="paper",
        yref="paper",
        x=0.5,
        y=0.5,
        showarrow=False,
        font=dict(size=16, color='white')
    )

    fig.update_layout(
        height=700,
        width=700,
        paper_bgcolor=background_color,
        plot_bgcolor=background_color,
        xaxis=dict(visible=False),
        yaxis=dict(visible=False)
    )

    return fig


# Standalone testing and HTML generation
if __name__ == '__main__':
    print("="*60)
    print("NBA Lineup Tendency Radar Chart - Standalone Test")
    print("="*60)

    # Load and prepare data
    print("\nLoading data...")
    csv_path = 'tendency_graph/luka_team_tendencies_graph_data.csv'
    df = load_tendency_data(csv_path)
    df = normalize_metrics(df)

    print(f"✓ Loaded and normalized data for {len(df)} lineups\n")

    # Test 1: Two lineups (minimum comparison)
    print("-" * 60)
    print("Test 1: Two-Lineup Comparison")
    print("-" * 60)
    fig = create_tendency_radar(
        df,
        selected_lineups=[0, 10],
        title="Luka Dončić - Comparing 2 Lineups"
    )
    output_file = 'test_two_lineups.html'
    fig.write_html(output_file)
    print(f"✓ Saved to: {output_file}\n")

    # Test 2: Three lineups (recommended)
    print("-" * 60)
    print("Test 2: Three-Lineup Comparison (Recommended)")
    print("-" * 60)
    fig = create_tendency_radar(
        df,
        selected_lineups=[0, 10, 20],
        title="Luka Dončić - Comparing 3 Lineups"
    )
    output_file = 'test_three_lineups.html'
    fig.write_html(output_file)
    print(f"✓ Saved to: {output_file}\n")

    # Test 3: Five lineups (maximum overlays)
    print("-" * 60)
    print("Test 3: Five-Lineup Comparison (Maximum)")
    print("-" * 60)
    fig = create_tendency_radar(
        df,
        selected_lineups=[0, 5, 10, 15, 20],
        title="Luka Dončić - Comparing 5 Lineups"
    )
    output_file = 'test_five_lineups.html'
    fig.write_html(output_file)
    print(f"✓ Saved to: {output_file}\n")

    # Test 4: Default visualization (first 3 lineups)
    print("-" * 60)
    print("Test 4: Default Visualization")
    print("-" * 60)
    fig = create_tendency_radar(
        df,
        selected_lineups=[0, 1, 2]
    )
    output_file = 'luka_tendencies_radar.html'
    fig.write_html(output_file)
    print(f"✓ Saved to: {output_file}\n")

    print("="*60)
    print("TEST SUMMARY")
    print("="*60)
    print("✓ All tests completed successfully!")
    print("\nGenerated HTML files:")
    print("  1. test_two_lineups.html - 2 lineup comparison")
    print("  2. test_three_lineups.html - 3 lineup comparison (recommended)")
    print("  3. test_five_lineups.html - 5 lineup comparison (maximum)")
    print("  4. luka_tendencies_radar.html - default visualization")
    print("\nOpen any HTML file in your browser to view the interactive radar chart!")
    print("\nWhat to check:")
    print("  ✓ 8-axis octagonal shape")
    print("  ✓ Multiple colored polygon overlays")
    print("  ✓ Hover shows lineup composition + exact values")
    print("  ✓ Legend allows toggling lineups on/off")
    print("  ✓ Dark theme with teal/cyan accents")
    print("="*60)
