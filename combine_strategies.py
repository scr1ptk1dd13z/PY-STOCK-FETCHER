import os
import pandas as pd

# Constants
INPUT_FILE = "Data/stock_data.csv"
OUTPUT_DIR = "Data/Strategy_Outputs"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def contrarian_strategy(df):
    filtered_df = df[
        (df['1-Year Return'] < -0.1) &
        (df['Price to Book'] < 1.0) &
        (df['Trailing EPS'] > 0) &
        (df['Recommendation Mean'] <= 3.0)
    ].copy()
    filtered_df['Strategy'] = 'Contrarian'
    return filtered_df

def deep_value_strategy(df):
    df = df.dropna(subset=['Price to Book', 'PE Ratio', 'Free Cash Flow', 'Debt to Equity'])
    filtered_df = df[
        (df['Price to Book'] < 1.0) &
        (df['PE Ratio'] < 10) &
        (df['Free Cash Flow'] > 0.05) &
        (df['Debt to Equity'] < 1.0)
    ].copy()
    filtered_df['Deep Value Score'] = (
        (1 / filtered_df['Price to Book'] * 0.3) +
        (1 / filtered_df['PE Ratio'] * 0.3) +
        (filtered_df['Free Cash Flow'] * 0.2) +
        (1 / (filtered_df['Debt to Equity'] + 1) * 0.2)
    )
    filtered_df['Strategy'] = 'Deep Value'
    return filtered_df

def defensive_strategy(df):
    filtered_df = df[
        (df['Beta'] < 1.0) &
        (df['PE Ratio'] > 0) &
        (df['PE Ratio'] < 25) &
        (df['Current Ratio'] > 1.5) &
        (df['Quick Ratio'] > 1.0) &
        (df['Profit Margins'] > 0.05) &
        (df['Operating Margins'] > 0.10) &
        (df['Debt to Equity'] < 0.5)
    ].copy()
    filtered_df['Strategy'] = 'Defensive'
    return filtered_df

def dividend_strategy(df):
    filtered_df = df[
        (df['Dividend Yield'] > 0.03) &
        (df['Payout Ratio'] < 0.7) &
        (df['Free Cash Flow'] > 0) &
        (df['Five-Year Avg. Dividend Yield'] > 0.02)
    ].copy()
    filtered_df['Strategy'] = 'Dividend'
    return filtered_df

def esg_strategy(df):
    filtered_df = df[
        (df['Revenue Growth (YoY)'] > 0.05) &
        (df['Profit Margins'] > 0.1) &
        (df['Current Ratio'] >= 1.5) &
        (df['Debt to Equity'] < 1.0)
    ].copy()
    filtered_df['Strategy'] = 'ESG'
    return filtered_df

def growth_strategy(df):
    filtered_df = df[
        (df['Revenue Growth (YoY)'] > 0.15) &
        (df['Earnings Growth (YoY)'] > 0.15) &
        (df['PE Ratio'] > 20) &
        (df['Price to Sales'] > 2)
    ].copy()
    filtered_df['Strategy'] = 'Growth'
    return filtered_df

def momentum_strategy(df):
    filtered_df = df[
        (df['1-Year Return'] > 0.2) &
        (df['Average Volume'] > 100000) &
        (df['Beta'] >= 1.0)
    ].copy()
    filtered_df['Strategy'] = 'Momentum'
    return filtered_df

def quality_strategy(df):
    filtered_df = df[
        (df['PE Ratio'] > 0) &
        (df['Price to Book'] < 3.0) &
        (df['Return on Assets'] > 0.1) &
        (df['Return on Equity'] > 0.15)
    ].copy()
    filtered_df['Strategy'] = 'Quality'
    return filtered_df

def value_strategy(df):
    filtered_df = df[
        (df['PE Ratio'] < 15) &
        (df['Price to Book'] < 3) &
        (df['PEG Ratio'] < 1) &
        (df['Dividend Yield'] > 0.02) &
        (df['Debt to Equity'] < 1) &
        (df['Free Cash Flow'] > 0)
    ].copy()
    # Calculate Value Score
    filtered_df['Value Score'] = (
        (1 - (filtered_df['PE Ratio'] / filtered_df['PE Ratio'].max())) * 0.2 +
        (1 - (filtered_df['Price to Book'] / filtered_df['Price to Book'].max())) * 0.15 +
        (1 - (filtered_df['PEG Ratio'] / filtered_df['PEG Ratio'].max())) * 0.15 +
        (filtered_df['Dividend Yield'] / filtered_df['Dividend Yield'].max()) * 0.2 +
        (1 - (filtered_df['Debt to Equity'] / filtered_df['Debt to Equity'].max())) * 0.15 +
        (filtered_df['Free Cash Flow'] / filtered_df['Free Cash Flow'].max()) * 0.15
    )
    filtered_df['Strategy'] = 'Value'
    return filtered_df

def combine_results(df, strategies):
    all_results = []
    for strategy_name, strategy_func in strategies.items():
        print(f"Running {strategy_name} strategy...")
        result = strategy_func(df)
        if not result.empty:
            result.to_csv(os.path.join(OUTPUT_DIR, f"{strategy_name}_results.csv"), index=False)
            all_results.append(result)
    if all_results:
        combined = pd.concat(all_results, ignore_index=True)
        combined.to_csv(os.path.join(OUTPUT_DIR, "combined_results.csv"), index=False)
        print("All strategy results combined and saved.")
    else:
        print("No stocks passed the strategies.")

def main():
    # Load stock data
    if not os.path.exists(INPUT_FILE):
        print(f"Input file {INPUT_FILE} not found.")
        return
    
    df = pd.read_csv(INPUT_FILE)
    print("Loaded stock data.")

    # Define strategies
    strategies = {
        'Contrarian': contrarian_strategy,
        'Deep Value': deep_value_strategy,
        'Defensive': defensive_strategy,
        'Dividend': dividend_strategy,
        'ESG': esg_strategy,
        'Growth': growth_strategy,
        'Momentum': momentum_strategy,
        'Quality': quality_strategy,
        'Value': value_strategy,
    }

    # Run strategies and combine results
    combine_results(df, strategies)

if __name__ == "__main__":
    main()
