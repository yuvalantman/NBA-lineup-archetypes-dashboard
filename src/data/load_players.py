"""
Load and prepare player data for dashboard.
This module provides utilities for loading All-Star player metadata
including photos and team logos.
"""

import pandas as pd
from pathlib import Path

def load_player_data(csv_path='data/raw/allstar_data.csv'):
    """
    Load all-star player data.
    """
    # Using Path to ensure it works across different OS
    project_root = Path(__file__).parent.parent.parent
    full_path = project_root / csv_path

    if not full_path.exists():
        # Fallback for local testing
        if Path(csv_path).exists():
            full_path = Path(csv_path)
        else:
            raise FileNotFoundError(f"Player data not found at {full_path}")

    df = pd.read_csv(full_path)

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
    try:
        df = load_player_data()
        print(f"\nDataFrame shape: {df.shape}")
        print(f"First 5 players: {df['PLAYER'].head().tolist()}")
        print("\n✓ All tests passed!")
    except Exception as e:
        print(f"× Test failed: {e}")