import time

import pandas as pd
import requests
from bs4 import BeautifulSoup

# this file should have the urls of each faculty member's google scholar page
INPUT_URL_FILE = r"C:\Work\scholar_links.xlsx"
OUTPUT_FILE = r"C:\Work\scholar_articles.xlsx"

SCHOLAR_BASE_URL = "https://scholar.google.com/"

df = pd.read_excel(INPUT_URL_FILE)

result_df = pd.DataFrame()

def find_articles(fname, surl):
    header = {'User-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                            'Chrome/64.0.3282.186 Safari/537.36'}
    page = requests.get(surl, headers=header)
    soup = BeautifulSoup(page.content, 'html.parser')
    rows = soup.findAll("tr", class_="gsc_a_tr")
    for row in rows:
        year = row.find("td", class_="gsc_a_y").text
        try:
            if int(year) > 2016:
                paper = row.find("a", class_="gsc_a_at").text
                paper_url = row.find("a", {'class': "gsc_a_at", 'href': True})['href']
                page = requests.get(SCHOLAR_BASE_URL + paper_url, headers=header)
                soup = BeautifulSoup(page.content, 'html.parser')
                table = soup.find("div", id='gsc_oci_table')
                divs = table.findAll("div", class_='gs_scl')
                return_dict = {}
                for div in divs:
                    label = div.find("div", class_="gsc_oci_field").text
                    value = div.find("div", class_="gsc_oci_value").text
                    return_dict[label] = value
                return_dict['Name'] = fname
                return_dict['Scholar Page'] = surl
                return_dict['Title'] = paper
                return_dict['Scholar Paper Link'] = paper_url
                return_dict['Year'] = year
                print(return_dict)
                result_df = result_df.append(return_dict, ignore_index=True)
                time.sleep(2)
        except ValueError:
            pass
        time.sleep(2)


result = [find_articles(x, y) for x, y in zip(df['Name'], df['Google Scholar'])]

result_df.to_excel(OUTPUT_FILE)

print(result)
