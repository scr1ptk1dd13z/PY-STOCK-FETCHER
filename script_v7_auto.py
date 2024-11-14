import pandas as pd
import yfinance as yf
import time
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading
from queue import Queue
import random
import logging

class RateLimiter:
    def __init__(self, calls_per_second=2):
        self.calls_per_second = calls_per_second
        self.interval = 1.0 / calls_per_second
        self.last_call = time.monotonic()
        self.lock = threading.Lock()
        
    def wait(self):
        with self.lock:
            current_time = time.monotonic()
            elapsed = current_time - self.last_call
            if elapsed < self.interval:
                time.sleep(self.interval - elapsed + random.uniform(0.1, 0.3))  # Add jitter
            self.last_call = time.monotonic()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create a rate limiter instance
rate_limiter = RateLimiter(calls_per_second=2)  # Adjust this value as needed

def fetch_ticker_data(ticker, index, total_tickers):
    rate_limiter.wait()  # Wait before making the request
    logger.info(f"Fetching data for {ticker} ({index}/{total_tickers})")
    
    stock = yf.Ticker(ticker)
    max_retries = 3
    base_delay = 2  # Base delay in seconds
    
    for retry in range(max_retries):
        try:
            info = stock.info
            
            return {
                "Symbol": ticker,
                "Name": info.get("longName", "N/A"),
                # ... [rest of your existing fields remain the same]
                "Total Revenue": info.get("totalRevenue", "N/A"),
            }
            
        except Exception as e:
            if retry < max_retries - 1:
                # Exponential backoff with jitter
                delay = (base_delay * (2 ** retry)) + random.uniform(0.1, 1.0)
                logger.warning(f"Retry {retry + 1}/{max_retries} for {ticker} after {delay:.2f}s. Error: {str(e)}")
                time.sleep(delay)
            else:
                logger.error(f"Failed to fetch data for {ticker} after {max_retries} attempts: {str(e)}")
                return None

def get_tickers(exchange_name):
    try:
        with open(f"{exchange_name}_SYMBOLS.txt", "r") as file:
            return file.read().splitlines()
    except FileNotFoundError:
        logger.error(f"Symbol file for {exchange_name} not found")
        return []

def fetch_stock_data(tickers):
    stock_data = []
    total_tickers = len(tickers)
    start_time = time.monotonic()
    successful = 0
    failed = 0

    # Use a smaller thread pool to prevent overwhelming the API
    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = {
            executor.submit(fetch_ticker_data, ticker, index, total_tickers): ticker 
            for index, ticker in enumerate(tickers, start=1)
        }
        
        for future in as_completed(futures):
            ticker = futures[future]
            try:
                result = future.result()
                if result:
                    stock_data.append(result)
                    successful += 1
                else:
                    failed += 1
            except Exception as e:
                logger.error(f"Error processing {ticker}: {str(e)}")
                failed += 1

    elapsed_time = time.monotonic() - start_time
    logger.info(f"""
        Fetching completed in {elapsed_time:.2f} seconds
        Successful: {successful}
        Failed: {failed}
        Success Rate: {(successful/total_tickers)*100:.2f}%
    """)

    return pd.DataFrame(stock_data)

if __name__ == "__main__":
    try:
        # Fetch tickers from both exchanges
        custom_tickers = get_tickers("NYSE")
        canadian_tickers = get_tickers("TSX")
        
        if not custom_tickers and not canadian_tickers:
            raise ValueError("No tickers found in input files")

        top_tickers = custom_tickers + canadian_tickers
        logger.info(f"Starting data collection for {len(top_tickers)} tickers")

        # Fetch stock data
        stock_df = fetch_stock_data(top_tickers)

        # Get the current date
        current_date = datetime.now().strftime("%Y-%m-%d")

        # Define file names
        csv_file_name = f"custom_us_canadian_stocks_{current_date}.csv"
        excel_file_name = f"custom_us_canadian_stocks_{current_date}.xlsx"

        # Save to files
        stock_df.to_csv(csv_file_name, index=False)
        stock_df.to_excel(excel_file_name, index=False)

        logger.info(f"Data saved to {csv_file_name} and {excel_file_name}")
        
        # Download the CSV file
        files.download(csv_file_name)

    except Exception as e:
        logger.error(f"Program failed: {str(e)}")
