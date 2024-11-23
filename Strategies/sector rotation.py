import pandas as pd

def sector_rotation_strategy(df):
    # Drop rows with missing values in key sector rotation metrics
    df_clean = df.dropna(subset=[
        'Revenue Growth (YoY)',
        'Profit Margins',
        'Sector',
        'Market Cap',
        'PE Ratio'
    ])
    
    # Identify high-growth sectors
    sector_growth = df_clean.groupby('Sector')['Revenue Growth (YoY)'].mean()
    top_sectors = sector_growth[sector_growth > 0.05].index
    
    # Filter stocks based on sector rotation criteria
    filtered_df = df_clean[
        (df_clean['Sector'].isin(top_sectors)) &
        (df_clean['Revenue Growth (YoY)'].between(0.05, 1.0)) &
        (df_clean['Profit Margins'].between(0.05, 0.5)) &
        (df_clean['PE Ratio'].between(5, 25)) &
        (df_clean['Market Cap'] > 1e9)
    ].copy()
    
    # Calculate Sector Rotation Score
    filtered_df['Sector Rotation Score'] = (
        (filtered_df['Revenue Growth (YoY)'] * 0.4) +
        (filtered_df['Profit Margins'] * 0.3) +
        ((25 - filtered_df['PE Ratio']) * 0.3)
    )
    
    filtered_df['Strategy'] = 'Sector Rotation'
    return filtered_df