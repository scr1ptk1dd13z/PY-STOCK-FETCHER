# Stock Data Fetcher

This project is designed to be run in Google Colab, providing a simple and efficient way to fetch detailed stock data for U.S. and Canadian companies. By utilizing the yfinance library, it collects various financial metrics and insights, helping users analyze stocks and make informed investment decisions.

The script fetches data for a customizable list of tickers, retrieves relevant financial information, and exports it to both CSV and Excel formats for easy analysis.

| Column Header                     | Column Letter | Description                                                  | Data Type        | Calculation/Unit                      |
|-----------------------------------|---------------|--------------------------------------------------------------|------------------|---------------------------------------|
| Symbol                            | A             | Ticker symbol for the stock                                 | String           | -                                     |
| Name                              | B             | Full name of the company                                    | String           | -                                     |
| Sector                            | C             | Sector the company operates in                              | String           | -                                     |
| Industry                          | D             | Industry category                                          | String           | -                                     |
| Country                           | E             | Country of the company's headquarters                       | String           | -                                     |
| Currency                          | F             | Currency used for financial data                           | String           | -                                     |
| Exchange                          | G             | Stock exchange where the company is listed                 | String           | -                                     |
| Website                           | H             | Company's official website                                  | String           | -                                     |
| Current Price                     | I             | Current trading price of the stock                          | Number (float)   | -                                     |
| Market Cap                        | J             | Total market capitalization                                 | Currency         | -                                     |
| Enterprise Value                  | K             | Total value of the company, including debt                  | Currency         | -                                     |
| PE Ratio                          | L             | Price-to-Earnings ratio                                     | Number (float)   | Current Price / Earnings per Share   |
| Forward PE                        | M             | Projected Price-to-Earnings ratio                           | Number (float)   | Current Price / Projected Earnings per Share |
| PEG Ratio                         | N             | Price/Earnings to Growth ratio                               | Number (float)   | PE Ratio / Earnings Growth Rate       |
| Price to Book                     | O             | Price-to-Book ratio                                        | Number (float)   | Current Price / Book Value per Share |
| Price to Sales                    | P             | Price-to-Sales ratio                                        | Number (float)   | Current Price / Revenue per Share    |
| Book Value per Share              | Q             | Book value of the company divided by outstanding shares    | Currency         | -                                     |
| Revenue per Share                 | R             | Revenue divided by outstanding shares                       | Currency         | -                                     |
| Revenue Growth (YoY)             | S             | Year-over-Year revenue growth percentage                     | Percentage       | ((Current Revenue - Previous Revenue) / Previous Revenue) * 100 |
| Earnings Growth (YoY)             | T             | Year-over-Year earnings growth percentage                    | Percentage       | ((Current Earnings - Previous Earnings) / Previous Earnings) * 100 |
| EBITDA Margins                    | U             | EBITDA as a percentage of revenue                           | Percentage       | (EBITDA / Revenue) * 100             |
| Gross Margins                     | V             | Gross profit as a percentage of revenue                    | Percentage       | (Gross Profit / Revenue) * 100       |
| Operating Margins                 | W             | Operating income as a percentage of revenue                 | Percentage       | (Operating Income / Revenue) * 100   |
| Profit Margins                    | X             | Net income as a percentage of revenue                       | Percentage       | (Net Income / Revenue) * 100         |
| Dividend Rate                     | Y             | Annual dividend paid per share                              | Currency         | -                                     |
| Dividend Yield                    | Z             | Dividend as a percentage of current price                  | Percentage       | (Dividend Rate / Current Price) * 100|
| Payout Ratio                      | AA            | Percentage of earnings paid out as dividends                | Percentage       | (Dividend Rate / Earnings per Share) * 100 |
| Five-Year Avg. Dividend Yield     | AB            | Average dividend yield over the last five years            | Percentage       | -                                     |
| Ex-Dividend Date                  | AC            | Date on which the stock begins trading without the next dividend | Date          | -                                     |
| Free Cash Flow                    | AD            | Cash generated after capital expenditures                    | Currency         | Operating Cash Flow - Capital Expenditures |
| Operating Cash Flow                | AE            | Cash generated from operations                               | Currency         | -                                     |
| Total Cash                        | AF            | Total cash and cash equivalents on the balance sheet        | Currency         | -                                     |
| Cash per Share                    | AG            | Cash available for each outstanding share                   | Currency         | Total Cash / Shares Outstanding       |
| Total Debt                        | AH            | Total debt of the company                                   | Currency         | -                                     |
| Net Debt                          | AI            | Total debt minus cash and cash equivalents                   | Currency         | Total Debt - Total Cash              |
| Debt to Equity                    | AJ            | Ratio of total debt to shareholder's equity                 | Number (float)   | Total Debt / Total Equity             |
| Current Ratio                     | AK            | Current assets divided by current liabilities                | Number (float)   | Current Assets / Current Liabilities   |
| Quick Ratio                       | AL            | (Current Assets - Inventory) / Current Liabilities         | Number (float)   | (Current Assets - Inventory) / Current Liabilities |
| Beta                              | AM            | Measure of stock volatility relative to the market         | Number (float)   | -                                     |
| 52-Week High                      | AN            | Highest trading price in the last 52 weeks                 | Currency         | -                                     |
| 52-Week Low                       | AO            | Lowest trading price in the last 52 weeks                  | Currency         | -                                     |
| Average Volume                    | AP            | Average trading volume over a specific period              | Number           | -                                     |
| Regular Market Volume             | AQ            | Trading volume during the most recent market session        | Number           | -                                     |
| Current Price Change (%)          | AR            | Percentage change in current price from the previous close  | Percentage       | ((Current Price - Previous Close) / Previous Close) * 100 |
| 1-Year Return                     | AS            | Return on investment over the past year                     | Percentage       | ((Current Price - Price One Year Ago) / Price One Year Ago) * 100 |
| Insider Ownership                  | AT            | Percentage of shares owned by company insiders              | Percentage       | -                                     |
| Institutional Ownership            | AU            | Percentage of shares owned by institutions                  | Percentage       | -                                     |
| Short Ratio                       | AV            | Number of shares sold short compared to shares outstanding  | Number (float)   | -                                     |
| Target High Price                 | AW            | Highest target price set by analysts                        | Currency         | -                                     |
| Target Low Price                  | AX            | Lowest target price set by analysts                         | Currency         | -                                     |
| Target Mean Price                 | AY            | Average target price set by analysts                        | Currency         | -                                     |
| Recommendation Mean               | AZ            | Average recommendation from analysts (e.g., Buy, Hold)     | String           | -                                     |
| Number of Analyst Opinions        | BA            | Number of analysts providing recommendations                | Number           | -                                     |

---
