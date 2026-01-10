# Zone Shot Chart Customization Guide

## Court Visualization
**File:** [src/app/components/court_visualization.py](src/app/components/court_visualization.py)

This file contains the `draw_nba_court()` function which draws all court lines. You can modify:
- Court boundary coordinates
- Paint dimensions
- 3-point line arc
- Hoop and backboard positions
- Any other court element

---

## Zone Shapes - Three Types Available

### 1. **Rectangle (type: 'rect')**
Simple rectangular zone using two corner points.

```python
{
    'name': 'Zone Name',
    'zone_key': ('SHOT_ZONE_BASIC', 'SHOT_ZONE_AREA', 'SHOT_ZONE_RANGE'),
    'shape_type': 'rect',
    'bounds': {'x': [x_min, x_max], 'y': [y_min, y_max]},
    'center': [label_x, label_y]
}
```

**Modify:** Adjust x and y coordinates to change size/position.

---

### 2. **Polygon (type: 'polygon')**
Irregular shape with 4+ corner points for complex zones.

```python
{
    'name': 'Left Paint',
    'zone_key': ('In The Paint (Non-RA)', 'Left Side(L)', 'Less Than 8 ft.'),
    'shape_type': 'polygon',
    'corners': [[-80, -47.5], [-47.5, -47.5], [-47.5, 40], [-80, 40]],
    'center': [-70, 30]
}
```

**Modify:** Add/remove corner coordinates `[[x1, y1], [x2, y2], [x3, y3], ...]`
- Corners should be in **order** (clockwise or counter-clockwise)
- Use 4 corners for rectangles, 6+ for complex shapes
- Format: `[[x, y], [x, y], ...]`

---

### 3. **Arc (type: 'arc')**
Curved zones using arc paths for circles/curved sections.

```python
{
    'name': 'Restricted Area',
    'zone_key': ('Restricted Area', 'Center(C)', 'Less Than 8 ft.'),
    'shape_type': 'arc',
    'path': create_arc_path(center_x=0, center_y=0, radius=40, start_angle=-90, end_angle=90),
    'center': [0, 20]
}
```

**Parameters:**
- `center_x, center_y`: Center of the arc (0, 0 is hoop)
- `radius`: Distance from center
- `start_angle`: Starting angle in degrees (0°=right, 90°=up, -90°=down)
- `end_angle`: Ending angle in degrees
- `large_arc`: Set to `True` if arc is >180°

**Modify:** Adjust center, radius, and angles to reshape curves.

---

## Zone File Location
**File:** [src/app/components/shot_chart.py](src/app/components/shot_chart.py)

**Zones are defined:** Line ~351-509 in `create_zone_shot_chart()` function

**Helper functions for zone creation:**
- `create_polygon_path()` - Line ~27-47
- `create_arc_path()` - Line ~50-88

---

## Court Coordinates Reference

### Court Dimensions (Plotly coordinates)
- **Width:** -250 to +250 (X axis)
- **Length:** -47.5 to ~425 (Y axis)
- **Hoop:** (0, 0)
- **Baseline:** Y = -47.5
- **Far end:** Y ≈ 425

### Key Court Features
- **Restricted Area circle:** Center (0, 0), radius ~40
- **Paint:** X from -80 to 80, Y from -47.5 to ~142.5
- **3-Point Line arc:** Center (0, -47.5), radius ~237.5
- **3-Point corners:** X ≈ ±220

---

## Step-by-Step: How to Modify a Zone

### Example: Change the Restricted Area to a true semicircle

**Current:**
```python
{
    'name': 'Restricted Area',
    'shape_type': 'arc',
    'path': create_arc_path(center_x=0, center_y=0, radius=40, start_angle=-90, end_angle=90),
}
```

**To make a full semicircle:**
```python
{
    'name': 'Restricted Area',
    'shape_type': 'arc',
    'path': create_arc_path(center_x=0, center_y=0, radius=40, start_angle=0, end_angle=180, large_arc=True),
    # 0° to 180° with large_arc=True draws the bottom semicircle
}
```

### Example: Change Left Paint to an irregular pentagon

**Current:**
```python
{
    'name': 'Left Paint',
    'shape_type': 'polygon',
    'corners': [[-80, -47.5], [-47.5, -47.5], [-47.5, 40], [-80, 40]],
}
```

**To make irregular:**
```python
{
    'name': 'Left Paint',
    'shape_type': 'polygon',
    'corners': [[-100, -47.5], [-47.5, -47.5], [-47.5, 30], [-60, 50], [-100, 50]],
    # Added extra corner at [-60, 50] for irregular edge
}
```

---

## Zone Statistics Calculation

For each zone, the chart calculates:

1. **FG% (Shooting Percentage)**
   - Color based: Red (0%) → Yellow (50%) → Green (100%)
   - Calculated from: `made_shots / total_shots`

2. **Opacity (Frequency/Tendency)**
   - Opacity scale: 0.3 (rare) to 1.0 (frequent)
   - Calculated from: `shots_in_zone / all_lineup_shots`

3. **Zone Display**
   - Shows `"NA"` in gray if no shots
   - Shows `"XX%"` where XX is FG% if shots exist

---

## Testing Your Changes

1. Modify zone definitions in shot_chart.py
2. Save file
3. Reload dashboard (Ctrl+R in browser)
4. Select a player and lineup
5. Click "Zones" radio button to see updates

---

## Angle Reference for Arcs

When using `create_arc_path()`:

```
        90°
        |
180° ---+--- 0°
        |
       270° / -90°
```

**Common angles:**
- `0°` = Right (3 o'clock)
- `90°` = Up (12 o'clock)
- `180°` = Left (9 o'clock)
- `-90°` = Down (6 o'clock)

**Example: Top half of circle from left to right**
```python
create_arc_path(center_x=0, center_y=0, radius=40, start_angle=180, end_angle=0, large_arc=True)
```

---

## Need Help?

- **Polygon not showing?** Check corners are in order (clockwise/counter-clockwise)
- **Arc looks wrong?** Verify start_angle, end_angle, and large_arc flag
- **Overlapping zones?** Adjust zone boundaries/corners
- **Text label in wrong spot?** Update the `'center': [x, y]` value
