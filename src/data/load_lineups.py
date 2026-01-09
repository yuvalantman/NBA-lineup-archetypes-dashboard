# TODO: load lineup-level data
import pandas as pd
from pathlib import Path
import build_archetype_lineups
import lineup_score

ROOT = Path(__file__).parent.parent.parent

def load_lineups_data():
    df_player_archetypes = pd.read_csv(ROOT / "data" / "interim" / "lineups" / "player_archetypes.csv")
    df_advanced = pd.read_csv(ROOT / "data" / "interim" / "lineups" / "allstar_lineups_data_advanced_with_season.csv")
    df_base = pd.read_csv(ROOT / "data" / "interim" / "lineups" / "allstar_lineups_data_base_with_season.csv")
    df_scoring = pd.read_csv(ROOT / "data" / "interim" / "lineups" / "allstar_lineups_data_scoring_with_season.csv")
    df_misc = pd.read_csv(ROOT / "data" / "interim" / "lineups" / "allstar_lineups_data_misc_with_season.csv")
    df_opponent = pd.read_csv(ROOT / "data" / "interim" / "lineups" / "allstar_lineups_data_opponent_with_season.csv")
    df_full_shots = pd.read_csv(ROOT / "data" / "interim" / "lineups" / "shots_with_lineups_full.csv")
    
    df_archetype_lineups = build_archetype_lineups.build_archetype_lineups(df_player_archetypes, df_advanced)
    
    df_efficiency = build_archetype_lineups.build_efficiency_df(df_archetype_lineups, df_advanced)
    df_tendencies = build_archetype_lineups.build_tendencies_df(df_archetype_lineups, df_scoring, df_advanced)
    df_team_vs_opponent = build_archetype_lineups.build_team_vs_opponent_df(df_archetype_lineups, df_opponent, df_base)
    df_shots = build_archetype_lineups.build_shots_df(df_archetype_lineups, df_full_shots)
    
    df_efficiency.to_csv(ROOT / "data" / "processed" / "try" / "allstar_efficiency_graph_data.csv", index=False)
    df_tendencies.to_csv(ROOT / "data" / "processed" / "try" / "allstar_tendencies_graph_data.csv", index=False)
    df_team_vs_opponent.to_csv(ROOT / "data" / "processed" / "try" / "allstar_team_vs_opponent_graph_data.csv", index=False)
    df_shots.to_csv(ROOT / "data" / "processed" / "try"/ "allstar_shots_data.csv")

    df_scores_lineups = lineup_score.lineups_scores(df_archetype_lineups, df_efficiency, df_tendencies, df_team_vs_opponent)
    top15 = (
        df_scores_lineups
        .groupby("star_player", as_index=False, group_keys=False)
        .head(15)
    )
    df_efficiency = df_efficiency.round(2)
    df_tendencies = df_tendencies.round(2)
    df_team_vs_opponent = df_team_vs_opponent.round(2)
    
    top15 = top15[["star_player", "LINEUP_ARCHETYPE"]]
    return {
        "lineups": df_scores_lineups,
        "efficiency": df_efficiency.merge(top15),
        "shots": df_shots.merge(top15),
        "tendencies": df_tendencies.merge(top15),
        "team_vs_opp": df_team_vs_opponent.merge(top15),
    }


dashboard_tables = load_lineups_data()

dashboard_tables["lineups"].to_csv(ROOT / "data" / "processed" / "Archetype_lineups_with_scores_data.csv")
dashboard_tables["efficiency"].to_csv(ROOT / "data" / "processed" / "Ready_efficiency_data.csv")
dashboard_tables["shots"].to_csv(ROOT / "data" / "processed" / "Ready_shots_data.csv")
dashboard_tables["tendencies"].to_csv(ROOT / "data" / "processed" / "Ready_tendencies_data.csv")
dashboard_tables["team_vs_opp"].to_csv(ROOT / "data" / "processed" / "Ready_team_vs_opp_data.csv")