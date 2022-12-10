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
        driver.find_element(By.XPATH, '//*[@id="join-form-submit"]').click()
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


def number_verification_2(driver):

    iframe = driver.find_element(By.XPATH, "//iframe[@class='challenge-dialog__iframe']")
    driver.switch_to.frame(iframe)
    numresopnse = getNumber()
    count_verif()
    fill_text(driver.find_element(By.NAME, "phoneNumber"), numresopnse['number'])
    next = driver.find_element(By.XPATH, "//*[text()[contains(.,'Submit')]]")
    driver.execute_script("arguments[0].click();", next)
    print(numresopnse['number'])
    time.sleep(5)
    if "You can't use this phone number.  Please try a different one." in driver.page_source:
        driver.switch_to.default_content()
        # driver.find_element(By.XPATH, '//*[@class="challenge-dialog__close"]').click()
        # number_verification_1(driver)
        return number_verification_2(driver)
    else:
        driver.switch_to.default_content()
        return numresopnse

def number_verification_3(driver, numresopnse):
    iframe = driver.find_element(By.XPATH, "//iframe[@class='challenge-dialog__iframe']")
    driver.switch_to.frame(iframe)
    for i in range(45):
        time.sleep(5)
        smsresponse = getSms(numresopnse['id'])
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
    number_verification_1(driver)
    numresopnse = number_verification_2(driver)
    return number_verification_3(driver, numresopnse)