import pandas as pd
import yfinance as yf
import time
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading
from queue import Queue
import random
import logging
from collections import deque
from datetime import datetime, timedelta

class RateLimiter:
    def __init__(self, calls_per_second=4):
        self.calls_per_second = calls_per_second
        self.interval = 1.0 / calls_per_second
        self.last_call_times = deque(maxlen=calls_per_second)
        self.lock = threading.Lock()
        
    def wait(self):
        with self.lock:
            current_time = time.monotonic()
            
            # Remove old timestamps
            while self.last_call_times and current_time - self.last_call_times[0] > 1.0:
                self.last_call_times.popleft()
            
            # If we haven't hit our rate limit, don't wait
            if len(self.last_call_times) < self.calls_per_second:
                self.last_call_times.append(current_time)
                return
            
            # Calculate wait time based on oldest request
            if self.last_call_times:
                wait_time = 1.0 - (current_time - self.last_call_times[0])
                if wait_time > 0:
                    time.sleep(wait_time)
            
            self.last_call_times.append(current_time)

class RateMonitor:
    def __init__(self, window_seconds=60):
        self.requests = deque()
        self.window_seconds = window_seconds
        self.lock = threading.Lock()
        self.error_count = 0
        
    def add_request(self, success=True):
        now = time.time()
        with self.lock:
            self.requests.append((now, success))
            while self.requests and self.requests[0][0] < now - self.window_seconds:
                self.requests.popleft()
                
    def get_stats(self):
        with self.lock:
            if not self.requests:
                return 0, 100, 0
            
            total = len(self.requests)
            successful = sum(1 for _, success in self.requests if success)
            requests_per_second = total / self.window_seconds
            success_rate = (successful / total * 100) if total > 0 else 100
            
            return requests_per_second, success_rate, total

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create instances
rate_limiter = RateLimiter(calls_per_second=3)
rate_monitor = RateMonitor(window_seconds=60)

def print_stats():
    requests_per_second, success_rate, total = rate_monitor.get_stats()
    logger.info(f"""
    Last 60 seconds stats:
    - Requests per second: {requests_per_second:.1f}
    - Success rate: {success_rate:.1f}%
    - Total requests: {total}
    """)

def fetch_ticker_data(ticker, index, total_tickers):
    rate_limiter.wait()
    logger.info(f"Fetching data for {ticker} ({index}/{total_tickers})")
    
    stock = yf.Ticker(ticker)
    max_retries = 3
    base_delay = 1
    
    for retry in range(max_retries):
        try:
            info = stock.info
            rate_monitor.add_request(success=True)
            
            if retry > 0:
                logger.info(f"Successfully retrieved {ticker} on attempt {retry + 1}")
            
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
            rate_monitor.add_request(success=False)
            if retry < max_retries - 1:
                delay = (base_delay * (2 ** retry)) + random.uniform(0.1, 0.5)
                logger.warning(f"Retry {retry + 1}/{max_retries} for {ticker} after {delay:.2f}s. Error: {str(e)}")
                time.sleep(delay)
            else:
                logger.error(f"Failed to fetch data for {ticker} after {max_retries} attempts: {str(e)}")
                return None

def fetch_stock_data(tickers):
    stock_data = []
    total_tickers = len(tickers)
    start_time = time.monotonic()
    successful = 0
    failed = 0
    stats_interval = 60
    last_stats_time = time.monotonic()

    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = {
            executor.submit(fetch_ticker_data, ticker, index, total_tickers): ticker 
            for index, ticker in enumerate(tickers, start=1)
        }
        
        for future in as_completed(futures):
            ticker = futures[future]
            try:
                result = future.result()
                if result:
                    stock_data.append(result)
                    successful += 1
                else:
                    failed += 1
                
                current_time = time.monotonic()
                if current_time - last_stats_time >= stats_interval:
                    print_stats()
                    last_stats_time = current_time
                    
            except Exception as e:
                logger.error(f"Error processing {ticker}: {str(e)}")
                failed += 1

    elapsed_time = time.monotonic() - start_time
    logger.info(f"""
    Fetching completed in {elapsed_time:.2f} seconds
    Successful: {successful}
    Failed: {failed}
    Success Rate: {(successful/total_tickers)*100:.2f}%
    """)

    return pd.DataFrame(stock_data)

def get_tickers(exchange_name):
    try:
        with open(f"{exchange_name}_SYMBOLS.txt", "r") as file:
            return file.read().splitlines()
    except FileNotFoundError:
        logger.error(f"Symbol file for {exchange_name} not found")
        return []

if __name__ == "__main__":
    try:
        custom_tickers = get_tickers("NYSE")
        canadian_tickers = get_tickers("TSX")
        
        if not custom_tickers and not canadian_tickers:
            raise ValueError("No tickers found in input files")

        top_tickers = custom_tickers + canadian_tickers
        logger.info(f"Starting data collection for {len(top_tickers)} tickers")

        stock_df = fetch_stock_data(top_tickers)

        current_date = datetime.now().strftime("%Y-%m-%d")
        csv_file_name = f"custom_us_canadian_stocks_{current_date}.csv"
        excel_file_name = f"custom_us_canadian_stocks_{current_date}.xlsx"

        stock_df.to_csv(csv_file_name, index=False)
        stock_df.to_excel(excel_file_name, index=False)

        logger.info(f"Data saved to {csv_file_name} and {excel_file_name}")
        files.download(csv_file_name)

    except Exception as e:
        logger.error(f"Program failed: {str(e)}")
