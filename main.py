from src.app.run import create_app
import os

app = create_app()

if __name__ == "__main__":
    print("NBA Dashboard is starting...")
    port = int(os.environ.get("PORT", 8050))
    app.run(debug=False, host="0.0.0.0", port=port)