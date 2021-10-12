# make sure to change the year (right now running == 2016)
# make sure to backup old file if you still want old data!!
# sleeps five seconds before each faculty
# sleeps five seconds after each article.
# takes a long time to run, but this avoids being flagged as a bot.

import time
import pandas as pd
import requests
from bs4 import BeautifulSoup
from selenium import webdriver

# load page
chrome_path = r"C:\Work\chromedriver.exe"
driver = webdriver.Chrome(chrome_path)


# this file should have the urls of each faculty member's google scholar page
INPUT_URL_FILE = r"C:\Work\scholar_links.xlsx"
OUTPUT_FILE = r"C:\Work\scholar_articles.xlsx"
SCHOLAR_BASE_URL = r"https://scholar.google.com/"
TEMP_OUTPUT = r"C:\Work\scholar_articles_temp.xlsx"


def captcha(s, page):
    cookies = s.cookies.get_dict()
    for cookie in cookies:
        driver.add_cookie(cookie)
    captcha_url = page.url
    driver.get(captcha_url)
    input("Press enter once you've done the stupid fucking captcha...")
    cookies = driver.get_cookies()
    for cookie in cookies:
        s.cookies.set(cookie['name'], cookie['value'])
    driver.close()
    return s


def find_articles(fname, surl, results, s):
    time.sleep(5)
    header = {'User-agent': 'haas-scholar results bot'}
    page = s.get(surl, headers=header)
    print("Running for %s" % fname)
    print("Status code: %s" % page.status_code)
    if page.status_code == 429:
        print("Yikes, Status code: 429, captcha incoming...")
        s = captcha(s, page)
        page = s.get(surl, headers=header)
    soup = BeautifulSoup(page.content, 'html.parser')
    rows = soup.findAll("tr", class_="gsc_a_tr")
    for row in rows:
        year = row.find("td", class_="gsc_a_y").text
        try:
            if int(year) == 2016:
                paper = row.find("a", class_="gsc_a_at").text
                paper_url = row.find("a", {'class': "gsc_a_at", 'href': True})['href']
                page = s.get(SCHOLAR_BASE_URL + paper_url, headers=header)
                if page.status_code == 429:
                    s = captcha(s, page)
                    page = s.get(SCHOLAR_BASE_URL + paper_url, headers=header)
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
                results = results.append(return_dict, ignore_index=True)
                time.sleep(5)
        except ValueError:
            pass
    return results


url_df = pd.read_excel(INPUT_URL_FILE)
urls = url_df.values.tolist()
df = pd.DataFrame()
with requests.Session() as s:
    for url in urls:
        df = pd.read_excel(TEMP_OUTPUT)
        df = find_articles(url[0], url[1], df, s)
        df.to_excel(TEMP_OUTPUT, index=False)

df.to_excel(OUTPUT_FILE, index=False)
print(df)
