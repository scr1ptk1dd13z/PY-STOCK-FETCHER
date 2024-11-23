import pandas as pd

def momentum_strategy(df):
    # Drop rows with missing values in key momentum metrics
    df_clean = df.dropna(subset=[
        '1-Year Return',
        'Average Volume',
        'Beta'
    ])
    
    # Filter stocks based on momentum criteria
    filtered_df = df_clean[
        (df_clean['1-Year Return'] > 0.2) &
        (df_clean['Average Volume'] > 100000) &
        (df_clean['Beta'] >= 1.0)
    ].copy()
    
    # Calculate Momentum Score
    filtered_df['Momentum Score'] = filtered_df['1-Year Return']
    
    filtered_df['Strategy'] = 'Momentum'
    return filtered_df