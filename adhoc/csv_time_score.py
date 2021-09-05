import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

# csv formatted as:
# time,score
# 6:00:00 PM,6.22
# 9:30:00 AM,6.149

df = pd.read_csv('C:\Work\py-dat.csv')
df = df.dropna()


def convert_to_dec(str_time):
    str_list = str_time.split(":")
    str_list[1] = str(int(str_list[1])/60).lstrip("0")
    if "PM" in str_list[2].upper():
        str_list[0] = int(str_list[0])+12
    return float("".join(str(x) for x in str_list[:2]))


df['Time'] = [convert_to_dec(x) for x in df['Time']]
df.sort_values(by='Time', ascending=True, inplace=True)

plt.plot(df['Time'], df['Score'], 'ro')

plt.title('Start time vs Score')
plt.xlabel('Start Time')
plt.ylabel('Score')

print(df.head())

X = df.iloc[:, :-1].values  # all rows, all columns *except* last
y = df.iloc[:, 1].values  # all rows, only *second* column

regressor = LinearRegression()

regressor.fit(X, y)
slope = regressor.coef_
intercept = regressor.intercept_

regression_line = [(slope*x)+intercept for x in df['Time']]

plt.plot(df['Time'], regression_line)

print(regressor.intercept_)
print(regressor.coef_)

plt.show()
