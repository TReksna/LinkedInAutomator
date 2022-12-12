from datetime import datetime
import ast, random

def log_message_classification(email, target_name, targetlink, conv_link, target_interested):

    with open("X:\Profiles\\" + email + "\log.txt", "r", encoding="utf-8") as file:
        lines = file.readlines()

    for line in lines:
        line_dict = ast.literal_eval(line.replace("\n", ""))
        if line_dict['action'] == 'response classified':
            if line_dict['conversation link'] == conv_link:
                print("This conversation has already been classified")
                return

    write_log(email, {'action': 'response classified', 'interested': target_interested,
                      'conversation link': conv_link, 'target link': targetlink, 'target name': target_name})

def user_agent(email):
    genesis = get_genesis(email)
    agent_path = r"C:\Users\User\Desktop\ProfileBuilder\BuildigProfiles\user_agents.txt"
    if 'agent' in genesis.keys():
        return genesis['agent']



def unsupported_agent(email):
    genesis = get_genesis(email)
    agent_path = r"C:\Users\User\Desktop\ProfileBuilder\BuildigProfiles\user_agents.txt"
    if 'agent' in genesis.keys():
        print("Unsupported agent in genesis")
    with open("X:\Profiles\\" + email + "\log.txt", "r", encoding="utf-8") as file:
        lines = file.readlines()
    for line in lines:
        if 'set user agent' in line:
            unsupported = ast.literal_eval(line.replace("\n", ""))['agent']
            with open(agent_path, "r") as file:
                alines = file.readlines()
            l0 = len(alines)
            alines.remove(unsupported+"\n")
            if len(alines) - l0 < 1:
                print(unsupported)
                print("Unsupported agent line could not be removed")
            with open(agent_path, "w") as file:
                file.writelines(alines)
            lines.remove(line)
            with open("X:\Profiles\\" + email + "\log.txt", "w", encoding="utf-8") as lfile:
                lfile.writelines(lines)
            return
    print("User agent could not be removed")

def log_connection(email, name, link, job, when):
    with open("X:\Profiles\\" + email + "\log.txt", "r", encoding="utf-8") as file:
        lines = file.readlines()
        for line in lines:
            line_dict = ast.literal_eval(line.replace("\n", ""))
            if 'action' in line_dict.keys():
                if line_dict['action'] == "accepted":
                    if line_dict['link'] == link:
                        return
    logdict = {'action':'accepted', 'name':name, 'link':link, 'job':job, 'when':when}
    write_log(email, logdict)

def log_genesis(info):
    t0 = datetime.today().strftime('%d.%m.%Y %H:%M:%S')
    info['action'] = 'genesis'
    info['time'] = t0
    with open("X:/Profiles/"+info['email']+"/log.txt", "w", encoding="windows-1252") as file:
        file.write(str(info)+"\n")

def write_log(email, logdict):

    logdict['time'] = datetime.today().strftime('%d.%m.%Y %H:%M:%S')

    with open("X:\Profiles\\"+email+"\log.txt", "a", encoding="utf-8") as file:
        file.write(str(logdict)+"\n")

    with open("log_all.txt", "r", encoding="utf-8") as readfile:
        lines = readfile.readlines()
        lines.reverse()
    # file:///X:/Profiles/cofbiotankte1982@mail.ru/log.txt
    with open("log_all.txt", "a", encoding="utf-8") as file:

        for line in lines:
            if r"file:///" in line:
                if email not in line:
                    file.write(r">>>>>>>>file:///X:/Profiles/"+email+"/log.txt\n")
                break

        file.write(str(logdict) + "\n")


def get_genesis(email):
    with open("X:\Profiles\\" + email + "\log.txt", "r", encoding="utf-8") as file:
        lines = file.readlines()

    if "genesis" in lines[0]:

        return ast.literal_eval(lines[0].replace("\n", ""))
    else:
        return {}

def get_restr_genesis(email):
    with open("X:\Profiles\Restricted Logs\\" + email + ".txt", "r", encoding="utf-8") as file:
        lines = file.readlines()

    return ast.literal_eval(lines[0].replace("\n", ""))

def get_lastlog(email):
    with open("X:\Profiles\\" + email + "\log.txt", "r", encoding="utf-8") as file:
        lines = file.readlines()

    return ast.literal_eval(lines[-1].replace("\n", ""))

def message_in_log(email, message):

    with open("X:\Profiles\\" + email + "\log.txt", "r", encoding="utf-8") as file:
        lines = file.readlines()

    for line in lines:
        line_dict = ast.literal_eval(line.replace("\n", ""))
        if "author" in line_dict.keys():
            if message['author'] == line_dict['author'] and message['message time'] == line_dict['message time'] and message['contents'] == line_dict['contents']:
                return True
        if 'action' in line_dict.keys():
            if 'action' == 'message sent' and message['target link'] == line_dict['target link'] and message['contents'] == line_dict['contents']:
                return True
    return False

def log_conversation(email, conversation, targetlink):



    for message in conversation:
        if not message_in_log(email, message):
            message_log_dict = message
            message_log_dict['action'] = 'read message'
            message_log_dict['target link'] = targetlink
            write_log(email, message_log_dict)





# with open("Errors/success.txt", "r") as file:
#     lines = file.readlines()
#
# for line in lines:
#     l = line.split(" ")[0]
#     print(l, how_many(l, 'Join'))


