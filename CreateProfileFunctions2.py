from Browsing import openChrome
import time, traceback
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
import random, os
import ast
from datetime import datetime
from BuildigProfiles.InsertPicture import onboarding_putpic
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from BuildigProfiles.MailRu import get_pin, get_conf_link, get_pin_link
from WriteLog import write_log, log_genesis
import pandas as pd
from selenium.webdriver.common.keys import Keys
from popData import mail, company, job_postal
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from LaunchDebug import openDebugChrome, QuitDebugChrome
from BuildigProfiles.smspva import getNumber, getSms
from LaunchDebug import openDebugChrome, QuitDebugChrome
from BuildigProfiles.smspva import getNumber, getSms
import win32com.client as comclt
#test for git
from Humanlike import fill_text, pause, scroll_to_elem, mini_pause
def cold_join(driver, email, password, firstname, lastname):
    driver.get("https://www.linkedin.com/signup")
    wait = WebDriverWait(driver, 10)

    # join = wait.until(ec.visibility_of_element_located((By.ID, 'join-form__welcome-button')))
    #
    # join.click()

    while True:
        try:
            email_field = wait.until(ec.visibility_of_element_located((By.XPATH, '//*[@id="email-address"]')))
            break
        except Exception:
            try:
                email_field = wait.until(ec.visibility_of_element_located((By.XPATH, '//*[@id="email-or-phone"]')))
                break
            except Exception:
                traceback.print_exc()
                input("?")
                driver.refresh()

    fill_text(email_field, email)
    fill_text(driver.find_element(By.XPATH, '//*[@id="password"]'), password)
    actions = ActionChains(driver)
    actions = actions.send_keys(Keys.RETURN)
    actions.perform()
    time.sleep(2)

    if "Someone’s already using that email." in driver.page_source:
        driver.close()
        raise Exception("Someone’s already using that email.")

    try:
        driver.find_element(By.XPATH, '//*[@action-type="ACCEPT"]').click()
        print("Cookies clicked")
        pause()
    except Exception:
        print("No cookie prompt")
    fill_text(driver.find_element(By.XPATH, '//*[@id="first-name"]'),firstname)
    fill_text(driver.find_element(By.XPATH, '//*[@id="last-name"]'),lastname)

    security_attempts = 0

    while True and security_attempts < 6:

        driver.find_element(By.XPATH, '//*[@id="join-form-submit"]').click()
        time.sleep(3)
        try:
            iframe = driver.find_element(By.XPATH, "//iframe[@class='challenge-dialog__iframe']")
            driver.switch_to.frame(iframe)
            try:
                driver.find_element(By.XPATH, '//*[@name="phoneNumber"]')

                break
            except NoSuchElementException:
                security_attempts += 1
                print("Seurity attemts:", security_attempts)
                driver.switch_to.default_content()
                try:
                    driver.find_element(By.XPATH, '//*[@class="challenge-dialog__close"]').click()
                except ElementNotInteractableException:
                    continue

                time.sleep(3)
        except NoSuchElementException:
            break


    driver = verify_number(driver)
    return driver

def verify_number(driver):

    for attempt in range(5):
        print("Attempt number", attempt+1)
        pause()
        try:
            driver.find_element(By.ID, "select-register-phone-country").click()
        except Exception:
            driver.switch_to.default_content()

            driver.find_element(By.XPATH, '//*[@class="challenge-dialog__close"]').click()
            time.sleep(3)
            driver.find_element(By.XPATH, '//*[@id="join-form-submit"]').click()
            time.sleep(3)

            iframe = driver.find_element(By.XPATH, "//iframe[@class='challenge-dialog__iframe']")
            driver.switch_to.frame(iframe)
            return verify_number(driver)
        pause()
        for option in driver.find_elements(By.TAG_NAME, "option"):
            if "United States" in option.text:
                option.click()
                pause()
                break

        numresopnse = getNumber()

        fill_text(driver.find_element_by_name("phoneNumber"),numresopnse['number'])

        next = driver.find_element(By.XPATH, "//*[text()[contains(.,'Submit')]]")
        driver.execute_script("arguments[0].click();", next)
        # driver.find_element_by_name("pin").send_keys(smsresponse['sms'])
        print(numresopnse['number'])
        time.sleep(5)
        for i in range(25):
            if "profile-location" in driver.current_url:
                return driver
            if i % 7 == 0 and i > 0:
                resend = driver.find_element_by_class_name("btn__resend_link")
                resend.click()
            smsresponse = getSms(numresopnse['id'])
            print(i, smsresponse)
            if smsresponse['sms']:
                break
            time.sleep(5)
            if "You can't use this phone number.  Please try a different one." in driver.page_source:
                verify_number(driver)
        if smsresponse['sms']:
            fill_text(driver.find_element_by_name("pin"),smsresponse['sms'])
            next = driver.find_element(By.XPATH, "//*[text()[contains(.,'Submit')]]")
            driver.execute_script("arguments[0].click();", next)
            return driver
        else:
            try:
                driver.switch_to.default_content()
                driver.find_element(By.CLASS_NAME, "challenge-dialog__close").click()
            except Exception:
                traceback.print_exc()
                print(driver.page_source)
                input("??")


            driver.find_element_by_xpath('//*[@id="join-form-submit"]').click()
            time.sleep(3)
            iframe = driver.find_element_by_xpath("//iframe[@class='challenge-dialog__iframe']")
            driver.switch_to.frame(iframe)
    input("After 5 attempts phone number failed")
    return driver


def profile_location(driver, genesis=None):
    # country_input = driver.find_element(By.XPATH, '//input[@id="typeahead-input-for-country"]')
    # country_input.clear()
    # fill_text(country_input,"United States")
    # driver.find_element(By.XPATH, '//div[@role="option"]').click()
    # time.sleep(1)
    # fill_text(driver.find_element(By.XPATH, '//input[@id="typeahead-input-for-postal-code"]'),genesis['postal'])
    next = driver.find_element(By.XPATH, "//*[text()[contains(.,'Next')]]")
    driver.execute_script("arguments[0].click();", next)
    time.sleep(1)
    try:
        driver.find_element(By.XPATH, "//*[text()[contains(.,'Next')]]").click()
    except Exception:
        return

def handle_confirmation(driver, genesis):
    link = get_pin_link(genesis['email'], genesis['password'])
    driver.get(link)

def profile_edit(driver, jobtitle, mostrecentcompany="random"):

    # jobtitle = genesis['jobtitle'].capitalize()
    # mostrecentcompany = genesis['company']

    if mostrecentcompany == "random":
        with open("BuildigProfiles/GeneratedData/CompanyNames.txt", "r") as file:
            comp_lines = file.readlines()
        with open("BuildigProfiles/GeneratedData/CompanyNames.txt", "w") as file:
            file.writelines(comp_lines[1:])
        mostrecentcompany = comp_lines[0].replace("\n","")
    wait = WebDriverWait(driver, 10)
    job_title_field = wait.until(
        ec.visibility_of_element_located((By.XPATH, '//input[@id="typeahead-input-for-title"]')))
    pause()
    fill_text(job_title_field,jobtitle)

    for element in driver.find_element_by_class_name("search-basic-typeahead").find_elements_by_tag_name("span"):
        if jobtitle.lower() in element.get_attribute("innerHTML").lower():
            driver.execute_script("arguments[0].click();", element)
            break

    pause()
    emptype = driver.find_element(By.XPATH, '//select[@id="typeahead-input-for-employment-type-picker"]')
    driver.execute_script("arguments[0].click();", emptype)
    pause()
    emp1 = emptype.find_elements_by_tag_name("option")[1]
    emp1.click()
    pause()
    comp = driver.find_element_by_id("typeahead-input-for-company")
    fill_text(comp,mostrecentcompany)
    pause()
    comp.send_keys(Keys.RETURN)
    pause()

    industry = driver.find_elements(By.ID, "work-industry")
    if len(industry) > 0:
        industry[0].click()

        for option in driver.find_elements(By.TAG_NAME, "option"):
            if "Market Research" in option.get_attribute("innerHTML"):
                option.click()
                break
    pause()
    next = driver.find_element(By.XPATH, "//*[text()[contains(.,'Continue')]]")
    driver.execute_script("arguments[0].click();", next)

def job_seeker_intent(driver):
    pause()
    driver.find_element(By.XPATH, "//span[text()[contains(.,'Not now')]]").click()
    pause()

def abook_import(driver):
    pause()
    driver.find_element(By.XPATH, "//span[text()[contains(.,'Skip')]]").click()
    pause()
    driver.find_element(By.XPATH, "//button[text()[contains(.,'Skip')]]").click()
    pause()

def has_been_contacted(element):
    p = element.find_elements_by_tag_name("p")
    target_name = p[0].get_attribute("innerHTML").replace("\n", "").strip()
    target_job = p[1].get_attribute("innerHTML").replace("\n", "").strip()
    text = target_name + " ::::: " + target_job + "\n"
    text = ''.join([i if ord(i) < 128 else ' ' for i in text])
    with open("BuildigProfiles/onboarding_connections.txt", "r", encoding="windows-1252") as file:
        onctext = file.read()
    if text in onctext:
        print("FOUND:", text)
        return True
    return False

def people_you_may_know(driver, email, conrange=(25,40)):
    all_possible_connections = driver.find_elements_by_xpath('//li-icon[@type="plus-icon"]')
    tc0 = time.time()

    while len(all_possible_connections) < 7:
        time.sleep(1)
        all_possible_connections = driver.find_elements_by_xpath('//li-icon[@type="plus-icon"]')
        if time.time() - tc0 > 15:
            break
    condict = {}

    if conrange[1] > 0:

        maxcons = random.randint(conrange[0], conrange[1])

        # maxcons = 1

        concount = 0
        wigetcards = driver.find_elements_by_class_name("onboarding-card-widget__card")


        print("Before filtering {} targets available".format(len(wigetcards)))

        wigetcards = [w for w in wigetcards if not has_been_contacted(w)]


        # if len(wigetcards) < 1:
        #     break

        sample_wigetcards = random.sample(wigetcards, min(maxcons, len(wigetcards)))


        print("After filtering {} targets available".format(len(wigetcards)))

        print("Will connect to {} people".format(maxcons))

        for element in sample_wigetcards:

            scroll_to_elem(driver,element)

            if concount >= maxcons:
                break


            p = element.find_elements_by_tag_name("p")
            target_name = p[0].get_attribute("innerHTML").replace("\n", "").strip()
            target_job = p[1].get_attribute("innerHTML").replace("\n", "").strip()
            text = target_name + " ::::: " + target_job + "\n"
            text = ''.join([i if ord(i) < 128 else ' ' for i in text])
            with open("BuildigProfiles/onboarding_connections.txt", "r", encoding="windows-1252") as file:
                onctext = file.read()
            if text in onctext:
                print("FOUND:", text)
            else:
                icon = element.find_element(By.CLASS_NAME, 'onboarding-card__selectable-icon')
                con = icon.find_element(By.TAG_NAME, 'button')
                driver.execute_script("arguments[0].click();", con)

                pause()
                condict[target_name] = target_job
                concount += 1

                with open("BuildigProfiles/onboarding_connections.txt", "a", encoding="windows-1252") as file:
                    file.write(text)


        onboarding_dict = {'action': 'onboarding connects', 'count': str(len(condict)), 'targets': str(condict)}

        write_log(email, onboarding_dict)

        driver.find_element(By.XPATH, "//span[text()[contains(.,'Add')]]").click()
        pause()
    else:
        pause()
        driver.find_element(By.XPATH, "//span[text()[contains(.,'Skip')]]").click()
        pause()

def profile_photo(driver):
    try:
        driver.find_element(By.XPATH, "//span[text()[contains(.,'Continue')]]").click()
        pause()
        return
    except Exception:
        pass
    pause()
    onboarding_putpic(driver)
    pause()
    # write_log(genesis['email'], {'action': 'picture inserted during onboarding'})
    driver.find_element(By.XPATH, "//span[text()[contains(.,'Continue')]]").click()
    pause()
    try:
        con = driver.find_element(By.XPATH, "//span[text()[contains(.,'Continue')]]")
        driver.execute_script("arguments[0].click();", con)
    except Exception:
        return

def get_the_app(driver):
    pause()
    try:
        driver.find_element(By.XPATH, "//span[text()[contains(.,'Skip')]]").click()
    except NoSuchElementException:
        driver.find_element(By.XPATH, "//span[text()[contains(.,'Next')]]").click()
    pause()

def follow_recomendations(driver):
    follows = []

    while len(follows) < 10:
        follows = [x for x in driver.find_elements_by_tag_name("button") if "Follow" in x.get_attribute("innerHTML")]
        pause()
    sample_follows = random.sample(follows, random.randint(5, 10))
    for follow in sample_follows:
        scroll_to_elem(driver, follow)
        driver.execute_script("arguments[0].click();", follow)
        pause()
    follow_dict = {'action': 'onboarding follows', 'count': str(len(sample_follows))}

    # write_log(genesis['email'], follow_dict)

    driver.find_element(By.XPATH, "//span[text()[contains(.,'Finish')]]").click()
    print("Finish clicked!")

def gen_data_pop(filename):
    with open("BuildigProfiles/GeneratedData/"+filename, "r") as file:
        lines = file.readlines()
    with open("BuildigProfiles/GeneratedData/" + filename, "w") as file:
        file.writelines(lines[1:])

    return lines[0].replace("\n","")

def gen_data_random(filename):
    with open("BuildigProfiles/GeneratedData/"+filename, "r") as file:
        lines = file.readlines()
    return random.choice(lines).replace("\n","")

def sythetic_genesis(email="pop", password="pop", proxy=None, company="pop", jobtitle="Assistant Manager", postal="pop", experiment="Default", make_profile=True):

    if email == "pop" or password == "pop":
        mail_value = mail()
        email = mail_value.split(":")[0]
        password = mail_value.split(":")[1]

    if company == "pop":
        company = gen_data_pop("CompanyNames.txt")

    if postal == "pop":
        locline = gen_data_random("uszips.txt")
        postal = locline.split(";")[0]

    genesis = {'email': email, 'password': password, 'proxy': proxy,
               'company': company, 'jobtitle': jobtitle, 'postal': postal, 'experiment': experiment}

    if make_profile:

        profileinfopath = "X:\Profiles\\" + genesis['email']

        try:
            os.mkdir(profileinfopath)
        except FileExistsError:
            pass

        log_genesis(genesis)

    print(email)
    return genesis


def launch_chrome_debug(port=8988):

    opt = Options()
    opt.add_experimental_option("debuggerAddress", "localhost:{}".format(port))
    driver = webdriver.Chrome(options=opt, executable_path=r"C:\Users\User\Desktop\SurveyJunkie\chromedriver.exe")
    return driver

def decider(url):

    decsisons = {"cold-join":cold_join, "profile-location":profile_location,
                 "profile-edit":profile_edit, "handle-confirmation":handle_confirmation,
                 "job-seeker-intent":job_seeker_intent, "abook-import":abook_import,
                 "people-you-may-know":people_you_may_know,"profile-photo-upload":profile_photo,
                 "get-the-app":get_the_app, "follow-recommendations":follow_recomendations}

    for k, v in decsisons.items():
        if k in url:
            return v

def step(driver, genesis):
    pause()
    url = driver.current_url
    print(url)
    if "onboarding-landing" in url:
        return True
    try:
        f = decider(url)
        f(driver, genesis)
    except TypeError:
        step(driver, genesis)
    print(url)
    t0 = time.time()
    while url == driver.current_url and time.time()-t0<120:

        time.sleep(0.1)

        if time.time() - t0 > 60:
            print("Step taking unusually long time. Will reset in {} seconds".format(round(120-(time.time() - t0))))

    print(driver.current_url)
    time.sleep(1)

