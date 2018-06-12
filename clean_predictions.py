#!/usr/bin/env python

import pandas as pd
import numpy as np
import sys

def export(table, out_path):
    table.to_csv(out_path, index = False)
    print('CSV exported to:', out_path)

def main():
    data = pd.read_csv('data/predictions.csv')
    data['stress'] = data['predicted'].astype(str).str[0]
    data['stress'] = pd.to_numeric(data.stress, errors = 'coerce')
    data.drop(['inst#', 'actual', 'error', 'predicted', 'prediction'], axis = 1, inplace = True)
    data = data.reset_index(drop = True)

    export(data, 'data/lookup_table.csv')

if __name__ == "__main__":
    main()
