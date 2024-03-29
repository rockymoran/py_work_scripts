# using a spreadsheet with CCN and Terms, this will download each course roster
# before running it the C:\Work\Scripting_Downloads directory must be empty (otherwise rename step will get all
# messed up). Script tests for that before running.
# run "combine_excel.py" afterward if you want to put all of the data into one sheet. this step necessitates moving
# the fetched files into the work/temp directory.

from working import sis_day_time
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
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
download_dir = r"""C:\Work\Scripting_Downloads\\"""

# set script variables for urls and file locations
# for faculty_file, it requires columns named (case sensitive) "ccn" and "term"
# (term is in campus solutions format, eg 2228 for Fall 22)
report_url = """https://bcsint.is.berkeley.edu/psc/bcsprd_3/EMPLOYEE/SA/q/?ICAction=ICQryNameExcelURL=PUBLIC.UCCS_R_ROSTER_DETAIL"""
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
    select = Select(driver.find_element(By.XPATH, cs_roster_type))
    select.select_by_value("FIN")
    xpath(results).click()


def download_reports():
    sis_day_time.login.login_sis(driver, xpath, wait)
    wait("""//*[@id="PTSKEYWORD"]""")
    params = {'cmd': 'Page.setDownloadBehavior', 'params': {'behavior': 'allow', 'downloadPath': download_dir}}
    driver.command_executor._commands["send_command"] = ("POST", '/session/$sessionId/chromium/send_command')
    driver.execute("send_command", params)
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

