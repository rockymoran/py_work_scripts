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
driver.get("""https://coursescheduling.haas.berkeley.edu/Search""")
xpath = driver.find_element_by_xpath


# file format
# CCN   ROOM    DAY START   END
# 00001 C125    MW  10:00AM 12:30PM
# 00002 N100    TTh 9:30AM  11:00AM

def wait(x):
    WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, x)))
    return


def wait_invis(x):
    WebDriverWait(driver, 10).until(EC.invisibility_of_element_located((By.XPATH, x)))
    return


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
        recordID = row[0]
        room = row[1]
        day = row[2]
        start = row[3]
        end = row[4]
        wait("""/html/body/div[2]/div[1]/div/div/form/div[1]/div[2]/div[3]/span/span/input""")
        xpath("""//*[@id="Clear"]""")
        wait("""//*[@id="SearchForm"]/div[1]/div[2]/div[3]/span/span/input""")
        xpath("""//*[@id="SearchForm"]/div[1]/div[2]/div[3]/span/span/input""").clear()
        time.sleep(1)
        xpath("""//*[@id="SearchForm"]/div[1]/div[2]/div[3]/span/span/input""").send_keys(term)
        time.sleep(1)
        wait("""//*[@id="SearchButton"]""")
        if usedID > 1:
            xpath("""//*[@id="searchModel_Schedule_ID"]""").clear()
            xpath("""//*[@id="searchModel_Schedule_ID"]""").send_keys(recordID)
        else:
            xpath("""//*[@id="searchModel_CCN"]""").clear()
            xpath("""//*[@id="searchModel_CCN"]""").send_keys(recordID)
        xpath("""//*[@id="SearchButton"]""").click()
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
        xpath("""//*[@id="ClassroomGrid"]/table/tbody/tr/td[2]/span[1]/span/input""").send_keys(room)
        time.sleep(1)
        driver.find_element_by_css_selector("""#ClassroomGrid > table > tbody > tr > td:nth-child(2) > span.k-widget.k-combobox.k-header.k-combobox-clearable > span > input""").send_keys(Keys.DOWN)
        xpath("""//*[@id="ClassroomGrid"]/table/tbody/tr/td[4]/span[1]/span/input""").clear()
        xpath("""//*[@id="ClassroomGrid"]/table/tbody/tr/td[4]/span[1]/span/input""").send_keys(day)
        time.sleep(1)
        driver.find_element_by_css_selector("""#ClassroomGrid > table > tbody > tr > td:nth-child(4) > span.k-widget.k-combobox.k-header.k-combobox-clearable > span > input""").send_keys(Keys.ENTER)
        xpath("""//*[@id="Begin_Time"]""").clear()
        xpath("""//*[@id="Begin_Time"]""").send_keys(start)
        xpath("""//*[@id="End_Time"]""").clear()
        xpath("""//*[@id="End_Time"]""").send_keys(end)
        xpath("""//*[@id="ClassroomGrid"]/table/tbody/tr/td[1]/a[1]""").click()
        time.sleep(1)
        wait("""//*[@id="Searchbutton"]""")
        try:
            xpath("""//*[@id="Searchbutton"]""").click()
            print(recordID)
        except:
            time.sleep(3)
            driver.get("""https://coursescheduling.haas.berkeley.edu/Search""")
            print("Potential issue: ", recordID)
