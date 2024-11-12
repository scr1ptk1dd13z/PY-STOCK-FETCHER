import pandas as pd
from google.colab import files

# Step 1: Prompt user to upload the CSV file
uploaded = files.upload()

# Load the uploaded CSV file into a DataFrame
for filename in uploaded.keys():
    df = pd.read_csv(filename)

# Define the momentum investing filter function
def filter_stocks_momentum(df):
    # Drop rows with missing values in key momentum columns
    df = df.dropna(subset=['1-Year Return', 'Average Volume', 'Beta'])

    # Filter stocks based on momentum criteria
    filtered_df = df[
        (df['1-Year Return'] > 0.2) &        # Require at least 20% return over the past year
        (df['Average Volume'] > 100000) &    # Ensure sufficient trading volume
        (df['Beta'] >= 1.0)                  # Target stocks with higher beta (above or equal to 1)
    ].copy()

    # Calculate Momentum Score (using 1-Year Return as the score metric)
    filtered_df['Momentum Score'] = filtered_df['1-Year Return']

    # Select the top 10 stocks based on Momentum Score
    top_10_stocks = filtered_df.nlargest(10, 'Momentum Score')

    return top_10_stocks

# Step 2: Apply the momentum filter function
top_10_stocks_momentum = filter_stocks_momentum(df)

# Step 3: Save the symbols to a text file, one symbol per line
output_file = 'top_10_stocks_momentum.txt'
with open(output_file, 'w') as f:
    for symbol in top_10_stocks_momentum['Symbol']:
        f.write(f"{symbol}\n")

files.download(output_file)

# Display the selected stocks with detailed info
top_10_stocks_momentum_display = top_10_stocks_momentum[['Symbol', 'Name', 'Sector', 'Industry', 'Country', 'Currency', 'Exchange', 'Current Price', 'Market Cap', '1-Year Return', 'Average Volume', 'Beta', 'Momentum Score']]
top_10_stocks_momentum_display
