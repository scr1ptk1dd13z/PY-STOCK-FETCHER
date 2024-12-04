import pandas as pd

def defensive_strategy(df):
    # Required columns for defensive strategy
    defensive_columns = [
        'Beta', 'PE Ratio', 'Current Ratio', 'Profit Margins',
        'Gross Margins', 'Operating Margins', 'EBITDA Margins',
        'Debt to Equity', 'Quick Ratio'
    ]
    
    # Remove rows with missing values in key metrics
    df_clean = df.dropna(subset=defensive_columns)
    
    # Filter stocks based on defensive criteria
    filtered_df = df_clean[
        (df_clean['Beta'] < 1.0) &
        (df_clean['PE Ratio'] > 0) &
        (df_clean['PE Ratio'] < 25) &
        (df_clean['Current Ratio'] > 1.5) &
        (df_clean['Quick Ratio'] > 1.0) &
        (df_clean['Profit Margins'] > 0.05) &
        (df_clean['Operating Margins'] > 0.10) &
        (df_clean['Debt to Equity'] < 0.5)
    ].copy()
    
    # Calculate component scores
    filtered_df['Beta_Score'] = 1 - (filtered_df['Beta'] / filtered_df['Beta'].max())
    filtered_df['PE_Score'] = 1 - (filtered_df['PE Ratio'] / filtered_df['PE Ratio'].max())
    filtered_df['Liquidity_Score'] = filtered_df['Current Ratio'] / filtered_df['Current Ratio'].max()
    filtered_df['Profit_Score'] = filtered_df['Profit Margins'] / filtered_df['Profit Margins'].max()
    filtered_df['Operating_Score'] = filtered_df['Operating Margins'] / filtered_df['Operating Margins'].max()
    filtered_df['Debt_Score'] = 1 - (filtered_df['Debt to Equity'] / filtered_df['Debt to Equity'].max())
    filtered_df['Quick_Score'] = filtered_df['Quick Ratio'] / filtered_df['Quick Ratio'].max()
    filtered_df['Gross_Score'] = filtered_df['Gross Margins'] / filtered_df['Gross Margins'].max()
    
    # Calculate final defensive score
    filtered_df['Defensive Score'] = (
        filtered_df['Beta_Score'] * 0.20 +
        filtered_df['PE_Score'] * 0.10 +
        filtered_df['Liquidity_Score'] * 0.15 +
        filtered_df['Quick_Score'] * 0.10 +
        filtered_df['Profit_Score'] * 0.15 +
        filtered_df['Operating_Score'] * 0.10 +
        filtered_df['Gross_Score'] * 0.10 +
        filtered_df['Debt_Score'] * 0.10
    )
    
    filtered_df['Strategy'] = 'Defensive'
    return filtered_df