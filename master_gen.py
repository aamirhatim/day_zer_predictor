#!/usr/bin/env python
'''
ATTRIBUTES EXTRACTED:
- percent area cultivated
- annual precipitation
'''

import pandas as pd
import numpy as np
import sys

def create_master():
    # Import CSVs
    land_stats = pd.read_csv('data/clean/land_stats_AQUASTAT_clean.csv', index_col = False)
    precipitation = pd.read_csv('data/clean/precipitation_AQUASTAT_clean.csv', index_col = False)
    water_resources = pd.read_csv('data/clean/water_resources_AQUASTAT_clean.csv', index_col = False)

    # Isolate attributes
    percent_cultivated = land_stats[['Country', 'Year', 'percent_cultivated']]
    annual_ppt = precipitation[['Country', 'Year', 'annual_ppt_mm']]
    # print annual_ppt

    # Join attributes into master table
    master = pd.merge(percent_cultivated, annual_ppt,  how = 'outer', left_on = ['Country','Year'], right_on = ['Country','Year'])
    # print master

    # Export to CSV
    output = 'data/clean/master.csv'
    master.to_csv(output, index = False)
    print('CSV exported to:', output)

def main():
    create_master()

if __name__ == "__main__":
    main()
