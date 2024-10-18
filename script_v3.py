# Update the fetch_stock_data function to use the new order
def fetch_stock_data(tickers):
    stock_data = []
    total_tickers = len(tickers)
    for index, ticker in enumerate(tickers, start=1):
        print(f"Fetching data for {ticker} ({index}/{total_tickers})")
        stock = yf.Ticker(ticker)
        retries = 3
        while retries > 0:
            try:
                # Fetch the stock's detailed info
                info = stock.info

                # Append data to list
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
                    }
                )
                break  # Exit retry loop if successful
            except Exception as e:
                retries -= 1
                if retries == 0:
                    print(f"Failed to fetch data for {ticker}: {e}")
                else:
                    time.sleep(1)  # Wait a second before retrying

    return pd.DataFrame(stock_data)

    # Function to get tickers from S&P 500


def get_sp500_tickers():
    sp500_url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
    tables = pd.read_html(sp500_url)
    sp500_table = tables[0]
    sp500_table.columns = sp500_table.columns.map(str)
    symbol_column = None
    for col in sp500_table.columns:
        if "Symbol" in col or "Ticker" in col:
            symbol_column = col
            break
    if symbol_column is None:
        raise KeyError("Could not find the Symbol or Ticker column in S&P 500 table.")

    return sp500_table[symbol_column].tolist()


# Static list of top TSX tickers
def get_tsx_tickers():
    tsx_tickers = [
        "RY.TO",
        "TD.TO",
        "BNS.TO",
        "BMO.TO",
        "CM.TO",
        "ENB.TO",
        "SU.TO",
        "TRP.TO",
        "CNR.TO",
        "CNQ.TO",
        "GIL.TO",
        "BCE.TO",
        "FTS.TO",
        "MFC.TO",
        "BAM.A.TO",
    ]
    return tsx_tickers


# Fetch tickers from both S&P 500 and TSX Composite
us_tickers = get_sp500_tickers()
canadian_tickers = get_tsx_tickers()

# Combine both lists and limit to top 1500 stocks
top_tickers = us_tickers + canadian_tickers
top_tickers = top_tickers[:1500]  # Limiting to top 1500 tickers

# Fetch stock data
stock_df = fetch_stock_data(top_tickers)

# Get the current date
current_date = datetime.now().strftime("%Y-%m-%d")

# Define file names with the current date
csv_file_name = f"top_1500_us_canadian_stocks_{current_date}.csv"
excel_file_name = f"top_1500_us_canadian_stocks_{current_date}.xlsx"

# Save to CSV and Excel
stock_df.to_csv(csv_file_name, index=False)
stock_df.to_excel(excel_file_name, index=False)

print(
    f"Data for top US and Canadian stocks has been saved to {csv_file_name} and {excel_file_name}"
)

# Automatically download the CSV file
files.download(csv_file_name)
