# NBA Lineup Archetypes Dashboard

Team project: interactive Dash dashboard to explore lineup performance around 11 selected NBA "star" players, using archetype clustering for their teammates.

## 1. Project overview

High-level idea:

- Choose 11 focal players ("stars").
- For the last 10 seasons, collect **all lineups that include at least one of these stars**.
- Build a **player-season table**:
  - Each row = a (player, season) pair.
  - A player can have multiple rows (one per season).
  - For each row, pull many stats/features for that player-season.
- Cluster all player-season rows into **archetypes** (role types).
- Build **lineup tables**:
  - For each star player, collect all lineups that include them.
  - Replace non-star players in each lineup with their **archetype labels**.
  - Group lineups by **archetype combinations** (e.g., Star + [Creator, Wing Shooter, Rim Protector, Connector]).
  - Compute **weighted averages** of lineup metrics using minutes played together.
- Build a **Dash dashboard**:
  - Select a star player.
  - Select an archetype combination.
  - Visualize lineup metrics for that combo and compare to other combos.

> (Optional future step – not implemented yet):  
> For a chosen star + archetype combination, show the list of actual players from last season that match each archetype and simulate predicted metrics for a specific 4-player + star lineup.

---

## 2. Repository structure

```text
NBA-lineup-archetypes-dashboard/
├─ README.md
├─ .gitignore
├─ requirements.txt
├─ data/
│  ├─ raw/          # original data pulled from APIs / sources
│  │  ├─ lineups/
│  │  ├─ clusters/
│  ├─ interim/      # cleaned / merged tables before modeling
│  │  ├─ lineups/
│  │  ├─ clusters/
│  └─ processed/    # final tables used directly by the dashboard
├─ notebooks/
│  ├─ Per_season_data_pull.ipynb    # data for clusters pull
│  ├─ lineups_data_pull.ipynb
│  └─ 03_clustering_experiments.ipynb
├─ src/
│  ├─ __init__.py
│  ├─ data/
│  │  ├─ __init__.py
│  │  ├─ load_players.py
│  │  ├─ load_lineups.py
│  │  └─ build_archetype_lineups.py
│  ├─ models/
│  │  ├─ __init__.py
│  │  └─ clustering.py
│  └─ app/
│     ├─ __init__.py
│     ├─ layout.py
│     ├─ callbacks.py
│     └─ run.py
└─ tests/
