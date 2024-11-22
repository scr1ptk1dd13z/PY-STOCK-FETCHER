import time
import pandas as pd
from yfinance import Ticker
from datetime import datetime
import logging
from typing import List, Dict, Any

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def read_tickers(file_path: str) -> List[str]:
    """
    Read stock tickers from a file.
    
    Args:
        file_path (str): Path to file containing tickers
    
    Returns:
        List[str]: List of stock tickers
    """
    with open(file_path, 'r') as f:
        return [line.strip() for line in f if line.strip()]

def fetch_stock_info(ticker: str) -> Dict[str, Any]:
    """
    Fetch detailed stock information for a given ticker.
    
    Args:
        ticker (str): Stock ticker symbol
    
    Returns:
        Dict[str, Any]: Dictionary containing stock information
    """
    try:
        stock = Ticker(ticker)
        # Get historical data first
        data = stock.history(period="1d")
        if data.empty:
            logging.warning(f"No historical data found for {ticker}")
            return None
            
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
        logging.error(f"Error fetching info for {ticker}: {e}")
        return None

def fetch_data(tickers_file: str, output_file: str) -> None:
    """
    Fetch stock data for tickers from file and save it to a CSV file.
    
    Args:
        tickers_file (str): Path to file containing tickers
        output_file (str): Path to save the output CSV
    """
    tickers = read_tickers(tickers_file)
    logging.info(f"Fetching data for {len(tickers)} tickers...")
    
    stock_data = []
    total_tickers = len(tickers)
    
    for idx, ticker in enumerate(tickers, 1):
        try:
            logging.info(f"Processing {ticker} ({idx}/{total_tickers})...")
            stock_info = fetch_stock_info(ticker)
            
            if stock_info:
                stock_data.append(stock_info)
            
            time.sleep(0.2)  # Original rate limit handling
            
        except Exception as e:
            logging.error(f"Failed to fetch data for {ticker}: {e}")
            continue  # Skip to next ticker on error
    
    if stock_data:
        df = pd.DataFrame(stock_data)
        df.to_csv(output_file, index=False)
        logging.info(f"Data saved to {output_file}")
        logging.info(f"Successfully processed {len(stock_data)} out of {total_tickers} tickers")
    else:
        logging.error("No data was collected. Check the errors above.")

if __name__ == "__main__":
    tickers_file = "NYSE_SYMBOLS.txt"
    output_file = f"Data/nyse_stock_data_{datetime.now().strftime('%Y-%m-%d')}.csv"
    
    fetch_data(tickers_file, output_file)
