#!/usr/bin/env python
'''
ATTRIBUTES EXTRACTED:
- percent area cultivated
- annual precipitation
- Rainwater Harvesting awareness
- desalination water produced
- seasonal variability
- water stress level**
- total renewable resources per capita
- total water withdrawal per capita
- dependency ratio
- percent agricultural withdrawal
- percent industrial withdrawal
- percent municipal withdrawn
- total exploitable**
'''

import pandas as pd
import numpy as np
import sys

def export(table, out_path):
    table.to_csv(out_path, index = False)
    print('CSV exported to:', out_path)

def create_master():
    years = [1962, 1967, 1972, 1977, 1982, 1987, 1992, 1997, 2002, 2007, 2012, 2013, 2014]

    # Import CSVs
    land_stats = pd.read_csv('data/clean/land_stats_AQUASTAT_clean.csv', index_col = False)
    precipitation = pd.read_csv('data/clean/precipitation_AQUASTAT_clean.csv', index_col = False)
    water_resources = pd.read_csv('data/clean/water_resources_AQUASTAT_clean.csv', index_col = False)
    rwh = pd.read_csv('data/raw/RWH_multiple_sources.csv', index_col = False)
    stress = pd.read_csv('data/clean/stress_AQUASTAT_clean.csv', index_col = False)
    desal = pd.read_csv('data/clean/desalination_AQUASTAT_clean.csv', index_col = False)
    resources = pd.read_csv('data/clean/water_resources_AQUASTAT_clean.csv', index_col = False)

    # Isolate attributes and put into a list
    attributes = []
    attributes.append(land_stats[['Country', 'Year', 'percent_cultivated']])
    attributes.append(precipitation[['Country', 'Year', 'annual_ppt_mm']])
    attributes.append(desal[['Country', 'Year', 'desalination']])
    attributes.append(resources[['Country', 'Year', 'dependency', 'total_renewable_pc', 'agri_withdraw_percent', 'ind_withdraw_percent', 'muni_withdraw_percent', 'total_withdraw_pc']])
    attributes.append(stress[['Country', 'Year', 'stress']])

    # Create master table with first attribute
    master = attributes[0]

    # Join remaining attributes into master table
    for a in range(len(attributes)-1):
        master = pd.merge(master, attributes[a+1], how = 'outer', left_on = ['Country','Year'], right_on = ['Country','Year'])

    ##########################################
    ## Clean up RWH Data then add to master ##
    ##########################################
    harvesting = pd.DataFrame(columns = ['Country', 'Year', 'rwh_awareness'])
    for i in range(master.shape[0]):
        country = master.at[i, 'Country']                           # Get country name in master row
        yr = master.at[i, 'Year']                                   # Get year in master row
        rwh_ind = rwh.index[rwh['Country']==country].tolist()       # Get index of country in rwh
        if len(rwh_ind) == 0:
            awareness = 0
        else:
            rwh_ind = rwh_ind[0]
            awareness = rwh.at[rwh_ind, 'RWH_awareness']
        harvesting.loc[i] = [country, yr, awareness]

    # Export RWH data to clean CSV
    export(harvesting, 'data/clean/rwh_awareness_multiple_sources_clean.csv')
    ##########################################
    ##########################################


    ##########################################
    ## Clean up Seasonal Variability Data   ##
    ## then add to master                   ##
    ##########################################
    seasonal_var = resources[(resources.seasonal_variability > 0)][['Country', 'Year', 'seasonal_variability']].reset_index(drop=True)
    seasonal = pd.DataFrame(columns = ['Country', 'Year', 'seasonal_variability'])
    for i in range(master.shape[0]):
        country = master.at[i, 'Country']                                               # Get country name in master row
        yr = master.at[i, 'Year']                                                       # Get year in master row
        seasonal_ind = seasonal_var.index[seasonal_var['Country']==country].tolist()    # Get index of country in seasonal
        if len(seasonal_ind) == 0:
            variability = 0
        else:
            seasonal_ind = seasonal_ind[0]
            variability = seasonal_var.at[seasonal_ind, 'seasonal_variability']
        seasonal.loc[i] = [country, yr, variability]

    # Export seasonal variability data to clean CSV
    export(seasonal, 'data/clean/seasonal_variability_AQUASTAT_clean.csv')
    ##########################################
    ##########################################

    # Add to master
    master = pd.merge(master, harvesting, how = 'outer', left_on = ['Country','Year'], right_on = ['Country','Year'])
    master = pd.merge(master, seasonal, how = 'outer', left_on = ['Country','Year'], right_on = ['Country','Year'])

    # Export master to CSV
    export(master, 'data/master.csv')

def main():
    create_master()

if __name__ == "__main__":
    main()
