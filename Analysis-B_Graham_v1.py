import pandas as pd
from google.colab import files

# Step 1: Prompt user to upload the CSV file
uploaded = files.upload()

# Load the uploaded CSV file into a DataFrame
for filename in uploaded.keys():
    df = pd.read_csv(filename)

# Define a Graham-inspired filtering function with relaxed criteria
def filter_stocks_graham_relaxed(df):
    # Relaxed criteria for filtering
    filtered_df = df[
        (df['Earnings Growth (YoY)'] > -5) &   # Allow slightly negative growth
        (df['Debt to Equity'] < 2) &          # Loosen debt management
        (df['PE Ratio'] < 20) &               # Slightly higher PE ratio allowed
        (df['Price to Book'] < 2)             # Increase Price-to-Book ratio limit
    ].copy()  # Make a copy to avoid SettingWithCopyWarning
    
    # Calculate the score using .loc to avoid warnings
    filtered_df.loc[:, 'Score'] = 1 / (filtered_df['PE Ratio'] * filtered_df['Price to Book'])
    
    # Select the top 10 stocks based on the score
    top_10_stocks = filtered_df.nlargest(10, 'Score')
    
    return top_10_stocks

# Step 3: Apply the relaxed filtering function
top_10_stocks_graham_relaxed = filter_stocks_graham_relaxed(df)

# Step 4: Save the symbols to a text file, one symbol per line
output_file = 'top_10_stocks_bgraham_relaxed.txt'
with open(output_file, 'w') as f:
    for symbol in top_10_stocks_graham_relaxed['Symbol']:
        f.write(f"{symbol}\n")

# Download the output file
files.download(output_file)

print(f'Top 10 stock symbols based on Graham\'s relaxed criteria saved to {output_file}.')

# Display the selected symbols
print(top_10_stocks_graham_relaxed[['Symbol', 'Name']])
