import pandas as pd

def value_strategy(df):
    filtered_df = df[
        (df['PE Ratio'] < 15) &
        (df['Price to Book'] < 3) &
        (df['PEG Ratio'] < 1) &
        (df['Dividend Yield'] > 0.02) &
        (df['Debt to Equity'] < 1) &
        (df['Free Cash Flow'] > 0)
    ].copy()
    
    filtered_df['PE_Score'] = 1 - (filtered_df['PE Ratio'] / filtered_df['PE Ratio'].max())
    filtered_df['PB_Score'] = 1 - (filtered_df['Price to Book'] / filtered_df['Price to Book'].max())
    filtered_df['PEG_Score'] = 1 - (filtered_df['PEG Ratio'] / filtered_df['PEG Ratio'].max())
    filtered_df['Div_Score'] = filtered_df['Dividend Yield'] / filtered_df['Dividend Yield'].max()
    filtered_df['Debt_Score'] = 1 - (filtered_df['Debt to Equity'] / filtered_df['Debt to Equity'].max())
    filtered_df['FCF_Score'] = filtered_df['Free Cash Flow'] / filtered_df['Free Cash Flow'].max()
    
    filtered_df['Value Score'] = (
        filtered_df['PE_Score'] * 0.2 +
        filtered_df['PB_Score'] * 0.15 +
        filtered_df['PEG_Score'] * 0.15 +
        filtered_df['Div_Score'] * 0.2 +
        filtered_df['Debt_Score'] * 0.15 +
        filtered_df['FCF_Score'] * 0.15
    )
    
    filtered_df['Strategy'] = 'Value'
    return filtered_df