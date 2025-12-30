"""
Reusable Tendency Radar Component for Dashboard Integration

Provides a self-contained radar chart component that can be easily
integrated into the main NBA lineup analysis dashboard.
"""

import sys
from pathlib import Path
import pandas as pd
from dash import dcc, html, Input, Output

# Add parent directories to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from data.load_tendencies import create_lineup_label
from .tendency_radar_chart import create_tendency_radar, create_empty_figure


def create_tendency_radar_component(
    df_tendencies: pd.DataFrame,
    default_lineups: list = None,
    component_id: str = 'tendency-radar',
    star_player: str = 'Luka Dončić',
    external_checklist_id: str = None,
    show_internal_checklist: bool = True,
    card_color: str = '#2A3642',
    accent_color: str = '#00BFFF',
    header_color: str = '#008080'
) -> html.Div:
    """
    Create a self-contained tendency radar chart component.

    Args:
        df_tendencies: DataFrame with normalized tendency data
        default_lineups: List of lineup indices to display by default
        component_id: Unique ID prefix for component elements
        star_player: Name of star player for title
        external_checklist_id: If provided, use external checklist instead of internal
        show_internal_checklist: If False, hide internal checklist (use external only)
        card_color: Background color for cards
        accent_color: Accent/border color
        header_color: Header text color

    Returns:
        Dash html.Div containing the complete component
    """
    if default_lineups is None:
        default_lineups = [0, 10, 20]  # Default: 3 diverse lineups

    # Create lineup options
    lineup_options = []
    for i in range(len(df_tendencies)):
        label = create_lineup_label(df_tendencies.iloc[i])
        lineup_options.append({
            'label': f"Lineup {i+1}: {label}",
            'value': i
        })

    # Prepare children list (conditionally include checklist)
    children_list = []

    # Only show internal checklist if requested
    if show_internal_checklist and external_checklist_id is None:
        children_list.append(
            # Lineup Selector (Compact Version)
            html.Div(
                style={
                    'backgroundColor': card_color,
                    'padding': '15px',
                    'borderRadius': '5px',
                    'marginBottom': '15px',
                    'border': f'1px solid {accent_color}'
                },
                children=[
                    html.Label(
                        "Select Lineups to Compare (2-5 recommended):",
                        style={
                            'color': 'white',
                            'fontWeight': 'bold',
                            'fontSize': '14px',
                            'marginBottom': '10px',
                            'display': 'block'
                        }
                    ),

                    # Checklist in scrollable container
                    html.Div(
                        style={
                            'maxHeight': '150px',
                            'overflowY': 'auto',
                            'padding': '10px',
                            'backgroundColor': 'rgba(0, 0, 0, 0.2)',
                            'borderRadius': '5px'
                        },
                        children=[
                            dcc.Checklist(
                                id=f'{component_id}-lineup-checklist',
                                options=lineup_options,
                                value=default_lineups,
                                style={'color': 'white', 'fontSize': '12px'},
                                labelStyle={
                                    'display': 'block',
                                    'marginBottom': '6px',
                                    'cursor': 'pointer'
                                },
                                inputStyle={'marginRight': '8px', 'cursor': 'pointer'}
                            )
                        ]
                    ),

                    # Quick select dropdown
                    html.Div(
                        style={'marginTop': '10px'},
                        children=[
                            html.Label(
                                "Quick Select:",
                                style={
                                    'color': 'white',
                                    'fontSize': '12px',
                                    'marginRight': '8px',
                                    'display': 'inline-block',
                                    'fontWeight': 'bold'
                                }
                            ),
                            dcc.Dropdown(
                                id=f'{component_id}-quick-select',
                                options=[
                                    {'label': 'First 3', 'value': 'first_3'},
                                    {'label': 'Random 3', 'value': 'random_3'},
                                    {'label': 'All (30)', 'value': 'all'},
                                    {'label': 'Clear', 'value': 'clear'}
                                ],
                                placeholder='Quick select...',
                                style={
                                    'width': '150px',
                                    'display': 'inline-block',
                                    'fontSize': '12px'
                                },
                                clearable=False
                            )
                        ]
                    ),

                    # Validation message
                    html.Div(
                        id=f'{component_id}-validation-message',
                        style={
                            'marginTop': '10px',
                            'padding': '8px',
                            'borderRadius': '4px',
                            'fontSize': '12px'
                        }
                    )
                ]
            )
        )

    # Always include the radar chart
    children_list.append(
        # Radar Chart
        html.Div(
            style={
                'backgroundColor': card_color,
                'padding': '15px',
                'borderRadius': '5px',
                'border': f'1px solid {accent_color}'
            },
            children=[
                dcc.Graph(
                    id=f'{component_id}-chart',
                    config={
                        'displayModeBar': True,
                        'displaylogo': False,
                        'toImageButtonOptions': {
                            'format': 'png',
                            'filename': f'{star_player.lower().replace(" ", "_")}_tendency_radar',
                            'height': 1000,
                            'width': 1000,
                            'scale': 2
                        }
                    }
                )
            ]
        )
    )

    # Create and return component
    component = html.Div(
        style={'marginBottom': '30px'},
        children=children_list
    )

    return component


def register_tendency_radar_callbacks(
    app,
    df_tendencies: pd.DataFrame,
    component_id: str = 'tendency-radar',
    star_player: str = 'Luka Dončić',
    external_checklist_id: str = None
):
    """
    Register callbacks for the tendency radar component.

    Args:
        app: Dash app instance
        df_tendencies: DataFrame with normalized tendency data
        component_id: Component ID prefix (must match component creation)
        star_player: Name of star player for chart title
        external_checklist_id: If provided, listen to external checklist instead of internal
    """

    # Determine which checklist to listen to
    checklist_id = external_checklist_id if external_checklist_id else f'{component_id}-lineup-checklist'

    # Quick select callback (only if using internal checklist)
    if not external_checklist_id:
        @app.callback(
            Output(f'{component_id}-lineup-checklist', 'value'),
            Input(f'{component_id}-quick-select', 'value'),
            prevent_initial_call=True
        )
        def quick_select(selection):
            """Handle quick selection dropdown."""
            import random

            if selection == 'first_3':
                return [0, 1, 2]
            elif selection == 'random_3':
                return random.sample(range(len(df_tendencies)), 3)
            elif selection == 'all':
                return list(range(len(df_tendencies)))
            elif selection == 'clear':
                return []

            return [0, 10, 20]

    # Main radar chart callback
    if external_checklist_id:
        # External checklist - no validation messages
        @app.callback(
            Output(f'{component_id}-chart', 'figure'),
            Input(checklist_id, 'value')
        )
        def update_tendency_radar(selected_lineups):
            """Update radar chart based on lineup selection (external checklist)."""
            if not selected_lineups:
                selected_lineups = []

            try:
                fig = create_tendency_radar(
                    df=df_tendencies,
                    selected_lineups=selected_lineups,
                    star_player=star_player,
                    height=400,
                    width=450
                )
                return fig
            except Exception as e:
                print(f"Error creating tendency radar: {e}")
                return create_empty_figure(f"Error: {str(e)}")
    else:
        # Internal checklist - with validation messages
        @app.callback(
            [Output(f'{component_id}-chart', 'figure'),
             Output(f'{component_id}-validation-message', 'children'),
             Output(f'{component_id}-validation-message', 'style')],
            Input(checklist_id, 'value')
        )
        def update_tendency_radar(selected_lineups):
            """Update radar chart based on lineup selection."""
            base_style = {
                'marginTop': '10px',
                'padding': '8px',
                'borderRadius': '4px',
                'fontSize': '12px'
            }

            # Validation
            if not selected_lineups or len(selected_lineups) == 0:
                return (
                    create_empty_figure("Please select at least 1 lineup"),
                    "⚠️ No lineups selected",
                    {**base_style, 'backgroundColor': '#FFC107', 'color': 'black'}
                )

            if len(selected_lineups) == 1:
                message = "ℹ️ Showing 1 lineup. Select 2-5 for comparison."
                style = {**base_style, 'backgroundColor': '#17A2B8', 'color': 'white'}
            elif len(selected_lineups) > 5:
                message = f"⚠️ {len(selected_lineups)} lineups (may be crowded)"
                style = {**base_style, 'backgroundColor': '#FFC107', 'color': 'black'}
            else:
                message = f"✓ Comparing {len(selected_lineups)} lineups"
                style = {**base_style, 'backgroundColor': '#28A745', 'color': 'white'}

            # Create chart
            try:
                fig = create_tendency_radar(
                    df=df_tendencies,
                    selected_lineups=selected_lineups,
                    star_player=star_player,
                    height=400,
                    width=450
                )
                return fig, message, style

            except Exception as e:
                print(f"Error creating tendency radar: {e}")
                return (
                    create_empty_figure(f"Error: {str(e)}"),
                    f"❌ Error: {str(e)}",
                    {**base_style, 'backgroundColor': '#DC3545', 'color': 'white'}
                )


# Example usage documentation
INTEGRATION_EXAMPLE = """
# How to integrate into your main dashboard:

## Step 1: Import in your layout file (src/app/layout.py)

from src.data.load_tendencies import load_tendency_data, normalize_metrics
from src.app.components.tendency_radar import (
    create_tendency_radar_component,
    register_tendency_radar_callbacks
)

# Load data
df_tendencies = load_tendency_data('tendency_graph/luka_team_tendencies_graph_data.csv')
df_tendencies = normalize_metrics(df_tendencies)

## Step 2: Add to your layout

layout = html.Div([
    # ... your existing components ...

    html.Hr(style={'borderColor': '#008080', 'margin': '20px 0'}),

    html.H2(
        "Lineup Tendency Profile",
        style={'textAlign': 'center', 'color': '#008080', 'marginBottom': '20px'}
    ),

    create_tendency_radar_component(
        df_tendencies=df_tendencies,
        default_lineups=[0, 5, 10],  # Customize default selection
        component_id='tendency-radar',
        star_player='Luka Dončić'
    ),

    # ... more components ...
])

## Step 3: Register callbacks (src/app/callbacks.py or __init__.py)

def register_callbacks(app):
    # ... your existing callbacks ...

    # Register tendency radar callbacks
    register_tendency_radar_callbacks(
        app,
        df_tendencies=df_tendencies,
        component_id='tendency-radar',
        star_player='Luka Dončić'
    )

## Done!
The tendency radar chart is now integrated into your dashboard.
"""

if __name__ == '__main__':
    print("="*60)
    print("Tendency Radar Component - Integration Guide")
    print("="*60)
    print(INTEGRATION_EXAMPLE)
