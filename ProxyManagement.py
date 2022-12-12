import shlex, subprocess, ast, traceback, os, time, random, json
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from urllib.request import urlopen


from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
# proxyUptime=2h
import random

def move_to_small_screen(driver):
    if driver.get_window_position()['x'] < 1912:
        driver.set_window_position(1922, 0, windowHandle='current')
        driver.maximize_window()
    return driver

def connect(port, address="linkedin.com", country=None, city=None, ip=None):

    # with open("Context/usedIPs.txt", "r") as file:
    #     excluded = "-"+",-".join([x.replace("\n", "") for x in file.readlines()])

    # cmd = '''curl -x private.residential.proxyrack.net:1000{}
    # -U tomsr;country=LV;proxyIp={}:b85935-85f215-c382d5-e83421-2e4a57 {}'''.format(port, excluded, address)

    cmd = f'''curl -x private.residential.proxyrack.net:1000{port}
        -U maris29'''
    if country:
        cmd += f";country={country}"

    if city:
        cmd += f";city={city}"

    if ip:
        cmd += f";proxyIp={ip}"


    cmd += f":5f7e32-fac927-d56375-c4c5d9-baa613 {address}"

    print(cmd)
    args = shlex.split(cmd)
    process = subprocess.Popen(args, shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()


    dict_str = stdout.decode("UTF-8")

    # info = json.loads(dict_str)
    return (dict_str)

def session_info(port):
    cmd = '''curl -x private.residential.proxyrack.net:1000{} 
    -U maris29:5f7e32-fac927-d56375-c4c5d9-baa613 http://api.proxyrack.net/stats'''.format(port)

    args = shlex.split(cmd)
    process = subprocess.Popen(args, shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()


    dict_str = stdout.decode("UTF-8")
    # print("ProxyRack data:")
    try:
        info = json.loads(dict_str)
        # print("requestParams:",info['requestParams'])
        # print("ipinfo:", info['ipinfo'])
    except Exception:
        # print("JSON decode error")
        # print(dict_str)
        info = {'ipinfo':{'ip':None, 'country':None, 'city':None}}

    return(info)

def release(port):
    cmd = '''curl -x private.residential.proxyrack.net:1000{} 
    -U maris29:5f7e32-fac927-d56375-c4c5d9-baa613 http://api.proxyrack.net/release'''.format(port)
    args = shlex.split(cmd)
    process = subprocess.Popen(args, shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

def manage_connection(port=0, country=None, city=None, ip = None, data_dir=None, return_driver=True):

    release(port)

    connect(port, country=country, city=city, ip=ip)

    info = session_info(port)
    print(info['ipinfo'])

    tries = 0

    while True:


        if info['ipinfo']['ip']:

                break

        else:
            tries+=1


        release(port)
        if tries < 4:
            connect(port, country=country, ip=ip)
        else:
            if tries > 6:
                return {'ip':None}
            connect(port, country=country, city=city)
        time.sleep(1)

        info = session_info(port)

    return info['ipinfo']

def start_driver(port, data_dir):

    proxy = "private.residential.proxyrack.net:1000{}".format(port)

    caps = DesiredCapabilities().CHROME
    caps["pageLoadStrategy"] = "none"

    chrome_options = webdriver.ChromeOptions()

    chrome_options.add_argument('--proxy-server=%s' % proxy)

    s = Service("chromedriver.exe")
    if data_dir:
        chrome_options.add_argument("user-data-dir="+data_dir)
    driver = webdriver.Chrome(service=s, options=chrome_options, desired_capabilities=caps)

    driver = move_to_small_screen(driver)

    return driver

def rotating_usa(address = "ss.lv"):

    cmd = '''curl -x usa.rotating.proxyrack.net:9000
        -U maris29:af3939-155236-ef578f-f61ae4-234f92 {}'''.format(address)

    print(cmd)
    args = shlex.split(cmd)
    process = subprocess.Popen(args, shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()


    dict_str = stdout.decode("UTF-8")
    print(dict_str)

    print(connect(0))

    proxy = "usa.rotating.proxyrack.net:9000"
    caps = DesiredCapabilities().CHROME
    caps["pageLoadStrategy"] = "none"
    chrome_options = webdriver.ChromeOptions()

    chrome_options.add_argument('--proxy-server=%s' % proxy)

    s = Service("chromedriver.exe")
    # chrome_options.add_argument("user-data-dir="+r"C:\Users\User\Desktop\SSlvMessenger\Agent_user_directories\agent1")
    driver = webdriver.Chrome(service=s, options=chrome_options, desired_capabilities=caps)

    return driver


# driver.get("https://www.ss.lv/msg/lv/real-estate/plots-and-lands/riga-region/adazu-nov/adazi/U3QBGklqQl0=.html")
# input("?")
