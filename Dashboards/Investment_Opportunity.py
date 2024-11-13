import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from IPython.display import display, HTML
import numpy as np
from plotly.subplots import make_subplots

def load_and_prepare_data():
    """
    Loads and prepares data with investment-specific cleaning
    """
    from google.colab import files
    print("Please upload your CSV file...")
    uploaded = files.upload()
    file_name = list(uploaded.keys())[0]
    df = pd.read_csv(file_name)
    
    # Convert numeric columns
    numeric_columns = [
        'Market Cap', 'PE Ratio', 'Price to Book', 'Price to Sales',
        'Profit Margins', 'Operating Margins', 'Current Ratio',
        'Debt to Equity', 'Return on Equity', 'Return on Assets',
        'Revenue Growth (YoY)', 'Current Price'
    ]
    
    for col in numeric_columns:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
    
    return clean_financial_metrics(df)

def clean_financial_metrics(df):
    """
    Investment-specific data cleaning
    """
    cleaned_df = df.copy()
    cleaned_df = cleaned_df.replace([np.inf, -np.inf], np.nan)
    
    # Remove extreme outliers
    metrics_limits = {
        'PE Ratio': (0, 500),
        'Price to Book': (0, 100),
        'Price to Sales': (0, 100),
        'Debt to Equity': (0, 1000),
        'Current Ratio': (0, 100),
        'Return on Equity': (-100, 100),
        'Return on Assets': (-100, 100),
        'Revenue Growth (YoY)': (-100, 1000)
    }
    
    for metric, (min_val, max_val) in metrics_limits.items():
        if metric in cleaned_df.columns:
            cleaned_df.loc[cleaned_df[metric] > max_val, metric] = np.nan
            cleaned_df.loc[cleaned_df[metric] < min_val, metric] = np.nan
    
    return cleaned_df

def calculate_opportunity_score(row):
    """
    Calculate an investment opportunity score based on key metrics
    """
    score = 0
    weights = {
        'PE Ratio': -0.2,  # Lower is better
        'Price to Book': -0.15,  # Lower is better
        'Return on Equity': 0.2,  # Higher is better
        'Revenue Growth (YoY)': 0.2,  # Higher is better
        'Profit Margins': 0.15,  # Higher is better
        'Current Ratio': 0.1,  # Higher is better
    }
    
    for metric, weight in weights.items():
        if metric in row and pd.notna(row[metric]):
            # Normalize the value between 0 and 1
            if metric in ['PE Ratio', 'Price to Book']:
                # For metrics where lower is better
                score += weight * (1 - min(row[metric]/100, 1))
            else:
                # For metrics where higher is better
                score += weight * min(max(row[metric]/100, 0), 1)
    
    return max(min(score * 100, 100), 0)  # Scale to 0-100

def create_opportunity_dashboard(df):
    """
    Creates the main investment opportunity dashboard
    """
    # Calculate opportunity scores
    df['Opportunity Score'] = df.apply(calculate_opportunity_score, axis=1)
    
    # Create the dashboard layout
    display(HTML("""
        <h1 style='text-align: center; color: #ffffff; 
                   text-shadow: 2px 2px 4px rgba(0,0,0,0.5); 
                   font-family: "Courier New", monospace;'>
            Investment Opportunity Screener 1.0
        </h1>
    """))
    
    # Top opportunities card
    top_opportunities = df.nlargest(5, 'Opportunity Score')
    opportunities_html = """
    <div style="background-color: #2d2d2d; padding: 20px; border-radius: 10px; margin: 20px 0;">
        <h2 style="color: #ffffff; margin-bottom: 15px;">Top 5 Investment Opportunities</h2>
        <div style="display: flex; flex-wrap: wrap; gap: 10px;">
    """
    
    for _, company in top_opportunities.iterrows():
        opportunities_html += f"""
        <div style="flex: 1; min-width: 250px; background-color: #3d3d3d; padding: 15px; border-radius: 8px;">
            <h3 style="color: #ffffff; margin: 0;">{company['Symbol']}</h3>
            <p style="color: #e0e0e0; margin: 5px 0;">Score: {company['Opportunity Score']:.1f}</p>
            <p style="color: #e0e0e0; margin: 5px 0;">P/E: {company['PE Ratio']:.1f}</p>
            <p style="color: #e0e0e0; margin: 5px 0;">ROE: {company['Return on Equity']:.1f}%</p>
            <p style="color: #e0e0e0; margin: 5px 0;">Growth: {company['Revenue Growth (YoY)']:.1f}%</p>
        </div>
        """
    
    opportunities_html += "</div></div>"
    display(HTML(opportunities_html))
    
    # Create visualizations
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=(
            'Opportunity Score vs Market Cap',
            'Growth vs Profitability',
            'Value Metrics Distribution',
            'Financial Health Indicators'
        )
    )
    
    # 1. Opportunity Score vs Market Cap
    fig.add_trace(
        go.Scatter(
            x=df['Market Cap'],
            y=df['Opportunity Score'],
            mode='markers',
            text=df['Symbol'],
            marker=dict(
                size=10,
                color=df['Opportunity Score'],
                colorscale='Viridis',
                showscale=True
            ),
            name='Companies'
        ),
        row=1, col=1
    )
    
    # 2. Growth vs Profitability
    fig.add_trace(
        go.Scatter(
            x=df['Revenue Growth (YoY)'],
            y=df['Profit Margins'],
            mode='markers',
            text=df['Symbol'],
            marker=dict(
                size=10,
                color=df['Opportunity Score'],
                colorscale='Viridis'
            ),
            name='Growth/Profit'
        ),
        row=1, col=2
    )
    
    # 3. Value Metrics
    fig.add_trace(
        go.Box(
            y=df['PE Ratio'],
            name='P/E Ratio',
            boxmean=True
        ),
        row=2, col=1
    )
    fig.add_trace(
        go.Box(
            y=df['Price to Book'],
            name='P/B Ratio',
            boxmean=True
        ),
        row=2, col=1
    )
    
    # 4. Financial Health
    fig.add_trace(
        go.Scatter(
            x=df['Current Ratio'],
            y=df['Debt to Equity'],
            mode='markers',
            text=df['Symbol'],
            marker=dict(
                size=10,
                color=df['Opportunity Score'],
                colorscale='Viridis'
            ),
            name='Financial Health'
        ),
        row=2, col=2
    )
    
    # Update layout
    fig.update_layout(
        height=800,
        template='plotly_dark',
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        showlegend=False
    )
    
    fig.show()
    
    # Create sector analysis
    sector_scores = df.groupby('Sector')['Opportunity Score'].mean().sort_values(ascending=False)
    
    fig_sector = px.bar(
        sector_scores,
        title='Average Opportunity Score by Sector',
        template='plotly_dark'
    )
    
    fig_sector.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        height=400
    )
    
    fig_sector.show()

def generate_dashboard():
    """
    Main function to generate the investment dashboard
    """
    df = load_and_prepare_data()
    create_opportunity_dashboard(df)

# Run the dashboard
generate_dashboard()
