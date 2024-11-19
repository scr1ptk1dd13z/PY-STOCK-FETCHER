import os
import pandas as pd
import yfinance as yf
import time
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed

# Function to fetch data for each ticker
def fetch_ticker_data(ticker, index, total_tickers, delay_between_requests):
    print(f"Fetching data for {ticker} ({index}/{total_tickers})")
    stock = yf.Ticker(ticker)
    retries = 5  # Max retries for each ticker
    delay = delay_between_requests  # Start with the global delay
    while retries > 0:
        try:
            info = stock.info
            # Return data as a dictionary
            return {
                "Symbol": ticker,
                "Name": info.get("longName", "N/A"),
                "Sector": info.get("sector", "N/A"),
                "Industry": info.get("industry", "N/A"),
                "Country": info.get("country", "N/A"),
                "Currency": info.get("currency", "N/A"),
                "Exchange": info.get("exchange", "N/A"),
                "Website": info.get("website", "N/A"),
                "Current Price": info.get("currentPrice", "N/A"),
                "Market Cap": info.get("marketCap", "N/A"),
                # Add other fields as required
            }
        except Exception as e:
            # Handle rate-limiting and other transient errors
            if "429" in str(e):
                print(f"Rate limit hit for {ticker}. Retrying in {delay} seconds...")
                time.sleep(delay)
                delay *= 2  # Exponential backoff
                retries -= 1
            else:
                print(f"Error fetching data for {ticker}: {e}")
                break
    # Log failure
    return {"Symbol": ticker, "Error": "Failed after retries"}

# Main function to fetch data for all tickers
def fetch_all_data(tickers, delay_between_requests):
    results = []
    total_tickers = len(tickers)
    with ThreadPoolExecutor(max_workers=5) as executor:  # Adjust worker count if necessary
        future_to_ticker = {
            executor.submit(fetch_ticker_data, ticker, index + 1, total_tickers, delay_between_requests): ticker
            for index, ticker in enumerate(tickers)
        }
        for future in as_completed(future_to_ticker):
            results.append(future.result())
    return results

if __name__ == "__main__":
    # Load your list of tickers
    tickers_file = "tickers.txt"  # Replace with your file containing tickers
    if not os.path.exists(tickers_file):
        print(f"Error: {tickers_file} not found.")
        exit(1)

    with open(tickers_file, "r") as f:
        tickers = [line.strip() for line in f.readlines()]

    delay_between_requests = 1.5  # Adjust this based on your tolerance
    output_dir = "Data"
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, f"daily_stock_data_{datetime.now().strftime('%Y-%m-%d')}.csv")

    # Fetch data
    start_time = time.time()
    data = fetch_all_data(tickers, delay_between_requests)
    end_time = time.time()

    # Save results to a CSV file
    df = pd.DataFrame(data)
    df.to_csv(output_file, index=False)

    print(f"Data fetching completed in {end_time - start_time:.2f} seconds.")
    print(f"Results saved to {output_file}")
