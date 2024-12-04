import pandas as pd

def load_from_csv(filepath):
    return pd.read_csv(filepath)

def save_to_csv(dataframe, filepath):
    dataframe.to_csv(filepath, index=False)
    print(f"Data saved to {filepath}")
