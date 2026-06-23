"""
Data Ingestion Script - Mutual Fund Analytics
================================================
This script loads and explores all 10 CSV datasets.
For each dataset, it prints:
- Dataset shape (rows, columns)
- Data types
- First few rows (head)
- Any anomalies detected
"""

import pandas as pd
import numpy as np
import os
import sys
from pathlib import Path

# Configuration
DATA_RAW_DIR = Path("data/raw")
DATA_PROCESSED_DIR = Path("data/processed")

# Create directories if they don't exist
DATA_RAW_DIR.mkdir(parents=True, exist_ok=True)
DATA_PROCESSED_DIR.mkdir(parents=True, exist_ok=True)


def load_and_explore_csv(file_path):
    """
    Load a CSV file and print comprehensive exploration information.
    
    Parameters:
    -----------
    file_path : str or Path
        Path to the CSV file
        
    Returns:
    --------
    pd.DataFrame or None
        DataFrame if successful, None if failed
    """
    try:
        df = pd.read_csv(file_path)
        
        print(f"\n{'='*80}")
        print(f"📊 Dataset: {file_path.name}")
        print(f"{'='*80}")
        
        # Shape information
        print(f"\n📏 Shape: {df.shape[0]} rows × {df.shape[1]} columns")
        
        # Data types
        print(f"\n📋 Data Types:")
        print(df.dtypes)
        
        # First few rows
        print(f"\n🔝 First 5 rows:")
        print(df.head())
        
        # Statistical summary
        print(f"\n📈 Statistical Summary:")
        print(df.describe(include='all'))
        
        # Missing values
        print(f"\n❌ Missing Values:")
        missing_count = df.isnull().sum()
        if missing_count.sum() > 0:
            print(missing_count[missing_count > 0])
        else:
            print("No missing values detected!")
        
        # Detect anomalies
        print(f"\n⚠️ Anomalies Detected:")
        anomalies = detect_anomalies(df)
        if anomalies:
            for anomaly in anomalies:
                print(f"  - {anomaly}")
        else:
            print("  No major anomalies detected!")
        
        # Duplicate rows
        duplicates = df.duplicated().sum()
        if duplicates > 0:
            print(f"  - {duplicates} duplicate rows found")
        
        return df
        
    except Exception as e:
        print(f"\n❌ Error loading {file_path}: {str(e)}")
        return None


def detect_anomalies(df):
    """
    Detect common data quality anomalies.
    
    Parameters:
    -----------
    df : pd.DataFrame
        DataFrame to analyze
        
    Returns:
    --------
    list
        List of anomalies found
    """
    anomalies = []
    
    # Check for empty dataframe
    if df.empty:
        anomalies.append("Empty dataframe")
    
    # Check for columns with all null values
    all_null_cols = df.columns[df.isnull().all()].tolist()
    if all_null_cols:
        anomalies.append(f"Columns with all null values: {all_null_cols}")
    
    # Check for potential AMFI code issues
    if 'Scheme Code' in df.columns or 'scheme_code' in df.columns:
        code_col = 'Scheme Code' if 'Scheme Code' in df.columns else 'scheme_code'
        invalid_codes = df[df[code_col].isnull() | (df[code_col] == 0)]
        if len(invalid_codes) > 0:
            anomalies.append(f"Invalid AMFI codes: {len(invalid_codes)} rows with null/zero codes")
    
    # Check for negative values in numeric columns (if they shouldn't be)
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    for col in numeric_cols:
        if (df[col] < 0).any() and 'return' not in col.lower() and 'change' not in col.lower():
            neg_count = (df[col] < 0).sum()
            anomalies.append(f"Column '{col}': {neg_count} negative values (unexpected)")
    
    return anomalies


def main():
    """Main execution function."""
    print("\n" + "="*80)
    print("🚀 MUTUAL FUND ANALYTICS - DATA INGESTION")
    print("="*80)
    print(f"Looking for CSV files in: {DATA_RAW_DIR.absolute()}\n")
    
    # Find all CSV files
    csv_files = list(DATA_RAW_DIR.glob("*.csv"))
    
    if not csv_files:
        print(f"⚠️ No CSV files found in {DATA_RAW_DIR}")
        print("📝 Please add CSV files to the data/raw/ directory")
        return
    
    print(f"Found {len(csv_files)} CSV files:\n")
    for i, file in enumerate(csv_files, 1):
        print(f"  {i}. {file.name}")
    
    # Load and explore each CSV
    dataframes = {}
    for csv_file in sorted(csv_files):
        df = load_and_explore_csv(csv_file)
        if df is not None:
            dataframes[csv_file.stem] = df
    
    # Summary report
    print(f"\n\n{'='*80}")
    print("📊 SUMMARY REPORT")
    print(f"{'='*80}")
    print(f"\nSuccessfully loaded {len(dataframes)} datasets\n")
    
    # Fund Master specific analysis
    if 'fund_master' in dataframes or any('master' in key.lower() for key in dataframes.keys()):
        master_df = dataframes.get('fund_master') or next(
            (v for k, v in dataframes.items() if 'master' in k.lower()), None
        )
        if master_df is not None:
            print("\n📈 FUND MASTER ANALYSIS:")
            print("-" * 80)
            
            if 'Fund House' in master_df.columns or 'fund_house' in master_df.columns:
                house_col = 'Fund House' if 'Fund House' in master_df.columns else 'fund_house'
                print(f"Unique Fund Houses: {master_df[house_col].nunique()}")
                print(f"Fund Houses: {master_df[house_col].unique()[:10]}")
            
            if 'Category' in master_df.columns or 'category' in master_df.columns:
                cat_col = 'Category' if 'Category' in master_df.columns else 'category'
                print(f"\nUnique Categories: {master_df[cat_col].nunique()}")
                print(f"Categories: {master_df[cat_col].unique()}")
            
            if 'Sub-Category' in master_df.columns or 'sub_category' in master_df.columns:
                subcat_col = 'Sub-Category' if 'Sub-Category' in master_df.columns else 'sub_category'
                print(f"\nUnique Sub-Categories: {master_df[subcat_col].nunique()}")
                print(f"Sub-Categories: {master_df[subcat_col].unique()[:10]}")
            
            if 'Risk Grade' in master_df.columns or 'risk_grade' in master_df.columns:
                risk_col = 'Risk Grade' if 'Risk Grade' in master_df.columns else 'risk_grade'
                print(f"\nUnique Risk Grades: {master_df[risk_col].nunique()}")
                print(f"Risk Grades: {master_df[risk_col].unique()}")
    
    # AMFI Code Validation
    print("\n\n✅ AMFI CODE VALIDATION:")
    print("-" * 80)
    validate_amfi_codes(dataframes)
    
    print(f"\n{'='*80}")
    print("✨ Data ingestion complete!")
    print(f"{'='*80}\n")
    
    return dataframes


def validate_amfi_codes(dataframes):
    """
    Validate that AMFI codes in nav_history exist in fund_master.
    
    Parameters:
    -----------
    dataframes : dict
        Dictionary of loaded dataframes
    """
    # Find master and nav history dataframes
    master_df = None
    nav_df = None
    
    for key, df in dataframes.items():
        if 'master' in key.lower():
            master_df = df
        if 'nav' in key.lower() or 'history' in key.lower():
            nav_df = df
    
    if master_df is None:
        print("⚠️ Fund master data not found for validation")
        return
    
    # Find scheme code column in master
    code_col_master = next(
        (col for col in master_df.columns if 'code' in col.lower() or 'scheme' in col.lower()),
        None
    )
    
    if code_col_master is None:
        print("⚠️ Scheme code column not found in fund master")
        return
    
    master_codes = set(master_df[code_col_master].dropna().unique())
    print(f"Total unique AMFI codes in fund master: {len(master_codes)}")
    
    if nav_df is not None and not nav_df.empty:
        code_col_nav = next(
            (col for col in nav_df.columns if 'code' in col.lower() or 'scheme' in col.lower()),
            None
        )
        
        if code_col_nav:
            nav_codes = set(nav_df[code_col_nav].dropna().unique())
            missing_codes = nav_codes - master_codes
            
            if missing_codes:
                print(f"⚠️ {len(missing_codes)} codes in NAV history NOT found in fund master:")
                print(f"   Missing codes: {list(missing_codes)[:10]}")
            else:
                print("✅ All NAV codes are present in fund master")
        else:
            print("⚠️ Scheme code column not found in NAV data")


if __name__ == "__main__":
    dataframes = main()
