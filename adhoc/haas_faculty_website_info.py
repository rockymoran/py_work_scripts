# uses haas faculty website to find each faculty's name, group, google scholar page

import pandas as pd
import requests
import re
from bs4 import BeautifulSoup

# this file should have the urls of each faculty member's Haas website
INPUT_FACULTY_FILE = r"C:\Work\haas_faculty_urls.txt"
OUTPUT_FILE = r"C:\Work\scholar_links.xlsx"

# url addition for google scholar to get all results and sorted by date
SCHOLAR_URL_APPEND = r"&pagesize=100&view_op=list_works&sortby=pubdate"

df = pd.read_csv(INPUT_FACULTY_FILE, header=None, names=["url"])


# for any given haas faculty url, goes to the site then looks for their name, their title (which has their group in
# it), and google scholar url.
def get_faculty_info(url):
    header = {'User-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                            'Chrome/64.0.3282.186 Safari/537.36'}
    page = requests.get(url, headers=header)
    soup = BeautifulSoup(page.content, 'html.parser')
    try:
        name = soup.find("h1", itemprop="name headline").text
    except AttributeError:
        name = ""
    try:
        title = soup.find("p", {"class": "intro-text"}).get_text(separator="\n")
    except AttributeError:
        title = ""
    # grab all of the links on the page, then find the first one that is a google scholar link. don't know of a
    # better way to do this, sadly. if it gets through all of them and none are found, sets scholar_link to blank.
    try:
        for link in soup.find_all('a'):
            if re.search(r"https:\/\/scholar.google.com\/citations", link['href']):
                scholar_link = link['href'] + SCHOLAR_URL_APPEND
                break
            scholar_link = ""
    except AttributeError:
        scholar_link = ""

    print("%s processed." % name)
    return name, title, scholar_link


# applies the get_faculty_info function to each row of the data file, then creates a new column result for name,
# title, scholar as they are found. (result_type ="expand" is key! "list-like results will be turned into columns")
df[["Name", "Title and Group", "Google Scholar"]] = df.apply(lambda x: get_faculty_info(x["url"]), axis=1,
                                                             result_type="expand")

df.to_excel(OUTPUT_FILE)
