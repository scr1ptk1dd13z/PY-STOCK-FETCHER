import pandas as pd
from google.colab import files

# Step 1: Prompt user to upload the CSV file
uploaded = files.upload()

# Load the uploaded CSV file into a DataFrame
for filename in uploaded.keys():
    df = pd.read_csv(filename)

# Define the turnaround investing filter function
def filter_stocks_turnaround(df):
    # Drop rows with missing values in key turnaround columns
    df = df.dropna(subset=['Earnings Growth (YoY)', 'Operating Margins', 'Total Debt', 'Current Price'])

    # Filter stocks based on turnaround criteria
    filtered_df = df[
        (df['Earnings Growth (YoY)'] > 0.1) &                # Positive earnings growth YoY (at least 10%)
        (df['Operating Margins'] > 0) &                      # Positive operating margins (company showing profitability)
        (df['Total Debt'] < df['Market Cap'])                # Debt less than the market cap (manageable debt)
    ].copy()

    # Calculate Turnaround Score
    filtered_df['Turnaround Score'] = (
        (filtered_df['Earnings Growth (YoY)'] * 0.5) +      # Weight earnings growth heavily
        (filtered_df['Operating Margins'] * 0.3) -          # Weight profitability positively
        (filtered_df['Total Debt'] / filtered_df['Market Cap'] * 0.2)  # Debt ratio penalty
    )

    # Select the top 10 stocks based on the Turnaround Score
    top_10_stocks = filtered_df.nlargest(10, 'Turnaround Score')

    # Add clickable Yahoo Finance link to the ticker symbol
    top_10_stocks['Symbol'] = top_10_stocks['Symbol'].apply(
        lambda x: f'<a href="https://finance.yahoo.com/quote/{x}" target="_blank">{x}</a>'
    )

    return top_10_stocks

# Step 2: Apply the turnaround filter function
top_10_stocks_turnaround = filter_stocks_turnaround(df)

# Step 3: Save the symbols to a text file, one symbol per line
output_file = 'top_10_stocks_turnaround.txt'
with open(output_file, 'w') as f:
    for symbol in top_10_stocks_turnaround['Symbol']:
        f.write(f"{symbol}\n")

files.download(output_file)

# Display the selected stocks with detailed info and clickable Yahoo Finance links in Colab
top_10_stocks_turnaround_display = top_10_stocks_turnaround[['Symbol', 'Name', 'Sector', 'Country', 'Current Price', 'Market Cap', 'Earnings Growth (YoY)', 'Operating Margins', 'Total Debt', 'Turnaround Score']]

# Make the ticker symbols clickable
top_10_stocks_turnaround_display = top_10_stocks_turnaround_display.style.format({'Symbol': lambda x: x})
top_10_stocks_turnaround_display
