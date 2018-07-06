# enrollment control
# elements on enrollment control page (xpath)
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import NoSuchElementException, TimeoutException, StaleElementReferenceException


def save_record():
    xpath("""//*[@id="#ICSave"]""").click()
    time.sleep(2)
    WebDriverWait(driver, 50).until(ec.invisibility_of_element_located((By.ID, "SAVED_win0")))
    return


def wait(x):
    WebDriverWait(driver, 10).until(ec.element_to_be_clickable((By.XPATH, x)))
    return


def frame_wait(x):
    WebDriverWait(driver, 50).until(ec.frame_to_be_available_and_switch_to_it(x))
    return


def url_wait(x):
    WebDriverWait(driver, 10).until(ec.url_to_be(x))
    return


class Meetings:
    def __init__(self):
        # next in list
        self.next_course = """//*[@id="#ICNextInList"]"""

        # grading access
        self.access = """//*[@id="CLASS_INSTR_GRADE_RSTR_ACCESS$0"]"""

    def change_access(self):
        select = Select(xpath(self.access))
        select.select_by_value('A') # (A)pprove or (G)rade

# load page
chrome_path = r"C:\Work\chromedriver.exe"
driver = webdriver.Chrome(chrome_path)
driver.maximize_window()
driver.get("""https://bcsint.is.berkeley.edu""")
xpath = driver.find_element_by_xpath


def main():
    n = 0
    setup = False
    while not setup:
        print("Campus Solutions -> Schedule Class Meetings -> [Search for term and program, go into first record] -> Meetings")
        input("Press enter to begin. ")
        setup = True
    grading = Meetings()
    frame_wait("ptifrmtgtframe")
    course_condition = True
    while course_condition:
        wait(grading.access)
        grading.change_access()
        time.sleep(2)
        n += 1
        save_record()
        course_condition = xpath(grading.next_course).is_enabled()
        xpath(grading.next_course).click()
        time.sleep(2)
    print("Changed " + str(n) + " records.")
    return


if __name__ == '__main__':
    main()
