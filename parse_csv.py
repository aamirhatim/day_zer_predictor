#!/usr/bin/env python3.6
'''
PANDAS code to parse and clean CSV files from AQUASTAT
'''
import pandas as pd
import numpy as np
import sys

def aquastat(filepath, output):
    # Import list of countries
    c = pd.read_csv('data/raw/countries.csv')
    # List of country IDs
    countries = c.as_matrix(c.columns[:1]).T[0]

    # Import CSV
    print('Parsing AQUASTAT CSV:', filepath, '...')
    input_csv = pd.read_csv(filepath, index_col = False)

    # Remove unnecessary columns
    input_csv.drop(['Variable Id', 'Symbol', 'Md'], axis = 1, inplace = True)

    # Rename columns
    input_csv.rename(columns = {'Area':'Country', 'Area Id':'Area_Id', 'Variable Name':'Variable_Name'}, inplace = True)

    # Only keep rows that have a country in the Country column
    input_csv = input_csv[input_csv['Country'].isin(countries)].reset_index(drop = True)

    # Shift dates by 2 years to standardize to years divisible by 5
    for i in range(input_csv.shape[0]):
        date = input_csv.at[i, 'Year']
        mod = date%5
        if mod != 0:
            input_csv.at[i, 'Year'] = int(5 * round(float(date)/5))

    # Split 'Variable_Name' column into individual attribute columns
    attributes = input_csv['Variable_Name'].unique()
    split_attr = input_csv[input_csv['Variable_Name'] == attributes[0]][['Country', 'Year', 'Value']]
    split_attr.rename(columns = {'Value': attributes[0]}, inplace = True)
    split_attr.reset_index(drop = True)

    # Combine variable columns into one table
    for v in range(len(attributes)-1):
        # Isolate one variable and its values
        temp = input_csv[input_csv['Variable_Name'] == attributes[v+1]][['Country', 'Year', 'Value']]
        temp.rename(columns = {'Value': attributes[v+1]}, inplace = True)
        temp.reset_index(drop = True)

        # Join table with the final CSV
        split_attr = pd.merge(split_attr, temp,  how = 'outer', left_on = ['Country','Year'], right_on = ['Country','Year'])
        split_attr.reset_index(drop = True)

    # Export final CSV
    split_attr.reset_index(drop = True)
    split_attr.to_csv(output, index = False)
    print('CSV exported to:', output)

def main():
    source = sys.argv[1]
    filepath = 'data/raw/' + sys.argv[2] + '.csv'
    output = 'data/clean/' + sys.argv[2] + '_clean.csv'

    if source == 'aquastat':
        aquastat(filepath, output)
    else:
        print('Uknown source!')

if __name__ == "__main__":
    main()
