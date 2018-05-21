#!/usr/bin/env python3.6
'''
PANDAS code to query the precipitation csv from AQUASTAT
'''

import pandas as pd
import numpy as np

def main():
    filename = 'precipitation_AQUASTAT.csv'
    path = 'data/'+filename

    precip = pd.read_csv(path)
    delvalues = ['Md', 'Symbol', 'Area Id', 'Variable Id']
    for x in delvalues:
        del precip[x]

    # ind = precip[precip.loc['Metadata:']].index.values.astype(int)
    print(precip.info())

if __name__ == "__main__":
    main()
