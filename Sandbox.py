from CustomEmailManager import check_mail
from ProxyManagement import *
from BrowserManagement import *
from Login import *
import pandas as pd
import os, random

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

def log_df(email):

    with open(fr"X:\Profiles\\{email}\log.txt", "r", encoding="utf-8") as file:
        dict_list = [ast.literal_eval(d.replace("\n","")) for d in file.readlines()]

        df = pd.DataFrame(dict_list)
        df = df[df['ip'].notna()]

        return df

def make_all_login_xlxs():
    elist = list(os.listdir(r"X:\Profiles"))
    df_list = []
    for email in elist:
        try:
            df = log_df(email)
            df = df.dropna(axis=1, how='all')
            g = df.iloc[0]
            df = df.fillna({'email':g['email'], 'password':g['password'],'first_name':g['first_name'],'last_name':g['last_name']})
            df_list.append(df)
        except Exception:
            print("ERROR:", email)

    df_all = pd.concat(df_list, ignore_index=True)
    df_all.to_excel("oldAll.xlsx")

df_all = pd.read_excel("oldAll.xlsx", index_col=0)
port = 0
elist = [e for e in list(os.listdir(r"X:\Profiles")) if e not in pd.read_csv("OldAccStatus.csv", index_col=0)['email'].unique()]
star_l = len(elist)
random.shuffle(elist)
for n, email in enumerate(elist):

    print(email)
    st_df = pd.read_csv("OldAccStatus.csv", index_col=0)
    print("TOTAL", star_l, "REMAINING", star_l-n)
    if email in st_df['email'].unique():
        continue
    try:
        df = log_df(email)
    except Exception:
        continue
    last_ip = df.iloc[-1]['ip']
    all_ips = df['ip'].unique()
    last_city = df.iloc[-1]['city'].replace(" ","")
    last_country = df.iloc[-1]['country']
    print(last_ip, last_city, last_country)
    if last_city == 'Vancouver':
        last_country =None
    passw = df['password'].unique()[0]

    info = manage_connection(port=port, return_driver=False, country=last_country, ip=last_ip, city=last_city)
    # driver, info = manage_connection(data_dir=fr"X:\Profiles\\{email}\ChromeData", ip=last_ip, city=last_city)

    print(info)

    if not info['ip']:
        continue

    if info['ip'] in all_ips:
        driver = start_driver(port=port, data_dir=fr"X:\Profiles\\{email}\ChromeData")

    else:
        df_ip = df_all[df_all['ip'] == info['ip']]
        if len(df_ip) > 0:
            for eml in df_ip['email'].unique():
                if eml not in st_df['email'].unique():
                    email = eml
                    print("FOUND ALTERNATIVE ACC:", email)
                    df = log_df(email)
                    passw = df['password'].unique()[0]
                    driver = start_driver(port=port, data_dir=fr"X:\Profiles\\{email}\ChromeData")
                    break
            else:
                continue
        else:
            continue


    alive = innitialise_linkedin(driver, email, passw)
    if alive == "Time too long":
        continue
    conections = ""
    if alive:

        try:
            conections = WebDriverWait(driver, 10).until(
                ec.visibility_of_element_located((By.XPATH, '//a[@href="/mynetwork/"]//*[@class="feed-identity-widget-item__stat"]'))).text
        except Exception:
            conections = ""

    status_dict = {"email":email, "ip":last_ip, "alive":alive, "conections":conections, "city":last_city}


    ft_df = pd.DataFrame([status_dict])
    st_df = pd.concat([st_df, ft_df], ignore_index=True)
    st_df.to_csv("OldAccStatus.csv")
    time.sleep(40*random.random())
    driver.quit()

# print(connect(3))
# print(session_info(3))
# driver = BrowserDebug(dport = 8950, data_dir=r"C:\Profiles\shse3rdohm@outlook.com", proxy_server="private.residential.proxyrack.net:10003")
# #
