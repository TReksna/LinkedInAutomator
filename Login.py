import time, shutil
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
import os
from Humanlike import *
from BrowserManagement import *
from selenium.common.exceptions import InvalidArgumentException
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import traceback



def try_credentials(driver, email, password):

    try:
        wait = WebDriverWait(driver, 10)
        user_field = wait.until(
            ec.visibility_of_element_located((By.ID, "session_key")))
    except Exception:
        return

    pass_field = driver.find_element(By.ID, "session_password")

    fill_text(user_field, email)
    fill_text(pass_field, password)

    driver.find_element(By.CLASS_NAME, "sign-in-form__submit-button").click()
    t0 = time.time()
    while time.time() - t0 < 10:

        if "Your account has been restricted" in driver.page_source or "Access to your account has been temporarily restricted" in driver.page_source:
            time.sleep(5)
            print("ACCOUNT RESTRICTED!")

            driver.quit()

            return "Restricted"
        if "Let's do a quick security check" in driver.page_source:
            print("Security check")

            driver.set_window_position(0, 0, windowHandle='current')
            time.sleep(100)
            if "Let's do a quick security check" in driver.page_source:
                driver.quit()
                return "Security check"
            else:
                return "Success"

        if "Couldn’t find a LinkedIn account associated with this email. Please try again." in driver.page_source:

            driver.quit()

            return "Nonexistant LinkedIn account email"
    return "Success"
    # input("What happened?")
    # driver.quit()

def innitialise_linkedin(driver, email, password):

    t0 = time.time()
    while True:
        if time.time() - t0 >12:
            input("?")
            return False
        driver.get("https://www.linkedin.com/feed/")
        try:
            wait = WebDriverWait(driver, 2)
            wait.until(ec.visibility_of_element_located((By.CLASS_NAME, 'global-nav__content')))
            return True
        except Exception:

            print("Navigation bar not found, assuming new login")
            driver.get("https://www.linkedin.com/checkpoint/lg/sign-in-another-account")

        try:
            wait = WebDriverWait(driver, 1)
            wait.until(ec.visibility_of_element_located((By.ID, 'artdeco-global-alert-container')))
            driver.find_element(By.XPATH, "//button[text()[contains(.,'Accept')]]").click()
        except Exception:
            print("Cookie prompt not found")

        try:
            wait = WebDriverWait(driver, 2)
            username = wait.until(ec.visibility_of_element_located((By.NAME, 'session_key')))
            print(username.get_attribute('value'))
            if username.get_attribute('value') != email:
                username.send_keys(Keys.CONTROL + "a")
                username.send_keys(Keys.DELETE)
                username.send_keys(email)
                pass_field = driver.find_element(By.ID, "password")
                pass_field.send_keys(Keys.CONTROL + "a")
                pass_field.send_keys(Keys.DELETE)
                pass_field.send_keys(password)
            driver.find_element(By.XPATH, "//button[text()[contains(.,'Sign in')]]").click()
            time.sleep(1)
        except Exception:
            continue

        if "That's not the right password." in driver.page_source:
            return False
        if "Couldn’t find a LinkedIn account associated with this email." in driver.page_source:
            return False
        if "Let's do a quick security check" in driver.page_source:
            input("Solve capcha")
            continue


def move_to_small_screen(driver):
    if driver.get_window_position()['x'] < 1912:
        driver.set_window_position(1922, 0, windowHandle='current')
        driver.maximize_window()

def openChrome(proxy=None, profilepath=None):

    chrome_options = webdriver.ChromeOptions()
    if proxy:
        chrome_options.add_argument('--proxy-server=%s' % proxy)
    if profilepath:
        chrome_options.add_argument("user-data-dir=%s" % profilepath)

    try:
        driver = webdriver.Chrome(chrome_options = chrome_options)
    except Exception:
        traceback.print_exc()
        return None

    move_to_small_screen(driver)

    return driver

def initialLogin(email, password):

    if not os.path.exists(f"C:/Profiles/{email}"):
        os.mkdir(f"C:/Profiles/{email}")


    driver = openChrome(profilepath=f"C:/Profiles/{email}")

    driver.get("https://www.linkedin.com/")

    try_credentials(driver, email, password)

    return driver


