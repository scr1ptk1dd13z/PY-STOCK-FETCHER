# Required Imports
import os
import pandas as pd
import yfinance as yf
import time
from datetime import datetime

# Global call counter and start time
call_counter = 0

# Function to fetch data for each ticker
def fetch_ticker_data(ticker):
    global call_counter
    print(f"Fetching data for {ticker}")
    stock = yf.Ticker(ticker)
    call_counter += 1  # Increment call counter

    try:
        info = stock.info
        return stock_data.append(
                    {
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
                )
    except Exception as e:
        print(f"Error fetching data for {ticker}: {e}")
        return None

# Read S&P symbols from file
def load_tickers(file_path):
    with open(file_path, "r") as f:
        return [line.strip() for line in f.readlines()]

# Main script logic
def main():
    # File containing the NYSE tickers
    ticker_file = "NYSE_SYMBOLS.txt"
    tickers = load_tickers(ticker_file)
    total_tickers = len(tickers)

    print(f"Total tickers to process: {total_tickers}")

    all_data = []
    batch_size = 400  # Number of tickers per batch
    wait_time = 4 * 60  # 4 minutes in seconds

    for i in range(0, total_tickers, batch_size):
        batch_tickers = tickers[i : i + batch_size]
        print(f"Processing batch {i // batch_size + 1} with {len(batch_tickers)} tickers...")

        batch_data = [fetch_ticker_data(ticker) for ticker in batch_tickers if ticker]
        all_data.extend([data for data in batch_data if data])  # Exclude None results

        if i + batch_size < total_tickers:  # If more batches are left
            print(f"Batch {i // batch_size + 1} complete. Waiting for 4 minutes...")
            time.sleep(wait_time)

    # Convert to DataFrame and save as CSV
    df = pd.DataFrame(all_data)
    today = datetime.now().strftime("%Y-%m-%d")
    output_file = f"Data/nyse_daily_stock_data_{today}.csv"

    # Ensure output folder exists
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    df.to_csv(output_file, index=False)
    print(f"Data saved to {output_file}")

if __name__ == "__main__":
    main()
