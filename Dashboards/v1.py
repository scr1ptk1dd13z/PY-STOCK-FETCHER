# Required imports
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from IPython.display import display, HTML
import numpy as np

def clean_financial_metrics(df):
    """
    Cleans financial metrics by handling infinities and outliers
    """
    cleaned_df = df.copy()
    
    # Replace infinite values with NaN
    cleaned_df = cleaned_df.replace([np.inf, -np.inf], np.nan)
    
    # For PE Ratio, filter out extreme values (e.g., above 500)
    if 'PE Ratio' in cleaned_df.columns:
        cleaned_df.loc[cleaned_df['PE Ratio'] > 500, 'PE Ratio'] = np.nan
        cleaned_df.loc[cleaned_df['PE Ratio'] < -500, 'PE Ratio'] = np.nan
    
    return cleaned_df

def create_key_metrics_cards(df):
    """
    Creates a row of cards showing key metrics with better handling of edge cases
    """
    # Clean the data first
    df = clean_financial_metrics(df)
    
    metrics_html = """
    <div style="display: flex; justify-content: space-between; flex-wrap: wrap; margin: 20px 0;">
    """
    
    # Calculate metrics with proper error handling
    def safe_mean(series, decimals=2):
        clean_series = series.dropna()
        if len(clean_series) == 0:
            return "N/A"
        mean_val = clean_series.mean()
        if isinstance(mean_val, (int, float)):
            return f"{mean_val:.{decimals}f}"
        return "N/A"
    
    def format_market_cap(value):
        if pd.isna(value) or value == "N/A":
            return "N/A"
        if value >= 1e12:
            return f"${value/1e12:.2f}T"
        if value >= 1e9:
            return f"${value/1e9:.2f}B"
        if value >= 1e6:
            return f"${value/1e6:.2f}M"
        return f"${value:,.0f}"
    
    # Calculate average metrics with better handling
    metrics = [
        ('Average P/E Ratio', safe_mean(df['PE Ratio'].loc[lambda x: (x > 0) & (x < 500)])),
        ('Average Market Cap', format_market_cap(df['Market Cap'].dropna().mean())),
        ('Average Dividend Yield', f"{safe_mean(df['Dividend Yield'].dropna() * 100)}%"),
        ('Average Profit Margin', f"{safe_mean(df['Profit Margins'].dropna() * 100)}%")
    ]
    
    for title, value in metrics:
        metrics_html += f"""
        <div style="flex: 1; min-width: 200px; margin: 10px; padding: 20px; 
                    background-color: #2d2d2d; border-radius: 10px; box-shadow: 0 2px 5px rgba(0,0,0,0.3);">
            <h3 style="margin: 0; color: #e0e0e0;">{title}</h3>
            <p style="font-size: 24px; margin: 10px 0 0 0; color: #ffffff;">{value}</p>
        </div>
        """
    
    metrics_html += "</div>"
    return HTML(metrics_html)

def load_and_prepare_data():
    """
    Loads data from uploaded CSV file and performs initial preprocessing with better error handling
    """
    from google.colab import files
    print("Please upload your CSV file...")
    uploaded = files.upload()
    file_name = list(uploaded.keys())[0]
    df = pd.read_csv(file_name)
    
    # Clean numeric columns by converting to numeric and handling NaN values
    numeric_columns = ['Market Cap', 'PE Ratio', 'Profit Margins', 'Current Price', 'Dividend Yield']
    for col in numeric_columns:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
    
    # Clean the financial metrics
    df = clean_financial_metrics(df)
    
    return df

def create_key_metrics_cards(df):
    """
    Creates a row of cards showing key metrics
    """
    metrics_html = """
    <div style="display: flex; justify-content: space-between; flex-wrap: wrap; margin: 20px 0;">
    """
    
    # Calculate average metrics with NaN handling
    avg_pe = df['PE Ratio'].dropna().mean()
    avg_market_cap = df['Market Cap'].dropna().mean()
    avg_dividend_yield = df['Dividend Yield'].dropna().mean() * 100
    avg_profit_margin = df['Profit Margins'].dropna().mean() * 100
    
    # Create metric cards
    metrics = [
        ('Average P/E Ratio', f"{avg_pe:.2f}"),
        ('Average Market Cap', f"${avg_market_cap:,.0f}"),
        ('Average Dividend Yield', f"{avg_dividend_yield:.2f}%"),
        ('Average Profit Margin', f"{avg_profit_margin:.2f}%")
    ]
    
    for title, value in metrics:
        metrics_html += f"""
        <div style="flex: 1; min-width: 200px; margin: 10px; padding: 20px; 
                    background-color: #2d2d2d; border-radius: 10px; box-shadow: 0 2px 5px rgba(0,0,0,0.3);">
            <h3 style="margin: 0; color: #e0e0e0;">{title}</h3>
            <p style="font-size: 24px; margin: 10px 0 0 0; color: #ffffff;">{value}</p>
        </div>
        """
    
    metrics_html += "</div>"
    return HTML(metrics_html)

def create_sector_distribution(df):
    """
    Creates a pie chart showing sector distribution
    """
    sector_dist = df['Sector'].value_counts()
    fig = px.pie(values=sector_dist.values, 
                 names=sector_dist.index, 
                 title='Market Distribution by Sector')
    
    # Update layout for dark theme
    fig.update_layout(
        template='plotly_dark',
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    return fig

def create_performance_scatter(df):
    """
    Creates a scatter plot of PE Ratio vs Market Cap with Profit Margins as color
    """
    # Remove rows with NaN values in required columns
    df_clean = df.dropna(subset=['PE Ratio', 'Market Cap', 'Profit Margins'])
    
    fig = px.scatter(df_clean, 
                    x='PE Ratio',
                    y='Market Cap',
                    color='Profit Margins',
                    size='Market Cap',
                    size_max=60,
                    hover_data=['Symbol', 'Current Price'],
                    title='Company Performance Overview')
    
    # Update layout for dark theme
    fig.update_layout(
        template='plotly_dark',
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    return fig

def create_margin_comparison(df):
    """
    Creates an improved box plot comparing different margin types
    """
    margin_cols = ['Gross Margins', 'Operating Margins', 'Profit Margins', 'EBITDA Margins']
    margin_data = []
    
    for col in margin_cols:
        if col in df.columns:
            # Convert to percentage and filter out extreme values
            values = df[col].dropna() * 100
            # Remove extreme outliers (values beyond 3 standard deviations)
            mean = values.mean()
            std = values.std()
            filtered_values = values[abs(values - mean) <= 3*std]
            
            margin_data.extend([{
                'Margin Type': col.replace(' Margins', ''),
                'Value': value
            } for value in filtered_values])
    
    if margin_data:
        margin_df = pd.DataFrame(margin_data)
        
        # Create figure with more detailed styling
        fig = go.Figure()
        
        for margin_type in margin_df['Margin Type'].unique():
            values = margin_df[margin_df['Margin Type'] == margin_type]['Value']
            
            fig.add_trace(go.Box(
                y=values,
                name=margin_type,
                boxpoints='outliers',  # Show outliers
                jitter=0.3,  # Add jitter to points
                pointpos=-1.8,  # Position of points
                marker_color='rgb(107,174,214)',
                line_color='rgb(107,174,214)',
                boxmean=True  # Add mean line
            ))
        
        # Update layout with better formatting
        fig.update_layout(
            title={
                'text': 'Margin Distribution Analysis',
                'y':0.95,
                'x':0.5,
                'xanchor': 'center',
                'yanchor': 'top',
                'font': {'size': 24}
            },
            yaxis_title={
                'text': 'Percentage (%)',
                'font': {'size': 16}
            },
            xaxis_title={
                'text': 'Margin Type',
                'font': {'size': 16}
            },
            template='plotly_dark',
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            showlegend=False,
            height=600,  # Increase height
            yaxis=dict(
                gridcolor='rgba(128,128,128,0.2)',
                zerolinecolor='rgba(128,128,128,0.2)',
                tickfont={'size': 14},
                range=[0, 100]  # Set y-axis range from 0 to 100%
            ),
            xaxis=dict(
                tickfont={'size': 14}
            ),
            margin=dict(t=100, b=50, l=50, r=50)
        )
        
        # Add annotations for median values
        for i, margin_type in enumerate(margin_df['Margin Type'].unique()):
            values = margin_df[margin_df['Margin Type'] == margin_type]['Value']
            median = values.median()
            
            fig.add_annotation(
                x=margin_type,
                y=median,
                text=f"Median: {median:.1f}%",
                showarrow=True,
                arrowhead=2,
                arrowsize=1,
                arrowwidth=2,
                arrowcolor="white",
                font=dict(size=12, color="white"),
                bgcolor="rgba(0,0,0,0.6)",
                bordercolor="white",
                borderwidth=1,
                borderpad=4,
                xshift=40
            )
        
        return fig
    return None

def generate_dashboard():
    """
    Main function to generate the complete dashboard
    """
    # Load data
    df = load_and_prepare_data()
    
    # Display title with dark theme styling
    display(HTML("""
        <h1 style='text-align: center; color: #ffffff; 
                   text-shadow: 2px 2px 4px rgba(0,0,0,0.5); 
                   font-family: "Courier New", monospace;'>
            scr1ptk1dd13z Dashboard 1.0
        </h1>
    """))
    
    # Display key metrics cards
    display(create_key_metrics_cards(df))
    
    # Create and display visualizations
    visualizations = [
        create_sector_distribution(df),
        create_performance_scatter(df),
        create_margin_comparison(df)
    ]
    
    # Display only non-None visualizations
    for fig in visualizations:
        if fig is not None:
            fig.show()

# Run the dashboard
generate_dashboard()
