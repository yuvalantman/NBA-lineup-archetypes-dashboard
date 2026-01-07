# lineup_score.py
import numpy as np
import pandas as pd

# -----------------------------
# Helpers
# -----------------------------
def zscore_per_star(df, col):
    return (
        df.groupby("star_player")[col]
        .transform(lambda x: (x - x.mean()) / (x.std(ddof=0) + 1e-6))
    )

# -----------------------------
# Main
# -----------------------------
def lineups_scores(
    df_archetype_lineups,
    df_efficiency,
    df_tendencies,
    df_team_vs_opponent
):
    # ------------------------------------------------
    # 1. Merge all lineup-level info
    # ------------------------------------------------
    df = (
        df_efficiency
        .merge(df_tendencies, on=["star_player", "LINEUP_ARCHETYPE"], how="left")
        .merge(df_team_vs_opponent, on=["star_player", "LINEUP_ARCHETYPE"], how="left")
    )
    MIN_THRESH = 55
    df = df[df["min_sum"] >= MIN_THRESH].copy()

    # ------------------------------------------------
    # 2. Normalize PER STAR PLAYER
    # ------------------------------------------------
    EFF_COLS = ["net_rating", "offensive_rating", "defensive_rating"]
    STYLE_COLS = [
        "pct_pts_3pt", "pct_pts_paint", "pct_pts_fb",
        "pct_pts_2pt_mr", "pct_ast_fgm", "pct_uast_fgm", "efg_pct", "ts_pct"
    ]
    DEF_COLS = [
        ("fg_pct", "opp_fg_pct"),
        ("ast", "opp_ast"),
        ("oreb", "opp_oreb"),
        ("dreb", "opp_dreb"),
        ("tov", "opp_tov"),
        ("stl", "opp_stl"),
        ("blk", "opp_blk"),
        ("pf", "opp_pf"),
    ]

    for c in EFF_COLS + STYLE_COLS:
        df[c + "_Z"] = zscore_per_star(df, c)

    # defensive deltas (team - opponent)
    for team_col, opp_col in DEF_COLS:
        delta = df[team_col] - df[opp_col]
        df[f"{team_col}_DELTA_Z"] = zscore_per_star(
            df.assign(_delta=delta), "_delta"
        )

    # ------------------------------------------------
    # 3. Scores
    # ------------------------------------------------
    df["EFF_SCORE"] = (
        0.7 * df["net_rating_Z"]
        + 0.5 * df["offensive_rating_Z"]
        - 0.2 * df["defensive_rating_Z"]
    )

    df["STYLE_SCORE"] = (
        0.25 * df["efg_pct_Z"]
        + 0.1 * df["pct_ast_fgm_Z"]
        + 0.1 * df["pct_uast_fgm_Z"]
        + 0.15 * df["ts_pct_Z"]
        + 0.1 * df["pct_pts_3pt_Z"]
        + 0.1 * df["pct_pts_paint_Z"]
        + 0.1 * df["pct_pts_fb_Z"]
        + 0.1 * df["pct_pts_2pt_mr_Z"]
    )

    df["DEF_SCORE"] = (
        - 0.25 * df["tov_DELTA_Z"]
        + 0.5 * df["stl_DELTA_Z"]
        + 0.5 * df["dreb_DELTA_Z"]
        + 0.5 * df["blk_DELTA_Z"]
        - 0.25 * df["pf_DELTA_Z"]
    )

    # ------------------------------------------------
    # 4. Minutes confidence (anti-noise)
    # ------------------------------------------------
    df["MIN_CONF"] = (
        np.log1p(df["min_sum"]) /
        np.log1p(df.groupby("star_player")["min_sum"].transform("max"))
    ) ** 1.35

    # ------------------------------------------------
    # 5. Final score
    # ------------------------------------------------
    df["QUALITY_SCORE"] = (
        0.45 * df["EFF_SCORE"]
        + 0.30 * df["STYLE_SCORE"]
        + 0.25 * df["DEF_SCORE"]
    ) * df["MIN_CONF"]

    return df.sort_values(
        ["star_player", "QUALITY_SCORE"],
        ascending=[True, False]
    )
