# TODO: replace players with archetypes and group metrics
import pandas as pd
from pathlib import Path

ROOT = Path(__file__).parent.parent.parent
#ARCHETYPES_PATH = ROOT / "data" / "interim" / "lineups" / "player_archetypes.csv"
#lineups_path = ROOT / "data" / "interim" / "lineups" / "allstar_lineups_data_advanced_with_season.csv"

ALL_STAR_IDS = set([203999, 201939, 201935, 202695, 2544, 1629029, 203507, 1630162, 1626164, 201142, 1628983])
#DF_ARCHETYPES = pd.read_csv(ARCHETYPES_PATH)
#df_lineups = pd.read_csv(lineups_path)



def weighted_mean(df, value_col, weight_col):
    return (df[value_col] * df[weight_col]).sum() / df[weight_col].sum()

def parse_group_ids(group_id: str) -> list[int]:
    return [int(pid) for pid in group_id.split("-")]

def process_lineup_row(row, all_star_ids, archetype_map, player_name_map):
    season = row["SEASON"]
    group_id = row["GROUP_ID"]
    group_name = row.get("GROUP_NAME", None)

    players = parse_group_ids(group_id)

    # which all-stars are in this lineup
    stars_in_lineup = [pid for pid in players if pid in all_star_ids]

    output_rows = []

    for star_id in stars_in_lineup:
        other_players = [pid for pid in players if pid != star_id]

        # map other players to archetypes
        archetypes = []
        for pid in other_players:
            key = (pid, season)
            if key not in archetype_map:
                archetypes = None
                break
            archetypes.append(archetype_map[key])

        if archetypes is None:
            continue  # skip incomplete mappings

        lineup_archetype = "-".join(sorted(archetypes))

        output_rows.append({
            "ALL_STAR_ID": star_id,
            "ALL_STAR_NAME": player_name_map.get(star_id),
            "GROUP_ID": group_id,
            "GROUP_NAME": group_name,
            "LINEUP_ARCHETYPE": lineup_archetype,
            "SEASON":season
        })

    return output_rows



def build_archetype_lineups(df_archetypes: pd.DataFrame, df_lineups: pd.DataFrame) -> pd.DataFrame:
    archetype_map = (
        df_archetypes
        .set_index(["PLAYER_ID", "SEASON"])["FINAL_ARCHETYPE"]
        .to_dict()
    )
    player_name_map = (
        df_archetypes
        .drop_duplicates("PLAYER_ID")
        .set_index("PLAYER_ID")["PLAYER"]
        .to_dict()
    )
    rows = []
    df_lineups = df_lineups[df_lineups["MIN"] >= 4]

    for _, row in df_lineups.iterrows():
        rows.extend(
            process_lineup_row(
                row,
                ALL_STAR_IDS,
                archetype_map,
                player_name_map
            )
        )

    df_archetype_lineups = pd.DataFrame(rows)
    return df_archetype_lineups

# df_archetype_lineups = build_archetype_lineups()
# df_archetype_lineups.to_csv(ROOT / "data" / "processed" / "archetype_lineups.csv", index=False)


def build_efficiency_df(df_archetype_lineups: pd.DataFrame, df_lineups=pd.DataFrame):
    df_efficiency = df_archetype_lineups.merge(
        df_lineups[["SEASON", "GROUP_ID", "GROUP_NAME", "MIN",
                    "OFF_RATING", "DEF_RATING", "NET_RATING"]],
        on=["SEASON", "GROUP_ID"],
        how="left"
    )

    df_efficiency["_weighted_off_rating"] = df_efficiency["MIN"] * df_efficiency["OFF_RATING"]
    df_efficiency["_weighted_def_rating"] = df_efficiency["MIN"] * df_efficiency["DEF_RATING"]
    df_efficiency["_weighted_net_rating"] = df_efficiency["MIN"] * df_efficiency["NET_RATING"]
    
    df_efficiency_grouped = (
        df_efficiency
        .groupby(["ALL_STAR_ID", "LINEUP_ARCHETYPE"], as_index=False)
        .agg(
            ALL_STAR_NAME=("ALL_STAR_NAME", "first"),
            off_weighted_sum=("_weighted_off_rating", "sum"),
            def_weighted_sum=("_weighted_def_rating", "sum"),
            net_weighted_sum=("_weighted_net_rating", "sum"),
            min_sum=("MIN", "sum")
        )
    )
    df_efficiency_grouped["offensive_rating"] = (
        df_efficiency_grouped["off_weighted_sum"] /
        df_efficiency_grouped["min_sum"]
    )

    df_efficiency_grouped["defensive_rating"] = (
        df_efficiency_grouped["def_weighted_sum"] /
        df_efficiency_grouped["min_sum"]
    )

    df_efficiency_grouped["net_rating"] = (
        df_efficiency_grouped["net_weighted_sum"] /
        df_efficiency_grouped["min_sum"]
    )


    df_efficiency_grouped.drop(columns=["off_weighted_sum", "def_weighted_sum",
                                        "net_weighted_sum"], inplace=True)
    df_efficiency_grouped[["player1_archetype", "player2_archetype", "player3_archetype",
                            "player4_archetype"]] = df_efficiency_grouped["LINEUP_ARCHETYPE"].str.split("-", expand=True)
    #df_efficiency_grouped.drop(columns=["LINEUP_ARCHETYPE"], inplace=True)
    df_efficiency_grouped.rename(columns={"ALL_STAR_NAME": "star_player"}, inplace=True)
    df_efficiency_grouped.drop(columns=["ALL_STAR_ID"], inplace=True)
    df_efficiency_grouped = df_efficiency_grouped[["star_player", "LINEUP_ARCHETYPE", "player1_archetype", "player2_archetype",
                                                    "player3_archetype", "player4_archetype", "offensive_rating",
                                                    "defensive_rating", "net_rating", "min_sum"]]
    df_efficiency_grouped.sort_values(by=["star_player","min_sum"], ascending=[True, False], inplace=True)

    # df_efficiency_final = df_efficiency_grouped.merge(
    #     df_scores_lineups[["star_player","LINEUP_ARCHETYPE", "SCORE"]],
    #     on=["star_player", "LINEUP_ARCHETYPE"],
    #     how="left"
    # )
    # df_efficiency_top = (
    #     df_efficiency_final
    #     .sort_values("SCORE", ascending=False)
    #     .groupby(["star_player"], as_index=False, group_keys=False)
    #     .head(15)
    # )
    return df_efficiency_grouped

# df_efficiency = build_efficiency_df()
# df_efficiency.to_csv(ROOT / "data" / "processed" / "allstar_efficiency_graph_data.csv", index=False)

def build_tendencies_df(df_archetype_lineups: pd.DataFrame, df_scoring=pd.DataFrame, df_advanced=pd.DataFrame) -> pd.DataFrame:
    df_tendencies = df_archetype_lineups.merge(
        df_scoring[["SEASON", "GROUP_ID", "GROUP_NAME",
                    "PCT_PTS_3PT", "PCT_PTS_PAINT", "PCT_PTS_FB",
                    "PCT_PTS_2PT_MR", "PCT_AST_FGM", "PCT_UAST_FGM"]],
        on=["SEASON", "GROUP_ID"],
        how="left"
    ).merge(
        df_advanced[["SEASON", "GROUP_ID","EFG_PCT", "TS_PCT", "MIN"]],
        on=["SEASON", "GROUP_ID"],
        how="left"
    )

    df_tendencies_grouped = (
        df_tendencies
        .groupby(["ALL_STAR_ID", "LINEUP_ARCHETYPE"], as_index=False)
        .apply(lambda g: pd.Series({
            "star_player": g["ALL_STAR_NAME"].iloc[0],
            "min_sum": g["MIN"].sum(),

            "pct_pts_3pt": weighted_mean(g, "PCT_PTS_3PT", "MIN"),
            "pct_pts_paint": weighted_mean(g, "PCT_PTS_PAINT", "MIN"),
            "pct_pts_fb": weighted_mean(g, "PCT_PTS_FB", "MIN"),
            "pct_pts_2pt_mr": weighted_mean(g, "PCT_PTS_2PT_MR", "MIN"),
            "pct_ast_fgm": weighted_mean(g, "PCT_AST_FGM", "MIN"),
            "pct_uast_fgm": weighted_mean(g, "PCT_UAST_FGM", "MIN"),
            "efg_pct": weighted_mean(g, "EFG_PCT", "MIN"),
            "ts_pct": weighted_mean(g, "TS_PCT", "MIN"),
        }))
        .reset_index(drop=True)
    )

    #df_tendencies_grouped.drop(columns=["MIN"], inplace=True)
    df_tendencies_grouped[["player1_archetype", "player2_archetype", "player3_archetype",
                            "player4_archetype"]] = df_tendencies_grouped["LINEUP_ARCHETYPE"].str.split("-", expand=True)
    #df_tendencies_grouped.rename(columns={"ALL_STAR_NAME": "star_player"}, inplace=True)
    #df_tendencies_grouped.drop(columns=["ALL_STAR_ID"], inplace=True)
    df_tendencies_grouped = df_tendencies_grouped[["star_player", "LINEUP_ARCHETYPE", "player1_archetype", "player2_archetype",
                                                    "player3_archetype", "player4_archetype", "pct_pts_3pt",
                                                    "pct_pts_paint", "pct_pts_fb", "pct_pts_2pt_mr",
                                                    "pct_ast_fgm", "pct_uast_fgm", "efg_pct", "ts_pct", "min_sum"]]
    df_tendencies_grouped.sort_values(by=["star_player","min_sum"], ascending=[True, False], inplace=True)
    return df_tendencies_grouped

def build_team_vs_opponent_df(df_archetype_lineups: pd.DataFrame, df_opponent=pd.DataFrame, df_base=pd.DataFrame) -> pd.DataFrame:
    df_team_vs_opponent = df_archetype_lineups.merge(
        df_base[["SEASON", "GROUP_ID", "GROUP_NAME", "MIN",
                    "FG_PCT", "FTA", "AST", "OREB", "DREB", "TOV", "STL", "BLK", "PFD", "PF"]],
        on=["SEASON", "GROUP_ID"],
        how="left"
    ).merge(
        df_opponent[["SEASON", "GROUP_ID", "OPP_FG_PCT", "OPP_FTA", "OPP_AST", "OPP_OREB", "OPP_DREB",
                    "OPP_TOV", "OPP_STL", "OPP_BLK", "OPP_PFD", "OPP_PF"]],
        on=["SEASON", "GROUP_ID"],
        how="left"
    )
    df_team_vs_opponent_grouped = (
        df_team_vs_opponent
        .groupby(["ALL_STAR_ID", "LINEUP_ARCHETYPE"], as_index=False)
        .apply(lambda g: pd.Series({
            "star_player": g["ALL_STAR_NAME"].iloc[0],
            "min_sum": g["MIN"].sum(),

            "fg_pct": weighted_mean(g, "FG_PCT", "MIN"),
            "fta": weighted_mean(g, "FTA", "MIN"),
            "ast": weighted_mean(g, "AST", "MIN"),
            "oreb": weighted_mean(g, "OREB", "MIN"),
            "dreb": weighted_mean(g, "DREB", "MIN"),
            "tov": weighted_mean(g, "TOV", "MIN"),
            "stl": weighted_mean(g, "STL", "MIN"),
            "blk": weighted_mean(g, "BLK", "MIN"),
            "pfd": weighted_mean(g, "PFD", "MIN"),
            "pf": weighted_mean(g, "PF", "MIN"),

            "opp_fg_pct": weighted_mean(g, "OPP_FG_PCT", "MIN"),
            "opp_fta": weighted_mean(g, "OPP_FTA", "MIN"),
            "opp_ast": weighted_mean(g, "OPP_AST", "MIN"),
            "opp_oreb": weighted_mean(g, "OPP_OREB", "MIN"),
            "opp_dreb": weighted_mean(g, "OPP_DREB", "MIN"),
            "opp_tov": weighted_mean(g, "OPP_TOV", "MIN"),
            "opp_stl": weighted_mean(g, "OPP_STL", "MIN"),
            "opp_blk": weighted_mean(g, "OPP_BLK", "MIN"),
            "opp_pfd": weighted_mean(g, "OPP_PFD", "MIN"),
            "opp_pf": weighted_mean(g, "OPP_PF", "MIN"),
        }))
        .reset_index(drop=True)
    )

    #df_team_vs_opponent_grouped.drop(columns=["MIN"], inplace=True)
    df_team_vs_opponent_grouped[["player1_archetype", "player2_archetype", "player3_archetype",
                            "player4_archetype"]] = df_team_vs_opponent_grouped["LINEUP_ARCHETYPE"].str.split("-", expand=True)
    #df_team_vs_opponent_grouped.rename(columns={"ALL_STAR_NAME": "star_player"}, inplace=True)
    #df_team_vs_opponent_grouped.drop(columns=["ALL_STAR_ID"], inplace=True)
    df_team_vs_opponent_grouped = df_team_vs_opponent_grouped[["star_player", "LINEUP_ARCHETYPE", "player1_archetype",
                                                                "player2_archetype", "player3_archetype",
                                                                "player4_archetype", "fg_pct",
                                                                "opp_fg_pct", "fta", "opp_fta", "ast", "opp_ast",
                                                                "oreb", "opp_oreb", "dreb", "opp_dreb", "tov",
                                                                "opp_tov", "stl", "opp_stl", "blk", "opp_blk",
                                                                "pf", "opp_pf", "min_sum"]]
    df_team_vs_opponent_grouped.sort_values(by=["star_player","min_sum"], ascending=[True, False], inplace=True)
    return df_team_vs_opponent_grouped

def build_shots_df(df_archetype_lineups: pd.DataFrame, df_full_shots=pd.DataFrame) -> pd.DataFrame:
    df_full_shots.rename(columns={"lineup_id":"GROUP_ID"}, inplace=True)
    df_shots = df_full_shots.merge(
        df_archetype_lineups[["GROUP_ID", "SEASON", "ALL_STAR_ID", "ALL_STAR_NAME", "LINEUP_ARCHETYPE"]],
        on=["GROUP_ID", "SEASON"],
        how= "inner"
    )
    #df_shots.dropna(subset = ["LINEUP_ARCHETYPE"], reset_index=True)
    df_shots[["player1_archetype", "player2_archetype", "player3_archetype",
                            "player4_archetype"]] = df_shots["LINEUP_ARCHETYPE"].str.split("-", expand=True)
    df_shots.rename(columns={"ALL_STAR_NAME" : "star_player"}, inplace = True)
    df_shots = df_shots[["star_player", "LINEUP_ARCHETYPE", "player1_archetype", "player2_archetype", "player3_archetype",
                            "player4_archetype", "LOC_X", "LOC_Y", "SHOT_MADE_FLAG", "SHOT_DISTANCE", "PERIOD"]]
    return df_shots






