"""
Opponent Placeholder Component for Dashboard

Simple placeholder for future lineup vs opponent comparison chart.
"""

from dash import html


def create_opponent_placeholder(
    component_id: str = 'opponent',
    height: int = 450,
    card_color: str = '#2A3642',
    accent_color: str = '#008080',
    border_color: str = '#00BFFF'
) -> html.Div:
    """
    Create styled placeholder for future opponent comparison chart.

    Args:
        component_id: Unique ID prefix for component elements
        height: Placeholder height in pixels
        card_color: Background color
        accent_color: Accent color for text
        border_color: Border color

    Returns:
        Dash html.Div with "Coming Soon" placeholder
    """
    return html.Div(
        id=f'{component_id}-placeholder',
        style={
            'backgroundColor': card_color,
            'border': f'2px dashed {border_color}',
            'borderRadius': '10px',
            'padding': '40px',
            'minHeight': f'{height}px',
            'display': 'flex',
            'flexDirection': 'column',
            'alignItems': 'center',
            'justifyContent': 'center',
            'fontFamily': 'Calibri, sans-serif'
        },
        children=[
            # Icon placeholder
            html.Div(
                "📊",
                style={
                    'fontSize': '60px',
                    'marginBottom': '20px',
                    'opacity': '0.5'
                }
            ),

            # Main title
            html.H3(
                "Lineup vs Opponent",
                style={
                    'color': accent_color,
                    'marginBottom': '15px',
                    'fontSize': '24px',
                    'fontWeight': 'bold',
                    'textAlign': 'center'
                }
            ),

            # Subtitle
            html.P(
                "Coming Soon",
                style={
                    'color': 'rgba(255, 255, 255, 0.6)',
                    'fontSize': '16px',
                    'marginBottom': '10px',
                    'textAlign': 'center'
                }
            ),

            # Description
            html.P(
                "This section will display lineup performance comparisons against different opponent archetypes.",
                style={
                    'color': 'rgba(255, 255, 255, 0.4)',
                    'fontSize': '13px',
                    'textAlign': 'center',
                    'maxWidth': '300px',
                    'lineHeight': '1.6'
                }
            )
        ]
    )


# Example usage documentation
INTEGRATION_EXAMPLE = """
# How to integrate into your main dashboard:

## Step 1: Import in your layout file (src/app/__init__.py)

from src.app.components.opponent_placeholder import create_opponent_placeholder

## Step 2: Add to your layout

layout = html.Div([
    # ... other components ...

    create_opponent_placeholder(
        component_id='opponent',
        height=450
    ),

    # ... more components ...
])

## Done!
Simple placeholder with no callbacks needed.

## Future Implementation:
When ready to implement the actual chart, replace this component with:
- Opponent archetype analysis
- Head-to-head performance metrics
- Matchup difficulty ratings
"""

if __name__ == '__main__':
    print("="*60)
    print("Opponent Placeholder Component - Integration Guide")
    print("="*60)
    print(INTEGRATION_EXAMPLE)
