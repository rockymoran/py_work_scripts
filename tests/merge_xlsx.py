import pandas as pd
import numpy as np
import glob

all_data = pd.DataFrame()
for f in glob.glob("C:\Work\omri\*.xlsx"):
    df = pd.read_excel(f, skiprows=1)
    all_data = all_data.append(df, ignore_index=True)

all_data.to_csv("C:\Work\omri\output.csv")

