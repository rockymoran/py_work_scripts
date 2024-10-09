# sets instructors on courses in the sis
# note it will remove existing instructors if multiple are present, so do not use just to add one name
# instead make sure ALL names are on each row (separated by semicolons)

import time
import csv
import traceback
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import NoSuchFrameException, TimeoutException
from working import sis_day_time
from datetime import date
import logging

logging.basicConfig(level=logging.WARNING)
logging.getLogger("selenium.webdriver.remote.remote_connection").disabled = True
logging.getLogger("urllib3.connectionpool").disabled = True


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

# thing to wait for on inst page (indicating we are in the results)
add_inst = """//*[@id="CLASS_INSTR$new$0$$0"]"""


def search_emp(instructor, list_pos):
    add_inst = """//*[@id="CLASS_INSTR$new$0$$0"]"""
    id_box_pre = """//*[@id="CLASS_INSTR_EMPLID$"""
    id_box_suf = """"]"""
    search_glass_pre = """//*[@id="CLASS_INSTR_EMPLID$prompt$img$"""
    search_glass_suf = """"]"""
    search_glass = search_glass_pre + str(0) + search_glass_suf
    search_lname = """//*[@id="UC_INSTR_VW2_LAST_NAME_SRCH"]"""
    search_fname = """//*[@id="UC_INSTR_VW2_FIRST_NAME_SRCH"]"""
    search_click = """//*[@id="#ICSearch"]"""
    first_result = """//*[@id="SEARCH_RESULT1"]"""
    search_cancel = """//*[@id="#ICCancel"]"""

    last_name, first_name = instructor.split(",")
    search_last_name = ''.join(e for e in last_name if e.isalnum()).upper()
    search_first_name = ''.join(e for e in first_name if e.isalnum()).upper()

    position_entered = 0

    # if this is the first instructor being added to a CCN, delete all others
    if list_pos == 0:  # only do this for the first instructor on a course
        # check if multiple instructors exist on the course record
        while True:
            try:
                xpath("""//*[@id="CLASS_INSTR$delete$1$$0"]""").click()
            except NoSuchElementException:
                logging.debug('NoSuchElementException found while deleting instructors')
                break
            time.sleep(1)
            WebDriverWait(driver, 120).until(
                ec.invisibility_of_element_located((By.XPATH, """//*[@id="processing"]""")))
            driver.switch_to.parent_frame()
            logging.debug('switched frame')
            wait("""//*[@id="#ALERTOK"]""")
            xpath("""//*[@id="#ALERTOK"]""").click()
            logging.debug('clicked ok')
            time.sleep(1)
            WebDriverWait(driver, 120).until(
                ec.invisibility_of_element_located((By.XPATH, """//*[@id="processing"]""")))
            time.sleep(1)
            frame_wait("ptifrmtgtframe")
            logging.debug('found main frame again')


    # if this isn't the first instructor for the course, click "add inst" button.
    # then find an empty instructor box and check its id
    # use that box's id ("position_entered") as the one you're entering data into--prevent from overwriting
    # instructors
    logging.debug('deleted instructors or not first instructor')
    logging.debug('now adding new instructors')
    if list_pos > 0:
        logging.debug('not first instructor in list - adding fields')
        xpath(add_inst).click()
        time.sleep(2)
        for i in range(list_pos + 1):
            try:
                xpath("""//*[@id="CLASS_INSTR$hviewall$0"]""").click()
                time.sleep(1)
            except:
                pass
            search_box = id_box_pre + str(i) + id_box_suf
            inst_value = xpath(search_box).get_attribute("Value")
            inst_value = inst_value[:]
            if inst_value == "":
                position_entered = i
                search_glass = search_glass_pre + str(position_entered) + search_glass_suf
                break
    xpath(search_glass).click()
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
    wait(search_lname)
    xpath(search_lname).send_keys(search_last_name)
    xpath(search_fname).send_keys(search_first_name)
    time.sleep(1)
    xpath(search_click).click()
    WebDriverWait(driver, 120).until(ec.invisibility_of_element_located((By.XPATH, """//*[@id="processing"]""")))
    try:
        wait(first_result)
        time.sleep(1)
        xpath(first_result).click()
        success = True
    except:
        wait(search_cancel)
        time.sleep(1)
        xpath(search_cancel).click()
        success = False
    logging.debug('search done waiting for frame')
    try:
        frame_wait("ptifrmtgtframe")
    except TimeoutException:
        driver.switch_to.parent_frame()
        frame_wait("ptifrmtgtframe")
    logging.debug('frame found')
    return position_entered, success


def role_change(which_box, role="PI"):
    # this is not working yet; manually change instructor role below from options defined below
    approval = {
        "PI": "A",  # primary instructor, approve grades
        "TNIC": "G",  # gsi/reader, enter grades
        "APRX": "A",  # admin proxy, enter grades
        }

    access_drop_pre = """//*[@id="CLASS_INSTR_GRADE_RSTR_ACCESS$"""
    access_drop_suf = """"]"""

    instructor_role_drop_pre = """//*[@id="CLASS_INSTR_INSTR_ROLE$"""
    instructor_role_drop_suf = """"]"""

    access_drop = access_drop_pre + str(which_box) + access_drop_suf
    instructor_role_drop = instructor_role_drop_pre + str(which_box) + instructor_role_drop_suf

    select = Select(xpath(instructor_role_drop))
    select.select_by_value(role)
    select = Select(xpath(access_drop))
    select.select_by_value(approval[role])


# file format (instructor_discrepancies.csv)
# CCN   Last, First
# 19754 Miller, Conrad
# 19755 Walker, William; Dal Bo, Ernesto

def main():
    file = r"C:\Work\instructor_discrepancies.csv"

    sis_day_time.login.login_sis(driver, xpath, wait)
    term = input("Which term? (e.g. 2278): ")
    driver.get("""https://bcsint.is.berkeley.edu/psp/bcsprd/EMPLOYEE/SA/c/ESTABLISH_COURSES.CLASS_DATA_SCTN.GBL""")
    frame_wait("ptifrmtgtframe")
    with open(file) as csvfile:
        file = csv.reader(csvfile, delimiter='\t')
        for row in file:
            problem = 0  # using this to see when the thing is failing (so if it prints "CCN problem 3" then we know it
            # failed after changing instructor role
            ccn = row[0]
            faculty_list = row[1].split(";")
            try:  # if role is in file, use it
                role = row[2].upper()
                if role == '':
                    role = "PI"
            except IndexError:  # otherwise default to primary instructor
                role = "PI"
            for i, faculty in enumerate(faculty_list):
                faculty = faculty.strip()
                try:
                    sis_search(ccn, term)
                    wait(add_inst)
                    time.sleep(1)

                    entered, success = search_emp(faculty, i)
                    problem += 1  # 1
                    save_record()
                    problem += 1  # 2
                    if success:
                        role_change(entered, role)
                        problem += 1  # 3
                        save_record()
                        problem += 1  # 4
                        driver.save_screenshot(r"C:\Work\selenium_screenshots\\" + ccn + "-" + term + "-" + date + ".png")
                        problem += 1  # 5
                    return_to_results()
                    problem += 1  # 6
                    if success:
                        print("%s - %s success" % (ccn, faculty))
                    else:
                        print("%s - %s failed" % (ccn, faculty))
                except Exception as e:
                    print(e)
                    driver.get(
                        """https://bcsint.is.berkeley.edu/psp/bcsprd/EMPLOYEE/SA/c/ESTABLISH_COURSES.CLASS_DATA_SCTN.GBL""")
                    frame_wait("ptifrmtgtframe")
                    print(ccn + " problem " + str(problem))
                wait("""//*[@id="PTS_CFG_CL_WRK_PTS_SRCH_CLEAR"]""")
    driver.close()


if __name__ == "__main__":
    main()
