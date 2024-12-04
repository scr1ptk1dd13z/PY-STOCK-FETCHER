import pandas as pd

def small_cap_strategy(df):
    # Drop rows with missing values in key small-cap metrics
    df_clean = df.dropna(subset=[
        'Market Cap',
        'Current Price',
        'PE Ratio',
        'Revenue Growth (YoY)',
        'Return on Assets'
    ])
    
    # Filter stocks based on small-cap criteria
    filtered_df = df_clean[
        (df_clean['Market Cap'] < 2000000000) &
        (df_clean['PE Ratio'] > 0) &
        (df_clean['Revenue Growth (YoY)'] > 0) &
        (df_clean['Return on Assets'] > 0.05)
    ].copy()
    
    # Calculate Small-Cap Score
    filtered_df['Small-Cap Score'] = (
        (1 / filtered_df['Market Cap'] * 0.4) +
        (filtered_df['Revenue Growth (YoY)'] * 0.3) +
        (filtered_df['Return on Assets'] * 0.2) +
        (1 / filtered_df['PE Ratio'] * 0.1)
    )
    
    filtered_df['Strategy'] = 'Small-Cap'
    return filtered_df