import csv
import time
import login
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException
# from selenium.webdriver.common.action_chains import ActionChains

# load page
chrome_path = r"c:\Work\chromedriver.exe"
driver = webdriver.Chrome(chrome_path)
xpath = driver.find_element_by_xpath


# file format
# CCN   INST
# 00001 Smith, M
# 00002 Gonzales, R

def wait(x):
    WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, x)))
    return


def wait_invis(x):
    WebDriverWait(driver, 10).until(EC.invisibility_of_element_located((By.XPATH, x)))
    return


login.login_cs(driver, xpath, wait)

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

with open(r"C:\Work\inst_cs.txt") as csvfile:
    file = csv.reader(csvfile, delimiter='\t')
    for row in file:
        recordID = row[0]
        instructor = row[1]
        try:
            wait("""/html/body/div[2]/div[1]/div/div/form/div[1]/div[2]/div[3]/span/span/input""")
        except WebDriverException:
            driver.get("""https://coursescheduling.haas.berkeley.edu/Search""")
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
        wait("""//*[@id="SearchButton"]""")
        xpath("""//*[@id="SearchButton"]""").click()
        time.sleep(1)
        wait("""//*[@id="GridCSList"]/table/tbody/tr/td[2]/a""")
        time.sleep(1)
        WebDriverWait(driver, 30).until(EC.invisibility_of_element_located((By.XPATH, """/html/body/div[16]/div[1]""")))
        time.sleep(1)
        xpath("""//*[@id="GridCSList"]/table/tbody/tr/td[2]/a""").click()
        wait_invis("""//div[@class=’k-loading-mask’]""")
        if editMode > 1:
            wait("""//*[@id="InstructorGrid"]/div[1]/a/span""")
            xpath("""//*[@id="InstructorGrid"]/div[1]/a/span""").click()
        else:
            wait("""//*[@id="InstructorGrid"]/table/tbody/tr/td[1]/a/span""")
            xpath("""//*[@id="InstructorGrid"]/table/tbody/tr/td[1]/a/span""").click()
        wait("""//*[@id="InstructorGrid"]/table/tbody/tr/td[2]/span[1]/span/input""")
        xpath("""//*[@id="InstructorGrid"]/table/tbody/tr/td[2]/span[1]/span/input""").clear()
        xpath("""//*[@id="InstructorGrid"]/table/tbody/tr/td[2]/span[1]/span/input""").send_keys(row[1])
        time.sleep(1)
        driver.find_element_by_css_selector("""#InstructorGrid > table > tbody > tr > td:nth-child(2) > 
        span.k-widget.k-combobox.k-header.k-combobox-clearable > span > input""").send_keys(Keys.DOWN)
        xpath("""//*[@id="InstructorGrid"]/table/tbody/tr/td[1]/a[1]/span""").click()
        time.sleep(1)
        wait("""//*[@id="Searchbutton"]""")
        try:
            xpath("""//*[@id="Searchbutton"]""").click()
            print(recordID)
        except Exception as e:
            time.sleep(3)
            driver.get("""https://coursescheduling.haas.berkeley.edu/Search""")
            print("Potential issue: ", recordID)

