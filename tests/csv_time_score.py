from datetime import datetime, timedelta
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as md
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

ds = pd.read_csv('C:\Work\py-dat.csv')


ds = ds.dropna()

ds['Time'] = [datetime.strptime(str(x), '%I:%M:%S %p') for x in ds['Time']]
ds['Time'] = pd.DatetimeIndex(ds['Time']).time

ds.plot(x='Time', y='Score', style='o')
#
# plt.title('Start time vs Score')
# plt.xlabel('Start Time')
# plt.ylabel('Score')
# print(ds.head())
# plt.show()

X = ds.iloc[:, :-1].values
y = ds.iloc[:, 1].values

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)

regressor = LinearRegression()
regressor.fit(X_train, y_train)

print(regressor.intercept_)
