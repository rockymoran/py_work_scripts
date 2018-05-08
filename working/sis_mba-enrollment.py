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


class EnrollmentControl:
    def __init__(self):
        # next section
        self.next_section = """//*[@id="$ICField3$hdown$0"]"""

        # next section inactive
        self.next_inactive = """//*[@id="win0div$ICField3GP$0"]/table/tbody/tr/td[2]/img[2]"""

        # next in list
        self.next_course = """//*[@id="#ICNextInList"]"""

        # enrollment cap
        self.cap = """//*[@id="CLASS_TBL_ENRL_CAP$0"]"""

        # add consent dropdown
        self.add_consent_drop = """//*[@id="CLASS_TBL_CONSENT$0"]"""

        # drop consent dropdown
        self.drop_consent_drop = """//*[@id="CLASS_TBL_SSR_DROP_CONSENT$0"]"""

    def change_enrollment(self):
        xpath(self.cap).clear()
        xpath(self.cap).send_keys("999")

    def change_consent(self):
        select = Select(xpath(self.add_consent_drop))
        select.select_by_value('D')
        select = Select(xpath(self.drop_consent_drop))
        select.select_by_value('N')


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
        input("Press enter to begin. ")
        setup = True
    enrollment = EnrollmentControl()
    frame_wait("ptifrmtgtframe")
    course_condition = True
    while course_condition:
        section_condition = True
        while section_condition:
            try:
                wait(enrollment.add_consent_drop)
                enrollment.change_enrollment()
                enrollment.change_consent()
                save_record()
                n += 1
            except StaleElementReferenceException:
                print("Timeout at " + str(xpath(""""//*[@id="CLASS_TBL_SCTY_CATALOG_NBR"]""").text))
                time.sleep(5)
            try:
                xpath(enrollment.next_section).click()
                time.sleep(2)
            except NoSuchElementException:
                section_condition = False
        course_condition = xpath(enrollment.next_course).is_enabled()
        xpath(enrollment.next_course).click()
    print("Changed " + str(n) + " records.")
    return


if __name__ == '__main__':
    main()
