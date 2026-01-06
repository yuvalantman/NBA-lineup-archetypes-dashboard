"""
NBA Lineup Tendency Data Processing Module.
Handles loading, normalization, and preparation of lineup-specific
performance metrics for radar/spider charts.
"""

import pandas as pd
import numpy as np
from typing import List, Dict
from pathlib import Path

# Mapping of dataset columns to display labels and formatting
METRIC_CONFIG = {
    'pct_pts_3pt':   {'label': '3PT % Pts',    'format': '{:.1%}'},
    'pct_pts_paint': {'label': 'Paint % Pts',  'format': '{:.1%}'},
    'pct_pts_fb':    {'label': 'Fastbreak %',  'format': '{:.1%}'},
    'pct_pts_2pt_mr':{'label': 'Midrange %',   'format': '{:.1%}'},
    'pct_ast_fgm':   {'label': 'Assisted %',   'format': '{:.1%}'},
    'pct_uast_fgm':  {'label': 'Unassisted %', 'format': '{:.1%}'},
    'efg_pct':       {'label': 'eFG%',         'format': '{:.1%}'},
    'ts_pct':        {'label': 'True Shooting%','format': '{:.1%}'}
}

DEFAULT_METRICS = list(METRIC_CONFIG.keys())

def load_tendency_data(csv_path: str = 'data/processed/Ready_tendencies_data.csv') -> pd.DataFrame:
    """Load and validate the processed tendency CSV."""
    project_root = Path(__file__).parent.parent.parent
    full_path = project_root / csv_path
    
    if not full_path.exists():
        raise FileNotFoundError(f"Tendency data not found at: {full_path}")
        
    df = pd.read_csv(full_path)
    return df

def normalize_metrics(df: pd.DataFrame, metrics: List[str] = None) -> pd.DataFrame:
    """
    Perform Min-Max normalization (0 to 1) for selected metrics.
    Ensures smaller percentage values are visible on radar charts.
    """
    if metrics is None:
        metrics = DEFAULT_METRICS
        
    df_norm = df.copy()
    for col in metrics:
        if col in df.columns:
            m_min = df[col].min()
            m_max = df[col].max()
            # Avoid division by zero if all values are identical
            if m_max == m_min:
                df_norm[f'{col}_norm'] = 0.5
            else:
                df_norm[f'{col}_norm'] = (df[col] - m_min) / (m_max - m_min)
    return df_norm

def prepare_radar_data(df: pd.DataFrame, lineup_index: int, metrics: List[str] = None) -> Dict:
    """
    Prepares a single lineup's data for the Plotly Radar Chart.
    Strictly follows 'one lineup at a time' rule.
    """
    if metrics is None:
        metrics = DEFAULT_METRICS
        
    # Ensure data is normalized before plotting
    norm_cols = [f'{m}_norm' for m in metrics]
    if not all(col in df.columns for col in norm_cols):
        df = normalize_metrics(df, metrics)
        
    row = df.iloc[lineup_index]
    
    # Format lineup label from Archetype columns
    label = row['LINEUP_ARCHETYPE'].replace('-', ', ') if 'LINEUP_ARCHETYPE' in row else "Lineup"
    
    return {
        'label': label,
        'metrics': [METRIC_CONFIG[m]['label'] for m in metrics],
        'values': [row[f'{m}_norm'] for m in metrics], # For the chart shape
        'real_values': [row[m] for m in metrics]       # For the hover tooltips
    }