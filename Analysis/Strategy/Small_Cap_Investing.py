import pandas as pd
from google.colab import files

# Step 1: Prompt user to upload the CSV file
uploaded = files.upload()

# Load the uploaded CSV file into a DataFrame
for filename in uploaded.keys():
    df = pd.read_csv(filename)

# Define the small-cap investing filter function
def filter_stocks_small_cap(df):
    # Drop rows with missing values in key small-cap columns
    df = df.dropna(subset=['Market Cap', 'Current Price', 'PE Ratio', 'Revenue Growth (YoY)', 'Return on Assets'])

    # Filter stocks based on small-cap criteria
    filtered_df = df[
        (df['Market Cap'] < 2000000000) &       # Market cap under $2 billion for small-cap
        (df['PE Ratio'] > 0) &                  # Positive PE ratio (financially healthy)
        (df['Revenue Growth (YoY)'] > 0) &      # Positive revenue growth in the last year
        (df['Return on Assets'] > 0.05)         # Minimum return on assets for profitability
    ].copy()

    # Calculate Small-Cap Score to rank stocks by small-cap appeal
    filtered_df['Small-Cap Score'] = (
        (1 / filtered_df['Market Cap'] * 0.4) +        # Weight smaller market cap
        (filtered_df['Revenue Growth (YoY)'] * 0.3) +  # Favor higher revenue growth
        (filtered_df['Return on Assets'] * 0.2) +      # Favor higher ROA
        (1 / filtered_df['PE Ratio'] * 0.1)            # Favor lower PE ratio
    )

    # Select the top 10 stocks based on the Small-Cap Score
    top_10_stocks = filtered_df.nlargest(10, 'Small-Cap Score')

    # Add clickable Yahoo Finance link to the ticker symbol
    top_10_stocks['Symbol'] = top_10_stocks['Symbol'].apply(
        lambda x: f'<a href="https://finance.yahoo.com/quote/{x}" target="_blank">{x}</a>'
    )

    return top_10_stocks

# Step 2: Apply the small-cap filter function
top_10_stocks_small_cap = filter_stocks_small_cap(df)

# Step 3: Save the symbols to a text file, one symbol per line
output_file = 'top_10_stocks_small_cap.txt'
with open(output_file, 'w') as f:
    for symbol in top_10_stocks_small_cap['Symbol']:
        f.write(f"{symbol}\n")

files.download(output_file)

# Display the selected stocks with detailed info and clickable Yahoo Finance links in Colab
top_10_stocks_small_cap_display = top_10_stocks_small_cap[['Symbol', 'Name', 'Sector', 'Industry', 'Country', 'Current Price', 'Market Cap', 'PE Ratio', 'Revenue Growth (YoY)', 'Return on Assets', 'Small-Cap Score']]

# Make the ticker symbols clickable
top_10_stocks_small_cap_display = top_10_stocks_small_cap_display.style.format({'Symbol': lambda x: x})
top_10_stocks_small_cap_display
