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

            return {
                "Symbol": ticker,
                "Name": info.get("longName", "N/A"),
                "Sector": info.get("sector", "N/A"),
                "Industry": info.get("industry", "N/A"),
                "Country": info.get("country", "N/A"),
                "Currency": info.get("currency", "N/A"),
                "Exchange": info.get("exchange", "N/A"),
                "Current Price": info.get("currentPrice", "N/A"),
                "Market Cap": info.get("marketCap", "N/A"),
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
        
        for i, ticker in enumerate(tickers, 1):
            try:
                # Check if we need a longer pause
                if consecutive_calls >= self.config['fetching']['batch_size']:
                    pause_duration = self.config['fetching']['batch_pause_duration']
                    self.logger.info(f"Reached batch limit. Pausing for {pause_duration} seconds")
                    time.sleep(pause_duration)
                    consecutive_calls = 0
                
                # Fetch ticker data
                result = self.fetch_single_ticker(ticker)
                results.append(result)
                
                # Basic rate limiting
                time.sleep(self.config['fetching']['api_rate_limit_ms'] / 1000)
                consecutive_calls += 1
                
                if i % 50 == 0:
                    self.logger.info(f"Processed {i} tickers")
            except Exception as e:
                self.logger.error(f"Unexpected error processing {ticker}: {e}")
                results.append({"Symbol": ticker, "Error": str(e)})
        
        df = pd.DataFrame(results)
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
        
        output_dir = self.config['fetching']['output_folder']
        os.makedirs(output_dir, exist_ok=True)
        
        full_path = os.path.join(output_dir, filename)
        
        try:
            df.to_csv(full_path, index=False)
            print(f"Data saved to {full_path}")
            self.logger.info(f"Data saved to {full_path}")
        except Exception as e:
            self.logger.error(f"Failed to save data: {e}")


def main():
    try:
        fetcher = StockDataFetcher()
        tickers = fetcher.load_tickers()
        
        if not tickers:
            print("No tickers found. Exiting.")
            sys.exit(1)
        
        stock_data = fetcher.fetch_stock_data(tickers)
        fetcher.save_data(stock_data)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
