import pandas as pd
from google.colab import files

# Step 1: Prompt user to upload the CSV file
uploaded = files.upload()

# Load the uploaded CSV file into a DataFrame
for filename in uploaded.keys():
    df = pd.read_csv(filename)

# Define the growth investing filter function
def filter_stocks_growth(df):
    # Drop rows with missing values in key growth columns
    df = df.dropna(subset=['Revenue Growth (YoY)', 'Earnings Growth (YoY)', 'PE Ratio', 'Price to Sales'])

    # Filter stocks based on growth criteria
    filtered_df = df[
        (df['Revenue Growth (YoY)'] > 0.15) &    # At least 15% revenue growth year-over-year
        (df['Earnings Growth (YoY)'] > 0.15) &   # At least 15% earnings growth YoY
        (df['PE Ratio'] > 20) &                  # P/E ratio greater than 20
        (df['Price to Sales'] > 2)               # P/S ratio greater than 2
    ].copy()

    # Calculate Growth Score (weighted formula based on growth criteria)
    filtered_df['Growth Score'] = (
        (filtered_df['Revenue Growth (YoY)'] * 0.4) +     # Emphasize revenue growth
        (filtered_df['Earnings Growth (YoY)'] * 0.3) +    # Emphasize earnings growth
        (1 / filtered_df['PE Ratio'] * 0.2) +             # Moderate weighting on high P/E
        (1 / filtered_df['Price to Sales'] * 0.1)         # Slight weight on high P/S
    )

    # Select the top 10 stocks based on the Growth Score
    top_10_stocks = filtered_df.nlargest(10, 'Growth Score')

    # Add clickable Yahoo Finance link to the ticker symbol
    top_10_stocks['Symbol_Link'] = top_10_stocks['Symbol'].apply(
        lambda x: f'<a href="https://finance.yahoo.com/quote/{x}" target="_blank">{x}</a>'
    )

    return top_10_stocks

# Step 2: Apply the growth filter function
top_10_stocks_growth = filter_stocks_growth(df)

# Step 3: Save the symbols to a text file, one symbol per line
output_file = 'top_10_stocks_growth.txt'
with open(output_file, 'w') as f:
    for symbol in top_10_stocks_growth['Symbol']:  # Use original Symbol column
        f.write(f"{symbol}\n")

files.download(output_file)

# Display the selected stocks with detailed info and clickable Yahoo Finance links in Colab
display_columns = [
    'Symbol_Link', 'Name', 'Sector', 'Industry', 'Country', 'Currency', 'Exchange',
    'Current Price', 'Market Cap', 'Revenue Growth (YoY)', 'Earnings Growth (YoY)',
    'PE Ratio', 'Price to Sales', 'Growth Score'
]

# Display with HTML rendering enabled for clickable links
from IPython.display import HTML
display_df = top_10_stocks_growth[display_columns].copy()
display_df = display_df.rename(columns={'Symbol_Link': 'Symbol'})  # Rename back for display
HTML(display_df.to_html(escape=False))
