import os
import pandas as pd
import yfinance as yf
import time
from datetime import datetime

# Constants
OUTPUT_DIR = "Data"
API_DELAY = 0.2  # Delay between API calls to avoid rate limiting
BATCH_SIZE = 400  # Fetch this many tickers before pausing
PAUSE_DURATION = 240  # Pause for 4 minutes after a batch

# Ensure output directory exists
os.makedirs(OUTPUT_DIR, exist_ok=True)

def fetch_stock_data(tickers):
    """
    Fetch stock information for a list of tickers.
    """
    stock_data = []
    for i, ticker in enumerate(tickers):
        print(f"Fetching data for {ticker} ({i + 1}/{len(tickers)})...")
        try:
            stock = yf.Ticker(ticker)
            info = stock.info
            stock_data.append(
                {
                    "Symbol": ticker,
                    "Name": info.get("longName", "N/A"),
                    "Sector": info.get("sector", "N/A"),
                    "Industry": info.get("industry", "N/A"),
                    "Country": info.get("country", "N/A"),
                    "Currency": info.get("currency", "N/A"),
                    "Exchange": info.get("exchange", "N/A"),
                    "Current Price": info.get("currentPrice", "N/A"),
                    "Market Cap": info.get("marketCap", "N/A"),
                }
            )
        except Exception as e:
            print(f"Error fetching data for {ticker}: {e}")
        time.sleep(API_DELAY)
        if (i + 1) % BATCH_SIZE == 0:
            print(f"Pausing for {PAUSE_DURATION} seconds after {i + 1} tickers...")
            time.sleep(PAUSE_DURATION)
    return pd.DataFrame(stock_data)

def main():
    input_file = "NYSE_SYMBOLS.txt"
    if not os.path.exists(input_file):
        print(f"Input file {input_file} not found.")
        return

    with open(input_file, "r") as file:
        tickers = [line.strip() for line in file.readlines()]

    stock_data = fetch_stock_data(tickers)
    if not stock_data.empty:
        today = datetime.now().strftime("%Y-%m-%d")
        output_file = os.path.join(OUTPUT_DIR, f"stock_data_{today}.csv")
        stock_data.to_csv(output_file, index=False)
        print(f"Stock data saved to {output_file}")
    else:
        print("No stock data fetched.")

if __name__ == "__main__":
    main()
