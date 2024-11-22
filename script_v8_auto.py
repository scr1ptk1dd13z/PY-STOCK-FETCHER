import time
import pandas as pd
from yfinance import Ticker
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def fetch_data(tickers: list, output_file: str) -> None:
    """
    Fetch stock data for given tickers and save it to a CSV file.
    
    Args:
        tickers (list): List of stock tickers to fetch data for.
        output_file (str): Path to save the output CSV.
    """
    logging.info(f"Fetching data for {len(tickers)} tickers...")
    all_data = []
    
    for ticker in tickers:
        try:
            stock = Ticker(ticker)
            data = stock.history(period="1d")
            data["Ticker"] = ticker
            all_data.append(data)
            time.sleep(0.2)  # API rate limit handling
        except Exception as e:
            logging.error(f"Failed to fetch data for {ticker}: {e}")

    df = pd.concat(all_data)
    df.to_csv(output_file, index=False)
    logging.info(f"Data saved to {output_file}")

if __name__ == "__main__":
    # Example tickers, replace with file input logic
    tickers = ["AAPL", "GOOGL", "AMZN"]
    output_file = f"Data/nyse_daily_stock_data_{datetime.now().strftime('%Y-%m-%d')}.csv"

    fetch_data(tickers, output_file)
