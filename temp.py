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
