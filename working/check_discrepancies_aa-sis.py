import pandas as pd
import tkinter as tk
from tkinter import filedialog

# Checks current Haas Course Schedule with current Campus Solutions Course Schedule for discrepancies with day/time/room
# instructors and courses that are printed/print suppressed.
# Compares using CCN/Course Nbr. Any course that does not have a CCN will not have a result.
# Result file should be visually checked for obvious reasons for discrepancies
# (e.g., campus room assignment or no times), then file can be ran using "sis_day_time.py" module to do data entry.
# use an "export to excel" file from course scheduling ("haas") - paste in location from file explorer "copy as path"
# and a "uccs_r_schd_extended" report from campus solutions ("campus")
# results will output to (and overwrite the contents of):
# c:\work\course_discrepancies.csv
# c:\work\instructor_discrepancies.csv
# C:\work\print_discrepancies.csv
#

root = tk.Tk()
root.withdraw()

haas = filedialog.askopenfilename(title='Please select the Haas Course Scheduling "Export to Excel" file.',
                                  filetypes=[('Excel', '.xlsx')])
campus = filedialog.askopenfilename(title='Please select the SIS "uccs_r_schd_extended" report from campus.',
                                    filetypes=[('Excel', '.xlsx')])
output_room = r'C:\work\course_discrepancies.csv'
output_inst = r'C:\work\instructor_discrepancies.csv'
output_print = r'C:\work\print_discrepancies.csv'
output_rooms_columns = ["CCN", 'Days', 'StartT', 'EndT', 'Room']
output_inst_columns = ["CCN", "Instructor"]
output_print_suppress = ['Print Course', "Schedule Print"]

room_list = {
    "C110": "CHEIC110",
    "C125": "CHEIC125",
    "C132": "CHEIC132",
    "C135": "CHEIC135",
    "C138": "CHEIC138",
    "C210": "CHEIC210",
    "C220": "CHEIC220",
    "C230": "CHEIC230",
    "C250": "CHEIC250",
    "C320": "CHEIC320",
    "C325": "CHEIC325",
    "C330": "CHEIC330",
    "C335": "CHEIC335",
    "C337": "CHEIC337",
    "C420": "CHEIC420",
    "I": "STAD124",
    "N100": "CHOUN100",
    "N170": "CHOUN170",
    "N270": "CHOUN270",
    "N300": "CHOUN300",
    "N340": "CHOU340344",
    "N370": "CHOUN370",
    "N400": "CHOUN400",
    "N440": "CHOU440444",
    "N470": "CHOUN470",
    "N500": "CHOUN500",
    "N540": "CHOU540544",
    "N570": "CHOUN570",
    "I-Lab": "STAD124",
    "F295": "HAASF295",
    "I-Lab 124": "STAD124",
    "F320": "HAASF320",
    "F678": "HAASF678",
    "S300T": "HAASS300T"
}
days_list = {
    'M': "M",
    'T': "T",
    'W': "W",
    'R': "Th",
    'F': "F",
    'S': "S",
    'U': "Su",
    'MW': "MW",
    'TR': "TTh",
    'MWF': "MWF"
}


haas_df = pd.read_excel(haas)
haas_df['Schedule'] = haas_df['Schedule'].astype(str)
Rm_split = haas_df['Schedule'].str.split(n=0, expand=True)
Inst_split = haas_df['Instructor'].str.split(pat=',', n=1, expand=True)
time_split = Rm_split[1].str.split('-', n=0, expand=True)
haas_df['Days'] = Rm_split[0]
haas_df['StartT'] = time_split[0]
haas_df['EndT'] = time_split[1]
haas_df['Room'] = Rm_split[2]
haas_df['new_room'] = haas_df['Room'].map(room_list)
haas_df['StartT'] = pd.to_datetime(haas_df["StartT"]).dt.strftime("%I:%M%p")
haas_df['EndT'] = pd.to_datetime(haas_df["EndT"]).dt.strftime("%I:%M%p")
haas_df['haas_daytime'] = haas_df['Days'] + haas_df['StartT'] + haas_df['EndT'] + haas_df['new_room']
haas_df['haas_inst_lname'] = Inst_split[0]
haas_df['CCN'] = haas_df['CCN'].astype(str)

campus_df = pd.read_excel(campus, skiprows=1)
campus_df['Instructor Name'] = campus_df['Instructor Name'].astype(str)
Inst_split = campus_df['Instructor Name'].str.split(pat=',', n=1, expand=True)
campus_df['Class Nbr'] = campus_df['Class Nbr'].astype(str)
campus_df['new_day'] = campus_df['Meeting Days (MTWRFSU)'].map(days_list)
campus_df['Start Time'] = pd.to_datetime(campus_df["Start Time"]).dt.strftime("%I:%M%p")
campus_df['End Time'] = pd.to_datetime(campus_df['End Time']) + pd.Timedelta(minutes=1)
campus_df['End Time'] = pd.to_datetime(campus_df["End Time"]).dt.strftime("%I:%M%p")
campus_df['campus_daytime'] = campus_df['new_day'] + campus_df['Start Time'] + campus_df['End Time'] + \
                              campus_df['Facility ID']
campus_df['campus_inst_lname'] = Inst_split[0]
campus_df['Section'] = campus_df['Section'].apply(str)
campus_df['Print Course'] = campus_df["Subject"] + campus_df["Catalog Nbr"] + "." + campus_df["Section"]

combine = pd.merge(haas_df, campus_df, left_on=['CCN'], right_on=["Class Nbr"], indicator=True, how='outer')
combine_room = combine[(combine['haas_daytime'] != combine['campus_daytime']) & (combine['_merge'] == "both")]
combine_room = combine_room[output_rooms_columns].drop_duplicates()
combine_inst = combine[(combine['haas_inst_lname'] != combine['campus_inst_lname']) & (combine['_merge'] == "both")]
combine_inst = combine_inst[output_inst_columns].drop_duplicates()
combine_inst = combine_inst[(combine_inst['Instructor'] != 'TBD, Instructor') & (combine_inst['Instructor'] != 'TBD, GSI')].dropna()
combine_print = combine[((combine['Schedule Print'] == "N") & (combine['_merge'] == "both")) |
                        ((combine['Schedule Print'] == "Y") & (combine['_merge'] == "right_only"))]
combine_print = combine_print[output_print_suppress].drop_duplicates()

# print(combine_room)
# print(combine_inst)
# print(combine_print.columns)

combine_room.to_csv(output_room, index=False, sep='\t', header=None)
combine_inst.to_csv(output_inst, index=False, sep='\t', header=None)
combine_print.to_csv(output_print, index=False, sep='\t', header=None)
