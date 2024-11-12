import pandas as pd
from google.colab import files

# Step 1: Prompt user to upload the CSV file
uploaded = files.upload()

# Load the uploaded CSV file into a DataFrame
for filename in uploaded.keys():
    df = pd.read_csv(filename)

def filter_stocks_defensive(df):
    # Drop rows with missing values in key defensive metrics columns
    defensive_columns = [
        'Beta', 'PE Ratio', 'Current Ratio', 'Profit Margins',
        'Gross Margins', 'Operating Margins', 'EBITDA Margins',
        'Debt to Equity', 'Quick Ratio'
    ]
    df = df.dropna(subset=defensive_columns)

    # Filter stocks based on defensive criteria
    filtered_df = df[
        (df['Beta'] < 1.0) &                     # Low volatility relative to market
        (df['PE Ratio'] > 0) &                   # Positive P/E ratio
        (df['PE Ratio'] < 25) &                  # Not overvalued
        (df['Current Ratio'] > 1.5) &            # Strong liquidity
        (df['Quick Ratio'] > 1.0) &              # Strong quick ratio
        (df['Profit Margins'] > 0.05) &          # Minimum 5% profit margin
        (df['Operating Margins'] > 0.10) &       # Minimum 10% operating margin
        (df['Debt to Equity'] < 0.5)             # Conservative debt levels
    ].copy()

    # Calculate Defensive Score components
    filtered_df['Beta_Score'] = 1 - (filtered_df['Beta'] / filtered_df['Beta'].max())
    filtered_df['PE_Score'] = 1 - (filtered_df['PE Ratio'] / filtered_df['PE Ratio'].max())
    filtered_df['Liquidity_Score'] = filtered_df['Current Ratio'] / filtered_df['Current Ratio'].max()
    filtered_df['Profit_Score'] = filtered_df['Profit Margins'] / filtered_df['Profit Margins'].max()
    filtered_df['Operating_Score'] = filtered_df['Operating Margins'] / filtered_df['Operating Margins'].max()
    filtered_df['Debt_Score'] = 1 - (filtered_df['Debt to Equity'] / filtered_df['Debt to Equity'].max())
    filtered_df['Quick_Score'] = filtered_df['Quick Ratio'] / filtered_df['Quick Ratio'].max()
    filtered_df['Gross_Score'] = filtered_df['Gross Margins'] / filtered_df['Gross Margins'].max()

    # Calculate weighted Defensive Score
    filtered_df['Defensive Score'] = (
        filtered_df['Beta_Score'] * 0.20 +           # Low volatility is key
        filtered_df['PE_Score'] * 0.10 +            # Reasonable valuation
        filtered_df['Liquidity_Score'] * 0.15 +     # Strong liquidity
        filtered_df['Quick_Score'] * 0.10 +         # Quick ratio importance
        filtered_df['Profit_Score'] * 0.15 +        # Profitability
        filtered_df['Operating_Score'] * 0.10 +     # Operating efficiency
        filtered_df['Gross_Score'] * 0.10 +         # Gross margin strength
        filtered_df['Debt_Score'] * 0.10            # Low debt
    )

    # Select the top 10 stocks based on the Defensive Score
    top_10_stocks = filtered_df.nlargest(10, 'Defensive Score')

    # Add clickable Yahoo Finance link to the ticker symbol
    top_10_stocks['Symbol_Link'] = top_10_stocks['Symbol'].apply(
        lambda x: f'<a href="https://finance.yahoo.com/quote/{x}" target="_blank">{x}</a>'
    )

    # Round the scores for better display
    score_columns = ['Beta_Score', 'PE_Score', 'Liquidity_Score', 'Profit_Score', 
                    'Operating_Score', 'Debt_Score', 'Quick_Score', 'Gross_Score', 'Defensive Score']
    top_10_stocks[score_columns] = top_10_stocks[score_columns].round(3)

    return top_10_stocks

# Apply the defensive filter function
top_10_stocks_defensive = filter_stocks_defensive(df)

# Save the symbols to a text file
output_file = 'top_10_stocks_defensive.txt'
with open(output_file, 'w') as f:
    for symbol in top_10_stocks_defensive['Symbol']:
        f.write(f"{symbol}\n")

files.download(output_file)

# Prepare display columns with key metrics and scores
display_columns = [
    'Symbol_Link', 'Name', 'Sector', 'Industry',
    'Current Price', 'Beta', 'PE Ratio', 
    'Current Ratio', 'Quick Ratio',
    'Profit Margins', 'Operating Margins',
    'Gross Margins', 'EBITDA Margins',
    'Debt to Equity', 'Defensive Score'
]

# Create final display DataFrame
display_df = top_10_stocks_defensive[display_columns].copy()
display_df = display_df.rename(columns={'Symbol_Link': 'Symbol'})

# Format numeric columns for better readability
format_dict = {
    'Current Price': '${:.2f}',
    'Beta': '{:.2f}',
    'PE Ratio': '{:.1f}',
    'Current Ratio': '{:.2f}x',
    'Quick Ratio': '{:.2f}x',
    'Profit Margins': '{:.1%}',
    'Operating Margins': '{:.1%}',
    'Gross Margins': '{:.1%}',
    'EBITDA Margins': '{:.1%}',
    'Debt to Equity': '{:.2f}',
    'Defensive Score': '{:.3f}'
}

# Apply formatting
for col, fmt in format_dict.items():
    if col in display_df.columns:
        display_df[col] = display_df[col].apply(lambda x: fmt.format(x))

# Add a sector concentration check
sector_concentration = top_10_stocks_defensive['Sector'].value_counts()
sector_warning = ""
if sector_concentration.max() > 3:
    sector_warning = f"""
    <div style="color: orange; padding: 10px; margin: 10px 0; border: 1px solid orange; border-radius: 5px;">
        ⚠️ Note: {sector_concentration.idxmax()} sector represents {sector_concentration.max()} out of 10 stocks. 
        Consider diversifying across sectors for better risk management.
    </div>
    """

# Display with HTML rendering enabled for clickable links
from IPython.display import HTML
html_content = sector_warning + display_df.to_html(escape=False)
HTML(html_content)
