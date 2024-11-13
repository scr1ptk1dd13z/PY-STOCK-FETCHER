# Financial Analysis Toolkit 📊
A comprehensive Python-based toolkit for financial market analysis, value investing screening, and automated stock data collection. This project combines powerful financial data gathering with sophisticated analysis tools, designed for both professional investors and financial analysts.
# 🌟 Key Features
## 1. Automated Data Collection (script_v7.py)

- Multi-threaded stock data fetching from Yahoo Finance
- Comprehensive financial metrics collection (50+ data points per stock)
- Supports multiple exchanges (NYSE, TSX)
- Automatic CSV and Excel export
- Built-in retry mechanism for reliable data collection

## 2. Value Investing Analysis (Value.py)

- Implements Graham-style value investing principles
- Sophisticated stock screening based on:
  - P/E Ratio
  - Price-to-Book
  - PEG Ratio
  - Dividend Yield
  - Debt-to-Equity
  - Free Cash Flow
- Proprietary value scoring system
- Automated generation of top value stock picks

## 3. Sector Analysis Dashboard (Sector_v1.py)
- Interactive visualizations using Plotly
- Key metrics dashboard including:
  - Sector distribution analysis
  - Performance scatter plots
  - Margin comparison analysis
- Dark theme optimized interface
- Real-time financial metrics calculations

## 4. Excel Report Generation (XLSX_Sector_v1.py)
- Automated Excel report creation with advanced formatting
- Sector and industry-based grouping
- Interactive Yahoo Finance hyperlinks
- Conditional formatting for key metrics
- Advanced number formatting and data presentation

# 📋 Requirements
python
```
pandas
yfinance
plotly
openpyxl
numpy
google-colab (if running in Colab)
```

# 🚀 Quick Start
## 1. Clone the repository:
bash
```
git clone https://github.com/yourusername/financial-analysis-toolkit.git
```
## 2. Install dependencies:
python
```
pip install -r requirements.txt
```
## 3. Run the main data collection script:
python
```
python script_v7.py
```

# 📊 Usage Examples
## Collecting Stock Data
python
```
from script_v7 import fetch_stock_data

### Fetch data for specific tickers
tickers = ['AAPL', 'MSFT', 'GOOGL']
stock_data = fetch_stock_data(tickers)
```
### Running Value Analysis
python
```
from Value import filter_stocks_value

### Filter stocks based on value criteria
value_stocks = filter_stocks_value(stock_data)
```
# 📈 Analysis Methodology
## Value Investing Metrics
- PE Ratio < 15: Traditional value indicator
- Price-to-Book < 3: Asset-based valuation metric
- PEG Ratio < 1: Growth-adjusted valuation
- Dividend Yield > 2%: Income potential
- Debt-to-Equity < 1: Financial health indicator
- Positive Free Cash Flow: Operational efficiency

## Scoring System
The toolkit employs a weighted scoring system:
- P/E Score (20%)
- Dividend Score (20%)
- P/B Score (15%)
- PEG Score (15%)
- Debt Score (15%)
- Free Cash Flow Score (15%)

# 🛠 Advanced Features
## Custom Data Collection
- Configurable retry mechanism
- Threaded data collection for improved performance
- Extensive error handling
- Automatic data cleaning and formatting

## Report Customization
- Configurable Excel formatting rules
- Custom financial metric calculations
- Adjustable screening criteria
- Flexible visualization options

# 📝 License
MIT License - see LICENSE.md for details

# 🤝 Contributing
1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a new Pull Request

# 💡 Support
For support and questions, please open an issue in the GitHub repository.

# 🔄 Regular Updates
The toolkit is regularly updated with:
- New financial metrics
- Improved analysis algorithms
- Enhanced visualization options
- Additional data sources

# ⚠️ Disclaimer
This toolkit is for educational and research purposes only. Always conduct your own due diligence before making investment decisions.
