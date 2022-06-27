# using a spreadsheet with CAMPUS SOLUTIONS ID number, this will download each faculty member's mentorship report
# before running it the C:\Work\Roster_Downloads directory must be empty (otherwise rename step will get all
# messed up. Script tests for that before running.

from working import sis_day_time
from selenium.webdriver.support.ui import Select
import pandas as pd
import rename_rosters
import os
import time

# various sis and selenium variables
wait = sis_day_time.wait
xpath = sis_day_time.xpath
frame_wait = sis_day_time.frame_wait
driver = sis_day_time.driver
WebDriverWait = sis_day_time.WebDriverWait

# set script variables for urls and file locations
# for faculty_file, it requires a column named "ccn" and "term"
# make sure to specify the sheet name in row 23
report_url = """https://bcsint.is.berkeley.edu/psc/bcsprd_3/EMPLOYEE/SA/q/
                ?ICAction=ICQryNameExcelURL=PUBLIC.UCCS_R_ROSTER_DETAIL"""
faculty_file = r"""C:\Work\rosterCCNs.xlsx"""
cs_search = """//*[@id="InputKeys_CLASS_NBR"]"""
cs_term = """//*[@id="InputKeys_STRM"]"""
cs_roster_type = """//*[@id="InputKeys_GRADE_ROSTER_TYPE"]"""
results = """//*[@id="#ICQryDownloadExcelFrmPrompt"]"""


# load file of CCNs and Terms
df = pd.read_excel(faculty_file)
df['ccn'] = df['ccn'].astype("string")
df['term'] = df['term'].astype("string")

# go to report page
# search for ID number
# download file


def run_report(row):
    ccn = row['ccn']
    driver.get(report_url)
    wait(cs_search)
    xpath(cs_search).clear()
    xpath(cs_search).send_keys(ccn)
    xpath(cs_term).send_keys(row['term'])
    select = Select(driver.find_element_by_xpath(cs_roster_type))
    select.select_by_value("FIN")
    xpath(results).click()


def download_reports():
    sis_day_time.login.login_sis(driver, xpath, wait)
    wait("""//*[@id="PTNUI_LAND_WRK_GROUPBOX14$PIMG"]/span""")
    df.apply(run_report, axis=1)


if __name__ == '__main__':
    if os.path.isdir(rename_rosters.path):
        if not os.listdir(rename_rosters.path):
            download_reports()
            time.sleep(5)
            rename_rosters.renameFiles()
        else:
            print("Directory is not empty. Remove files from " + rename_rosters.path + " and rerun.")
    else:
        print(rename_rosters.path + " directory doesn't exist")

