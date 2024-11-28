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
    # Ensure logs directory exists
    os.makedirs('logs', exist_ok=True)
    
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

        # Ensure Data directory exists
        os.makedirs('Data', exist_ok=True)

        # Initialize fetcher
        fetcher = StockDataFetcher()

        # Load tickers using fetcher's method
        logger.info("Loading ticker list")
        tickers = fetcher.load_tickers()
        
        if not tickers:
            logger.error("No tickers found. Exiting.")
            sys.exit(1)
        
        logger.info(f"Loaded {len(tickers)} tickers")

        # Fetch stock data
        logger.info("Starting stock data fetch")
        stock_data = fetcher.fetch_stock_data(tickers)

        # Check if stock_data is empty or contains only errors
        if stock_data.empty or stock_data['Error'].notna().all():
            logger.error("No valid stock data retrieved.")
            sys.exit(1)

        # Generate filename with current date
        today = datetime.now().strftime('%Y-%m-%d')
        raw_data_file = f"Data/raw_stock_data_{today}.csv"

        # Save raw data
        logger.info(f"Saving raw stock data to {raw_data_file}")
        stock_data.to_csv(raw_data_file, index=False)

        # Log some basic stats
        logger.info(f"Processed {len(stock_data)} stocks")
        successful_stocks = len(stock_data[stock_data['Error'].isna()])
        logger.info(f"Total stocks with successful data: {successful_stocks}")

        print("Stock data fetch and save completed successfully.")

    except Exception as e:
        logging.error(f"Pipeline execution failed: {e}", exc_info=True)
        sys.exit(1)

if __name__ == "__main__":
    main()
