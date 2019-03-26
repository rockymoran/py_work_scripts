import pandas as pd
import plotly.plotly as py
import plotly.figure_factory as ff

# input file
file = r"C:\Work\20190326_1107_Schedule.xlsx"

df = pd.read_excel(file)

print(df.head())
