import pandas as pd

def dividend_strategy(df):
    # Filter stocks based on dividend criteria
    filtered_df = df[
        (df['Dividend Yield'] > 0.03) &
        (df['Payout Ratio'] < 0.7) &
        (df['Free Cash Flow'] > 0) &
        (df['Five-Year Avg. Dividend Yield'] > 0.02)
    ].copy()
    
    # Calculate Dividend Score
    filtered_df['Dividend Score'] = filtered_df['Dividend Yield'] / filtered_df['Payout Ratio']
    
    # Add strategy label
    filtered_df['Strategy'] = 'Dividend'
    
    return filtered_df
