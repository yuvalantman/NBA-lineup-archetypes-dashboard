import dash
from dash import Dash
import pandas as pd
from src.app.layout import create_layout
from src.app.callbacks import register_callbacks
from src.data.load_players import load_players


def create_app():
    app = Dash(__name__, suppress_callback_exceptions=True)

    # 1. Load Data (Crucial for the dashboard to function)
    try:
        # Update these paths to match your folder structure
        df_players = load_players()
        df_efficiency = pd.read_csv('data/Ready_efficiency_data.csv')
        df_shots = pd.read_csv('data/Ready_shot_data.csv')
        df_tendencies = pd.read_csv('data/Ready_tendencies_data.csv')
        df_team_vs_opp = pd.read_csv('data/Ready_team_vs_opp_data.csv')
        print("✅ Data loaded successfully!")
    except Exception as e:
        print(f"❌ Error loading CSV files: {e}")
        # Fallback to empty DataFrames to prevent a total crash
        df_efficiency = pd.DataFrame()
        df_shots = pd.DataFrame()
        df_team_vs_opp = pd.DataFrame()

    # 2. Your Custom CSS for Dropdown Styling
    app.index_string = '''
    <!DOCTYPE html>
    <html>
        <head>
            {%metas%}
            <title>NBA Lineup Analytics</title>
            {%favicon%}
            {%css%}
            <style>
                .Select-control, .Select-menu-outer, .Select-menu, .VirtualizedSelectOption {
                    font-family: Calibri, sans-serif !important;
                    font-size: 13px !important;
                }
                html, body {
                    background-color: #0b1019 !important;
                    margin: 0;
                    padding: 0;
                }
                .Select-control { background-color: #1a2332 !important; border-color: #00BFFF !important; }
                .Select-menu-outer { background-color: #1a2332 !important; border-color: #00BFFF !important; }
                .Select-menu { background-color: #1a2332 !important; }
                .VirtualizedSelectOption { background-color: #1a2332 !important; color: white !important; }
                .VirtualizedSelectOption:hover { background-color: #2a3642 !important; color: #00BFFF !important; }
                .Select-value { background-color: #008080 !important; border-color: #00BFFF !important; color: white !important; }
                .Select-value-label { color: white !important; }
                .Select-placeholder { color: rgba(255, 255, 255, 0.5) !important; }
                .Select-input > input { color: white !important; }
                .Select-arrow { border-color: #00BFFF transparent transparent !important; }
                
                .custom-clean-dropdown .VirtualizedSelectOption {
                    color: white !important;
                    background-color: #161d2b !important;
                }

                .custom-clean-dropdown .VirtualizedSelectFocusedOption {
                    color: #00BFFF !important;
                    background-color: #1f2a44 !important;
                }

                .custom-clean-dropdown .Select-option {
                    color: #161d2b !important;
                    background-color: #161d2b !important;
                }

                .custom-clean-dropdown .Select-control {
                    background-color: #0b1019 !important;
                    color: #161d2b !important;
                    border: 1px solid #2d384d !important;
                }

                .custom-clean-dropdown .Select-menu-outer {
                    background-color: #161d2b !important;
                    color: #161d2b !important;
                }

                .custom-clean-dropdown .Select-option {
                    background-color: #161d2b !important;
                    color: #161d2b !important;
                }

                .custom-clean-dropdown .Select-option.is-focused {
                    background-color: #1f2a44 !important;
                }

                .custom-clean-dropdown .Select-value-label {
                    color: #161d2b !important;
                }

                .custom-clean-dropdown .Select-placeholder {
                    color: rgba(255,255,255,0.5) !important;
                }
                .custom-clean-dropdown .Select-control .Select-value-label {
                    color: #161d2b !important;
                }

                .custom-clean-dropdown .Select-control .Select-input input {
                    color: #161d2b !important;
                }
                .custom-clean-dropdown .Select-value-label {
                    white-space: nowrap;
                    overflow: hidden;
                    text-overflow: ellipsis;
                    max-width: 320px;
                }

            </style>
        </head>
        <body>
            {%app_entry%}
            <footer>
                {%config%}
                {%scripts%}
                {%renderer%}
            </footer>
        </body>
    </html>
    '''

    # 3. Connect Layout & Callbacks (Passing the loaded data)
    app.layout = create_layout(app, df_players)
    register_callbacks(app, df_players, df_efficiency, df_tendencies, df_shots, df_team_vs_opp)

    return app

if __name__ == "__main__":
    app = create_app()
    app.run_server(debug=True, port=8050)
    