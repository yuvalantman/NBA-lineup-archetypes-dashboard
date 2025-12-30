# ⚡ START HERE - Run Your Dashboard

## ✅ All Issues Fixed!

The import errors have been resolved. Follow these 3 steps:

---

## 🚀 Step-by-Step Instructions

### Step 1: Activate Virtual Environment ⚙️

Open Terminal and run:

```bash
source .venv/bin/activate
```

✅ You should see `(.venv)` appear at the start of your prompt.

---

### Step 2: Install Dependencies 📦

**IMPORTANT**: Only need to do this ONCE (first time):

```bash
pip install -r requirements.txt
```

This will install:
- ✅ Dash (web framework)
- ✅ Plotly (visualizations)
- ✅ Pandas (data handling)
- ✅ NumPy (numerical operations)
- ✅ NBA API (NBA data)
- ✅ scikit-learn (ML utilities)

Wait for it to finish... (takes ~1-2 minutes)

---

### Step 3: Run the Dashboard 🎯

```bash
python main.py
```

You should see:

```
NBA Dashboard is starting...
Dash is running on http://127.0.0.1:8052/

 * Serving Flask app 'run'
 * Debug mode: on
WARNING: This is a development server.
```

---

### Step 4: Open in Browser 🌐

Open your web browser and go to:

## **http://localhost:8052**

You should see the NBA Lineup Analysis Dashboard!

---

## 🎉 What You'll See

1. **Top Left** - Star player dropdown
2. **Left Column** - Player profile with photo and stats
3. **Center** - Interactive shot chart
4. **Top Right** - Lineup selector
5. **Right Column** - Efficiency landscape & tendency radar

---

## 🛑 Stop the Dashboard

Press `Ctrl + C` in the Terminal

---

## ❓ Troubleshooting

### "Module not found" Error

Make sure you:
1. Activated virtual environment: `source .venv/bin/activate`
2. Installed dependencies: `pip install -r requirements.txt`

### Port Already in Use

Edit `main.py` and change:
```python
app.run(debug=True, port=8053)  # Change 8052 to 8053
```

### Still Having Issues?

Check [FINAL_SETUP.md](FINAL_SETUP.md) for detailed troubleshooting.

---

## ✅ Summary

```bash
# 1. Activate
source .venv/bin/activate

# 2. Install (first time only)
pip install -r requirements.txt

# 3. Run
python main.py

# 4. Open browser → http://localhost:8052
```

That's it! 🎯
