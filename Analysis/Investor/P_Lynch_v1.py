import pandas as pd
from google.colab import files

# Step 1: Prompt user to upload the CSV file
uploaded = files.upload()

# Load the uploaded CSV file into a DataFrame
for filename in uploaded.keys():
    df = pd.read_csv(filename)

# Define a GARP-inspired filtering function
def filter_stocks_garp(df):
    # Further relaxed criteria for GARP
    filtered_df = df[
        (df['Earnings Growth (YoY)'] > 0) &   # Allow any positive growth
        (df['PEG Ratio'] < 2.0) &            # Increase PEG ratio limit to 2.0
        (df['PE Ratio'] < 40) &              # Allow higher PE ratio
        (df['Debt to Equity'] < 3)           # Loosen debt-to-equity ratio further
    ].copy()  # Make a copy to avoid SettingWithCopyWarning
    
    # Calculate the score using .loc to avoid warnings
    filtered_df.loc[:, 'Score'] = filtered_df['Earnings Growth (YoY)'] / filtered_df['PEG Ratio']
    
    # Select the top 10 stocks based on the score
    top_10_stocks = filtered_df.nlargest(10, 'Score')
    
    return top_10_stocks

# Step 3: Apply the GARP filtering function
top_10_stocks_garp = filter_stocks_garp(df)

# Step 4: Save the symbols to a text file, one symbol per line
output_file = 'top_10_stocks_garp.txt'
with open(output_file, 'w') as f:
    for symbol in top_10_stocks_garp['Symbol']:
        f.write(f"{symbol}\n")

# Download the output file
files.download(output_file)

print(f'Top 10 stock symbols based on more relaxed GARP criteria saved to {output_file}.')

# Display the selected symbols
print(top_10_stocks_garp[['Symbol', 'Name']])
