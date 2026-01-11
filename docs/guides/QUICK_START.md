# Quick Start Guide

## Running the NBA Dashboard in 3 Steps

### Step 1: Activate Virtual Environment

```bash
source .venv/bin/activate
```

You should see `(.venv)` appear at the start of your terminal prompt.

### Step 2: Install Dependencies (First Time Only)

```bash
pip install -r requirements.txt
```

This installs all required packages (Dash, Plotly, Pandas, etc.)

### Step 3: Run the Dashboard

```bash
python main.py
```

You should see:
```
NBA Dashboard is starting...
Dash is running on http://127.0.0.1:8052/
```

### Step 4: Open in Browser

Navigate to: **http://localhost:8052**

---

## Stopping the Dashboard

Press `Ctrl + C` in the terminal

## Deactivating Virtual Environment

```bash
deactivate
```

---

## Troubleshooting

### "Module not found" errors
Make sure you activated the virtual environment first:
```bash
source .venv/bin/activate
pip install -r requirements.txt
```

### Port already in use
Change the port in [main.py](main.py) from 8052 to another number (e.g., 8053)

### Data file errors
Ensure all files are in the correct locations (see full [README.md](README.md))

---

For detailed documentation, see [README.md](README.md)
