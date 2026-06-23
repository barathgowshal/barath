# Data Quality Summary - Mutual Fund Analytics

## Project Setup Status ✅

**Project Name:** Mutual Fund Analytics Capstone  
**Start Date:** 20 June 2026  
**Status:** Day 1 - Data Ingestion Complete  
**Repository:** barathgowshal/barath

---

## Project Structure

```
barath/
├── data/
│   ├── raw/              # Raw CSV datasets (10 files expected)
│   └── processed/        # Processed data files
├── notebooks/            # Jupyter notebooks for analysis
├── sql/                  # SQL queries
├── dashboard/            # Dashboard scripts
├── reports/              # Analysis reports
├── data_ingestion.py     # Data loading & exploration script
├── live_nav_fetch.py     # Live NAV fetching script
├── requirements.txt      # Python dependencies
├── .gitignore           # Git configuration
└── README.md            # Project documentation
```

---

## Day 1 Deliverables

### 1. ✅ Project Folder Structure
- ✓ `data/raw/` - for raw CSV datasets
- ✓ `data/processed/` - for processed data
- ✓ `notebooks/` - for Jupyter notebooks
- ✓ `sql/` - for SQL queries
- ✓ `dashboard/` - for dashboard scripts
- ✓ `reports/` - for analysis reports

### 2. ✅ Git Repository
- ✓ Repository initialized: `barathgowshal/barath`
- ✓ Branch created: `day-1-data-ingestion`
- ✓ Initial commit pushed

### 3. ✅ Dependencies Installation
All required packages defined in `requirements.txt`:

**Core Data Science:**
- pandas 2.0.3 (data manipulation)
- numpy 1.24.3 (numerical computing)
- scipy 1.11.2 (scientific computing)

**Visualization:**
- matplotlib 3.7.2 (plotting)
- seaborn 0.12.2 (statistical visualization)
- plotly 5.15.0 (interactive plots)

**Database & API:**
- sqlalchemy 2.0.20 (database ORM)
- requests 2.31.0 (HTTP requests)

**Jupyter & Notebooks:**
- jupyter 1.0.0
- jupyterlab 4.0.5
- ipython 8.15.0

### 4. ✅ Data Ingestion Script (data_ingestion.py)

**Features:**
- Loads all CSV files from `data/raw/`
- For each dataset displays:
  - Shape (rows × columns)
  - Data types
  - First 5 rows (head)
  - Statistical summary
  - Missing value analysis
  - Anomaly detection
  - Duplicate row identification

**Fund Master Analysis:**
- Unique fund houses
- Categories and sub-categories
- Risk grades distribution

**AMFI Code Validation:**
- Validates AMFI codes consistency
- Checks nav_history codes against fund_master
- Reports missing or invalid codes

### 5. ✅ Live NAV Fetching Script (live_nav_fetch.py)

**Funds Fetched:**
1. HDFC Top 100 Direct (125497) - Primary fund
2. SBI Bluechip (119551)
3. ICICI Bluechip (120503)
4. Nippon Large Cap (118632)
5. Axis Bluechip (119092)
6. Kotak Bluechip (120841)

**Features:**
- Fetches data from mfapi.in API
- Parses JSON responses
- Saves individual fund CSVs
- Creates `nav_live_summary.csv` with latest NAVs
- Includes API error handling
- Rate limiting (1 second between requests)
- Connection testing before execution

---

## How to Run

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Place Raw Data
Place your 10 CSV datasets in `data/raw/` directory:
- fund_master.csv
- nav_history.csv
- (and 8 other datasets)

### Step 3: Run Data Ingestion
```bash
python data_ingestion.py
```

**Output:**
- Console output showing dataset summaries
- Shape, dtypes, and head() for each file
- Anomaly detection results
- Fund master analysis
- AMFI code validation report

### Step 4: Fetch Live NAV Data
```bash
python live_nav_fetch.py
```

**Output:**
- NAV data for 6 mutual funds saved as CSVs
- `nav_live_summary.csv` with latest NAVs
- API fetch status report
- Console output with fetch timestamps and NAV ranges

### Step 5: Use Jupyter for Analysis
```bash
jupyter lab
```

Create notebooks in `notebooks/` directory for exploratory analysis.

---

## Expected CSV Files in data/raw/

After running the scripts, expect these files:

**From data_ingestion.py:**
- fund_master.csv (Fund metadata)
- nav_history.csv (Historical NAV data)
- (8 additional datasets)

**From live_nav_fetch.py:**
- nav_125497_hdfc_top_100_direct.csv
- nav_119551_sbi_bluechip.csv
- nav_120503_icici_bluechip.csv
- nav_118632_nippon_large_cap.csv
- nav_119092_axis_bluechip.csv
- nav_120841_kotak_bluechip.csv
- nav_live_summary.csv (Summary of latest NAVs)

---

## Data Quality Checks Performed

### Missing Values Analysis
- Count of NULL values per column
- Percentage of missing data
- Flag columns with >50% missing values

### AMFI Code Validation
- All codes are valid 6-digit numbers
- Codes in nav_history match fund_master
- No duplicate codes within same dataset

### Anomaly Detection
- Empty dataframes
- Columns with all NULL values
- Invalid AMFI codes (NULL or 0)
- Unexpected negative values
- Duplicate rows

### Data Type Validation
- Numeric columns are properly typed
- Date columns are datetime format
- Categorical columns identified

---

## Known Limitations

1. **API Dependency:** Live NAV fetch requires internet connection
2. **API Rate Limits:** mfapi.in may have rate limiting (handled with 1-second delays)
3. **Data Availability:** Some historical NAV data may have gaps
4. **CSV Format:** Assumes UTF-8 encoding and standard CSV structure

---

## Next Steps (Day 2+)

- Exploratory Data Analysis (EDA)
- Time series analysis of NAV trends
- Fund performance comparison
- Risk analysis
- Portfolio construction strategies
- Dashboard development
- Advanced analytics and reporting

---

## File Descriptions

| File | Purpose |
|------|----------|
| `data_ingestion.py` | Load and explore all datasets |
| `live_nav_fetch.py` | Fetch live NAV from API |
| `requirements.txt` | Python dependencies |
| `data/raw/` | Raw CSV datasets |
| `data/processed/` | Processed datasets |
| `notebooks/` | Jupyter analysis notebooks |
| `sql/` | SQL queries |
| `dashboard/` | Dashboard code |
| `reports/` | Final reports |

---

## Git Commit History

```
Day 1: Data ingestion complete
├── Initial project setup
├── Directory structure created
├── data_ingestion.py added
├── live_nav_fetch.py added
├── requirements.txt created
└── Documentation completed
```

---

## Contact & Support

For issues or questions:
- Repository: https://github.com/barathgowshal/barath
- Branch: day-1-data-ingestion

---

*Last Updated: 23 June 2026*  
*Status: Complete - Ready for Day 2 Analysis*
