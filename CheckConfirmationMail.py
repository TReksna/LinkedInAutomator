from CustomEmailManager import *
# hugo9npzri@outlook.de,sHhqz8qr8,outlook.office365.com
# mails = check_mail("hugo9npzri@outlook.de","sHhqz8qr8", "outlook.office365.com")
mails = check_mail("shse3rdohm@outlook.com","Th8cau8rhzc", "outlook.office365.com")
# mails = check_mail("m7c7hdemo@outlook.com","hrff3zrY2ls", "outlook.office365.com")
# mails = check_mail('agesonob1989@mail.ru',"4KXrrUj5Lo", "imap.mail.ru")
for mail in mails:
    if mail['subject'] == "LinkedIn is better on the app":
        continue
    print(mail['subject'], mail['date'], mail['from'])

    # if len(mail['body']) < 500:
    #     print(mail['subject'], mail['date'], mail['from'])
    # else:
    #     print(mail)


# from bs4 import BeautifulSoup as bs
# root = mails[-1]['body'] #convert the generated HTML to a string
# soup = bs(root)                #make BeautifulSoup
# prettyHTML = soup.prettify()
#
# print(prettyHTML)