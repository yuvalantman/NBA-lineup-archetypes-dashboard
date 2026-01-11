"""
Helper functions for creating flexible NBA court zones with arcs.
Allows creating zones with straight-line or arc-based edges.
"""

import math


def create_zone_rect(x_min, x_max, y_min, y_max):
    """
    Simple rectangular zone.
    
    Args:
        x_min, x_max: X boundaries
        y_min, y_max: Y boundaries
    
    Returns:
        Dict with zone shape definition for use in zones list
    """
    return {
        'shape_type': 'rect',
        'bounds': {'x': [x_min, x_max], 'y': [y_min, y_max]}
    }


def calculate_arc_angles(center_x, center_y, radius, point1, point2):
    """
    Calculate start and end angles for an arc connecting two points.
    
    Args:
        center_x, center_y: Center of arc circle
        radius: Radius of arc circle
        point1: (x, y) tuple - first point
        point2: (x, y) tuple - second point
    
    Returns:
        (start_angle, end_angle) in degrees (0° = right, 90° = up, -90° = down, 180° = left)
    """
    x1, y1 = point1
    x2, y2 = point2
    
    # Calculate angles from center to each point
    angle1 = math.degrees(math.atan2(y1 - center_y, x1 - center_x))
    angle2 = math.degrees(math.atan2(y2 - center_y, x2 - center_x))
    
    return angle1, angle2


def create_arc_path(center_x, center_y, radius, start_angle, end_angle, large_arc=False):
    """
    Creates an SVG arc path string.
    
    Args:
        center_x, center_y: Center of the arc
        radius: Radius of the arc
        start_angle: Starting angle in degrees (0° = right, 90° = up)
        end_angle: Ending angle in degrees
        large_arc: If True, draws the larger arc (>180°)
        
    Returns:
        SVG path string for use with Plotly add_shape(type="path")
    """
    start_rad = math.radians(start_angle)
    end_rad = math.radians(end_angle)
    
    # Calculate start and end points
    x1 = center_x + radius * math.cos(start_rad)
    y1 = center_y + radius * math.sin(start_rad)
    x2 = center_x + radius * math.cos(end_rad)
    y2 = center_y + radius * math.sin(end_rad)
    
    large_arc_flag = 1 if large_arc else 0
    sweep_flag = 1  # Clockwise
    
    path = f"M {x1} {y1} A {radius} {radius} 0 {large_arc_flag} {sweep_flag} {x2} {y2}"
    
    return path


def create_zone_with_arc(corners, arc_between=(0, 1), arc_center=None, arc_radius=None):
    """
    Creates a zone with 4 corners where one edge can be an arc instead of a straight line.
    
    Args:
        corners: List of 4 [x, y] coordinates: [corner0, corner1, corner2, corner3]
                 These form a closed polygon when connected in order
        
        arc_between: Tuple (i, j) indicating which two corners to connect with an arc.
                     Values: (0, 1), (1, 2), (2, 3), or (3, 0)
                     Default (0, 1) means arc from corner 0 to corner 1
        
        arc_center: (x, y) tuple - center point of the arc circle
                    If None, no arc will be created
        
        arc_radius: Radius of the arc circle
                    If None, no arc will be created
    
    Returns:
        Dict with zone shape definition including:
        - 'shape_type': 'path' (will use SVG path with arc)
        - 'path': SVG path string with arc
        - 'corners': Original corners for reference
    
    Example:
        # Create a 3-point corner zone with an arc along the 3-point line
        corners = [
            [-250, -47.5],      # corner 0: baseline left
            [-220, -47.5],      # corner 1: baseline right  
            [-220, 100],        # corner 2: top right
            [-250, 100]         # corner 3: top left
        ]
        
        zone = create_zone_with_arc(
            corners=corners,
            arc_between=(0, 1),  # Arc from baseline left to baseline right
            arc_center=(0, -47.5),  # Center of 3-point arc
            arc_radius=237.5      # 3-point arc radius
        )
    """
    if arc_center is None or arc_radius is None:
        # No arc, just use regular polygon
        return {
            'shape_type': 'polygon',
            'corners': corners
        }
    
    i, j = arc_between
    point_i = corners[i]
    point_j = corners[j]
    
    # Calculate arc angles from center to each point
    angle_i, angle_j = calculate_arc_angles(arc_center[0], arc_center[1], arc_radius, point_i, point_j)
    
    # Determine if we need large_arc flag (>180° sweep)
    angle_diff = (angle_j - angle_i) % 360
    large_arc = angle_diff > 180
    
    # Create arc path
    arc_path_str = create_arc_path(
        arc_center[0], arc_center[1], arc_radius, 
        angle_i, angle_j, 
        large_arc=large_arc
    )
    
    # Add straight lines between other corners
    # Build path by going: corner_i -> arc to -> corner_j -> corner_j+1 -> ... -> corner_i-1 -> back to corner_i
    
    path = arc_path_str  # Start with the arc
    
    # Add remaining corners as straight lines
    for k in range(j + 1, i + 4):
        corner_idx = k % 4
        next_corner = corners[corner_idx]
        path += f" L {next_corner[0]} {next_corner[1]}"
    
    # Close the path
    path += " Z"
    
    return {
        'shape_type': 'path',
        'path': path,
        'corners': corners,
        'arc_info': {
            'between': arc_between,
            'center': arc_center,
            'radius': arc_radius
        }
    }


# Example usage:
if __name__ == "__main__":
    print("Zone Helper Functions - Examples\n")
    
    # Example 1: Simple rectangle
    print("Example 1: Simple rectangle zone")
    rect_zone = create_zone_rect(-80, 80, -51, 80)
    print(f"Result: {rect_zone}\n")
    
    # Example 2: 3-point corner with arc along baseline
    print("Example 2: 3-point corner with arc along 3-point line")
    corner_3pt = create_zone_with_arc(
        corners=[
            [-250, -47.5],      # baseline left
            [-220, -47.5],      # baseline right  
            [-220, 100],        # top right
            [-250, 100]         # top left
        ],
        arc_between=(0, 1),    # Arc from corner 0 to corner 1
        arc_center=(0, -47.5), # 3-point arc center
        arc_radius=237.5       # 3-point arc radius
    )
    print(f"Shape type: {corner_3pt['shape_type']}")
    print(f"Path: {corner_3pt['path'][:100]}...\n")
    
    # Example 3: Wing zone with arc along 3-point line
    print("Example 3: Wing 3-point zone with arc")
    wing_3pt = create_zone_with_arc(
        corners=[
            [-246, 88],         # bottom left (on 3-point arc)
            [-74, 88],          # bottom right
            [-74, 237],         # top right
            [-250, 237]         # top left
        ],
        arc_between=(0, 1),    # Arc from corner 0 to corner 1 (bottom edge)
        arc_center=(0, -47.5), # 3-point arc center
        arc_radius=237.5       # 3-point arc radius
    )
    print(f"Shape type: {wing_3pt['shape_type']}")
    print(f"Path: {wing_3pt['path'][:100]}...\n")
    
    # Example 4: Paint area - rectangle
    print("Example 4: Paint area (simple rectangle)")
    paint = create_zone_rect(-80, 80, -51, 80)
    print(f"Result: {paint}\n")
