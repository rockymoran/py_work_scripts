# from list of courses, sets their topics number.
# uses "maintain schedule of classes" page
# searches for course, then finds individual CCN.
# once on ccn page, adds topics title. Note this uses the SHORT TITLE.
# loop through file records, adding tiers
# File format (topics_sis.txt):
# Semester  Subj    Num CCN     Topic title
# 2218      MBA	    207	40061   Edible Education
# 2218      MBA	    207	40066   Leader as Coach

import csv
import time
import traceback
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException, TimeoutException, InvalidElementStateException
from working import sis_day_time
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import NoSuchFrameException

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


def add_topic(ccn, t_id):
    while xpath("""//*[@id="CLASS_TBL_CLASS_NBR$0"]""").text != ccn:
        xpath("""//*[@id="$ICField21$hdown$0"]""").click()
        wait_processing()
    wait_processing()
    xpath("""//*[@id="CLASS_TBL_CRS_TOPIC_ID$67$$prompt$img$0"]""").click()
    wait_processing()
    time.sleep(2)
    driver.switch_to.parent_frame()
    for check in range(99):
        try:
            driver.switch_to.frame("ptModFrame_" + str(check))
            break
        except NoSuchFrameException:
            pass
        except Exception:
            traceback.print_exc()
    i = 0
    while i < 20:
        try:
            driver.find_element_by_link_text(t_id).click()
            result = "pass"
            break
        except NoSuchElementException:
            try:
                xpath("""//*[@id="#ICCancel"]""").click()
                result = "fail"
                break
            except NoSuchElementException:
                time.sleep(5)
                i += 1
                result = "timeout"
    wait_processing()
    frame_wait("ptifrmtgtframe")
    return result


def main():
    # load page
    sis_day_time.login.login_sis(driver, xpath, wait)
    input("Press enter to start")
    with open(r"C:\Work\topics_sis.txt") as csvfile:
        file = csv.reader(csvfile, delimiter='\t')
        for row in file:
            driver.get("""https://bcsint.is.berkeley.edu/psp/bcsprd/EMPLOYEE/SA/c/ESTABLISH_COURSES.CLASS_DATA.GBL""")
            frame_wait("ptifrmtgtframe")
            term, subject, course_number, ccn, t_id = row
            maintain_soc_search(subject, course_number, term)
            time.sleep(1)
            try:  # test whether search goes directly to results, or first record must be clicked
                wait("""//*[@id="CLASS_TBL_SESSION_CODE$0"]""")
            except TimeoutException:
                xpath("""//*[@id="SEARCH_RESULT1"]""").click()
                wait("""//*[@id="CLASS_TBL_SESSION_CODE$0"]""")
            result = add_topic(ccn, t_id)
            if result == "timeout":
                break
            else:
                save_record()
                return_to_results()
                wait("""//*[@id="#ICClear"]""")
            print_results = [term, subject, course_number, ccn, t_id, result]
            print(*print_results, sep='\t')  # Prints
            # completed CCN to
            # screen
    print("Complete")


if __name__ == "__main__":
    main()
