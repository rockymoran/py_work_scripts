import csv
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.common.action_chains import ActionChains

# load page
chrome_path = r"C:\Work\chromedriver.exe"
driver = webdriver.Chrome(chrome_path)
driver.maximize_window()
website = """https://api.haas.berkeley.edu/Search"""
driver.get(website)
xpath = driver.find_element_by_xpath


# file format
# CCN   DAY     START   END     START_DATE  END_DATE     ROOM
# 00001 MW      10:00AM 12:30PM 5/19/2035   6/24/2035    C125
# 00002 TTh     9:30AM  11:00AM 5/19/2035   6/24/2035    N300

def wait(x):
    WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, x)))
    return


def wait_invis(x):
    WebDriverWait(driver, 30).until(EC.invisibility_of_element_located((By.XPATH, x)))
    return


class Course:
    def __init__(self, recordID, room, day, start, end, start_d="", end_d=""):
        self.recordID = recordID
        self.room = room
        self.day = day
        self.start = start
        self.end = end
        self.start_d = start_d
        self.end_d = end_d


# set semester
term = input("Semester and year (e.g., Spring 2142): ")

usedID = 0

while (usedID == 0) or (usedID > 2):
    while True:
            try:
                usedID = int(input("Which ID type (1 = CCN, 2 = Schedule ID): "))
            except ValueError:
                print("Sorry, I didn't understand that.\n")
                continue
            else:
                break

editMode = 0

while (editMode == 0) or (editMode > 2):
    while True:
            try:
                editMode = int(input("Which edit type (1 = Replace Existing, 2 = New Entry): "))
            except ValueError:
                print("Sorry, I didn't understand that.\n")
                continue
            else:
                break

with open(r"C:\Work\rooms.txt") as csvfile:
    file = csv.reader(csvfile, delimiter='\t')
    for row in file:
        current_course = Course(row[0], row[4], row[1], row[2], row[3])
        try:
            current_course.start_d = row[5]
            current_course.end_d = row[6]
            noDates = False
        except IndexError:
            noDates = True
        wait("""/html/body/div[2]/div[1]/div/div/form/div[1]/div[2]/div[3]/span/span/input""")
        xpath("""//*[@id="Clear"]""")
        wait("""//*[@id="SearchForm"]/div[1]/div[2]/div[3]/span/span/input""")
        xpath("""//*[@id="SearchForm"]/div[1]/div[2]/div[3]/span/span/input""").clear()
        time.sleep(1)
        try:
            xpath("""//*[@id="SearchForm"]/div[1]/div[2]/div[3]/span/span/input""").send_keys(term)
        except:
            time.sleep(3)
            wait("""//*[@id="searchModel_CCN"]""")
            wait("""//*[@id="SearchForm"]/div[1]/div[2]/div[3]/span/span/input""")
            xpath("""//*[@id="SearchForm"]/div[1]/div[2]/div[3]/span/span/input""").send_keys(term)
        time.sleep(1)
        wait("""//*[@id="SearchButton"]""")
        if usedID > 1:
            xpath("""//*[@id="searchModel_Schedule_ID"]""").clear()
            xpath("""//*[@id="searchModel_Schedule_ID"]""").send_keys(current_course.recordID)
        else:
            xpath("""//*[@id="searchModel_CCN"]""").clear()
            xpath("""//*[@id="searchModel_CCN"]""").send_keys(current_course.recordID)
        xpath("""//*[@id="SearchButton"]""").click()
        try:
            wait("""//*[@id="GridCSList"]/table/tbody/tr/td[2]/a""")
        except:
            time.sleep(1)
            wait("""//*[@id="GridCSList"]/table/tbody/tr/td[2]/a""")
        time.sleep(1)
        wait_invis("""//div[@class='modal-backdrop fade in']""")
        xpath("""//*[@id="GridCSList"]/table/tbody/tr/td[2]/a""").click()
        wait_invis("""//div[@class=’k-loading-mask’]""")
        if editMode > 1:
            wait("""// *[ @ id = "ClassroomGrid"] / div / a / span""")
            xpath("""//*[@id="ClassroomGrid"]/div/a/span""").click()
        else:
            wait("""//*[@id="ClassroomGrid"]/table/tbody/tr/td[1]/a/span""")
            xpath("""//*[@id="ClassroomGrid"]/table/tbody/tr/td[1]/a/span""").click()
        wait("""// *[ @ id = "ClassroomGrid"] / table / tbody / tr / td[1] / a[1]""")
        xpath("""//*[@id="ClassroomGrid"]/table/tbody/tr/td[2]/span[1]/span/input""").clear()
        xpath("""//*[@id="ClassroomGrid"]/table/tbody/tr/td[2]/span[1]/span/input""").send_keys(current_course.room)
        time.sleep(1)
        driver.find_element_by_css_selector("""#ClassroomGrid > table > tbody > tr > td:nth-child(2) > span.k-widget.k-combobox.k-header.k-combobox-clearable > span > input""").send_keys(Keys.DOWN)
        xpath("""//*[@id="ClassroomGrid"]/table/tbody/tr/td[4]/span[1]/span/input""").clear()
        xpath("""//*[@id="ClassroomGrid"]/table/tbody/tr/td[4]/span[1]/span/input""").send_keys(current_course.day)
        time.sleep(1)
        driver.find_element_by_css_selector("""#ClassroomGrid > table > tbody > tr > td:nth-child(4) > span.k-widget.k-combobox.k-header.k-combobox-clearable > span > input""").send_keys(Keys.ENTER)
        xpath("""//*[@id="Begin_Time"]""").clear()
        xpath("""//*[@id="Begin_Time"]""").send_keys(current_course.start)
        xpath("""//*[@id="End_Time"]""").clear()
        xpath("""//*[@id="End_Time"]""").send_keys(current_course.end)
        if not noDates:
            xpath("""//*[@id="Begin_Date"]""").clear()
            xpath("""//*[@id="Begin_Date"]""").send_keys(current_course.start_d)
            xpath("""//*[@id="End_Date"]""").clear()
            xpath("""//*[@id="End_Date"]""").send_keys(current_course.end_d)
        xpath("""//*[@id="ClassroomGrid"]/table/tbody/tr/td[1]/a[1]""").click()
        time.sleep(1)
        wait("""//*[@id="Searchbutton"]""")
        try:
            xpath("""//*[@id="Searchbutton"]""").click()
            print(current_course.recordID)
        except:
            time.sleep(3)
            driver.get(website)
            print("Potential issue: ", current_course.recordID)
