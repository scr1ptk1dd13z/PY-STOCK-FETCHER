import pandas as pd
import numpy as np
from google.colab import files

# Step 1: Prompt user to upload the CSV file
uploaded = files.upload()

# Load the uploaded CSV file into a DataFrame
for filename in uploaded.keys():
    df = pd.read_csv(filename)

def filter_stocks_blend(df, min_market_cap=1000000000):  # $1B minimum market cap
    # Essential columns for each category
    growth_cols = ['Revenue Growth (YoY)', 'Earnings Growth (YoY)', 'PE Ratio', 'PEG Ratio']
    value_cols = ['PE Ratio', 'Price to Book', 'Price to Sales', 'Enterprise to EBITDA']
    income_cols = ['Dividend Yield', 'Payout Ratio', 'Free Cash Flow']
    defensive_cols = ['Beta', 'Current Ratio', 'Debt to Equity', 'Profit Margins']
    quality_cols = ['Return on Equity', 'Return on Assets', 'Operating Margins', 'EBITDA Margins']
    
    all_required_cols = list(set(growth_cols + value_cols + income_cols + defensive_cols + quality_cols))
    
    # Initial filtering
    filtered_df = df[
        (df['Market Cap'] >= min_market_cap) &  # Size filter
        (df['PE Ratio'] > 0) &                  # Remove negative earnings
        (df['Price to Book'] > 0)               # Remove negative book value
    ].copy()
    
    # Handle missing values - fill with category medians
    for col in all_required_cols:
        if col in filtered_df.columns:
            filtered_df[col] = filtered_df[col].fillna(filtered_df[col].median())

    # 1. Growth Score (20% weight)
    filtered_df['Growth_Score'] = (
        (filtered_df['Revenue Growth (YoY)'] / filtered_df['Revenue Growth (YoY)'].max() * 0.4) +
        (filtered_df['Earnings Growth (YoY)'] / filtered_df['Earnings Growth (YoY)'].max() * 0.4) +
        (1 / (filtered_df['PEG Ratio'] / filtered_df['PEG Ratio'].min()) * 0.2)
    ).clip(0, 1)

    # 2. Value Score (20% weight)
    filtered_df['Value_Score'] = (
        (filtered_df['PE Ratio'].min() / filtered_df['PE Ratio'] * 0.3) +
        (filtered_df['Price to Book'].min() / filtered_df['Price to Book'] * 0.3) +
        (filtered_df['Price to Sales'].min() / filtered_df['Price to Sales'] * 0.2) +
        (filtered_df['Enterprise to EBITDA'].min() / filtered_df['Enterprise to EBITDA'] * 0.2)
    ).clip(0, 1)

    # 3. Income Score (20% weight)
    filtered_df['Income_Score'] = (
        (filtered_df['Dividend Yield'] / filtered_df['Dividend Yield'].max() * 0.4) +
        ((1 - filtered_df['Payout Ratio']) / (1 - filtered_df['Payout Ratio']).max() * 0.3) +
        (filtered_df['Free Cash Flow'] / filtered_df['Free Cash Flow'].max() * 0.3)
    ).clip(0, 1)

    # 4. Defensive Score (20% weight)
    filtered_df['Defensive_Score'] = (
        ((1 - filtered_df['Beta']) / (1 - filtered_df['Beta']).max() * 0.3) +
        (filtered_df['Current Ratio'] / filtered_df['Current Ratio'].max() * 0.3) +
        ((1 - filtered_df['Debt to Equity']) / (1 - filtered_df['Debt to Equity']).max() * 0.2) +
        (filtered_df['Profit Margins'] / filtered_df['Profit Margins'].max() * 0.2)
    ).clip(0, 1)

    # 5. Quality Score (20% weight)
    filtered_df['Quality_Score'] = (
        (filtered_df['Return on Equity'] / filtered_df['Return on Equity'].max() * 0.3) +
        (filtered_df['Return on Assets'] / filtered_df['Return on Assets'].max() * 0.3) +
        (filtered_df['Operating Margins'] / filtered_df['Operating Margins'].max() * 0.2) +
        (filtered_df['EBITDA Margins'] / filtered_df['EBITDA Margins'].max() * 0.2)
    ).clip(0, 1)

    # Calculate final Blend Score
    filtered_df['Blend Score'] = (
        filtered_df['Growth_Score'] * 0.20 +
        filtered_df['Value_Score'] * 0.20 +
        filtered_df['Income_Score'] * 0.20 +
        filtered_df['Defensive_Score'] * 0.20 +
        filtered_df['Quality_Score'] * 0.20
    )

    # Get top 15 stocks
    top_stocks = filtered_df.nlargest(15, 'Blend Score')

    # Add sector diversity check
    sector_counts = top_stocks['Sector'].value_counts()
    over_concentrated = sector_counts[sector_counts > 3].index.tolist()
    
    if over_concentrated:
        # If sectors are over-concentrated, adjust selection
        final_stocks = pd.DataFrame()
        for sector in top_stocks['Sector'].unique():
            sector_stocks = top_stocks[top_stocks['Sector'] == sector].head(3)
            final_stocks = pd.concat([final_stocks, sector_stocks])
        
        # Take top 10 from balanced selection
        top_10_stocks = final_stocks.nlargest(10, 'Blend Score')
    else:
        top_10_stocks = top_stocks.head(10)

    # Add clickable Yahoo Finance link
    top_10_stocks['Symbol_Link'] = top_10_stocks['Symbol'].apply(
        lambda x: f'<a href="https://finance.yahoo.com/quote/{x}" target="_blank">{x}</a>'
    )

    return top_10_stocks

# Apply the blend filter function
top_10_stocks_blend = filter_stocks_blend(df)

# Save the symbols to a text file
output_file = 'top_10_stocks_blend.txt'
with open(output_file, 'w') as f:
    for symbol in top_10_stocks_blend['Symbol']:
        f.write(f"{symbol}\n")

files.download(output_file)

# Prepare display columns with key metrics and scores
display_columns = [
    'Symbol_Link', 'Name', 'Sector', 'Industry',
    'Current Price', 'Market Cap',
    'Revenue Growth (YoY)', 'PE Ratio', 'Price to Book',
    'Dividend Yield', 'Beta', 'Return on Equity',
    'Growth_Score', 'Value_Score', 'Income_Score',
    'Defensive_Score', 'Quality_Score', 'Blend Score'
]

# Create final display DataFrame
display_df = top_10_stocks_blend[display_columns].copy()
display_df = display_df.rename(columns={'Symbol_Link': 'Symbol'})

# Format numeric columns for better readability
format_dict = {
    'Current Price': '${:.2f}',
    'Market Cap': '${:,.0f}M',
    'Revenue Growth (YoY)': '{:.1%}',
    'PE Ratio': '{:.1f}',
    'Price to Book': '{:.2f}',
    'Dividend Yield': '{:.1%}',
    'Beta': '{:.2f}',
    'Return on Equity': '{:.1%}',
    'Growth_Score': '{:.3f}',
    'Value_Score': '{:.3f}',
    'Income_Score': '{:.3f}',
    'Defensive_Score': '{:.3f}',
    'Quality_Score': '{:.3f}',
    'Blend Score': '{:.3f}'
}

# Apply formatting
for col, fmt in format_dict.items():
    if col in display_df.columns:
        if col == 'Market Cap':
            display_df[col] = display_df[col].apply(lambda x: fmt.format(x/1000000))
        else:
            display_df[col] = display_df[col].apply(lambda x: fmt.format(x))

# Add sector diversification analysis
sector_analysis = top_10_stocks_blend['Sector'].value_counts()
sector_summary = f"""
<div style="padding: 10px; margin: 10px 0; border: 1px solid #ddd; border-radius: 5px;">
    <h4>Sector Distribution:</h4>
    {'<br>'.join([f'{sector}: {count} stocks' for sector, count in sector_analysis.items()])}
</div>
"""

# Display with HTML rendering enabled for clickable links
from IPython.display import HTML
html_content = sector_summary + display_df.to_html(escape=False)
HTML(html_content)
