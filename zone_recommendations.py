"""
Zone Coordinate Recommendations Based on Shot Data Analysis

Court System Reference:
- Baseline: Y = -47.5
- Hoop: (0, 0)
- Free Throw Line: Y = 142.5
- Far End: Y ≈ 425
- 3-Point Arc Center: (0, -47.5), radius 237.5
- Restricted Area: Center (0, 0), radius 40

Key Insights from Shot Data:
1. Restricted Area shots concentrate around (-39 to 39, -34 to 39)
2. Paint (non-RA) <8ft: (-80 to 79, -51 to 80)
3. Paint (non-RA) 8-16ft: (-79 to 79, 70 to 138)
4. Mid-Range zones show distinct X separation (left/center/right) with 8-16ft and 16-24ft Y ranges
5. 3-Point zones: Corner (±220-250, -46 to 87), Wing/Above Break
6. Backcourt: Y > 400
"""

zones_data = [
    {
        "id": 1,
        "name": "Restricted Area",
        "shape_type": "arc",
        "zone_key": ("Restricted Area", "Center(C)", "Less Than 8 ft."),
        "center": (0, 0),
        "radius": 40,
        "angle_start": -90,
        "angle_end": 90,
        "label_pos": (0, -5),
        "notes": "Arc at hoop, radius 40 (matches restricted area line)"
    },
    
    # Paint (Non-RA) - <8ft: Y from -51 to 80
    {
        "id": 2,
        "name": "Paint <8ft Center",
        "shape_type": "rect",
        "zone_key": ("In The Paint (Non-RA)", "Center(C)", "Less Than 8 ft."),
        "bounds": (-80, -51, 80, 80),
        "label_pos": (0, 15),
        "notes": "Use shot bounds X[-80,79] Y[-51,80]"
    },
    
    # Paint (Non-RA) Left 8-16ft
    {
        "id": 3,
        "name": "Paint <16ft Left",
        "shape_type": "rect",
        "zone_key": ("In The Paint (Non-RA)", "Left Side(L)", "8-16 ft."),
        "bounds": (-80, 70, -41, 138),
        "label_pos": (-60, 100),
        "notes": "Shot X[-80,-41] Y[-38,138], use Y[70,138] for consistency with center"
    },
    
    # Paint (Non-RA) Right 8-16ft
    {
        "id": 4,
        "name": "Paint <16ft Right",
        "shape_type": "rect",
        "zone_key": ("In The Paint (Non-RA)", "Right Side(R)", "8-16 ft."),
        "bounds": (41, 70, 80, 138),
        "label_pos": (60, 100),
        "notes": "Shot X[41,80] Y[-31,138], use Y[70,138]"
    },
    
    # Paint (Non-RA) Center 8-16ft
    {
        "id": 5,
        "name": "Paint 8-16ft Center",
        "shape_type": "rect",
        "zone_key": ("In The Paint (Non-RA)", "Center(C)", "8-16 ft."),
        "bounds": (-40, 70, 40, 138),
        "label_pos": (0, 100),
        "notes": "Shot X[-79,79] Y[70,138]"
    },
    
    # Mid-Range 8-16ft zones (between paint and free throw line)
    {
        "id": 6,
        "name": "Mid-Range 8-16ft Left",
        "shape_type": "rect",
        "zone_key": ("Mid-Range", "Left Side(L)", "8-16 ft."),
        "bounds": (-160, -44, -80, 137),
        "label_pos": (-120, 40),
        "notes": "Shot X[-160,-81] Y[-44,137], use left boundary X=-80 to avoid overlap"
    },
    
    {
        "id": 7,
        "name": "Mid-Range 8-16ft Right",
        "shape_type": "rect",
        "zone_key": ("Mid-Range", "Right Side(R)", "8-16 ft."),
        "bounds": (80, -42, 160, 137),
        "label_pos": (120, 40),
        "notes": "Shot X[81,160] Y[-42,137]"
    },
    
    {
        "id": 8,
        "name": "Mid-Range 8-16ft Center",
        "shape_type": "rect",
        "zone_key": ("Mid-Range", "Center(C)", "8-16 ft."),
        "bounds": (-40, 139, 40, 160),
        "label_pos": (0, 148),
        "notes": "Shot Y[139,160], above free throw"
    },
    
    # Mid-Range 16-24ft zones (between FT line and 3-point)
    {
        "id": 9,
        "name": "Mid-Range 16-24ft Left Center",
        "shape_type": "rect",
        "zone_key": ("Mid-Range", "Left Side Center(LC)", "16-24 ft."),
        "bounds": (-190, 95, -80, 223),
        "label_pos": (-135, 160),
        "notes": "Shot X[-190,-50], use right boundary=-80 for consistency"
    },
    
    {
        "id": 10,
        "name": "Mid-Range 16-24ft Right Center",
        "shape_type": "rect",
        "zone_key": ("Mid-Range", "Right Side Center(RC)", "16-24 ft."),
        "bounds": (80, 95, 187, 224),
        "label_pos": (135, 160),
        "notes": "Shot X[50,187], use left boundary=80"
    },
    
    {
        "id": 11,
        "name": "Mid-Range 16-24ft Center",
        "shape_type": "rect",
        "zone_key": ("Mid-Range", "Center(C)", "16-24 ft."),
        "bounds": (-70, 153, 71, 237),
        "label_pos": (0, 190),
        "notes": "Shot X[-70,71] Y[153,237], above free throw"
    },
    
    {
        "id": 12,
        "name": "Mid-Range 16-24ft Left Side",
        "shape_type": "rect",
        "zone_key": ("Mid-Range", "Left Side(L)", "16-24 ft."),
        "bounds": (-220, -39, -130, 138),
        "label_pos": (-175, 40),
        "notes": "Shot X[-220,-130] Y[-39,138], side wing area"
    },
    
    {
        "id": 13,
        "name": "Mid-Range 16-24ft Right Side",
        "shape_type": "rect",
        "zone_key": ("Mid-Range", "Right Side(R)", "16-24 ft."),
        "bounds": (130, -41, 220, 139),
        "label_pos": (175, 40),
        "notes": "Shot X[130,220] Y[-41,139]"
    },
    
    # 3-Point zones
    {
        "id": 14,
        "name": "3-Point Left Corner",
        "shape_type": "rect",
        "zone_key": ("Left Corner 3", "Left Side(L)", "24+ ft."),
        "bounds": (-250, -47.5, -220, 87),
        "label_pos": (-235, 20),
        "notes": "Shot X[-250,-220] Y[-46,87], corner area"
    },
    
    {
        "id": 15,
        "name": "3-Point Right Corner",
        "shape_type": "rect",
        "zone_key": ("Right Corner 3", "Right Side(R)", "24+ ft."),
        "bounds": (220, -47.5, 250, 87),
        "label_pos": (235, 20),
        "notes": "Shot X[220,250] Y[-46,87]"
    },
    
    {
        "id": 16,
        "name": "3-Point Left Wing/Above Break",
        "shape_type": "polygon",
        "zone_key": ("Above the Break 3", "Left Side Center(LC)", "24+ ft."),
        "corners": [(-246, 88), (-74, 88), (-74, 237), (-250, 237)],
        "label_pos": (-160, 160),
        "notes": "Shot X[-246,-74] Y[88,397], wing above break"
    },
    
    {
        "id": 17,
        "name": "3-Point Right Wing/Above Break",
        "shape_type": "polygon",
        "zone_key": ("Above the Break 3", "Right Side Center(RC)", "24+ ft."),
        "corners": [(74, 88), (248, 88), (250, 237), (75, 237)],
        "label_pos": (160, 160),
        "notes": "Shot X[75,248] Y[88,397]"
    },
    
    {
        "id": 18,
        "name": "3-Point Center/Above Break",
        "shape_type": "rect",
        "zone_key": ("Above the Break 3", "Center(C)", "24+ ft."),
        "bounds": (-127, 228, 113, 397),
        "label_pos": (0, 310),
        "notes": "Shot X[-127,113] Y[228,397], top of key above break"
    },
    
    # Backcourt - shots >400 on Y axis
    {
        "id": 19,
        "name": "Backcourt",
        "shape_type": "rect",
        "zone_key": ("Backcourt", "Back Court(BC)", "Back Court Shot"),
        "bounds": (-225, 398, 225, 425),
        "label_pos": (0, 410),
        "notes": "Shot Y[398-417], treat as FG%=0 zone (defensive rebound area)"
    },
]

print("OPTIMIZED ZONE COORDINATES FOR SHOT_CHART.PY")
print("=" * 100)
print("\nZONES TO ADD TO shot_chart.py ZONES DICTIONARY:\n")

for zone in zones_data:
    print(f"\n{zone['id']}. {zone['name']}")
    print(f"   Zone Key: {zone['zone_key']}")
    print(f"   Shape: {zone['shape_type']}")
    if zone['shape_type'] == 'rect':
        print(f"   Bounds: x_min={zone['bounds'][0]}, y_min={zone['bounds'][1]}, x_max={zone['bounds'][2]}, y_max={zone['bounds'][3]}")
    elif zone['shape_type'] == 'polygon':
        print(f"   Corners: {zone['corners']}")
    elif zone['shape_type'] == 'arc':
        print(f"   Arc: center={zone['center']}, radius={zone['radius']}, angles=[{zone['angle_start']}, {zone['angle_end']}]")
    print(f"   Label Pos: {zone['label_pos']}")
    print(f"   Notes: {zone['notes']}")
