import pandas as pd



df = pd.read_csv('water_resources.csv')
df2 = df.loc[(df['Variable Name'] == 'Total renewable water resources per capita') & (df['Year'] == 2014)]
print(df2)
