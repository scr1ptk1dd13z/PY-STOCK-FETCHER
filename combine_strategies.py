import pandas as pd

# Create mock in-memory data for testing
def generate_mock_data():
    """Generate mock data for analysis."""
    data = {
        "Ticker": ["AAPL", "MSFT", "GOOGL", "TSLA", "AMZN"],
        "Price": [150, 320, 2800, 720, 3500],
        "High": [152, 325, 2850, 740, 3550],
        "Low": [148, 315, 2750, 700, 3400],
        "Close": [150, 320, 2800, 720, 3500],
        "1-Year Return": [-0.15, 0.25, -0.05, 0.4, 0.1],
        "Price to Book": [10, 15, 4, 12, 20],
        "Trailing EPS": [5.2, 8.1, 10.5, 4.8, 12.0],
        "Recommendation Mean": [2.8, 1.5, 3.0, 2.2, 2.9],
        "PE Ratio": [30, 35, 25, 40, 28],
        "FCF Yield": [0.03, 0.02, 0.05, 0.04, 0.01],
        "Debt to Equity": [0.5, 0.8, 0.4, 0.6, 0.9],
        "Dividend Yield": [0.03, 0.04, 0.02, 0.01, 0.05],
        "Payout Ratio": [0.6, 0.5, 0.7, 0.8, 0.4],
    }
    return pd.DataFrame(data)

# Normalize a series for scoring
def normalize(series, reverse=False):
    if reverse:
        return 1 - (series - series.min()) / (series.max() - series.min())
    return (series - series.min()) / (series.max() - series.min())

# Contrarian Strategy
def filter_stocks_contrarian(df):
    filtered_df = df[
        (df['1-Year Return'] < -0.1) &
        (df['Price to Book'] < 1.0) &
        (df['Trailing EPS'] > 0) &
        (df['Recommendation Mean'] <= 3.0)
    ].copy()

    filtered_df['Contrarian Score'] = (
        (1 / filtered_df['Price to Book']) * 0.5 +
        (1 - filtered_df['1-Year Return']) * 0.5
    )

    return filtered_df.sort_values(by="Contrarian Score", ascending=False).head(3)

# Dividend Strategy
def filter_stocks_dividend(df):
    filtered_df = df[
        (df['Dividend Yield'] > 0.03) &
        (df['Payout Ratio'] < 0.7) &
        (df['FCF Yield'] > 0)
    ].copy()

    filtered_df['Dividend Score'] = (
        normalize(filtered_df['Dividend Yield']) * 0.4 +
        normalize(1 / filtered_df['Payout Ratio']) * 0.3 +
        normalize(filtered_df['FCF Yield']) * 0.3
    )

    return filtered_df.sort_values(by="Dividend Score", ascending=False).head(3)

# Main Execution
if __name__ == "__main__":
    # Generate mock data
    df = generate_mock_data()

    # Strategy functions
    strategies = {
        "Contrarian Strategy": filter_stocks_contrarian,
        "Dividend Strategy": filter_stocks_dividend,
    }

    # Run each strategy and print results
    for strategy_name, strategy_func in strategies.items():
        print(f"\n--- {strategy_name} ---")
        results = strategy_func(df)
        print(results[['Ticker', 'Price', f"{strategy_name.split()[0]} Score"]])
