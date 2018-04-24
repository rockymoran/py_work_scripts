import csv
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException

#load page
chrome_path = r"C:\Work\chromedriver.exe"
driver  = webdriver.Chrome(chrome_path)
driver.maximize_window()
driver.get("""https://bcsint.is.berkeley.edu""")
xpath = driver.find_element_by_xpath

def wait(x):
    element = WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH,x)))
    return;

def framewait(x):
    element = WebDriverWait(driver,50).until(EC.frame_to_be_available_and_switch_to_it(x))
    return;

def urlwait(x):
    element = WebDriverWait(driver,10).until(EC.url_to_be(x))
    return;

#set semester
term = input("Term (e.g., 2985)\n")
institution = "UCB01"

framewait("ptifrmtgtframe")

with open(r"C:\Work\enter-inst-sis-data.txt") as csvfile:
    file = csv.reader(csvfile, delimiter='\t')
    #log = open(r"C:\Work\log.txt", "w")
    for row in file:
        CCN = row[0]
        instructor = row[1]
        xpath("""//*[@id="#ICClear"]""").click()
        time.sleep ( 1.5 )
        xpath("""//*[@id="CLASS_SCTN_SCTY_INSTITUTION"]""").send_keys(institution)
        time.sleep ( 1.5 )
        xpath("""//*[@id="CLASS_SCTN_SCTY_STRM"]""").send_keys(term)
        time.sleep ( 1.5 )
        xpath("""//*[@id="CLASS_SCTN_SCTY_CLASS_NBR"]""").send_keys(CCN)
        time.sleep ( 1.5 )
        xpath("""//*[@id="#ICSearch"]""").click()
        wait("""//*[@id="CLASS_INSTR_EMPLID$0"]""")
        time.sleep( 1.5 )
        xpath("""//*[@id="CLASS_INSTR_EMPLID$0"]""").clear()
        xpath("""//*[@id="CLASS_INSTR_EMPLID$0"]""").send_keys(instructor)
        time.sleep( 1.5 )
        xpath("""//*[@id="#ICSave"]""").click()
        time.sleep ( 2 )
        element = WebDriverWait(driver,50).until(EC.invisibility_of_element_located((By.ID,"SAVED_win0")))
        xpath("""//*[@id="#ICList"]""").click()
        try:
            elem = xpath("""//*[@id="#ALERTYES"]""")
            if elem.is_displayed():
                elem.click()
                wait("""//*[@id="#ICSave"]""")
                xpath("""//*[@id="#ICSave"]""").click()
        except NoSuchElementException:
            pass
        wait("""//*[@id="#ICClear"]""")
        print(CCN)
print("Complete")
