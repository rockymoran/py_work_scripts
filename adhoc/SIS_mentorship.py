# using a spreadsheet with CAMPUS SOLUTIONS ID number, this will download each faculty member's mentorship report
# before running it the C:\Work\Scripting_Downloads directory must be empty (otherwise rename step will get all
# messed up. Script tests for that before running.

from working import sis_day_time
import pandas as pd
import rename_mentorship
import os
import time

# various sis and selenium variables
wait = sis_day_time.wait
xpath = sis_day_time.xpath
frame_wait = sis_day_time.frame_wait
driver = sis_day_time.driver
WebDriverWait = sis_day_time.WebDriverWait

# set script variables for urls and file locations
# for faculty_file, it only requires a column named "SIS ID"
# this should be the SIS ID number of all of the ladder faculty members
# make sure to specify the sheet name in row 23
report_url = "https://bcsint.is.berkeley.edu/psc/bcsprd_1/EMPLOYEE/SA/q/" \
             "?ICAction=ICQryNameExcelURL=PUBLIC.UCCS_G_COMMITTEE_BY_MEMBER"
faculty_file = """C:\Work\ladder-phd-mentorship-test.xlsx"""
cs_search = """//*[@id="InputKeys_EMPLID"]"""
results = """//*[@id="#ICQryDownloadExcelFrmPrompt"]"""

# load file of SIS ID numbers
df = pd.read_excel(faculty_file, sheet_name='UID')

# go to report page
# search for ID number
# download file


def run_report(fac_id):
    driver.get(report_url)
    wait(cs_search)
    xpath(cs_search).send_keys(fac_id)
    xpath(results).click()


def download_reports():
    sis_day_time.login.login_sis(driver, xpath, wait)
    wait("""//*[@id="PTNUI_LAND_WRK_GROUPBOX14$PIMG"]/span""")
    df['SIS ID'].apply(run_report)


if __name__ == '__main__':
    if os.path.isdir(rename_mentorship.path):
        if not os.listdir(rename_mentorship.path):
            download_reports()
            time.sleep(5)
            rename_mentorship.renameFiles()
        else:
            print("Directory is not empty. Remove files from " + rename_mentorship.path + " and rerun.")
    else:
        print(rename_mentorship.path + " directory doesn't exist")

