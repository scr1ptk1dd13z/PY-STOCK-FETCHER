import pandas as pd
import yfinance as yf
import time
from datetime import datetime
from google.colab import files
from concurrent.futures import ThreadPoolExecutor, as_completed

# Function to fetch data for each batch of tickers
def fetch_batch_data(tickers):
    try:
        print(f"Fetching data for {len(tickers)} tickers: {tickers[:5]}...")  # Display first 5 tickers in the batch
        # Fetch the data for multiple tickers in one request
        data = yf.download(tickers, group_by='ticker', period="1d", interval="1d")
        
        # Process the data to extract relevant information
        stock_data = []
        for ticker in tickers:
            stock_info = data[ticker].iloc[-1]  # Get the latest data for the ticker
            stock_data.append({
                "Symbol": ticker,
                "Current Price": stock_info['Close'] if 'Close' in stock_info else "N/A",
                "Open": stock_info['Open'] if 'Open' in stock_info else "N/A",
                "High": stock_info['High'] if 'High' in stock_info else "N/A",
                "Low": stock_info['Low'] if 'Low' in stock_info else "N/A",
                "Volume": stock_info['Volume'] if 'Volume' in stock_info else "N/A",
                "Adj Close": stock_info['Adj Close'] if 'Adj Close' in stock_info else "N/A"
            })
        return stock_data
    except Exception as e:
        print(f"Error fetching batch data for {tickers}: {e}")
        return []

# Function to get tickers array from file
def get_tickers(exchange_name):
    with open(f"{exchange_name}_SYMBOLS.txt", "r") as file:
        return file.read().splitlines()

# Function to fetch stock data in batches
def fetch_stock_data_in_batches(tickers, batch_size=500, wait_time=30):
    stock_data = []
    total_tickers = len(tickers)
    
    # Process in batches
    for i in range(0, total_tickers, batch_size):
        batch_tickers = tickers[i:i + batch_size]
        print(f"Processing batch {i//batch_size + 1} of {len(tickers)//batch_size + 1}")
        
        # Fetch stock data for this batch
        batch_data = fetch_batch_data(batch_tickers)
        stock_data.extend(batch_data)
        
        # Wait between batches to avoid rate limiting
        if i + batch_size < total_tickers:
            print(f"Waiting for {wait_time} seconds before next batch...")
            time.sleep(wait_time)
    
    return pd.DataFrame(stock_data)

if __name__ == "__main__":
    # Fetch tickers from the custom list and TSX Composite
    custom_tickers = get_tickers("NYSE")
    canadian_tickers = get_tickers("TSX")

    # Combine both lists without limiting the number of stocks
    top_tickers = custom_tickers + canadian_tickers

    # Fetch stock data in batches
    stock_df = fetch_stock_data_in_batches(top_tickers)

    # Get the current date
    current_date = datetime.now().strftime("%Y-%m-%d")

    # Define file names with the current date
    csv_file_name = f"custom_us_canadian_stocks_{current_date}.csv"
    excel_file_name = f"custom_us_canadian_stocks_{current_date}.xlsx"

    # Save to CSV and Excel
    stock_df.to_csv(csv_file_name, index=False)
    stock_df.to_excel(excel_file_name, index=False)

    print(
        f"Data for custom US and Canadian stocks has been saved to {csv_file_name} and {excel_file_name}"
    )

    # Automatically download the CSV file
    files.download(csv_file_name)
