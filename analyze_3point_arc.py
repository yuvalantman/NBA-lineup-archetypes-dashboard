import math

# 3-point arc center: (0, -47.5), radius 237.5
# Calculate where the arc reaches at different Y values

center_x, center_y = 0, -47.5
radius = 237.5

print("3-POINT ARC BOUNDARIES AT KEY Y VALUES:")
print("=" * 60)

for y in [-47.5, 0, 50, 95, 138, 142.5, 220, 237]:
    dx_sq = radius**2 - (y - center_y)**2
    if dx_sq >= 0:
        x_extent = math.sqrt(dx_sq)
        print(f"Y={y:7.1f}: X ranges from {-x_extent:7.1f} to {x_extent:7.1f}")
    else:
        print(f"Y={y:7.1f}: Beyond arc (arc doesn't reach this far)")

print("\n\nANGLE CALCULATIONS FOR 3-POINT ZONES:")
print("=" * 60)

# For left wing zone bounds
points = [
    ("Left Corner bottom", -220, -47.5),
    ("Left Corner top", -220, 87),
    ("Left Wing inner bottom", -160, 88),
    ("Left Wing outer top", -74, 237),
    ("Center top", 0, 397),
]

for name, x, y in points:
    if x != 0 or y != center_y:
        angle = math.degrees(math.atan2(y - center_y, x - center_x))
        # Normalize to 0-360
        if angle < 0:
            angle += 360
        distance = math.sqrt((x - center_x)**2 + (y - center_y)**2)
        print(f"{name:25s} ({x:4.0f}, {y:4.1f}): angle={angle:6.1f}°, dist={distance:7.1f}")

print("\n\nRECOMMENDATIONS FOR 3-POINT ZONES:")
print("=" * 60)
print("""
1. CORNERS: Keep as rectangles since they're before the arc kicks in
   - Left Corner: X[-250, -220], Y[-47.5, 87]
   - Right Corner: X[220, 250], Y[-47.5, 87]

2. WINGS: Use arcs to follow the 3-point line
   - Left Wing: Arc from ~135° to ~156° (following actual 3-point arc)
   - Right Wing: Arc from ~24° to ~45°
   - Center: Arc from ~45° to ~135° (top of the key)

3. MID-RANGE ADJUSTMENTS: Stop zones before they hit 3-point arc
   - Mid-Range 16-24ft Left Center: X[-190, -148] (not -80, stop at 3-pt arc)
   - Mid-Range 16-24ft Right Center: X[148, 187] (not from 80, stop at 3-pt arc)
   - Mid-Range 16-24ft Center: Limit Y to ~140 max
   - Mid-Range 16-24ft Left Side: Keep as-is (135 < 148)
   - Mid-Range 16-24ft Right Side: Keep as-is (130 < 148)
""")
