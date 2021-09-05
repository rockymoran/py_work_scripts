import csv
import time
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException, InvalidElementStateException
from working import sis_day_time

wait = sis_day_time.wait
xpath = sis_day_time.xpath
sis_search = sis_day_time.sis_search
save_record = sis_day_time.save_record
return_to_results = sis_day_time.return_to_results
frame_wait = sis_day_time.frame_wait
driver = sis_day_time.driver
WebDriverWait = sis_day_time.WebDriverWait


def url_wait(x):
    WebDriverWait(driver, 10).until(EC.url_to_be(x))
    return


def addnew_search(w, x, y, z="UCB01"):
    xpath("""//*[@id="#ICClear"]""").click()
    time.sleep(1.5)
    xpath("""//*[@id="CRSE_OFFER_SCTY_INSTITUTION"]""").send_keys(z)
    time.sleep(1.5)
    xpath("""//*[@id="CRSE_OFFER_SCTY_STRM"]""").send_keys(y)
    time.sleep(1.5)
    xpath("""//*[@id="CRSE_OFFER_SCTY_SUBJECT"]""").send_keys(w)
    time.sleep(1.5)
    xpath("""//*[@id="CRSE_OFFER_SCTY_CATALOG_NBR"]""").send_keys(x)
    time.sleep(1.5)
    xpath("""//*[@id="#ICSearch"]""").click()
    return


def section_info(x):
    y = x
    if xpath("""//*[@id="CLASS_TBL_CLASS_NBR$0"]""").text != "0":
        xpath("""//*[@id="$ICField21$new$0$$0"]""").click()
        wait("""//*[@id="CLASS_TBL_EMPLID$prompt$img$0"]""")
    while len(y) < 3:
        y = "0" + y
    xpath("""//*[@id="CLASS_TBL_CLASS_SECTION$0"]""").send_keys(y)
    try:
        xpath("""//*[@id="CLASS_TBL_ASSOCIATED_CLASS$0"]""").clear()
        xpath("""//*[@id="CLASS_TBL_ASSOCIATED_CLASS$0"]""").send_keys(re.sub("\D", "", x))
    except InvalidElementStateException:
        pass
    return


def schedule_print(x):
    time.sleep(1)
    if x == 2:
        if xpath("""//*[@id="CLASS_TBL_SCHEDULE_PRINT$0"]""").is_selected():
            xpath("""//*[@id="CLASS_TBL_SCHEDULE_PRINT$0"]""").click()
    return


# load page
sis_day_time.login.login_sis(driver, xpath, wait)

# set semester, schedule print, ccn variable
term = input("Term (e.g., 2985): ")
s_print = 3
while s_print > 2:
    s_print = int(input("Should records print in campus schedule? (1 = yes, 2 = no): "))
ccn = ''

# loop through file records, adding sections
# File format:
# Subj  Num Sec SID
# MBA	207	1B	40061
# MBA	207	2B	40066
with open(r"C:\Work\new-section-sis-data.txt") as csvfile:
    frame_wait("ptifrmtgtframe")
    file = csv.reader(csvfile, delimiter='\t')
    for row in file:
        subject = row[0]
        course_number = row[1]
        section = row[2]
        sid = row[3]
        addnew_search(subject, course_number, term)
        time.sleep(1)
        try:  # test whether search goes directly to results, or first record must be clicked
            wait("""//*[@id="CLASS_TBL_SESSION_CODE$0"]""")
        except TimeoutException:
            xpath("""//*[@id="SEARCH_RESULT1"]""").click()
            wait("""//*[@id="CLASS_TBL_SESSION_CODE$0"]""")
        section_info(section)
        save_record()
        schedule_print(s_print)
        save_record()
        ccn = xpath("""//*[@id="CLASS_TBL_CLASS_NBR$0"]""").text
        return_to_results()
        wait("""//*[@id="#ICClear"]""")
        print(str(sid).strip(), ",", ccn.strip(), sep='')  # Prints results to screen for pasting into CSV and import.
print("Complete")


