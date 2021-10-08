# ok, i don't remember whether this worked well or not (and this is the night after i wrote it
# i think it basically created a sheet that I had to massage in excel. but it did combine the files, so there's that.

# create empty df
# for files 1-26
#   create temp df
#   find "Semester Year Name Concat" value in sheet which will have YEAR SEM info
#   add YEAR SEM to be a column
#   append file to df

import pandas as pd
import re

master_columns = ['Course Subject Short Nm', 'Course Number', 'Instructor Name', 'Average Grade', 'Letter GradeA+',
                  'Letter GradeA', 'Letter GradeA-', 'Letter GradeB+', 'Letter GradeB', 'Letter GradeB-',
                  'Letter GradeC+', 'Letter GradeC', 'Letter GradeC-', 'Letter GradeD+', 'Letter GradeD',
                  'Letter GradeF', 'Letter Grade Total', 'Non-Letter GradePass', 'Non-Letter GradeSatisfactory',
                  'Non-Letter GradeNot Pass', 'Non-Letter GradeUnsatisfactory', 'Non-Letter Grade Total',
                  'Administrative CodeIncomplete', 'Administrative CodeIn Progress', 'Administrative CodeUnknown',
                  'Administrative Code Total', 'Semester', 'Letter GradeD-', 'Administrative CodeNot Reported',
                  'Administrative CodeMissing', 'Administrative CodeWithdrawn', 'UnknownUnknown', 'Unknown Total']

df = pd.DataFrame(columns=master_columns)
search_string = "Semester Year Name Concat"
INPUT_PATH_PRE = r"D:\Windows User Files\Downloads\Grade Distribution ("
INPUT_PATH_SUF = r").xlsx"
OUTPUT_PATH = r"c:\work\output_grades.xlsx"


for i in range(26):
    path = INPUT_PATH_PRE + str(i) + INPUT_PATH_SUF
    temp_df = pd.read_excel(path, skiprows=range(1, 2), header=2)
    #temp_df.columns = ["".join(a) for a in temp_df.columns.to_flat_index()]
    #temp_df = temp_df.reset_index()
    #temp_df = temp_df.rename(columns=lambda x: re.sub('(_*Unnamed: \d*_level_\d)', '', x))
    print(temp_df.columns)
    dog = temp_df.loc[temp_df['Course Number'].str.contains("Semester Year Name", case=False, na=False)]\
        ['Course Number'].values
    dog = dog.tolist()
    cat = ""
    cat = cat.join(dog).replace("Semester Year Name Concat is equal to ", "")
    temp_df['Semester'] = cat

    # the following commented out code was a way for me to iterate through all of the temp_dfs and get a list of every
    # column that exists so that I could make a master list (above as "master columns")

    # columns = temp_df.columns.tolist()
    # for column in columns:
    #     if column not in master_columns:
    #         master_columns.append(column)
    #         print(master_columns)
    for column in master_columns:
        if column not in temp_df.columns:
            temp_df[column] = '0'
    print(temp_df.columns)
    temp_df = temp_df.fillna(0)
    print("temp df columns %s" % temp_df.columns)
    print("perm df columns %s" % df.columns)
    df = pd.concat([df, temp_df], ignore_index=True)


print(df)
df.to_excel(OUTPUT_PATH)
