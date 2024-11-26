import os
import sys
import pandas as pd
import yfinance as yf
import time
import yaml
import logging
from typing import List, Dict, Optional

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
        with open(config_path, "r") as file:
            self.config = yaml.safe_load(file)
        
        # Configure logging
        self._setup_logging()

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
                "Current Price": info.get("currentPrice", "N/A"),
                "Market Cap": info.get("marketCap", "N/A"),
                "PE Ratio": info.get("trailingPE", "N/A"),
                "Dividend Yield": info.get("dividendYield", "N/A"),
            }
        except Exception as e:
            self.logger.error(f"Error fetching data for {ticker}: {e}")
            return {"Symbol": ticker, "Error": str(e)}

    def fetch_stock_data(self, tickers: List[str]) -> pd.DataFrame:
        """
        Fetch stock data for multiple tickers with batching
        """
        if not tickers:
            print("No tickers provided. Exiting.")
            return pd.DataFrame()

        self.logger.info(f"Starting stock data fetch for {len(tickers)} tickers")
        
        results = []
        for i, ticker in enumerate(tickers, 1):
            result = self.fetch_single_ticker(ticker)
            results.append(result)
            
            # Rate limiting
            time.sleep(self.config['fetching']['api_rate_limit_ms'] / 1000)
            
            # Optional batching
            if i % self.config['fetching'].get('batch_size', 100) == 0:
                self.logger.info(f"Processed {i} tickers")
        
        df = pd.DataFrame(results)
        
        # Log stats
        successful_tickers = df[df.get('Error', pd.Series()).isna()].shape[0]
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
