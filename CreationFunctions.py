from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.common.exceptions import *
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from Browsing import move_to_small_screen
from AuthBrowsing import connect_new_ip, connect_us
import os, time, traceback, random, ast
from CreateLinkedIn.MailRu import solve_mail_ru_capcha
from Humanlike import fill_text, pause, scroll_to_elem, mini_pause
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import *
from CreateLinkedIn.smspva import *
from CreateLinkedIn.InsertPicture import onboarding_putpic
from WriteLog import write_log, log_genesis, get_genesis
from CreateLinkedIn.ProfileDataManager import update_col, get_value
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
# from InviteByList import invite
# from ReportCreation import report_creation_tele
from fake_useragent import UserAgent
from AuthBrowsing import session_info
from CreateLinkedIn.ProfileDataManager import *
from CreateLinkedIn.zip_finder import zip_state_from_city, random_zip
from Emails.CustomEmailManager import check_mail, get_email_pin


def find_correct_tab(driver, url, printing=False):

    for n, handle in enumerate(driver.window_handles):
        if len(driver.window_handles) > 0:
            driver.switch_to(handle)
        this_url = driver.current_url
        if printing:
            print("Tab Nr.{} URL:{}".format(n, url))
        if url in this_url:
            return True


def count_verif(read=False):
    with open("CreateLinkedIn/PhoneVerification.txt", "r") as file:
        n = int(file.read()) + 1
    if read:
        return str(n-1)
    with open("CreateLinkedIn/PhoneVerification.txt", "w") as file:
        file.write(str(n))

def number_verification_1(driver):

    security_attempts = 0
    while True and security_attempts < 6:
        time.sleep(1)
        try:
            driver.find_element(By.XPATH, '//*[@id="join-form-submit"]').click()
        except Exception:
            print("Join click intercepted, trying without")

        time.sleep(3)
        try:

            iframe = driver.find_element(By.XPATH, "//iframe[@class='challenge-dialog__iframe']")
            driver.switch_to.frame(iframe)
            try:
                pause()
                driver.find_element(By.XPATH, '//*[@name="phoneNumber"]')
                select = driver.find_element(By.ID, "select-register-phone-country")

                if select.get_attribute('value') != "us":
                    print(select.get_attribute('value'))
                    select.click()
                    pause()
                    for option in driver.find_elements(By.TAG_NAME, "option"):
                        if "United States" in option.text:
                            option.click()
                            pause()
                driver.switch_to.default_content()
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


def number_verification_2(driver, email):
    if get_value(email, 'phone_attempts') > 5:
        print("NUMBER FAIL!!!")
        raise Exception("number fail")

    iframe = driver.find_element(By.XPATH, "//iframe[@class='challenge-dialog__iframe']")
    driver.switch_to.frame(iframe)
    numresopnse = getNumber()
    count_verif()
    try:
        fill_text(driver.find_element(By.NAME, "phoneNumber"), numresopnse['number'])
    except Exception:
        raise Exception("number fail")
    next = driver.find_element(By.XPATH, "//*[text()[contains(.,'Submit')]]")
    driver.execute_script("arguments[0].click();", next)
    update_value(email, 'phone_attempts', get_value(email, 'phone_attempts')+1)
    print(numresopnse['number'])
    time.sleep(5)
    if "You can't use this phone number.  Please try a different one." in driver.page_source:
        ban(numresopnse['id'])
        driver.switch_to.default_content()
        # driver.find_element(By.XPATH, '//*[@class="challenge-dialog__close"]').click()
        # number_verification_1(driver)
        return number_verification_2(driver, email)
    else:
        driver.switch_to.default_content()
        return numresopnse

def number_verification_3(driver, numresopnse, email):
    iframe = driver.find_element(By.XPATH, "//iframe[@class='challenge-dialog__iframe']")
    driver.switch_to.frame(iframe)
    for i in range(45):
        time.sleep(5)
        if "You have exceeded the maximum number of code requests" in driver.page_source:
            raise Exception("number fail")
        try:
            smsresponse = getSms(numresopnse['id'])
        except Exception:
            print("Can't get SMS response")
            continue
        print(i, smsresponse)
        if smsresponse['sms']:
            fill_text(driver.find_element(By.NAME, "pin"), smsresponse['sms'])
            next = driver.find_element(By.XPATH, "//*[text()[contains(.,'Submit')]]")
            driver.execute_script("arguments[0].click();", next)
            return
        elif i % 15 == 0:
            resend = driver.find_element_by_class_name("btn__resend_link")
            resend.click()
    driver.switch_to.default_content()
    driver.find_element(By.CLASS_NAME, "challenge-dialog__close").click()
    denial(numresopnse['id'])
    number_verification_1(driver)
    numresopnse = number_verification_2(driver, email)
    return number_verification_3(driver, numresopnse, email)

def initial_mailru_login(driver, creation):
    email = creation['email']
    password = creation['password']

    if "mail.ru/login" not in driver.current_url:
        driver.get("https://account.mail.ru/login")

    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.NAME, 'username'))).send_keys(
        email.replace("@mail.ru", ""))
    time.sleep(0.5)

    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//*[@type="submit"]'))).click()
    time.sleep(2)

    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.NAME, 'password'))).send_keys(password)
    time.sleep(0.5)

    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//*[@type="submit"]'))).click()
    time.sleep(1)

    print("Email sign in clicked")

    for _ in range(10):
        if "Это точно вы? Введите код с картинки, чтобы войти в аккаунт" in driver.page_source:
            print("Found capcha prompt")
            break
        try:
            driver.find_element(By.XPATH, '//*[@id="mailbox"]/form[1]/div[2]/input').send_keys(
                password)
            driver.find_element(By.XPATH, '//*[@id="mailbox"]/form[1]/button[2]').click()
            break
        except Exception:
            time.sleep(1)

def initial_linkedin_visit(driver):

    print("Starting intial LinkedIn visit")

    li_signup_link = 'https://www.linkedin.com/signup'

    driver.execute_script("window.open('https://www.linkedin.com/signup');")
    driver.switch_to.window(driver.window_handles[-1])
    pause()
    # if driver.current_url != li_signup_link:
    #
    #     ActionChains(driver) \
    #         .key_down(Keys.CONTROL) \
    #         .send_keys('T') \
    #         .key_up(Keys.CONTROL) \
    #         .perform()
    #     driver.switch_to.window(driver.window_handles[-1])
    #     pause()
    #     if driver.current_url != li_signup_link:
    #         driver.execute_script("window.open('');")
    #         driver.switch_to.window(driver.window_handles[-1])
    #         driver.get('https://www.linkedin.com/signup')


def linkedin_fill_mail(driver, creation):
    email = creation['email']
    password = creation['password']

    try:
        WebDriverWait(driver, 4).until(ec.visibility_of_element_located((By.XPATH, '//*[@id="join-form__welcome-button"]'))).click()
    except TimeoutException:
        print("No join button located")

    print("Looking for email field")
    t0 = time.time()
    while (time.time()-t0<30):
        try:
            fill_text(driver.find_element(By.XPATH, '//*[@id="email-address"]'), email)
            break
        except (ElementNotInteractableException, NoSuchElementException):
            try:
                fill_text(driver.find_element(By.XPATH, '//*[@id="email-or-phone"]'), email)
                break
            except (ElementNotInteractableException, NoSuchElementException):
                try:
                    driver.find_element(By.CLASS_NAME, "join-with-button__text").click()
                except Exception:
                    continue

    pause()
    print("Filling password")
    try:
        fill_text(driver.find_element(By.XPATH, '//*[@id="password"]'), password)
    except Exception:
        raise Exception("Can't connect to LinkedIn")
    pause()

    print("Hitting enter")
    actions = ActionChains(driver)
    actions = actions.send_keys(Keys.RETURN)
    actions.perform()
    pause()

    if "Someone’s already using that email." in driver.page_source:
        driver.close()
        raise Exception("Someone’s already using that email.")

    try:
        driver.find_element(By.XPATH, '//*[@action-type="ACCEPT"]').click()
        print("Cookies clicked")
        pause()
    except Exception:
        print("No cookie prompt")

    pause()

def linkedin_fill_name(driver, creation, n = 0):
    firstname = creation['first_name']
    lastname = creation['last_name']

    print("Filling  name")

    wait = WebDriverWait(driver, 10)
    try:
        name_field = wait.until(
            ec.visibility_of_element_located((By.XPATH, '//*[@id="first-name"]')))
    except Exception:
        try:
            driver.find_element(By.CLASS_NAME, "join-form__form-body-submit-button").click()
            pause()
            if n > 10:
                driver.refresh()
                pause()
                linkedin_fill_mail(driver, creation)
            return linkedin_fill_name(driver, creation, n+1)

        except Exception:
            raise Exception("Sign up name error")
    pause()

    fill_text(name_field, firstname)
    fill_text(driver.find_element(By.XPATH, '//*[@id="last-name"]'), lastname)
    mini_pause()
    print("Hitting enter")
    actions = ActionChains(driver)
    actions = actions.send_keys(Keys.RETURN)
    actions.perform()
    pause()
    with open("CreateLinkedIn/PhoneVerification.txt", "w") as file:
        file.write("0")

    with open("CreateLinkedIn/user_agents_verified.txt", "r") as agent_file:
        verified_agents = agent_file.read()
    try:
        if creation['agent'] not in verified_agents:
            with open("CreateLinkedIn/user_agents_verified.txt", "a") as agent_file:
                print("Adding user agent to list of verified agents")
                agent_file.write(creation['agent'] + "\n")
    except KeyError:
        print("Avoiding agent file")

def cold_join_cPanel(driver, creation):
    email = creation['email']
    password = creation['password']
    firstname = creation['first_name']
    lastname = creation['last_name']

    driver.get("https://www.linkedin.com/signup")
    pause()
    linkedin_fill_mail(driver, creation)
    pause()
    linkedin_fill_name(driver, creation)
    number_verification_1(driver)
    numresopnse = number_verification_2(driver, email)
    number_verification_3(driver, numresopnse, email)

    time.sleep(3)

    genesis = {"email": email, "password": password, "first_name": firstname, "last_name": lastname,
               'ip': creation['ip'],
               'city': creation['city']}#, 'user_agent': creation['user_agent']}
    print(genesis)


    # update_col(email, 'phone_verified', True)
    return driver, genesis

def cold_join(driver, creation):
    email = creation['email']
    password = creation['password']
    firstname = creation['first_name']
    lastname = creation['last_name']


    t_start = time.time()

    initial_mailru_login(driver, creation)
    initial_linkedin_visit(driver)

    print(driver.current_url)
    if 'linkedin' not in driver.current_url:

        driver.switch_to.window(driver.window_handles[-1])
        print(driver.current_url)
        if 'linkedin' not in driver.current_url:
            driver.switch_to.window(driver.window_handles[0])
            print(driver.current_url)
    pause()


    linkedin_fill_mail(driver, creation)
    pause()
    linkedin_fill_name(driver, creation)
    driver.switch_to.window(driver.window_handles[-1])
    number_verification_1(driver)

    driver.switch_to.window(driver.window_handles[0])
    mail_ru_url = driver.current_url

    if "Это точно вы? Введите код с картинки, чтобы войти в аккаунт" in driver.page_source:
        capcha_prompt = True
        print("Capcha prompt located")

    else:

        capcha_prompt = False

    driver.switch_to.window(driver.window_handles[1])
    pause()

    numresopnse = number_verification_2(driver, email)

    if capcha_prompt:
        t0 = time.time()
        driver.switch_to.window(driver.window_handles[0])

        solve_mail_ru_capcha(driver)

        driver.switch_to.window(driver.window_handles[1])
        print("Capcha solved in {} seconds".format(round(time.time()-t0)))
    else:
        print("Mail.ru logged in without capcha. Sleeping 20 seconds for number verification")
        try:
            driver.find_element(By.XPATH, "//span[text()[contains(.,'Accept')]]").click()
            print("Mail ru cookies accepted")
        except Exception:
            print("Mail ru cookies not found")
        time.sleep(20)

    number_verification_3(driver, numresopnse, email)

    time.sleep(3)



    genesis = {"email": email, "password": password, "first_name": firstname, "last_name": lastname, 'ip':creation['ip'],
               'city':creation['city'],  'user_agent':creation['user_agent']}
    print(genesis)

    print("Total time for first part: {} seconds (approx {} minutes)".format(round(time.time()-t_start), round((time.time()-t_start)/60)))
    update_col(email, 'phone_verified', True)
    return driver, genesis

def rnd_zip():

    with open("CreateLinkedIn/GeneratedData/zips.txt", "r", encoding="utf-8") as file:
        for n, line in enumerate(file):
            if n>random.randint(2, 30000):
                return line.replace("\n","")


def profile_location(driver, email):

    try:
        add_postal_state(email, get_value(email, 'city'))
    except Exception:
        # try:
        #     country_input = driver.find_element(By.XPATH, '//input[@id="typeahead-input-for-country"]')
        #     country = country_input.get_attribute('value')
        #     area = driver.find_element(By.XPATH, '//input[@id="typeahead-input-for-location-within-picker"]').get_attribute(
        #         'value')
        #     if country == "United States":
        #         state = area.split(", ")[-1]
        #
        #         update_col(email, 'state', state)
        #         update_col(email, 'postal', zip)
        print("State was not updated in sql")



    while "profile-location" not in driver.current_url:
        print("Waiting for profile-location, current url:")
        print(driver.current_url)
        if "mail.ru" in driver.current_url:
            desired_handle = [handle for handle in driver.window_handles if handle != driver.current_window_handle][0]

            driver.switch_to.window(desired_handle)
        pause()
    country_input = driver.find_element(By.XPATH, '//input[@id="typeahead-input-for-country"]')
    country = country_input.get_attribute('value')
    # postal = driver.find_element(By.XPATH, '//input[@id="typeahead-input-for-postal-code"]').get_attribute('value')
    # area = WebDriverWait(driver, 10).until(
    #     ec.visibility_of_element_located(
    #         (By.XPATH, '//*[@class="onboarding-profile-location__field-container"]'))).get_attribute('value')
    try:
        postal = WebDriverWait(driver, 10).until(
            ec.visibility_of_element_located(
                (By.XPATH, '//input[@id="typeahead-input-for-postal-code"]'))).get_attribute('value')
        area = WebDriverWait(driver, 10).until(
            ec.visibility_of_element_located((By.XPATH, '//*[@class="onboarding-profile-location__field-container"]'))).get_attribute('value')
    except TimeoutException:
        postal = None
        area = None

    logdict = {'action':'linkedin assumed location', 'country':country, 'postal':postal, 'area': area}
    write_log(email, logdict)

    if country_input.get_attribute('value') != "United States":
        print(country_input.get_attribute('value'))

        for _ in range(2):
            try:
                country_input.clear()
                pause()
                fill_text(country_input,"United States")
                pause()
                driver.find_element(By.XPATH, '//div[@role="option"]').click()
                pause()
                break
            except Exception:
                continue
        postal_input = driver.find_element(By.XPATH, '//input[@id="typeahead-input-for-postal-code"]')
        postal = get_value(email, 'postal')
        print(postal)
        if not postal:
            postal = random_zip()
        fill_text(postal_input, postal)
        wait = WebDriverWait(driver, 10)
        wait.until(
            ec.visibility_of_element_located((By.XPATH, '//*[@class="onboarding-profile-location__field-container"]')))
        pause()

        country_input = driver.find_element(By.XPATH, '//input[@id="typeahead-input-for-country"]')
        country = country_input.get_attribute('value')
        postal = driver.find_element(By.XPATH, '//input[@id="typeahead-input-for-postal-code"]').get_attribute('value')
        try:
            area = driver.find_element(By.XPATH, '//input[@id="typeahead-input-for-location-within-picker"]').get_attribute(
                'value')
        except Exception:
            area = None
        logdict = {'action': 'edited location', 'country': country, 'postal': postal, 'area': area}
        write_log(email, logdict)

    else:
        try:
            postal_input = driver.find_element(By.XPATH, '//input[@id="typeahead-input-for-postal-code"]')
            postal = postal_input.get_attribute('value')
            update_col(email, 'postal', postal)
        except Exception:
            print("No postal code located")
        try:
            area = driver.find_element(By.XPATH, '//input[@id="typeahead-input-for-location-within-picker"]').get_attribute(
                'value')
            update_col(email, 'area', area)
        except Exception:
            print("No Area located")

    # fill_text(driver.find_element(By.XPATH, '//input[@id="typeahead-input-for-postal-code"]'),genesis['postal'])
    for i in range(15):
        time.sleep(1)
        print(i)
        if "profile-location" not in driver.current_url:
            print("Profile-location complete")
            return
        try:
            next = driver.find_element(By.XPATH, "//*[text()[contains(.,'Next')]]")
        except Exception:
            print("Next not found")
            continue
        if i % 3 == 0:
            try:
                next.click()
                print("Next clicked via selenium")
            except Exception:
                print("Next can't be clicked via selenium")
            pause()
        elif i % 2 == 0:
            driver.execute_script("arguments[0].click();", next)
            print("Next clicked via javascript")
            pause()

def profile_edit(driver, email):

    mostrecentcompany = get_value(email, 'company')
    jobtitle = get_value(email, 'job')
    mostrecentcompany = get_value(email, 'company')

    while "profile-edit" not in driver.current_url:
        print("Waiting for profile-edit, current url:")
        print(driver.current_url)
        pause()

    wait = WebDriverWait(driver, 10)
    job_title_field = wait.until(
        ec.visibility_of_element_located((By.XPATH, '//input[@id="typeahead-input-for-title"]')))
    pause()

    # extract_jobs(driver)
    fill_text(job_title_field,jobtitle)

    pause()

    for element in driver.find_element_by_class_name("search-basic-typeahead").find_elements_by_tag_name("span"):
        try:
            if jobtitle.lower() in element.get_attribute("innerHTML").lower():
                driver.execute_script("arguments[0].click();", element)
                break
        except Exception:
            continue

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

        select_industy = get_value(email, 'industry')

        for option in driver.find_elements(By.TAG_NAME, "option"):

            if "select_industy" in option.get_attribute("innerHTML"):
                option.click()
                break
    pause()
    next = driver.find_element(By.XPATH, "//*[text()[contains(.,'Continue')]]")
    driver.execute_script("arguments[0].click();", next)

def extract_jobs(driver):

    wait = WebDriverWait(driver, 10)
    job_title_field = wait.until(
        ec.visibility_of_element_located((By.XPATH, '//input[@id="typeahead-input-for-title"]')))
    pause()

    jobs = ["Student", "Intern", "Researcher", "Trainee", "Assistant", "Graduate"]

    suggested_jobs = []

    for jobtitle in jobs:

        fill_text(job_title_field, jobtitle)

        for element in driver.find_element_by_class_name("search-basic-typeahead").find_elements_by_tag_name("span"):
            suggested_jobs.append(element.text+"\n")
        with open(r"CreateLinkedIn/suggested_jobs.txt", "a", encoding="utf-8") as file:
            file.writelines(suggested_jobs)

        job_title_field.clear()



def handle_confirmation(driver, email):

    while "handle-confirmation" not in driver.current_url:
        print("Waiting for handle-confirmation, current url:")
        print(driver.current_url)
        pause()

    driver.switch_to.window(driver.window_handles[0])
    pin = None
    driver.refresh()
    t_mess = time.time()
    refreshed = False
    while len(driver.find_elements(By.XPATH, '//span[@class="ll-sj__normal"]')) < 1:
        if time.time() - t_mess > 120 and not refreshed:
            driver.refresh()
            refreshed = True
        if time.time() - t_mess > 240:
            raise Exception("Out of message time")
        if "Укажите резервную почту, чтобы войти в аккаунт" in driver.page_source:
            second_email = get_value(email, "second_email")
            driver.find_element(By.TAG_NAME, "input").send_keys(second_email)
            driver.find_element(By.XPATH, '//button[@type="submit"]').click()
            print("2nd email")
        print("Waiting for messages")
        time.sleep(2)
    tw0 = time.time()

    while True:
        titles = driver.find_elements(By.XPATH, '//span[@class="ll-sj__normal"]')
        print("Total {} messages found".format(len(titles)))
        try:
            for title in [x.text for x in titles]:
                print(title)
                if "your pin is " in title:
                    pin = title.split("your pin is ")[1].split(".")[0]
                    break
        except Exception:
            print("Can't get all titles")
        if pin:
            break
        print("No pin recieved yet")
        time.sleep(1)
        if time.time() - tw0 > 30:
            driver.refresh()
            tw0 = time.time()
    driver.switch_to.window(driver.window_handles[-1])
    conf = driver.find_element(By.ID, "email-confirmation-input")
    fill_text(conf, pin)
    pause()
    driver.find_element(By.XPATH, "//*[text()[contains(.,'Agree')]]").click()
    time.sleep(1)
    if "not the right code" in driver.current_url:
        handle_confirmation(driver, email)
    update_col(email, 'is_email_verified', 'True')

def handle_confirmation(driver, email):

    while "handle-confirmation" not in driver.current_url:
        print("Waiting for handle-confirmation, current url:")
        print(driver.current_url)
        pause()

    pin = get_email_pin(email, get_genesis(email)["password"])

    conf = driver.find_element(By.ID, "email-confirmation-input")
    fill_text(conf, pin)
    pause()
    driver.find_element(By.XPATH, "//*[text()[contains(.,'Agree')]]").click()
    time.sleep(1)
    if "not the right code" in driver.current_url:
        handle_confirmation(driver, email)
    update_col(email, 'is_email_verified', 'True')

def job_seeker_intent(driver):
    while "job-seeker-intent" not in driver.current_url:
        print("Waiting for handle-confirmation, current url:")
        print(driver.current_url)
        pause()

    driver.find_element(By.XPATH, "//span[text()[contains(.,'Not now')]]").click()
    pause()

def abook_import(driver):
    while "abook-import" not in driver.current_url:
        print("Waiting for handle-confirmation, current url:")
        print(driver.current_url)
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
    with open("CreateLinkedIn/onboarding_connections.txt", "r", encoding="windows-1252") as file:
        onctext = file.read()
    if text in onctext:
        print("FOUND:", text)
        return True
    return False

def people_you_may_know(driver, email, conrange=(5,20)):
    while "people-you-may-know" not in driver.current_url:
        print("Waiting for people_you_may_know, current url:")
        print(driver.current_url)
        pause()
    all_possible_connections = driver.find_elements(By.XPATH, '//li-icon[@type="plus-icon"]')
    tc0 = time.time()

    while len(all_possible_connections) < 7:
        time.sleep(1)
        all_possible_connections = driver.find_elements(By.XPATH, '//li-icon[@type="plus-icon"]')
        if time.time() - tc0 > 15:
            break
    condict = {}

    if conrange[1] > 0:

        maxcons = random.randint(conrange[0], conrange[1])
        for smax in range(int((conrange[1]-conrange[0])/10)):
            print("Will the count be between {} and {}?".format(conrange[0]+10*smax, conrange[0]+10*(smax+1)))
            if random.random() > 0.5:
                print("Yes!")
                maxcons = random.randint(conrange[0]+10*smax, conrange[0]+10*(smax+1))
                break
            else:
                print("No!")
        print("Count will be", maxcons)

        # maxcons = 1

        concount = 0
        wigetcards = driver.find_elements(By.CLASS_NAME, "onboarding-card-widget__card")


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
            with open("CreateLinkedIn/onboarding_connections.txt", "r", encoding="windows-1252") as file:
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

                with open("CreateLinkedIn/onboarding_connections.txt", "a", encoding="windows-1252") as file:
                    file.write(text)


        onboarding_dict = {'action': 'onboarding connects', 'count': str(len(condict)), 'targets': str(condict)}

        write_log(email, onboarding_dict)

        print(onboarding_dict)
        print(email)


        driver.find_element(By.XPATH, "//span[text()[contains(.,'Add')]]").click()
        pause()
    else:
        pause()
        driver.find_element(By.XPATH, "//span[text()[contains(.,'Skip')]]").click()
        pause()

def profile_photo(driver):
    while "profile-photo" not in driver.current_url:
        print("Waiting for profile_photo, current url:")
        print(driver.current_url)
        pause()
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
    try:
        driver.find_element(By.XPATH, "//span[text()[contains(.,'Continue')]]").click()
        pause()
    except Exception:
        try:
            con = driver.find_element(By.XPATH, "//span[text()[contains(.,'Continue')]]")
            driver.execute_script("arguments[0].click();", con)
        except Exception:
            return

def get_the_app(driver):
    while "get-the-app" not in driver.current_url:
        print("Waiting for get_the_app, current url:")
        print(driver.current_url)
        pause()
    for _ in range(20):
        try:
            driver.find_element(By.XPATH, "//span[text()[contains(.,'Skip')]]").click()
            pause()
            return
        except NoSuchElementException:
            try:
                driver.find_element(By.XPATH, "//span[text()[contains(.,'Next')]]").click()
                pause()
                return
            except NoSuchElementException:
                try:
                    driver.find_element(By.XPATH, "//span[text()[contains(.,'Finish')]]").click()
                    pause()
                    return
                except NoSuchElementException:
                    print("Looking for next or continue")
    print("next or continue not found")
    raise Exception


def follow_recomendations(driver):
    while "follow-recommendations" not in driver.current_url:
        print("Waiting for follow-recommendation, current url:")
        print(driver.current_url)
        pause()
    follows = []
    t0 = time.time()
    while len(follows) < 10 and time.time() - t0 < 15:
        follows = [x for x in driver.find_elements(By.TAG_NAME, "button") if "Follow" in x.get_attribute("innerHTML")]
        pause()
    if len(follows) > 1:

        sample_follows = random.sample(follows, random.randint(5, 10))
        for follow in sample_follows:
            scroll_to_elem(driver, follow)
            driver.execute_script("arguments[0].click();", follow)
            pause()
    try:
        driver.find_element(By.XPATH, "//span[text()[contains(.,'Finish')]]").click()
        print("Finish clicked!")
    except Exception:
        print("could not find finish :(")

    with open("CreateLinkedIn/settings/created_wait.txt", "r") as wfile:
        sleep_time = float(wfile.read())
        print(f"Sleeping for {sleep_time} seconds")
        time.sleep(sleep_time)

    

def career_accelerator_intent(driver):
    # Neither of these
    try:
        pause()
        driver.find_element(By.XPATH, "//span[text()[contains(.,'Neither of these')]]").click()
        pause()
    except Exception:
        traceback.print_exc()
        try:
            pause()
            driver.find_element(By.XPATH, "//span[text()[contains(.,'here for something else')]]").click()
            pause()
        except Exception:
            traceback.print_exc()


def selector(driver, email, job, invite_suggested=False, invite_list=True):


    print("crruent url:", driver.current_url)

    past_url = None
    refresh_count = 0



    while "feed" not in driver.current_url:
        for u in range(20):

            if past_url == driver.current_url:
                print(u, past_url)
                if u == 19:
                    driver.refresh()
                    refresh_count += 1
                    break
                time.sleep(1)
            else:
                break
        # if refresh_count > 3:
        #     raise Exception

        past_url = driver.current_url
        if "mail.ru" in driver.current_url:
            driver.switch_to.window(driver.window_handles[-1])
            print("focused on wring tab")
            print(driver.current_url)
            if "mail.ru" in driver.current_url:
                print("still focused on wring tab")
                driver.switch_to.window(driver.window_handles[0])
                print(driver.current_url)
        if "career-accelerator-intent" in driver.current_url:
            career_accelerator_intent(driver)
        if "profile-location" in driver.current_url:
            profile_location(driver, email)
        elif "profile-edit" in driver.current_url:
            profile_edit(driver, email)
        elif "handle-confirmation" in driver.current_url:
            handle_confirmation(driver, email)
        elif "job-seeker-intent" in driver.current_url:
            job_seeker_intent(driver)
        elif "abook-import" in driver.current_url:
            abook_import(driver)
        elif "people-you-may-know" in driver.current_url:
            people_you_may_know(driver, email)
        elif "profile-photo" in driver.current_url:
            profile_photo(driver)
        elif "get-the-app" in driver.current_url:
            get_the_app(driver)
        elif "follow-recommendations" in driver.current_url:
            follow_recomendations(driver)
        time.sleep(2)

    # if invite_list:
    #     try:
    #         invite(driver, email)
    #     except Exception:
    #         traceback.print_exc()
    #         input("List invite error?")

    with open("CreateLinkedIn/pause.txt", "r") as pfile:
        if "True" in pfile.read():
            input("Stopping due to pause.txt")

# def selectorCpanel(driver, email, job, invite_suggested=False, invite_list=True):
#
#
#     print("crruent url:", driver.current_url)
#
#     past_url = None
#     refresh_count = 0
#
#     while "feed" not in driver.current_url:
#         for u in range(20):
#
#             if past_url == driver.current_url:
#                 print(u, past_url)
#                 if u == 19:
#                     driver.refresh()
#                     refresh_count += 1
#                     break
#                 time.sleep(1)
#             else:
#                 break
#         # if refresh_count > 3:
#         #     raise Exception
#
#         past_url = driver.current_url
#
#         if "career-accelerator-intent" in driver.current_url:
#             career_accelerator_intent(driver)
#         if "profile-location" in driver.current_url:
#             profile_location(driver, email)
#         elif "profile-edit" in driver.current_url:
#             profile_edit(driver, email)
#         elif "handle-confirmation" in driver.current_url:
#             handle_confirmation(driver, email)
#         elif "job-seeker-intent" in driver.current_url:
#             job_seeker_intent(driver)
#         elif "abook-import" in driver.current_url:
#             abook_import(driver)
#         elif "people-you-may-know" in driver.current_url:
#             people_you_may_know(driver, email)
#         elif "profile-photo" in driver.current_url:
#             profile_photo(driver)
#         elif "get-the-app" in driver.current_url:
#             get_the_app(driver)
#         elif "follow-recommendations" in driver.current_url:
#             follow_recomendations(driver)
#         time.sleep(2)
#
#     # if invite_list:
#     #     try:
#     #         invite(driver, email)
#     #     except Exception:
#     #         traceback.print_exc()
#     #         input("List invite error?")
#
#     with open("CreateLinkedIn/pause.txt", "r") as pfile:
#         if "True" in pfile.read():
#             input("Stopping due to pause.txt")

def report(details):
    with open("CreateLinkedIn/BuildReport.txt", "a", encoding="utf-8") as file:
        file.write(str(details)+"\n")
    with open("CreateLinkedIn/BuildReport.txt", "r", encoding="utf-8") as file:
        lines = file.readlines()

    r = [ast.literal_eval(x.replace("\n","")) for x in lines]

    if len(r) < 3:
        return

    # if not r[-1]['success'] and not r[-2]['success'] and not r[-2]['success']:
    #
    #     input("\n\n3 Fails in a row!")

def checkSMSPVA():

    balance, count = getInfo()
    print("Current SMSPVA balance:", balance, "USA phone numbers remaining:", count)
    while float(balance) < 0.2:
        print("Waiting for money in SMSPVA")
        time.sleep(60)
        balance, count = getInfo()
        print("Current balance:", balance, "USA phone numbers remaining:", count)

