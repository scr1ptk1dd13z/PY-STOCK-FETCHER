import os
from Utils.fetcher import fetch_stock_data
from Utils.file_ops import save_to_csv, load_from_csv
from combine_strategies import combine_analysis
from datetime import datetime

def main():
    # Fetch stock data
    tickers = load_from_csv("Data/tickers.csv")["Symbol"]
    stock_data = fetch_stock_data(tickers)

    # Save raw data
    today = datetime.now().strftime('%Y-%m-%d')
    raw_data_file = f"Data/raw_stock_data_{today}.csv"
    save_to_csv(stock_data, raw_data_file)
    print(f"Stock data saved to {raw_data_file}.")

    # Run strategies
    combined_results = combine_analysis(stock_data)

    # Save results
    results_file = f"Data/strategy_results_{today}.csv"
    save_to_csv(combined_results, results_file)
    print(f"Strategy results saved to {results_file}.")

if __name__ == "__main__":
    main()
