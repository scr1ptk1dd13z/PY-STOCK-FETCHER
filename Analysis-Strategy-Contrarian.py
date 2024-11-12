import pandas as pd
from google.colab import files

# Step 1: Prompt user to upload the CSV file
uploaded = files.upload()

# Load the uploaded CSV file into a DataFrame
for filename in uploaded.keys():
    df = pd.read_csv(filename)

# Define the contrarian investing filter function
def filter_stocks_contrarian(df):
    # Drop rows with missing values in key contrarian columns
    df = df.dropna(subset=['1-Year Return', 'Price to Book', 'Trailing EPS', 'Recommendation Mean'])

    # Filter stocks based on contrarian criteria
    filtered_df = df[
        (df['1-Year Return'] < -0.1) &          # Negative return of at least -10% in the past year
        (df['Price to Book'] < 1.0) &           # Low P/B ratio (indicating potential undervaluation)
        (df['Trailing EPS'] > 0) &              # Positive EPS (financially healthy)
        (df['Recommendation Mean'] <= 3.0)      # Low analyst rating (potential for improvement)
    ].copy()

    # Calculate Contrarian Score (using a weighted formula based on the above criteria)
    filtered_df['Contrarian Score'] = (
        (filtered_df['1-Year Return'].abs() * 0.4) +    # Weight higher negative returns
        (1 / filtered_df['Price to Book'] * 0.3) +      # Weight undervaluation
        (filtered_df['Trailing EPS'] * 0.2) +           # Financial health
        (3.0 - filtered_df['Recommendation Mean']) * 0.1 # Analyst improvement expectation
    )

    # Select the top 10 stocks based on the Contrarian Score
    top_10_stocks = filtered_df.nlargest(10, 'Contrarian Score')

    # Add clickable Yahoo Finance link to the ticker symbol
    top_10_stocks['Symbol'] = top_10_stocks['Symbol'].apply(
        lambda x: f'<a href="https://finance.yahoo.com/quote/{x}" target="_blank">{x}</a>'
    )

    return top_10_stocks

# Step 2: Apply the contrarian filter function
top_10_stocks_contrarian = filter_stocks_contrarian(df)

# Step 3: Save the symbols to a text file, one symbol per line
output_file = 'top_10_stocks_contrarian.txt'
with open(output_file, 'w') as f:
    for symbol in top_10_stocks_contrarian['Symbol']:
        f.write(f"{symbol}\n")

files.download(output_file)

# Display the selected stocks with detailed info and clickable Yahoo Finance links in Colab
top_10_stocks_contrarian_display = top_10_stocks_contrarian[['Symbol', 'Name', 'Sector', 'Industry', 'Country', 'Currency', 'Exchange', 'Current Price', 'Market Cap', '1-Year Return', 'Price to Book', 'Trailing EPS', 'Recommendation Mean', 'Contrarian Score']]

# Make the ticker symbols clickable
top_10_stocks_contrarian_display = top_10_stocks_contrarian_display.style.format({'Symbol': lambda x: x})
top_10_stocks_contrarian_display
