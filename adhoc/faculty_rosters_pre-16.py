# use "faculty_grade_rosters.py" if data isn't prior to F16
# using a spreadsheet with CCN and Terms, this will download each course roster
# before running it the C:\Work\Scripting_Downloads directory must be empty (otherwise rename step will get all
# messed up). Script tests for that before running.

import time

from working import sis_day_time
from selenium.webdriver.support.ui import Select
import pandas as pd
import rename_rosters
import os
import re
import warnings
import os

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
report_url = """https://bcsint.is.berkeley.edu/psp/bcsprd/EMPLOYEE/SA/c/ESTABLISH_COURSES.CLASS_ROSTER.GBL?pts_Portal=
                EMPLOYEE&pts_PortalHostNode=SA&pts_Market=GBL&sesSrchTxt=roster&sesCrefID=undefined&cmd=uninav"""
faculty_file = r"""C:\Work\rosterCCNs.xlsx"""
cs_class_nbr = """//*[@id="CLASS_RSTR_SRCH_CLASS_NBR"]"""
cs_term = """//*[@id="CLASS_RSTR_SRCH_STRM"]"""
cs_roster_type = """//*[@id="InputKeys_GRADE_ROSTER_TYPE"]"""
results = """//*[@id="#ICSearch"]"""
dl_roster = """//*[@id="CLASS_ROSTER_VW$hexcel$0"]"""
course = """//*[@id="DERIVED_SSR_FC_SSR_CLASSNAME_LONG"]"""
roster_term = """//*[@id="DERIVED_SSR_FC_SSS_PAGE_KEYDESCR2"]"""


# load file of CCNs and Terms
df = pd.read_excel(faculty_file)
df['ccn'] = df['ccn'].astype("string")
df['term'] = df['term'].astype("string")

# go to report page
# search for ID number
# download file


def run_report(row):
    ccn = row['ccn']
    term = row['term']
    driver.get(report_url)
    frame_wait("ptifrmtgtframe")
    wait(cs_class_nbr)
    xpath(cs_class_nbr).clear()
    xpath(cs_class_nbr).send_keys(ccn)
    xpath(cs_term).send_keys(term)
    xpath(results).click()
    try:
        wait(dl_roster)
        xpath(dl_roster).click()
        filename = re.match(r""".+?(?=\|)""", xpath(roster_term).text).group(0) + xpath(course).text + ".xls"
        renameFile(filename)
    except:
        pass



def renameFile(filename):
    path = r"C:\Work\Scripting_Downloads"
    orig = r"\ps.xls"
    warnings.simplefilter("ignore")
    src = path + orig
    while True:
        try:
            f = open(src, 'r')
            f.close()
            break
        except:
            time.sleep(1)
    dst = path + "\\" + filename
    os.rename(src, dst)


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
        else:
            print("Directory is not empty. Remove files from " + rename_rosters.path + " and rerun.")
    else:
        print(rename_rosters.path + " directory doesn't exist")

