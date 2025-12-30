from dash import Dash
from src.app.layout import create_layout
from src.app.callbacks import register_callbacks

def create_app():
    app = Dash(__name__, suppress_callback_exceptions=True)
    app.index_string = '''
    <!DOCTYPE html>
    <html>
        <head>
            {%metas%}
            <title>NBA Lineup Archetypes</title>
            {%favicon%}
            {%css%}
            <style>
                .Select-control, .Select-menu-outer, .Select-menu, .VirtualizedSelectOption {
                    font-family: Calibri, sans-serif !important;
                    font-size: 13px !important;
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

    # חיבור ה-Layout וה-Callbacks (הלוגיקה של האפליקציה)
    app.layout = create_layout(app)
    register_callbacks(app)

    return app

if __name__ == "__main__":
    app = create_app()
    app.run_server(debug=True, port=8050)