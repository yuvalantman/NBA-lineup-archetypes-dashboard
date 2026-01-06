import plotly.graph_objects as go

def create_tendency_radar(df, selected_lineup_index=None):
    """
    Simplified radar logic to avoid missing data_logic file.
    """
    if df is None or selected_lineup_index is None:
        return go.Figure()

    # Logic to get the row from the dataframe
    try:
        row = df.iloc[selected_lineup_index]
        # Change these to match your actual CSV column names
        metrics = ['transition_pct', 'iso_pct', 'pr_bh_pct', 'post_up_pct', 'spot_up_pct']
        labels = ['Transition', 'Isolation', 'P&R Ball Handler', 'Post Up', 'Spot Up']
        values = [row.get(m, 0) for m in metrics]
        
        fig = go.Figure(data=go.Scatterpolar(
            r=values,
            theta=labels,
            fill='toself',
            line_color='#00BFFF'
        ))
        fig.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)')
        return fig
    except:
        return go.Figure()