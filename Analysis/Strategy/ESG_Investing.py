import pandas as pd
from google.colab import files

# Step 1: Prompt user to upload the CSV file
uploaded = files.upload()

# Load the uploaded CSV file into a DataFrame
for filename in uploaded.keys():
    df = pd.read_csv(filename)

# Define the ESG investing filter function
def filter_stocks_esg(df):
    # Drop rows with missing values in key ESG columns
    df = df.dropna(subset=['Revenue Growth (YoY)', 'Profit Margins', 'Current Ratio', 'Debt to Equity'])

    # Filter stocks based on ESG criteria
    filtered_df = df[
        (df['Revenue Growth (YoY)'] > 0.05) &       # Revenue growth of at least 5% in the last year
        (df['Profit Margins'] > 0.1) &              # Profit margin above 10%
        (df['Current Ratio'] >= 1.5) &              # Strong current ratio (for financial stability)
        (df['Debt to Equity'] < 1.0)                # Low debt-to-equity ratio (less leveraged)
    ].copy()

    # Calculate ESG Score based on environmental, social, and governance-friendly financial metrics
    filtered_df['ESG Score'] = (
        (filtered_df['Revenue Growth (YoY)'] * 0.3) +  # Weight revenue growth positively
        (filtered_df['Profit Margins'] * 0.3) +        # Weight higher profit margins
        (filtered_df['Current Ratio'] * 0.2) +         # Weight higher current ratio
        ((1.0 - filtered_df['Debt to Equity']) * 0.2)  # Favor lower debt-to-equity ratios
    )

    # Select the top 10 stocks based on the ESG Score
    top_10_stocks = filtered_df.nlargest(10, 'ESG Score')

    # Add clickable Yahoo Finance link to the ticker symbol
    top_10_stocks['Symbol'] = top_10_stocks['Symbol'].apply(
        lambda x: f'<a href="https://finance.yahoo.com/quote/{x}" target="_blank">{x}</a>'
    )

    return top_10_stocks

# Step 2: Apply the ESG filter function
top_10_stocks_esg = filter_stocks_esg(df)

# Step 3: Save the symbols to a text file, one symbol per line
output_file = 'top_10_stocks_esg.txt'
with open(output_file, 'w') as f:
    for symbol in top_10_stocks_esg['Symbol']:
        f.write(f"{symbol}\n")

files.download(output_file)

# Display the selected stocks with detailed info and clickable Yahoo Finance links in Colab
top_10_stocks_esg_display = top_10_stocks_esg[['Symbol', 'Name', 'Sector', 'Industry', 'Country', 'Current Price', 'Market Cap', 'Revenue Growth (YoY)', 'Profit Margins', 'Current Ratio', 'Debt to Equity', 'ESG Score']]

# Make the ticker symbols clickable
top_10_stocks_esg_display = top_10_stocks_esg_display.style.format({'Symbol': lambda x: x})
top_10_stocks_esg_display
