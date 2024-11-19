# Required Imports
import os
import pandas as pd
import yfinance as yf
import time
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor

# Global call counter and timer
call_counter = 0
start_time = time.time()

# Function to fetch data for each ticker
def fetch_ticker_data(ticker, index, total_tickers):
    global call_counter, start_time
    print(f"Fetching data for {ticker} ({index}/{total_tickers})")
    stock = yf.Ticker(ticker)

    # Check and respect API rate limits globally
    elapsed_time = time.time() - start_time
    if call_counter > 0 and elapsed_time < call_counter:
        sleep_time = call_counter - elapsed_time
        print(f"Sleeping for {sleep_time:.2f} seconds to respect API rate limits...")
        time.sleep(sleep_time)

    # Fetch the stock's detailed info
    try:
        call_counter += 1
        info = stock.info
        time.sleep(1)  # Add a slight delay to spread calls evenly

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
            "Dividend Yield": info.get("dividendYield", "N/A"),
            "Payout Ratio": info.get("payoutRatio", "N/A"),
            "Five-Year Avg. Dividend Yield": info.get("fiveYearAvgDividendYield", "N/A"),
        }
    except Exception as e:
        print(f"Error fetching data for {ticker}: {e}")
        return None

# Main Execution
if __name__ == "__main__":
    # Create the Data folder if it doesn't exist
    os.makedirs("Data", exist_ok=True)

    # List of stock tickers (example)
    tickers = ["AAPL", "MSFT", "GOOGL", "TSLA", "AMZN"]
    total_tickers = len(tickers)

    # Fetch data concurrently
    results = []
    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = [
            executor.submit(fetch_ticker_data, ticker, i + 1, total_tickers)
            for i, ticker in enumerate(tickers)
        ]
        for future in futures:
            result = future.result()
            if result:
                results.append(result)

    # Save data to CSV
    data = pd.DataFrame(results)
    output_path = "Data/daily_stock_data_" + datetime.now().strftime("%Y-%m-%d") + ".csv"
    data.to_csv(output_path, index=False)
    print(f"Data for {total_tickers} stocks has been saved to {output_path}")
