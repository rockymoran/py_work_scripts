import csv
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.common.action_chains import ActionChains

# load page
chrome_path = r"C:\Work\chromedriver.exe"
driver = webdriver.Chrome(chrome_path)
driver.maximize_window()
driver.get("""https://coursescheduling.haas.berkeley.edu/Search""")
xpath = driver.find_element_by_xpath


def wait(x):
    WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, x)))
    return


# set semester
term = input("Semester and year (e.g., Spring 2142): ").strip()

usedID = 0

while (usedID == 0) or (usedID > 2):
    while True:
            try:
                usedID = int(input("Which ID type (1 = CCN, 2 = Schedule ID): ").strip())
            except ValueError:
                print("Sorry, I didn't understand that.\n")
                continue
            else:
                break


with open(r"C:\Work\dates.txt") as csvfile:
    file = csv.reader(csvfile, delimiter='\t')
    for row in file:
        recordID = row[0]
        startDate = row[1]
        endDate = row[2]
        wait("""/html/body/div[2]/div[1]/div/div/form/div[1]/div[2]/div[3]/span/span/input""")
        xpath("""//*[@id="Clear"]""")
        try:
            wait("""/html/body/div[2]/div[1]/div/div/form/div[1]/div[2]/div[3]/span/span/input""")
            xpath("""/html/body/div[2]/div[1]/div/div/form/div[1]/div[2]/div[3]/span/span/input""").clear()
            xpath("""/html/body/div[2]/div[1]/div/div/form/div[1]/div[2]/div[3]/span/span/input""").send_keys(term)
        except WebDriverException:
            time.sleep(5)
            wait("""/html/body/div[2]/div[1]/div/div/form/div[1]/div[2]/div[3]/span/span/input""")
            xpath("""/html/body/div[2]/div[1]/div/div/form/div[1]/div[2]/div[3]/span/span/input""").clear()
            xpath("""/html/body/div[2]/div[1]/div/div/form/div[1]/div[2]/div[3]/span/span/input""").send_keys(term)
        time.sleep(1)
        wait("""//*[@id="searchModel_CCN"]""")
        if usedID > 1:
            xpath("""//*[@id="searchModel_Schedule_ID"]""").clear()
            xpath("""//*[@id="searchModel_Schedule_ID"]""").send_keys(recordID)
        else:
            xpath("""//*[@id="searchModel_CCN"]""").clear()
            xpath("""//*[@id="searchModel_CCN"]""").send_keys(recordID)
        wait("""//*[@id="SearchButton"]""")
        xpath("""//*[@id="SearchButton"]""").click()
        time.sleep(1)
        wait("""//*[@id="GridCSList"]/table/tbody/tr/td[2]/a""")
        time.sleep(1)
        WebDriverWait(driver, 30).until(EC.invisibility_of_element_located((By.XPATH, """/html/body/div[16]/div[1]""")))
        time.sleep(1)
        xpath("""//*[@id="GridCSList"]/table/tbody/tr/td[2]/a""").click()
        wait("""//*[@id="ClassroomGrid"]/table/tbody/tr/td[1]/a/span""")
        xpath("""//*[@id="ClassroomGrid"]/table/tbody/tr/td[1]/a/span""").click()
        wait("""//*[@id="Begin_Date"]""")
        xpath("""//*[@id="Begin_Date"]""").clear()
        xpath("""//*[@id="Begin_Date"]""").send_keys(startDate)
        time.sleep(1)
        wait("""// *[ @ id = "End_Date"]""")
        xpath("""// *[ @ id = "End_Date"]""").clear()
        xpath("""// *[ @ id = "End_Date"]""").send_keys(endDate)
        time.sleep(1)
        xpath("""//*[@id="ClassroomGrid"]/table/tbody/tr/td[1]/a[1]""").click()
        time.sleep(1)
        wait("""//*[@id="Searchbutton"]""")
        try:
            xpath("""//*[@id="Searchbutton"]""").click()
            print(recordID)
        except:
            time.sleep(3)
            driver.get("""https://coursescheduling.haas.berkeley.edu/Search""")

