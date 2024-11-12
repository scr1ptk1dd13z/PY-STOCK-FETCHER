import pandas as pd
from google.colab import files

# Step 1: Prompt user to upload the CSV file
uploaded = files.upload()

# Load the uploaded CSV file into a DataFrame
for filename in uploaded.keys():
    df = pd.read_csv(filename)

# Calculate 'FCF Yield' from 'Free Cash Flow' and 'Market Cap'
df['FCF Yield'] = df['Free Cash Flow'] / df['Market Cap']

# Define the deep value investing filter function
def filter_stocks_deep_value(df):
    # Drop rows with missing values in the necessary columns
    df = df.dropna(subset=['Price to Book', 'PE Ratio', 'FCF Yield', 'Debt to Equity'])

    # Filter stocks based on deep value criteria
    filtered_df = df[
        (df['Price to Book'] < 1.0) &                # Low Price-to-Book ratio
        (df['PE Ratio'] < 10) &                      # Low PE Ratio
        (df['FCF Yield'] > 0.05) &                   # High FCF Yield (5%+)
        (df['Debt to Equity'] < 1.0)                 # Low Debt to Equity
    ].copy()

    # Calculate Deep Value Score
    filtered_df['Deep Value Score'] = (
        (1 / filtered_df['Price to Book'] * 0.3) +   # Undervaluation (higher score for lower P/B)
        (1 / filtered_df['PE Ratio'] * 0.3) +        # Earnings value
        (filtered_df['FCF Yield'] * 0.2) +           # Strong cash flow yield
        (1 / (filtered_df['Debt to Equity'] + 1) * 0.2) # Financial health
    )

    # Select the top 10 stocks based on the Deep Value Score
    top_10_stocks = filtered_df.nlargest(10, 'Deep Value Score')

    # Add clickable Yahoo Finance link to the ticker symbol
    top_10_stocks['Symbol'] = top_10_stocks['Symbol'].apply(
        lambda x: f'<a href="https://finance.yahoo.com/quote/{x}" target="_blank">{x}</a>'
    )

    return top_10_stocks

# Step 2: Apply the deep value filter function
top_10_stocks_deep_value = filter_stocks_deep_value(df)

# Step 3: Save the symbols to a text file, one symbol per line
output_file = 'top_10_stocks_deep_value.txt'
with open(output_file, 'w') as f:
    for symbol in top_10_stocks_deep_value['Symbol']:
        f.write(f"{symbol}\n")

files.download(output_file)

# Display the selected stocks with detailed info and clickable Yahoo Finance links in Colab
top_10_stocks_deep_value_display = top_10_stocks_deep_value[['Symbol', 'Name', 'Sector', 'Country', 'Current Price', 'Market Cap', 'Price to Book', 'PE Ratio', 'FCF Yield', 'Debt to Equity', 'Deep Value Score']]
top_10_stocks_deep_value_display = top_10_stocks_deep_value_display.style.format({'Symbol': lambda x: x})
top_10_stocks_deep_value_display
