import pandas as pd
import plotly.plotly as py
import plotly.figure_factory as ff

# input file
file = r"C:\work\20190323_1317_Schedule.xlsx"

df = pd.read_excel(file)

print(df.head())
