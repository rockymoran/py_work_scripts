from selenium import webdriver
from working import sis_day_time
import pandas as pd

# various sis and selenium variables
wait = sis_day_time.wait
xpath = sis_day_time.xpath
frame_wait = sis_day_time.frame_wait
driver = sis_day_time.driver
WebDriverWait = sis_day_time.WebDriverWait

# set script variables for urls and file locations
report_url = "https://bcsint.is.berkeley.edu/psc/bcsprd_1/EMPLOYEE/SA/q/" \
             "?ICAction=ICQryNameExcelURL=PUBLIC.UCCS_G_COMMITTEE_BY_MEMBER"
faculty_file = """C:\Work\ladder-phd-mentorship.xlsx"""
cs_search = """//*[@id="InputKeys_EMPLID"]"""
results = """//*[@id="#ICQryDownloadExcelFrmPrompt"]"""

# load file of SIS ID numbers
df = pd.read_excel(faculty_file, sheet_name='Ladder')

# go to report page
# search for ID number
# download file
# log success or failure


def run_report(fac_id):
    driver.get(report_url)
    wait(cs_search)
    xpath(cs_search).send_keys(fac_id)
    xpath(results).click()


def main():
    sis_day_time.login.login_sis(driver, xpath, wait)
    wait("""//*[@id="PTNUI_LAND_WRK_GROUPBOX14$PIMG"]/span""")
    df['SIS ID'].apply(run_report)


if __name__ == '__main__':
    main()
