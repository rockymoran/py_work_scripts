# uses haas faculty website to find each faculty's name, education

import pandas as pd
import requests
import re
from bs4 import BeautifulSoup
import csv

# this file should have the urls of each faculty member's Haas website
INPUT_FACULTY_FILE = r"C:\Work\haas_faculty_urls.txt"
OUTPUT_FILE = r"C:\Work\fac_education.xlsx"

columns = ['Berkeley_ID', 'Employee_Name', 'Institution', 'Location', 'Major', 'Degree']

# df = pd.read_csv(INPUT_FACULTY_FILE, header=None, names=["url"])
df = pd.DataFrame(columns=columns)


# for any given haas faculty url, goes to the site then looks for the education field and copies the contents.
def get_faculty_education(url, df):
    header = {'User-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                            'Chrome/64.0.3282.186 Safari/537.36'}
    page = requests.get(url, headers=header)
    soup = BeautifulSoup(page.content, 'html.parser')
    try:
        name = soup.find("h1", itemprop="name headline").text
    except AttributeError:
        name = ""
    try:
        div_contents = soup.find('h2', text='Education').findParent()
        lis = div_contents.findAll("li")
        for li in lis:
            new_row = {'Employee_Name': name, "Education": li.text, "URL": url}
            df = df.append(new_row, ignore_index=True)
    except AttributeError:
        pass

    print("%s processed." % name)
    return df


def stripper(text):
    fields = text.split(",")
    return_series = pd.Series(fields)
    if return_series.size == 3:
        return return_series
    else:
        return text, "", ""


# goes through file and creates a row in dataframe for each education record
with open(INPUT_FACULTY_FILE) as csvfile:
    file = csv.reader(csvfile)
    for row in file:
        url = row[0]
        df = get_faculty_education(url, df)

df[['Degree', 'Major', 'Institution']] = df.apply(lambda x: stripper(x["Education"]), axis=1)

strip_columns = ['Degree', 'Major', 'Institution']
for column in strip_columns:
    df[column] = df[column].str.strip()

print(df)
df.to_excel(OUTPUT_FILE, columns=columns, index=False)
