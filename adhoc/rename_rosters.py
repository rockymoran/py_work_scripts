# not working yet

import warnings
import os
import pandas as pd

path = r"""C:\Work\Scripting_Downloads\\"""
warnings.simplefilter("ignore")

def renameFiles():
    for filename in os.listdir(path):
        df = pd.read_excel(path + filename, skiprows=1)
        df['Term'] = df['Term'].astype("string")
        df['Subject'] = df['Subject'].astype("string")
        df['Ctlg Nbr Trim'] = df['Ctlg Nbr Trim'].astype("string")
        df['Class Nbr'] = df['Class Nbr'].astype("string")
        try:
            dst = df.loc[0, 'Term'] + df.loc[0, 'Subject'] + df.loc[0, 'Ctlg Nbr Trim'] + " " + df.loc[0, 'Class Nbr'] + " - " + filename
        except KeyError:
            dst = filename
        src = path + filename
        dst = path + dst
        os.rename(src, dst)


if __name__ == '__main__':
    renameFiles()
