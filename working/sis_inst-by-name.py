import time
import csv
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import NoSuchFrameException
from working import sis_day_time
# import re

wait = sis_day_time.wait
xpath = sis_day_time.xpath
sis_search = sis_day_time.sis_search
NoSuchElementException = sis_day_time.NoSuchElementException
save_record = sis_day_time.save_record
return_to_results = sis_day_time.return_to_results
frame_wait = sis_day_time.frame_wait
driver = sis_day_time.driver
WebDriverWait = sis_day_time.WebDriverWait


class EmployeeSearch:
    # open instructor search window
    search_glass = """//*[@id="CLASS_INSTR_EMPLID$prompt$img$0"]"""
    search_lname = """//*[@id="INSTR_ORG_DVW_LAST_NAME_SRCH"]"""
    search_fname = """//*[@id="INSTR_ORG_DVW_FIRST_NAME_SRCH"]"""
    search_click = """//*[@id="#ICSearch"]"""
    first_result = """//*[@id="RESULT14$0"]"""
    search_cancel = """//*[@id="#ICCancel"]"""
    instructor_role_drop = """//*[@id="CLASS_INSTR_INSTR_ROLE$0"]"""
    proxy = "APRX"
    gsi = "TNIC"
    pri = "PI"

    def __init__(self, frame_count, full_name, role=1):
        self.frame_count = frame_count
        self.last_name, self.first_name = full_name.split(",")
        self.search_last_name = ''.join(e for e in self.last_name if e.isalnum()).upper()
        self.search_first_name = ''.join(e for e in self.first_name if e.isalnum()).upper()
        self.role = role

    def search_emp(self):
        xpath(EmployeeSearch.search_glass).click()
        time.sleep(2)
        WebDriverWait(driver, 120).until(ec.invisibility_of_element_located((By.XPATH, """//*[@id="processing"]""")))
        driver.switch_to.parent_frame()
        try:
            driver.switch_to.frame("ptModFrame_0")
        except NoSuchFrameException:
            driver.switch_to.frame("ptModFrame_" + str(self.frame_count))
        wait(EmployeeSearch.search_lname)
        xpath(EmployeeSearch.search_lname).send_keys(self.search_last_name)
        xpath(EmployeeSearch.search_fname).send_keys(self.search_first_name)
        time.sleep(1)
        xpath(EmployeeSearch.search_click).click()
        WebDriverWait(driver, 120).until(ec.invisibility_of_element_located((By.XPATH, """//*[@id="processing"]""")))
        try:
            wait(EmployeeSearch.first_result)
            time.sleep(1)
            xpath(EmployeeSearch.first_result).click()
        except:
            wait(EmployeeSearch.search_cancel)
            time.sleep(1)
            xpath(EmployeeSearch.search_cancel).click()
            print("Not found.")
        frame_wait("ptifrmtgtframe")

    def role_change(self):
        # this is not working yet; manually change instructor role below from options defined above
        select = Select(xpath(EmployeeSearch.instructor_role_drop))
        select.select_by_value(EmployeeSearch.pri)


# file format
# CCN   Last, First
# 19754 Miller, Conrad
# 19755 Walker, William

def main():
    sis_day_time.login.login_sis(driver, xpath, wait)
    term = input("Which term? (e.g. 2278): ")
    frame_wait("ptifrmtgtframe")
    frame_count = 0
    with open(r"C:\Work\instructor_discrepancies.csv") as csvfile:
        file = csv.reader(csvfile, delimiter='\t')
        for row in file:
            ccn = row[0]
            instructor = EmployeeSearch(frame_count, row[1])
            sis_search(ccn, term)
            wait(instructor.search_glass)
            time.sleep(1)
            instructor.search_emp()
            save_record()
            instructor.role_change()
            save_record()
            return_to_results()
            wait("""//*[@id="#ICClear"]""")
            print(ccn)
            frame_count += 1


if __name__ == "__main__":
    main()
