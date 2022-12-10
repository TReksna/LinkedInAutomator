import requests, random, string, time

image_url = "https://thispersondoesnotexist.com/image"


for x in range(1000):

    print(x)
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

    time.sleep(1)
