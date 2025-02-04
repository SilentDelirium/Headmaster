# Headmaster alpha v1 (headmaster_a1)
# credit to: SilntDlrium
# this is a python script used to access and manipulate the site for the online school, "Michigan Connections Academy"
#
# SET UP THE 'my_info.py' WITH YOUR INFORMATION, OR THIS WILL FAIL IMMEDIATELY
#
# It will (hopefully) be able to:
# - open a Chrome browser (headless or non)
# - access the connections website
# - sign in to the adult account
# - if today is a school day: fill in an "8" , if not, it fills in a "0"
# - retrieve if any assignments are marked for completion
# - if yes; send how many
# - if yes; mark them as completed
# - if yes and successful; send a verification that (number) of assignments has been successfully marked complete
# - exit script (or keep open depending on "my_info.py//keep_open")
import logging
import time
from datetime import date

# normal school day count
import numpy as np
from my_info import (is_summer, days_left, login_url, username_id, password_id, submit_button_id, username,
                     password, success_url, home_url, assignments_url, off_days, attendance_url, last_day)
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

# = begin code

start = date(2024, 9, 8)
end = date(2025, 6, 7)

school_days_left = np.busday_count(date.today(), last_day, holidays=off_days)

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

driver = webdriver.Chrome()

# Number of retries
max_retries = 3

assignments = 0

today = date.today()

no_school = False


def is_school_day(t, o):
    # Check if today is in the list of days with no school
    if t in o:
        return False

    # Check if today is a weekend (Saturday or Sunday)
    if today.weekday() >= 5:
        return False

    # If neither condition is met, it's a school day
    return True


if is_school_day(t=today, o=off_days):
    no_school = False
else:
    no_school = True
if no_school:
    print("There is NO SCHOOL today!")
else:
    print("Today IS a school day.")

if is_summer:
    print("Summer break has been activated!")
else:
    print("It is currently NOT summer break.")
    print("There are " + str(days_left) + " days until summer break.")
    print('Number of school days left is: ', school_days_left)


def do_login():
    driver.get(login_url)
    WebDriverWait(driver, 10).until(EC.url_contains(login_url))

    print("Login url reached")

    # Find the username, password fields, and submit button using the imported IDs
    username_field = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, username_id)))
    # print("username field found")

    submit_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, submit_button_id)))
    # print("submit field found")

    # Fill in the username using the imported credentials
    username_field.send_keys(username)
    # print("username field keys sent")

    password_field = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, password_id)))
    # print("password field found")

    password_field.send_keys(password)
    # print("password field keys sent")

    # Click the submit button
    submit_button.click()
    # print("submit clicked")

    # Wait for the success URL to appear
    WebDriverWait(driver, 10).until(EC.url_contains(success_url))

    # Check if the login was successful by verifying the current URL against the success URL
    if success_url in driver.current_url:
        logger.info("Login Successful!")

        # Navigate directly to the home URL
        driver.get(home_url)
        WebDriverWait(driver, 10).until(EC.url_contains(home_url))
        if home_url in driver.current_url:
            logger.info("Navigated to the home URL.")
            driver.back()
            print("Finished logging in.")
        driver.get(home_url)
        WebDriverWait(driver, 10).until(EC.url_contains(home_url))


def do_attendance():
    # Part b: attendance
    # navigate to the Attendance URL
    driver.get(attendance_url)
    WebDriverWait(driver, 10).until(EC.url_contains(attendance_url))
    logger.info("Arrived at Attendance URL.")
    # Identify and select attendance boxes
    if no_school:
        hours = 0
    else:
        hours = 8
    web_user = "4181429"
    student_id = "97221"
    # BELOW changing today to an off_day / weekend ###
    attendance_field_id = str((web_user + "_" + date.strftime(today, "%m%d%Y") + "_" + student_id))
    # ABOVE
    hours_input = driver.find_element(By.ID, attendance_field_id)
    print("Table ID matched!")
    print(hours, " hours to input for today.")
    hours_input.clear()
    hours_input.send_keys(hours)
    # Locate and click the "Save" button
    save_button = driver.find_element(By.ID, value="save")
    save_button.click()
    print("Successfully saved ", hours, " hours for today.")
    logger.info("Finished with Attendance tasks.")


def do_assignments(number_of_assignments):
    # Part a: assignments
    # decide if there are assignments to be marked
    time.sleep(2)
    # try:
    # this bit used to work, they changed ids and shit, fuckers
    # if driver.find_element(By.PARTIAL_LINK_TEXT, "lesson"):
    #    pull_text = driver.find_element(By.PARTIAL_LINK_TEXT, "lesson")
    # else:
    #    pull_text = driver.find_element(By.PARTIAL_LINK_TEXT, "lesson")
    # logger.info(pull_text)
    # today_assignments, temp = pull_text.split(' ', 1)
    # today_assignments = int(today_assignments)
    # today_assignments = int(driver.find_element(By.CLASS_NAME, "field"))
    # print(today_assignments)
    # except NoSuchElementException:
    # logger.warning("Element with partial link text 'lessons' not found. Skipping assignment processing.")
    # logger.warning("Element with class name 'field' not found. Skipping assignment processing.")
    # today_assignments = 0

    # global assignments
    # assignments = today_assignments
    # print(f"There are {assignments} assignments to mark today.")
    driver.get(assignments_url)
    WebDriverWait(driver, 10).until(EC.url_contains(assignments_url))
    # Identify and select drop-down forms
    # Count the number of <select> elements on the page using JavaScript
    drop_down_forms_count = int(driver.execute_script("return document.getElementsByTagName('select').length"))

    # this bit has been edited... I changed from matching lesson number from the home page
    # rather than match that to drop-downs found, i'm just mashing through the drop-downs. fuck it

    logger.info(f"Found {drop_down_forms_count} assignment drop-down forms.")

    # Check if the number of drop-down forms matches the number of assignments
    if drop_down_forms_count > 0:

        # Loop through drop-down forms and select "Completed"
        for i in range(drop_down_forms_count):
            # Locate the drop-down element
            drop_down = driver.find_element(By.XPATH, f"(//select)[{i + 1}]")  # Adjust index if necessary

            # Click on the drop-down to open options
            drop_down.click()

            # Locate and click the "Completed" option
            completed_option = driver.find_element(By.XPATH, f"(//select)[{i + 1}]/option[text()='Completed']")
            completed_option.click()

        # Locate and click the "Save" button
        save_button = driver.find_element(By.ID, value="save")
        save_button.click()

        logger.info("Marked all assignments as 'Completed'.")

        # logger.warning("Number of drop-down forms does not match the number of assignments.")
    else:
        logger.info("There are no assignments to mark today.")

    time.sleep(3)
    print("Assignments section is complete.")
    time.sleep(3)


do_login()

do_assignments(assignments)

do_attendance()

print("Task Complete")
