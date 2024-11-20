# 📈 Stock Data Fetching & Analysis Project

This project provides a complete workflow for gathering, analyzing, and visualizing stock data from top US and Canadian companies, focusing on different investing strategies. The scripts can fetch detailed financial metrics, perform analysis using various investment philosophies, and output formatted files, making it an ideal toolkit for both short-term traders and long-term investors.

## ✨ Features
- 🔍 Data Collection for the NYSE + NASDAQ Companies: Retrieves 4000+ tickers.
- 📊 Comprehensive Financial Metrics: Collects valuation ratios, margins, growth rates, ownership data, and performance metrics.
- 🔄 Resilient Data Fetching: Incorporates retry mechanisms to handle temporary connection issues.
- 💾 Multiple Output Formats: Saves data in CSV and Excel, formatted for easy analysis.
- 📈 Automated Analysis: Provides built-in scripts for various investment strategies, such as Growth, Value, and Defensive investing.
- ⏰ Automated Updates: Configurable GitHub workflow for automatic daily data updates.

## 📁 Project Structure
- `README.md`: Comprehensive documentation for understanding, installing, and using the 
- `LICENSE.md`: Specifies terms and permissions for using and sharing this project.
- `requirements.txt`: Lists Python dependencies.
- `NYSE_SYMBOLS.txt` and TSX_SYMBOLS.txt: Stock ticker files for US and Canadian companies.
- `script_v6.py`, `script_v7.py`: Core scripts for data fetching and processing.
- `/Analysis/Investor/`: Investment analysis scripts based on various philosophies (e.g., Benjamin Graham, Peter Lynch).
- `.github/workflows/run-script-daily.yml`: Workflow file to automate daily script execution on GitHub.

## ⚙️ Installation and Setup
1. Clone the Repository:
```bash
git clone https://github.com/yourusername/colab_stock_info_nyse.git
cd colab_stock_info_nyse
```
2. Install Dependencies:
  - Use Google Colab for streamlined setup: open the main .ipynb file in Colab, which installs required libraries automatically.
  - Alternatively, install dependencies manually:
  - ```bash
    pip install -r requirements.txt
    ```
3. Set Up Google Colab:
  - Upload the project files to your Colab environment.
  - Open the main notebook file in Colab, which will guide you through running scripts and downloading outputs.

## 🚀 Usage Guide
1. Run Data Collection:
  - Open `script_v6.py` or `script_v7.py` in Google Colab or your Python environment.
  - Follow on-screen prompts to fetch stock data, which will save output files in CSV and Excel formats. 
2. Run Investment Analysis:
  - Access specific analysis scripts (e.g., `B_Graham_Relaxed.py`) in the `/Analysis/Investor/` directory.
  - Each script outputs a list of stocks based on its investment philosophy, saved in a separate results folder.
3. Customize & Export Data:
  - Use Google Colab or a Python environment to view and edit CSV/Excel outputs.
  - Optional: Use the generated XLSX files to format data for easy visualization in tools like Looker Studio or Power BI.

## 📅 Automated Workflow
The project includes a GitHub Actions workflow for daily updates:
1. Setup:
  - In the `.github/workflows/` folder, the `run-script-daily.yml` file is preconfigured for daily execution.
2. Configure:
  - Ensure GitHub Actions are enabled in your repo.
  - Customize the schedule by editing the `cron` timing in the YAML file.
3. Run:
  - The workflow will automatically fetch and update data daily, saving the latest files in your repository.

## 📊 Output Explanation
  - Data Columns

| **Column Name** | **Description** | **Example Value** |
| :--------------- | :--------------------------------- | :-------- |
| Ticker | Company stock symbol | AAPL |
| Market Cap | Total company market cap | $2.5 Trillion |
| PE Ratio | Price-to-Earnings ratio | 15.6 |
| Dividend Yield | Annual dividend yield percentage | 2.0% |

### Key Metrics:
  - Valuation Ratios: Includes PE, PB, and Price-to-Sales ratios for quick value assessment.
  - Profit Margins: Shows operating and net profit margins, essential for profitability analysis.
  - Growth Rates: Displays revenue and earnings growth over 1, 3, and 5-year periods.
  - Ownership & Institutional Holdings: Useful for understanding market sentiment.

### Example Dashboards:
For easy visual analysis, export the generated Excel files into visualization tools. Use Looker Studio or Power BI to create:
  - Comparison Charts: Assess growth rates across multiple stocks.
  - Sector Performance: Visualize metrics by industry.
  - Dividend Analysis: Focus on high dividend yields and income potential.

## 💡 Example Use Cases
  - 📈 Long-Term Investing: Use Graham and Lynch-inspired scripts to identify undervalued, growth-oriented stocks for long holds.
  - 📉 Contrarian Strategy: Leverage scripts that identify underperforming stocks with turnaround potential.
  - 📊 Sector Analysis: Use dashboards to compare sectors or analyze trends within an industry.

## 📜 License
This project is licensed under the MIT License, allowing you to use, modify, and distribute it freely under specified terms. For more details, see the [LICENSE](LICENSE.md) file.

## 🤝 Contributing
Contributions are welcome! If you’d like to improve the project, please fork the repository, make changes, and submit a pull request. Feel free to open issues for bug reports or feature requests.

## 🙏 Acknowledgments
Special thanks to contributors and open-source libraries that make this project possible.
