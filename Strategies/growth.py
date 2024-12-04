import pandas as pd

def growth_strategy(df):
    # Drop rows with missing values in key growth metrics
    df_clean = df.dropna(subset=[
        'Revenue Growth (YoY)',
        'Earnings Growth (YoY)',
        'PE Ratio',
        'Price to Sales'
    ])
    
    # Filter stocks based on growth criteria
    filtered_df = df_clean[
        (df_clean['Revenue Growth (YoY)'] > 0.15) &
        (df_clean['Earnings Growth (YoY)'] > 0.15) &
        (df_clean['PE Ratio'] > 20) &
        (df_clean['Price to Sales'] > 2)
    ].copy()
    
    # Calculate Growth Score
    filtered_df['Growth Score'] = (
        (filtered_df['Revenue Growth (YoY)'] * 0.4) +
        (filtered_df['Earnings Growth (YoY)'] * 0.3) +
        (1 / filtered_df['PE Ratio'] * 0.2) +
        (1 / filtered_df['Price to Sales'] * 0.1)
    )
    
    filtered_df['Strategy'] = 'Growth'
    return filtered_df