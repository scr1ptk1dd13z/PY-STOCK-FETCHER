# Required Imports
import os
import pandas as pd
import yfinance as yf
import time
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed

# Function to fetch data for each ticker
def fetch_ticker_data(ticker, index, total_tickers):
    print(f"Fetching data for {ticker} ({index}/{total_tickers})")
    stock = yf.Ticker(ticker)
    retries = 3
    delay = 1  # Initial delay of 1 second
    while retries > 0:
        try:
            # Fetch the stock's detailed info
            info = stock.info
            
            # Sleep for 1 second before each request to prevent rate limits
            time.sleep(1)

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
            retries -= 1
            if retries == 0:
                print(f"Failed to fetch data for {ticker}: {e}")
            else:
                time.sleep(delay)
                delay *= 2

# Function to get tickers array from file
def get_tickers(exchange_name):
    with open(f"{exchange_name}_SYMBOLS.txt", "r") as file:
        return file.read().splitlines()

# Function to fetch data for all tickers and collect the results
def fetch_stock_data(tickers):
    stock_data = []
    total_tickers = len(tickers)
    start_time = time.monotonic()

    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = [executor.submit(fetch_ticker_data, ticker, index, total_tickers) for index, ticker in enumerate(tickers, start=1)]
        
        for future in as_completed(futures):
            try:
                result = future.result()
                if result:
                    stock_data.append(result)
            except Exception as e:
                print(f"An error occurred: {e}")

    elapsed_time = time.monotonic() - start_time 
    print(f"All info fetched in {elapsed_time:.2f} seconds")

    return pd.DataFrame(stock_data)

if __name__ == "__main__":
    # Fetch tickers from the custom list and TSX Composite
    custom_tickers = get_tickers("NYSE")
    canadian_tickers = get_tickers("TSX")

    # Combine both lists
    top_tickers = custom_tickers + canadian_tickers

    # Fetch stock data
    stock_df = fetch_stock_data(top_tickers)

    # Create "Data" folder if it doesn't exist
    os.makedirs("Data", exist_ok=True)

    # Get the current date
    current_date = datetime.now().strftime("%Y-%m-%d")

    # Define CSV file path in the "Data" folder with the current date
    csv_file_name = f"Data/daily_stock_data{current_date}.csv"

    # Save to CSV
    stock_df.to_csv(csv_file_name, index=False)

    print(f"Data for custom US and Canadian stocks has been saved to {csv_file_name}")
