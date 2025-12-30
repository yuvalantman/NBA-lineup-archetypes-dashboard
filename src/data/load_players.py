<<<<<<< HEAD
"""
Load and prepare player data for dashboard.

This module provides utilities for loading All-Star player metadata
including photos and team logos.
"""

import pandas as pd
from pathlib import Path


def load_player_data(csv_path='star_graph_data/allstar_data.csv'):
    """
    Load all-star player data.

    Args:
        csv_path: Path to CSV file with player metadata

    Returns:
        DataFrame with columns:
        - PLAYER: Player name
        - Height: Player height
        - Weight: Player weight
        - Position: Player position
        - CURRENT_TEAM: Team name

    Raises:
        FileNotFoundError: If CSV file doesn't exist
    """
    csv_path = Path(csv_path)

    if not csv_path.exists():
        raise FileNotFoundError(f"Player data not found at {csv_path}")

    df = pd.read_csv(csv_path)

    # Validate required columns
    required_cols = ['PLAYER', 'Height', 'Weight', 'Position', 'CURRENT_TEAM']
    missing_cols = [col for col in required_cols if col not in df.columns]

    if missing_cols:
        raise ValueError(f"Missing required columns: {missing_cols}")

    print(f"✓ Loaded {len(df)} players")

    return df


# Testing functionality
if __name__ == '__main__':
    print("Testing Player Data Loading...\n")

    # Test data loading
    df = load_player_data()

    print(f"\nDataFrame shape: {df.shape}")
    print(f"Columns: {list(df.columns)}\n")

    print("First 5 players:")
    for i in range(min(5, len(df))):
        row = df.iloc[i]
        print(f"  {i+1}. {row['PLAYER']} - {row['Position']} - {row['CURRENT_TEAM']}")

    print("\n✓ All tests passed!")
=======
# TODO: load player-season data from data/raw
def load_player_data():
    pass
>>>>>>> 35217567569a3e4a4d5abe233313123ba3bbeed6
