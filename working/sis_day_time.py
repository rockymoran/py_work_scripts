import csv
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import NoSuchElementException
from datetime import datetime
from datetime import timedelta

# load page
chrome_path = r"C:\Work\chromedriver.exe"
driver = webdriver.Chrome(chrome_path)
driver.maximize_window()
driver.get("""https://bcsint.is.berkeley.edu""")
xpath = driver.find_element_by_xpath
loading = """//*[@id="processing"]"""


def wait(x):
    WebDriverWait(driver,10).until(ec.element_to_be_clickable((By.XPATH, x)))
    return


def frame_wait(x):
    WebDriverWait(driver,50).until(ec.frame_to_be_available_and_switch_to_it(x))
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
    WebDriverWait(driver, 10).until(ec.url_to_be(x))
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
    try:
        x = x.replace(" ", "")
        y = y.replace(" ", "")
        y = datetime.strptime(y, '%I:%M%p') - timedelta(minutes=1)
        y = datetime.strftime(y, '%I:%M%p')
    except ValueError:
        x = ""
        y = ""
    time.sleep(1.5)
    # remove old room first
    xpath("""//*[@id="CLASS_MTG_PAT_FACILITY_ID$0"]""").clear()
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
    try:
        wait("""//*[@id="CLASS_TBL_ENRL_CAP$0"]""")
    except:
        xpath("""//*[@id="ICTAB_1"]""").click()
        wait("""//*[@id="CLASS_TBL_ENRL_CAP$0"]""")
    xpath("""//*[@id="CLASS_TBL_ENRL_CAP$0"]""").clear()
    xpath("""//*[@id="CLASS_TBL_ENRL_CAP$0"]""").send_keys(x)
    xpath("""//*[@id="#ICSave"]""").click()
    time.sleep(1.5)
    return


def find_max(x):
    room_list = {
        "C110": 47,
        "C125": 62,
        "C132": 12,
        "C135": 62,
        "C210": 64,
        "C220": 64,
        "C230": 129,
        "C250": 25,
        "C320": 31,
        "C325": 31,
        "C330": 31,
        "C335": 25,
        "C337": 10,
        "C420": 75,
        "I": 70,
        "N100": 130,
        "N170": 55,
        "N270": 55,
        "N300": 76,
        "N340": 48,
        "N370": 74,
        "N400": 76,
        "N440": 48,
        "N470": 74,
        "N500": 78,
        "N540": 48,
        "N570": 74,
        "I-Lab": 70,
        "F295": 299,
        "F320": 70,
        "F678": 12,
        "I-Lab 124": 70,
        "S300T": 60
    }
    return room_list.get(x, "none")


def change_room(x):
    key = x
    room_list = {
        "C110": "CHEIC110",
        "C125": "CHEIC125",
        "C132": "CHEIC132",
        "C135": "CHEIC135",
        "C138": "CHEIC138",
        "C210": "CHEIC210",
        "C220": "CHEIC220",
        "C230": "CHEIC230",
        "C250": "CHEIC250",
        "C320": "CHEIC320",
        "C325": "CHEIC325",
        "C330": "CHEIC330",
        "C335": "CHEIC335",
        "C337": "CHEIC337",
        "C420": "CHEIC420",
        "I": "STAD124",
        "N100": "CHOUN100",
        "N170": "CHOUN170",
        "N270": "CHOUN270",
        "N300": "CHOUN300",
        "N340": "CHOU340344",
        "N370": "CHOUN370",
        "N400": "CHOUN400",
        "N440": "CHOU440444",
        "N470": "CHOUN470",
        "N500": "CHOUN500",
        "N540": "CHOU540544",
        "N570": "CHOUN570",
        "I-Lab": "STAD124",
        "F295": "HAASF295",
        "I-Lab 124": "STAD124",
        "F320": "HAASF320",
        "F678": "HAASF678",
        "S300T": "HAASS300T"
    }
    xpath("""//*[@id="CLASS_MTG_PAT_FACILITY_ID$0"]""").clear()
    xpath("""//*[@id="CLASS_MTG_PAT_FACILITY_ID$0"]""").send_keys(room_list.get(key, "none"))
    save_record()
    time.sleep(1.5)
    try:
        driver.switch_to.parent_frame()
        wait("""//*[@id="#ICOK"]""")
        xpath("""//*[@id="#ICOK"]""").click()
        frame_wait("ptifrmtgtframe")
        print("Room conflict")
        wait("""//*[@id="CLASS_MTG_PAT_FACILITY_ID$0"]""")
        xpath("""//*[@id="CLASS_MTG_PAT_FACILITY_ID$0"]""").clear()
    except:
        pass
    return


def save_record():
    try:
        xpath("""//*[@id="#ICSave"]""").click()
    except:
        frame_wait("ptifrmtgtframe")
        xpath("""//*[@id="#ICSave"]""").click()
    time.sleep(2)
    WebDriverWait(driver, 50).until(ec.invisibility_of_element_located((By.ID, "SAVED_win0")))
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


def main():
    # set semester and whether course max enrollment changes
    term = input("Term (e.g., 2985): ")
    maxes = 0
    global_skip = 0

    while (maxes == 0) or (maxes > 2):
        while True:
                try:
                    maxes = int(input("Change course maxes? Won't work after registration has begun. (1 = Yes, 2 = No): "))
                except ValueError:
                    print("Sorry, I didn't understand that.\n")
                    continue
                else:
                    break

    while (global_skip == 0) or (global_skip > 2):
        while True:
                try:
                    global_skip = int(input("Create room assignments? (1 = Yes, 2 = No): "))
                except ValueError:
                    print("Sorry, I didn't understand that.\n")
                    continue
                else:
                    break

    with open(r"C:\Work\enter-days-sis-data.txt") as csvfile:
        frame_wait("ptifrmtgtframe")
        file = csv.reader(csvfile, delimiter='\t')
        # file format
        # CCN   Days    StartT  EndT    Room
        # 01234 MW      12:30PM 2:00PM  C110
        # 01235 TTh     2:00PM  3:30PM  N300
        for row in file:
            CCN = row[0]
            start = row[3]
            end = row[2]
            days = row[1]
            try:
                room = row[4]
                if len(room) > 0:
                    if global_skip == 1:
                        skip_room = False
                    else:
                        skip_room = True
                    room_max = find_max(room)
                else:
                    skip_room = True
            except IndexError:
                skip_room = True
            sis_search(CCN, term)
            WebDriverWait(driver, 50).until(ec.invisibility_of_element_located((By.XPATH, loading)))
            if maxes == 1:
                change_max()
                save_record()
            xpath("""//*[@id="ICTAB_0"]""").click()
            WebDriverWait(driver, 50).until(ec.invisibility_of_element_located((By.XPATH, loading)))
            wait("""// *[ @ id = "CLASS_MTG_PAT_STND_MTG_PAT$0"]""")
            change_days(days)
            time.sleep(1)
            change_times(start, end)
            if not skip_room:
                change_room(room)
            time.sleep(1.5)
            save_record()
            if maxes == 1:
                change_max(room_max)
            WebDriverWait(driver, 50).until(ec.invisibility_of_element_located((By.XPATH, loading)))
            save_record()
            return_to_results()
            WebDriverWait(driver, 50).until(ec.invisibility_of_element_located((By.XPATH, loading)))
            wait("""//*[@id="#ICClear"]""")
            print(CCN)
    print("Complete")


if __name__ == "__main__":
    main()