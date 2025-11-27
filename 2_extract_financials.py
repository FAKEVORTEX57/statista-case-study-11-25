import pandas as pd
import yfinance as yf
import time
import os

INPUT_FILE = 'data/sp500_tickers.csv'
OUTPUT_FILE = 'data/raw_financials_data.csv'
TEST_LIMIT = None  

def extract_financials():
    """
    Reads the ticker list and fetches financial data from Yahoo Finance.
    Returns a list of dictionaries (one per year per company).
    """
    if not os.path.exists(INPUT_FILE):
        print(f"Error: {INPUT_FILE} not found. Please run 1_fetch_tickers.py first.")
        return

    df_tickers = pd.read_csv(INPUT_FILE)
    symbols = df_tickers['Symbol'].tolist()
    
    if TEST_LIMIT:
        print(f"--- TEST MODE: Processing only first {TEST_LIMIT} companies ---")
        symbols = symbols[:TEST_LIMIT]

    all_data = []
    
    print(f"Starting extraction for {len(symbols)} companies...")

    for i, ticker_symbol in enumerate(symbols):
        print(f"[{i+1}/{len(symbols)}] Processing {ticker_symbol}...")
        
        try:
            stock = yf.Ticker(ticker_symbol)
            
            # A. Metadata or Info
            info = stock.info
            country = info.get('country', 'Unknown')
            industry = info.get('industry', 'Unknown')
            currency = info.get('currency', 'USD')
            company_name = info.get('longName', ticker_symbol)
            
            # B. Income Statement
            financials = stock.financials
            # print(financials)

            if financials.empty:
                print(f"   Warning: No financial data found for {ticker_symbol}")
                continue

            # C. ERevenue + Optional KPIs
            target_rows = ['Total Revenue', 'Net Income', 'Gross Profit']
            
            available_rows = [r for r in target_rows if r in financials.index]
            df_subset = financials.loc[available_rows]
            # print(df_subset)
            
            # D. Columns are dates
            recent_years = df_subset.columns[:3]
            
            # E. One record per Year
            for date_col in recent_years:
                year_str = str(date_col.year)
                
                # Structure
                record = {
                    'Symbol': ticker_symbol,
                    'Company Name': company_name,
                    'Country': country,
                    'Industry': industry,
                    'Year': year_str,
                    'Currency': currency
                }
                
                # Financial Metrics
                for row_name in available_rows:
                    val = df_subset.loc[row_name, date_col]
                    record[row_name] = val
                
                all_data.append(record)
                
        except Exception as e:
            print(f"   Error fetching {ticker_symbol}: {e}")
        
        # Being polite to the server
        time.sleep(0.5)

    # 4. Save Results
    if all_data:
        df_results = pd.DataFrame(all_data)
        df_results.to_csv(OUTPUT_FILE, index=False)
        print(f"\nSUCCESS {len(df_results)} rows of data.")
        print(f"Saved to {OUTPUT_FILE}")
        # print(df_results.head())
    else:
        print("\nFAILURE")

if __name__ == "__main__":
    extract_financials()