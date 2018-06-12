import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import Pipeline



data = pd.read_csv('stress.csv')
data.head()

X = data['Year'].values[:,np.newaxis]
y = data['Stress'].values

model = LinearRegression()
model.fit(X, y)

#polynomial regression, degree 6
model1 = Pipeline([('poly', PolynomialFeatures(degree=6)),
                  ('linear', LinearRegression(fit_intercept=False))])
model1.fit(X,y)
print(model1.named_steps['linear'].coef_)


#finding X intercept for linear regression
# slope = model.coef_
# x_intercept = model.intercept_
# print(model.intercept_)
# print(model.coef_)
#
# critical_year = (100-x_intercept)/slope
# print("Year of critical water shortage:", critical_year)
#
#
#
plt.scatter(X, y,color='r')
plt.plot(X, model1.predict(X),color='k')
plt.show()
