import requests
import pandas as pd
from datetime import datetime
from google.colab import files
import time

# Replace 'YOUR_API_KEY' with your actual Alpha Vantage API key
api_key = 'YOUR_API_KEY'  # Make sure to insert your key here

# List of NYSE symbols
nyse_tickers = [
    "AAPL", "ABT", "ADP", "T", "PG",
    "KO", "JNJ", "PEP", "VZ", "PFE",
    "MMM", "MRK", "WMT", "CSCO", "IBM",
    "MCD", "CVX", "XOM", "ABEV", "AMGN",
    "LMT", "QCOM", "INTC", "UNP", "SPG",
    "DOV", "TROW", "DTE", "BAX", "CL",
    "MDT", "TGT", "SYY", "WBA", "DHR",
    "HIG", "TRV", "LNT", "NKE", "CHRW",
    "CAG", "BHP", "APD", "SYK", "NSC",
    "ORCL", "O", "DOV", "WM", "KMB"
]

# Function to fetch stock data for a given ticker
def fetch_stock_data(tickers):
    stock_data = []
    skipped_tickers = []
    total_tickers = len(tickers)

    for index, ticker in enumerate(tickers, start=1):
        print(f"Fetching data for {ticker} ({index}/{total_tickers})")
        retries = 3
        while retries > 0:
            try:
                # Construct the URL for the Alpha Vantage API
                url = f"https://www.alphavantage.co/query?function=OVERVIEW&symbol={ticker}&apikey={api_key}"
                
                # Requesting data
                response = requests.get(url)
                data = response.json()

                if 'Symbol' in data and data['Symbol'] == ticker:
                    stock_data.append({
                        'Symbol': ticker,
                        'Name': data.get('Name', 'N/A'),
                        'Market Cap': data.get('MarketCapitalization', 'N/A'),
                        'Price': data.get('50DayMovingAverage', 'N/A'),  # Using 50-day moving average as a proxy
                        'PE Ratio': data.get('PERatio', 'N/A'),
                        'Forward PE': data.get('ForwardPE', 'N/A'),
                        'Dividend Yield': data.get('DividendYield', 'N/A'),
                        'Payout Ratio': data.get('PayoutRatio', 'N/A'),
                        'Price to Book': data.get('PriceToBookRatio', 'N/A'),
                        'Price to Sales': data.get('PriceToSalesRatioTTM', 'N/A'),
                        'Beta': data.get('Beta', 'N/A'),
                        '52-Week High': data.get('52WeekHigh', 'N/A'),
                        '52-Week Low': data.get('52WeekLow', 'N/A'),
                        'Average Volume': data.get('QuarterlyEarningsGrowthYOY', 'N/A'),  # Proxy for average volume
                        'ROE': data.get('ReturnOnEquityTTM', 'N/A'),
                        'ROA': data.get('ReturnOnAssetsTTM', 'N/A'),
                        'Revenue Growth (YoY)': data.get('QuarterlyRevenueGrowthYOY', 'N/A'),
                        'EPS Growth (YoY)': data.get('QuarterlyEarningsGrowthYOY', 'N/A'),
                        'EBITDA': data.get('EBITDA', 'N/A'),
                        '1-Year Return': data.get('52WeekHighChangePercent', 'N/A'),  # Proxy for 1-year return
                        'Gross Margins': data.get('GrossProfitTTM', 'N/A')
                    })
                    break
                else:
                    raise ValueError("No valid data found for ticker")
            except Exception as e:
                retries -= 1
                if retries == 0:
                    print(f"Failed to fetch data for {ticker}: {e}")
                    skipped_tickers.append(ticker)
                else:
                    print(f"Retrying for {ticker}...")
                    time.sleep(1)  # Wait a second before retrying
        time.sleep(12)  # Adding delay between each ticker to respect rate limits

    return pd.DataFrame(stock_data), skipped_tickers

# Fetch stock data
stock_df, skipped = fetch_stock_data(nyse_tickers)

# Get the current date
current_date = datetime.now().strftime('%Y-%m-%d')

# Define file names with the current date
csv_file_name = f'nyse_stock_data_{current_date}.csv'
excel_file_name = f'nyse_stock_data_{current_date}.xlsx'

# Save to CSV and Excel
stock_df.to_csv(csv_file_name, index=False)
stock_df.to_excel(excel_file_name, index=False)

print(f"Data for NYSE stocks has been saved to {csv_file_name} and {excel_file_name}")

# Log skipped tickers to a text file
if skipped:  # Corrected condition
    skipped_file_name = f'skipped_tickers_{current_date}.txt'
    with open(skipped_file_name, 'w') as f:
        for ticker in skipped:
            f.write(f"{ticker}\n")
    files.download(skipped_file_name)
    print(f"Skipped tickers have been saved to {skipped_file_name}")

# Automatically download the CSV file
files.download(csv_file_name)
