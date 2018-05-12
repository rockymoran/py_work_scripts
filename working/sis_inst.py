import csv
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException, WebDriverException

#load page
chrome_path = r"C:\Work\chromedriver.exe"
driver = webdriver.Chrome(chrome_path)
driver.maximize_window()
driver.get("""https://bcsint.is.berkeley.edu""")
xpath = driver.find_element_by_xpath


def wait(x):
    WebDriverWait(driver,10).until(ec.element_to_be_clickable((By.XPATH, x)))
    return


def frame_wait(x):
    WebDriverWait(driver,50).until(ec.frame_to_be_available_and_switch_to_it(x))
    return


def urlwait(x):
    WebDriverWait(driver,10).until(ec.url_to_be(x))
    return


# set semester
term = input("Term (e.g., 2985): ")
institution = "UCB01"

frame_wait("ptifrmtgtframe")


def main():
    with open(r"C:\Work\enter-inst-sis-data.txt") as csvfile:
        file = csv.reader(csvfile, delimiter='\t')
        # log = open(r"C:\Work\log.txt", "w")
        for row in file:
            CCN_error = False
            CCN = row[0]
            instructor = row[1]
            xpath("""//*[@id="#ICClear"]""").click()
            time.sleep(1.5)
            xpath("""//*[@id="CLASS_SCTN_SCTY_INSTITUTION"]""").send_keys(institution)
            time.sleep(1.5)
            xpath("""//*[@id="CLASS_SCTN_SCTY_STRM"]""").send_keys(term)
            time.sleep(1.5)
            xpath("""//*[@id="CLASS_SCTN_SCTY_CLASS_NBR"]""").send_keys(CCN)
            time.sleep(1.5)
            xpath("""//*[@id="#ICSearch"]""").click()
            wait("""//*[@id="CLASS_INSTR_EMPLID$0"]""")
            time.sleep(1.5)
            xpath("""//*[@id="CLASS_INSTR_EMPLID$0"]""").clear()
            xpath("""//*[@id="CLASS_INSTR_EMPLID$0"]""").send_keys(instructor)
            time.sleep(1.5)
            xpath("""//*[@id="#ICSave"]""").click()
            time.sleep(2)
            element = WebDriverWait(driver, 50).until(ec.invisibility_of_element_located((By.ID, "SAVED_win0")))
            try:
                xpath("""//*[@id="#ICList"]""").click()
            except WebDriverException:
                time.sleep(1)
                driver.switch_to.parent_frame()
                wait("""//*[@id="#ICOK"]""")
                xpath("""//*[@id="#ICOK"]""").click()
                frame_wait("ptifrmtgtframe")
                wait("""//*[@id="#ICList"]""")
                xpath("""//*[@id="#ICList"]""").click()
                driver.switch_to.parent_frame()
                wait("""//*[@id="#ALERTNO"]""")
                xpath("""//*[@id="#ALERTNO"]""").click()
                frame_wait("ptifrmtgtframe")
                print(CCN + ": Instructor not found.")
                CCN_error = True
            try:
                elem = xpath("""//*[@id="#ALERTYES"]""")
                if elem.is_displayed():
                    elem.click()
                    wait("""//*[@id="#ICSave"]""")
                    xpath("""//*[@id="#ICSave"]""").click()
            except NoSuchElementException:
                pass
            wait("""//*[@id="#ICClear"]""")
            if not CCN_error:
                print(CCN)
    print("Complete")


if __name__ == "__main__":
    main()
