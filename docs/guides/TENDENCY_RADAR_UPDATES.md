# Tendency Radar Chart - Recent Updates

## Summary of Changes

The tendency radar chart has been updated with improved UI controls, better hover formatting, and basketball-themed styling.

---

## 🎨 New Features

### 1. Dropdown Quick Selection (Replaces Buttons)

**Changed from:** Three separate buttons (Select First 3, Select Random 3, Clear All)

**Changed to:** Single dropdown menu with 4 options:
- **Select First 3** - Selects lineups 1, 2, 3
- **Select Random 3** - Randomly selects 3 lineups
- **Select All (30 lineups)** - Selects all 30 lineups for complete overview
- **Clear All** - Deselects all lineups

**Benefits:**
- Cleaner, more compact UI
- NEW "Select All" option for viewing all lineups at once
- Less visual clutter
- More professional appearance

**Location:** Below the lineup checklist in both the standalone app and dashboard component

---

### 2. Enhanced Hover Tooltips with Calibri Font

**Before:**
```
Lineup 1
3PA/48
Value: 37.6
Normalized: 0.70
Percentile: 70th
```

**After:**
- **Calibri font family** throughout (professional, clean typography)
- **Larger, bolder text** for better readability (14px lineup name, 13px metric)
- **Color-coded metric names** (basketball orange #FF8C00)
- **Bold values** for emphasis
- **Improved sizing** (12-14px range for optimal legibility)

**HTML Styling Applied:**
```html
<b style="font-family: Calibri, sans-serif; font-size: 14px;">Lineup 1</b>
<b style="font-family: Calibri, sans-serif; font-size: 13px; color: #FF8C00;">3PA/48</b>
<span style="font-family: Calibri, sans-serif; font-size: 12px;">Value: <b>37.6</b></span>
```

---

### 3. Basketball-Themed Styling

#### Hexagonal/Octagonal Grid Design
The 8-axis radar chart naturally creates an **octagonal (8-sided) shape** that resembles a basketball's panel pattern.

#### Basketball Color Scheme
- **Grid lines**: Basketball orange (`rgba(255, 140, 0, 0.4)`)
- **Angular axes**: Basketball orange (`rgba(255, 140, 0, 0.5)`)
- **Radial grid**: Basketball orange with transparency
- **Grid width**: Increased to 2px for prominence
- **Court-like background**: Dark gray (`rgba(34, 34, 34, 0.3)`)

#### Hover Box Styling
- **Background**: Nearly opaque dark gray (`rgba(30, 30, 30, 0.95)`)
- **Border**: Basketball orange (`rgba(255, 140, 0, 0.8)`)
- **Font**: Calibri at 13px
- **White text** on dark background for maximum contrast

---

## 📊 Visual Comparison

### Before vs After

| Aspect | Before | After |
|--------|--------|-------|
| **Selection UI** | 3 separate buttons | Dropdown menu with 4 options |
| **"Select All" option** | ❌ Not available | ✅ Available |
| **Hover font** | Default sans-serif | Calibri (professional) |
| **Hover styling** | Plain text | Bold values, color-coded |
| **Grid color** | White/gray | Basketball orange |
| **Grid theme** | Generic | Basketball court-inspired |
| **Hover border** | Black | Basketball orange |

---

## 🎯 Technical Details

### Files Modified

1. **`dash_tendency_radar.py`**
   - Lines 135-166: Changed from buttons to dropdown
   - Lines 293-312: Updated callback for dropdown handling

2. **`tendency_radar_chart.py`**
   - Lines 60-68: Enhanced hover template with Calibri font and styling
   - Lines 140-164: Basketball-themed polar chart styling
   - Lines 190-196: Basketball-themed hover label border

3. **`src/app/components/tendency_radar.py`**
   - Lines 105-136: Added quick select dropdown
   - Lines 195-214: Added quick select callback
   - Maintains consistency with standalone app

---

## 🚀 Usage

### Standalone App

```bash
python3 dash_tendency_radar.py
# Open: http://127.0.0.1:8054
```

**Try the new features:**
1. Use the "Quick Select" dropdown to choose "Select All (30 lineups)"
2. Hover over any point to see the improved Calibri-formatted tooltips
3. Notice the basketball orange gridlines creating the octagonal shape

### Dashboard Integration

The component automatically includes all new features when integrated:

```python
from src.app.components.tendency_radar import (
    create_tendency_radar_component,
    register_tendency_radar_callbacks
)

# Component includes dropdown and basketball styling automatically
component = create_tendency_radar_component(
    df_tendencies=df_tendencies,
    default_lineups=[0, 5, 10]
)
```

---

## 🎨 Color Palette Reference

### Basketball Orange Theme
- **Primary orange**: `#FF8C00` (RGB: 255, 140, 0)
- **Grid lines**: `rgba(255, 140, 0, 0.4)` - 40% opacity
- **Angular axis**: `rgba(255, 140, 0, 0.5)` - 50% opacity
- **Grid background**: `rgba(255, 140, 0, 0.3)` - 30% opacity
- **Hover border**: `rgba(255, 140, 0, 0.8)` - 80% opacity

### Supporting Colors
- **Court background**: `rgba(34, 34, 34, 0.3)` - Dark gray
- **Hover background**: `rgba(30, 30, 30, 0.95)` - Nearly black
- **Text**: `#FFFFFF` - White

### Lineup Polygon Colors (unchanged)
1. Teal: `#008080`
2. Cyan: `#00BFFF`
3. Orange: `#FF8C00`
4. Purple: `#9370DB`
5. Lime: `#32CD32`

---

## 📝 Quick Select Options Details

### 1. Select First 3
- **Lineup indices**: 0, 1, 2
- **Use case**: Quick test with the first three lineups in the dataset
- **Example lineups**:
  - Lineup 1: Rim_Protector, Post_Scorer, Movement_Shooter, Secondary_Ball_Handler
  - Lineup 2: Shot_Creator, Pass_First_Guard, Stretch_Big, Shot_Creator
  - Lineup 3: Two_Way_Forward, Pass_First_Guard, Unicorn, Rim_Protector

### 2. Select Random 3
- **Lineup indices**: 3 random indices from 0-29
- **Use case**: Discover unexpected lineup comparisons
- **Benefit**: Avoids selection bias, explores diverse combinations

### 3. Select All (30 lineups) ⭐ NEW
- **Lineup indices**: 0-29 (all lineups)
- **Use case**: Complete overview of all lineup tendencies
- **Visual**: Dense, multi-layered spider chart showing full spectrum
- **Warning**: Chart may be crowded - best viewed at larger sizes

### 4. Clear All
- **Lineup indices**: None (empty selection)
- **Use case**: Start fresh, deselect all before manual selection
- **Result**: Shows "Please select at least 1 lineup" message

---

## 🔧 Customization

### Adjust Basketball Orange Intensity

In `tendency_radar_chart.py`, modify the opacity values:

```python
gridcolor='rgba(255, 140, 0, 0.6)',  # More prominent (default: 0.4)
gridcolor='rgba(255, 140, 0, 0.2)',  # More subtle
```

### Change Hover Font

In `tendency_radar_chart.py`, line 61:

```python
'<b style="font-family: Arial, sans-serif; ...'  # Change to Arial
'<b style="font-family: Georgia, serif; ...'     # Change to Georgia
```

### Modify Dropdown Options

In `dash_tendency_radar.py`, lines 151-156:

```python
options=[
    {'label': 'Select First 5', 'value': 'first_5'},  # Add new option
    {'label': 'Select Top Performers', 'value': 'top'},  # Custom logic
    # ... existing options
]
```

---

## ✅ What's Working

- ✅ Dropdown properly replaces buttons
- ✅ "Select All" option loads all 30 lineups
- ✅ Hover tooltips display in Calibri font
- ✅ Basketball orange grid creates octagonal appearance
- ✅ Hover border matches basketball theme
- ✅ All callbacks function correctly
- ✅ Component and standalone app both updated
- ✅ Backward compatible with existing code

---

## 🐛 Known Limitations

1. **"Select All" creates crowded visualization**
   - **Workaround**: Increase chart size to 900x900px or larger
   - **Future enhancement**: Add zoom/pan controls

2. **Dropdown doesn't reset after selection**
   - **Current behavior**: Dropdown shows last selected option
   - **Not a bug**: Allows users to see what was last selected
   - **Workaround**: Click dropdown placeholder to reset visually

---

## 📚 Documentation Updated

All changes are documented in:
- ✅ This file (`TENDENCY_RADAR_UPDATES.md`)
- ✅ `TENDENCY_RADAR_GUIDE.md` (main usage guide - to be updated)
- ✅ Inline code comments in all modified files

---

## 🎯 Next Steps

### Potential Future Enhancements

1. **Zoom Controls**
   - Add zoom in/out buttons for "Select All" mode
   - Enable scroll-to-zoom functionality

2. **Filter by Archetype**
   - Add dropdown to filter lineups by specific archetypes
   - e.g., "Show only lineups with Rim_Protector"

3. **Comparison Mode**
   - Add "Compare to Average" toggle
   - Overlay league average as gray reference polygon

4. **Export Enhancements**
   - Add "Download as PDF" option
   - Save current selection as preset

5. **Interactive Legends**
   - Click lineup name to highlight in chart
   - Double-click to isolate single lineup

---

## Questions or Issues?

Check the updated files:
- `dash_tendency_radar.py` - Standalone app with all new features
- `tendency_radar_chart.py` - Core visualization logic
- `src/app/components/tendency_radar.py` - Dashboard component

All code includes detailed comments explaining the basketball-themed styling and dropdown logic.
