import pandas as pd

def deep_value_strategy(df):
    filtered_df = df[
        (df['Price to Book'] < 1.0) &
        (df['PE Ratio'] < 10) &
        (df['FCF Yield'] > 0.05) &
        (df['Debt to Equity'] < 1.0)
    ].copy()
    
    filtered_df['Deep Value Score'] = (
        (1 / filtered_df['Price to Book'] * 0.3) +
        (1 / filtered_df['PE Ratio'] * 0.3) +
        (filtered_df['FCF Yield'] * 0.2) +
        (1 / (filtered_df['Debt to Equity'] + 1) * 0.2)
    )
    
    filtered_df['Strategy'] = 'Deep Value'
    return filtered_df