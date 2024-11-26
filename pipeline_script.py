import os
import sys
import logging
from datetime import datetime

# Ensure the project root directory is in the Python path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from fetcher import StockDataFetcher
from Utils.file_ops import load_from_csv, save_to_csv

def setup_logging():
    """Set up logging for the pipeline"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s: %(message)s',
        handlers=[
            logging.FileHandler('logs/pipeline.log'),
            logging.StreamHandler(sys.stdout)
        ]
    )

def main():
    try:
        # Setup logging
        setup_logging()
        logger = logging.getLogger(__name__)

        # Load tickers
        logger.info("Loading ticker list")
        tickers_file = "Input/tickers.txt"  # Standardized ticker file path
        with open(tickers_file, "r") as f:
            tickers = [line.strip() for line in f if line.strip()]
        
        logger.info(f"Loaded {len(tickers)} tickers from {tickers_file}")

        # Initialize fetcher
        fetcher = StockDataFetcher()

        # Fetch stock data
        logger.info("Starting stock data fetch")
        stock_data = fetcher.fetch_stock_data(tickers)

        # Generate filename with current date
        today = datetime.now().strftime('%Y-%m-%d')
        raw_data_file = f"Data/raw_stock_data_{today}.csv"

        # Save raw data
        logger.info(f"Saving raw stock data to {raw_data_file}")
        stock_data.to_csv(raw_data_file, index=False)

        # Optional: Add further processing or strategy analysis here
        # For now, we'll just log some basic stats
        logger.info(f"Processed {len(stock_data)} stocks")
        logger.info(f"Total stocks with successful data: {len(stock_data[stock_data['Error'].isna()])}")

        print("Stock data fetch and save completed successfully.")

    except Exception as e:
        logging.error(f"Pipeline execution failed: {e}", exc_info=True)
        sys.exit(1)

if __name__ == "__main__":
    main()
