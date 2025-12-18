import pandas as pd
import logging

# Paths as per your requirements
PATH_BIO = 'data/processed/allstar_data.csv'
PATH_EFF = 'data/processed/luka_efficiency_graph_data.csv'
PATH_METRICS = 'data/processed/luka_metrics_graph_data.csv'
PATH_TENDENCIES = 'data/processed/luka_team_tendencies_graph_data.csv'


def get_player_bio():
    """Loads player physical and team data for the info card."""
    try:
        df = pd.read_csv(PATH_BIO)
        # Required fields: PLAYER, Height, Weight, Position, CURRENT_TEAM
        df.columns = [c.upper() for c in df.columns]
        return df.iloc[0]  # Returns the star player's data
    except Exception as e:
        logging.error(f"Error loading Bio: {e}")
        return None


def get_lineup_efficiency():
    """Loads offensive/defensive ratings and creates the combination string."""
    try:
        df = pd.read_csv(PATH_EFF)
        df.columns = [c.lower() for c in df.columns]

        # Combine Star + 4 Archetypes for the legend
        arch_cols = ['star_player', 'player1_archetype', 'player2_archetype',
                     'player3_archetype', 'player4_archetype']

        df['lineup_id'] = range(len(df))
        df['combination'] = df[arch_cols].apply(
            lambda x: ' | '.join(x.values.astype(str)), axis=1
        )
        return df
    except Exception as e:
        logging.error(f"Error loading Efficiency: {e}")
        return pd.DataFrame()


def get_lineup_metrics():
    """Loads pace, turnovers, assists, rebounds, blocks, and steals."""
    try:
        df = pd.read_csv(PATH_METRICS)
        df.columns = [c.lower() for c in df.columns]
        return df
    except Exception as e:
        logging.error(f"Error loading Metrics: {e}")
        return pd.DataFrame()


def get_lineup_tendencies():
    """Loads additional team playstyle data (FTA, 3PA, Points in Paint, etc.)."""
    try:
        df = pd.read_csv(PATH_TENDENCIES)
        df.columns = [c.lower() for c in df.columns]
        return df
    except Exception as e:
        logging.error(f"Error loading Tendencies: {e}")
        return pd.DataFrame()