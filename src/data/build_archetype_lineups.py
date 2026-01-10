# TODO: replace players with archetypes and group metrics
import pandas as pd
from pathlib import Path
import numpy as np

ROOT = Path(__file__).parent.parent.parent
#ARCHETYPES_PATH = ROOT / "data" / "interim" / "lineups" / "player_archetypes.csv"
#lineups_path = ROOT / "data" / "interim" / "lineups" / "allstar_lineups_data_advanced_with_season.csv"

ALL_STAR_IDS = set([203999, 201939, 201935, 202695, 2544, 1629029, 203507, 1630162, 1626164, 201142, 1628983])
#DF_ARCHETYPES = pd.read_csv(ARCHETYPES_PATH)
#df_lineups = pd.read_csv(lineups_path)


# ============================================================================
# ZONE ASSIGNMENT FUNCTIONS
# ============================================================================

def point_in_circle(px, py, cx, cy, r):
    """Check if point (px, py) is inside circle"""
    return (px - cx) ** 2 + (py - cy) ** 2 <= r ** 2


def point_in_polygon(px, py, corners):
    """Check if point (px, py) is inside polygon using ray casting algorithm"""
    n = len(corners)
    inside = False
    p1x, p1y = corners[0]
    for i in range(1, n + 1):
        p2x, p2y = corners[i % n]
        if py > min(p1y, p2y):
            if py <= max(p1y, p2y):
                if px <= max(p1x, p2x):
                    if p1y != p2y:
                        xinters = (py - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                    if p1x == p2x or px <= xinters:
                        inside = not inside
        p1x, p1y = p2x, p2y
    return inside


def point_in_arc_zone(px, py, corners, arc_between, arc_center, arc_radius):
    """
    Check if point is in a zone with an arc boundary.
    
    For zones with arcs, we check:
    1. Is the point in the polygon formed by the corners?
    2. Is the point within a reasonable distance of the arc boundary?
    
    Arc types:
    - Paint zones (radius 80): arc curves INWARD toward basket, contracts the zone
    - 3-point zones (radius 237.5): arc curves OUTWARD, expands the zone
    
    Args:
        px, py: Point coordinates
        corners: List of corner coordinates (includes all corner points)
        arc_between: (i, j) tuple of corner indices the arc connects
        arc_center: (cx, cy) center of the arc circle
        arc_radius: radius of the arc circle
    
    Returns:
        True if point should be in this zone
    """
    if arc_between is None or arc_center is None or arc_radius is None:
        # No arc, just use polygon
        return point_in_polygon(px, py, corners)
    
    # Get the two corners where the arc is
    i, j = arc_between
    arc_corner_i = corners[i]
    arc_corner_j = corners[j]
    
    # Distance from point to arc center
    dist_to_center = ((px - arc_center[0]) ** 2 + (py - arc_center[1]) ** 2) ** 0.5
    
    import math
    def angle_to_point(ax, ay, cx, cy):
        return math.atan2(ay - cy, ax - cx)
    
    angle_i = angle_to_point(arc_corner_i[0], arc_corner_i[1], arc_center[0], arc_center[1])
    angle_j = angle_to_point(arc_corner_j[0], arc_corner_j[1], arc_center[0], arc_center[1])
    angle_p = angle_to_point(px, py, arc_center[0], arc_center[1])
    
    # Normalize angles to [0, 2π)
    angle_i = angle_i % (2 * math.pi)
    angle_j = angle_j % (2 * math.pi)
    angle_p = angle_p % (2 * math.pi)
    
    # Check if angle_p is between angle_i and angle_j
    if angle_i < angle_j:
        angle_in_range = angle_i <= angle_p <= angle_j
    else:
        angle_in_range = angle_p >= angle_i or angle_p <= angle_j
    
    if arc_radius > 150:
        # 3-point zones - arc bulges outward from basket
        # Point is in zone if:
        # 1. Inside the straight-line polygon, OR
        # 2. Beyond polygon but within arc radius tolerance and correct angle
        
        in_poly = point_in_polygon(px, py, corners)
        if in_poly:
            return True
        
        # Check if point is near the arc (beyond the straight-line polygon)
        if angle_in_range and abs(dist_to_center - arc_radius) < 30:
            return True
        
        return False
    else:
        # Paint zones - arc bulges inward toward basket
        # Point is in zone if:
        # 1. Inside the polygon boundary, AND
        # 2. Beyond the arc (farther from center than arc radius)
        
        in_poly = point_in_polygon(px, py, corners)
        if not in_poly:
            return False
        
        # For paint zone arcs, we want points that are:
        # - In the polygon bounding box, AND
        # - On the correct side of the arc (farther from center than the arc)
        # This prevents points too close to the basket from being in this zone
        # (they should be in Restricted Area instead)
        
        if angle_in_range:
            # Point is in the angular range of the arc
            # Accept it if it's beyond the arc (farther from center)
            # Or close enough to the arc line
            if dist_to_center >= arc_radius - 5:  # Beyond or on the arc
                return True
        
        # For points outside the arc's angular range, just use polygon check
        return in_poly


def get_shot_zone(loc_x, loc_y):
    """
    Determine which zone a shot belongs to based on LOC_X and LOC_Y coordinates.
    
    Properly handles zone boundaries including arc curves for 3-point line and restricted area.
    Restricted Area takes priority over Close Paint.
    Zone checking order matters: simpler zones (corners) checked before complex blended zones.
    
    Args:
        loc_x: X coordinate of shot
        loc_y: Y coordinate of shot
    
    Returns:
        Zone name (str) or None if shot doesn't match any zone
    """
    
    # Define the 15 zones with their exact boundaries including arcs
    # ORDER MATTERS: Check non-arc zones and precise zones first, blended zones last
    zones = [
        # PAINT ZONES
        {
            'name': 'Restricted Area',
            'type': 'circle',
            'center': (0, 0),
            'radius': 40
        },
        {
            'name': 'Close Paint',
            'type': 'arc_zone',
            'corners': [[-80, -47.5], [80, -47.5], [80, 20], [-80, 20]],
            'arc_between': (3, 2),
            'arc_center': (0, 0),
            'arc_radius': 80
        },
        {
            'name': 'Far Paint',
            'type': 'arc_zone',
            'corners': [[-80, 20], [80, 20], [80, 142.5], [-80, 142.5]],
            'arc_between': (0, 1),
            'arc_center': (0, 0),
            'arc_radius': 80
        },
        
        # 3-POINT CORNERS - Check these BEFORE blended zones
        {
            'name': 'Left Corner 3',
            'type': 'polygon',
            'corners': [[-250, -47.5], [-220, -47.5], [-220, 92.5], [-250, 92.5]]
        },
        {
            'name': 'Right Corner 3',
            'type': 'polygon',
            'corners': [[220, -47.5], [250, -47.5], [250, 92.5], [220, 92.5]]
        },
        
        # LEFT MID-RANGE
        {
            'name': 'Left Midrange Close',
            'type': 'polygon',
            'corners': [[-160, -47.5], [-80, -47.5], [-80, 92.5], [-160, 92.5]]
        },
        {
            'name': 'Left Midrange Far',
            'type': 'polygon',
            'corners': [[-220, -47.5], [-160, -47.5], [-160, 92.5], [-220, 92.5]]
        },
        
        # RIGHT MID-RANGE
        {
            'name': 'Right Midrange Close',
            'type': 'polygon',
            'corners': [[80, -47.5], [160, -47.5], [160, 92.5], [80, 92.5]]
        },
        {
            'name': 'Right Midrange Far',
            'type': 'polygon',
            'corners': [[160, -47.5], [220, -47.5], [220, 92.5], [160, 92.5]]
        },
        
        # CENTER MID-RANGE - Arc zone, check before blended zones
        {
            'name': 'Center Midrange',
            'type': 'arc_zone',
            'corners': [[-80, 142.5], [80, 142.5], [96, 216], [-96, 216]],
            'arc_between': (3, 2),
            'arc_center': (0, 0),
            'arc_radius': 237.5
        },
        
        # 3-POINT WINGS/ABOVE THE BREAK - Check these before blended zones
        {
            'name': 'Above the Break Center 3',
            'type': 'arc_zone',
            'corners': [[-96, 216], [96, 216], [150, 340], [-150, 340]],
            'arc_between': (0, 1),
            'arc_center': (0, 0),
            'arc_radius': 237.5
        },
        {
            'name': 'Above the Break Left 3',
            'type': 'arc_zone',
            'corners': [[-250, 92.5], [-220, 92.5], [-96, 216], [-150, 340], [-250, 340]],
            'arc_between': (1, 2),
            'arc_center': (0, 0),
            'arc_radius': 237.5
        },
        {
            'name': 'Above the Break Right 3',
            'type': 'arc_zone',
            'corners': [[250, 92.5], [250, 340], [150, 340], [96, 216], [220, 92.5]],
            'arc_between': (3, 4),
            'arc_center': (0, 0),
            'arc_radius': 237.5
        },
        
        # LEFT/CENTER MID-RANGE BLEND - Check after specific zones
        {
            'name': 'Left Center Midrange',
            'type': 'arc_zone',
            'corners': [[-80, 92.5], [-80, 142.5], [-96, 216], [-220, 92.5]],
            'arc_between': (3, 2),
            'arc_center': (0, 0),
            'arc_radius': 237.5
        },
        
        # RIGHT/CENTER MID-RANGE BLEND - Check after specific zones
        {
            'name': 'Right Center Midrange',
            'type': 'arc_zone',
            'corners': [[80, 92.5], [80, 142.5], [96, 216], [220, 92.5]],
            'arc_between': (2, 3),
            'arc_center': (0, 0),
            'arc_radius': 237.5
        },
    ]
    
    # Check Restricted Area first (takes priority)
    if point_in_circle(loc_x, loc_y, 0, 0, 40):
        return 'Restricted Area'
    
    # Check all other zones in order
    for zone in zones:
        if zone['name'] == 'Restricted Area':
            continue  # Already checked above
        
        if zone['type'] == 'circle':
            if point_in_circle(loc_x, loc_y, zone['center'][0], zone['center'][1], zone['radius']):
                return zone['name']
        
        elif zone['type'] == 'polygon':
            if point_in_polygon(loc_x, loc_y, zone['corners']):
                return zone['name']
        
        elif zone['type'] == 'arc_zone':
            if point_in_arc_zone(loc_x, loc_y, zone['corners'], zone['arc_between'], 
                                zone['arc_center'], zone['arc_radius']):
                return zone['name']
    
    return None


def assign_zones_to_shots(df):
    """
    Add a ZONE column to a shots dataframe by assigning zones based on LOC_X and LOC_Y.
    Also filters out shots outside the court boundaries.
    
    Valid court range: LOC_Y between -47.5 and 340 (baseline to baseline)
    
    Args:
        df: DataFrame with LOC_X and LOC_Y columns
    
    Returns:
        DataFrame with new ZONE column and out-of-bounds shots removed
    """
    df = df.copy()
    
    # Filter out out-of-bounds shots (LOC_Y <= -47.5 or LOC_Y > 340)
    initial_count = len(df)
    df = df[(df['LOC_Y'] > -47.5) & (df['LOC_Y'] <= 340)].copy()
    filtered_count = len(df)
    
    if filtered_count < initial_count:
        print(f"Filtered out {initial_count - filtered_count} out-of-bounds shots")
    
    # Assign zones to remaining shots
    df['ZONE'] = df.apply(lambda row: get_shot_zone(row['LOC_X'], row['LOC_Y']), axis=1)
    return df



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
    df_lineups = df_lineups[df_lineups["MIN"] >= 6]

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
    df_team_vs_opponent_grouped["fg_pct"] = df_team_vs_opponent_grouped["fg_pct"] * 100
    df_team_vs_opponent_grouped["opp_fg_pct"] = df_team_vs_opponent_grouped["opp_fg_pct"] * 100   
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
                            "player4_archetype", "LOC_X", "LOC_Y", "SHOT_MADE_FLAG", "SHOT_DISTANCE", "SHOT_ZONE_BASIC", "SHOT_ZONE_AREA", "SHOT_ZONE_RANGE", "PERIOD"]]
    
    # Add zone column based on shot coordinates
    df_shots = assign_zones_to_shots(df_shots)
    
    return df_shots






