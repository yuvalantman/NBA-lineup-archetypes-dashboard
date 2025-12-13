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
├─ Makefile
│
├─ data/
│  ├─ raw/          # original data pulled from APIs / sources
│  │  ├─ lineups/
│  │  ├─ clusters/
│  ├─ interim/      # cleaned / merged tables before modeling
│  │  ├─ lineups/
│  │  ├─ clusters/
│  └─ processed/    # final tables used directly by the dashboard
│
├─ notebooks/
│  ├─ Per_season_data_pull.ipynb    # data for clusters pull
│  ├─ lineups_data_pull.ipynb
│  └─ 03_clustering_experiments.ipynb
│
├─ src/
│  ├─ __init__.py
│  │
│  ├─ data/
│  │  ├─ __init__.py
│  │  ├─ load_players.py
│  │  ├─ load_lineups.py
│  │  └─ build_archetype_lineups.py
│  │
│  ├─ models/
│  │  ├─ __init__.py
│  │  └─ clustering.py
│  │
│  └─ app/
│     ├─ __init__.py
│     ├─ layout.py
│     ├─ callbacks.py
│     └─ run.py
│
└─ tests/
```
---

## 3. Installation
A. Clone this repository

  git clone https://github.com/<username>/NBA-lineup-archetypes-dashboard.git

  cd NBA-lineup-archetypes-dashboard

B. Install environment (via Makefile)

  make install

  This will:
  Create a .venv virtual environment

  Install all requirements

  Prepare the project for development

C. Run the dashboard locally
  make run

  Dashboard starts at:
  http://127.0.0.1:8050/
  
---

## 4. Collaboration workflow
Branching strategy

- main → stable, production-ready code
- dev → integration branch (optional)
- Feature branches → individual tasks

  Examples:
  - feature/clustering
  - feature/data-processing
  - feature/dashboard-ui

Workflow example

  git checkout -b feature/clustering
  # make changes
  git add .

  git commit -m "Implement clustering step"

  git push -u origin feature/clustering

Then open a Pull Request (PR) to main.

---

## 5. Data guidelines
# Safe to commit:
- Notebooks
- Small raw datasets in data/raw/
- Source code (src/)
- Configuration files

# Do NOT commit:
- data/interim/
- data/processed/
- Raw files > 50–100 MB (GitHub will reject them)
- API keys or secrets
- Binary temporary files

---

## 6. Deployment (for course evaluation)

This repository is structured to support deployment on:
- Render (recommended)
- Railway
- HuggingFace Spaces
- Heroku (paid)
- DigitalOcean

Deployment will require adding:
- Procfile
- runtime.txt (optional)
- Uploading small processed datasets to data/processed/

When you reach deployment, instructions will be added.

---

## 7. Notes
Notebooks should use relative paths (data/raw/...)

Dash app loads data from data/processed/

The Makefile provides a reproducible setup for all team members