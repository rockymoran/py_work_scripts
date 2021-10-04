from openpyxl import load_workbook
import pandas as pd
import requests
import re
from bs4 import BeautifulSoup


SEARCH_URL = r"https://scholar.google.com/citations?hl=en&view_op=search_authors&mauthors="
# use file created by haas_faculty_website_info, manually create "Sheet2" with just the names of people that don't
# have a scholar url in Sheet1
FACULTY_FILE = r"C:\Work\scholar_links.xlsx"

df = pd.read_excel(FACULTY_FILE, sheet_name="Sheet2")


def search_scholar(name):
    link = "Not found"
    header = {'User-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                            'Chrome/64.0.3282.186 Safari/537.36'}
    name = re.sub(r"[().]", "", name)
    name = re.sub(r"[\s]", "+", name)
    url = SEARCH_URL + name
    page = requests.get(url, headers=header)
    soup = BeautifulSoup(page.content, 'html.parser')
    users = soup.findAll("div", {"class": "gsc_1usr"})
    for user in users:
        if user(text=lambda t: "Berkeley" in t):
            link = user.select_one('a', {"class": "gs_ai_pho"})['href']
            print(link)
            break
    return link


df["Matches"] = df.apply(lambda x: search_scholar(x["Name"]), axis=1)

with pd.ExcelWriter(FACULTY_FILE, engine='openpyxl') as writer:
    writer.book = load_workbook(FACULTY_FILE)
    df.to_excel(writer, "Search_Results")
