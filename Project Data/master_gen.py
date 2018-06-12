#!/usr/bin/env python
'''
ATTRIBUTES:
- percent area cultivated
- annual precipitation
- Rainwater Harvesting awareness
- desalination water produced
- seasonal variability
- water stress level (CLASS)
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
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import LogisticRegression
from sklearn.linear_model import Ridge
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import Pipeline

def export(table, out_path):
    table.to_csv(out_path, index = False)
    print('CSV exported to:', out_path)

def create_master():
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

def fill_master():
    master = pd.read_csv('data/master.csv', index_col = False)
    countries = master.Country.unique().tolist()            # Get list of countries

    for c in countries:
        data = master[master['Country']==c]
        print('Filling data for', c)

        ind = np.array(data.index.values.tolist())          # Get index values for each row
        years = np.array([data.Year.tolist()])              # Get years

        vals = np.array(data['stress'].tolist())            # Get stress values
        fitting_vals = np.array(data['stress'].tolist())    # Duplicate for fitting

        missing_val = 0                                     # Flag for array with missing values
        for i in range(len(vals)):                          # Convert NaNs to 0
            if np.isnan(vals[i]):
                vals[i] = 0
                missing_val = 1

        if missing_val == 1:
            model = best_fit(years.T, vals)                 # Create best fit line model if missing values present
            for i in range(len(vals)):
                if np.isnan(fitting_vals[i]):
                    new_val = max(model.predict(years[0][i]), 0)
                    master.at[ind[i], 'stress'] = new_val

    export(master, 'data/master_filled.csv')

def categorize_target():
    master = pd.read_csv('data/master_filled.csv', index_col = False)
    master.insert(len(master.columns), 'stress_level', 'none')          # Insert stress level column

    for i in range(master.shape[0]):                                    # Determine category and add to stress level column
        stress = master.at[i,'stress']
        if stress <= 20.0:
            master.at[i,'stress_level'] = 'none'
        elif stress <= 40.0:
            master.at[i,'stress_level'] = 'low'
        elif stress <= 60.0:
            master.at[i,'stress_level'] = 'medium'
        elif stress <= 80.0:
            master.at[i,'stress_level'] = 'alert'
        elif stress <= 100.0:
            master.at[i,'stress_level'] = 'high'
        else:
            master.at[i,'stress_level'] = 'critical'

    master.drop(['stress'], axis = 1, inplace = True)                   # Delete numerical stress column
    export(master, 'data/master_category.csv')                          # Export CSV

def best_fit(x, y):
    model = Ridge(alpha=0.5)
    model.fit(x,y)
    return model

def build_test_training_sets():
    master = pd.read_csv('data/master_category.csv', index_col = False)
    total_samples = master.shape[0]                             # Get total number of samples
    num_test = int(total_samples/10)                            # Calculate percentage of test samples

    master_test = pd.DataFrame()                                # Generate test and train dataframes
    master_train = pd.DataFrame()

    i = 0
    visited = [0 for x in range(total_samples)]                 # Build array to keep track of visited rows
    while i < num_test:                                         # Randomly add rows to test set
        ind = np.random.randint(0,total_samples)
        if visited[ind] == 0:
            master_test = master_test.append(master.loc[ind])
            visited[ind] = 1
            i += 1

    for j in range(total_samples):                              # Add remaining rows to training set
        if visited[j] == 0:
            master_train = master_train.append(master.loc[j])

    export(master_test, 'data/master_test.csv')                 # Export CSV files
    export(master_train, 'data/master_train.csv')

def main():
    # create_master()
    fill_master()
    categorize_target()
    build_test_training_sets()

if __name__ == "__main__":
    main()
