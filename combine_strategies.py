import pandas as pd

def normalize(series, reverse=False):
    """Normalize a pandas series to a 0-1 scale."""
    if reverse:
        return 1 - (series - series.min()) / (series.max() - series.min())
    return (series - series.min()) / (series.max() - series.min())

def calculate_scores_and_rank(df, strategy_name, score_column, top_n=3):
    """Calculate scores for a strategy and return top N ranked stocks."""
    df = df.sort_values(by=score_column, ascending=False).head(top_n)
    return df[['Ticker', 'Price', 'Price Variance 24h', score_column]]

# Define Contrarian Strategy
def filter_stocks_contrarian(df):
    filtered_df = df[
        (df['1-Year Return'] < -0.1) &
        (df['Price to Book'] < 1.0) &
        (df['Trailing EPS'] > 0) &
        (df['Recommendation Mean'] <= 3.0)
    ].copy()
    
    filtered_df['Contrarian Score'] = normalize(1 / filtered_df['Price to Book']) * 0.5 + \
                                      normalize(filtered_df['1-Year Return'], reverse=True) * 0.5
    return calculate_scores_and_rank(filtered_df, 'Contrarian', 'Contrarian Score')

# Define Deep Value Strategy
def filter_stocks_deep_value(df):
    filtered_df = df.dropna(subset=['Price to Book', 'PE Ratio', 'FCF Yield', 'Debt to Equity'])
    filtered_df = filtered_df[
        (df['Price to Book'] < 1.0) &
        (df['PE Ratio'] < 10) &
        (df['FCF Yield'] > 0.05) &
        (df['Debt to Equity'] < 1.0)
    ].copy()

    filtered_df['Deep Value Score'] = normalize(1 / filtered_df['Price to Book']) * 0.3 + \
                                      normalize(1 / filtered_df['PE Ratio']) * 0.3 + \
                                      normalize(filtered_df['FCF Yield']) * 0.2 + \
                                      normalize(1 / (filtered_df['Debt to Equity'] + 1)) * 0.2
    return calculate_scores_and_rank(filtered_df, 'Deep Value', 'Deep Value Score')

# Define Dividend Investing Strategy
def filter_stocks_dividend(df):
    filtered_df = df[
        (df['Dividend Yield'] > 0.03) &
        (df['Payout Ratio'] < 0.7) &
        (df['Free Cash Flow'] > 0) &
        (df['Five-Year Avg. Dividend Yield'] > 0.02)
    ].copy()

    filtered_df['Dividend Score'] = normalize(filtered_df['Dividend Yield']) * 0.4 + \
                                    normalize(1 / filtered_df['Payout Ratio']) * 0.3 + \
                                    normalize(filtered_df['Free Cash Flow']) * 0.3
    return calculate_scores_and_rank(filtered_df, 'Dividend', 'Dividend Score')

# Define Growth Strategy
def filter_stocks_growth(df):
    filtered_df = df[
        (df['Revenue Growth (YoY)'] > 0.15) &
        (df['Earnings Growth (YoY)'] > 0.15) &
        (df['PE Ratio'] > 20) &
        (df['Price to Sales'] > 2)
    ].copy()

    filtered_df['Growth Score'] = normalize(filtered_df['Revenue Growth (YoY)']) * 0.5 + \
                                  normalize(filtered_df['Earnings Growth (YoY)']) * 0.5
    return calculate_scores_and_rank(filtered_df, 'Growth', 'Growth Score')

# Example Main Function to Process Strategies
def process_strategies(df):
    strategies = {
        "Contrarian": filter_stocks_contrarian,
        "Deep Value": filter_stocks_deep_value,
        "Dividend": filter_stocks_dividend,
        "Growth": filter_stocks_growth,
    }

    for strategy_name, strategy_func in strategies.items():
        print(f"\nTop 3 Stocks for {strategy_name} Strategy:")
        try:
            top_stocks = strategy_func(df)
            print(top_stocks)
        except Exception as e:
            print(f"Error processing {strategy_name}: {e}")

if __name__ == "__main__":
    # Load sample data (replace this with actual data)
    df = pd.read_csv('sample_stock_data.csv')  # Ensure your file has necessary columns
    df['Price Variance 24h'] = (df['High'] - df['Low']) / df['Close']  # Example calculation

    process_strategies(df)
