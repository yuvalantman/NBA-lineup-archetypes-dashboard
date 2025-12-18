import dash
from dash import dcc, html, Input, Output, State
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
import os
from pathlib import Path

# --- 1. THEME & STYLE ---
DARK_BLUE_BG = '#0B1622'
CARD_BLUE_BG = '#152232'
TEXT_LIGHT = '#E0E6ED'
ACCENT_ORANGE = '#FF6B35'
HIGHLIGHT_COLOR = 'rgba(255, 107, 53, 0.2)'
CUSTOM_FONT = 'Segoe UI, sans-serif'
LINEUP_COLORS = [
    '#FF6B35', '#E35E2D', '#C75125', '#AB441D',
    '#8F3715', '#732A0D', '#571D05', '#FF8C42'
]
# --- 2. DATA LOADING ---
# Paths provided by you
# 1. Get the directory where THIS file (graphs.py) is located
# current_file_path will be: /Users/tomerfilo/Downloads/clusters/src/app/
current_file_path = Path(__file__).resolve().parent

# 2. Go up two levels to reach the project root (clusters/)
project_root = current_file_path.parent.parent

# 3. Define the data directory relative to the project root
DATA_DIR = project_root / "data" / "processed"

# 4. Update your PATH constants using the resolved directory
PATH_BIO = str(DATA_DIR / 'allstar_data.csv')
PATH_EFF = str(DATA_DIR / 'luka_efficiency_graph_data.csv')
PATH_METRICS = str(DATA_DIR / 'luka_metrics_graph_data.csv')
PATH_TENDENCIES = str(DATA_DIR / 'luka_team_tendencies_graph_data.csv')

def prepare_data():
    # Load Efficiency Data (Main for Lineup selection)
    df_eff = pd.read_csv(PATH_EFF)
    df_eff.columns = [c.lower() for c in df_eff.columns]

    # Archetype combination logic
    arch_cols = ['star_player', 'player1_archetype', 'player2_archetype', 'player3_archetype', 'player4_archetype']
    df_eff['lineup_id'] = range(len(df_eff))
    df_eff['combination'] = df_eff[arch_cols].apply(lambda x: ' | '.join(x.values.astype(str)), axis=1)

    # Load other tables
    df_bio = pd.read_csv(PATH_BIO)
    df_bio.columns = [c.upper() for c in df_bio.columns]

    df_metrics = pd.read_csv(PATH_METRICS)
    df_metrics.columns = [c.lower() for c in df_metrics.columns]

    df_tendencies = pd.read_csv(PATH_TENDENCIES)
    df_tendencies.columns = [c.lower() for c in df_tendencies.columns]

    return df_bio, df_eff, df_metrics, df_tendencies


DF_BIO, DF_EFF, DF_METRICS, DF_TENDENCIES = prepare_data()

# --- 3. COURT SHAPES ---
COURT_SHAPES = [
    dict(type='rect', x0=0, y0=0, x1=50, y1=47, line=dict(color='white', width=1)),
    dict(type='circle', x0=23.5, y0=45, x1=26.5, y1=48, line=dict(color='white', width=1)),
    dict(type='line', x0=21.5, y0=47, x1=28.5, y1=47, line=dict(color='white', width=1)),
    dict(type='rect', x0=17, y0=0, x1=33, y1=47, line=dict(color='white', width=1)),
    dict(type='path', path='M 18 47 C 18 35, 32 35, 32 47', line=dict(color='white', width=1)),
    dict(type='path', path='M 0 47 C 0 10, 50 10, 50 47', line=dict(color='white', width=1)),
]

# --- 4. DASH INITIALIZATION ---
# --- 4. DASH INITIALIZATION ---
app = dash.Dash(__name__)

app.layout = html.Div(
    style={'backgroundColor': DARK_BLUE_BG, 'color': TEXT_LIGHT, 'fontFamily': CUSTOM_FONT, 'padding': '20px'},
    children=[
        # Header
        html.Div(
            style={
                'display': 'flex',
                'justifyContent': 'center',
                'alignItems': 'center',
                'position': 'relative',
                'borderBottom': f'2px solid {ACCENT_ORANGE}',
                'paddingBottom': '10px'
            },
            children=[
                html.H1("NBA Lineup Intelligence", style={'margin': 0, 'textAlign': 'center'}),
                html.Img(
                    src="https://cdn.nba.com/logos/leagues/logo-nba.svg",
                    style={'height': '50px', 'position': 'absolute', 'right': '0'}
                )
            ]  # This closes the 'children' list
        ),
        # Main Grid (3 Columns)
        html.Div(style={'display': 'flex', 'gap': '20px', 'marginTop': '20px'}, children=[

            # Column 1: Bio & Tendencies
            html.Div(style={'flex': '1.2', 'display': 'flex', 'flexDirection': 'column', 'gap': '20px'}, children=[
                # Player Selector Div
                html.Div(style={'backgroundColor': CARD_BLUE_BG, 'padding': '15px', 'borderRadius': '15px'}, children=[
                    html.P("SELECT PLAYER", style={'color': ACCENT_ORANGE, 'fontSize': '10px', 'fontWeight': 'bold',
                                                   'margin': '0 0 5px 0'}),
                    dcc.Dropdown(
                        id='star-player-dropdown',
                        options=[{'label': name, 'value': name} for name in DF_BIO['PLAYER'].unique()],
                        value=DF_BIO['PLAYER'].iloc[0],
                        clearable=False,
                        style={'backgroundColor': DARK_BLUE_BG, 'color': 'black'}
                    )
                ]),  # Closes Selector Div

                html.Div(id='bio-card', style={
                    'backgroundColor': CARD_BLUE_BG,
                    'padding': '25px',
                    'borderRadius': '12px',
                    'borderLeft': f'4px solid {ACCENT_ORANGE}'
                }),
                dcc.Graph(id='tendencies-scatter')

            ]),
            # Column 2: Courts (Middle)
            html.Div(style={'flex': '2.5', 'backgroundColor': CARD_BLUE_BG, 'borderRadius': '15px', 'padding': '15px'},
                     children=[
                         html.H3("EFFICIENCY ON COURTS", style={'textAlign': 'center', 'color': ACCENT_ORANGE}),
                         dcc.Graph(id='court-plot', style={'height': '900px'}, config={'displayModeBar': False})
                     ]),

            # Column 3: Legend & Radar
            html.Div(style={'flex': '1.5', 'display': 'flex', 'flexDirection': 'column', 'gap': '20px'}, children=[
                # Legend container
                html.Div(style={'backgroundColor': CARD_BLUE_BG, 'padding': '20px', 'borderRadius': '15px'}, children=[
                    html.H4("COMPARE LINEUPS", style={'color': ACCENT_ORANGE}),
                    html.Button("Toggle All Lineups", id="select-all-button", n_clicks=0,
                                style={'width': '100%', 'backgroundColor': '#1C4B4F', 'color': 'white',
                                       'border': 'none', 'borderRadius': '5px', 'padding': '10px', 'marginBottom': '10px',
                                       'cursor': 'pointer'}),
                    dcc.Checklist(
                        id='lineup-checklist',
                        value=DF_EFF['lineup_id'].tolist(),
                        options=[{
                            'label': html.Div([
                                html.Div(style={
                                    'backgroundColor': LINEUP_COLORS[i % len(LINEUP_COLORS)],
                                    'width': '12px', 'height': '12px',
                                    'borderRadius': '50%', 'display': 'inline-block', 'marginRight': '8px'
                                }),
                                html.Span(
                                    f"Lineup {i + 1}",
                                    title=row['combination'],
                                    style={'fontSize': '14px', 'fontWeight': 'bold', 'cursor': 'help'}
                                ),
                            ]),
                            'value': row['lineup_id']
                        } for i, row in DF_EFF.iterrows()],
                        style={'maxHeight': '400px', 'overflowY': 'auto'}
                    )
                ]),
                # Radar container
                html.Div(style={'backgroundColor': CARD_BLUE_BG, 'padding': '15px', 'borderRadius': '15px'}, children=[
                    html.H5("LINEUP METRICS", style={'textAlign': 'center', 'color': ACCENT_ORANGE}),
                    dcc.Graph(id='radar-plot', style={'height': '450px'}, config={'displayModeBar': False})
                ])
            ]) # End Column 3
        ]) # End Main Grid
    ]
)

# --- 5. CALLBACKS ---

# 1. Update Bio Card
@app.callback(Output('bio-card', 'children'), [Input('star-player-dropdown', 'value')])
def update_bio(selected_player):
    player_data = DF_BIO[DF_BIO['PLAYER'] == selected_player].iloc[0]

    return [
        html.Div("★", style={'position': 'absolute', 'top': '-10px', 'right': '10px', 'color': ACCENT_ORANGE,
                             'fontSize': '30px'}),
        html.Div(style={
            'width': '100px', 'height': '100px', 'borderRadius': '50%', 'border': f'3px solid {ACCENT_ORANGE}',
            'margin': '0 auto', 'backgroundColor': '#122B44', 'display': 'flex', 'alignItems': 'center',
            'justifyContent': 'center'
        }, children=[html.Span("PHOTO", style={'color': TEXT_LIGHT, 'opacity': 0.3})]),

        html.H2(player_data['PLAYER'], style={'textAlign': 'center', 'fontSize': '18px', 'marginTop': '10px'}),
        html.P(f"ID: {player_data['PLAYER_ID']}", style={'textAlign': 'center', 'fontSize': '10px', 'opacity': 0.6}),

        html.Div(style={'display': 'flex', 'justifyContent': 'space-around', 'backgroundColor': DARK_BLUE_BG,
                        'padding': '8px', 'borderRadius': '10px', 'marginTop': '10px'}, children=[
            html.Div([html.P("HT", style={'fontSize': '9px', 'color': ACCENT_ORANGE, 'margin': 0}),
                      html.B(player_data['HEIGHT'])]),
            html.Div([html.P("WT", style={'fontSize': '9px', 'color': ACCENT_ORANGE, 'margin': 0}),
                      html.B(player_data['WEIGHT'])]),
            html.Div([html.P("POS", style={'fontSize': '9px', 'color': ACCENT_ORANGE, 'margin': 0}),
                      html.B(player_data['POSITION'])])
        ]),
        html.P(f"DRAFT: {player_data['DRAFT YEAR']} | TEAM: {player_data['CURRENT_TEAM']}",
               style={'textAlign': 'center', 'marginTop': '10px', 'fontSize': '11px', 'fontWeight': 'bold'})
    ]


# 2. Update Court Efficiency
@app.callback(Output('court-plot', 'figure'), [Input('lineup-checklist', 'value')])
def update_courts(selected_ids):
    fig = make_subplots(rows=2, cols=1, vertical_spacing=0.05, subplot_titles=("Offensive Rating", "Defensive Rating"))

    # Normalization helper
    all_rtg = pd.concat([DF_EFF['offensive_rating'], DF_EFF['defensive_rating']])
    v_min, v_max = all_rtg.min(), all_rtg.max()

    def norm(v):
        return ((v - v_min) / (v_max - v_min + 1)) * 40 + 5

    for i, lid in enumerate(selected_ids):
        row = DF_EFF[DF_EFF['lineup_id'] == lid].iloc[0]
        color = LINEUP_COLORS[i % len(LINEUP_COLORS)]

        fig.add_trace(go.Scatter(
            x=[norm(row['offensive_rating'])], y=[23.5],
            mode='markers',
            marker=dict(size=18, color=color, line=dict(width=0)),
            name=row['combination'],
            hovertemplate=f"<b>Lineup:</b> {row['combination']}<br><b>Off Rtg:</b> %{{x}}<extra></extra>",
            showlegend=False
        ), row=1, col=1)

        # Defense (Row 2)
        fig.add_trace(go.Scatter(
            x=[norm(row['defensive_rating'])], y=[23.5],
            mode='markers',
            marker=dict(size=18, color=color, line=dict(width=0)),
            hovertemplate=f"<b>Lineup:</b> {row['combination']}<br><b>Def Rtg:</b> %{{x}}<extra></extra>",
            showlegend=False
        ), row=2, col=1)

    for r in [1, 2]:
        for shape in COURT_SHAPES:
            fig.add_shape(shape, row=r, col=1)
        fig.update_xaxes(range=[0, 50], visible=False, row=r, col=1)
        fig.update_yaxes(range=[0, 50], visible=False, scaleanchor="x", scaleratio=1, row=r, col=1)

    fig.update_layout(
        margin=dict(l=40, r=40, t=40, b=40),
        template='plotly_dark',
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        showlegend=False
    )
    return fig


# 3. Update Radar Plot (Metrics)
@app.callback(Output('radar-plot', 'figure'), [Input('lineup-checklist', 'value')])
def update_radar(selected_ids):
    fig = go.Figure()
    categories = ['pace', 'turnover_percentage', 'assist_percentage', 'rebound_percentage', 'blocks_per48',
                  'steals_per48']

    for i, lid in enumerate(selected_ids):
        row = DF_METRICS.iloc[lid]
        color = LINEUP_COLORS[i % len(LINEUP_COLORS)]
        fig.add_trace(go.Scatterpolar(r=[row[c] for c in categories] + [row[categories[0]]],
                                      theta=categories + [categories[0]], fill='toself', name=f"L{lid}",
                                      line_color=color))

    fig.update_layout(polar=dict(bgcolor=DARK_BLUE_BG, radialaxis=dict(visible=False), gridshape='linear'), paper_bgcolor='rgba(0,0,0,0)',
                      template='plotly_dark', showlegend=False)
    return fig


# 4. Update Tendencies (Bottom Left)
@app.callback(Output('tendencies-scatter', 'figure'), [Input('lineup-checklist', 'value')])
def update_tendencies_scatter(selected_ids):
    fig = go.Figure()

    for i, lid in enumerate(selected_ids):
        row = DF_TENDENCIES.iloc[lid]
        color = LINEUP_COLORS[i % len(LINEUP_COLORS)]

        fig.add_trace(go.Scatter(
            x=[row['points_in_paint']],
            y=[row['three_pa_per48']],
            mode='markers+text',
            text=[f"L{lid}"],
            textposition="top center",
            marker=dict(size=15, color=color, line=dict(width=1, color='white')),
            name=f"Lineup {lid}"
        ))

    fig.update_layout(
        template='plotly_dark',
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(255,255,255,0.05)',
        xaxis=dict(title="Points in Paint", gridcolor='#333'),
        yaxis=dict(title="3PA per 48", gridcolor='#333'),
        margin=dict(l=40, r=20, t=20, b=40),
        showlegend=False
    )
    return fig

@app.callback(
    Output('lineup-checklist', 'value'),
    [Input('select-all-button', 'n_clicks')],
    [State('lineup-checklist', 'options')]
)
def toggle_all(n_clicks, options):
    all_values = [option['value'] for option in options]
    if n_clicks % 2 == 0:
        return all_values
    return []

if __name__ == '__main__':
    app.run(debug=True)