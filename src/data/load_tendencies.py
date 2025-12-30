"""
NBA Lineup Tendency Data Loading and Normalization

This module provides utilities for loading and processing lineup tendency data
for spider/radar chart visualizations.
"""

import pandas as pd
import numpy as np
from typing import List, Dict
from pathlib import Path


# Metric configuration with display names
METRIC_CONFIG = {
    'fta_per48': {
        'label': 'FTA/48',
        'description': 'Free Throw Attempts per 48 min',
        'format': '{:.1f}'
    },
    'three_pa_per48': {
        'label': '3PA/48',
        'description': '3-Point Attempts per 48 min',
        'format': '{:.1f}'
    },
    'points_off_turnovers': {
        'label': 'Points Off TO',
        'description': 'Points from Turnovers',
        'format': '{:.1f}'
    },
    'second_chance_points': {
        'label': '2nd Chance Pts',
        'description': 'Second Chance Points',
        'format': '{:.1f}'
    },
    'points_in_paint': {
        'label': 'Paint Points',
        'description': 'Points in the Paint',
        'format': '{:.1f}'
    },
    'pct_midrange_points': {
        'label': 'Midrange %',
        'description': '% Points from Midrange',
        'format': '{:.1%}'
    },
    'pct_unassisted_points': {
        'label': 'Unassisted %',
        'description': '% Unassisted Points',
        'format': '{:.1%}'
    },
    'pct_fastbreak_points': {
        'label': 'Fastbreak %',
        'description': '% Fastbreak Points',
        'format': '{:.1%}'
    }
}

# Default metrics list (all 8)
DEFAULT_METRICS = list(METRIC_CONFIG.keys())


def load_tendency_data(csv_path: str) -> pd.DataFrame:
    """
    Load lineup tendency data from CSV file.

    Args:
        csv_path: Path to CSV file containing tendency data

    Returns:
        DataFrame with lineup data and metrics

    Raises:
        FileNotFoundError: If CSV file doesn't exist
        ValueError: If required columns are missing
    """
    csv_path = Path(csv_path)

    if not csv_path.exists():
        raise FileNotFoundError(f"CSV file not found: {csv_path}")

    # Load data
    df = pd.read_csv(csv_path)

    # Validate required columns
    required_cols = ['star_player', 'player1_archetype', 'player2_archetype',
                     'player3_archetype', 'player4_archetype']
    required_cols.extend(DEFAULT_METRICS)

    missing_cols = [col for col in required_cols if col not in df.columns]
    if missing_cols:
        raise ValueError(f"Missing required columns: {missing_cols}")

    print(f"✓ Loaded {len(df)} lineups from {csv_path.name}")

    return df


def normalize_metrics(df: pd.DataFrame, metrics: List[str] = None) -> pd.DataFrame:
    """
    Normalize metrics to 0-1 scale using min-max scaling.

    For each metric:
    - 0 = worst value in the dataset
    - 1 = best value in the dataset
    - 0.5 = midpoint

    Args:
        df: DataFrame with raw metric values
        metrics: List of metric column names to normalize (defaults to all)

    Returns:
        DataFrame with added {metric}_norm columns
    """
    if metrics is None:
        metrics = DEFAULT_METRICS

    df_normalized = df.copy()

    for metric in metrics:
        if metric not in df.columns:
            print(f"WARNING: Metric '{metric}' not found in DataFrame, skipping")
            continue

        values = df[metric].values
        min_val = values.min()
        max_val = values.max()

        # Handle edge case: all values identical
        if max_val == min_val:
            df_normalized[f'{metric}_norm'] = 0.5
            print(f"WARNING: All values identical for '{metric}', set to 0.5")
        else:
            # Min-max normalization
            df_normalized[f'{metric}_norm'] = (values - min_val) / (max_val - min_val)

    return df_normalized


def create_lineup_label(row: pd.Series, include_star: bool = False) -> str:
    """
    Format lineup composition as a readable string.

    Args:
        row: DataFrame row with archetype columns
        include_star: If True, include star player name

    Returns:
        Formatted lineup string
    """
    archetypes = [
        row['player1_archetype'],
        row['player2_archetype'],
        row['player3_archetype'],
        row['player4_archetype']
    ]

    lineup_str = ', '.join(archetypes)

    if include_star and 'star_player' in row.index:
        lineup_str = f"{row['star_player']}: {lineup_str}"

    return lineup_str


def get_metric_labels() -> Dict[str, str]:
    """
    Get mapping of metric column names to display labels.

    Returns:
        Dictionary mapping column names to short labels
    """
    return {metric: config['label'] for metric, config in METRIC_CONFIG.items()}


def get_metric_descriptions() -> Dict[str, str]:
    """
    Get mapping of metric column names to full descriptions.

    Returns:
        Dictionary mapping column names to descriptions
    """
    return {metric: config['description'] for metric, config in METRIC_CONFIG.items()}


def calculate_percentile(df: pd.DataFrame, metric: str, value: float) -> int:
    """
    Calculate what percentile a value represents within the dataset.

    Args:
        df: DataFrame with metric values
        metric: Column name of the metric
        value: Value to calculate percentile for

    Returns:
        Percentile rank (1-100)
    """
    if metric not in df.columns:
        return 50  # Default to median if metric not found

    # Count how many values are less than or equal to this value
    rank = (df[metric] <= value).sum()

    # Convert to percentile (1-100)
    percentile = int((rank / len(df)) * 100)

    return percentile


def format_metric_value(metric: str, value: float) -> str:
    """
    Format metric value according to its type.

    Args:
        metric: Metric column name
        value: Raw value to format

    Returns:
        Formatted string representation
    """
    if metric not in METRIC_CONFIG:
        return f"{value:.2f}"

    format_str = METRIC_CONFIG[metric]['format']
    return format_str.format(value)


def prepare_radar_data(df: pd.DataFrame, lineup_indices: List[int],
                       metrics: List[str] = None) -> Dict:
    """
    Prepare data structure for radar chart visualization.

    Args:
        df: DataFrame with normalized metrics
        lineup_indices: List of lineup row indices to include
        metrics: List of metrics to include (defaults to all)

    Returns:
        Dictionary with radar chart data:
        {
            'lineups': [
                {
                    'index': 0,
                    'label': 'Rim_Protector, Post_Scorer, ...',
                    'normalized_values': [0.5, 0.8, ...],
                    'original_values': [18.4, 37.6, ...],
                    'percentiles': [60, 85, ...]
                },
                ...
            ],
            'metric_labels': ['FTA/48', '3PA/48', ...],
            'metric_names': ['fta_per48', 'three_pa_per48', ...]
        }
    """
    if metrics is None:
        metrics = DEFAULT_METRICS

    # Ensure metrics are normalized
    norm_cols = [f'{m}_norm' for m in metrics]
    if not all(col in df.columns for col in norm_cols):
        raise ValueError("DataFrame must have normalized metric columns. Call normalize_metrics() first.")

    radar_data = {
        'lineups': [],
        'metric_labels': [get_metric_labels()[m] for m in metrics],
        'metric_names': metrics
    }

    for idx in lineup_indices:
        if idx < 0 or idx >= len(df):
            print(f"WARNING: Lineup index {idx} out of range, skipping")
            continue

        row = df.iloc[idx]

        lineup_data = {
            'index': idx,
            'label': create_lineup_label(row),
            'normalized_values': [row[f'{m}_norm'] for m in metrics],
            'original_values': [row[m] for m in metrics],
            'percentiles': [calculate_percentile(df, m, row[m]) for m in metrics]
        }

        radar_data['lineups'].append(lineup_data)

    return radar_data


# Testing functionality
if __name__ == '__main__':
    print("Testing Lineup Tendency Data Loading...\n")

    # Test data loading
    csv_path = 'tendency_graph/luka_team_tendencies_graph_data.csv'
    df = load_tendency_data(csv_path)

    print(f"\nDataFrame shape: {df.shape}")
    print(f"Columns: {list(df.columns)}\n")

    # Test normalization
    df = normalize_metrics(df)
    print("\n✓ Metrics normalized")

    # Test lineup labeling
    print("\nFirst 5 lineup labels:")
    for i in range(5):
        label = create_lineup_label(df.iloc[i])
        print(f"  {i+1}. {label}")

    # Test metric labels
    print("\nMetric labels:")
    for metric, label in get_metric_labels().items():
        print(f"  {metric:30} → {label}")

    # Test percentile calculation
    print("\nPercentile examples for first lineup:")
    row = df.iloc[0]
    for metric in DEFAULT_METRICS[:3]:
        value = row[metric]
        percentile = calculate_percentile(df, metric, value)
        formatted = format_metric_value(metric, value)
        print(f"  {metric}: {formatted} (Rank: {percentile}th percentile)")

    # Test radar data preparation
    print("\n" + "="*60)
    print("Testing radar data preparation...")
    radar_data = prepare_radar_data(df, [0, 5, 10])
    print(f"✓ Prepared data for {len(radar_data['lineups'])} lineups")
    print(f"  Metrics: {radar_data['metric_labels']}")
    print(f"  First lineup: {radar_data['lineups'][0]['label']}")

    print("\n✓ All tests passed!")
