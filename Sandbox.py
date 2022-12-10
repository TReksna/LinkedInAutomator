from CustomEmailManager import check_mail
from ProxyManagement import *
from BrowserManagement import *

print(connect(3))
print(session_info(3))
driver = BrowserDebug(dport = 8950, data_dir=r"C:\Profiles\shse3rdohm@outlook.com", proxy_server="private.residential.proxyrack.net:10003")
#

input("check mail?")
