import pandas as pd

# Checks current Haas Course Schedule with current Campus Solutions Course Schedule for discrepancies with day/time/room
# Compares using CCN/Course Nbr. Any course that does not have a CCN will not have a result.
# Result file should be visually checked for obvious reasons for discrepancies
# (e.g., campus room assignment or no times), then file can be ran using "sis_day_time.py" module to do data entry.
# use an "export to excel" file from course scheduling ("haas") - paste in location from file explorer "copy as path"
# and a "uccs_r_schd_extended" report from campus solutions ("campus")
# results will output to (and overwrite the contents of) c:\work\course_discrepancies.csv
#
haas = r"C:\Users\rocky_moran\Downloads\20190319_1303_Schedule.xlsx"
campus = r"C:\Users\rocky_moran\Downloads\UCCS_R_SCHD_EXTENDED_267175394.xlsx"
output = r'C:\work\course_discrepancies.csv'
output_columns = ["CCN", 'Days', 'StartT', 'EndT', 'Room']
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
Rm_split = haas_df['Rm'].str.split(n=0, expand=True)
time_split = Rm_split[1].str.split('-', n=0, expand=True)
haas_df['Days'] = Rm_split[0]
haas_df['StartT'] = time_split[0]
haas_df['EndT'] = time_split[1]
haas_df['Room'] = Rm_split[2]
haas_df['new_room'] = haas_df['Room'].map(room_list)
haas_df['StartT'] = pd.to_datetime(haas_df["StartT"]).dt.strftime("%I:%M%p")
haas_df['EndT'] = pd.to_datetime(haas_df["EndT"]).dt.strftime("%I:%M%p")
haas_df['haas_daytime'] = haas_df['Days'] + haas_df['StartT'] + haas_df['EndT'] + haas_df['new_room']

campus_df = pd.read_excel(campus, skiprows=1)
campus_df['Class Nbr'] = campus_df['Class Nbr'].astype(str)
campus_df['new_day'] = campus_df['Meeting Days (MTWRFSU)'].map(days_list)
campus_df['Start Time'] = pd.to_datetime(campus_df["Start Time"]).dt.strftime("%I:%M%p")
campus_df['End Time'] = pd.to_datetime(campus_df['End Time']) + pd.Timedelta(minutes=1)
campus_df['End Time'] = pd.to_datetime(campus_df["End Time"]).dt.strftime("%I:%M%p")
campus_df['campus_daytime'] = campus_df['new_day'] + campus_df['Start Time'] + campus_df['End Time'] + \
                              campus_df['Facility ID']

combine = pd.merge(haas_df, campus_df, left_on=['CCN'], right_on=["Class Nbr"])
combine = combine[(combine['haas_daytime'] != combine['campus_daytime'])]

print(combine.head())

combine.to_csv(output, columns=output_columns, index=False, sep='\t', header=None)



