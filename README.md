<<<<<<< HEAD
# NBA Lineup Analysis Dashboard

An interactive dashboard for analyzing NBA player performance, shot charts, lineup efficiency, and team tendencies.

## Project Overview

This project provides a comprehensive analysis tool for NBA data, featuring:
- **Player Profiles**: Visual cards with player stats, photos, and team logos
- **Shot Charts**: Interactive heatmaps showing shooting patterns and efficiency
- **Efficiency Landscape**: 3D visualization of lineup performance metrics
- **Tendency Radar**: Multi-dimensional comparison of lineup playing styles

## Project Structure

```
clusters/
├── main.py                    # Main entry point to run the dashboard
├── requirements.txt           # Python dependencies
├── .gitignore                # Git ignore rules
│
├── src/                       # Source code
│   ├── app/                  # Dash application
│   │   ├── run.py           # App factory and initialization
│   │   ├── layout.py        # Dashboard layout definition
│   │   ├── callbacks.py     # Interactive callback handlers
│   │   └── components/      # Reusable UI components
│   │       ├── player_profile.py
│   │       ├── court_visualization.py
│   │       ├── efficiency_landscape.py
│   │       ├── tendency_radar.py
│   │       └── opponent_placeholder.py
│   │
│   ├── data/                 # Data loading utilities
│   │   ├── load_players.py
│   │   ├── load_efficiency.py
│   │   ├── load_tendencies.py
│   │   └── load_lineups.py
│   │
│   └── models/              # Data models (clustering, etc.)
│       └── clustering.py
│
├── data/                     # Data files
│   ├── raw/                 # Raw data from NBA API
│   │   ├── allstar_data.csv
│   │   └── allstar_shots_with_lineups.csv
│   └── processed/           # Processed/aggregated data
│       ├── luka_efficiency_graph_data.csv
│       └── luka_team_tendencies_graph_data.csv
│
├── assets/                   # Static assets
│   ├── images/
│   │   └── player_photos/   # Player headshots
│   └── logos/               # Team logos
│
├── docs/                     # Documentation
│   └── guides/              # Component-specific guides
│       ├── EFFICIENCY_GRAPH_GUIDE.md
│       ├── PLAYER_PROFILE_INTEGRATION.md
│       ├── TENDENCY_RADAR_GUIDE.md
│       └── TENDENCY_RADAR_UPDATES.md
│
└── archive/                  # Archived old experiments
    └── old_experiments/
```

## Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Setup Steps

1. **Clone or navigate to the project directory**:
   ```bash
   cd /path/to/clusters
   ```

2. **Create a virtual environment** (recommended):
   ```bash
   python3 -m venv .venv
   ```

3. **Activate the virtual environment**:
   - On macOS/Linux:
     ```bash
     source .venv/bin/activate
     ```
   - On Windows:
     ```bash
     .venv\Scripts\activate
     ```

4. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Running the Dashboard

### Quick Start

Simply run the main script:

```bash
python main.py
```

The dashboard will start on [http://localhost:8052](http://localhost:8052)

### Alternative Method

You can also run directly from the app module:

```bash
python -m src.app.run
```

This will start the dashboard on [http://localhost:8050](http://localhost:8050) (default port)

### Accessing the Dashboard

Once running, open your web browser and navigate to:
- **http://localhost:8052** (if using `main.py`)
- **http://localhost:8050** (if using `src.app.run`)

You should see:
```
NBA Dashboard is starting...
Dash is running on http://127.0.0.1:8052/

 * Serving Flask app 'run'
 * Debug mode: on
```

## Using the Dashboard

### Main Features

1. **Star Player Selection** (Top Left)
   - Select any NBA All-Star from the dropdown
   - Updates player profile, shot chart automatically

2. **Player Profile Card** (Left Column)
   - Displays player photo, stats (height, weight, position)
   - Shows team logo

3. **Shot Chart** (Center Column)
   - Interactive visualization of all shots
   - Green dots = made shots, Red dots = missed shots
   - Hover for shot details (distance, zone, result)

4. **Lineup Comparison** (Top Right)
   - Select 2-5 lineups to compare
   - Updates efficiency landscape and tendency radar

5. **Efficiency Landscape** (Right Column)
   - 3D visualization of offensive/defensive ratings
   - Compare multiple lineups simultaneously

6. **Tendency Radar** (Bottom Right)
   - Multi-dimensional comparison of playing styles
   - Metrics: pace, 3-point tendency, rim attempts, etc.

### Tips

- **Best Performance**: Select 2-5 lineups for optimal visualization clarity
- **Shot Chart Zoom**: Use mouse wheel to zoom, click and drag to pan
- **Efficiency Graph**: Rotate the 3D view by clicking and dragging
- **Export**: Most visualizations have a camera icon for downloading as PNG

## Data Sources

- **NBA Stats API**: Player statistics and shot data
- **Lineup Data**: Curated lineup combinations with performance metrics
- **Player Photos**: Sourced from official NBA images
- **Team Logos**: Official NBA team branding

## Troubleshooting

### Port Already in Use

If port 8052 is already in use, you can change it in [main.py](main.py):

```python
app.run(debug=True, port=8053)  # Change to any available port
```

### Missing Data Files

Ensure all data files are in the correct locations:
- `data/raw/allstar_data.csv` - Player information
- `data/raw/allstar_shots_with_lineups.csv` - Shot data
- `data/processed/luka_efficiency_graph_data.csv` - Efficiency metrics
- `data/processed/luka_team_tendencies_graph_data.csv` - Tendency metrics

### Missing Player Images/Logos

If player photos or team logos are missing:
- Check `assets/images/player_photos/` for player headshots
- Check `assets/logos/` for team logos
- The dashboard will show placeholder icons if images are not found

### Import Errors

If you see import errors, make sure you're running from the project root directory:

```bash
cd /path/to/clusters
python main.py
```

## Development

### Project Dependencies

Core libraries used:
- **Dash**: Web application framework
- **Plotly**: Interactive visualizations
- **Pandas**: Data manipulation
- **NumPy**: Numerical computations
- **NBA API**: NBA statistics
- **scikit-learn**: Machine learning utilities

### Adding New Features

1. **New Components**: Add to `src/app/components/`
2. **New Data Loaders**: Add to `src/data/`
3. **Update Layout**: Modify `src/app/layout.py`
4. **Add Callbacks**: Update `src/app/callbacks.py`

### Code Style

- Follow PEP 8 guidelines
- Use type hints where applicable
- Add docstrings to all functions
- Keep components modular and reusable

## Credits

Built with [Dash](https://dash.plotly.com/) & [Plotly](https://plotly.com/)

Data from [NBA Stats API](https://www.nba.com/stats/)

## License

This project is for educational purposes.
=======
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
### A. Clone this repository

  git clone https://github.com/<username>/NBA-lineup-archetypes-dashboard.git

  cd NBA-lineup-archetypes-dashboard

### B. Install environment (via Makefile)

  make install

  This will:
  Create a .venv virtual environment

  Install all requirements

  Prepare the project for development

### C. Run the dashboard locally
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
  #### make changes
  git add .

  git commit -m "Implement clustering step"

  git push -u origin feature/clustering

Then open a Pull Request (PR) to main.

---

## 5. Data guidelines
### Safe to commit:
- Notebooks
- Small raw datasets in data/raw/
- Source code (src/)
- Configuration files

### Do NOT commit:
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
>>>>>>> 35217567569a3e4a4d5abe233313123ba3bbeed6
