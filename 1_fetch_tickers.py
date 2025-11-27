import pandas as pd
import requests
import io
import os

def get_sp500_tickers(limit=200):
    """
    Scrapes S&P 500 tickers by searching for the correct table dynamically.
    """
    url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    } # Mimic a real browser request
    
    print(f"Downloading data from {url}...")
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        tables = pd.read_html(io.StringIO(response.text))
        print(f"Found {len(tables)} tables on the page. Searching for the ticker table...")

        target_df = None
        
        # LOOP through all tables to find the right one
        for i, table in enumerate(tables):
            cols = [str(c).replace(' ', '_') for c in table.columns]
            
            if 'Symbol' in cols and 'Security' in cols:
                print(f" -> Table {i} looks correct! It has 'Symbol' and 'Security'.")
                target_df = table
                target_df.columns = cols
                break
        
        if target_df is None:
            raise ValueError("Could not locate the S&P 500 table among the page elements.")

        # Formatting:  '.' (BRK.B) to '-' (BRK-B)
        target_df['Symbol'] = target_df['Symbol'].str.replace('.', '-', regex=False)
        
        subset_df = target_df.head(limit)
        
        print(f"Successfully extracted {len(subset_df)} tickers.")
        return subset_df
        
    except Exception as e:
        print(e)
        return pd.DataFrame()

if __name__ == "__main__":
    if not os.path.exists('data'):
        os.makedirs('data')
        
    df_tickers = get_sp500_tickers(limit=200)
    
    if not df_tickers.empty:
        output_path = 'data/sp500_tickers.csv'
        df_tickers.to_csv(output_path, index=False)
        print(f"SUCCESS saved to {output_path}")
    else:
        print("FAILURE")