import pandas as pd
import yfinance as yf
import time
import yaml
import logging

# Load configuration
with open("config.yaml", "r") as file:
    config = yaml.safe_load(file)

# Config values
ticker_file = config["fetching"]["ticker_file"]
batch_size = config["fetching"]["batch_size"]
api_rate_limit_ms = config["fetching"]["api_rate_limit_ms"]
pause_duration = config["fetching"]["pause_duration"]
output_folder = config["fetching"]["output_folder"]
log_file = config["fetching"]["log_file"]

# Logging configuration
logging.basicConfig(
    filename=log_file,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Function to fetch stock data
def fetch_stock_data(tickers):
    logging.info("Starting stock data fetch process.")
    stock_data = []
    for i, ticker in enumerate(tickers):
        try:
            stock = yf.Ticker(ticker)
            info = stock.info
            stock_data.append({
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
            })
            logging.info(f"Successfully fetched data for ticker: {ticker}")
        except Exception as e:
            logging.error(f"Error fetching data for {ticker}: {e}")
        time.sleep(api_rate_limit_ms / 1000)  # Convert ms to seconds
        if (i + 1) % batch_size == 0:
            logging.info(f"Processed {i + 1} tickers. Pausing for {pause_duration} seconds...")
            time.sleep(pause_duration)
    logging.info("Stock data fetch process completed.")
    return pd.DataFrame(stock_data)

# Main execution
if __name__ == "__main__":
    # Load tickers
    with open(ticker_file, "r") as file:
        tickers = [line.strip() for line in file.readlines()]
    
    logging.info(f"Loaded {len(tickers)} tickers from {ticker_file}.")
    
    # Fetch stock data
    stock_df = fetch_stock_data(tickers)
    
    # Save to CSV
    output_path = f"{output_folder}/stock_data.csv"
    stock_df.to_csv(output_path, index=False)
    logging.info(f"Stock data saved to {output_path}.")
