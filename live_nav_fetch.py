"""
Live NAV Fetching Script - Mutual Fund Analytics
==================================================
This script fetches live NAV (Net Asset Value) data from mfapi.in API.
It fetches data for:
1. HDFC Top 100 Direct (125497) - Primary fund
2. SBI Bluechip (119551)
3. ICICI Bluechip (120503)
4. Nippon Large Cap (118632)
5. Axis Bluechip (119092)
6. Kotak Bluechip (120841)

NAV data is saved to CSV files in data/raw/ directory.
"""

import requests
import pandas as pd
import json
from pathlib import Path
from datetime import datetime
import time

# Configuration
BASE_URL = "https://api.mfapi.in/mf"
DATA_RAW_DIR = Path("data/raw")

# Fund schemes to fetch
FUNDS_TO_FETCH = {
    "HDFC Top 100 Direct": "125497",
    "SBI Bluechip": "119551",
    "ICICI Bluechip": "120503",
    "Nippon Large Cap": "118632",
    "Axis Bluechip": "119092",
    "Kotak Bluechip": "120841",
}

# Create directories if they don't exist
DATA_RAW_DIR.mkdir(parents=True, exist_ok=True)


def fetch_nav_data(scheme_code, fund_name):
    """
    Fetch NAV data from mfapi.in for a specific scheme.
    
    Parameters:
    -----------
    scheme_code : str
        AMFI scheme code
    fund_name : str
        Fund name for display
        
    Returns:
    --------
    dict or None
        JSON response with fund data, or None if request failed
    """
    try:
        url = f"{BASE_URL}/{scheme_code}"
        print(f"\n🔄 Fetching {fund_name} ({scheme_code})...")
        print(f"   URL: {url}")
        
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        print(f"✅ Successfully fetched {fund_name}")
        print(f"   Status: {response.status_code}")
        print(f"   NAV records: {len(data.get('data', []))}")
        
        return data
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Error fetching {fund_name}: {str(e)}")
        return None
    except json.JSONDecodeError as e:
        print(f"❌ Error parsing JSON for {fund_name}: {str(e)}")
        return None


def parse_nav_json_to_dataframe(json_data, fund_name, scheme_code):
    """
    Parse JSON response from mfapi.in and convert to DataFrame.
    
    Parameters:
    -----------
    json_data : dict
        JSON response from API
    fund_name : str
        Name of the fund
    scheme_code : str
        AMFI scheme code
        
    Returns:
    --------
    pd.DataFrame or None
        DataFrame with NAV data, or None if parsing failed
    """
    try:
        if not json_data or 'data' not in json_data:
            print(f"❌ Invalid JSON structure for {fund_name}")
            return None
        
        nav_records = json_data.get('data', [])
        
        if not nav_records:
            print(f"⚠️ No NAV records found for {fund_name}")
            return None
        
        # Parse NAV records
        records = []
        for record in nav_records:
            if isinstance(record, dict):
                records.append({
                    'date': record.get('date'),
                    'nav': record.get('nav'),
                })
            else:
                # Handle if records are lists [date, nav]
                if len(record) >= 2:
                    records.append({
                        'date': record[0],
                        'nav': record[1],
                    })
        
        if not records:
            print(f"⚠️ Could not parse NAV records for {fund_name}")
            return None
        
        df = pd.DataFrame(records)
        
        # Add metadata columns
        df['fund_name'] = fund_name
        df['scheme_code'] = scheme_code
        df['fetch_date'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # Convert nav to numeric
        df['nav'] = pd.to_numeric(df['nav'], errors='coerce')
        
        # Convert date to datetime
        df['date'] = pd.to_datetime(df['date'], errors='coerce')
        
        # Reorder columns
        df = df[['scheme_code', 'fund_name', 'date', 'nav', 'fetch_date']]
        
        print(f"   ✓ Parsed {len(df)} NAV records")
        print(f"   ✓ Date range: {df['date'].min()} to {df['date'].max()}")
        print(f"   ✓ NAV range: {df['nav'].min():.2f} to {df['nav'].max():.2f}")
        
        return df
        
    except Exception as e:
        print(f"❌ Error parsing {fund_name} data: {str(e)}")
        return None


def save_nav_to_csv(df, scheme_code, fund_name):
    """
    Save NAV DataFrame to CSV file.
    
    Parameters:
    -----------
    df : pd.DataFrame
        NAV data
    scheme_code : str
        AMFI scheme code
    fund_name : str
        Fund name
        
    Returns:
    --------
    str or None
        Path to saved file, or None if failed
    """
    try:
        # Create filename
        filename = f"nav_{scheme_code}_{fund_name.replace(' ', '_').lower()}.csv"
        file_path = DATA_RAW_DIR / filename
        
        # Save to CSV
        df.to_csv(file_path, index=False)
        print(f"💾 Saved to: {file_path}")
        
        return str(file_path)
        
    except Exception as e:
        print(f"❌ Error saving CSV for {fund_name}: {str(e)}")
        return None


def create_live_nav_summary(dataframes_dict):
    """
    Create a summary CSV with latest NAV for all funds.
    
    Parameters:
    -----------
    dataframes_dict : dict
        Dictionary of fund_name: dataframe
        
    Returns:
    --------
    pd.DataFrame
        Summary dataframe
    """
    summary_records = []
    
    for fund_name, df in dataframes_dict.items():
        if df is None or df.empty:
            continue
        
        latest = df.iloc[0]  # First row should be latest (usually sorted by date desc)
        
        summary_records.append({
            'fund_name': fund_name,
            'scheme_code': latest.get('scheme_code'),
            'latest_nav': latest.get('nav'),
            'latest_date': latest.get('date'),
            'fetch_timestamp': latest.get('fetch_date'),
        })
    
    if not summary_records:
        print("❌ No data to create summary")
        return None
    
    summary_df = pd.DataFrame(summary_records)
    
    # Save summary
    summary_file = DATA_RAW_DIR / "nav_live_summary.csv"
    summary_df.to_csv(summary_file, index=False)
    
    return summary_df


def main():
    """Main execution function."""
    print("\n" + "="*80)
    print("🚀 LIVE NAV FETCHING - MUTUAL FUND ANALYTICS")
    print("="*80)
    print(f"API Base URL: {BASE_URL}")
    print(f"Data directory: {DATA_RAW_DIR.absolute()}\n")
    
    all_dataframes = {}
    successful_fetches = 0
    failed_fetches = 0
    
    # Fetch data for each fund
    for fund_name, scheme_code in FUNDS_TO_FETCH.items():
        print(f"\n{'-'*80}")
        print(f"Fund: {fund_name}")
        print(f"{'-'*80}")
        
        # Fetch JSON data
        json_data = fetch_nav_data(scheme_code, fund_name)
        
        if json_data is None:
            print(f"⏭️  Skipping {fund_name} due to fetch error")
            failed_fetches += 1
            all_dataframes[fund_name] = None
            continue
        
        # Parse to DataFrame
        df = parse_nav_json_to_dataframe(json_data, fund_name, scheme_code)
        
        if df is None:
            print(f"⏭️  Skipping {fund_name} due to parsing error")
            failed_fetches += 1
            all_dataframes[fund_name] = None
            continue
        
        # Save to CSV
        saved_path = save_nav_to_csv(df, scheme_code, fund_name)
        
        if saved_path:
            all_dataframes[fund_name] = df
            successful_fetches += 1
        else:
            failed_fetches += 1
            all_dataframes[fund_name] = None
        
        # Rate limiting - be respectful to the API
        time.sleep(1)
    
    # Create summary
    print(f"\n{'='*80}")
    print("📊 CREATING SUMMARY")
    print(f"{'='*80}")
    
    summary_df = create_live_nav_summary(all_dataframes)
    
    if summary_df is not None:
        print("\n📋 Live NAV Summary:")
        print(summary_df.to_string(index=False))
    
    # Final report
    print(f"\n{'='*80}")
    print("✨ FETCH COMPLETE")
    print(f"{'='*80}")
    print(f"✅ Successful: {successful_fetches}/{len(FUNDS_TO_FETCH)}")
    print(f"❌ Failed: {failed_fetches}/{len(FUNDS_TO_FETCH)}")
    print(f"\n📁 Data saved to: {DATA_RAW_DIR.absolute()}")
    print(f"{'='*80}\n")
    
    return all_dataframes


def test_api_connection():
    """Test API connection with a simple request."""
    print("\n🔍 Testing API connection...")
    try:
        response = requests.get(f"{BASE_URL}/125497", timeout=5)
        if response.status_code == 200:
            print("✅ API connection successful!")
            return True
        else:
            print(f"⚠️ API returned status {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ API connection failed: {str(e)}")
        return False


if __name__ == "__main__":
    # Test API first
    if not test_api_connection():
        print("\n⚠️ Cannot proceed without API connection")
        exit(1)
    
    # Fetch data
    dataframes = main()
