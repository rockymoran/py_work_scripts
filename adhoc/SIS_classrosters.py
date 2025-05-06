from selenium import webdriver
from working import sis_day_time
import pandas as pd
from selenium.webdriver.support.ui import Select

# various sis and selenium variables
wait = sis_day_time.wait
xpath = sis_day_time.xpath
frame_wait = sis_day_time.frame_wait
driver = sis_day_time.driver
WebDriverWait = sis_day_time.WebDriverWait

# set script variables for urls and file locations
roster_url = """https://bcsint.is.berkeley.edu/psc/bcsprd_1/EMPLOYEE/SA/q/?ICAction=ICQryNameExcelURL=PUBLIC.UCCS_G_ENRL_BY_CLASS"""
ccn_term_file = """C:\Work\sem_ccn.xlsx"""
term_search = """//*[@id="InputKeys_STRM"]"""
email_type = """//*[@id="InputKeys_E_ADDR_TYPE"]"""
ccn_field = """//*[@id="InputKeys_CLASS_NBR"]"""
results = """//*[@id="#ICQryDownloadExcelFrmPrompt"]"""
subject_field = """//*[@id="InputKeys_SUBJECT"]"""


# load file of SIS ID numbers
df = pd.read_excel(ccn_term_file)

# go to roster page
# search for term and ccn
# download file
# log success or failure


def run_report(x):
    driver.get(roster_url)
    wait(term_search)
    select = Select(driver.find_element('id', 'InputKeys_E_ADDR_TYPE'))
    xpath(term_search).send_keys(str(x["term"]))
    xpath(subject_field).clear()
    xpath(subject_field).send_keys(str(x["prog"]))
    xpath(ccn_field).clear()
    xpath(ccn_field).send_keys(str(x["ccn"]))
    select.select_by_value('CAMP')
    xpath(results).click()


def main():
    sis_day_time.login.login_sis(driver, xpath, wait)
    wait("""//*[@id="win0hdrdivPT_TITLE_CONT"]""")
    # print(df.head())
    df.apply(run_report, axis=1)


if __name__ == '__main__':
    main()
