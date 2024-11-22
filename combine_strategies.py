import pandas as pd

# Generate mock data
def generate_mock_data():
    """Generate mock data for analysis."""
    data = {
        "Ticker": ["AAPL", "MSFT", "GOOGL", "TSLA", "AMZN"],
        "Price": [150, 320, 2800, 720, 3500],
        "1-Year Return": [-0.15, 0.25, -0.05, 0.4, 0.1],
        "Price to Book": [0.8, 2.5, 4, 1.2, 3.5],
        "Trailing EPS": [5.2, 8.1, 10.5, 4.8, 12.0],
        "Recommendation Mean": [2.8, 1.5, 3.0, 2.2, 2.9],
        "PE Ratio": [30, 35, 25, 40, 28],
        "FCF Yield": [0.03, 0.02, 0.05, 0.04, 0.01],
        "Debt to Equity": [0.5, 0.8, 0.4, 0.6, 0.9],
        "Dividend Yield": [0.03, 0.04, 0.02, 0.01, 0.05],
        "Payout Ratio": [0.6, 0.5, 0.7, 0.8, 0.4],
        "Beta": [0.9, 1.2, 1.1, 0.8, 0.95],
        "Current Ratio": [1.8, 1.2, 1.6, 1.9, 1.7],
        "Quick Ratio": [1.2, 1.1, 1.5, 1.3, 1.4],
        "Profit Margins": [0.06, 0.08, 0.12, 0.05, 0.09],
        "Operating Margins": [0.12, 0.18, 0.22, 0.1, 0.15],
        "Revenue Growth (YoY)": [0.2, 0.15, 0.1, 0.25, 0.18],
        "Earnings Growth (YoY)": [0.18, 0.14, 0.2, 0.3, 0.12],
        "Market Cap": [1.5e9, 1.8e12, 2.2e12, 700e9, 1.3e12],
        "Average Volume": [500000, 800000, 300000, 200000, 600000],
    }
    return pd.DataFrame(data)

# Normalize scores
def normalize(series, reverse=False):
    if reverse:
        return 1 - (series - series.min()) / (series.max() - series.min())
    return (series - series.min()) / (series.max() - series.min())

# Strategy Functions
def filter_stocks_contrarian(df):
    filtered_df = df[
        (df['1-Year Return'] < -0.1) &
        (df['Price to Book'] < 1.0) &
        (df['Trailing EPS'] > 0) &
        (df['Recommendation Mean'] <= 3.0)
    ].copy()
    filtered_df['Contrarian Score'] = (
        normalize(1 / filtered_df['Price to Book']) * 0.5 +
        normalize(1 - filtered_df['1-Year Return']) * 0.5
    )
    return filtered_df.sort_values(by="Contrarian Score", ascending=False).head(3)

def filter_stocks_deep_value(df):
    filtered_df = df[
        (df['Price to Book'] < 1.0) &
        (df['PE Ratio'] < 10) &
        (df['FCF Yield'] > 0.05) &
        (df['Debt to Equity'] < 1.0)
    ].copy()
    filtered_df['Deep Value Score'] = (
        normalize(1 / filtered_df['Price to Book']) * 0.3 +
        normalize(1 / filtered_df['PE Ratio']) * 0.3 +
        normalize(filtered_df['FCF Yield']) * 0.2 +
        normalize(1 / (filtered_df['Debt to Equity'] + 1)) * 0.2
    )
    return filtered_df.sort_values(by="Deep Value Score", ascending=False).head(3)

def filter_stocks_defensive(df):
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
    filtered_df['Defensive Score'] = (
        normalize(1 / filtered_df['Beta']) * 0.3 +
        normalize(filtered_df['Profit Margins']) * 0.3 +
        normalize(filtered_df['Operating Margins']) * 0.4
    )
    return filtered_df.sort_values(by="Defensive Score", ascending=False).head(3)

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

def filter_stocks_momentum(df):
    filtered_df = df[
        (df['1-Year Return'] > 0.2) &
        (df['Average Volume'] > 100000) &
        (df['Beta'] >= 1.0)
    ].copy()
    filtered_df['Momentum Score'] = (
        normalize(filtered_df['1-Year Return']) * 0.6 +
        normalize(filtered_df['Average Volume']) * 0.4
    )
    return filtered_df.sort_values(by="Momentum Score", ascending=False).head(3)

def filter_stocks_growth(df):
    filtered_df = df[
        (df['Revenue Growth (YoY)'] > 0.15) &
        (df['Earnings Growth (YoY)'] > 0.15) &
        (df['PE Ratio'] > 20)
    ].copy()
    filtered_df['Growth Score'] = (
        normalize(filtered_df['Revenue Growth (YoY)']) * 0.5 +
        normalize(filtered_df['Earnings Growth (YoY)']) * 0.5
    )
    return filtered_df.sort_values(by="Growth Score", ascending=False).head(3)

def filter_stocks_quality(df):
    filtered_df = df[
        (df['PE Ratio'] > 0) &
        (df['Price to Book'] < 3.0) &
        (df['Profit Margins'] > 0.1) &
        (df['Operating Margins'] > 0.1)
    ].copy()
    filtered_df['Quality Score'] = (
        normalize(filtered_df['Profit Margins']) * 0.5 +
        normalize(filtered_df['Operating Margins']) * 0.5
    )
    return filtered_df.sort_values(by="Quality Score", ascending=False).head(3)

# Main Execution
if __name__ == "__main__":
    df = generate_mock_data()

    strategies = {
        "Contrarian Strategy": filter_stocks_contrarian,
        "Deep Value Strategy": filter_stocks_deep_value,
        "Defensive Strategy": filter_stocks_defensive,
        "Dividend Strategy": filter_stocks_dividend,
        "Momentum Strategy": filter_stocks_momentum,
        "Growth Strategy": filter_stocks_growth,
        "Quality Strategy": filter_stocks_quality,
    }

    for strategy_name, strategy_func in strategies.items():
        print(f"\n--- {strategy_name} ---")
        results = strategy_func(df)
        if results.empty:
            print("No stocks passed the filters.")
        else:
            print(results[['Ticker', 'Price', f"{strategy_name.split()[0]} Score"]])

# Convert to DataFrame and save as CSV
df = pd.DataFrame(all_data)
today = datetime.now().strftime("%Y-%m-%d")
output_file = f"Data/nyse_daily_stock_analysis_{today}.csv"

# Ensure output folder exists
os.makedirs(os.path.dirname(output_file), exist_ok=True)

df.to_csv(output_file, index=False)
print(f"Data saved to {output_file}")
