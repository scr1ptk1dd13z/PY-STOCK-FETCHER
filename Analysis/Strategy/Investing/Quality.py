import pandas as pd
from google.colab import files

# Step 1: Prompt user to upload the CSV file
uploaded = files.upload()

# Load the uploaded CSV file into a DataFrame
for filename in uploaded.keys():
    df = pd.read_csv(filename)

# Define the quality investing filter function
def filter_stocks_quality(df):
    # Drop rows with missing values in the selected quality investing columns
    df = df.dropna(subset=['PE Ratio', 'Price to Book', 'Return on Assets', 'Return on Equity', 'Current Price'])

    # Filter stocks based on quality investing criteria
    filtered_df = df[
        (df['PE Ratio'] > 0) &                  # Positive PE ratio
        (df['Price to Book'] < 3.0) &           # P/B ratio within a reasonable range
        (df['Return on Assets'] > 0.1) &        # Strong ROA
        (df['Return on Equity'] > 0.15)         # Strong ROE
    ].copy()

    # Calculate Quality Score based on weighted metrics
    filtered_df['Quality Score'] = (
        (1 / filtered_df['PE Ratio'] * 0.3) +        # Weight lower PE ratio
        (1 / filtered_df['Price to Book'] * 0.3) +   # Weight lower P/B ratio
        (filtered_df['Return on Assets'] * 0.2) +    # Higher ROA
        (filtered_df['Return on Equity'] * 0.2)      # Higher ROE
    )

    # Select the top 10 stocks based on the Quality Score
    top_10_stocks = filtered_df.nlargest(10, 'Quality Score')

    # Add clickable Yahoo Finance link to the ticker symbol
    top_10_stocks['Symbol'] = top_10_stocks['Symbol'].apply(
        lambda x: f'<a href="https://finance.yahoo.com/quote/{x}" target="_blank">{x}</a>'
    )

    return top_10_stocks

# Step 2: Apply the quality filter function
top_10_stocks_quality = filter_stocks_quality(df)

# Step 3: Save the symbols to a text file, one symbol per line
output_file = 'top_10_stocks_quality.txt'
with open(output_file, 'w') as f:
    for symbol in top_10_stocks_quality['Symbol']:
        f.write(f"{symbol}\n")

files.download(output_file)

# Display the selected stocks with detailed info and clickable Yahoo Finance links in Colab
top_10_stocks_quality_display = top_10_stocks_quality[['Symbol', 'Name', 'Sector', 'Industry', 'Country', 'Current Price', 'Market Cap', 'PE Ratio', 'Price to Book', 'Return on Assets', 'Return on Equity', 'Quality Score']]

# Make the ticker symbols clickable
top_10_stocks_quality_display = top_10_stocks_quality_display.style.format({'Symbol': lambda x: x})
top_10_stocks_quality_display
