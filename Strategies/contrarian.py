import pandas as pd

def contrarian_strategy(df):
    filtered_df = df[
        (df['1-Year Return'] < -0.1) &
        (df['Price to Book'] < 1.0) &
        (df['Trailing EPS'] > 0) &
        (df['Recommendation Mean'] <= 3.0)
    ].copy()
    filtered_df['Strategy'] = 'Contrarian'
    return filtered_df
