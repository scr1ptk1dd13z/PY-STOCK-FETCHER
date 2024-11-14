import pandas as pd
import yfinance as yf
import time
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed

# Function to fetch data for each ticker
def fetch_ticker_data(ticker, index, total_tickers):
    print(f"Fetching data for {ticker} ({index}/{total_tickers})")
    stock = yf.Ticker(ticker)
    retries = 5  # Allow for more retries if necessary
    backoff_time = 5  # Initial backoff time (in seconds)
    
    while retries > 0:
        try:
            # Fetch the stock's detailed info
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
                "Dividend Yield": info.get("dividendYield", "N/A"),
                "Payout Ratio": info.get("payoutRatio", "N/A"),
                "Five-Year Avg. Dividend Yield": info.get("fiveYearAvgDividendYield", "N/A"),
                "Ex-Dividend Date": info.get("exDividendDate", "N/A"),
                "Free Cash Flow": info.get("freeCashflow", "N/A"),
                "Operating Cash Flow": info.get("operatingCashflow", "N/A"),
                "Total Cash": info.get("totalCash", "N/A"),
                "Cash per Share": info.get("totalCashPerShare", "N/A"),
                "Total Debt": info.get("totalDebt", "N/A"),
                "Net Debt": info.get("netDebt", "N/A"),
                "Debt to Equity": info.get("debtToEquity", "N/A"),
                "Current Ratio": info.get("currentRatio", "N/A"),
                "Quick Ratio": info.get("quickRatio", "N/A"),
                "Beta": info.get("beta", "N/A"),
                "52-Week High": info.get("fiftyTwoWeekHigh", "N/A"),
                "52-Week Low": info.get("fiftyTwoWeekLow", "N/A"),
                "Average Volume": info.get("averageVolume", "N/A"),
                "Regular Market Volume": info.get("regularMarketVolume", "N/A"),
                "Current Price Change (%)": info.get("regularMarketChangePercent", "N/A"),
                "1-Year Return": info.get("52WeekChange", "N/A"),
                "Insider Ownership": info.get("heldPercentInsiders", "N/A"),
                "Institutional Ownership": info.get("heldPercentInstitutions", "N/A"),
                "Short Ratio": info.get("shortRatio", "N/A"),
                "Target High Price": info.get("targetHighPrice", "N/A"),
                "Target Low Price": info.get("targetLowPrice", "N/A"),
                "Target Mean Price": info.get("targetMeanPrice", "N/A"),
                "Recommendation Mean": info.get("recommendationMean", "N/A"),
                "Number of Analyst Opinions": info.get("numberOfAnalystOpinions", "N/A"),
                "Return on Assets": info.get("returnOnAssets", "N/A"),
                "Return on Equity": info.get("returnOnEquity", "N/A"),
                "Enterprise to EBITDA": info.get("enterpriseToEbitda", "N/A"),
                "Trailing EPS": info.get("trailingEps", "N/A"),
                "Forward EPS": info.get("forwardEps", "N/A"),
                "Total Revenue": info.get("totalRevenue", "N/A"),
            }
        except Exception as e:
            if "Too Many Requests" in str(e):
                print(f"Rate limit exceeded for {ticker}, retrying in {backoff_time} seconds...")
                time.sleep(backoff_time)
                retries -= 1
                backoff_time *= 2  # Exponential backoff
                if retries == 0:
                    print(f"Failed to fetch data for {ticker} after multiple retries: {e}")
            else:
                retries -= 1
                if retries == 0:
                    print(f"Failed to fetch data for {ticker}: {e}")
                else:
                    time.sleep(1)  # Wait a second before retrying

# Function to get tickers array from file
def get_tickers(exchange_name):
    with open(f"{exchange_name}_SYMBOLS.txt", "r") as file:
        return file.read().splitlines()

# Function to fetch data for all tickers in batches
def fetch_stock_data_in_batches(tickers, batch_size=500, wait_time=30):
    stock_data = []
    total_tickers = len(tickers)
    
    # Process in batches
    for i in range(0, total_tickers, batch_size):
        batch_tickers = tickers[i:i + batch_size]
        print(f"Processing batch {i//batch_size + 1} of {len(tickers)//batch_size + 1}")
        
        # Fetch stock data for this batch
        batch_data = fetch_stock_data(batch_tickers)
        stock_data.extend(batch_data)
        
        # Wait between batches
        if i + batch_size < total_tickers:
            print(f"Waiting for {wait_time} seconds before next batch...")
            time.sleep(wait_time)
    
    return pd.DataFrame(stock_data)

# Function to fetch stock data for a list of tickers
def fetch_stock_data(tickers):
    stock_data = []
    total_tickers = len(tickers)
    start_time = time.monotonic()

    # Create a thread pool with a maximum of 10 threads
    with ThreadPoolExecutor(max_workers=10) as executor:
        # Submit multiple tasks to the pool
        futures = [executor.submit(fetch_ticker_data, ticker, index, total_tickers) for index, ticker in enumerate(tickers, start=1)]
        
        # Collect results as each Future completes
        for future in as_completed(futures):
            try:
                result = future.result()  # Retrieve the result from each Future
                if result:  # Only append if the result is not None
                    stock_data.append(result)
            except Exception as e:
                print(f"An error occurred: {e}")

    elapsed_time = time.monotonic() - start_time 
    print(f"All info fetched in {elapsed_time:.2f} seconds")

    return stock_data

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
