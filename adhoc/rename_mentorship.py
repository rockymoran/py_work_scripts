# automatically used by SIS_mentorship.py

import os
import pandas as pd

path = """C:\Work\Scripting_Downloads\\"""


def renameFiles():
    for filename in os.listdir(path):
        df = pd.read_excel(path + filename, skiprows=1)
        try:
            dst = df.loc[1, 'Member Name'] + " - " + filename
        except KeyError:
            dst = filename
        src = path + filename
        dst = path + dst
        os.rename(src, dst)


if __name__ == '__main__':
    renameFiles()
