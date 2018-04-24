import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

chrome_path = r"C:\Work\chromedriver.exe"
driver  = webdriver.Chrome(chrome_path)
driver.maximize_window()
driver.get("""http://coursescheduling-qa.haas.berkeley.edu/Search""")

## wait for manual login
wait = WebDriverWait(driver,30)
element = wait.until(EC.element_to_be_clickable((By.XPATH,"""//*[@id="SearchButton"]""")))
## end wait


with open(r"C:\Work\test.csv") as csvfile:
    file = csv.reader(csvfile, delimiter='\t')
    for row in file:
        print = row
        driver.find_element_by_xpath("""//*[@id="searchModel_CCN"]""").send_keys(row[0])
        driver.find_element_by_xpath("""//*[@id="SearchDiv"]/div[2]/div[2]/span/span/input""").send_keys(row[1])
        #driver.find_element_by_xpath("""//*[@id="SearchDiv"]/div[2]/div[2]/span/span/input""").send_keys(Keys.ENTER)
        driver.find_element_by_xpath("""//*[@id="AddCourseButton"]""").click()
