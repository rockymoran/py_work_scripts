# enrollment control
# elements on enrollment control page (xpath)
import time, csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import NoSuchElementException
from working import sis_day_time

wait = sis_day_time.wait
xpath = sis_day_time.xpath
sis_search = sis_day_time.sis_search
save_record = sis_day_time.save_record
return_to_results = sis_day_time.return_to_results
frame_wait = sis_day_time.frame_wait
driver = sis_day_time.driver
WebDriverWait = sis_day_time.WebDriverWait



def url_wait(x):
    WebDriverWait(driver, 10).until(ec.url_to_be(x))
    return


class Meetings:
    def __init__(self):
        # loading image
        self.loading = """//*[@id="processing"]"""

        # next section
        self.next_section = """//*[@id="$ICField4$hdown$0"]"""

        # next in list
        self.next_course = """//*[@id="#ICNextInList"]"""

        # room field
        self.facility = """//*[@id="CLASS_MTG_PAT_FACILITY_ID$0"]"""

        # meeting pattern field
        self.pattern = """//*[@id="CLASS_MTG_PAT_STND_MTG_PAT$0"]"""

        # meeting start time
        self.mtg_start = """//*[@id="CLASS_MTG_PAT_MEETING_TIME_START$0"]"""

        # meeting end time
        self.mtg_end = """//*[@id="CLASS_MTG_PAT_MEETING_TIME_END$0"]"""

        # days
        self.monday = """// *[ @ id = "CLASS_MTG_PAT_MON$0"]"""
        self.tuesday = """// *[ @ id = "CLASS_MTG_PAT_TUES$0"]"""
        self.wednesday = """// *[ @ id = "CLASS_MTG_PAT_WED$0"]"""
        self.thursday = """// *[ @ id = "CLASS_MTG_PAT_THURS$0"]"""
        self.friday = """// *[ @ id = "CLASS_MTG_PAT_FRI$0"]"""
        self.saturday = """// *[ @ id = "CLASS_MTG_PAT_SAT$0"]"""
        self.sunday = """// *[ @ id = "CLASS_MTG_PAT_SUN$0"]"""

        # course info
        self.course = """//*[@id="CLASS_TBL_SCTY_CATALOG_NBR"]"""
        self.section = """//*[@id="CLASS_TBL_CLASS_SECTION$0"]"""
        self.ccn = """//*[@id="CLASS_TBL_CLASS_NBR$0"]"""

    def clear_days(self):
        if xpath(self.monday).is_selected():
            xpath(self.monday).click()
        if xpath(self.tuesday).is_selected():
            xpath(self.tuesday).click()
        if xpath(self.wednesday).is_selected():
            xpath(self.wednesday).click()
        if xpath(self.thursday).is_selected():
            xpath(self.thursday).click()
        if xpath(self.friday).is_selected():
            xpath(self.friday).click()
        if xpath(self.saturday).is_selected():
            xpath(self.saturday).click()
        if xpath(self.sunday).is_selected():
            xpath(self.sunday).click()

    def clear_room(self):
        xpath(self.facility).clear()

    def clear_times(self):
        xpath(self.mtg_start).clear()
        xpath(self.mtg_end).clear()
        xpath(self.pattern).clear()


# load page
# chrome_path = r"C:\Work\chromedriver.exe"
# driver = webdriver.Chrome(chrome_path)
# driver.maximize_window()
# driver.get("""https://bcsint.is.berkeley.edu""")
# xpath = driver.find_element_by_xpath
sis_day_time.login.login_sis(driver, xpath, wait)


def main():
    n = 0
    setup = False
    excludes = list()
    while not setup:
        if input("Exclude courses (exclude.txt)? (Y or N): ").upper() == "Y":
            with open(r"C:\Work\exclude.txt") as csvfile:
                file = csv.reader(csvfile, delimiter='\t')
                for row in file:
                    excludes.append(row)
        input("Press enter to begin once on Schedule Class Meetings page. ")
        setup = True
    frame_wait("ptifrmtgtframe")
    course_condition = True
    while course_condition:
        course_section = Meetings()
        section_condition = True
        while section_condition:
            WebDriverWait(driver, 50).until(ec.invisibility_of_element_located((By.XPATH, course_section.loading)))
            if str(xpath(course_section.ccn).text) in str(excludes):
                time.sleep(2)
                print(xpath(course_section.course).text + "." + xpath(course_section.section).text + " skipped.")
            else:
                try:
                    driver.find_element_by_xpath("""//*[@id="DERIVED_SR_CMB_SCT_DTL_PB$0"]""")
                    print(xpath(course_section.course).text + "." + xpath(course_section.section).text +
                          " skipped: Combined section.")
                except NoSuchElementException:
                    course_section.clear_days()
                    course_section.clear_times()
                    course_section.clear_room()
                    save_record()
                    print(xpath(course_section.course).text + "." + xpath(course_section.section).text + " (" +
                          xpath(course_section.ccn).text + ")" + " " + xpath(course_section.mtg_end).get_attribute("value"))
                    n += 1
            try:
                xpath(course_section.next_section).click()
                time.sleep(2)
            except NoSuchElementException:
                section_condition = False
        course_condition = xpath(course_section.next_course).is_enabled()
        xpath(course_section.next_course).click()
    print("Changed " + str(n) + " records.")
    return


if __name__ == '__main__':
    main()
