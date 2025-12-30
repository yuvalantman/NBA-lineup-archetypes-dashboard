from src.app.run import create_app

app = create_app()

if __name__ == "__main__":
    print("NBA Dashboard is starting...")
    app.run(debug=True, port=8052)