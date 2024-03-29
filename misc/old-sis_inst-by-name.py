import time
import csv
import traceback
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import NoSuchFrameException
from working import sis_day_time
from datetime import date

wait = sis_day_time.wait
xpath = sis_day_time.xpath
sis_search = sis_day_time.sis_search
NoSuchElementException = sis_day_time.NoSuchElementException
save_record = sis_day_time.save_record
return_to_results = sis_day_time.return_to_results
frame_wait = sis_day_time.frame_wait
driver = sis_day_time.driver
WebDriverWait = sis_day_time.WebDriverWait

# date for screen shot
today = date.today()
date = today.strftime("%b-%d-%Y")


class EmployeeSearch:
    # open instructor search window
    search_glass = """//*[@id="CLASS_INSTR_EMPLID$prompt$img$0"]"""
    search_lname = """//*[@id="UC_INSTR_VW2_LAST_NAME_SRCH"]"""
    search_fname = """//*[@id="UC_INSTR_VW2_FIRST_NAME_SRCH"]"""
    search_click = """//*[@id="#ICSearch"]"""
    first_result = """//*[@id="SEARCH_RESULT1"]"""
    search_cancel = """//*[@id="#ICCancel"]"""
    instructor_role_drop = """//*[@id="CLASS_INSTR_INSTR_ROLE$0"]"""
    proxy = "APRX"
    gsi = "TNIC"
    pri = "PI"
    access_drop = """//*[@id="CLASS_INSTR_GRADE_RSTR_ACCESS$0"]"""
    approve = "A"
    grade = "G"

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
        for check in range(99):
            try:
                driver.switch_to.frame("ptModFrame_" + str(check))
                break
            except NoSuchFrameException:
                pass
            except Exception:
                traceback.print_exc()
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
        select = Select(xpath(EmployeeSearch.access_drop))
        select.select_by_value(EmployeeSearch.approve)


# file format (instructor_discrepancies.csv)
# CCN   Last, First
# 19754 Miller, Conrad
# 19755 Walker, William

def main():
    file = r"C:\Work\instructor_discrepancies.csv"

    sis_day_time.login.login_sis(driver, xpath, wait)
    term = input("Which term? (e.g. 2278): ")
    driver.get("""https://bcsint.is.berkeley.edu/psp/bcsprd/EMPLOYEE/SA/c/ESTABLISH_COURSES.CLASS_DATA_SCTN.GBL""")
    frame_wait("ptifrmtgtframe")
    frame_count = 0
    with open(file) as csvfile:
        file = csv.reader(csvfile, delimiter='\t')
        for row in file:
            problem = 0  # using this to see when the thing is failing (so if it prints "CCN problem 3" then we know it
            # failed after changing instructor role
            try:
                ccn = row[0]
                instructor = EmployeeSearch(frame_count, row[1])
                sis_search(ccn, term)
                wait(instructor.search_glass)
                time.sleep(1)
                instructor.search_emp()
                problem += 1  # 1
                save_record()
                problem += 1  # 2
                instructor.role_change()
                problem += 1  # 3
                save_record()
                problem += 1  # 4
                driver.save_screenshot(r"C:\Work\selenium_screenshots\\" + ccn + "-" + term + "-" + date + ".png")
                problem += 1  # 5
                return_to_results()
                problem += 1  # 6
                print(ccn)
            except Exception:
                # traceback.print_exc()
                driver.get(
                    """https://bcsint.is.berkeley.edu/psp/bcsprd/EMPLOYEE/SA/c/ESTABLISH_COURSES.CLASS_DATA_SCTN.GBL""")
                frame_wait("ptifrmtgtframe")
                frame_count = 0
                print(ccn + " problem " + str(problem))
            wait("""//*[@id="#ICClear"]""")
            frame_count += 1
    driver.close()


if __name__ == "__main__":
    main()
