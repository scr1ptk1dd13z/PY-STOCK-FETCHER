import pandas as pd
from google.colab import files
from datetime import datetime

# Step 1: Prompt user to upload the CSV file
uploaded = files.upload()

# Load the uploaded CSV file into a DataFrame
for filename in uploaded.keys():
    df = pd.read_csv(filename)

def filter_stocks_income(df):
    # Drop rows with missing values in key dividend columns
    dividend_columns = [
        'Dividend Rate', 'Dividend Yield', 'Payout Ratio', 
        'Five-Year Avg. Dividend Yield', 'Free Cash Flow',
        'Operating Cash Flow', 'Current Price'
    ]
    df = df.dropna(subset=dividend_columns)

    # Filter stocks based on income/dividend criteria
    filtered_df = df[
        (df['Dividend Yield'] > 0.03) &          # Minimum 3% dividend yield
        (df['Payout Ratio'] < 0.75) &            # Conservative payout ratio < 75%
        (df['Free Cash Flow'] > 0) &             # Positive free cash flow
        (df['Operating Cash Flow'] > 0) &        # Positive operating cash flow
        (df['Five-Year Avg. Dividend Yield'] > 0)  # Has dividend history
    ].copy()

    # Calculate dividend coverage ratio (Free Cash Flow / Total Dividend Payments)
    filtered_df['Dividend Coverage'] = filtered_df.apply(
        lambda row: row['Free Cash Flow'] / (row['Dividend Rate'] * row['Market Cap'] / row['Current Price'])
        if row['Dividend Rate'] > 0 else 0, axis=1
    )

    # Calculate Income Score components
    filtered_df['Yield_Score'] = filtered_df['Dividend Yield'] / filtered_df['Dividend Yield'].max()
    filtered_df['Payout_Score'] = 1 - (filtered_df['Payout Ratio'] / filtered_df['Payout Ratio'].max())
    filtered_df['Coverage_Score'] = filtered_df['Dividend Coverage'] / filtered_df['Dividend Coverage'].max()
    filtered_df['Historical_Score'] = filtered_df['Five-Year Avg. Dividend Yield'] / filtered_df['Five-Year Avg. Dividend Yield'].max()
    filtered_df['FCF_Score'] = filtered_df['Free Cash Flow'] / filtered_df['Free Cash Flow'].max()

    # Calculate weighted Income Score
    filtered_df['Income Score'] = (
        filtered_df['Yield_Score'] * 0.30 +          # Current yield is most important
        filtered_df['Payout_Score'] * 0.20 +         # Sustainable payout ratio
        filtered_df['Coverage_Score'] * 0.20 +       # Strong dividend coverage
        filtered_df['Historical_Score'] * 0.15 +     # Consistent dividend history
        filtered_df['FCF_Score'] * 0.15             # Strong cash flow support
    )

    # Select the top 10 stocks based on the Income Score
    top_10_stocks = filtered_df.nlargest(10, 'Income Score')

    # Add clickable Yahoo Finance link to the ticker symbol
    top_10_stocks['Symbol_Link'] = top_10_stocks['Symbol'].apply(
        lambda x: f'<a href="https://finance.yahoo.com/quote/{x}" target="_blank">{x}</a>'
    )

    # Round the scores for better display
    score_columns = ['Yield_Score', 'Payout_Score', 'Coverage_Score', 'Historical_Score', 'FCF_Score', 'Income Score']
    top_10_stocks[score_columns] = top_10_stocks[score_columns].round(3)

    return top_10_stocks

# Apply the income filter function
top_10_stocks_income = filter_stocks_income(df)

# Save the symbols to a text file
output_file = 'top_10_stocks_income.txt'
with open(output_file, 'w') as f:
    for symbol in top_10_stocks_income['Symbol']:
        f.write(f"{symbol}\n")

files.download(output_file)

# Prepare display columns with key metrics and scores
display_columns = [
    'Symbol_Link', 'Name', 'Sector', 'Industry',
    'Current Price', 'Dividend Rate', 'Dividend Yield',
    'Five-Year Avg. Dividend Yield', 'Payout Ratio',
    'Dividend Coverage', 'Free Cash Flow',
    'Operating Cash Flow', 'Income Score'
]

# Create final display DataFrame
display_df = top_10_stocks_income[display_columns].copy()
display_df = display_df.rename(columns={'Symbol_Link': 'Symbol'})

# Format numeric columns for better readability
format_dict = {
    'Current Price': '${:.2f}',
    'Dividend Rate': '${:.2f}',
    'Dividend Yield': '{:.1%}',
    'Five-Year Avg. Dividend Yield': '{:.1%}',
    'Payout Ratio': '{:.1%}',
    'Dividend Coverage': '{:.2f}x',
    'Free Cash Flow': '${:,.0f}M',
    'Operating Cash Flow': '${:,.0f}M',
    'Income Score': '{:.3f}'
}

# Apply formatting
for col, fmt in format_dict.items():
    if col in display_df.columns:
        if col in ['Free Cash Flow', 'Operating Cash Flow']:
            display_df[col] = display_df[col].apply(lambda x: fmt.format(x/1000000))  # Convert to millions
        else:
            display_df[col] = display_df[col].apply(lambda x: fmt.format(x))

# Display with HTML rendering enabled for clickable links
from IPython.display import HTML
HTML(display_df.to_html(escape=False))
