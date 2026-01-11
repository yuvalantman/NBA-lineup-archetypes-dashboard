# NBA Lineup Archetypes Dashboard

An interactive analytics dashboard for exploring **NBA lineup performance and player archetypes**. This educational project analyzes lineup metrics for elite NBA players and their teammates using data-driven clustering and visualization techniques.

> **For Educational Purposes**: This project is built as a course assignment to demonstrate data analysis, clustering, and interactive dashboard development with NBA player data.

---

## Overview

This dashboard answers key questions about NBA lineups:
- **Which archetype combinations work best** for a star player?
- **How do lineup metrics compare** (efficiency, shot tendencies, defensive coverage)?
- **What shooting patterns emerge** in different lineup archetypes?

**Key Methodology:**
1. **Archetype Clustering**: Players are clustered into role-based archetypes (e.g., "Creator," "Wing Shooter," "Rim Protector") based on their seasonal statistics
2. **Lineup Grouping**: Real lineups are reconstructed with archetype labels instead of individual players
3. **Performance Metrics**: Compute weighted averages of efficiency, tendencies, and shot data for each lineup combination

---

## What's on the Dashboard

### Main Interactive Features

| Feature | What It Does |
|---------|-------------|
| **Star Player Selector** | Choose from 11 focal NBA players |
| **Archetype Selector** | Pick a 5-player archetype combination |
| **Player Profile** | View player stats, team, and photo |
| **Efficiency Landscape** | 3D scatter plot comparing offensive/defensive ratings across lineups |
| **Tendency Heatmap** | Visual breakdown of play-style percentages |
| **Shot Chart** | Interactive court visualization with shooting patterns and zones |
| **Team vs Opponent Stats** | Compare your lineup's stats against league opponents |

### Data Visualizations
- **Shot zones** with success rates
- **3D efficiency curves** for multiple lineup comparisons
- **Radar-style heatmaps** for playing style tendencies
- **Interactive filtering** by archetype combinations

---

## Project Structure

```
NBA-lineup-archetypes-dashboard/
├── main.py                          # Entry point (runs with: python main.py)
├── requirements.txt                 # Python dependencies
├── README.md                        # This file
│
├── src/
│   ├── app/                         # Dash web application
│   │   ├── run.py                  # App initialization & data loading
│   │   ├── layout.py               # Dashboard page layout
│   │   ├── callbacks.py            # Interactive event handlers
│   │   └── components/             # Reusable visualization components
│   │       ├── archetype_profile.py
│   │       ├── player_profile.py
│   │       ├── efficiency_landscape.py
│   │       ├── shot_chart.py
│   │       ├── team_vs_opp.py
│   │       ├── tendency_heatmap.py
│   │       ├── court_visualization.py
│   │       └── __init__.py
│   │
│   ├── data/                        # Data loading & processing
│   │   ├── load_players.py
│   │   ├── load_efficiency.py
│   │   ├── load_lineups.py
│   │   ├── load_tendencies.py
│   │   ├── build_archetype_lineups.py
│   │   ├── lineup_score.py
│   │   ├── zone_helpers.py
│   │   └── __init__.py
│   │
│   └── models/
│       ├── clustering.py            # Player archetype clustering logic
│       └── __init__.py
│
├── data/                            # Data files
│   ├── raw/                         # Original data from NBA API
│   │   ├── allstar_data.csv
│   │   ├── allstar_lineups_data_synthetic.csv
│   │   ├── full_players_shotloc.csv
│   │   ├── full_players_shottype_small.csv
│   │   ├── full_players_defense_*.csv
│   │   └── lineups/
│   ├── interim/                     # Processed intermediate data
│   │   ├── clusters/
│   │   └── lineups/
│   └── processed/                   # Final data for dashboard
│       ├── Archetype_lineups_with_scores_data.csv
│       ├── Ready_efficiency_data.csv
│       ├── Ready_shots_data.csv
│       ├── Ready_team_vs_opp_data.csv
│       ├── Ready_tendencies_data.csv
│       └── files_for_demo/
│
├── assets/                          # Static files
│   ├── custom_styles.css
│   ├── images/
│   │   └── player_photos/           # Player headshots
│   └── logos/
│
├── notebooks/                       # Jupyter notebooks for analysis
│   ├── Per_season_Data_pull.ipynb
│   ├── lineups_data_pull.ipynb
│   └── clustering.ipynb
│
├── docs/                            # Documentation
│   └── guides/
│       ├── EFFICIENCY_GRAPH_GUIDE.md
│       ├── PLAYER_PROFILE_INTEGRATION.md
│       └── TENDENCY_RADAR_GUIDE.md
│
└── tests/                           # Unit tests
```

---

## Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Local Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/[your-repo]/NBA-lineup-archetypes-dashboard.git
   cd NBA-lineup-archetypes-dashboard
   ```

2. **Create a virtual environment** (recommended):
   ```bash
   python -m venv .venv
   ```

3. **Activate the virtual environment**:
   - **Windows**:
     ```bash
     .venv\Scripts\activate
     ```
   - **macOS/Linux**:
     ```bash
     source .venv/bin/activate
     ```

4. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

---

## Running the Dashboard

### Local Development

```bash
python main.py
```

The dashboard will start at: **http://localhost:8050**

You should see:
```
NBA Dashboard is starting...
✅ Efficiency data loaded: X lineups
✅ Tendencies data loaded: X lineups
...
Dashboard running at: http://localhost:8050
```

### Using the Dashboard

1. **Select a Star Player** from the top dropdown
2. **Choose an Archetype Combination** from the second selector
3. **View Performance Metrics** in the interactive visualizations
4. **Hover/Click** on charts for detailed information
5. **Use 3D Controls** to rotate the efficiency landscape (click and drag)

---

## Deployment

This dashboard is deployed and accessible online at: **[Render URL]**

### Deploy Your Own (Render)

1. **Push code to GitHub**:
   ```bash
   git add .
   git commit -m "Deploy dashboard"
   git push origin main
   ```

2. **Connect to Render**:
   - Go to [render.com](https://render.com)
   - Create new Web Service
   - Connect your GitHub repository
   - Set **Start Command** to: `gunicorn main:app`
   - Deploy

3. **Share the public URL** with your class!

---

## Technology Stack

| Technology | Purpose |
|-----------|---------|
| **Dash** | Interactive web framework |
| **Plotly** | Interactive visualizations |
| **Pandas** | Data manipulation |
| **NumPy** | Numerical computations |
| **scikit-learn** | Clustering algorithms |
| **Gunicorn** | Production WSGI server |

---

## Data Sources

- **NBA Stats API**: Player statistics, lineups, and shot data
- **Archetype Clustering**: K-means clustering on seasonal player stats
- **Lineup Data**: Real NBA lineups from historical games

---

## Troubleshooting

### Port Already in Use
If port 8050 is unavailable, the app will automatically try the next port.

### Missing Data Files
Ensure these files exist in `data/processed/`:
- `Ready_efficiency_data.csv`
- `Ready_tendencies_data.csv`
- `Ready_shots_data.csv`
- `Ready_team_vs_opp_data.csv`

### Import Errors
Run from the project root directory:
```bash
cd NBA-lineup-archetypes-dashboard
python main.py
```

---

## Contributing

To add features:
1. Create a feature branch: `git checkout -b feature/my-feature`
2. Add code to appropriate files
3. Test locally: `python main.py`
4. Push and open a pull request

---

## Credits

Built with:
- [Dash](https://dash.plotly.com/) for interactive dashboards
- [Plotly](https://plotly.com/) for visualizations
- [NBA Stats API](https://www.nba.com/stats/) for data

---

## License

This project is for **educational purposes** as part of a course assignment.
