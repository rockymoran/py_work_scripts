import pandas as pd

# use a "export to excel" file from course scheduling
# exports a file with the following format:
# # file format
# # CCN   Days    StartT  EndT    Room
# # 01234 MW      12:30PM 2:00PM  C110
# # 01235 TTh     2:00PM  3:30PM  N300
# results will output to (and overwrite the contents of) a file in C:\Work\enter-days-sis-data.txt

haas = r"C:\Users\rocky_moran\Downloads\20190318_1307_Schedule.xlsx"
output = r"C:\work\enter-days-sis-data.txt"
output_columns = ["CCN", "Days", "StartT", "EndT", "Room"]
room_list = [
    "C110",
    "C125",
    "C132",
    "C135",
    "C138",
    "C210",
    "C220",
    "C230",
    "C250",
    "C320",
    "C325",
    "C330",
    "C335",
    "C337",
    "C420",
    "N100",
    "N170",
    "N270",
    "N300",
    "N340",
    "N370",
    "N400",
    "N440",
    "N470",
    "N500",
    "N540",
    "N570",
    "I-Lab",
    "F295",
    "F320",
    "F678",
    "S300T"
]

df = pd.read_excel(haas)

# Remove all rows where CCN is either TBD or blank
df = df[df.CCN.notnull()]
df = df[df.Rm.notnull()]
df.drop(df[(df.CCN == 'TBD')].index, inplace=True)


# Process Rm column
# ignore any 'second' rooms (just grab the first room assignment)
# split by space
# then split time column by '-'

Rm_split = df['Rm'].str.split(n=0, expand=True)
time_split = Rm_split[1].str.split('-', n=0, expand=True)
df['Days'] = Rm_split[0]
df['StartT'] = time_split[0]
df['EndT'] = time_split[1]
df['Room'] = Rm_split[2]

# Remove any column where 'Room' is not a Haas room.
df = df[df.Room.isin(room_list)]

df.to_csv(output, columns=output_columns, sep='\t', index=False, header=None)
