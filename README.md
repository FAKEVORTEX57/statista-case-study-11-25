# S&P 500 Financial Data Extraction Pipeline

## Overview
This project is a data engineering case study submission. It automates the extraction of financial data for S&P 500 companies using Python. 

The pipeline identifies public companies, extracts their last 3 years of financial reports (Revenue, Net Income, Gross Profit, Operating Income, Pretax Income) via the Yahoo Finance API, and transforms the data into a structured CSV format.

## Project Structure
* `1_fetch_tickers.py`: Scrapes and cleans the list of S&P 500 companies from Wikipedia.
* `2_extract_financials.py`: Queries the Yahoo Finance API for historical data.
* `3_qa_and_export.py`: Performs quality checks (null handling, row counts) and exports the final dataset.
* `data/`: Contains the intermediate and final CSV outputs.

## Requirements
* Python 3.8+
* pandas
* yfinance
* requests
* lxml

## How to Run
1. Install dependencies:
   ```bash
   pip install pandas yfinance requests lxml
   ```
2. Run the pipeline steps in order:
   ```bash
   python 1_fetch_tickers.py
   python 2_extract_financials.py
   python 3_qa_and_export.py
   ```
3. The final output will be available at `data/final_submission_financials.csv`.

## Data Dictionary
| Column           | Description                                       |
| -------------    | -----------------------------------------------   |
| Symbol           | Stock ticker symbol (e.g., MMM)                   |
| Company Name     | Full legal name of the company                    |
| Country          | Headquarters location                             |
| Industry         | Industry classification                           |
| Year             | Fiscal year of the financial report               |
| Total Revenue    | Revenue figure                                    |
| Net Income       | (Optional KPI) Net profit or loss                 |
| Gross Profit     | (Optional KPI) Revenue minus cost of goods sold   |
| Operating Income | (Optional KPI) Profit from business operations    |
| Pretax Income    | (Optional KPI) Income before tax deduction        |
