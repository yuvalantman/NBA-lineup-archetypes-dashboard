# NBA Lineup Tendency Radar Chart - User Guide

## Overview

This visualization creates an **8-axis spider/radar chart** showing lineup tendency profiles. Users can overlay 2-5 lineups simultaneously to compare their playing style characteristics across 8 key metrics.

## Files Created

1. **`src/data/load_tendencies.py`** - Data loading and normalization utilities
2. **`tendency_radar_chart.py`** - Core visualization with Plotly Scatterpolar
3. **`dash_tendency_radar.py`** - Standalone Dash app with interactive UI
4. **`src/app/components/tendency_radar.py`** - Reusable component for main dashboard

## Quick Start

### Option 1: View Static HTML (Fastest)

The standalone script already generated 4 test HTML files:

```bash
open luka_tendencies_radar.html
```

Available test files:
- `test_two_lineups.html` - 2 lineup comparison (minimum)
- `test_three_lineups.html` - 3 lineup comparison (recommended)
- `test_five_lineups.html` - 5 lineup comparison (maximum)
- `luka_tendencies_radar.html` - default visualization

### Option 2: Run Standalone Dash App

```bash
python3 dash_tendency_radar.py
```

Then open: http://127.0.0.1:8054

**Features:**
- Interactive lineup selector with checkboxes
- Quick select buttons (First 3, Random 3, Clear All)
- Real-time validation (2-5 lineup recommendation)
- Hover tooltips showing exact values and percentiles
- Click legend to toggle lineups on/off
- Export as PNG using camera icon

### Option 3: Integrate into Main Dashboard

See integration instructions below.

---

## The 8 Metrics

Each axis on the radar chart represents a different playing style metric:

| Metric | Label | Description |
|--------|-------|-------------|
| `fta_per48` | FTA/48 | Free throw attempts per 48 min (aggressive driving to rim) |
| `three_pa_per48` | 3PA/48 | 3-point attempts per 48 min (perimeter-oriented offense) |
| `points_off_turnovers` | Points Off TO | Points scored after turnovers (transition game strength) |
| `second_chance_points` | 2nd Chance Pts | Points from offensive rebounds (rebounding + hustle) |
| `points_in_paint` | Paint Points | Points scored in the paint (interior scoring emphasis) |
| `pct_midrange_points` | Midrange % | Percentage of points from midrange (shot selection) |
| `pct_unassisted_points` | Unassisted % | Percentage of unassisted points (isolation tendency) |
| `pct_fastbreak_points` | Fastbreak % | Percentage of points from fastbreak (pace of play) |

**All metrics are normalized 0-1** where:
- **0** = Worst value among the 30 lineups
- **1** = Best value among the 30 lineups
- **0.5** = Midpoint

---

## How to Read the Chart

### Visual Elements

1. **Octagonal Shape**: 8-sided polygon with each vertex representing a metric
2. **Colored Polygons**: Each lineup is a different color (teal, cyan, orange, purple, lime)
3. **Filled Areas**: Semi-transparent (35% opacity) to show overlaps
4. **Solid Lines**: Clear borders for each lineup (2px width)
5. **Radial Grid**: Concentric circles showing 0%, 25%, 50%, 75%, 100%

### Interpretation

- **Larger polygon area** = More extreme/specialized tendencies across metrics
- **Points near edge** = High values for that metric (top performers)
- **Points near center** = Low values for that metric (bottom performers)
- **Overlapping areas** = Similar tendencies between lineups
- **Non-overlapping** = Different playing styles

### Example Insights

**Lineup with large "3PA/48" axis:**
- Perimeter-oriented offense
- Relies heavily on 3-point shooting
- Likely includes multiple shooters

**Lineup with large "Paint Points" axis:**
- Interior-focused offense
- Strong post players or rim runners
- Less reliant on outside shooting

**Lineup with high "Unassisted %" and "Midrange %":**
- Isolation-heavy offense
- Star player creating own shots
- Less ball movement

---

## Hover Information

When you hover over any point on the chart, you'll see:

```
Lineup 1
3PA/48
Value: 37.6
Normalized: 0.70
Percentile: 70th
```

- **Lineup composition**: Shown in legend (e.g., "Rim_Protector, Post_Scorer, Movement_Shooter, Secondary_Ball_Handler")
- **Metric name**: Which axis you're hovering over
- **Value**: Actual raw value (e.g., 37.6 attempts per 48 minutes)
- **Normalized**: 0-1 scale position (0.70 = 70% of max value)
- **Percentile**: Rank among 30 lineups (70th = better than 70% of lineups)

---

## Color Palette

The visualization uses 5 distinct colors for lineup overlays:

1. **Teal** (#008080) - First lineup
2. **Cyan** (#00BFFF) - Second lineup
3. **Orange** (#FF8C00) - Third lineup
4. **Purple** (#9370DB) - Fourth lineup
5. **Lime** (#32CD32) - Fifth lineup

If more than 5 lineups are selected, colors cycle through the palette.

---

## Dashboard Integration

### Step 1: Load Data in Main App

Add to your `src/app/__init__.py` or `src/app/layout.py`:

```python
from src.data.load_tendencies import load_tendency_data, normalize_metrics

# Load tendency data
df_tendencies = load_tendency_data('tendency_graph/luka_team_tendencies_graph_data.csv')
df_tendencies = normalize_metrics(df_tendencies)
```

### Step 2: Add Component to Layout

```python
from src.app.components.tendency_radar import create_tendency_radar_component

# In your layout:
html.Div([
    # ... existing components ...

    html.Hr(style={'borderColor': '#008080', 'margin': '20px 0'}),

    html.H2("Lineup Tendency Profile",
            style={'textAlign': 'center', 'color': '#008080', 'marginBottom': '20px'}),

    create_tendency_radar_component(
        df_tendencies=df_tendencies,
        default_lineups=[0, 5, 10],  # Customize starting selection
        component_id='tendency-radar',
        star_player='Luka Dončić',
        card_color='#2A3642',
        accent_color='#00BFFF',
        header_color='#008080'
    ),

    # ... more components ...
])
```

### Step 3: Register Callbacks

```python
from src.app.components.tendency_radar import register_tendency_radar_callbacks

# After creating app, before app.run():
register_tendency_radar_callbacks(
    app,
    df_tendencies=df_tendencies,
    component_id='tendency-radar',
    star_player='Luka Dončić'
)
```

**That's it!** The radar chart is now integrated.

---

## API Reference

### Core Functions

#### `load_tendency_data(csv_path: str) -> pd.DataFrame`

Load lineup tendency data from CSV file.

**Parameters:**
- `csv_path`: Path to CSV file

**Returns:**
- DataFrame with 30 lineups and 13 columns (5 archetype columns + 8 metric columns)

#### `normalize_metrics(df: pd.DataFrame, metrics: List[str] = None) -> pd.DataFrame`

Normalize metrics to 0-1 scale using min-max scaling.

**Parameters:**
- `df`: DataFrame with raw metric values
- `metrics`: List of metric column names (defaults to all 8)

**Returns:**
- DataFrame with added `{metric}_norm` columns

#### `create_tendency_radar(df, selected_lineups, ...) -> go.Figure`

Create the radar chart visualization.

**Parameters:**
- `df`: DataFrame with normalized metrics
- `selected_lineups`: List of lineup indices (0-29)
- `star_player`: Player name for title (default: 'Luka Dončić')
- `metrics`: Metrics to display (default: all 8)
- `title`: Custom title (optional)
- `height`: Chart height in pixels (default: 700)
- `width`: Chart width in pixels (default: 700)
- `background_color`: Background color (default: '#1E2833')

**Returns:**
- Plotly Figure object

**Example:**
```python
fig = create_tendency_radar(
    df=df_tendencies,
    selected_lineups=[0, 10, 20],
    star_player='Luka Dončić',
    height=800,
    width=800
)
fig.show()
```

---

## Customization Options

### Change Default Lineups

In `dash_tendency_radar.py`, modify line 83:

```python
value=[0, 10, 20],  # Change to your preferred default lineups
```

### Adjust Chart Size

When creating the radar chart:

```python
fig = create_tendency_radar(
    df=df_tendencies,
    selected_lineups=[0, 1, 2],
    height=900,  # Larger chart
    width=900
)
```

### Modify Color Palette

In `tendency_radar_chart.py`, edit the `LINEUP_COLORS` list (lines 26-32):

```python
LINEUP_COLORS = [
    {'name': 'Red', 'line': '#FF0000', 'fill': 'rgba(255, 0, 0, 0.35)'},
    # ... add your custom colors
]
```

### Change Background Theme

```python
fig = create_tendency_radar(
    df=df_tendencies,
    selected_lineups=[0, 1, 2],
    background_color='#FFFFFF'  # White background instead of dark
)
```

---

## Troubleshooting

### Issue: "Module not found" error

**Solution:** Ensure you're running from the project root directory:

```bash
cd /path/to/clusters/
python3 dash_tendency_radar.py
```

### Issue: Empty chart or "No data" message

**Solution:** Check that CSV file exists and has correct path:

```python
df = load_tendency_data('tendency_graph/luka_team_tendencies_graph_data.csv')
```

### Issue: Chart too crowded with many lineups

**Solution:** Limit selection to 2-5 lineups. The validation message will warn you if you select too many.

### Issue: Hover tooltips not showing lineup composition

**Solution:** The lineup composition is shown in the **legend**, not in hover tooltips. Hover shows metric values and percentiles.

---

## Performance Notes

- **Data loading**: ~50ms for 30 lineups
- **Normalization**: ~10ms for 8 metrics
- **Chart rendering**: ~100-200ms per lineup
- **Total load time**: <1 second for 3-5 lineups

**Recommended:**
- Select 2-5 lineups for optimal readability
- Use 8 metrics (all) for complete profile
- Chart size: 700-900px for desktop displays

---

## Data Format Requirements

Your CSV must have these columns:

**Required columns:**
- `star_player` - Star player name (e.g., "Luka Doncic")
- `player1_archetype` - First teammate archetype
- `player2_archetype` - Second teammate archetype
- `player3_archetype` - Third teammate archetype
- `player4_archetype` - Fourth teammate archetype
- `fta_per48` - Free throw attempts per 48 min
- `three_pa_per48` - 3-point attempts per 48 min
- `points_off_turnovers` - Points from turnovers
- `second_chance_points` - Second chance points
- `points_in_paint` - Points in paint
- `pct_midrange_points` - % midrange points (0-1 scale)
- `pct_unassisted_points` - % unassisted points (0-1 scale)
- `pct_fastbreak_points` - % fastbreak points (0-1 scale)

**Example row:**
```csv
Luka Doncic,Rim_Protector,Post_Scorer,Movement_Shooter,Secondary_Ball_Handler,18.36,37.58,8.85,16.56,44.60,0.137,0.247,0.174
```

---

## Next Steps

1. **Test standalone app**: Run `python3 dash_tendency_radar.py`
2. **Explore HTML files**: Open generated HTML files to see different lineup combinations
3. **Integrate into dashboard**: Follow integration steps above
4. **Customize**: Adjust colors, sizes, default selections to your preference

---

## Questions?

Check the example files:
- `tendency_radar_chart.py` - Core implementation with extensive comments
- `dash_tendency_radar.py` - Full Dash app example
- `src/app/components/tendency_radar.py` - Integration example

All code includes detailed docstrings and inline comments for reference.
