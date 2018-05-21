import pandas as pd



df = pd.read_csv('water_resources_revised.csv')
df2 = df.loc[(df['Variable Name'] == 'Total renewable water resources per capita') & (df['Year'] == 2014)]
df2 = df2.drop(['Variable Name'], axis = 1)
df2.to_csv('new_water_resources.csv', sep='\t')
print(df2)
