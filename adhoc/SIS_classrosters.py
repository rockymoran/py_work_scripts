from selenium import webdriver
from working import sis_day_time
import pandas as pd
from selenium.webdriver.support.ui import Select
import re
import sys
import tkinter as tk
from tkinter import filedialog

# various sis and selenium variables
wait = sis_day_time.wait
xpath = sis_day_time.xpath
frame_wait = sis_day_time.frame_wait
driver = sis_day_time.driver
WebDriverWait = sis_day_time.WebDriverWait

# set script variables for urls and file locations
roster_url = """https://bcsint.is.berkeley.edu/psc/bcsprd_1/EMPLOYEE/SA/q/?ICAction=ICQryNameExcelURL=PUBLIC.UCCS_G_ENRL_BY_CLASS"""
term_search = """//*[@id="InputKeys_STRM"]"""
email_type = """//*[@id="InputKeys_E_ADDR_TYPE"]"""
ccn_field = """//*[@id="InputKeys_CLASS_NBR"]"""
results = """//*[@id="#ICQryDownloadExcelFrmPrompt"]"""
subject_field = """//*[@id="InputKeys_SUBJECT"]"""


# Initialize Tkinter and hide the main window (we only want the popup)
root = tk.Tk()
root.withdraw()

print("Please select your Excel file...")

# Open the file dialog
ccn_term_file = filedialog.askopenfilename(
    title="Select the Course Schedule File",
    filetypes=[("Excel files", "*.xlsx;*.xls")]
)

# Check if user clicked "Cancel"
if not ccn_term_file:
    print("No file selected. Exiting script.")
    sys.exit()

# load file of SIS ID numbers
# needs at least CCN, Term, Year, Course columns (using CS export to excel by default)
df = pd.read_excel(ccn_term_file)

# --- START PREPROCESSING LOGIC ---

# FIX: Ensure CCN is always a 5-digit string (e.g., "1234" -> "01234")
# We use a lambda to handle cases where Excel stored it as a float (1234.0) or int (1234)
def clean_ccn(val):
    try:
        # convert to float first (handles 1234.0), then int, then string
        return str(int(float(val))).zfill(5)
    except:
        # Fallback for unexpected strings
        return str(val).zfill(5)

df['CCN'] = df['CCN'].apply(clean_ccn)

# Map semester names to their suffix digits (case-insensitive)
semester_map = {
    'spring': '2',
    'summer': '5',
    'fall': '8'
}


def calculate_term(row):
    # Clean and normalize inputs
    sem_key = str(row['Semester']).strip().lower()

    # Handle Year: Convert to int to remove decimals (e.g. 2025.0), then string, then take last 2 chars
    year_short = str(int(row['Year']))[-2:]

    # Get semester digit
    sem_digit = semester_map.get(sem_key)

    if not sem_digit:
        raise ValueError(f"Invalid Semester found: {row['Semester']}")

    # Combine: "2" + YY + S
    return f"2{year_short}{sem_digit}"


# Apply the term logic
df['term'] = df.apply(calculate_term, axis=1)

# 3. Logic to create "prog"
# We use Regex to extract the valid prefix from the "Course" column.
# The pattern looks for the specific prefixes at the start of the string (^)
valid_programs = ["PHDBA", "MFE", "EWMBA", "MBA", "UGBA", "XMBA"]
pattern = r"^(" + "|".join(valid_programs) + ")"

# This extracts the match into a new column called 'prog'
df['prog'] = df['Course'].astype(str).str.extract(pattern, expand=False)


# --- END PREPROCESSING LOGIC ---



# go to roster page
# search for term and ccn
# download file
# log success or failure


def run_report(x):
    driver.get(roster_url)
    wait(term_search)
    select = Select(driver.find_element('id', 'InputKeys_E_ADDR_TYPE'))
    xpath(term_search).send_keys(str(x["term"]))
    xpath(subject_field).clear()
    xpath(subject_field).send_keys(str(x["prog"]))
    xpath(ccn_field).clear()
    xpath(ccn_field).send_keys(str(x["CCN"]).zfill(5))
    select.select_by_value('CAMP')
    xpath(results).click()


def main():
    sis_day_time.login.login_sis(driver, xpath, wait)
    wait("""//*[@id="win0hdrdivPT_TITLE_CONT"]""")
    df.apply(run_report, axis=1)


if __name__ == '__main__':
    main()
