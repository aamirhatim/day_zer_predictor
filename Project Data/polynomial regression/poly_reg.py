import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import Pipeline

from datetime import timedelta, datetime


def convert_partial_year(number):

    year = int(number)
    d = timedelta(days=(number - year)*365)
    day_one = datetime(year,1,1)
    date = d + day_one
    return date



data = pd.read_csv('stress.csv')
data.head()

X = data['Year'].values[:,np.newaxis]
y = data['Stress'].values

model = LinearRegression()
model.fit(X, y)

# polynomial regression, degree 6
model1 = Pipeline([('poly', PolynomialFeatures(degree=3)),
                  ('linear', LinearRegression(fit_intercept=False))])
model1.fit(X,y)
#print(model1.named_steps['linear'].coef_)
c = model1.named_steps['linear'].coef_
#print(c)

# year = np.poly1d(c)

# print(year(6))





#finding X intercept for linear regression
slope = model.coef_
x_intercept = model.intercept_
print(model.intercept_)
print(model.coef_)

critical_year = (7-x_intercept)/slope
print("Year of critical water shortage:", critical_year)
ddmmyy = convert_partial_year(critical_year[0])
#print(ddmmyy)

format = "%a %b %d %Y"

today = datetime.today()
#print('ISO     :', today)

s = today.strftime(format)
#print('strftime:', s)

d = datetime.strptime(s, format)
day_zero = ddmmyy.strftime(format)
print(day_zero)





#
plt.scatter(X, y,color='r')
plt.plot(X, model.predict(X),color='k')

plt.show()
