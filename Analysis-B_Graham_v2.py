# Import necessary libraries
import pandas as pd

# Step 1: Prompt user to upload the CSV file
from google.colab import files
uploaded = files.upload()

# Load the uploaded CSV file into a DataFrame
file_name = list(uploaded.keys())[0]
df = pd.read_csv(file_name)

# Step 2: Define a Graham-style filtering function
def filter_stocks_graham(df):
    # Graham's conservative criteria for filtering stocks
    filtered_df = df[
        (df['Earnings Growth (YoY)'] > 0) &         # Positive earnings growth
        (df['Debt to Equity'] < 1.0) &              # Low debt-to-equity for financial stability
        (df['Current Ratio'] > 1.5) &               # High current ratio (indicates strong liquidity)
        (df['PE Ratio'] < 15) &                     # Price-to-Earnings below 15
        (df['Price to Book'] < 1.5)                 # Price-to-Book below 1.5 for value focus
    ]
    
    # Score calculation based on Graham's idea of margin of safety: higher earnings yield
    filtered_df['Score'] = filtered_df['Earnings Growth (YoY)'] / filtered_df['PE Ratio']
    
    # Select the top 10 stocks with the best score
    top_10_stocks = filtered_df.nlargest(10, 'Score')
    
    return top_10_stocks

# Step 3: Apply the filtering function
top_10_stocks = filter_stocks_graham(df)

# Step 4: Output the selected stocks to a text file
top_10_stocks_list = top_10_stocks['Symbol'].tolist()
with open('top_10_graham_stocks.txt', 'w') as f:
    for stock in top_10_stocks_list:
        f.write(f"{stock}\n")

# Step 5: Download the generated text file (if any stocks pass the filters)
if not top_10_stocks.empty:
    files.download('top_10_graham_stocks.txt')

# Display the selected stocks
top_10_stocks
