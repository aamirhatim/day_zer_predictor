#!/usr/bin/env python3.6
'''
PANDAS code to parse and clean CSV files from AQUASTAT
'''
import pandas as pd
import numpy as np
import sys

def aquastat(filepath, output):
    # Import list of countries
    c = pd.read_csv('data/countries.csv')
    c.rename(columns = {'Area':'Country', 'Area Id':'Area_Id'}, inplace = True)
    # List of country IDs
    countries = c.as_matrix(c.columns[:1]).T[0]

    # Import CSV
    print('Parsing AQUASTAT CSV', filepath, '...')
    input_csv = pd.read_csv(filepath, index_col = False)

    # Remove unnecessary columns
    input_csv.drop(['Variable Id', 'Symbol', 'Md'], axis = 1, inplace = True)

    # Rename columns
    input_csv.rename(columns = {'Area':'Country', 'Area Id':'Area_Id', 'Variable Name':'Variable_Name'}, inplace = True)

    # Only keep rows that have a country in the Country column
    input_csv = input_csv[input_csv['Country'].isin(countries)]
    input_csv[['Country', 'Value']].to_csv('data/output.csv', index = False)

    # Split 'Variable_Name' column into individual attribute columns
    attributes = input_csv['Variable_Name'].unique()
    split_attr = input_csv[input_csv['Variable_Name'] == attributes[0]][['Country', 'Year', 'Value']]
    split_attr.rename(columns = {'Value': attributes[0]}, inplace = True)

    # Combine variable columns into one table
    for v in range(len(attributes)-1):
        # Isolate one variable and its values
        temp = input_csv[input_csv['Variable_Name'] == attributes[v+1]][['Country', 'Year', 'Value']]
        temp.rename(columns = {'Value': attributes[v+1]}, inplace = True)

        # Join table with the final CSV
        split_attr = pd.merge(split_attr, temp,  how = 'outer', left_on = ['Country','Year'], right_on = ['Country','Year'])

    # Export final CSV
    split_attr.to_csv(output, index = False)
    print('CSV exported to', output)

def main():
    filepath = sys.argv[1]
    output = sys.argv[2]
    aquastat(filepath, output)

if __name__ == "__main__":
    main()
