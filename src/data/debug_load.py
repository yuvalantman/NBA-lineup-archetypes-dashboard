import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
import dash.exceptions

# Import the corrected data loading function
from src.data.load_data import load_and_preprocess_data
from sklearn.preprocessing import MinMaxScaler

# --- 1. Data Loading and Initial Setup ---

DF_LINEUPS = load_and_preprocess_data()

# CRITICAL CHECK: Prepare options based on the LINEUP COMBINATION
if DF_LINEUPS.empty:
    print("FATAL: DF_LINEUPS is empty. Dashboard will show placeholders.")
    LINEUP_OPTIONS = [{'label': 'No Data Loaded', 'value': 'None'}]
    INITIAL_LINEUP_ID = 'None'
    INITIAL_LINEUP_IDS = []
else:
    # Assign sequential ID and use the English term "Lineup"
    DF_LINEUPS['COMPACT_LABEL'] = ['Lineup ' + str(i + 1) for i in DF_LINEUPS.index]

    # Options for the Single-Select Dropdown (for emphasis)
    LINEUP_OPTIONS = [{'label': row['COMPACT_LABEL'], 'value': row['LINEUP_ID']}
                      for index, row in DF_LINEUPS.iterrows()]

    # Options for the Multi-Select Checklist (for filtering/comparison)
    CHECKLIST_OPTIONS = [{'label': row['COMPACT_LABEL'], 'value': row['LINEUP_ID']}
                         for index, row in DF_LINEUPS.iterrows()]

    INITIAL_LINEUP_ID = list(DF_LINEUPS['LINEUP_ID'])[0]
    # Default: Initially select ALL lineups for the checklist (as requested)
    INITIAL_LINEUP_IDS = list(DF_LINEUPS['LINEUP_ID'])

# --- Define Custom Styling and Colors ---
CUSTOM_FONT = "Calibri, sans-serif"
GRAPH_HEIGHT = 300
TALL_GRAPH_HEIGHT = 700
COURT_PLOT_HEIGHT = TALL_GRAPH_HEIGHT

BACKGROUND_COLOR = '#1E2833'
CARD_COLOR = '#2A3642'
PLOT_BG_COLOR = 'rgba(0, 139, 139, 0.15)'
HIGHLIGHT_COLOR = 'rgba(0, 139, 139, 0.3)'
MAIN_HEADER_COLOR = '#008080'  # Deep Teal

# Basketball Color Palette (Monochromatic Scale from Brown/Orange)
BASKETBALL_COLOR_SCALE = [
    '#8B4513',  # Darkest Brown
    '#A0522D',
    '#CD853F',
    '#D2B48C',
    '#FFD700'  # Lightest Gold/Yellow
]

# URL for a simple basketball image (used as the visual container)
BASKETBALL_IMAGE_URL = 'https://raw.githubusercontent.com/plotly/datasets/master/basketball-ball-clipart.png'

# Initialize the Dash application
app = dash.Dash(__name__)
server = app.server

# --- 2. Dashboard Layout ---

app.layout = html.Div(className='container',
                      style={'backgroundColor': BACKGROUND_COLOR, 'color': 'white', 'padding': '10px'}, children=[

        html.H1("All-Star Lineup Analysis Dashboard",
                style={'textAlign': 'center', 'color': MAIN_HEADER_COLOR, 'fontFamily': CUSTOM_FONT}),

        html.Div(className='main-content-row',
                 style={'display': 'flex', 'gap': '10px', 'minHeight': f'{TALL_GRAPH_HEIGHT}px'}, children=[

                # --- LEFT COLUMN (Vertical Stack) ---
                html.Div(className='left-column',
                         style={'flex': 1.5, 'display': 'flex', 'flexDirection': 'column', 'gap': '10px'}, children=[

                        # 1. Single-Select Dropdown
                        html.Div(style={'width': '100%', 'backgroundColor': CARD_COLOR, 'padding': '10px',
                                        'borderRadius': '5px'}, children=[
                            html.Label("Select Lineup (for Details):",
                                       style={'fontWeight': 'bold', 'color': 'white', 'fontFamily': CUSTOM_FONT,
                                              'fontSize': '14px'}),
                            dcc.Dropdown(
                                id='lineup-dropdown',
                                options=LINEUP_OPTIONS,
                                value=INITIAL_LINEUP_ID,
                                searchable=False,
                                clearable=False,
                                style={'width': '100%', 'backgroundColor': '#343A40', 'color': 'black',
                                       'fontFamily': CUSTOM_FONT, 'fontSize': '12px'}
                            )
                        ]),

                        # 2. Static Player Card
                        html.Div(id='player-profile-card',
                                 style={'border': '1px solid #00BFFF', 'padding': '10px',
                                        'boxShadow': '2px 2px 10px #00BFFF55', 'backgroundColor': CARD_COLOR,
                                        'height': f'{GRAPH_HEIGHT}px', 'flexShrink': 0},
                                 children=[
                                     html.H4("Star Player (Placeholder)",
                                             style={'textAlign': 'center', 'color': MAIN_HEADER_COLOR,
                                                    'fontFamily': CUSTOM_FONT}),
                                     html.Div(style={'width': '100%', 'height': '150px', 'backgroundColor': '#444',
                                                     'marginBottom': '10px'},
                                              children=html.P("Image Placeholder",
                                                              style={'textAlign': 'center', 'lineHeight': '150px',
                                                                     'color': 'white', 'fontFamily': CUSTOM_FONT})),
                                     html.P("Team: N/A (Static)", style={'color': 'white', 'fontFamily': CUSTOM_FONT}),
                                     html.P("Age: N/A (Static)", style={'color': 'white', 'fontFamily': CUSTOM_FONT}),
                                     html.P("Height: N/A (Static)",
                                            style={'color': 'white', 'fontFamily': CUSTOM_FONT}),
                                 ]),

                        # 3. Bar Plot: Core Metrics (Bottom Left)
                        html.Div(style={'backgroundColor': CARD_COLOR, 'padding': '5px 10px 10px 10px',
                                        'borderRadius': '5px', 'flexGrow': 1}, children=[
                            html.H5("Lineup Comparison: Core Metrics",
                                    style={'textAlign': 'center', 'color': 'white', 'fontFamily': CUSTOM_FONT,
                                           'marginBottom': '0px'}),
                            dcc.Graph(id='bar-comparison-plot', style={'height': GRAPH_HEIGHT})
                        ]),
                    ]),

                # --- CENTER COLUMN (Court Scatter Plot - Tall and Wide) ---
                html.Div(className='center-column',
                         style={'flex': 3, 'backgroundColor': CARD_COLOR, 'padding': '10px', 'borderRadius': '5px'},
                         children=[
                             html.H3("Offensive & Defensive Rating Visualized on Courts",
                                     style={'textAlign': 'center', 'color': 'white', 'fontFamily': CUSTOM_FONT}),
                             dcc.Graph(id='court-scatter-plot', style={'height': f'{COURT_PLOT_HEIGHT - 40}px'})
                         ]),

                # --- RIGHT COLUMN (Vertical Stack) ---
                html.Div(className='right-column',
                         style={'flex': 1.5, 'display': 'flex', 'flexDirection': 'column', 'gap': '10px'}, children=[

                        # 4. Interactive Legend/Checklist (Top Right)
                        html.Div(style={'backgroundColor': CARD_COLOR, 'padding': '10px', 'borderRadius': '5px',
                                        'height': f'{GRAPH_HEIGHT}px', 'overflowY': 'auto'}, children=[
                            html.H4("Lineup Selection (for Comparison)",
                                    style={'textAlign': 'center', 'color': MAIN_HEADER_COLOR,
                                           'fontFamily': CUSTOM_FONT}),

                            # Toggle Button (Select/Deselect All)
                            html.Button('Toggle All Lineups (Select/Deselect)', id='select-all-button', n_clicks=0,
                                        style={'width': '100%', 'backgroundColor': MAIN_HEADER_COLOR, 'color': 'white',
                                               'border': 'none', 'padding': '8px', 'marginBottom': '10px',
                                               'cursor': 'pointer', 'borderRadius': '3px'}),

                            dcc.Loading(
                                id="loading-legend",
                                type="default",
                                children=dcc.Checklist(
                                    id='global-legend-checklist',
                                    options=CHECKLIST_OPTIONS,
                                    value=INITIAL_LINEUP_IDS,  # Default value: ALL IDs
                                    labelStyle={'display': 'flex', 'align-items': 'center', 'padding': '5px 0',
                                                'color': 'white'},
                                    style={'maxHeight': '100%', 'overflowY': 'auto'}
                                )
                            )
                        ]),

                        # 5. Advanced Metrics Bar Chart (Bottom Right)
                        html.Div(style={'backgroundColor': CARD_COLOR, 'padding': '5px 10px 10px 10px',
                                        'borderRadius': '5px', 'flexGrow': 1}, children=[
                            html.H5("Advanced Metrics Breakdown",
                                    style={'textAlign': 'center', 'color': 'white', 'fontFamily': CUSTOM_FONT,
                                           'marginBottom': '0px'}),
                            dcc.Graph(id='pie-comparison-chart', style={'height': GRAPH_HEIGHT})
                            # Retain ID for compatibility
                        ]),
                    ]),
            ]),
    ])


# --- 3. Callbacks ---

# Helper function for default figure (Custom Style)
def get_custom_figure(text="No data available or error in selection.", height=GRAPH_HEIGHT):
    fig = go.Figure()
    fig.add_annotation(text=text, xref="paper", yref="paper", x=0.5, y=0.5, showarrow=False)
    fig.update_layout(
        template='plotly_dark',
        height=height,
        plot_bgcolor=PLOT_BG_COLOR,
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family=CUSTOM_FONT),
    )
    return fig


# --- Basketball Court Definitions ---
COURT_SHAPES = [
    dict(type='rect', x0=0, y0=0, x1=50, y1=47, line=dict(color='white', width=1)),
    dict(type='circle', x0=23.5, y0=45, x1=26.5, y1=48, line=dict(color='white', width=1)),
    dict(type='line', x0=21.5, y0=47, x1=28.5, y1=47, line=dict(color='white', width=1)),
    dict(type='rect', x0=17, y0=0, x1=33, y1=47, line=dict(color='white', width=1)),
    dict(type='path', path='M 18 47 C 18 35, 32 35, 32 47', line=dict(color='white', width=1)),
    dict(type='path', path='M 0 47 C 0 10, 50 10, 50 47', line=dict(color='white', width=1)),
]


# Callback 1: Select/Deselect All Button Logic (Toggle)
@app.callback(
    Output('global-legend-checklist', 'value'),
    [Input('select-all-button', 'n_clicks')],
    [State('global-legend-checklist', 'options')]
)
def select_all_lineups(n_clicks, options):
    if n_clicks is None or n_clicks == 0:
        raise dash.exceptions.PreventUpdate

    all_values = [opt['value'] for opt in options]

    if n_clicks % 2 == 0:
        # Even click: Select all
        return all_values
    else:
        # Odd click: Deselect all
        return []


# Callback 2: Checklist Styling (Maintains hover and coloring logic)
@app.callback(
    Output('global-legend-checklist', 'options'),
    [Input('global-legend-checklist', 'value')]
)
def update_checklist_styles(selected_ids):
    if DF_LINEUPS.empty:
        return []

    unique_combos = DF_LINEUPS[['LINEUP_ID', 'LINEUP_COMBINATION', 'COMPACT_LABEL']].drop_duplicates()
    options_with_hover_and_style = []

    color_map = {
        row['LINEUP_ID']: BASKETBALL_COLOR_SCALE[i % len(BASKETBALL_COLOR_SCALE)]
        for i, row in unique_combos.iterrows()
    }

    for index, row in unique_combos.iterrows():
        lineup_id = row['LINEUP_ID']
        compact_label = row['COMPACT_LABEL']
        full_combo = row['LINEUP_COMBINATION']
        color = color_map.get(lineup_id, 'white')

        is_selected = lineup_id in selected_ids

        custom_label = html.Div(
            title=full_combo,
            style={
                'display': 'flex',
                'alignItems': 'center',
                'fontWeight': 'bold' if is_selected else 'normal',
                'padding': '3px',
                'cursor': 'pointer',
                'backgroundColor': HIGHLIGHT_COLOR if is_selected else 'transparent'
            },
            children=[
                html.Div(style={'backgroundColor': color, 'width': '10px', 'height': '10px', 'borderRadius': '50%',
                                'marginRight': '8px'}),
                html.Span(compact_label, style={'fontSize': '12px', 'color': 'white', 'fontFamily': CUSTOM_FONT})
            ]
        )

        options_with_hover_and_style.append({
            'label': custom_label,
            'value': lineup_id,
            'title': full_combo
        })

    return options_with_hover_and_style


# Callback 3: Update Court Scatter Plot (Two Subplots)
@app.callback(
    Output('court-scatter-plot', 'figure'),
    [Input('global-legend-checklist', 'value')],
    [State('lineup-dropdown', 'value')]
)
def update_court_scatter(selected_checklist_ids, selected_dropdown_id):
    if not selected_checklist_ids or DF_LINEUPS.empty:
        return get_custom_figure("Select at least one Lineup for comparison.", height=COURT_PLOT_HEIGHT - 40)

    filtered_df = DF_LINEUPS[DF_LINEUPS['LINEUP_ID'].isin(selected_checklist_ids)].copy()

    if filtered_df.empty:
        return get_custom_figure("No data for selected lineups.", height=COURT_PLOT_HEIGHT - 40)

    all_ratings = pd.concat([filtered_df['OFFENSIVE_RATING'], filtered_df['DEFENSIVE_RATING']])
    max_val = all_ratings.max()
    min_val = all_ratings.min()

    def normalize_rating(rating):
        return ((rating - min_val) / (max_val - min_val)) * 50

    filtered_df['OFFENSE_X'] = normalize_rating(filtered_df['OFFENSIVE_RATING'])
    filtered_df['DEFENSE_Y'] = normalize_rating(filtered_df['DEFENSIVE_RATING'])

    fig = make_subplots(
        rows=2, cols=1,
        shared_xaxes=False,
        shared_yaxes=True,
        vertical_spacing=0.05,
        subplot_titles=("Offensive Efficiency (Score = X, Opponent Score = Y)",
                        "Defensive Efficiency (Opponent Score = X, Your Score = Y)")
    )

    full_df_indexed = DF_LINEUPS.set_index('LINEUP_ID')
    filtered_df['COLOR_INDEX'] = filtered_df['LINEUP_ID'].apply(
        lambda x: full_df_indexed.index.get_loc(x) % len(BASKETBALL_COLOR_SCALE)
    )
    filtered_df['HOVER_TEXT'] = filtered_df['LINEUP_COMBINATION'] + '<br>' + filtered_df['COMPACT_LABEL']

    color_scale_plotly = [[i / (len(BASKETBALL_COLOR_SCALE) - 1), color] for i, color in
                          enumerate(BASKETBALL_COLOR_SCALE)]

    # --- Court 1: Offensive Visualization (Top Row) ---

    fig.add_trace(go.Scatter(
        x=filtered_df['OFFENSE_X'],
        y=filtered_df['DEFENSE_Y'],
        mode='markers',
        marker=dict(
            size=filtered_df['POSSESSIONS'].apply(lambda x: np.log10(x) * 5 + 5 if x > 0 else 5),
            color=filtered_df['COLOR_INDEX'],
            colorscale=color_scale_plotly,
            showscale=False,
            cmin=0, cmax=len(BASKETBALL_COLOR_SCALE) - 1,
            opacity=0.8
        ),
        text=filtered_df['HOVER_TEXT'] + filtered_df.apply(
            lambda row: f"<br>OFF Rtg: {row['OFFENSIVE_RATING']:.2f}<br>DEF Rtg: {row['DEFENSIVE_RATING']:.2f}",
            axis=1),
        hovertemplate='%{text}<extra></extra>',
        name='Offense',
        showlegend=False
    ), row=1, col=1)

    # --- Court 2: Defensive Visualization (Bottom Row) ---

    fig.add_trace(go.Scatter(
        x=filtered_df['DEFENSE_Y'],
        y=filtered_df['OFFENSE_X'],
        mode='markers',
        marker=dict(
            size=filtered_df['POSSESSIONS'].apply(lambda x: np.log10(x) * 5 + 5 if x > 0 else 5),
            color=filtered_df['COLOR_INDEX'],
            colorscale=color_scale_plotly,
            showscale=False,
            cmin=0, cmax=len(BASKETBALL_COLOR_SCALE) - 1,
            opacity=0.8
        ),
        text=filtered_df['HOVER_TEXT'] + filtered_df.apply(
            lambda row: f"<br>DEF Rtg: {row['DEFENSIVE_RATING']:.2f}<br>OFF Rtg: {row['OFFENSIVE_RATING']:.2f}",
            axis=1),
        hovertemplate='%{text}<extra></extra>',
        name='Defense',
        showlegend=False
    ), row=2, col=1)

    # 4. Highlight the selected lineup (from the Dropdown)
    selected_row = filtered_df[filtered_df['LINEUP_ID'] == selected_dropdown_id]
    if not selected_row.empty:
        selected_x_offense = selected_row['OFFENSE_X']
        selected_y_defense = selected_row['DEFENSE_Y']

        # Highlight in Court 1
        fig.add_trace(go.Scatter(
            x=selected_x_offense,
            y=selected_y_defense,
            mode='markers',
            marker=dict(size=20, color='red', symbol='star-open', line=dict(width=2, color='white')),
            name='Selected Lineup (Offense)',
            hovertemplate=f"Selected: {selected_row['LINEUP_COMBINATION'].iloc[0]}<extra></extra>"
        ), row=1, col=1)

        # Highlight in Court 2
        fig.add_trace(go.Scatter(
            x=selected_y_defense,
            y=selected_x_offense,
            mode='markers',
            marker=dict(size=20, color='red', symbol='star-open', line=dict(width=2, color='white')),
            name='Selected Lineup (Defense)',
            hovertemplate=f"Selected: {selected_row['LINEUP_COMBINATION'].iloc[0]}<extra></extra>"
        ), row=2, col=1)

    # 5. Apply styling and Court Shapes to BOTH Subplots

    axis_layout = dict(
        range=[0, 50], showgrid=False, zeroline=False, visible=False, scaleanchor="x", scaleratio=1
    )

    fig.update_xaxes(axis_layout, row=1, col=1)
    fig.update_yaxes(axis_layout, row=1, col=1)
    fig.update_xaxes(axis_layout, row=2, col=1)
    fig.update_yaxes(axis_layout, row=2, col=1)

    for shape in COURT_SHAPES:
        fig.add_shape(shape, row=1, col=1)
        fig.add_shape(shape, row=2, col=1)

    # 6. Final Layout Update
    fig.update_layout(
        title={
            'text': 'Offensive & Defensive Rating Visualized on Courts',
            'y': 0.98, 'x': 0.5, 'xanchor': 'center', 'yanchor': 'top'
        },
        template='plotly_dark',
        plot_bgcolor=PLOT_BG_COLOR,
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family=CUSTOM_FONT),
        showlegend=False,
        height=COURT_PLOT_HEIGHT - 40,
        margin=dict(t=50, b=10, l=10, r=10)
    )

    return fig


# Callback 4: Update Bar Plot (Logic remains the same)
@app.callback(
    Output('bar-comparison-plot', 'figure'),
    [Input('global-legend-checklist', 'value')]
)
def update_bar_plot(selected_checklist_ids):
    if not selected_checklist_ids or DF_LINEUPS.empty:
        return get_custom_figure("Select lineups for comparison.")

    df_plot = DF_LINEUPS[DF_LINEUPS['LINEUP_ID'].isin(selected_checklist_ids)].copy()

    if df_plot.empty:
        return get_custom_figure("No data for selected lineups.")

    metrics = ['NET_RATING', 'PACE', 'REBOUND_PERCENTAGE', 'TURNOVER_PERCENTAGE']

    color_map = {
        row['COMPACT_LABEL']: BASKETBALL_COLOR_SCALE[i % len(BASKETBALL_COLOR_SCALE)]
        for i, row in DF_LINEUPS.iterrows()
    }

    df_melt = df_plot.melt(
        id_vars=['LINEUP_ID', 'COMPACT_LABEL'],
        value_vars=[m for m in metrics if m in df_plot.columns],
        var_name='Metric',
        value_name='Value'
    )

    fig = px.bar(
        df_melt,
        y='Metric',
        x='Value',
        color='COMPACT_LABEL',
        barmode='group',
        orientation='h',
        title='Core Metrics per Lineup (Color by Lineup)',
        template='plotly_dark',
        color_discrete_map=color_map
    )

    fig.update_yaxes(title='')
    fig.update_layout(
        plot_bgcolor=PLOT_BG_COLOR,
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family=CUSTOM_FONT, size=10),
        height=GRAPH_HEIGHT,
        showlegend=False,
        margin=dict(l=10, r=10, t=20, b=10)
    )

    return fig


# Callback 5: Update Advanced Metrics Breakdown (Bar Chart - UPDATED)
@app.callback(
    Output('pie-comparison-chart', 'figure'),
    [Input('lineup-dropdown', 'value')]
)
def update_advanced_metrics_bar_chart(selected_lineup_id):
    if selected_lineup_id in ['None', None] or DF_LINEUPS.empty:
        return get_custom_figure()

    # Locate the specific row for the selected lineup
    filtered_row_df = DF_LINEUPS[DF_LINEUPS['LINEUP_ID'] == selected_lineup_id]

    if filtered_row_df.empty:
        return get_custom_figure("Error filtering selected lineup.")

    filtered_row = filtered_row_df.iloc[0]  # Get the specific row data

    advanced_metrics_list = [
        'REBOUNDS_PER48', 'ASSISTS_PER48', 'STEALS_PER48', 'BLOCKS_PER48', 'PLUS_MINUS_PER48'
    ]

    # Create DataFrame for plotting
    available_data = filtered_row[
        [m for m in advanced_metrics_list if m in filtered_row.index]
    ].T.reset_index()
    available_data.columns = ['Metric', 'Value']

    # Add player names and compact label for hover
    player_names = filtered_row['LINEUP_COMBINATION']
    compact_label = filtered_row['COMPACT_LABEL']

    # Normalization for coloring (optional but keeps visual consistency)
    scaler = MinMaxScaler()
    available_data['Color_Value'] = scaler.fit_transform(available_data[['Value']].clip(lower=0))

    # Create Bar Chart (Horizontal Orientation for better labeling)
    fig = px.bar(
        available_data,
        x='Value',
        y='Metric',
        orientation='h',
        color='Color_Value',
        color_continuous_scale=BASKETBALL_COLOR_SCALE,
        template='plotly_dark'
    )

    # Customize the hover tooltip
    custom_hover_template = (
        f"<b>{compact_label}</b>: {player_names}<br>"
        "Metric: %{y}<br>"
        "Value: %{x:.2f}<extra></extra>"
    )

    fig.update_traces(
        hovertemplate=custom_hover_template,
        marker=dict(line=dict(width=1, color=CARD_COLOR))  # Add border to bars
    )

    # Final Layout Configuration
    fig.update_layout(
        title={
            'text': 'Advanced Metrics Breakdown',
            'x': 0.5, 'xanchor': 'center',
            'font': {'size': 14}
        },
        plot_bgcolor=PLOT_BG_COLOR,
        paper_bgcolor=CARD_COLOR,
        font=dict(family=CUSTOM_FONT, size=10),
        height=GRAPH_HEIGHT,
        showlegend=False,
        margin=dict(l=10, r=10, t=20, b=10),
        xaxis_title="Value",
        yaxis_title="",  # Clear y-axis title as Metric names are used

        # ADDED: Basketball image as background (opacity 0.2)
        images=[dict(
            source=BASKETBALL_IMAGE_URL,
            xref="paper", yref="paper",
            x=0.5, y=0.5,
            sizex=1.5, sizey=1.5,
            xanchor="center", yanchor="middle",
            layer="below",
            opacity=0.2
        )],
        coloraxis_showscale=False  # Hide the continuous color scale legend
    )

    return fig


if __name__ == '__main__':
    app.run(debug=True)