"""Test the new color palette"""
import sys
sys.path.insert(0, 'c:\\Users\\yuval\\NBA-lineup-archetypes-dashboard')

import pandas as pd
from src.app.components.shot_chart import create_zone_shot_chart

# Load sample data
df = pd.read_csv('data/processed/Ready_shots_data.csv')

# Filter to one lineup
first_lineup = df['LINEUP_ARCHETYPE'].unique()[0]
df = df[(df['LINEUP_ARCHETYPE'] == first_lineup)].head(500)

print(f"Testing with {len(df)} shots")

# Create shot chart
fig = create_zone_shot_chart(df)
fig.write_html('test_palette.html')
print(f"✓ Created test_palette.html with new color palette")
print("✓ Palette: Red (bad) -> Orange -> Yellow -> Lime -> Green (good)")
print("✓ Opacity now ranges from 0.15-0.95 for clearer visibility")
