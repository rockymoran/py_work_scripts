from selenium import webdriver
from working import sis_day_time
import pandas as pd
from selenium.webdriver.support.ui import Select
import re
import sys
import os
import glob
import time
import tkinter as tk
from tkinter import filedialog
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import warnings
from openpyxl import load_workbook

# Suppress the openpyxl default style warning
warnings.filterwarnings('ignore', category=UserWarning, module='openpyxl')

# Directory where files will be downloaded and renamed
download_dir = r"C:\Work\Report_Downloads"

# Ensure download directory exists
if not os.path.exists(download_dir):
    os.makedirs(download_dir)

# Configure Chrome options for downloads
chrome_options = webdriver.ChromeOptions()
prefs = {
    "download.default_directory": download_dir,
    "download.prompt_for_download": False,
    "download.directory_upgrade": True,
    "safebrowsing.enabled": True
}
chrome_options.add_experimental_option("prefs", prefs)

# Create our own driver instance for THIS script only
driver = webdriver.Chrome(options=chrome_options)


# Create local versions of the helper functions that use OUR driver
def xpath(x):
    return driver.find_element(By.XPATH, x)


def wait(x):
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, x)))
    return


def frame_wait(x):
    WebDriverWait(driver, 15).until(EC.frame_to_be_available_and_switch_to_it(x))
    return


# ROSTER (2011+) set script variables for urls and file locations
roster_url = """https://bcsint.is.berkeley.edu/psc/bcsprd_1/EMPLOYEE/SA/q/?ICAction=ICQryNameExcelURL=PUBLIC.UCCS_G_ENRL_BY_CLASS"""
email_type = """//*[@id="InputKeys_E_ADDR_TYPE"]"""
ccn_field = """//*[@id="InputKeys_CLASS_NBR"]"""
subject_field = """//*[@id="InputKeys_SUBJECT"]"""
term_search = """//*[@id="InputKeys_STRM"]"""
# EGRADES ROSTER (2010-) set script variables for urls and file locations
older_roster_url = """https://bcsint.is.berkeley.edu/psc/bcsprd_1/EMPLOYEE/SA/q/?ICAction=ICQryNameExcelURL=PUBLIC.UCCS_R_BF_EGRD_ROSTER"""
older_ccn_field = """//*[@id="InputKeys_UC_CRS_CNTL_NUM"]"""
older_term_search = """//*[@id="InputKeys_TERM"]"""
# Universal
results = """//*[@id="#ICQryDownloadExcelFrmPrompt"]"""

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
df = pd.read_excel(ccn_term_file)


# --- START PREPROCESSING LOGIC ---

def clean_ccn(val):
    try:
        return str(int(float(val))).zfill(5)
    except:
        return str(val).zfill(5)


df['CCN'] = df['CCN'].apply(clean_ccn)

# Map semester names to their suffix digits (case-insensitive)
semester_map = {
    'spring': '2',
    'summer': '5',
    'fall': '8'
}


def calculate_term(row):
    sem_key = str(row['Semester']).strip().lower()
    year_short = str(int(row['Year']))[-2:]
    sem_digit = semester_map.get(sem_key)

    if not sem_digit:
        raise ValueError(f"Invalid Semester found: {row['Semester']}")

    return f"2{year_short}{sem_digit}"


df['term'] = df.apply(calculate_term, axis=1)

# Logic to create "prog"
valid_programs = ["PHDBA", "MFE", "EWMBA", "MBA", "UGBA", "XMBA"]
pattern = r"^(" + "|".join(valid_programs) + ")"
df['prog'] = df['Course'].astype(str).str.extract(pattern, expand=False)


# --- END PREPROCESSING LOGIC ---

def wait_for_new_file(download_dir, existing_files, timeout=60):
    """Wait for a NEW file to appear that wasn't in the existing_files set"""
    seconds = 0
    while seconds < timeout:
        time.sleep(1)
        current_files = set(os.listdir(download_dir))

        # Check for new complete files (not in existing set and not temp files)
        new_files = current_files - existing_files
        complete_new_files = [f for f in new_files
                              if not f.endswith('.crdownload')
                              and not f.endswith('.tmp')
                              and not f.endswith('.part')]

        if complete_new_files:
            # Return the newest complete file
            newest = max(complete_new_files,
                         key=lambda f: os.path.getctime(os.path.join(download_dir, f)))
            return os.path.join(download_dir, newest)

        seconds += 1
    return None


def clean_filename(text):
    """Remove invalid characters from filename"""
    invalid_chars = r'[<>:"/\\|?*]'
    return re.sub(invalid_chars, '_', text)


def rename_downloaded_file(row, download_dir, existing_files):
    """Rename the downloaded file based on the row data"""
    # Wait for a NEW file to appear
    new_file = wait_for_new_file(download_dir, existing_files, timeout=60)

    if new_file:
        # Extract file extension
        _, ext = os.path.splitext(new_file)

        # Check if file has enrollment data and remove Grade column if present
        has_enrollment = True
        grade_removed = False

        try:
            # Read the Excel file (skip first row which is the report title)
            temp_df = pd.read_excel(new_file, header=1)

            # Check if dataframe has any data rows after the header
            if temp_df.empty or len(temp_df) == 0:
                has_enrollment = False
            else:
                # Check if all rows are empty (all NaN)
                if temp_df.isna().all().all():
                    has_enrollment = False

            # Check for Grade column and remove it if present
            if 'Grade' in temp_df.columns:
                temp_df = temp_df.drop('Grade', axis=1)
                grade_removed = True

                # Save the modified dataframe back to the file
                # Read the first row (report title) separately
                with pd.ExcelFile(new_file) as xls:
                    # Read first row as header to get the report title
                    title_df = pd.read_excel(xls, header=None, nrows=1)

                # Write back to Excel with the title row and modified data
                with pd.ExcelWriter(new_file, engine='openpyxl') as writer:
                    # Write title row
                    title_df.to_excel(writer, index=False, header=False, startrow=0)
                    # Write modified data (with headers) starting at row 2
                    temp_df.to_excel(writer, index=False, startrow=1)

        except Exception as e:
            print(f"Warning: Could not process file: {e}")
            # If we can't read the file, assume it has enrollment
            has_enrollment = True

        # Clean the instructor name (remove extra spaces, commas, etc.)
        instructor = clean_filename(str(row['Instructor']).strip())
        semester = str(row['Semester']).strip().title()
        year = str(int(row['Year']))
        course = str(row['Course']).strip()
        ccn = str(row['CCN']).zfill(5)

        # Add "No Enrollment" suffix if needed
        enrollment_suffix = " - No Enrollment" if not has_enrollment else ""

        # Create new filename: [Semester] [Year] - [Instructor] - [Course] [CCN] - No Enrollment (if applicable)
        new_filename = f"{semester} {year} - {instructor} - {course} {ccn}{enrollment_suffix}{ext}"
        new_filepath = os.path.join(download_dir, new_filename)

        # Handle duplicate filenames
        counter = 1
        base_filename = f"{semester} {year} - {instructor} - {course} {ccn}{enrollment_suffix}"
        while os.path.exists(new_filepath):
            new_filename = f"{base_filename} ({counter}){ext}"
            new_filepath = os.path.join(download_dir, new_filename)
            counter += 1

        # Rename the file
        try:
            os.rename(new_file, new_filepath)
            status_msg = f"Downloaded and renamed: {new_filename}"
            if not has_enrollment:
                status_msg = f"Downloaded and renamed (NO ENROLLMENT): {new_filename}"
            if grade_removed:
                status_msg += " [Grade column removed]"
            print(status_msg)
            return True
        except Exception as e:
            print(f"Error renaming file: {e}")
            return False
    else:
        print(
            f"Download timeout for: {row['Semester']} {row['Year']} - {row['Instructor']} - {row['Course']} {row['CCN']}")
        return False


def run_report(x):
    # Get snapshot of existing files BEFORE triggering download
    existing_files = set(os.listdir(download_dir))

    if int(x["Year"]) > 2010:
        driver.get(roster_url)
        wait(term_search)
        select = Select(driver.find_element('id', 'InputKeys_E_ADDR_TYPE'))
        xpath(term_search).send_keys(str(x["term"]))
        xpath(subject_field).clear()
        xpath(subject_field).send_keys(str(x["prog"]))
        xpath(ccn_field).clear()
        xpath(ccn_field).send_keys(str(x["CCN"]).zfill(5))
        select.select_by_value('CAMP')
    else:
        driver.get(older_roster_url)
        wait(older_term_search)
        xpath(older_term_search).send_keys(str(x["term"]))
        xpath(older_ccn_field).clear()
        xpath(older_ccn_field).send_keys(str(x["CCN"]).zfill(5))

    xpath(results).click()

    # Wait a moment for the download to initiate
    time.sleep(2)

    # Rename the downloaded file (pass existing files set)
    rename_downloaded_file(x, download_dir, existing_files)

    # Add a small delay between reports to prevent overlap
    time.sleep(1)


def main():
    # Use the login function with OUR driver instance
    sis_day_time.login.login_sis(driver, xpath, wait)
    wait("""//*[@id="win0hdrdivPT_TITLE_CONT"]""")
    df.apply(run_report, axis=1)


if __name__ == '__main__':
    main()