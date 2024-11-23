# Define the turnaround investing filter function
def filter_stocks_turnaround(df):
    # Drop rows with missing values in key turnaround columns
    df = df.dropna(subset=['Earnings Growth (YoY)', 'Operating Margins', 'Total Debt', 'Current Price'])

    # Filter stocks based on turnaround criteria
    filtered_df = df[
        (df['Earnings Growth (YoY)'] > 0.1) &                # Positive earnings growth YoY (at least 10%)
        (df['Operating Margins'] > 0) &                      # Positive operating margins (company showing profitability)
        (df['Total Debt'] < df['Market Cap'])                # Debt less than the market cap (manageable debt)
    ].copy()

    # Calculate Turnaround Score
    filtered_df['Turnaround Score'] = (
        (filtered_df['Earnings Growth (YoY)'] * 0.5) +      # Weight earnings growth heavily
        (filtered_df['Operating Margins'] * 0.3) -          # Weight profitability positively
        (filtered_df['Total Debt'] / filtered_df['Market Cap'] * 0.2)  # Debt ratio penalty
    )