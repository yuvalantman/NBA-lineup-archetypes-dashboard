import pandas as pd
import numpy as np

# Read the full shots data
df = pd.read_csv('data/interim/lineups/shots_with_lineups_full.csv')

# Group by the 3 zone columns
zone_stats = df.groupby(['SHOT_ZONE_BASIC', 'SHOT_ZONE_AREA', 'SHOT_ZONE_RANGE']).agg({
    'LOC_X': ['min', 'max', 'mean', 'count'],
    'LOC_Y': ['min', 'max', 'mean', 'count'],
    'SHOT_MADE_FLAG': 'mean'
}).round(1)

# Flatten column names
zone_stats.columns = ['_'.join(col).strip() for col in zone_stats.columns.values]
zone_stats = zone_stats.sort_values('LOC_X_count', ascending=False)

print('ZONE STATISTICS (sorted by shot count):')
print('=' * 150)
print(zone_stats.to_string())
print('\n\n')

# Print in a more readable format
print('DETAILED ZONE BREAKDOWN:')
print('=' * 150)
for idx, row in zone_stats.iterrows():
    basic, area, rng = idx
    x_count = int(row['LOC_X_count'])
    x_min = row['LOC_X_min']
    x_max = row['LOC_X_max']
    x_mean = row['LOC_X_mean']
    y_min = row['LOC_Y_min']
    y_max = row['LOC_Y_max']
    y_mean = row['LOC_Y_mean']
    fg_pct = row['SHOT_MADE_FLAG_mean']
    
    print(f'\n{basic} | {area} | {rng}')
    print(f'  Shots: {x_count} | FG%: {fg_pct:.1%}')
    print(f'  LOC_X: [{x_min:.0f}, {x_max:.0f}] (mean: {x_mean:.0f})')
    print(f'  LOC_Y: [{y_min:.0f}, {y_max:.0f}] (mean: {y_mean:.0f})')
