# NBA All-Star Player Profile - Integration Guide

## Overview

Split-panel player profile card showing:
- **Left side**: Large player photo
- **Right side**: Player stats (Name, Height, Weight, Position, Team) + Team logo
- **Dropdown selector**: Switch between all 11 All-Star players

## Files Created

1. **`player_profile_card.py`** - Core player card creation logic
2. **`dash_player_profile.py`** - Standalone Dash app demo
3. **`test_player_card.html`** - Test output (view in browser)

## Quick Start

### Option 1: View Standalone Test

Open the generated HTML file:
```bash
open test_player_card.html
```

### Option 2: Run Standalone Dash App

```bash
python3 dash_player_profile.py
```
Then open: http://localhost:8052

## Integration into Existing Dashboard

To add to `src/app/__init__.py`:

### Step 1: Import Required Functions

Add at the top of your `__init__.py`:

```python
# Add to imports section
import sys
sys.path.insert(0, '..')  # Add parent directory to path

from player_profile_card import (
    load_player_data,
    create_player_profile_card
)

# Load player data
DF_ALLSTARS = load_player_data('star_graph_data/allstar_data.csv')
ALLSTAR_PLAYERS = DF_ALLSTARS['PLAYER'].tolist()
```

### Step 2: Replace Static Player Card

**Find this section** in your left column (around line 101-119):

```python
# 2. Static Player Card
html.Div(id='player-profile-card',
         style={'border': '1px solid #00BFFF', 'padding': '10px',
                'boxShadow': '2px 2px 10px #00BFFF55', 'backgroundColor': CARD_COLOR,
                'height': f'{GRAPH_HEIGHT}px', 'flexShrink': 0},
         children=[
             html.H4("Star Player (Placeholder)", ...),
             html.Div(...),  # Image Placeholder
             html.P("Team: N/A (Static)", ...),
             html.P("Age: N/A (Static)", ...),
             html.P("Height: N/A (Static)", ...),
         ]),
```

**Replace with**:

```python
# 2. All-Star Player Profile Card (Dynamic)
html.Div(style={'backgroundColor': CARD_COLOR, 'padding': '10px',
                'borderRadius': '5px', 'marginBottom': '10px'}, children=[
    html.Label("Select All-Star:",
               style={'fontWeight': 'bold', 'color': 'white',
                      'fontFamily': CUSTOM_FONT, 'fontSize': '14px',
                      'marginBottom': '8px', 'display': 'block'}),
    dcc.Dropdown(
        id='allstar-player-dropdown',
        options=[{'label': p, 'value': p} for p in ALLSTAR_PLAYERS],
        value=ALLSTAR_PLAYERS[0],
        searchable=True,
        clearable=False,
        style={'backgroundColor': '#343A40', 'fontFamily': CUSTOM_FONT,
               'fontSize': '12px', 'marginBottom': '10px'}
    )
]),

# Player profile card container (will be updated by callback)
html.Div(id='player-profile-card-container',
         style={'marginBottom': '10px'}),
```

### Step 3: Add Callback

Add this callback **before** `if __name__ == '__main__':` at the end:

```python
# --- CALLBACK: Update All-Star Player Profile ---
@app.callback(
    Output('player-profile-card-container', 'children'),
    Input('allstar-player-dropdown', 'value')
)
def update_allstar_profile(selected_player):
    """Update player profile card when selection changes."""

    if not selected_player or DF_ALLSTARS.empty:
        return html.Div("No player selected",
                       style={'color': 'white', 'padding': '10px'})

    try:
        # Get player data
        player_row = DF_ALLSTARS[DF_ALLSTARS['PLAYER'] == selected_player].iloc[0]

        # Create profile card HTML
        card_html = create_player_profile_card(player_row, dark_theme=True)

        # Return using html.Iframe to display HTML content
        return html.Iframe(
            srcDoc=card_html,
            style={
                'width': '100%',
                'height': '450px',
                'border': 'none',
                'overflow': 'hidden',
                'marginTop': '10px'
            }
        )

    except Exception as e:
        print(f"Error creating player card: {str(e)}")
        import traceback
        traceback.print_exc()
        return html.Div(f"Error: {str(e)}",
                       style={'color': 'red', 'padding': '10px'})
```

## Layout Details

### Card Structure

```
┌─────────────────────────────────────────┐
│  [Player Dropdown Selector]             │
├─────────────────────────────────────────┤
│                     │                   │
│                     │  Name: LeBron     │
│   Player Photo      │  Height: 6-9      │
│   (Left Panel)      │  Weight: 250 lbs  │
│                     │  Position: Forward│
│                     │  Team: LA Lakers  │
│                     │                   │
│                     │  [Team Logo]      │
└─────────────────────────────────────────┘
```

### Styling

- **Background**: Dark theme (`#2A3642`)
- **Accent color**: Teal (`#008080`)
- **Border**: Blue glow (`#00BFFF`)
- **Font**: Calibri
- **Responsive**: Flexbox layout (50/50 split)

### Image Sizes

- **Player photo**: Max 400px height, contained to preserve aspect ratio
- **Team logo**: Max 120px, centered in bottom-right panel

## File Structure Requirements

Make sure your directory structure is:

```
clusters/
├── src/
│   └── app/
│       └── __init__.py (your main dashboard)
├── star_graph_data/
│   ├── allstar_data.csv
│   ├── player photos/
│   │   ├── Nikola Jokić.png
│   │   ├── Stephen Curry.png
│   │   └── ... (all player photos)
│   └── logo/
│       ├── Denver Nuggets logo.webp
│       ├── Golden State Warriors logo.png
│       └── ... (all team logos)
├── player_profile_card.py
└── dash_player_profile.py
```

## Data Format

Your `allstar_data.csv` should have these columns:

```csv
PLAYER_ID,PLAYER,Height,Weight,Position,Draft Year,CURRENT_TEAM
203999,Nikola Jokić,6-11,284.0,Center,2014,Denver Nuggets
...
```

**Required columns**:
- `PLAYER` - Full player name
- `Height` - Format: "6-11"
- `Weight` - Numeric (lbs)
- `Position` - Guard/Forward/Center
- `CURRENT_TEAM` - Full team name

## Image Naming Conventions

The code handles various naming patterns:

### Player Photos
- Exact match: `LeBron James.png`
- With spaces: `LeBron James .png` (trailing space)
- Leading space: ` Kevin Durant.jpg`
- Lowercase: `nikola-jokic-2-1.jpg.webp`

### Team Logos
- Standard: `Denver Nuggets logo.webp`
- Underscores: `Los_Angeles_Lakers_logo.svg.png`
- Special cases handled automatically

## Customization Options

### Change Card Size

In `player_profile_card.py`, modify the `create_player_profile_card()` function:

```python
# Adjust min-height
min-height: 450px;  # Instead of 350px

# Adjust image max sizes
max-height: 500px;  # Instead of 400px (player photo)
max-width: 150px;   # Instead of 120px (team logo)
```

### Change Colors

```python
# In create_player_profile_card() function
accent_color = '#FF6600'  # Change from teal to orange
border_color = '#FFD700'  # Change to gold
```

### Add More Stats

In the stats section, add:

```python
<div style="margin-bottom: 8px;">
    <span style="color: {accent_color}; font-weight: bold;">Draft Year:</span>
    <span style="margin-left: 10px;">{player_data['Draft Year']}</span>
</div>
```

## Troubleshooting

### Issue: Images not loading

**Solution**: Check file paths and run test script:
```bash
python3 player_profile_card.py
```

### Issue: "Module not found" error

**Solution**: Ensure player_profile_card.py is in the correct directory:
```python
# In __init__.py, add:
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))
```

### Issue: Card too small/large

**Solution**: Adjust the `min-height` in the HTML style (default: 350px)

### Issue: Team logo not appearing

**Solution**: Check logo file naming in `star_graph_data/logo/`
Run test to see which logos are missing.

## Performance Notes

- **Image encoding**: All images are base64-encoded (embedded in HTML)
- **Load time**: ~100-200ms per player switch
- **Memory**: Each card ~50-100KB in memory
- **Total data**: All 11 players loaded at startup (~5MB total)

## Next Steps

1. **Test standalone**: Run `python3 dash_player_profile.py`
2. **Verify images**: Check `test_player_card.html` in browser
3. **Integrate**: Follow steps above to add to main dashboard
4. **Customize**: Adjust colors/sizes as needed

## Advanced Features (Optional)

### Add Player Navigation Buttons

```python
html.Div(style={'display': 'flex', 'gap': '10px', 'justifyContent': 'center'},
         children=[
    html.Button('← Previous', id='prev-player-btn',
                style={'padding': '10px 20px'}),
    html.Button('Next →', id='next-player-btn',
                style={'padding': '10px 20px'})
])

# Add callback to handle navigation
```

### Add Player Comparison

```python
# Select two players to compare side-by-side
html.Div(style={'display': 'flex', 'gap': '20px'}, children=[
    html.Div(id='player-1-card', style={'flex': 1}),
    html.Div(id='player-2-card', style={'flex': 1})
])
```

### Add Animations

```python
# Add CSS transition in card style
transition: all 0.3s ease-in-out;
```

## Questions?

Check the example files:
- `player_profile_card.py` - Core implementation
- `dash_player_profile.py` - Dash integration
- `test_player_card.html` - Example output
