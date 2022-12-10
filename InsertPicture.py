import time, os, random
import sys
sys.path.append(r"C:\Users\User\Desktop\TargetLinkedIn")
from WriteLog import write_log
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

def if_no_pic_put(driver):

    home_url = "https://www.linkedin.com/feed/"
    if driver.current_url != home_url:
        driver.get(home_url)

    for a in driver.find_elements_by_tag_name("a"):
        link = a.get_attribute("href")
        if "add-photo/photo" in link:
            driver.get(link)
            upload_pic(driver)
            return

    if len(driver.find_elements_by_class_name("ghost-person")) > 1:
        driver.find_element_by_class_name("feed-identity-module__member-photo").click()
        photo_edits = []
        t0 = time.time()
        while len(photo_edits) < 1:
            photo_edits = driver.find_elements_by_class_name("pv-top-card__edit-photo-button")
            time.sleep(0.5)
            print("Looking for photo edit butto")
            if time.time() - t0 > 10:
                return
        photo_edits[0].click()
        upload_pic(driver)
        return

def upload_pic(driver):

    profile_url = driver.current_url


    newpath = r"C:\Users\User\Desktop\ProfileBuilder\BuildigProfiles\Pictures\New\\"
    oldpath = r"C:\Users\User\Desktop\ProfileBuilder\BuildigProfiles\Pictures\Used\\"
    driver.find_element_by_id("image-selector__file-upload-input").send_keys(newpath + os.listdir(newpath)[0])

    time.sleep(1)

    driver.find_element_by_xpath('//*[@data-control-name="profile_photo_crop_save"]').click()
    time.sleep(5)
    os.replace(newpath + os.listdir(newpath)[0], oldpath + os.listdir(newpath)[0])
    email = driver.desired_capabilities['chrome']['userDataDir'].split("\\")[2]
    write_log(email, {'action': 'picture inserted'})
    write_log(email, {'profile url':profile_url})

#
# def putpic(driver):
#
#     home_url = "https://www.linkedin.com/feed/"
#
#     if driver.current_url != home_url:
#         driver.get(home_url)
#
#     newpath = r"C:\Users\User\Desktop\TargetLinkedIn\BuildigProfiles\Pictures\New\\"
#     oldpath = r"C:\Users\User\Desktop\TargetLinkedIn\BuildigProfiles\Pictures\Used\\"
#
#     for a in driver.find_elements_by_tag_name("a"):
#         link = a.get_attribute("href")
#         if "add-photo/photo" in link:
#             driver.get(link)
#             break
#
#     time.sleep(2)
#
#     driver.find_element_by_id("image-selector__file-upload-input").send_keys(newpath+os.listdir(newpath)[0])
#
#     time.sleep(1)
#
#     driver.find_element_by_xpath('//*[@data-control-name="profile_photo_crop_save"]').click()
#     time.sleep(5)
#     os.replace(newpath+os.listdir(newpath)[0], oldpath+os.listdir(newpath)[0])
#     email = driver.desired_capabilities['chrome']['userDataDir'].split("\\")[2]
#     write_log(email, {'action':'picture inserted'})

def onboarding_putpic(driver):

    newpath = r"X:\Pictures\New\\"
    oldpath = r"X:\Pictures\Used\\"

    time.sleep(1)

    wait = WebDriverWait(driver, 20)
    wait.until(ec.visibility_of_element_located((By.CLASS_NAME, 'onboarding-photo__add-button')))

    # print(os.listdir(newpath))
    file = random.choice(os.listdir(newpath))
    driver.find_element_by_id("onboarding-photo__add-button-input").send_keys(newpath + file)

    time.sleep(1)

    driver.find_element_by_xpath('//*[@data-control-name="profile_photo_crop_save"]').click()
    time.sleep(5)

    os.replace(newpath + file, oldpath + file)

