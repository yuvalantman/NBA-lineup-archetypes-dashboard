# Efficiency Landscape Graph - Implementation Guide

## Overview

The efficiency landscape graph visualizes lineup performance by plotting **Offensive Rating** (x-axis) vs **Defensive Rating** (y-axis), similar to Kirk Goldsberry's NBA team visualizations.

## Files Created

1. **`efficiency_landscape.py`** - Standalone visualization script
2. **`dash_efficiency_example.py`** - Dash integration example
3. **`luka_efficiency_landscape.html`** - Generated HTML output

## Quick Start

### Option 1: View Standalone Visualization

```bash
python3 efficiency_landscape.py
```

This will:
- Load data from `data/processed/luka_efficiency_graph_data.csv`
- Create an interactive scatter plot
- Save to `luka_efficiency_landscape.html`
- Open in your browser

### Option 2: Run Dash App

```bash
python3 dash_efficiency_example.py
```

Then open: http://localhost:8051

## Data Format

Your CSV file should have these columns:

```csv
star_player,player1_archetype,player2_archetype,player3_archetype,player4_archetype,offensive_rating,defensive_rating,net_rating
```

Example:
```csv
Luka Doncic,Rim_Protector,Post_Scorer,Movement_Shooter,Secondary_Ball_Handler,118.0,87.9,-5.7
```

## Graph Features

### Axes
- **X-axis**: Offensive Rating (higher = better offense)
- **Y-axis**: Defensive Rating (INVERTED - top = better defense)
  - Lower defensive rating = better defense
  - Chart is inverted so better defense appears higher

### Visual Elements

1. **Points**: Each represents one lineup
   - Size: 12px markers
   - Color: Net Rating (green = good, red = bad)
   - Border: White outline for visibility

2. **Reference Lines** (dashed gray):
   - Vertical: Median offensive rating
   - Horizontal: Median defensive rating
   - These divide the chart into 4 quadrants

3. **Quadrants**:
   - **Top-Right (ELITE)**: Good offense + Good defense
   - **Top-Left**: Good defense, Poor offense
   - **Bottom-Right**: Good offense, Poor defense
   - **Bottom-Left (WEAK)**: Poor offense + Poor defense

4. **Hover Information**:
   - Star player name
   - 4 archetype names
   - Offensive Rating
   - Defensive Rating
   - Net Rating

### Color Scale
- Uses 'RdYlGn' (Red-Yellow-Green)
- Green: Positive net rating (good)
- Yellow: Near zero net rating
- Red: Negative net rating (bad)

## Integration with Existing Dashboard

To add to your existing Dash app in `src/app/__init__.py`:

### Step 1: Import the function

```python
# Add at top of file
from efficiency_landscape import create_efficiency_figure
import pandas as pd

# Load efficiency data
DF_EFFICIENCY = pd.read_csv('data/processed/luka_efficiency_graph_data.csv')
```

### Step 2: Add to Layout

Add this section to your dashboard layout:

```python
# Add after your shot chart section or wherever you want
html.Hr(style={'borderColor': MAIN_HEADER_COLOR, 'margin': '20px 0'}),

html.H2("Lineup Efficiency Landscape",
        style={'textAlign': 'center', 'color': MAIN_HEADER_COLOR,
               'fontFamily': CUSTOM_FONT, 'marginTop': '20px'}),

html.Div(style={'backgroundColor': CARD_COLOR, 'padding': '15px',
                'borderRadius': '5px', 'marginTop': '10px'}, children=[

    dcc.Graph(
        id='efficiency-landscape-graph',
        figure=create_efficiency_figure(
            DF_EFFICIENCY,
            star_player='Luka Dončić',
            dark_theme=True,
            height=650
        ),
        config={'displayModeBar': True, 'displaylogo': False}
    ),

    # Explanation
    html.Div(style={'marginTop': '15px', 'color': 'white',
                   'fontFamily': CUSTOM_FONT}, children=[
        html.P("Each point represents a lineup. Hover for details.",
               style={'fontSize': '14px'}),
        html.Ul([
            html.Li("Top-right quadrant = ELITE (good offense + defense)"),
            html.Li("Color shows Net Rating (green = good, red = bad)")
        ], style={'fontSize': '12px', 'lineHeight': '1.6'})
    ])
]),
```

### Step 3: (Optional) Add Interactive Dropdown

If you want to switch between different players:

```python
# In layout
dcc.Dropdown(
    id='efficiency-player-selector',
    options=[
        {'label': 'Luka Dončić', 'value': 'luka'},
        {'label': 'Other Player', 'value': 'other'},
    ],
    value='luka',
    style={'width': '300px', 'marginBottom': '10px'}
)

# Add callback
@app.callback(
    Output('efficiency-landscape-graph', 'figure'),
    Input('efficiency-player-selector', 'value')
)
def update_efficiency_graph(selected_player):
    # Load appropriate data file
    if selected_player == 'luka':
        df = pd.read_csv('data/processed/luka_efficiency_graph_data.csv')
        player_name = 'Luka Dončić'
    else:
        df = pd.read_csv(f'data/processed/{selected_player}_efficiency_graph_data.csv')
        player_name = 'Other Player'

    return create_efficiency_figure(df, star_player=player_name, dark_theme=True)
```

## Customization Options

### Change Colors

In `create_efficiency_figure()`, modify:

```python
# Different color scale
colorscale='Viridis'  # or 'Blues', 'Reds', 'Portland', etc.

# Change background
bg_color = '#YOUR_COLOR'
```

### Adjust Marker Size

```python
marker=dict(
    size=15,  # Increase from 12
    ...
)
```

### Change Reference Lines

```python
# Use mean instead of median
avg_offensive = df['offensive_rating'].mean()

# Or use fixed NBA average
avg_offensive = 110  # NBA league average
avg_defensive = 110
```

### Add Team Logos

If you have team data:

```python
# In create_efficiency_figure()
fig.add_trace(go.Scatter(
    x=df['offensive_rating'],
    y=df['defensive_rating'],
    mode='markers+text',
    text=df['team_logo_emoji'],  # e.g., '🏀', '⭐'
    textposition='middle center',
    ...
))
```

## Understanding the Visualization

### Best Lineups
Look for points that are:
- **Far right** (high offensive rating)
- **Top of chart** (low defensive rating, inverted)
- **Green color** (positive net rating)

### Worst Lineups
Look for points that are:
- **Far left** (low offensive rating)
- **Bottom of chart** (high defensive rating)
- **Red color** (negative net rating)

### Balanced vs Specialized
- **Diagonal spread**: Lineups trade offense for defense
- **Clustered in one quadrant**: Team has consistent style
- **Outliers**: Experimental or unusual lineup combinations

## Data Requirements

Minimum required:
```python
df.columns = [
    'offensive_rating',  # Float
    'defensive_rating',  # Float
    'net_rating',        # Float
    'player1_archetype', # String
    'player2_archetype', # String
    'player3_archetype', # String
    'player4_archetype'  # String
]
```

Optional:
```python
'star_player'  # String - for filtering/grouping
'possessions'  # Int - for bubble size
'win_pct'      # Float - alternative color metric
```

## Performance Tips

1. **For large datasets** (>1000 points):
   - Use `marker=dict(size=8)` for smaller points
   - Consider filtering to top/bottom N lineups
   - Add dropdown to select specific archetype combinations

2. **For real-time dashboards**:
   - Cache the figure creation
   - Use `dcc.Loading()` component
   - Limit updates with `prevent_initial_call=True`

3. **For mobile viewing**:
   - Reduce height to 500px
   - Increase marker size to 14px
   - Use simpler hover text

## Troubleshooting

### Issue: Y-axis not inverted
**Solution**: Ensure `yaxis=dict(autorange='reversed')` is set

### Issue: Colors not showing
**Solution**: Check that net_rating column has no NaN values:
```python
df['net_rating'] = df['net_rating'].fillna(0)
```

### Issue: Hover text not formatted
**Solution**: Ensure HTML tags use `<b>` not `**` for bold

### Issue: Reference lines missing
**Solution**: Check that avg values are within data range:
```python
print(f"X range: {df['offensive_rating'].min()} to {df['offensive_rating'].max()}")
print(f"Reference at: {avg_offensive}")
```

## Next Steps

1. **Add more players**: Create efficiency data for other stars
2. **Compare players**: Side-by-side efficiency landscapes
3. **Filter by archetype**: Show only lineups with specific archetypes
4. **Add animations**: Show how efficiency changed over time
5. **Export feature**: Allow users to download specific lineups

## Questions?

Check the example files:
- `efficiency_landscape.py` - Full implementation
- `dash_efficiency_example.py` - Dash integration
- `luka_efficiency_landscape.html` - Example output
