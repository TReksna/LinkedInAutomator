from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import traceback

from selenium.webdriver.chrome.options import Options

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
        driver = webdriver.Chrome(executable_path="chromedriver.exe", options=chrome_options)
    except Exception:
        traceback.print_exc()
        return None

    move_to_small_screen(driver)

    return driver

def openOwnChrome(proxy=None):
    chrome_options = webdriver.ChromeOptions()
    if proxy:
        chrome_options.add_argument('--proxy-server=%s' % proxy)

    chrome_options.add_argument("user-data-dir=%s" % r"X:\Profiles\Main")

    driver = webdriver.Chrome(executable_path="chromedriver.exe", options=chrome_options)

    return driver

