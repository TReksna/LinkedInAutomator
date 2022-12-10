import pandas as pd
from ProxyManagement import *
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
df = pd.read_csv("SJ/signups.csv")
used_proxies = df['ip'].unique()
print(pd.Timestamp.now())
driver, info = manage_connection(3)
print(info)
if info['ip'] in used_proxies:
    input("?")
driver.get("https://datametrics101.com")


email = "hugo9npzri@outlook.de"
password = "sHhqz8qr8"

join = WebDriverWait(driver, 100).until(
    ec.presence_of_element_located((By.CLASS_NAME, "join-now")))
join.click()
while True:
    try:
        time.sleep(10)
        driver.find_element(By.XPATH, '//*[@class="sign-up-popup"]//input[@name="email"]').send_keys(email)
        break
    except Exception:
        print("No email")
time.sleep(5)
driver.find_element(By.ID, "terms-checkbox").click()

time.sleep(2)
driver.find_element(By.XPATH, '//*[@class="sign-up-popup"]//*[@class="join-now"]').click()
new_dict = {"ip":info["ip"],"city":info["city"],"email":email,"password":"","time":pd.Timestamp.now()}
df = df.append(new_dict, ignore_index=True)
df.to_csv("SJ/signups.csv")
input(" ?")