import pandas as pd

def esg_strategy(df):
    # Drop rows with missing values in key ESG metrics
    df_clean = df.dropna(subset=[
        'Revenue Growth (YoY)',
        'Profit Margins',
        'Current Ratio',
        'Debt to Equity'
    ])
    
    # Filter stocks based on ESG criteria
    filtered_df = df_clean[
        (df_clean['Revenue Growth (YoY)'] > 0.05) &
        (df_clean['Profit Margins'] > 0.1) &
        (df_clean['Current Ratio'] >= 1.5) &
        (df_clean['Debt to Equity'] < 1.0)
    ].copy()
    
    # Calculate ESG Score
    filtered_df['ESG Score'] = (
        (filtered_df['Revenue Growth (YoY)'] * 0.3) +
        (filtered_df['Profit Margins'] * 0.3) +
        (filtered_df['Current Ratio'] * 0.2) +
        ((1.0 - filtered_df['Debt to Equity']) * 0.2)
    )
    
    filtered_df['Strategy'] = 'ESG'
    return filtered_df