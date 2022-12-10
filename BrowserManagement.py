from selenium import webdriver
import os, time
import socket, errno
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import traceback

def is_port_in_use(dport):

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        s.bind(("127.0.0.1", dport))
    except socket.error as e:
        if e.errno == errno.EADDRINUSE:
            print("Port is already in use")
            return True
        else:
            # something else raised the socket.error exception
            print(e)
            input("")

    s.close()
    return False


def BrowserDebug(dport = 8990, data_dir = "C:\Profiles\olgertsz", proxy_server = None):

    os_command = 'cd C:\Program Files\Google\Chrome\Application & chrome.exe --remote-debugging-port={}'.format(dport)
    if data_dir:
        os_command += ' --user-data-dir="{}"'.format(data_dir)
    if proxy_server:
        os_command += ' --proxy-server="{}"'.format(proxy_server)

    if not is_port_in_use(dport):
        print("Opening chrome in debug mode")
        os.popen(os_command)
        time.sleep(3)

    s = Service('chromedriver.exe')
    opt = Options()
    opt.add_experimental_option("debuggerAddress", "localhost:{}".format(dport))

    driver = webdriver.Chrome(options=opt, service=s)
    return driver

# def connectDebugChrome(dport="8990"):
#     s = Service('chromedriver.exe')
#     opt = Options()
#     opt.add_experimental_option("debuggerAddress", "localhost:{}".format(dport))
#
#
#     driver = webdriver.Chrome(options=opt, service=s)
#     return driver

def openChrome(proxy=None, data_dir=None):

    chrome_options = webdriver.ChromeOptions()
    if proxy:
        chrome_options.add_argument('--proxy-server=%s' % proxy)
    if data_dir:
        chrome_options.add_argument("user-data-dir=%s" % data_dir)

    try:
        driver = webdriver.Chrome(chrome_options=chrome_options)
    except Exception:
        traceback.print_exc()
        return None



    return driver

def get_user_path(driver):

    driver.get("chrome://version/")
