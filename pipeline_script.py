import os
from script_v8_auto import get_stock_data
from combine_strategies import combine_analysis
from datetime import datetime

# Step 1: Fetch stock data
stock_data = get_stock_data()

# Step 2: Save stock data to CSV
today = datetime.now().strftime('%Y-%m-%d')
stock_data_file = f'Data/stock_data_{today}.csv'
os.makedirs('Data', exist_ok=True)
stock_data.to_csv(stock_data_file, index=False)

# Step 3: Perform combined strategy analysis
combined_results_file = f'Data/combined_results_{today}.txt'
combine_analysis(stock_data, combined_results_file)
