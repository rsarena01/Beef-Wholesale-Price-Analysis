import pandas as pd
from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent
DATA_RAW = BASE_DIR.parent / 'data' / 'raw'
DATA_PROCESSED = BASE_DIR.parent / 'data' / 'processed'

def clean_wholesale(file_path: Path) -> pd.DataFrame:
    """ Load and aggregates monthly USDA Beef Wholesale price data."""
    df = pd.read_excel(file_path, sheet_name='Historical')

    # cleanly remove header and metadata artifacts
    col0 = df.iloc[:, 0]
    col0 = pd.to_datetime(col0, format='%Y-%m-%d', errors='coerce')
    df = df[pd.notnull(df[col0.name])]

    # data for beef
    df_beef = df.iloc[:, :5].copy()

    # rename columns
    df_beef.columns = [
        'period',
        'choice_price',
        'select_price',
        '90%_fresh_price',
        '90%_imported_frozen_price'
    ]

    # coerce data types using explicit assignment
    numeric_cols = df_beef.columns[1:]
    df_beef[numeric_cols] = df_beef[numeric_cols].apply(pd.to_numeric, errors='coerce')

    # standardize time-series feature
    df_beef['year'] = df_beef['period'].apply(pd.to_datetime, format='%Y', errors='coerce').dt.year
    df_beef = df_beef.drop(columns=['period'])

    # aggregate monthly data by year and normalize the index
    yearly_av = df_beef.groupby('year').mean()
    yearly_av['year'] = yearly_av.index
    yearly_av = yearly_av.reset_index(drop=True)

    # filter by logical condition for 2000 - 2025
    idx_0 = yearly_av.loc[yearly_av['year'] == 2000].index[0]
    idx_last = yearly_av.loc[yearly_av['year'] == 2025].index[0]
    return yearly_av.iloc[idx_0:idx_last + 1, :]

def clean_meat_and_supply_demand(file_path: Path) -> pd.DataFrame:
    """ Transforms quarterly/yearly balance sheet data into standardized annual format."""
    df = pd.read_excel(file_path, sheet_name='WASDE_Beef-Full')

    # drop null columns created from data import
    df_msd = df.dropna(axis=1, how='all')

    # rename columns
    df_msd.columns = [
    'year',
    'yr/qtr',
    'commercial_production',
    'farm_production',
    'total_production',
    'begin_stock',
    'imports',
    'total_supply',
    'exports',
    'end_stock',
    'total_disappearance',
    'population',
    'carcass_weight',
    'retail_weight',
    'boneless_retail_weight'
        ]

    # forward fill year for each quarter
    df_msd['year'] = df_msd['year'].ffill()

    # sanitize string numeric data types containing commas
    df_msd = df_msd.replace(',', '', regex=True)

    # isolate annual aggregates
    filtered = df_msd.loc[df_msd['yr/qtr'].str.contains('Yr')]
    filtered = filtered.drop(columns=['yr/qtr'])

    # coerce data types using explicit assignment
    numeric_cols = filtered.columns[1:]
    filtered[numeric_cols] = filtered[numeric_cols].apply(pd.to_numeric, errors='coerce')

    # normalize the index
    filtered = filtered.reset_index().drop(columns=['index'])

    # filter by logical condition for 2000 - 2025
    return filtered[filtered['year'].between(2000, 2025)]

def clean_ppi(file_path: Path) -> pd.DataFrame:
    """Parses St. Louis FRED Producer Price Index - All Commodities metadata."""
    df = pd.read_csv(file_path)

    # extract annual average
    df['year'] = df['observation_date'].str[:4].astype(int)
    df= df.drop(columns='observation_date')

    # cast target feature explicitly to numeric before calculating mean
    df['PPIACO'] = pd.to_numeric(df['PPIACO'], errors='coerce')

    # aggregate by year and normalize the index
    yearly_ppi = df.groupby('year').mean().round(4).reset_index()

    # filter by logical condition for 2000 - 2025
    return yearly_ppi[yearly_ppi['year'].between(2000, 2025)]

def main():
    """Executes full data compilation pipeline."""
    print("Initializing Data Cleaning Pipeline...")

    # define file locations
    wholesale_path = DATA_RAW / 'WholesalePrices.xlsx'
    meat_sd_path = DATA_RAW / 'MeatSDFull.xlsx'
    ppi_path = DATA_RAW / 'PPIACO.csv'

    # execute extraction and cleaning modules
    df_ws = clean_wholesale(wholesale_path)
    df_msd = clean_meat_and_supply_demand(meat_sd_path)
    df_ppi = clean_ppi(ppi_path)

    # execute data sources
    merged = pd.merge(df_ws, df_msd, on='year', how='inner')
    final_dataset = pd.merge(merged, df_ppi, on='year', how='inner')

    # structural and formatting changes
    final_dataset.insert(0, 'year', final_dataset.pop('year'))
    final_dataset['year'] = final_dataset['year'].astype(int)
    final_dataset = final_dataset.round(4)

    # output to clean target environment
    os.makedirs(DATA_PROCESSED, exist_ok=True)
    output_file = DATA_PROCESSED / 'beef_market_clean_dataset.csv'
    final_dataset.to_csv(output_file, index=False)

    print(f"Pipeline complete. Dataset shape: {final_dataset.shape}")
    print(f"File exported successfully to: {output_file}")


if __name__ == '__main__':
    main()
    