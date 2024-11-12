# Stock Data Fetching Script

This script fetches detailed stock information for the top US and Canadian companies, including S&P 500 and TSX Composite tickers. It collects data such as company fundamentals, financial ratios, and price metrics, then saves the data in CSV and Excel formats. The script is designed to be used in Google Colab for seamless data processing and easy file management.

## Features
- Fetches stock data for up to 11,500 companies from the S&P 500 and TSX Composite indices.
- Collects detailed financial information, including valuation ratios, margins, growth rates, ownership metrics, and stock performance data.
- Handles retries when fetching data to ensure resilience against temporary issues.
- Saves output data in both CSV and Excel formats for easy analysis.
- Supports auto-download of the CSV file in Google Colab.

## Data Columns

| Column Name                        | Description                                             | Data Type       | Calculation Type          | Column in Sheet |
|------------------------------------|---------------------------------------------------------|-----------------|---------------------------|----------------|
| Symbol                             | Ticker symbol of the company                             | Text            | -                         | A              |
| Name                               | Full name of the company                                 | Text            | -                         | B              |
| Sector                             | Economic sector                                          | Text            | -                         | C              |
| Industry                           | Specific industry within the sector                      | Text            | -                         | D              |
| Country                            | Company's country of operation                           | Text            | -                         | E              |
| Currency                           | Currency for the stock prices                            | Text            | -                         | F              |
| Exchange                           | Stock exchange where the company is listed               | Text            | -                         | G              |
| Website                            | Company's official website                               | Text            | -                         | H              |
| Current Price                      | Current stock price                                      | Currency        | -                         | I              |
| Market Cap                         | Market capitalization                                    | Currency        | Sum                       | J              |
| Enterprise Value                   | Total value considering debt                             | Currency        | Sum                       | K              |
| PE Ratio                           | Price-to-earnings ratio                                  | Number          | Average                   | L              |
| Forward PE                         | Estimated price-to-earnings for the next year            | Number          | Average                   | M              |
| PEG Ratio                          | Price/earnings to growth ratio                           | Number          | Average                   | N              |
| Price to Book                      | Price relative to book value per share                   | Number          | Average                   | O              |
| Price to Sales                     | Price relative to sales per share                        | Number          | Average                   | P              |
| Book Value per Share               | Value of net assets divided by shares outstanding        | Currency        | -                         | Q              |
| Revenue per Share                  | Revenue divided by shares outstanding                    | Currency        | -                         | R              |
| Revenue Growth (YoY)               | Year-over-year revenue growth                            | Percentage      | -                         | S              |
| Earnings Growth (YoY)              | Year-over-year earnings growth                           | Percentage      | -                         | T              |
| EBITDA Margins                     | EBITDA as a percentage of revenue                        | Percentage      | -                         | U              |
| Gross Margins                      | Gross profit as a percentage of revenue                  | Percentage      | -                         | V              |
| Operating Margins                  | Operating profit as a percentage of revenue              | Percentage      | -                         | W              |
| Profit Margins                     | Net profit as a percentage of revenue                    | Percentage      | -                         | X              |
| Dividend Rate                      | Annual dividend payout                                   | Currency        | -                         | Y              |
| Dividend Yield                     | Dividend as a percentage of current price                | Percentage      | -                         | Z              |
| Payout Ratio                       | Proportion of earnings paid as dividends                 | Percentage      | -                         | AA             |
| Five-Year Avg. Dividend Yield      | Average dividend yield over the past five years          | Percentage      | -                         | AB             |
| Ex-Dividend Date                   | Date when the next dividend will be paid                 | Date            | -                         | AC             |
| Free Cash Flow                     | Cash available after capital expenditures                | Currency        | Sum                       | AD             |
| Operating Cash Flow                | Cash generated from operations                           | Currency        | Sum                       | AE             |
| Total Cash                         | Total cash reserves                                      | Currency        | Sum                       | AF             |
| Cash per Share                     | Cash reserves divided by shares outstanding              | Currency        | -                         | AG             |
| Total Debt                         | Sum of short and long-term debt                          | Currency        | Sum                       | AH             |
| Net Debt                           | Total debt minus cash reserves                           | Currency        | Sum                       | AI             |
| Debt to Equity                     | Ratio of debt to shareholders' equity                    | Number          | Average                   | AJ             |
| Current Ratio                      | Current assets divided by current liabilities            | Number          | Average                   | AK             |
| Quick Ratio                        | (Current assets - inventories) divided by liabilities    | Number          | Average                   | AL             |
| Beta                               | Measure of stock volatility relative to the market       | Number          | Average                   | AM             |
| 52-Week High                       | Highest price in the last 52 weeks                       | Currency        | Max                       | AN             |
| 52-Week Low                        | Lowest price in the last 52 weeks                        | Currency        | Min                       | AO             |
| Average Volume                     | Average trading volume over a given period               | Number          | Average                   | AP             |
| Regular Market Volume              | Volume of shares traded in the current session           | Number          | -                         | AQ             |
| Current Price Change (%)           | Percentage change in the current price                   | Percentage      | -                         | AR             |
| 1-Year Return                      | Total return over the past year                          | Percentage      | -                         | AS             |
| Insider Ownership                  | Percentage of shares held by insiders                    | Percentage      | -                         | AT             |
| Institutional Ownership            | Percentage of shares held by institutions                | Percentage      | -                         | AU             |
| Short Ratio                        | Ratio of shares sold short to average trading volume     | Number          | Average                   | AV             |
| Target High Price                  | Highest analyst target price                             | Currency        | Max                       | AW             |
| Target Low Price                   | Lowest analyst target price                              | Currency        | Min                       | AX             |
| Target Mean Price                  | Average analyst target price                             | Currency        | Average                   | AY             |
| Recommendation Mean                | Average analyst recommendation (1=Strong Buy, 5=Sell)    | Number          | Average                   | AZ             |
| Number of Analyst Opinions         | Number of analysts providing recommendations             | Number          | Sum                       | BA             |

## Getting Started

To use this script, open the provided Google Colab notebook, execute the cells, and download the generated CSV or Excel file containing the fetched stock data.

