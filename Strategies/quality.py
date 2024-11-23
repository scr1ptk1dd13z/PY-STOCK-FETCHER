import pandas as pd

def quality_strategy(df):
    # Drop rows with missing values in key quality metrics
    df_clean = df.dropna(subset=[
        'PE Ratio',
        'Price to Book',
        'Return on Assets',
        'Return on Equity',
        'Current Price'
    ])
    
    # Filter stocks based on quality criteria
    filtered_df = df_clean[
        (df_clean['PE Ratio'] > 0) &
        (df_clean['Price to Book'] < 3.0) &
        (df_clean['Return on Assets'] > 0.1) &
        (df_clean['Return on Equity'] > 0.15)
    ].copy()
    
    # Calculate Quality Score
    filtered_df['Quality Score'] = (
        (1 / filtered_df['PE Ratio'] * 0.3) +
        (1 / filtered_df['Price to Book'] * 0.3) +
        (filtered_df['Return on Assets'] * 0.2) +
        (filtered_df['Return on Equity'] * 0.2)
    )
    
    filtered_df['Strategy'] = 'Quality'
    return filtered_df