# Stock Data Fetcher

This project is designed to be run in Google Colab, providing a simple and efficient way to fetch detailed stock data for U.S. and Canadian companies. By utilizing the yfinance library, it collects various financial metrics and insights, helping users analyze stocks and make informed investment decisions.

The script fetches data for a customizable list of tickers, retrieves relevant financial information, and exports it to both CSV and Excel formats for easy analysis.

| Column | Data Field                        | Description                                                                                                                   |
|--------|-----------------------------------|-------------------------------------------------------------------------------------------------------------------------------|
| A      | **Symbol**                        | The stock's ticker symbol (e.g., AAPL for Apple).                                                                           |
| B      | **Name**                          | The full name of the company.                                                                                               |
| C      | **Sector**                        | The broad category the company belongs to (e.g., Technology, Healthcare).                                                  |
| D      | **Industry**                      | A more specific classification within the sector (e.g., Software, Pharmaceuticals).                                        |
| E      | **Country**                       | The country where the company is based.                                                                                     |
| F      | **Currency**                      | The currency used for the stock (e.g., USD for U.S. dollars).                                                               |
| G      | **Exchange**                      | The stock exchange where the stock is traded (e.g., NYSE, NASDAQ).                                                         |
| H      | **Website**                       | The company’s official website.                                                                                             |
| I      | **Current Price**                 | The current trading price of the stock.                                                                                     |
| J      | **Market Cap**                   | The total market value of the company's outstanding shares, calculated as the price per share multiplied by the number of shares. |
| K      | **Enterprise Value**             | A measure of a company's total value, including market cap and debt, minus cash.                                           |
| L      | **PE Ratio**                     | The price-to-earnings ratio, indicating how much investors are willing to pay per dollar of earnings.                       |
| M      | **Forward PE**                   | The PE ratio based on forecasted earnings for the next year.                                                                |
| N      | **PEG Ratio**                    | The PE ratio divided by the company's growth rate, helping assess valuation relative to growth prospects.                    |
| O      | **Price to Book**                | The ratio of the stock's current price to its book value.                                                                    |
| P      | **Price to Sales**               | The ratio of the stock’s price to its revenue per share.                                                                    |
| Q      | **Book Value per Share**         | The net asset value of a company divided by the number of outstanding shares.                                                |
| R      | **Revenue per Share**            | The total revenue divided by the number of shares outstanding.                                                               |
| S      | **Revenue Growth (YoY)**         | The percentage increase in revenue compared to the previous year.                                                           |
| T      | **Earnings Growth (YoY)**        | The percentage increase in earnings compared to the previous year.                                                          |
| U      | **EBITDA Margins**               | Earnings before interest, taxes, depreciation, and amortization as a percentage of revenue.                                 |
| V      | **Gross Margins**                | The percentage of revenue that exceeds the cost of goods sold (COGS).                                                       |
| W      | **Operating Margins**            | The percentage of revenue left after paying for variable costs of production.                                               |
| X      | **Profit Margins**               | The percentage of revenue that remains as profit after all expenses are paid.                                               |
| Y      | **Dividend Rate**                | The amount of money paid to shareholders per share over a year.                                                              |
| Z      | **Dividend Yield**               | The annual dividend payment divided by the stock’s current price, expressed as a percentage.                                 |
| AA     | **Payout Ratio**                 | The percentage of earnings paid to shareholders in dividends.                                                                 |
| AB     | **Five-Year Avg. Dividend Yield**| The average dividend yield over the past five years.                                                                         |
| AC     | **Ex-Dividend Date**             | The date on which a stock begins trading without the right to receive the next dividend.                                     |
| AD     | **Free Cash Flow**               | Cash generated by the company that can be distributed to investors.                                                          |
| AE     | **Operating Cash Flow**          | Cash generated from the company's normal business operations.                                                                |
| AF     | **Total Cash**                   | The total amount of cash available to the company.                                                                          |
| AG     | **Cash per Share**               | The total cash divided by the number of shares outstanding.                                                                  |
| AH     | **Total Debt**                   | The total amount of debt the company has.                                                                                    |
| AI     | **Net Debt**                     | Total debt minus total cash.                                                                                                |
| AJ     | **Debt to Equity**               | The ratio of total debt to shareholders' equity.                                                                            |
| AK     | **Current Ratio**                | A measure of liquidity, indicating the company's ability to meet short-term obligations.                                     |
| AL     | **Quick Ratio**                  | A more stringent measure of liquidity that excludes inventory.                                                                |
| AM     | **Beta**                         | A measure of a stock's volatility in relation to the market.                                                                  |
| AN     | **52-Week High**                 | The highest price the stock has traded at over the last 52 weeks.                                                          |
| AO     | **52-Week Low**                  | The lowest price the stock has traded at over the last 52 weeks.                                                           |
| AP     | **Average Volume**               | The average number of shares traded daily over a specific period.                                                            |
| AQ     | **Regular Market Volume**        | The number of shares traded on a specific day.                                                                              |
| AR     | **Current Price Change (%)**     | The percentage change in the stock price from the previous close.                                                           |
| AS     | **1-Year Return**                | The total return of the stock over the last year, including price appreciation and dividends.                               |
| AT     | **Insider Ownership**            | The percentage of shares owned by company executives and insiders.                                                           |
| AU     | **Institutional Ownership**      | The percentage of shares owned by institutional investors.                                                                   |
| AV     | **Short Ratio**                  | The ratio of shares shorted compared to the average daily volume.                                                           |
| AW     | **Target High Price**            | The highest price target set by analysts for the stock.                                                                      |
| AX     | **Target Low Price**             | The lowest price target set by analysts for the stock.                                                                       |
| AY     | **Target Mean Price**            | The average price target set by analysts for the stock.                                                                     |
| AZ     | **Recommendation Mean**          | The average analyst rating (e.g., buy, hold, sell) for the stock.                                                            |
| BA     | **Number of Analyst Opinions**   | The number of analysts providing ratings and price targets for the stock.                                                    |

---
