import pandas as pd
from google.colab import files

# Step 1: Prompt user to upload the CSV file
uploaded = files.upload()

# Load the uploaded CSV file into a DataFrame
for filename in uploaded.keys():
    df = pd.read_csv(filename)

def filter_stocks_value(df):
    # Drop rows with missing values in key value investing columns
    value_columns = [
        'PE Ratio', 'Price to Book', 'PEG Ratio', 'Dividend Yield',
        'Debt to Equity', 'Free Cash Flow', 'Market Cap'
    ]
    df = df.dropna(subset=value_columns)

    # Filter stocks based on value criteria
    filtered_df = df[
        (df['PE Ratio'] < 15) &                  # Low P/E ratio
        (df['Price to Book'] < 3) &              # Low P/B ratio
        (df['PEG Ratio'] < 1) &                  # PEG ratio below 1 indicates undervalued growth
        (df['Dividend Yield'] > 0.02) &          # Dividend yield > 2%
        (df['Debt to Equity'] < 1) &             # Conservative debt level
        (df['Free Cash Flow'] > 0)               # Positive free cash flow
    ].copy()

    # Calculate Value Score (weighted formula based on value criteria)
    # Normalize metrics to 0-1 scale for fair comparison
    filtered_df['PE_Score'] = 1 - (filtered_df['PE Ratio'] / filtered_df['PE Ratio'].max())
    filtered_df['PB_Score'] = 1 - (filtered_df['Price to Book'] / filtered_df['Price to Book'].max())
    filtered_df['PEG_Score'] = 1 - (filtered_df['PEG Ratio'] / filtered_df['PEG Ratio'].max())
    filtered_df['Div_Score'] = filtered_df['Dividend Yield'] / filtered_df['Dividend Yield'].max()
    filtered_df['Debt_Score'] = 1 - (filtered_df['Debt to Equity'] / filtered_df['Debt to Equity'].max())
    filtered_df['FCF_Score'] = filtered_df['Free Cash Flow'] / filtered_df['Free Cash Flow'].max()

    # Weighted Value Score calculation
    filtered_df['Value Score'] = (
        filtered_df['PE_Score'] * 0.2 +          # P/E weight
        filtered_df['PB_Score'] * 0.15 +         # P/B weight
        filtered_df['PEG_Score'] * 0.15 +        # PEG weight
        filtered_df['Div_Score'] * 0.2 +         # Dividend yield weight
        filtered_df['Debt_Score'] * 0.15 +       # Debt level weight
        filtered_df['FCF_Score'] * 0.15          # Free cash flow weight
    )

    # Select the top 10 stocks based on the Value Score
    top_10_stocks = filtered_df.nlargest(10, 'Value Score')

    # Add clickable Yahoo Finance link to the ticker symbol
    top_10_stocks['Symbol_Link'] = top_10_stocks['Symbol'].apply(
        lambda x: f'<a href="https://finance.yahoo.com/quote/{x}" target="_blank">{x}</a>'
    )

    # Round the scores for better display
    score_columns = ['PE_Score', 'PB_Score', 'PEG_Score', 'Div_Score', 'Debt_Score', 'FCF_Score', 'Value Score']
    top_10_stocks[score_columns] = top_10_stocks[score_columns].round(3)

    return top_10_stocks

# Apply the value filter function
top_10_stocks_value = filter_stocks_value(df)

# Save the symbols to a text file
output_file = 'top_10_stocks_value.txt'
with open(output_file, 'w') as f:
    for symbol in top_10_stocks_value['Symbol']:
        f.write(f"{symbol}\n")

files.download(output_file)

# Prepare display columns with key metrics and scores
display_columns = [
    'Symbol_Link', 'Name', 'Sector', 'Industry',
    'Current Price', 'Market Cap', 'PE Ratio', 'Price to Book',
    'PEG Ratio', 'Dividend Yield', 'Debt to Equity', 'Free Cash Flow',
    'Value Score'
]

# Create final display DataFrame
display_df = top_10_stocks_value[display_columns].copy()
display_df = display_df.rename(columns={'Symbol_Link': 'Symbol'})

# Format numeric columns for better readability
format_dict = {
    'Current Price': '${:.2f}',
    'Market Cap': '${:,.0f}',
    'PE Ratio': '{:.2f}',
    'Price to Book': '{:.2f}',
    'PEG Ratio': '{:.2f}',
    'Dividend Yield': '{:.1%}',
    'Debt to Equity': '{:.2f}',
    'Free Cash Flow': '${:,.0f}',
    'Value Score': '{:.3f}'
}

# Apply formatting
for col, fmt in format_dict.items():
    if col in display_df.columns:
        display_df[col] = display_df[col].apply(lambda x: fmt.format(x))

# Display with HTML rendering enabled for clickable links
from IPython.display import HTML
HTML(display_df.to_html(escape=False))
