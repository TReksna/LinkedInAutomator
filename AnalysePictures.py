import requests, random, string, time, os, json, ast, traceback

valid = 0

image_url = "https://thispersondoesnotexist.com/image"

n=0
while True:

    n+=1

    img_data = requests.get(image_url).content
    digits = ''.join(random.choices(string.digits, k=random.randint(3,6)))
    letters = ''.join(random.choices(string.ascii_uppercase, k=random.randint(3,6)))
    phrase = random.choice(['Face', 'Picture', 'me', 'image', 'profile', 'June', 'best', 'pic'])
    sep = random.choice(["-", " ", "", "_"])

    image_name = phrase + sep
    if random.random() > 0.6:
        image_name += digits+sep+letters
    elif random.random() > 0.6:
        image_name += sep+letters+digits
    elif random.random() > 0.5:
        image_name += sep+letters
    else:
        image_name += sep+digits

    with open(r'X:\Pictures\{}.jpg'.format(image_name), 'wb') as handler:
        handler.write(img_data)

    picfile = image_name+".jpg"


    picpurify_url = 'https://www.picpurify.com/analyse/1.1'

    picpath = r'X:\Pictures\\'+picfile

    img_data = {'file_image': open(picpath, 'rb')}

    result_data = requests.post(picpurify_url,files = img_data, data = {"API_KEY":"n5b15pdT648xhZ73Pe8kgqGqsNjg5z1S", "task":"face_gender_age_detection"})
    results = json.loads(result_data.content.decode('utf8'))["face_detection"]["results"]
    age = results[0]["age_majority"]["decision"]
    gender = results[0]["gender"]["decision"]
    img_data['file_image'].close()
    if age == "major" and gender == "female":

        os.replace(picpath, r"X:\Pictures\New\\" +picfile)

        valid += 1
    else:
        os.remove(picpath)

    print(f"{valid}/{n} ({round(valid*100/(n))}%)")

# 2.
# cbdchemist1@gmail.com
# Highway2Hell$
# W6gzuKmU0litTXTTIKsAPYtQAHLodVS5
#
# 3.
# karlis@gaze.lv
# Highway2Hell$
# l5DYHzI5KLtNGUn8RSpGdbMWil1kFae0
#
# 4.
# targintelligence@gmail.com
# Highway2Hell$
# b2nRt9VEGsAhWjQ6XvD8GQuBMmw8FfYx
#
# 5.
# thesurveyacademia@gmail.com
# Time2Skyrocket#
# 30iBmSGYLoOqp6q1nZPQbSCiCpKm5q0x
#
# 6.
# info@eucoriga2022.com
# Time2Skyrocket#
# LAlJkvnWatJpNkc6WlssJx1BPoBIoTEu
#
# 7.
# rotaractdaugava@gmail.com
# Good4usss#
# D3BiPTlplYKBLWDuLxq6lIDn8Fmf3RhU
#
# 8.
# rigarotaract@gmail.com
# BetterWeWin9@
# BL9JMALLdqLuYmQHuvnfMaVSr2HNae9A