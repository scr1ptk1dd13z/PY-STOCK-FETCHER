import pandas as pd
import openpyxl
from openpyxl.styles import Font, Alignment
from openpyxl.utils import get_column_letter
from openpyxl.formatting.rule import ColorScaleRule
from google.colab import files
from datetime import datetime

# Step 1: Upload the file
uploaded = files.upload()

# Step 2: Read the uploaded CSV into a DataFrame
file_name = next(iter(uploaded))
df = pd.read_csv(file_name, encoding='ISO-8859-1')

# Step 3: Convert Ex-Dividend Date to readable date if in Unix timestamp format
def convert_to_date(value):
    try:
        if isinstance(value, (int, float)) and len(str(int(value))) >= 10:  # Check if Unix timestamp
            return datetime.utcfromtimestamp(value).strftime('%Y-%m-%d')
    except:
        pass
    return value

df['Ex-Dividend Date'] = df['Ex-Dividend Date'].apply(convert_to_date)

# Step 4: Group by sector and industry, sorting within each group by 1-Year Return
df = df.sort_values(by='1-Year Return', ascending=False)
sector_industry_groups = df.groupby(['Sector', 'Industry'])

# Step 5: Create an Excel writer in the current directory
output_file = 'sector_industry_performance_report_styled.xlsx'
with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
    # Create a sheet for each sector-industry group
    for (sector, industry), group_data in sector_industry_groups:
        # Remove any existing index and write data to the sheet
        group_data = group_data.reset_index(drop=True)
        sheet_name = f"{sector[:20]}_{industry[:20]}"  # Limit sheet name to 31 chars
        group_data.to_excel(writer, sheet_name=sheet_name, index=False)

        # Access the worksheet for additional styling
        worksheet = writer.sheets[sheet_name]
        
        # Freeze the first two columns (A and B)
        worksheet.freeze_panes = "C1"  # This freezes columns A and B, and the header row

        # Add Yahoo Finance hyperlinks to the Symbol (ticker) column
        for row in range(2, len(group_data) + 2):  # Start from row 2 to skip header
            ticker = worksheet[f"A{row}"].value  # Assumes "Symbol" is in column A
            yahoo_finance_url = f"https://finance.yahoo.com/quote/{ticker}"
            worksheet[f"A{row}"].value = f'=HYPERLINK("{yahoo_finance_url}", "{ticker}")'

        # Step 6: Style each sheet
        for col_idx, col_name in enumerate(group_data.columns, start=1):
            column_letter = get_column_letter(col_idx)

            # Adjust column widths, with a wider width for "Name" column
            if col_name == "Name":
                worksheet.column_dimensions[column_letter].width = 25
            else:
                worksheet.column_dimensions[column_letter].width = 15

            # Apply thousands separator and rounding for specified columns
            if col_name in ["Market Cap", "Free Cash Flow", "Operating Cash Flow", "Total Revenue", 
                            "Enterprise Value", "Total Cash", "Total Debt", "Average Volume", "Regular Market Volume"]:
                for cell in worksheet[column_letter]:
                    cell.number_format = '#,##0'

            # Apply decimal formatting for PE Ratio, Forward PE, Price to Book, and Price to Sales
            if col_name in ["PE Ratio", "Forward PE", "Price to Book", "Price to Sales"]:
                for cell in worksheet[column_letter]:
                    cell.number_format = '0.00'

            # Apply percentage format for columns with percent data
            if col_name in ["Revenue Growth (YoY)", "Profit Margins", "Dividend Yield",
                            "EBITDA Margins", "Gross Margins", "Operating Margins", "Payout Ratio",
                            "Insider Ownership", "Institutional Ownership", "Return on Assets", "Return on Equity"]:
                for cell in worksheet[column_letter]:
                    cell.number_format = '0.00%'

            # Apply conditional formatting with gradient colors for selected percentage columns
            if col_name in ["Revenue Growth (YoY)", "Profit Margins", "1-Year Return",
                            "EBITDA Margins", "Gross Margins", "Operating Margins", "Dividend Yield",
                            "Payout Ratio", "Insider Ownership", "Institutional Ownership", 
                            "Return on Assets", "Return on Equity"]:
                worksheet.conditional_formatting.add(
                    f"{column_letter}2:{column_letter}{len(group_data) + 1}",
                    ColorScaleRule(
                        start_type="num", start_value=-1, start_color="FF6347",  # Red for low values
                        mid_type="num", mid_value=0, mid_color="FFFFFF",        # White for neutral
                        end_type="num", end_value=1, end_color="32CD32"         # Green for high values
                    )
                )

# Step 7: Download the formatted Excel file
files.download(output_file)
