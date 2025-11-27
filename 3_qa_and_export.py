import pandas as pd
import os

INPUT_FILE = 'data/raw_financials_data.csv'
OUTPUT_FILE = 'data/final_submission_financials.csv'

def quality_assurance():
    """
    Cleans invalid entries (Revenue <= 0),
    Verifies project requirements (100-500),
    Exports dataset for submission.
    """
    if not os.path.exists(INPUT_FILE):
        print(f"Error: {INPUT_FILE} missing. Please run 2_extract_financials.py first.")
        return

    df = pd.read_csv(INPUT_FILE)
    original_count = len(df)
    
    # 1. CLEANING
    df = df[df['Total Revenue'] > 0]
    cleaned_count = len(df)
    print(f"Dropped {original_count - cleaned_count} rows with missing/zero revenue.")

    # 2. CHECK CONSTRAINT
    unique_companies = df['Symbol'].nunique()
    print(f"Unique Companies Extracted: {unique_companies}")
    
    if unique_companies < 100:
        print("Fewer than 100 companies.")
    elif unique_companies > 500:
        print("More than 500 companies.")
        
    # 3. Sorting, just ensuring
    df = df.sort_values(by=['Company Name', 'Year'], ascending=[True, False])

    # 4. FINAL EXPORT
    df.to_csv(OUTPUT_FILE, index=False)
    print(f"\nSUCCESS Final dataset saved to {OUTPUT_FILE}")
    print(f"Total Rows: {len(df)}")
    print("-" * 30)
    print("Top 5 Rows of Final Submission:")
    print(df.head())

if __name__ == "__main__":
    quality_assurance()