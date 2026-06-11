# U.S. Beef Market Analysis

## Overview

This project examines changes in the U.S. beef market by analyzing
production, trade, supply, and pricing data over time. The goal of the
analysis is to understand how major market factors, including domestic
production, imports, exports, and economic adjustments, relate to
changes in wholesale beef prices.

The workflow consists of collecting raw market and economic data,
cleaning and transforming the data into an analysis-ready format, and
performing exploratory analysis to identify trends and relationships
within the beef supply chain.

------------------------------------------------------------------------

## Project Structure

``` text
us_beef_analysis/
│
├── data/
│   ├── raw/
│   │   ├── USDA market datasets
│   │   ├── economic indicator datasets
│   │   └── original downloaded files
│   │
│   ├── processed/
│   │   └── beef_market_cleaned.csv
│   │
│   └── results/
│       └── analysis_results.csv
│
├── import_and_clean.py
│   └── Imports raw data, cleans variables,
│       handles formatting, and creates the processed dataset
│
├── eda.ipynb
│   └── Exploratory data analysis, visualizations,
│       and statistical exploration
│
└── README.md
```

------------------------------------------------------------------------

## Data Usage

Raw data should be placed in:

``` text
data/raw/
```

The cleaning script processes these files and creates the final dataset
used for analysis:

``` text
data/processed/beef_market_cleaned.csv
```

The processed dataset is intended to be the primary file used for
visualization and analysis. It contains standardized variables, cleaned
values, and derived features needed for evaluating beef market trends.

------------------------------------------------------------------------

## Data Processing

The data preparation workflow includes:

-   Importing USDA and economic datasets
-   Removing unnecessary formatting and metadata
-   Standardizing column names
-   Converting variables into appropriate numeric formats
-   Checking for missing values
-   Creating analysis-ready variables
-   Adjusting price measurements for inflation where applicable

After processing, the dataset contains consistent observations that can
be compared across years.

------------------------------------------------------------------------

## Analysis

The analysis focuses on the relationship between beef prices and major
market drivers.

Key areas explored include:

### Production and Supply

Production variables are used to examine how changes in domestic beef
availability relate to price movement. This includes measures such as:

-   Farm production
-   Commercial production
-   Total production
-   Beginning and ending stocks
-   Total supply

### Trade

Imports and exports are analyzed to understand the influence of
international trade on domestic beef availability.

Variables include:

-   Beef imports
-   Beef exports
-   Total disappearance

### Price Trends

Wholesale beef prices are evaluated over time to identify:

-   Long-term price trends
-   Changes in market conditions
-   Differences between nominal and inflation-adjusted prices

Inflation-adjusted price measures allow comparisons across years without
the effects of changing purchasing power.

------------------------------------------------------------------------

## Exploratory Data Analysis

Exploratory analysis is performed in:

``` text
eda.ipynb
```

The notebook includes:

-   Summary statistics
-   Distribution analysis
-   Trend visualizations
-   Correlation analysis
-   Examination of relationships between supply factors and price
    changes

------------------------------------------------------------------------

## Requirements

The project uses Python with the following packages:

``` bash
pip install pandas numpy matplotlib seaborn statsmodels openpyxl jupyter
```

These packages support:

-   Data manipulation
-   Numerical analysis
-   Visualization
-   Statistical modeling
-   Notebook execution
-   Spreadsheet file handling

------------------------------------------------------------------------

## Running the Project

### 1. Install dependencies

Create an environment and install requirements:

``` bash
pip install pandas numpy matplotlib seaborn statsmodels openpyxl jupyter statsmodels
```

### 2. Process the data

Run:

``` bash
python import_and_clean.py
```

This generates:

``` text
data/processed/beef_market_cleaned.csv
```

### 3. Perform analysis

Open:

``` bash
jupyter notebook eda.ipynb
```

Run the notebook cells to reproduce the exploratory analysis and
visualizations.

------------------------------------------------------------------------

## Purpose

This project provides a reproducible workflow for studying U.S. beef
market dynamics through data cleaning, exploratory analysis, and
statistical evaluation of supply chain factors affecting price changes.
