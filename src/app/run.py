from dash import Dash
from .layout import create_layout
from .callbacks import register_callbacks

def create_app():
    app = Dash(__name__)
    app.layout = create_layout(app)
    register_callbacks(app)
    return app

if __name__ == "__main__":
    app = create_app()
    app.run_server(debug=True)
