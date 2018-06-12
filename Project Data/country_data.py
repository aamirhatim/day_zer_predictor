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


#def collect_data():
#     # Import CSVs
country_stress = pd.read_csv('data/lookup_table.csv', index_col = False)
country_list = (country_stress.Country.unique())
critical_yearlist = []
critical_year = 0
for i in country_list:
    #print(i)
    data = country_stress[country_stress['Country']==i]
    #print(data)
    final_data = data.ix[:, ['Year', 'stress']]
    final_data.loc[-1] = [1850,0]
    final_data.index = final_data.index+1
    final_data = final_data.sort_index()
    #print(final_data)

    export(final_data, 'data/stress.csv')

    data = pd.read_csv('data/stress.csv')
    data.head()

    X = data['Year'].values[:,np.newaxis]
    y = data['stress'].values

    model = LinearRegression()
    model.fit(X, y)

    slope = model.coef_
    x_intercept = model.intercept_
    #print(model.intercept_)
    #print(model.coef_)

    critical_year = (7-x_intercept)/slope
    print(critical_year)
    critical_yearlist.append(critical_year[0])

clean_stress = pd.DataFrame({'Country':country_list,'YearZero':critical_yearlist})
export(clean_stress,'data/final_stress.csv')
