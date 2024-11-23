import pandas as pd

def income_strategy(df):
    # Drop rows with missing values in key dividend metrics
    dividend_columns = [
        'Dividend Rate', 'Dividend Yield', 'Payout Ratio',
        'Five-Year Avg. Dividend Yield', 'Free Cash Flow',
        'Operating Cash Flow', 'Current Price'
    ]
    df_clean = df.dropna(subset=dividend_columns)
    
    # Filter stocks based on income/dividend criteria
    filtered_df = df_clean[
        (df_clean['Dividend Yield'] > 0.03) &
        (df_clean['Payout Ratio'] < 0.75) &
        (df_clean['Free Cash Flow'] > 0) &
        (df_clean['Operating Cash Flow'] > 0) &
        (df_clean['Five-Year Avg. Dividend Yield'] > 0)
    ].copy()
    
    # Calculate dividend coverage ratio
    filtered_df['Dividend Coverage'] = filtered_df.apply(
        lambda row: row['Free Cash Flow'] / (row['Dividend Rate'] * row['Market Cap'] / row['Current Price'])
        if row['Dividend Rate'] > 0 else 0,
        axis=1
    )
    
    # Calculate component scores
    filtered_df['Yield_Score'] = filtered_df['Dividend Yield'] / filtered_df['Dividend Yield'].max()
    filtered_df['Payout_Score'] = 1 - (filtered_df['Payout Ratio'] / filtered_df['Payout Ratio'].max())
    filtered_df['Coverage_Score'] = filtered_df['Dividend Coverage'] / filtered_df['Dividend Coverage'].max()
    filtered_df['Historical_Score'] = filtered_df['Five-Year Avg. Dividend Yield'] / filtered_df['Five-Year Avg. Dividend Yield'].max()
    filtered_df['FCF_Score'] = filtered_df['Free Cash Flow'] / filtered_df['Free Cash Flow'].max()
    
    # Calculate Income Score
    filtered_df['Income Score'] = (
        filtered_df['Yield_Score'] * 0.30 +
        filtered_df['Payout_Score'] * 0.20 +
        filtered_df['Coverage_Score'] * 0.20 +
        filtered_df['Historical_Score'] * 0.15 +
        filtered_df['FCF_Score'] * 0.15
    )
    
    filtered_df['Strategy'] = 'Income'
    return filtered_df