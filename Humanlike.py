from selenium import webdriver
from selenium.webdriver.common.by import By
import time, random
import numpy as np

def fill_text(element, text, finish_pause=True):

    av = 0.121/4
    std = 0.011/4

    for letter in text:
        time.sleep(abs(np.random.normal(loc=av, scale=std)))
        element.send_keys(letter)

    if finish_pause:
        time.sleep(abs(np.random.normal(loc=2, scale=0.5)))

def pause():
    time.sleep(abs(np.random.normal(loc=2, scale=0.5)))

def mini_pause():
    time.sleep(abs(np.random.normal(loc=0.5, scale=0.02)))

def scroll_to_elem(driver, element):

    while True:

        el_y = element.location.get('y')
        win_y = driver.execute_script('return window.pageYOffset')
        win_height = driver.execute_script('return document.documentElement.clientHeight')
        # print("Element location: {}, window view range: {}, {}".format(el_y, win_y, win_y + win_height))

        if el_y > win_y and el_y < win_y + win_height:
            break

        scroll_len = round(abs(np.random.normal(loc=5, scale=1)))*100

        if win_y > el_y:

            scroll_len = -scroll_len

        # print(scroll_len)

        scroll_loc = str(win_y+scroll_len)

        driver.execute_script("window.scrollTo({ top: "+scroll_loc+", behavior: 'smooth' })")
        mini_pause()

def scroll_back_up(driver):
    while True:

        el_y = 100
        win_y = driver.execute_script('return window.pageYOffset')
        win_height = driver.execute_script('return document.documentElement.clientHeight')
        # print("Element location: {}, window view range: {}, {}".format(el_y, win_y, win_y + win_height))

        if el_y > win_y and el_y < win_y + win_height:
            break

        scroll_len = round(abs(np.random.normal(loc=5, scale=1)))*100

        if win_y > el_y:

            scroll_len = -scroll_len

        # print(scroll_len)

        scroll_loc = str(win_y+scroll_len)

        driver.execute_script("window.scrollTo({ top: "+scroll_loc+", behavior: 'smooth' })")
        mini_pause()

def scroll_to_elem_extra(driver):


    win_y = driver.execute_script('return window.pageYOffset')
    win_height = driver.execute_script('return document.documentElement.clientHeight')
    # print("Element location: {}, window view range: {}, {}".format(el_y, win_y, win_y + win_height))


    # print(scroll_len)

    scroll_loc = str(win_y+win_height+500)

    driver.execute_script("window.scrollTo({ top: "+scroll_loc+", behavior: 'smooth' })")
    mini_pause()

# driver.execute_script("window.scrollTo({ top: 200, behavior: 'smooth' })")
# time.sleep(1)
# driver.execute_script("window.scrollTo({ top: 200, behavior: 'smooth' })")
# time.sleep(1)
# driver.execute_script("window.scrollTo({ top: 200, behavior: 'smooth' })")
# time.sleep(1)

# message_box = driver.find_element(By.XPATH, '//div[@aria-label="Write a message…"]')
# sample_text = "The probability density function of the normal distribution, " \
#               "first derived by De Moivre and 200 years later by both Gauss and " \
#               "Laplace independently [2], is often called the bell curve because of its characteristic " \
#               "shape (see the example below)."
#
# fill_text(message_box, sample_text)