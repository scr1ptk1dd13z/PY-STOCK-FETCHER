import pandas as pd
import yfinance as yf
import time

API_DELAY = 0.2
BATCH_SIZE = 400
PAUSE_DURATION = 240

def fetch_stock_data(tickers):
    """
    Fetch stock information for a list of tickers.
    """
    stock_data = []
    for i, ticker in enumerate(tickers):
        print(f"Fetching data for {ticker} ({i + 1}/{len(tickers)})...")
        try:
            stock = yf.Ticker(ticker)
            info = stock.info
            stock_data.append(
                {
                    "Symbol": ticker,
                    "Name": info.get("longName", "N/A"),
                    "Sector": info.get("sector", "N/A"),
                    "Industry": info.get("industry", "N/A"),
                    "Country": info.get("country", "N/A"),
                    "Currency": info.get("currency", "N/A"),
                    "Current Price": info.get("currentPrice", "N/A"),
                    "Market Cap": info.get("marketCap", "N/A"),
                    "1-Year Return": info.get("52WeekChange", "N/A"),
                    "PE Ratio": info.get("trailingPE", "N/A"),
                    "Price to Book": info.get("priceToBook", "N/A"),
                    "Trailing EPS": info.get("trailingEps", "N/A"),
                    "Recommendation Mean": info.get("recommendationMean", "N/A"),
                }
            )
        except Exception as e:
            print(f"Error fetching data for {ticker}: {e}")
        time.sleep(API_DELAY)
        if (i + 1) % BATCH_SIZE == 0:
            print(f"Pausing for {PAUSE_DURATION} seconds after {i + 1} tickers...")
            time.sleep(PAUSE_DURATION)
    return pd.DataFrame(stock_data)

def get_stock_data():
    """
    Fetch stock data for all tickers in NYSE_SYMBOLS.txt.
    """
    input_file = "NYSE_SYMBOLS.txt"
    with open(input_file, "r") as file:
        tickers = [line.strip() for line in file.readlines()]
    return fetch_stock_data(tickers)
