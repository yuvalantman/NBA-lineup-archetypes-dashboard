"""
Load and prepare efficiency data for dashboard.

This module provides utilities for loading lineup efficiency ratings
(offensive rating, defensive rating, net rating).
"""

import pandas as pd
from pathlib import Path


def load_efficiency_data(csv_path='data/processed/luka_efficiency_graph_data.csv'):
    """
    Load lineup efficiency ratings.

    Args:
        csv_path: Path to CSV file with efficiency data

    Returns:
        DataFrame with columns:
        - offensive_rating: Offensive rating (points per 100 possessions)
        - defensive_rating: Defensive rating (points allowed per 100 possessions)
        - net_rating: Net rating (offensive - defensive)
        - player1_archetype, player2_archetype, player3_archetype, player4_archetype
        - star_player (optional)

    Raises:
        FileNotFoundError: If CSV file doesn't exist
    """
    csv_path = Path(csv_path)

    if not csv_path.exists():
        raise FileNotFoundError(f"Efficiency data not found at {csv_path}")

    df = pd.read_csv(csv_path)

    # Validate required columns
    required_cols = ['offensive_rating', 'defensive_rating', 'net_rating']
    missing_cols = [col for col in required_cols if col not in df.columns]

    if missing_cols:
        raise ValueError(f"Missing required columns: {missing_cols}")

    print(f"✓ Loaded efficiency data for {len(df)} lineups")

    return df


def get_efficiency_summary(df: pd.DataFrame) -> dict:
    """
    Get summary statistics for efficiency data.

    Args:
        df: DataFrame with efficiency data

    Returns:
        Dictionary with summary stats:
        - n_lineups: Number of lineups
        - avg_offensive: Average offensive rating
        - avg_defensive: Average defensive rating
        - avg_net: Average net rating
        - best_lineup_idx: Index of lineup with best net rating
        - worst_lineup_idx: Index of lineup with worst net rating
    """
    return {
        'n_lineups': len(df),
        'avg_offensive': df['offensive_rating'].mean(),
        'avg_defensive': df['defensive_rating'].mean(),
        'avg_net': df['net_rating'].mean(),
        'best_lineup_idx': df['net_rating'].idxmax(),
        'worst_lineup_idx': df['net_rating'].idxmin(),
        'median_offensive': df['offensive_rating'].median(),
        'median_defensive': df['defensive_rating'].median()
    }


# Testing functionality
if __name__ == '__main__':
    print("Testing Efficiency Data Loading...\n")

    # Test data loading
    df = load_efficiency_data()

    print(f"\nDataFrame shape: {df.shape}")
    print(f"Columns: {list(df.columns)}\n")

    # Get summary
    summary = get_efficiency_summary(df)

    print("Efficiency Summary:")
    print(f"  Lineups: {summary['n_lineups']}")
    print(f"  Avg Offensive Rating: {summary['avg_offensive']:.1f}")
    print(f"  Avg Defensive Rating: {summary['avg_defensive']:.1f}")
    print(f"  Avg Net Rating: {summary['avg_net']:.1f}")
    print(f"  Median Offensive: {summary['median_offensive']:.1f}")
    print(f"  Median Defensive: {summary['median_defensive']:.1f}")

    print("\nBest Lineup:")
    best = df.iloc[summary['best_lineup_idx']]
    print(f"  Net Rating: {best['net_rating']:.1f}")
    print(f"  Offensive: {best['offensive_rating']:.1f}")
    print(f"  Defensive: {best['defensive_rating']:.1f}")

    print("\nWorst Lineup:")
    worst = df.iloc[summary['worst_lineup_idx']]
    print(f"  Net Rating: {worst['net_rating']:.1f}")
    print(f"  Offensive: {worst['offensive_rating']:.1f}")
    print(f"  Defensive: {worst['defensive_rating']:.1f}")

    print("\n✓ All tests passed!")
