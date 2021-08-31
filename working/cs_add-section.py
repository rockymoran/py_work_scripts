import csv
import time
import login
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException

# load page
chrome_path = r"C:\Work\chromedriver.exe"
driver = webdriver.Chrome(chrome_path)
xpath = driver.find_element_by_xpath


def wait(x):
    WebDriverWait(driver, 30).until(ec.element_to_be_clickable((By.XPATH, x)))
    return


# set semester
term = input("Semester and year (e.g., Spring 2042): ")

# login
login.login_cs(driver, xpath, wait)

# example file format (tabs) (ind.txt)
# PHDBA299A	1	Dal Bo, E	19011	6	ind working title
with open(r"C:\Work\ind.txt") as csvfile:
    file = csv.reader(csvfile, delimiter='\t')
    for row in file:
        wait("""//*[@id="Clear"]""")
        try:
            wait("""//*[@id="Clear"]""")
            xpath("""//*[@id="SearchForm"]/div[1]/div[3]/div[3]/span/span/input""").clear()
            xpath("""//*[@id="SearchForm"]/div[1]/div[3]/div[3]/span/span/input""").send_keys(term)
        except WebDriverException:
            time.sleep(5)
            wait("""//*[@id="Clear"]""")
            xpath("""/html/body/div[2]/div[1]/div/div/form/div[1]/div[2]/div[3]/span/span/input""").clear()
            xpath("""/html/body/div[2]/div[1]/div/div/form/div[1]/div[2]/div[3]/span/span/input""").send_keys(term)
        time.sleep(1)
        wait("""//*[@id="SearchButton"]""")
        xpath("""//*[@id="AddCourseButton"]""").click()
        wait("""//*[@id="SubmitForm"]""")
        xpath("""//*[@id="AddCSForm"]/div/div[1]/div/span[1]/span/input""").send_keys(row[0])
        xpath("""//*[@id="AddCSForm"]/div/div[1]/div/span[1]/span/input""").send_keys(Keys.ENTER)
        xpath("""//*[@id="SectionText"]  """).send_keys(row[1])
        xpath("""//*[@id="CCNText"]""").send_keys(row[3])
        xpath("""//*[@id="AddCSForm"]/div/div[3]/div[3]/span[1]/span/input[1]""").send_keys(row[4])
        try:
            xpath("""//*[@id="AddCSForm"]/div/div[4]/div[3]/span[1]/span/input""").send_keys(row[5])
        except IndexError:
            xpath("""//*[@id="AddCSForm"]/div/div[4]/div[3]/span[1]/span/input""").send_keys("Lec")
        xpath("""//*[@id="AddCSForm"]/div/div[1]/div/span[1]/span/input""").send_keys(Keys.ENTER)
        xpath("""//*[@id="SubmitForm"]""").click()
        wait("""/html/body/div[22]/div[2]/div/div/div/div/div[4]/button[2]""")
        xpath("""/html/body/div[22]/div[2]/div/div/div/div/div[4]/button[2]""").click()
        wait("""//*[@id="InstructorGrid"]/table/tbody/tr/td[1]/a/span""")
        xpath("""//*[@id="InstructorGrid"]/table/tbody/tr/td[1]/a/span""").click()
        wait("""//*[@id="InstructorGrid"]/table/tbody/tr/td[2]/span[1]/span/input""")
        time.sleep(1)
        xpath("""//*[@id="InstructorGrid"]/table/tbody/tr/td[2]/span[1]/span/input""").send_keys()
        time.sleep(1)
        xpath("""//*[@id="InstructorGrid"]/table/tbody/tr/td[1]/a[1]/span""").click()
        # enter inst again
        wait("""//*[@id="InstructorGrid"]/table/tbody/tr/td[1]/a""")
        xpath("""//*[@id="InstructorGrid"]/table/tbody/tr/td[1]/a/span""").click()
        wait("""//*[@id="InstructorGrid"]/table/tbody/tr/td[2]/span[1]/span/input""")
        xpath("""//*[@id="InstructorGrid"]/table/tbody/tr/td[2]/span[1]/span/input""").clear()
        xpath("""//*[@id="InstructorGrid"]/table/tbody/tr/td[2]/span[1]/span/input""").send_keys(row[2])
        time.sleep(.5)
        xpath("""//*[@id="InstructorGrid"]/table/tbody/tr/td[2]/span[1]/span/input""").send_keys(Keys.DOWN)
        xpath("""//*[@id="InstructorGrid"]/table/tbody/tr/td[1]/a[1]/span""").click()
        try:
            xpath("""//*[@id="WTitleText"]""").clear()
            time.sleep(1)
            xpath("""//*[@id="WTitleText"]""").send_keys(row[6])
            xpath("""//*[@id="Savebutton"]""").click()
            wait("""/html/body/div[8]/div[2]/div/div/div/div/div[4]/button""")
            xpath("""/html/body/div[9]/div[2]/div/div/div/div/div[4]/button""").click()
        except:
            pass
        driver.get("""https://coursescheduling.haas.berkeley.edu/Search""")
        print(row[3])
