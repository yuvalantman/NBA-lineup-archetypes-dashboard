import dash
from graphs import app # Import the configured app and its layout/callbacks

# This entry point ensures the server runs correctly
if __name__ == '__main__':
    # You can change the port or debug mode here
    print("NBA Lineup Intelligence Dashboard is starting...")
    app.run_server(debug=True, port=8050)