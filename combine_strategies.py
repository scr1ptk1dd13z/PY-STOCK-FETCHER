import pandas as pd
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def combine_csv(input_folder: str, output_file: str) -> None:
    """
    Combine multiple strategy CSV files into a single file.

    Args:
        input_folder (str): Folder containing input CSV files.
        output_file (str): File path to save the combined CSV.
    """
    try:
        logging.info(f"Combining CSV files in {input_folder}...")
        combined_df = pd.concat(
            [pd.read_csv(f"{input_folder}/{file}") for file in os.listdir(input_folder) if file.endswith(".csv")]
        )
        combined_df.to_csv(output_file, index=False)
        logging.info(f"Combined CSV saved to {output_file}")
    except Exception as e:
        logging.error(f"Error during CSV combination: {e}")

if __name__ == "__main__":
    input_folder = "Data/Strategies"
    output_file = "Data/combined_output.csv"
    combine_csv(input_folder, output_file)
