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
        print(f"Failed to fetch data for {ticker}: {e}")
        return None

# Load tickers from S&P file
def load_sp_tickers(file_path):
    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            return [line.strip() for line in file.readlines()]
    else:
        raise FileNotFoundError(f"{file_path} not found.")

# Main function to fetch data
def main():
    sp_tickers_file = "S&P_SYMBOLS.txt"
    sp_tickers = load_sp_tickers(sp_tickers_file)
    total_tickers = len(sp_tickers)

    print(f"Loaded {total_tickers} tickers from {sp_tickers_file}.")

    data = []
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = {
            executor.submit(fetch_ticker_data, ticker, idx + 1, total_tickers): ticker
            for idx, ticker in enumerate(sp_tickers)
        }
        for future in futures:
            result = future.result()
            if result:
                data.append(result)

    # Save the data to a CSV file
    today = datetime.now().strftime("%Y-%m-%d")
    output_folder = "Data"
    os.makedirs(output_folder, exist_ok=True)
    output_file = os.path.join(output_folder, f"daily_stock_data_{today}.csv")
    pd.DataFrame(data).to_csv(output_file, index=False)
    print(f"Data saved to {output_file}")

if __name__ == "__main__":
    main()
