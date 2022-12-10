import pandas as pd
import random
# from CreateLinkedIn.ProfileDataManager import  *
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.max_colwidth', None)
pd.set_option('display.expand_frame_repr', False)



def zip_state_from_city(city):

    df = pd.read_csv(r"C:\Users\User\Desktop\ProfileManager\CreateLinkedIn\ProfileData\uszips.txt",
                     delimiter=";", encoding = "ISO-8859-1", dtype={'zip': str})

    if city == '':
        city = "New York"

    city = city.replace("The ","").replace("Cheektowaga", "New York")

    df1 = df[df['city']==city]
    if len(df1) < 1:
        df1 = df[df['county_name']==city]
    state = df1['state_name'].value_counts().index[0]
    df2 = df1[df1['state_name'] == state]
    row = df2.sample().iloc[0]
    zip = row['zip']

    return zip, state

def random_zip():
    df = pd.read_csv(r"C:\Users\User\Desktop\ProfileManager\CreateLinkedIn\ProfileData\uszips.txt",
                     delimiter=";", encoding="ISO-8859-1", dtype={'zip': str})
    return random.choice(df['zip'].unique)
