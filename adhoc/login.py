from selenium.common import NoSuchElementException

from working import config

username = config.username
password = config.password


def login_sis(driver, xpath, wait):
    driver.maximize_window()
    driver.get("""https://bcsint.is.berkeley.edu""")
    try:
        xpath("""//*[@id="sis-splash-sign-in-button"]""").click()
    except NoSuchElementException:
        print("Can't login. Are you connected to VPN?")
        return
    wait("""//*[@id="submitBtn"]/span""")
    xpath("""//*[@id="username"]""").send_keys(config.username)
    xpath("""//*[@id="password"]""").send_keys(config.password)
    xpath("""//*[@id="submitBtn"]/span""").click()
    return


def login_cs(driver, xpath, wait):
    driver.maximize_window()
    driver.get("""https://coursescheduling.haas.berkeley.edu""")
    wait("""//*[@id="loginForm"]/form/div/div[3]/input""")
    xpath("""//*[@id="UserName"]""").send_keys(config.username)
    xpath("""//*[@id="Password"]""").send_keys(config.password)
    xpath("""//*[@id="loginForm"]/form/div/div[3]/input""").click()
    return


def login_bCourses(driver, xpath, wait):
    driver.maximize_window()
    driver.get("""https://bcourses.berkeley.edu""")
    wait("""//*[@id="submit"]""")
    xpath("""//*[@id="username"]""").send_keys(config.username)
    xpath("""//*[@id="password"]""").send_keys(config.password)
    xpath("""//*[@id="submit"]""").click()
    return


def login_Blue(driver, xpath, wait):
    driver.maximize_window()
    driver.get("""https://course-evaluations.berkeley.edu""")
    wait("""//*[@id="submit"]""")
    xpath("""//*[@id="username"]""").send_keys(config.username)
    xpath("""//*[@id="password"]""").send_keys(config.password)
    xpath("""//*[@id="submit"]""").click()
    return

