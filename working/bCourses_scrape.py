import requests
import login
import os.path
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
url_base = 'https://bcourses.berkeley.edu/'
file = r"C:\Users\rocky_moran\Downloads\Spring 2019.xlsx"


def wait(x):
    WebDriverWait(driver, 20).until(ec.element_to_be_clickable((By.XPATH, x)))
    return


# opens up a new chrome window and logs in to bCourses. Must manually click 2-factor button and verify on phone
def bCourses():
    login.login_bCourses(driver, xpath, wait)
    wait("""//*[@id="right-side"]/div[4]/a[1]""")
    return driver.get_cookies()


# Creates name of file using appropriate format:
# PROGRAM_NUMBERSUFFIX, Course Title_YR_Sem_Lname.pdf
# EWMBA_200S, Data & Decisions_16_Fall_Finan.pdf
# UGBA_C5, Introduction to Entrepreneurship_17_Spring_McDaniel.pdf
# Columns in DF:
# Course (needs to be broken with an _), Title, Inst (can have multiple records, will need to remove all but first)
# Semester and year set at runtime below
df = pd.read_excel(file)
df.dropna(subset=['URL', 'Inst'], inplace=True)
sem = 'Spring'
year = '19'
log_file = r"H:\documents\Work\syllabi\log.txt"


def create_course(course_number):
    programs = {'MBA': 'MBA_', 'PHDBA': 'PHDBA_', 'UGBA': 'UGBA_', 'MFE': 'MFE_'}
    course_number = course_number.upper()
    for key, value in programs.items():
        course_number = course_number.replace(key, value)
    return course_number


def separate_instructors(instructors):
    x = instructors.find(',')
    return instructors[:int(x)]


df['Course'] = df['Course'].apply(create_course)
df['Inst'] = df['Inst'].apply(separate_instructors)
df.loc[df['Working Title'].isnull() == False, 'Title'] = df['Working Title']
df['Filename'] = df['Course'] + ', ' + df['Title'] + '_' + year + '_' + sem + '_' + df['Inst']


def get_syllabus(row, session):
    path = r'H:\documents\Work\syllabi/'
    url_add = '/assignments/syllabus'
    s = session
    c = s.get(row['URL'] + url_add).text
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
    cookies = bCourses()
    for cookie in cookies:
        s.cookies.set(cookie['name'], cookie['value'])
    driver.quit()
    df.apply(get_syllabus, axis=1, args=(s,))
