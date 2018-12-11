import csv
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, WebDriverException

# load page
chrome_path = r"C:\Work\chromedriver.exe"
driver = webdriver.Chrome(chrome_path)
driver.maximize_window()
driver.get("""https://bcsint.is.berkeley.edu""")
xpath = driver.find_element_by_xpath


def wait(x):
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, x)))
    return


def frame_wait(x):
    WebDriverWait(driver, 50).until(EC.frame_to_be_available_and_switch_to_it(x))
    return


def url_wait(x):
    WebDriverWait(driver, 10).until(EC.url_to_be(x))
    return


def sis_search(x, y, z="UCB01"):
    xpath("""//*[@id="#ICClear"]""").click()
    time.sleep(1.5)
    xpath("""//*[@id="CLASS_SCTN_SCTY_INSTITUTION"]""").send_keys(z)
    time.sleep(1.5)
    xpath("""//*[@id="CLASS_SCTN_SCTY_STRM"]""").send_keys(y)
    time.sleep(1.5)
    xpath("""//*[@id="CLASS_SCTN_SCTY_CLASS_NBR"]""").send_keys(x)
    time.sleep(1.5)
    xpath("""//*[@id="#ICSearch"]""").click()
    return


def save_record():
    xpath("""//*[@id="#ICSave"]""").click()
    time.sleep(2)
    WebDriverWait(driver, 50).until(EC.invisibility_of_element_located((By.ID, "SAVED_win0")))
    return


def return_to_results():
    saving_error = False
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
        print(course.CCN + ": Error changing room.")
        saving_error = True
    try:
        elem = xpath("""//*[@id="#ALERTYES"]""")
        if elem.is_displayed():
            elem.click()
            wait("""//*[@id="#ICSave"]""")
            xpath("""//*[@id="#ICSave"]""").click()
    except NoSuchElementException:
        if not saving_error:
            print(course.CCN)
    return


def change_room(x):
    xpath("""//*[@id="CLASS_MTG_PAT_FACILITY_ID$0"]""").clear()
    xpath("""//*[@id="CLASS_MTG_PAT_FACILITY_ID$0"]""").send_keys(course.room)
    return


class Course:
    def __init__(self, ccn, room):
        self.CCN = ccn
        self.room = room


# set semester
term = input("Term (e.g., 2985): ")


with open(r"C:\Work\enter-rooms-sis-data.txt") as csvfile:
    frame_wait("ptifrmtgtframe")
    file = csv.reader(csvfile, delimiter='\t')
    for row in file:
        course = Course(row[0], row[1])
        sis_search(course.CCN, term)
        wait("""// *[ @ id = "CLASS_MTG_PAT_STND_MTG_PAT$0"]""")
        change_room(course.room)
        time.sleep(1)
        save_record()
        return_to_results()
        wait("""//*[@id="#ICClear"]""")
print("Complete")
