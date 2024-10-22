# Import necessary libraries
import pandas as pd

# Step 1: Prompt user to upload the CSV file
from google.colab import files
uploaded = files.upload()

# Load the uploaded CSV file into a DataFrame
file_name = list(uploaded.keys())[0]
df = pd.read_csv(file_name)

# Step 2: Define a simplified filtering function
def filter_stocks_basic(df):
    # Basic criteria for filtering
    filtered_df = df[
        (df['Earnings Growth (YoY)'] > 0) & 
        (df['Debt to Equity'] < 2) & 
        (df['Price to Book'] < 10) & 
        (df['PE Ratio'] < 50)
    ]
    
    # Simple score calculation: using PE ratio and earnings growth
    filtered_df['Score'] = filtered_df['Earnings Growth (YoY)'] / filtered_df['PE Ratio']
    
    # Select the top 10 stocks
    top_10_stocks = filtered_df.nlargest(10, 'Score')
    
    return top_10_stocks

# Step 3: Apply the filtering function
top_10_stocks = filter_stocks_basic(df)

# Step 4: Output the selected stocks to a text file
top_10_stocks_list = top_10_stocks['Symbol'].tolist()
with open('top_10_basic_stocks.txt', 'w') as f:
    for stock in top_10_stocks_list:
        f.write(f"{stock}\n")

# Step 5: Download the generated text file (if any stocks pass the filters)
if not top_10_stocks.empty:
    files.download('top_10_basic_stocks.txt')

# Display the selected stocks
top_10_stocks
