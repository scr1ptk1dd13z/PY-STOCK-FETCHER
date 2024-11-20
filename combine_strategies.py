import pandas as pd

# Import strategy functions from their respective modules
from Analysis.Strategy.Investing.Growth import filter_stocks_growth
from Analysis.Strategy.Investing.Income import filter_stocks_income
from Analysis.Strategy.Investing.Sector_Rotation import filter_stocks_sector_rotation
from Analysis.Strategy.Investing.ESG import filter_stocks_esg
from Analysis.Strategy.Investing.Small_Cap import filter_stocks_small_cap
from Analysis.Strategy.Investing.Dividend import filter_stocks_dividend
from Analysis.Strategy.Investing.Value import filter_stocks_value
from Analysis.Strategy.Investing.Turnaround import filter_stocks_turnaround
from Analysis.Strategy.Investing.Deep_Value import filter_stocks_deep_value
from Analysis.Strategy.Investing.Quality import filter_stocks_quality
from Analysis.Strategy.Investing.Momentum import filter_stocks_momentum
from Analysis.Strategy.Investing.Defensive import filter_stocks_defensive
from Analysis.Strategy.Investing.Contrarian import filter_stocks_contrarian

# Input and output file paths
input_csv = "Data/nyse_daily_stock_data.csv"  # Adjust the path if necessary
output_csv = "Data/combined_output.csv"

# Load the input data
print(f"Loading input data from {input_csv}...")
df = pd.read_csv(input_csv)

# Initialize an empty list to store results from each strategy
results = []

# Define a helper function to run a strategy and append results
def run_strategy(filter_function, strategy_name):
    try:
        print(f"Running {strategy_name} strategy...")
        filtered_df = filter_function(df)
        filtered_df["Strategy"] = strategy_name  # Add a strategy column
        results.append(filtered_df)
    except Exception as e:
        print(f"Error in {strategy_name} strategy: {e}")

# Run all strategies
run_strategy(filter_stocks_growth, "Growth")
run_strategy(filter_stocks_income, "Income")
run_strategy(filter_stocks_sector_rotation, "Sector Rotation")
run_strategy(filter_stocks_esg, "ESG")
run_strategy(filter_stocks_small_cap, "Small-Cap")
run_strategy(filter_stocks_dividend, "Dividend")
run_strategy(filter_stocks_value, "Value")
run_strategy(filter_stocks_turnaround, "Turnaround")
run_strategy(filter_stocks_deep_value, "Deep Value")
run_strategy(filter_stocks_quality, "Quality")
run_strategy(filter_stocks_momentum, "Momentum")
run_strategy(filter_stocks_defensive, "Defensive")
run_strategy(filter_stocks_contrarian, "Contrarian")

# Combine all results into a single DataFrame
print("Combining results from all strategies...")
combined_results = pd.concat(results, ignore_index=True)

# Save the combined results to CSV
print(f"Saving combined results to {output_csv}...")
combined_results.to_csv(output_csv, index=False)

print("Done!")
