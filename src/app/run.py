"""
NBA Dashboard Application Runner
Loads data from CSV files and initializes the Dash application.
"""

import os
import pandas as pd
from dash import Dash
from src.app.layout import create_layout
from src.app.callbacks import register_callbacks


def create_app():
    """
    Creates and configures the NBA Dashboard Dash application.

    Data Sources:
        - Data/processed/Ready_efficiency_data.csv (offensive/defensive ratings)
        - Data/processed/Ready_tendencies_data.csv (play-style percentages)
        - Data/processed/Ready_shots_data.csv (shot location data)

    Returns:
        Configured Dash app instance
    """
    app = Dash(__name__)

    # --- Path Configuration ---
    current_dir = os.path.dirname(os.path.abspath(__file__))
    root_dir = os.path.abspath(os.path.join(current_dir, "..", ".."))

    # Paths to the three processed CSV files
    players_path = os.path.join(root_dir, 'Data', 'raw', 'allstar_data.csv')
    efficiency_path = os.path.join(root_dir, 'Data', 'processed', 'Ready_efficiency_data.csv')
    tendencies_path = os.path.join(root_dir, 'Data', 'processed', 'Ready_tendencies_data.csv')
    shots_path = os.path.join(root_dir, 'Data', 'processed', 'Ready_shots_data.csv')
    team_vs_opp_path = os.path.join(root_dir, 'Data', 'processed', 'Ready_team_vs_opp_data.csv')

    # --- Data Loading ---
    try:
        df_players = pd.read_csv(players_path)
        df_efficiency = pd.read_csv(efficiency_path)
        df_tendencies = pd.read_csv(tendencies_path)
        df_shots = pd.read_csv(shots_path)
        df_team_vs_opponent = pd.read_csv(team_vs_opp_path)

        print(f"✅ Efficiency data loaded: {len(df_efficiency)} lineups")
        print(f"✅ Tendencies data loaded: {len(df_tendencies)} lineups")
        print(f"✅ Shots data loaded: {len(df_shots)} shots")

        # For player dropdown and profile, use efficiency data as base
        # Add placeholder columns for player profile component
        if 'CURRENT_TEAM' not in df_players.columns:
            df_players['CURRENT_TEAM'] = 'NBA Team'

        for col in ['Height', 'Weight', 'Position']:
            if col not in df_players.columns:
                df_players[col] = "N/A"

        print(f"✅ Setup Complete: Dashboard ready with {df_players['PLAYER'].nunique()} players.")

    except FileNotFoundError as e:
        print(f"❌ Critical Error: Could not find CSV files")
        print(f"   Expected paths:")
        print(f"   - {efficiency_path}")
        print(f"   - {tendencies_path}")
        print(f"   - {shots_path}")
        df_efficiency = pd.DataFrame(columns=['star_player', 'LINEUP_ARCHETYPE'])
        df_tendencies = pd.DataFrame()
        df_shots = pd.DataFrame()

    # Initialize layout with efficiency data (for player selection)
    app.layout = create_layout(app, df_players)

    # Pass all three dataframes to callbacks
    register_callbacks(app, df_efficiency, df_tendencies, df_shots, df_team_vs_opponent)

    return app

if __name__ == '__main__':
    app = create_app()
    print("\n" + "="*60)
    print("🏀 NBA Lineup Strategic Analysis Dashboard")
    print("="*60)
    print("📊 Dashboard running at: http://localhost:8050")
    print("🔄 Debug mode: Enabled")
    print("="*60 + "\n")
    app.run(debug=True, port=8050)