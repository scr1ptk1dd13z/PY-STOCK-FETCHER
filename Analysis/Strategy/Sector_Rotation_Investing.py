import pandas as pd
from google.colab import files

# Step 1: Prompt user to upload the CSV file
uploaded = files.upload()

# Load the uploaded CSV file into a DataFrame
for filename in uploaded.keys():
    df = pd.read_csv(filename)

# Define the sector rotation investing filter function with refined criteria
def filter_stocks_sector_rotation(df):
    # Drop rows with missing values in relevant columns
    df = df.dropna(subset=['Revenue Growth (YoY)', 'Profit Margins', 'Sector', 'Market Cap', 'PE Ratio'])

    # Identify sectors with strong growth by calculating average revenue growth per sector
    sector_growth = df.groupby('Sector')['Revenue Growth (YoY)'].mean()
    top_sectors = sector_growth[sector_growth > 0.05].index  # Selecting sectors with >5% average growth

    # Filter stocks based on Sector Rotation criteria
    filtered_df = df[
        (df['Sector'].isin(top_sectors)) &                 # Focus on high-growth sectors
        (df['Revenue Growth (YoY)'].between(0.05, 1.0)) &  # Company revenue growth between 5% and 100%
        (df['Profit Margins'].between(0.05, 0.5)) &        # Profit margin between 5% and 50%
        (df['PE Ratio'].between(5, 25)) &                  # P/E ratio between 5 and 25
        (df['Market Cap'] > 1e9)                           # Minimum market cap of $1 billion
    ].copy()

    # Calculate Sector Rotation Score
    filtered_df['Sector Rotation Score'] = (
        (filtered_df['Revenue Growth (YoY)'] * 0.4) +     # Weight higher revenue growth
        (filtered_df['Profit Margins'] * 0.3) +           # Weight profit margins
        ((25 - filtered_df['PE Ratio']) * 0.3)            # Weight low P/E within growth sectors
    )

    # Select the top 10 stocks based on the Sector Rotation Score
    top_10_stocks = filtered_df.nlargest(10, 'Sector Rotation Score')

    # Add clickable Yahoo Finance link to the ticker symbol
    top_10_stocks['Symbol'] = top_10_stocks['Symbol'].apply(
        lambda x: f'<a href="https://finance.yahoo.com/quote/{x}" target="_blank">{x}</a>'
    )

    return top_10_stocks

# Step 2: Apply the sector rotation filter function
top_10_stocks_sector_rotation = filter_stocks_sector_rotation(df)

# Step 3: Save the symbols to a text file, one symbol per line
output_file = 'top_10_stocks_sector_rotation.txt'
with open(output_file, 'w') as f:
    for symbol in top_10_stocks_sector_rotation['Symbol']:
        f.write(f"{symbol}\n")

files.download(output_file)

# Display the selected stocks with detailed info and clickable Yahoo Finance links in Colab
top_10_stocks_sector_rotation_display = top_10_stocks_sector_rotation[['Symbol', 'Name', 'Sector', 'Country', 'Current Price', 'Market Cap', 'Revenue Growth (YoY)', 'Profit Margins', 'PE Ratio', 'Sector Rotation Score']]

# Make the ticker symbols clickable
top_10_stocks_sector_rotation_display = top_10_stocks_sector_rotation_display.style.format({'Symbol': lambda x: x})
top_10_stocks_sector_rotation_display
