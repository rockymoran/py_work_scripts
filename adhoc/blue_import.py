# does the manual blue import process
import login
from selenium.webdriver.support.ui import Select
import csv
import time
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException, InvalidElementStateException
from working import sis_day_time

wait = sis_day_time.wait
xpath = sis_day_time.xpath
driver = sis_day_time.driver

UserGroup = r"""//*[@id="BlueDataSource"]"""

Admin = r"""//*[@id="BlueAppControl_admin-link-btn"]"""
Datasources = r"""//*[@id="AdminUC_menu_item_data_sources"]/div/span"""

searches = ["Haas-Course_Instructors",
            "Haas-Course_Students",
            "Haas-Courses",
            "Haas-Instructors",
            "Haas-Students"]

progress = r"""//*[@id="AdminUC_Data_AdminDS_Import_lblConfirm"]"""


NavImportExport = r"""//*[@id="AdminUC_Data_primary-tabs_ImportExport"]"""
Import = r"""//*[@id="AdminUC_Data_AdminDS_Import_btnImport"]"""
Finalize = r"""//*[@id="AdminUC_Data_AdminDS_Import_btnConfirm"]"""

FilterText = r"""//*[@id="AdminUC_DataSources_AdminDataSource_Tabs_tbSearchValue"]"""
FilterValue = "haas"
FilterSearch = r"""//*[@id="AdminUC_DataSources_AdminDataSource_Tabs_btnSearch"]"""

EditDatasource = r"""//*[@id="AdminUC_DataSources_AdminDataSource_Tabs_MultiDataSource_listing"]/tbody/tr[3]/td[7]/a"""

Datasource_TableCheck = r"""//*[@id="AdminUC_DataSources_AdminDataSource_Tabs_MultiDataSource_listing"]/tbody/tr[
                        3]/td[2]/span """


# load page
login.login_Blue(driver, xpath, wait)

# wait for user to manually select administrator (idk, the dropdown isn't working with selenium), then go
wait(Admin)
xpath(Admin).click()


def import_datasources(searches, debug):
    for search in searches:
        if debug == 1:
            input("Enter to continue")
        else:
            pass
        wait(Datasources)
        time.sleep(2)
        xpath(Datasources).click()
        wait(FilterSearch)
        xpath(FilterText).send_keys(search)
        xpath(FilterSearch).click()
        time.sleep(2)
        if debug == 1:
            input("Enter to continue")
        else:
            pass
        wait(EditDatasource)
        if xpath(Datasource_TableCheck).text == search:
            print("{} found. Script continuing".format(search))
            time.sleep(2)
            xpath(EditDatasource).click()
        else:
            print("{} not found.".format(search))
            break
        if debug == 1:
            input("Enter to continue")
        else:
            pass
        wait(NavImportExport)
        time.sleep(2)
        xpath(NavImportExport).click()
        if debug == 1:
            input("Enter to continue")
        else:
            pass
        wait(Import)
        time.sleep(2)
        xpath(Import).click()
        if debug == 1:
            input("Enter to continue")
        else:
            pass
        wait(progress)
        WebDriverWait(driver, 120).until(
            EC.invisibility_of_element_located((By.XPATH, progress)))
        wait(Finalize)
        time.sleep(2)
        xpath(Finalize).click()
        wait(Import)


import_datasources(searches, 0)

