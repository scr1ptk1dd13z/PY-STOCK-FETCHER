import pandas as pd
from google.colab import files
from IPython.display import display

# Step 1: Prompt user to upload the CSV file
uploaded = files.upload()

# Load the uploaded CSV file into a DataFrame
for filename in uploaded.keys():
    df = pd.read_csv(filename)

# Define a Dividend Investing filtering function
def filter_stocks_dividend(df):
    # Dividend investing criteria
    filtered_df = df[
        (df['Dividend Yield'] > 0.03) &                 # Dividend yield > 3%
        (df['Payout Ratio'] < 0.7) &                    # Payout ratio < 70%
        (df['Free Cash Flow'] > 0) &                    # Positive free cash flow
        (df['Five-Year Avg. Dividend Yield'] > 0.02)    # Five-year average dividend yield > 2%
    ].copy()  # Make a copy to avoid SettingWithCopyWarning
    
    # Calculate a dividend score: Dividend Yield / Payout Ratio
    filtered_df.loc[:, 'Dividend Score'] = filtered_df['Dividend Yield'] / filtered_df['Payout Ratio']
    
    # Select the top 10 stocks based on the dividend score
    top_10_dividend_stocks = filtered_df.nlargest(10, 'Dividend Score')
    
    return top_10_dividend_stocks

# Step 3: Apply the Dividend Investing filtering function
top_10_dividend_stocks = filter_stocks_dividend(df)

# Step 4: Save the symbols to a text file, one symbol per line
output_file = 'top_10_stocks_dividend.txt'
with open(output_file, 'w') as f:
    for symbol in top_10_dividend_stocks['Symbol']:
        f.write(f"{symbol}\n")

# Download the output file
files.download(output_file)

print(f'Top 10 stock symbols based on dividend investing criteria saved to {output_file}.')

# Display the full table for the selected top 10 stocks
display(top_10_dividend_stocks)
