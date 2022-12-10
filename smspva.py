import requests, json, time

def getInfo():
    getbalance = "http://smspva.com/priemnik.php?metod=get_balance&apikey=uaMZWvWeMAnuiZGrRFUtcTNSGuH8yh"
    response = requests.get(getbalance)

    balance = response.json()['balance']

    getcount = "http://smspva.com/priemnik.php?metod=get_count_new&service=opt8&apikey=uaMZWvWeMAnuiZGrRFUtcTNSGuH8yh&country=US"
    response = requests.get(getcount)

    try:

        count = response.json()['online']

    except Exception:

        print("Number count not located")
        count = None

    return balance, count

def getNumber(pause_time=0):
    while True:
        try:
            balance, count = getInfo()
            break
        except Exception:
            print("SMSpva balance could not be obtained. Trying again in one minute")
            time.sleep(60)
    print("Phone numbers remaining:",count,"Money remaining:",balance,"This is enough for",int(float(balance)/0.18),"US phone verifications")
    if float(balance) < 0.2:
        input("Please add money to SMSPVA")
    getnumber = "http://smspva.com/priemnik.php?metod=get_number&country=US&service=opt8&apikey=uaMZWvWeMAnuiZGrRFUtcTNSGuH8yh"
    response = requests.get(getnumber).json()
    print(response)

    if not response['number']:
        pause_time += 1
        print("Number not obtained. Trying again after", pause_time, "seconds")
        time.sleep(pause_time)
        return getNumber(pause_time)

    return response

def getSms(id):

    getsmsms = "http://smspva.com/priemnik.php?metod=get_sms&country=US&service=opt8&id="+str(id)+"&apikey=uaMZWvWeMAnuiZGrRFUtcTNSGuH8yh"
    response = requests.get(getsmsms)

    return response.json()

def denial(id):

    query = "http://smspva.com/priemnik.php?metod=denial&country=US&service=opt8&id={}&apikey=uaMZWvWeMAnuiZGrRFUtcTNSGuH8yh".format(id)
    response = str(requests.get(query))
    print(response)


def ban(id):

    query = "http://smspva.com/priemnik.php?metod=ban&service=opt8&apikey=uaMZWvWeMAnuiZGrRFUtcTNSGuH8yh&id={}".format(id)
    response = str(requests.get(query))
    print(response)


def getNumber_smsactivate():

    query = "https://api.sms-activate.org/stubs/handler_api.php?api_key=10deb4Af6f00c4e9d14ee85dc4b60A7b&action=getNumber&service=tn&country=36"

    response = str(requests.get(query))

    numresponse = {"id":response.split(":")[1], "number":response.split(":")[2][1:]}
    return numresponse


