import os
import pandas as pd
from Strategies import (
    contrarian, deep_value, defensive, dividend, esg,
    growth, momentum, quality, value
)

def combine_analysis(df):
    strategies = {
        "Contrarian": contrarian.contrarian_strategy,
        "Deep Value": deep_value.deep_value_strategy,
        "Defensive": defensive.defensive_strategy,
        "Dividend": dividend.dividend_strategy,
        "ESG": esg.esg_strategy,
        "Growth": growth.growth_strategy,
        "Momentum": momentum.momentum_strategy,
        "Quality": quality.quality_strategy,
        "Value": value.value_strategy,

    }
    all_results = []
    for name, strategy_func in strategies.items():
        print(f"Running {name} strategy...")
        result = strategy_func(df)
        if not result.empty:
            all_results.append(result)

    return pd.concat(all_results, ignore_index=True) if all_results else pd.DataFrame()
