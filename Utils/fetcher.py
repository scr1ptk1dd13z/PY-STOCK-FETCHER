import os
import sys
import time
import random
import yaml
import logging
from typing import List, Dict, Optional

import pandas as pd
import yfinance as yf

class StockDataFetcher:
    def __init__(self, config_path=None):
        # Potential root directories to search
        self.potential_roots = [
            os.getcwd(),  # Current working directory
            os.path.dirname(os.path.abspath(__file__)),  # Directory of the script
            os.path.abspath(os.path.join(os.path.dirname(__file__), '..')),  # Parent directory
            os.path.expanduser('~'),  # User home directory
            '/'  # Root directory (last resort)
        ]
        
        # If no config path provided, look in potential locations
        if config_path is None:
            config_path = self.find_file('config.yaml')
        
        # Load configuration
        self._load_config(config_path)
        
        # Configure logging
        self._setup_logging()

    def _load_config(self, config_path: str):
        """
        Load and validate configuration
        """
        try:
            with open(config_path, "r") as file:
                self.config = yaml.safe_load(file)
            
            # Validate critical configuration sections
            required_keys = {
                'logging': ['log_file', 'level'],
                'fetching': ['api_rate_limit_ms', 'batch_size', 'batch_pause_duration', 'output_folder', 'output_filename_format']
            }
            
            for section, keys in required_keys.items():
                if section not in self.config:
                    raise KeyError(f"Missing {section} section in config")
                for key in keys:
                    if key not in self.config[section]:
                        raise KeyError(f"Missing {key} in {section} configuration")
        
        except (IOError, yaml.YAMLError) as e:
            print(f"Error loading configuration: {e}")
            raise

    def _setup_logging(self):
        """Set up logging with robust directory creation"""
        # Ensure log directory exists
        log_dir = os.path.dirname(self.config['logging']['log_file'])
        os.makedirs(log_dir, exist_ok=True)
        
        logging.basicConfig(
            filename=self.config['logging']['log_file'],
            level=getattr(logging, self.config['logging']['level']),
            format="%(asctime)s - %(levelname)s - %(message)s"
        )
        
        # Initialize logger
        self.logger = logging.getLogger(__name__)

    def find_file(self, filename: str) -> Optional[str]:
        """
        Search for a file in potential root directories
        """
        for root in self.potential_roots:
            for dirpath, _, filenames in os.walk(root):
                if filename in filenames:
                    return os.path.join(dirpath, filename)
        
        # If file not found
        print(f"Could not find {filename} in any of the search paths")
        return None

    def load_tickers(self) -> List[str]:
        """
        Attempt to find and load tickers from multiple possible locations
        """
        ticker_filenames = ['tickers.txt', 'ticker.txt', 'stocks.txt']
        
        for filename in ticker_filenames:
            ticker_path = self.find_file(filename)
            if ticker_path:
                try:
                    with open(ticker_path, "r") as f:
                        tickers = [line.strip() for line in f if line.strip()]
                    
                    print(f"Loaded {len(tickers)} tickers from {ticker_path}")
                    self.logger.info(f"Loaded {len(tickers)} tickers from {ticker_path}")
                    return tickers
                except Exception as e:
                    print(f"Error reading {ticker_path}: {e}")
                    self.logger.error(f"Error reading {ticker_path}: {e}")
        
        # If no tickers file found
        print("No tickers file found. Please create a tickers.txt file.")
        self.logger.error("No tickers file found")
        return []

    def fetch_single_ticker(self, ticker: str) -> Dict:
        """
        Fetch stock data for a single ticker with robust error handling
        """
        try:
            stock = yf.Ticker(ticker)
            info = stock.info

            # Use get() method with fallback values to prevent KeyError
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
            self.logger.error(f"Error fetching data for {ticker}: {e}")
            return {"Symbol": ticker, "Error": str(e)}

    def fetch_stock_data(self, tickers: List[str]) -> pd.DataFrame:
        """
        Fetch stock data for multiple tickers with advanced rate limiting and error handling
        """
        if not tickers:
            print("No tickers provided. Exiting.")
            return pd.DataFrame()

        self.logger.info(f"Starting stock data fetch for {len(tickers)} tickers")
        
        results = []
        consecutive_calls = 0
        retry_delay = 1  # Initial retry delay
        max_retry_delay = 60  # Maximum delay between retries
        
        for i, ticker in enumerate(tickers, 1):
            try:
                # Check if we need a longer pause
                if consecutive_calls >= self.config['fetching']['batch_size']:
                    pause_duration = self.config['fetching']['batch_pause_duration']
                    self.logger.info(f"Reached batch limit. Pausing for {pause_duration} seconds")
                    time.sleep(pause_duration)
                    consecutive_calls = 0
                    retry_delay = 1  # Reset retry delay
                
                # Fetch ticker data
                result = self.fetch_single_ticker(ticker)
                results.append(result)
                
                # Basic rate limiting
                time.sleep(self.config['fetching']['api_rate_limit_ms'] / 1000)
                
                consecutive_calls += 1
                
                # Optional progress logging
                if i % 50 == 0:
                    self.logger.info(f"Processed {i} tickers")
            
            except Exception as e:
                # Log and handle any unexpected errors
                self.logger.error(f"Unexpected error processing {ticker}: {e}")
                
                # Exponential backoff with jitter for rate limit errors
                if "429" in str(e):
                    self.logger.warning(f"Rate limit hit for {ticker}. Backing off.")
                    time.sleep(retry_delay + random.uniform(0, 1))
                    retry_delay = min(retry_delay * 2, max_retry_delay)
                
                results.append({"Symbol": ticker, "Error": str(e)})
        
        # Convert results to DataFrame
        df = pd.DataFrame(results)
        
        # Log stats
        successful_tickers = df[~df.get('Error', pd.Series()).notna()].shape[0]
        failed_tickers = df[df.get('Error', pd.Series()).notna()].shape[0]
        self.logger.info(f"Fetch complete. Successful: {successful_tickers}, Failed: {failed_tickers}")
        
        return df

    def save_data(self, df: pd.DataFrame, filename: str = None):
        """
        Save stock data to CSV with flexible naming
        """
        if df.empty:
            print("No data to save.")
            return

        if filename is None:
            filename = self.config['fetching']['output_filename_format'].format(
                date=time.strftime("%Y-%m-%d")
            )
        
        # Ensure output directory exists
        output_dir = self.config['fetching']['output_folder']
        os.makedirs(output_dir, exist_ok=True)
        
        full_path = os.path.join(output_dir, filename)
        
        try:
            df.to_csv(full_path, index=False)
            print(f"Data saved to {full_path}")
            self.logger.info(f"Data saved to {full_path}")
        except Exception as e:
            print(f"Failed to save data: {e}")
            self.logger.error(f"Failed to save data: {e}")

def main():
    try:
        # Create fetcher instance
        fetcher = StockDataFetcher()
        
        # Load tickers
        tickers = fetcher.load_tickers()
        
        if not tickers:
            print("No tickers found. Exiting.")
            sys.exit(1)
        
        # Fetch stock data
        stock_data = fetcher.fetch_stock_data(tickers)
        
        # Save data
        fetcher.save_data(stock_data)
    
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
