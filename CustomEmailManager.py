import imaplib
import email, time
from email.header import decode_header
import webbrowser
import os

# account credentials
# username = "nastiukhanushakova@mail.ru"
# password = "erN1QETq7JdbuE4R6NmR"

def clean(text):
    # clean text for creating a folder
    return "".join(c if c.isalnum() else "_" for c in text)

def check_mail(username, password, server):

    mdl = []

    # create an IMAP4 class with SSL
    imap = imaplib.IMAP4_SSL(server)
    #  https://server40.areait.lv:2083
    # authenticate
    imap.login(username, password)

    status, messages = imap.select("INBOX")
    # number of top emails to fetch

    N = 10
    # total number of emails
    messages = int(messages[0])



    for i in range(1, messages+1):

        # fetch the email message by ID

        res, msg = imap.fetch(str(i), "(RFC822)")
        for response in msg:
            if isinstance(response, tuple):
                # parse a bytes email into a message object
                msg = email.message_from_bytes(response[1])
                # decode the email subject
                subject, encoding = decode_header(msg["Subject"])[0]
                if isinstance(subject, bytes):
                    # if it's a bytes, decode to str
                    subject = subject.decode(encoding)

                date = msg["Date"]
                # decode email sender
                From, encoding = decode_header(msg.get("From"))[0]

                if isinstance(From, bytes):
                    From = From.decode(encoding)

                To, encoding = decode_header(msg.get("To"))[0]

                if isinstance(From, bytes):
                    To = From.decode(encoding)

                # if the email message is multipart

                parts = list(msg.walk())



                for n, part in enumerate(parts):


                    try:
                        body = part.get_payload(decode=True).decode()
                        mdl_dict = {"from": From, "subject":subject, "date":date, "body":body, "to":To}
                        if mdl_dict not in mdl:
                            mdl.append(mdl_dict)
                    except Exception:
                        pass


    # close the connection and logout
    imap.close()
    imap.logout()
    return mdl

def get_emails(email, password):

    mdl = check_mail(email, password)
    print(len(mdl))

    messages = []

    for md in mdl:



        # print(md['from'], md['to'])

        if md['from'] == "SS.COM":
            body = md['body']
            # print(body)
            if "Jums ir jauns ziņojums no lietotāja " in body:
                author = body.split("Jums ir jauns ziņojums no lietotāja ")[-1].split(".")[0]
            else:
                author = body.split("You received a new message from ")[-1].split(".")[0]
            conv_link = body.split('href="')[-1].split('"')[0]
            messages.append({'date':md['date'], 'author':author, 'link':conv_link, 'to':md['to']})

    return messages

# while True:
#     mails = get_emails("agents.centrs@surveyacademydata.com","CentrsAgents2022!")
#     print(mails)
#     if len(mails) > 3:
#         break
#     else:
#         time.sleep(5)

