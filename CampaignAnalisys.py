import pandas as pd

def hours_sice(action):

    hours = (pd.to_datetime('now') - pd.to_datetime(action).replace(hour = 9)) / pd.Timedelta(hours=1)

    return hours

def sent_from_acc(email = None, action = 'invite_sent'):
    dx = pd.read_csv("Data/SuggestedCampaign.csv", index_col=0)
    dx['elapsed'] = dx['invite_sent'].apply(hours_sice)
    if email:
        df = dx[dx['agent_mail'] == email]
    else:
        df = dx
    if action != 'invite_sent':
        df = df[(df[action] != False) & (df[action] != "False")]
    sent_today = len(df[df['elapsed'] < 24])
    sent_this_week = len(df[df['elapsed'] < 24 * 7])

    return {"today":sent_today, "last_week":sent_this_week, "total": len(df)}

# invite_sent,invite_accepted,followup_sent,response_received

# print(sent_from_acc("austra.kausiniece@gmail.com", action="response_received"))

# df = pd.read_csv("Data/SuggestedCampaign.csv", index_col=0)
# df['elapsed'] = df['invite_sent'].apply(hours_sice)
# sent_today = len(df[df['elapsed'] < 24])
# sent_this_week = len(df[df['elapsed'] < 24*7])
#
# print(sent_today, sent_this_week)