import os
import sys
import logging
import argparse
from datetime import datetime

# Ensure the project root directory is in the Python path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

# Try to import StockDataFetcher with more robust module finding
try:
    from fetcher import StockDataFetcher
except ImportError:
    # If importing from current directory fails, try alternative import methods
    try:
        import importlib.util
        
        def import_module_from_path(module_name, file_path):
            spec = importlib.util.spec_from_file_location(module_name, file_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            return module
        
        # Try to find fetcher.py in various locations
        possible_paths = [
            os.path.join(os.path.dirname(__file__), 'fetcher.py'),
            os.path.join(os.path.dirname(__file__), '..', 'fetcher.py'),
            'fetcher.py',
            '../fetcher.py'
        ]
        
        for path in possible_paths:
            try:
                if os.path.exists(path):
                    fetcher_module = import_module_from_path('fetcher', path)
                    StockDataFetcher = fetcher_module.StockDataFetcher
                    break
            except Exception:
                continue
        else:
            raise ImportError("Could not find fetcher module")
    
    except ImportError as e:
        print(f"Fatal Error: Could not import StockDataFetcher: {e}")
        sys.exit(1)

def setup_logging(verbose=False):
    """Set up logging for the pipeline"""
    # Ensure logs directory exists
    os.makedirs('logs', exist_ok=True)
    
    # Determine logging level based on verbosity
    log_level = logging.DEBUG if verbose else logging.INFO
    
    logging.basicConfig(
        level=log_level,
        format='%(asctime)s - %(levelname)s: %(message)s',
        handlers=[
            logging.FileHandler('logs/pipeline.log'),
            logging.StreamHandler(sys.stdout)
        ]
    )

def main(verbose=False):
    try:
        # Setup logging
        setup_logging(verbose)
        logger = logging.getLogger(__name__)

        # Ensure Data directory exists
        os.makedirs('Data', exist_ok=True)

        # Initialize fetcher
        logger.info("Initializing StockDataFetcher")
        fetcher = StockDataFetcher()

        # Load tickers using fetcher's method
        logger.info("Loading ticker list")
        
        # Try multiple possible ticker file locations
        ticker_files = [
            'tickers.txt',  # Current directory
            os.path.join(os.path.dirname(__file__), 'tickers.txt'),  # Script directory
            os.path.join(os.path.dirname(__file__), '..', 'tickers.txt')  # Parent directory
        ]
        
        tickers = []
        for ticker_file in ticker_files:
            if os.path.exists(ticker_file):
                logger.info(f"Attempting to load tickers from {ticker_file}")
                with open(ticker_file, 'r') as f:
                    tickers = [line.strip() for line in f if line.strip()]
                    if tickers:
                        break
        
        if not tickers:
            logger.error("No tickers found. Attempting to use fetcher's default method.")
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
    # Add argument parsing for verbosity
    parser = argparse.ArgumentParser(description="Stock Data Pipeline")
    parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose logging")
    args = parser.parse_args()
    
    main(verbose=args.verbose)
