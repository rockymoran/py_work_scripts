import pandas as pd

file = r"C:\Users\rocky_moran\Downloads\EvalDatesByInstructor Spring 2019 (3).xlsx"

df = pd.read_excel(file)
df = df.join(df.CourseEvalDates.str.split(';', expand=True)
                                             .stack().reset_index(drop=True, level=1).rename('NewCourseEvalDates'))
df.reset_index(inplace=True, drop=True)
df['Course'], df['Date'] = df['NewCourseEvalDates'].str.split(':', 1).str
df = df[(df['NewCourseEvalDates'].str.contains('/') == True)]
df = df[(df['Date'].str.contains('-') == False)]
df.reset_index(inplace=True, drop=True)
df['Date'] = pd.to_datetime(df.Date, infer_datetime_format=True)
print(df)
