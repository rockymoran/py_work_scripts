import requests
import login
import mimetypes
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from bs4 import BeautifulSoup
import pandas as pd

chrome_path = r"H:\documents\Work\chromedriver.exe"
driver = webdriver.Chrome(chrome_path)
xpath = driver.find_element_by_xpath
test_url = 'https://bcourses.berkeley.edu/courses/1477892'
report_url = 'https://bcsint.is.berkeley.edu/psc/bcsprd_7/EMPLOYEE', \
    '/SA/q/?ICAction=ICQryNameURL=PUBLIC.UCCS_G_COMMITTEE_BY_MEMBER'
file = r"C:\Users\rocky_moran\Downloads\Spring 2019.xlsx"


def wait(x):
    WebDriverWait(driver, 20).until(ec.element_to_be_clickable((By.XPATH, x)))
    return


# opens up a new chrome window and logs in to SIS. Must manually click 2-factor button and verify on phone
def SIS():
    login.login_sis(driver, xpath, wait)
    wait("""//*[@id="right-side"]/div[4]/a[1]""")
    return driver.get_cookies()


# Reads datafile with instructor UIDs into a dataframe.
df = pd.read_excel(file)
df.dropna(subset=['URL', 'Inst'], inplace=True)
log_file = r"""c:\Work\mentorship\log.txt"""


def get_report(row, session):
    path = r"C:\Work\mentorship"
    s = session
    c = s.get(report_url).text
    soup = BeautifulSoup(c, 'lxml')
    for link in soup.select('a[class*="instructure_file_link"]'):
        download_url = 'https://bcourses.berkeley.edu/' + link.get('href')
        r = s.get(download_url, allow_redirects=True)
        content_type = r.headers['content-type']
        extension = mimetypes.guess_extension(content_type)
        try:
            with open(path + row['Filename'] + extension, 'wb') as f:
                f.write(r.content)
                f.close()
                with open(log_file, "a+") as log:
                    log.write(str(row['CCN']) + "\t" + row['Filename'] + extension + "\r\n")
                    log.close()
        except TypeError:
            with open(log_file, "a+") as log:
                log.write(str(row['CCN']) + "\t" + row['Filename'] + "\tError" + "\r\n")
                log.close()
            pass


with requests.Session() as s:
    cookies = SIS()
    for cookie in cookies:
        s.cookies.set(cookie['name'], cookie['value'])
    driver.quit()
    df.apply(get_report, axis=1, args=(s,))
