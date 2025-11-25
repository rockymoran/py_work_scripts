# seems to work

import warnings
import os
import pandas as pd

path = r"""C:\Work\Scripting_Downloads\\"""
warnings.simplefilter("ignore")


def rename_files():
    filenames = os.listdir(path)
    for filename in filenames:
        # Process the file
        df = pd.read_excel(os.path.join(path, filename), skiprows=1)
        df['Term'] = df['Term'].astype("string")
        df['Subject'] = df['Subject'].astype("string")
        df['Catalog Nbr'] = df['Catalog Nbr'].astype("string")
        df['Class Nbr'] = df['Class Nbr'].astype("string")

        # Get the raw term string (e.g., "2212")
        try:
            raw_term = str(df.loc[0, 'Term'])
            # Parse Year: Skip the first char, take the next 2
            year_str = raw_term[1:3]

            # Parse Semester: Take the last char and map it
            sem_digit = raw_term[-1]
            sem_map = {
                '2': 'Spring',
                '5': 'Summer',
                '8': 'Fall'
            }
            sem_name = sem_map.get(sem_digit, "Unknown")

            # Create the new prefix (e.g., "21 Spring")
            readable_term = f"{year_str} {sem_name}"
        except KeyError:
            pass

        try:
            dst = readable_term + " " + df.loc[0, 'Subject'] + df.loc[0, 'Catalog Nbr'] + " " + df.loc[
                0, 'Class Nbr'] + " - ROSTER" + ".xlsx"
        except KeyError:
            dst = filename

        src = os.path.join(path, filename)
        dst = os.path.join(path, dst)

        # Rename the file
        os.rename(src, dst)


rename_files()
