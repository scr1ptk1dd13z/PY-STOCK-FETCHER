import os
import sys
import pandas as pd
import yfinance as yf
import time
import yaml
import logging
from typing import List, Dict

# Dynamically get the project root directory
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

class StockDataFetcher:
    def __init__(self, config_path=None):
        # If no config path provided, look in the project root
        if config_path is None:
            config_path = os.path.join(PROJECT_ROOT, 'config.yaml')
        
        # Load configuration
        with open(config_path, "r") as file:
            self.config = yaml.safe_load(file)
        
        # Ensure output and log directories exist
        os.makedirs(os.path.join(PROJECT_ROOT, self.config['fetching']['output_folder']), exist_ok=True)
        os.makedirs(os.path.join(PROJECT_ROOT, os.path.dirname(self.config['logging']['log_file'])), exist_ok=True)
        
        # Configure logging
        logging.basicConfig(
            filename=os.path.join(PROJECT_ROOT, self.config['logging']['log_file']),
            level=getattr(logging, self.config['logging']['level']),
            format="%(asctime)s - %(levelname)s - %(message)s"
        )
        
        # Initialize logger
        self.logger = logging.getLogger(__name__)

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
        if filename is None:
            filename = self.config['fetching']['output_filename_format'].format(
                date=time.strftime("%Y-%m-%d")
            )
        
        full_path = os.path.join(PROJECT_ROOT, self.config['fetching']['output_folder'], filename)
        
        try:
            df.to_csv(full_path, index=False)
            self.logger.info(f"Data saved to {full_path}")
        except Exception as e:
            self.logger.error(f"Failed to save data: {e}")

def main():
    # Construct the full path to tickers.txt
    tickers_path = os.path.join(PROJECT_ROOT, 'Input', 'tickers.txt')
    
    # Load tickers from file
    try:
        with open(tickers_path, "r") as f:
            tickers = [line.strip() for line in f if line.strip()]
        
        print(f"Loaded {len(tickers)} tickers from {tickers_path}")
        
        fetcher = StockDataFetcher()
        stock_data = fetcher.fetch_stock_data(tickers)
        fetcher.save_data(stock_data)
    
    except FileNotFoundError:
        print(f"Error: Tickers file not found at {tickers_path}")
        print("Please ensure 'tickers.txt' exists in the Input directory")
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
