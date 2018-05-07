import csv
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from datetime import datetime
from datetime import timedelta

# load page
chrome_path = r"C:\Work\chromedriver.exe"
driver = webdriver.Chrome(chrome_path)
driver.maximize_window()
driver.get("""https://bcsint.is.berkeley.edu""")
xpath = driver.find_element_by_xpath


def wait(x):
    WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH, x)))
    return


def frame_wait(x):
    WebDriverWait(driver,50).until(EC.frame_to_be_available_and_switch_to_it(x))
    return


def sis_search(x, y, z="UCB01"):
    xpath("""//*[@id="#ICClear"]""").click()
    time.sleep(1.5)
    xpath("""//*[@id="CLASS_SCTN_SCTY_INSTITUTION"]""").send_keys(z)
    time.sleep(1.5)
    xpath("""//*[@id="CLASS_SCTN_SCTY_STRM"]""").send_keys(y)
    time.sleep(1.5)
    xpath("""//*[@id="CLASS_SCTN_SCTY_CLASS_NBR"]""").send_keys(x)
    time.sleep(1.5)
    xpath("""//*[@id="#ICSearch"]""").click()
    return


def url_wait(x):
    WebDriverWait(driver, 10).until(EC.url_to_be(x))
    return


def change_days(x):
    x = x.upper()
    x = x.replace("TH", "R")
    x = x.replace("SU", "U")
    xpath("""//*[@id="CLASS_MTG_PAT_STND_MTG_PAT$0"]""").clear()
    time.sleep(1.5)
    monday = xpath("""// *[ @ id = "CLASS_MTG_PAT_MON$0"]""")
    tuesday = xpath("""// *[ @ id = "CLASS_MTG_PAT_TUES$0"]""")
    wednesday = xpath("""// *[ @ id = "CLASS_MTG_PAT_WED$0"]""")
    thursday = xpath("""// *[ @ id = "CLASS_MTG_PAT_THURS$0"]""")
    friday = xpath("""// *[ @ id = "CLASS_MTG_PAT_FRI$0"]""")
    saturday = xpath("""// *[ @ id = "CLASS_MTG_PAT_SAT$0"]""")
    sunday = xpath("""// *[ @ id = "CLASS_MTG_PAT_SUN$0"]""")
    if monday.is_selected():
        monday.click()
    if tuesday.is_selected():
        tuesday.click()
    if wednesday.is_selected():
        wednesday.click()
    if thursday.is_selected():
        thursday.click()
    if friday.is_selected():
        friday.click()
    if saturday.is_selected():
        saturday.click()
    if sunday.is_selected():
        sunday.click()
    if x.find("M") > - 1:
        monday.click()
    if x.find("T") > - 1:
        tuesday.click()
    if x.find("W") > - 1:
        wednesday.click()
    if x.find("R") > - 1:
        thursday.click()
    if x.find("F") > - 1:
        friday.click()
    if x.find("S") > - 1:
        saturday.click()
    if x.find("U") > - 1:
        sunday.click()
    return


def change_times(x, y):
    y = datetime.strptime(y, '%I:%M%p') - timedelta(minutes=1)
    y = datetime.strftime(y,'%I:%M%p')
    time.sleep(1.5)
    xpath("""//*[@id="CLASS_MTG_PAT_MEETING_TIME_START$0"]""").clear()
    time.sleep(.5)
    wait("""//*[@id="CLASS_MTG_PAT_MEETING_TIME_START$0"]""")
    xpath("""//*[@id="CLASS_MTG_PAT_MEETING_TIME_START$0"]""").send_keys(x)
    save_record()
    wait("""//*[@id="CLASS_MTG_PAT_MEETING_TIME_END$0"]""")
    xpath("""//*[@id="CLASS_MTG_PAT_MEETING_TIME_END$0"]""").clear()
    time.sleep(.5)
    xpath("""//*[@id="CLASS_MTG_PAT_MEETING_TIME_END$0"]""").send_keys(y)
    time.sleep(1.5)
    return


def change_max(x=1):
    wait("""//*[@id="ICTAB_1"]/span""")
    xpath("""// *[ @ id = "ICTAB_1"] / span""").click()
    wait("""//*[@id="CLASS_TBL_ENRL_CAP$0"]""")
    xpath("""//*[@id="CLASS_TBL_ENRL_CAP$0"]""").clear()
    xpath("""//*[@id="CLASS_TBL_ENRL_CAP$0"]""").send_keys(x)
    xpath("""//*[@id="#ICSave"]""").click()
    time.sleep(1.5)
    return


def save_record():
    xpath("""//*[@id="#ICSave"]""").click()
    time.sleep(2)
    element = WebDriverWait(driver, 50).until(EC.invisibility_of_element_located((By.ID, "SAVED_win0")))
    return


def return_to_results():
    xpath("""//*[@id="#ICList"]""").click()
    try:
        elem = xpath("""//*[@id="#ALERTYES"]""")
        if elem.is_displayed():
            elem.click()
            wait("""//*[@id="#ICSave"]""")
            xpath("""//*[@id="#ICSave"]""").click()
    except NoSuchElementException:
        pass
    return


# set semester and whether course max enrollment changes
term = input("Term (e.g., 2985): ")
maxes = 0

while (maxes == 0) or (maxes > 2):
    while True:
            try:
                maxes = int(input("Change course maxes? Won't work after registration has begun. (1 = Yes, 2 = No): "))
            except ValueError:
                print("Sorry, I didn't understand that.\n")
                continue
            else:
                break

with open(r"C:\Work\enter-days-sis-data.txt") as csvfile:
    frame_wait("ptifrmtgtframe")
    file = csv.reader(csvfile, delimiter='\t')
    # log = open(r"C:\Work\log.txt", "w")
    for row in file:
        CCN = row[0]
        start = row[1]
        end = row[2]
        days = row[3]
        room_max = row[4]
        sis_search(CCN, term)
        wait("""//*[@id="CLASS_TBL_ENRL_CAP$0"]""")
        time.sleep(1.5)
        change_max()
        save_record()
        xpath("""//*[@id="ICTAB_0"]/span""").click()
        wait("""// *[ @ id = "CLASS_MTG_PAT_STND_MTG_PAT$0"]""")
        change_days(days)
        time.sleep(1)
        change_times(start, end)
        time.sleep(1)
        save_record()
        change_max(room_max)
        save_record()
        return_to_results()
        wait("""//*[@id="#ICClear"]""")
        print(CCN)
print("Complete")

# xpath("""//*[@id="CLASS_INSTR_EMPLID$0"]""").clear()
# xpath("""//*[@id="CLASS_INSTR_EMPLID$0"]""").send_keys(instructor)
