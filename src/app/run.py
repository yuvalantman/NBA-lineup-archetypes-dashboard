from dash import Dash
<<<<<<< HEAD
from src.app.layout import create_layout
from src.app.callbacks import register_callbacks

def create_app():
    app = Dash(__name__, suppress_callback_exceptions=True)

    # Add custom CSS for dropdown styling
    app.index_string = '''
    <!DOCTYPE html>
    <html>
        <head>
            {%metas%}
            <title>{%title%}</title>
            {%favicon%}
            {%css%}
            <style>
                /* Custom dropdown styling */
                .Select-control,
                .Select-menu-outer,
                .Select-menu,
                .VirtualizedSelectOption {
                    font-family: Calibri, sans-serif !important;
                    font-size: 13px !important;
                }

                /* Dropdown background - dark blue */
                .Select-control {
                    background-color: #1a2332 !important;
                    border-color: #00BFFF !important;
                }

                .Select-menu-outer {
                    background-color: #1a2332 !important;
                    border-color: #00BFFF !important;
                }

                .Select-menu {
                    background-color: #1a2332 !important;
                }

                /* Dropdown options */
                .VirtualizedSelectOption {
                    background-color: #1a2332 !important;
                    color: white !important;
                }

                .VirtualizedSelectOption:hover {
                    background-color: #2a3642 !important;
                    color: #00BFFF !important;
                }

                .VirtualizedSelectFocusedOption {
                    background-color: #2a3642 !important;
                    color: #00BFFF !important;
                }

                /* Selected values */
                .Select-value {
                    background-color: #008080 !important;
                    border-color: #00BFFF !important;
                    color: white !important;
                }

                .Select-value-label {
                    color: white !important;
                }

                /* Placeholder text */
                .Select-placeholder {
                    color: rgba(255, 255, 255, 0.5) !important;
                }

                /* Input text */
                .Select-input > input {
                    color: white !important;
                }

                /* Arrow */
                .Select-arrow {
                    border-color: #00BFFF transparent transparent !important;
                }

                /* Multi-select: Hide individual value chips, show only count */
                #lineup-comparison-dropdown .Select-value {
                    display: none !important;
                }

                /* Show placeholder or custom text when items are selected */
                #lineup-comparison-dropdown .Select-value-label {
                    display: none !important;
                }

                /* Keep only the input visible to show selection count via placeholder */
                #lineup-comparison-dropdown .Select-multi-value-wrapper {
                    max-height: 38px !important;
                    overflow: hidden !important;
                }

                /* Hide the X buttons on multi-select chips */
                #lineup-comparison-dropdown .Select-value-icon {
                    display: none !important;
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

=======
from .layout import create_layout
from .callbacks import register_callbacks

def create_app():
    app = Dash(__name__)
>>>>>>> 35217567569a3e4a4d5abe233313123ba3bbeed6
    app.layout = create_layout(app)
    register_callbacks(app)
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)

