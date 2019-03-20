import pandas as pd

# use a "export to excel" file from course scheduling and a "uccs_r_schd_extended" report from campus solutions
# results will output to (and overwrite the contents of) a file in c:\work\sched_id_import.csv
haas = r'C:\Users\rocky_moran\Downloads\20190315_1315_Schedule.xlsx'
campus = r'C:\Users\rocky_moran\Downloads\UCCS_R_SCHD_EXTENDED_918891884.xlsx'
output = r'C:\work\sched_id_import.csv'
output_columns = ["schedule_ID", "Class Nbr"]

haas_df = pd.read_excel(haas)
campus_df = pd.read_excel(campus, skiprows=1)


haas_df['search_course'] = haas_df['Course'] + '.' + haas_df['Section']
campus_df['search_course'] = campus_df['Subject'] + \
                             campus_df['Catalog Nbr'] + '.' + campus_df['Section'].str.lstrip('0')

results = haas_df.merge(campus_df, on='search_course')
results.to_csv(output, columns=output_columns, index=False, header=None)
