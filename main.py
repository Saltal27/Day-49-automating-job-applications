from selenium import webdriver
import selenium.common.exceptions
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import os
import time


# my credentials
MY_PASSWORD = os.environ.get("MY_PASSWORD")
MY_PHONE_NUMBER = os.environ.get("MY_PHONE_NUMBER")

# driver path
chrome_driver_path = "C:\Development\chromedriver.exe"

options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)
service = Service(executable_path=chrome_driver_path)
driver = WebDriver(service=service, options=options)
driver.maximize_window()

driver.get("https://www.linkedin.com/jobs/search/?currentJobId=3537742905&f_AL=true&f_WT=2&geoId=92000000&keywords"
           "=python%20developer&location=Worldwide&refresh=true&sortBy=R")

# Signing in to my LinkedIN account
sign_in = driver.find_element(By.LINK_TEXT, 'Sign in')
sign_in.click()

email = driver.find_element(By.NAME, 'session_key')
email.send_keys('omarmobarak53@gmail.com')

password = driver.find_element(By.NAME, 'session_password')
password.send_keys(MY_PASSWORD)

sign_in_2nd = driver.find_element(By.XPATH, '//*[@id="organic-div"]/form/div[3]/button')
sign_in_2nd.click()
time.sleep(35)

# Looping through jobs applications
jobs_applications = driver.find_elements(By.CSS_SELECTOR, '.artdeco-entity-lockup__title a')
for job_application in jobs_applications:
    # Locating the link_element which I want to open in a new tab
    link_element = job_application
    link = link_element.get_attribute("href")

    # Simulating a Ctrl+Click action to open the link_element in a new tab
    link_element.send_keys(Keys.CONTROL + Keys.RETURN)

    # Switching to the new tab
    driver.switch_to.window(driver.window_handles[-1])

    # Verifying that the new tab has loaded the expected URL
    if driver.current_url == link:
        print("Link opened successfully in a new tab")
    else:
        print("Failed to open link_element in a new tab")

    # clicking the Easy Apply button (if it exists)
    try:
        easy_apply = driver.find_element(By.CSS_SELECTOR, '.jobs-apply-button span')
    except selenium.common.exceptions.NoSuchElementException:
        print("No application button, skipped.")
    else:
        easy_apply.click()

        # inserting my phone number
        phone_num = driver.find_element(By.CSS_SELECTOR, '.artdeco-text-input--container input')
        if phone_num.text == "":
            phone_num.send_keys(MY_PHONE_NUMBER)

        # submitting the job application (if it is a simple job application that only requires my phone number)
        submit_application = driver.find_element(By.CSS_SELECTOR, 'footer .display-flex button span')
        if submit_application.text == "Submit application":
            submit_application.click()
            print("applied successfully!")
        elif submit_application.text == "Next":
            print("Complex application, skipped.")
        else:
            print("Error")

        # pressing the tiny little x
        close_button = driver.find_element(By.CSS_SELECTOR, ".artdeco-modal__dismiss")
        close_button.click()

    # closing the new tab and switching back to the original tab
    driver.close()
    driver.switch_to.window(driver.window_handles[0])
