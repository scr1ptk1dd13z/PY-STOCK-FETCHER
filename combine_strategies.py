import os
import pandas as pd
from Strategies import (
    contrarian, deep_value, defensive, dividend, esg,
    growth, momentum, quality, value,
    # Adding missing imports
    income, sector_rotation, small_cap, turn_around
)

def combine_analysis(df):
    strategies = {
        "Contrarian": contrarian.contrarian_strategy,
        "Deep Value": deep_value.deep_value_strategy,
        "Defensive": defensive.defensive_strategy,
        "Dividend": dividend.dividend_strategy,
        "ESG": esg.esg_strategy,
        "Growth": growth.growth_strategy,
        "Income": income.income_strategy,
        "Momentum": momentum.momentum_strategy,
        "Quality": quality.quality_strategy,
        "Sector Rotation": sector_rotation.sector_rotation_strategy,
        "Small Cap": small_cap.small_cap_strategy,
        "Turn Around": turn_around.turn_around_strategy,
        "Value": value.value_strategy,
    }
    
    all_results = []
    for name, strategy_func in strategies.items():
        try:
            print(f"Running {name} strategy...")
            result = strategy_func(df)
            if not result.empty:
                # Add strategy name as a column to track strategy origin
                result['Strategy'] = name
                all_results.append(result)
        except Exception as e:
            print(f"Error in {name} strategy: {e}")
    
    return pd.concat(all_results, ignore_index=True) if all_results else pd.DataFrame()

# Optional: Add a main function for testing
def main():
    # Example usage
    df = pd.read_csv('your_stock_data.csv')  # Replace with actual data loading
    combined_results = combine_analysis(df)
    print(combined_results)

if __name__ == "__main__":
    main()
