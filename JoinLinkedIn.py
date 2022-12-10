from ProxyManagement import *
import pandas as pd
from BrowserManagement import *
port = 4
df_emails = pd.read_csv("Data/new_emails.csv")

mail_acc = df_emails.iloc[0]

print(connect(port))
s_info = session_info(port)

proxy_info = pd.Series({"addr":f"private.residential.proxyrack.net:1000{port}", "ip":s_info['ipinfo']['ip'],
              "city":s_info['ipinfo']['city'], "country":s_info['ipinfo']['country']})
print(proxy_info)

acc = pd.concat([mail_acc,proxy_info])
print(acc)

driver = BrowserDebug(dport=8990, data_dir="C:\Profiles\\"+mail_acc['mail'], proxy_server=proxy_info["addr"])
df = pd.DataFrame()
df[proxy_info['ip']] = proxy_info
df.to_csv("Data/StartedAccs.csv")