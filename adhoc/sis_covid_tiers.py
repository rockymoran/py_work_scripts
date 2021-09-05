# from list of courses, sets their tier and instruction mode.
# uses "maintain schedule of classes" page
# searches for course, then finds individual CCN.
# once on ccn page, adds tier/instruction mode
# loop through file records, adding tiers
# File format:
# Subj  Num CCN
# MBA	207	40061
# MBA	207	40066

import csv
import time
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
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


def wait_processing():
    WebDriverWait(driver, 120).until(ec.invisibility_of_element_located((By.XPATH, """//*[@id="processing"]""")))


def url_wait(x):
    WebDriverWait(driver, 10).until(EC.url_to_be(x))
    return


def maintain_soc_search(w, x, y, z="UCB01"):
    xpath("""//*[@id="#ICClear"]""").click()
    time.sleep(1.5)
    xpath("""//*[@id="CLASS_TBL_SCTY_INSTITUTION"]""").send_keys(z)
    time.sleep(1.5)
    xpath("""//*[@id="CLASS_TBL_SCTY_STRM"]""").send_keys(y)
    time.sleep(1.5)
    xpath("""//*[@id="CLASS_TBL_SCTY_SUBJECT"]""").send_keys(w)
    time.sleep(1.5)
    xpath("""//*[@id="CLASS_TBL_SCTY_CATALOG_NBR"]""").send_keys(x)
    time.sleep(1.5)
    xpath("""//*[@id="#ICSearch"]""").click()
    return


def add_tier(x):
    while xpath("""//*[@id="CLASS_TBL_CLASS_NBR$0"]""").text != x:
        xpath("""//*[@id="$ICField21$hdown$0"]""").click()
        wait_processing()
    xpath("""//*[@id="CLASS_ATTRIBUTE$new$0$$0"]""").click()
    wait_processing()
    time.sleep(1.5)
    wait_processing()
    xpath("""//*[@id="CLASS_ATTRIBUTE_CRSE_ATTR$1"]""").send_keys("TPRO")
    xpath("""//*[@id="CLASS_ATTRIBUTE_CRSE_ATTR_VALUE$1"]""").click()
    time.sleep(1.5)
    xpath("""//*[@id="CLASS_ATTRIBUTE_CRSE_ATTR_VALUE$1"]""").send_keys("T2 FLEX")
    return


# load page
sis_day_time.login.login_sis(driver, xpath, wait)

# set semester, schedule print, ccn variable
term = input("Term (e.g., 2985): ")


with open(r"C:\Work\covid_tiers.txt") as csvfile:
    frame_wait("ptifrmtgtframe")
    file = csv.reader(csvfile, delimiter='\t')
    for row in file:
        subject = row[0]
        course_number = row[1]
        ccn = row[2]
        maintain_soc_search(subject, course_number, term)
        time.sleep(1)
        try:  # test whether search goes directly to results, or first record must be clicked
            wait("""//*[@id="CLASS_TBL_SESSION_CODE$0"]""")
        except TimeoutException:
            xpath("""//*[@id="SEARCH_RESULT1"]""").click()
            wait("""//*[@id="CLASS_TBL_SESSION_CODE$0"]""")
        add_tier(ccn)
        save_record()
        ccn = xpath("""//*[@id="CLASS_TBL_CLASS_NBR$0"]""").text
        return_to_results()
        wait("""//*[@id="#ICClear"]""")
        print(ccn.strip())  # Prints completed CCN to screen
print("Complete")


