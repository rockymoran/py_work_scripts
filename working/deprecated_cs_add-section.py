import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

#load page
chrome_path = r"C:\Work\chromedriver.exe"
driver  = webdriver.Chrome(chrome_path)
driver.maximize_window()
driver.get("""http://coursescheduling-qa.haas.berkeley.edu/Search""")

def wait(x):
	element = WebDriverWait(driver,30).until(EC.element_to_be_clickable((By.XPATH,x)))
	return;

with open(r"C:\Work\ind.txt") as csvfile:
    xpath = driver.find_element_by_xpath
    file = csv.reader(csvfile, delimiter='\t')
    for row in file:
        # wait for page to load
        wait("""//*[@id="SearchButton"]""")
        ##
        # click add course
        xpath("""//*[@id="AddCourseButton"]""").click()
        ##
        # wait for add course section screen to pop-up
        wait("""//*[@id="SubmitForm"]""")
        xpath("""//*[@id="AddCSForm"]/div/div[1]/div/span[1]/span/input""").send_keys(row[0])
        xpath("""//*[@id="AddCSForm"]/div/div[1]/div/span[1]/span/input""").send_keys(Keys.ENTER)
        xpath("""//*[@id="SectionText"]  """).send_keys(row[1])
        xpath("""//*[@id="CCNText"]""").send_keys(row[3])
        xpath("""//*[@id="AddCSForm"]/div/div[3]/div[3]/span[1]/span/input[1]""").send_keys(row[4])
        xpath("""//*[@id="AddCSForm"]/div/div[4]/div[3]/span[1]/span/input""").send_keys(row[5])
        xpath("""//*[@id="AddCSForm"]/div/div[1]/div/span[1]/span/input""").send_keys(Keys.ENTER)
        xpath("""//*[@id="SubmitForm"]""").click()
        wait("""/html/body/div[22]/div[2]/div/div/div/div/div[4]/button[2]""")
        xpath("""/html/body/div[22]/div[2]/div/div/div/div/div[4]/button[2]""").click()
        wait("""//*[@id="InstructorGrid"]/table/tbody/tr/td[1]/a/span""")
        xpath("""//*[@id="InstructorGrid"]/table/tbody/tr/td[1]/a/span""").click()
        wait("""//*[@id="InstructorGrid"]/table/tbody/tr/td[2]/span[1]/span/input""")
        xpath("""//*[@id="InstructorGrid"]/table/tbody/tr/td[2]/span[1]/span/input""").clear()
        xpath("""//*[@id="InstructorGrid"]/table/tbody/tr/td[2]/span[1]/span/input""").send_keys(row[2])
        wait("""//*[@id="instructorModel_listbox"]""")
        xpath("""//*[@id="instructorModel_listbox"]""").send_keys(Keys.ENTER)
        wait("""/html/body/div[9]/div[2]/div/div/div/div/div[4]/button[2]""")
        xpath("""/html/body/div[9]/div[2]/div/div/div/div/div[4]/button[2]""").click()
        xpath("""//*[@id="InstructorGrid"]/table/tbody/tr/td[2]/span[1]/span/input""").send_keys(Keys.ENTER)
        xpath("""//*[@id="InstructorGrid"]/table/tbody/tr/td[1]/a[1]/span""").click()
        wait("""/html/body/div[9]/div[2]/div/div/div/div/div[4]/button[2]""")
        xpath("""/html/body/div[9]/div[2]/div/div/div/div/div[4]/button[2]""").click()
        wait("""//*[@id="Searchbutton"]""")
        xpath("""//*[@id="Searchbutton"]""").click()




