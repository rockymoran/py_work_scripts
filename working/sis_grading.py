# enrollment control
# elements on enrollment control page (xpath)
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as ec
from working import sis_day_time

wait = sis_day_time.wait
xpath = sis_day_time.xpath
sis_search = sis_day_time.sis_search
save_record = sis_day_time.save_record
return_to_results = sis_day_time.return_to_results
frame_wait = sis_day_time.frame_wait
driver = sis_day_time.driver


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
sis_day_time.login.login_sis(driver, xpath, wait)


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
