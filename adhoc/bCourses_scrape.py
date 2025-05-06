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
from working import sis_day_time

# Initialize Selenium components from shared module
wait = sis_day_time.wait
xpath = sis_day_time.xpath
driver = sis_day_time.driver
WebDriverWait = sis_day_time.WebDriverWait

# Configuration constants
test_url = 'https://bcourses.berkeley.edu/courses/1477892'
url_base = 'https://bcourses.berkeley.edu/'
file = r"C:\Work\bCourses-s25.xlsx"
sem = 'Spring'
year = '25'
log_file = r"C:\Work\syllabi\log.txt"


def bCourses():
    """Authenticate with bCourses and return session cookies"""
    login.login_bCourses(driver, xpath, wait)
    wait("""//*[@id="right-side"]/div[4]/a[1]""")
    return driver.get_cookies()


def get_dynamic_content(url):
    """Handle dynamic content interaction using Selenium"""
    driver.get(url)

    # NEW: Click syllabus expand button (adjust selector as needed)
    try:
        trigger = WebDriverWait(driver, 20).until(
            ec.element_to_be_clickable((By.CSS_SELECTOR, 'a.al-trigger'))
        )
        driver.execute_script("arguments[0].click();", trigger)
    except Exception as e:
        print(f"Trigger click failed: {str(e)}")

    # Wait for download link container (adjust selector as needed)
    WebDriverWait(driver, 10).until(
        ec.presence_of_element_located((By.CSS_SELECTOR, 'div.file-download-container'))
    )

    return driver.page_source


# MODIFIED: Data processing pipeline
df = pd.read_excel(file)
df.dropna(subset=['URL', 'Inst'], inplace=True)
df['Course'] = df['Course'].str.replace(r'(\D+)(\d+)', r'\1_\2', regex=True)  # Better course formatting
df['Inst'] = df['Inst'].str.split(',').str[0].str.strip()
df['Filename'] = df.apply(lambda x:
                          f"{x['Course']}, {x.get('Working Title', x['Title'])}_{year}_{sem}_{x['Inst']}",
                          axis=1
                          )


def get_syllabus(row, session):
    """MODIFIED: Uses Selenium-rendered content for link extraction"""
    path = r'C:\Work\syllabi/'

    try:
        # NEW: Get dynamically rendered content
        syllabus_url = f"{row['URL']}/assignments/syllabus"
        html_content = get_dynamic_content(syllabus_url)
        soup = BeautifulSoup(html_content, 'lxml')

        # NEW: Direct link extraction from rendered content
        link = soup.select_one('a.ui-corner-all[href*="download_frd=1"]')
        if not link:
            raise ValueError("Download link not found after dynamic load")

        download_url = link['href']  # Already contains full URL

        # Download file
        r = session.get(download_url, allow_redirects=True)
        content_type = r.headers.get('content-type', 'application/octet-stream')
        extension = mimetypes.guess_extension(content_type) or '.bin'

        # Save file
        full_path = os.path.join(path, f"{row['Filename']}{extension}")
        with open(full_path, 'wb') as f:
            f.write(r.content)

        # Log success
        with open(log_file, "a") as log:
            log.write(f"{row['CCN']}\t{full_path}\n")

    except Exception as e:
        # Log errors
        with open(log_file, "a") as log:
            log.write(f"{row['CCN']}\tERROR: {str(e)}\n")


# NEW: Structured execution flow
with requests.Session() as s:
    # Authenticate and transfer cookies
    cookies = bCourses()
    for cookie in cookies:
        s.cookies.set(cookie['name'], cookie['value'])

    # Process all records
    df.apply(get_syllabus, axis=1, args=(s,))

# Close browser after all processing
driver.quit()