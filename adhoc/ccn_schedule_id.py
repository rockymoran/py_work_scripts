import pandas as pd
import tkinter as tk
from tkinter import filedialog

# use an "export to excel" file from course scheduling and a "uccs_r_schd_extended" report from campus solutions
# results will output to (and overwrite the contents of) a file in c:\work\sched_id_import.csv
root = tk.Tk()
root.withdraw()

haas = filedialog.askopenfilename(title='Please select the Haas Course Scheduling "Export to Excel" file.',
                                  filetypes=[('Excel', '.xlsx')])
campus = filedialog.askopenfilename(title='Please select the SIS "UCCS_R_SCHD_EXTENDED" report from campus.',
                                    filetypes=[('Excel', '.xlsx')])
output = r'C:\work\sched_id_import.csv'
output_columns = ["Schedule_ID", "Class Nbr"]

haas_df = pd.read_excel(haas)
campus_df = pd.read_excel(campus, skiprows=1)


haas_df['search_course'] = haas_df['Course'].astype(str) + '.' + haas_df['Section'].astype(str)
campus_df['search_course'] = campus_df['Subject'].astype(str) + \
                             campus_df['Catalog Nbr'].astype(str) + '.' + campus_df['Section'].astype(str).str.lstrip('0')

results = haas_df.merge(campus_df, on='search_course')
results.to_csv(output, columns=output_columns, index=False, header=None)
