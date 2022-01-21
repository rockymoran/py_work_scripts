import csv
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, WebDriverException, TimeoutException

# load page
chrome_path = r"C:\Work\chromedriver.exe"
driver = webdriver.Chrome(chrome_path)
# driver.maximize_window()
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
    room_list = {
        "C110": "CHEIC110",
        "C125": "CHEIC125",
        "C132": "CHEIC132",
        "C135": "CHEIC135",
        "C138": "CHEIC138",
        "C210": "CHEIC210",
        "C220": "CHEIC220",
        "C230": "CHEIC230",
        "C250": "CHEIC250",
        "C320": "CHEIC320",
        "C325": "CHEIC325",
        "C330": "CHEIC330",
        "C335": "CHEIC335",
        "C337": "CHEIC337",
        "C420": "CHEIC420",
        "I": "STAD124",
        "N100": "CHOUN100",
        "N170": "CHOUN170",
        "N270": "CHOUN270",
        "N300": "CHOUN300",
        "N340": "CHOU340344",
        "N370": "CHOUN370",
        "N400": "CHOUN400",
        "N440": "CHOU440444",
        "N470": "CHOUN470",
        "N500": "CHOUN500",
        "N540": "CHOU540544",
        "N570": "CHOUN570",
        "I-Lab": "STAD124",
        "F295": "HAASF295",
        "I-Lab 124": "STAD124",
        "F320": "HAASF320",
        "F678": "HAASF678",
        "S300T": "HAASS300T"
    }
    xpath("""//*[@id="CLASS_MTG_PAT_FACILITY_ID$0"]""").clear()
    xpath("""//*[@id="CLASS_MTG_PAT_FACILITY_ID$0"]""").send_keys(room_list.get(x, ""))
    return


class Course:
    def __init__(self, ccn, room):
        self.CCN = ccn
        self.room = room


# set semester
term = input("Term (e.g., 2985): ")

# format
# ccn     room (use course scheduling room values--algorithm will translate to SIS values)
# 01234     n270


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
        try:
            wait("""//*[@id="#ICClear"]""")
        except TimeoutException:
            driver.get(
                """https://bcsint.is.berkeley.edu/psp/bcsprd/EMPLOYEE/SA/c/ESTABLISH_COURSES.CLASS_DATA_SCTN.GBL""")
            frame_wait("ptifrmtgtframe")
            wait("""//*[@id="#ICClear"]""")
            print("Loading error on above record.")

print("Complete")
