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
