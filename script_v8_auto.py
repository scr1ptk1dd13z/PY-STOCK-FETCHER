# Required Imports
import os
import pandas as pd
import yfinance as yf
import time
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor

# Global call counter and start time
call_counter = 0
start_time = time.time()

# Function to fetch data for each ticker
def fetch_ticker_data(ticker, index, total_tickers):
    global call_counter, start_time
    print(f"Fetching data for {ticker} ({index}/{total_tickers})")
    stock = yf.Ticker(ticker)

    # Enforce a delay of 200ms between API calls
    while (time.time() - start_time) < (call_counter * 0.2):
        time.sleep(0.01)  # Sleep for 10ms intervals to stay responsive

    # Increment the call counter and fetch data
    call_counter += 1
    try:
        info = stock.info
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
            "Enterprise Value": info.get("enterpriseValue", "N/A"),
            "PE Ratio": info.get("trailingPE", "N/A"),
            "Forward PE": info.get("forwardPE", "N/A"),
            "PEG Ratio": info.get("pegRatio", "N/A"),
            "Price to Book": info.get("priceToBook", "N/A"),
            "Price to Sales": info.get("priceToSalesTrailing12Months", "N/A"),
            "Book Value per Share": info.get("bookValue", "N/A"),
            "Revenue per Share": info.get("revenuePerShare", "N/A"),
            "Revenue Growth (YoY)": info.get("revenueGrowth", "N/A"),
            "Earnings Growth (YoY)": info.get("earningsGrowth", "N/A"),
            "EBITDA Margins": info.get("ebitdaMargins", "N/A"),
            "Gross Margins": info.get("grossMargins", "N/A"),
            "Operating Margins": info.get("operatingMargins", "N/A"),
            "Profit Margins": info.get("profitMargins", "N/A"),
            "Dividend Rate": info.get("dividendRate", "N/A"),
        }
    except Exception as e:
        print(f"Error fetching data for {ticker}: {e}")
        return {
            "Symbol": ticker,
            "Name": "Error",
            "Sector": "Error",
            "Industry": "Error",
            "Country": "Error",
        }

# Main function
def main():
    # Load symbols from files
    nyse_symbols = []
    tsx_symbols = []

    # Read symbols from NYSE file
    with open("NYSE_SYMBOLS.txt", "r") as nyse_file:
        nyse_symbols = [line.strip() for line in nyse_file.readlines()]

    # Read symbols from TSX file
    with open("TSX_SYMBOLS.txt", "r") as tsx_file:
        tsx_symbols = [line.strip() for line in tsx_file.readlines()]

    # Combine all symbols
    all_symbols = nyse_symbols + tsx_symbols

    # Create an empty list to store the results
    results = []

    # Fetch data for each ticker using a ThreadPoolExecutor
    total_tickers = len(all_symbols)
    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = [
            executor.submit(fetch_ticker_data, ticker, idx + 1, total_tickers)
            for idx, ticker in enumerate(all_symbols)
        ]
        for future in futures:
            results.append(future.result())

    # Convert results to a DataFrame
    df = pd.DataFrame(results)

    # Save to a CSV file
    date_str = datetime.now().strftime("%Y-%m-%d")
    output_dir = "Data"
    os.makedirs(output_dir, exist_ok=True)
    csv_file = os.path.join(output_dir, f"daily_stock_data_{date_str}.csv")
    df.to_csv(csv_file, index=False)
    print(f"Data has been saved to {csv_file}")

# Run the script
if __name__ == "__main__":
    main()
