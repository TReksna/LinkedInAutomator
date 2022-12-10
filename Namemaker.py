import os, random, csv, string

def rndname():

    file = r"BuildigProfiles\Names" + "\\" + random.choice(os.listdir(r"BuildigProfiles\Names"))

    with open(file, 'r') as f:
        reader = csv.reader(f)

        data = list(reader)

        return random.choice(data)

def randomname(sex="F"):

    while True:

        name = rndname()

        firstname = name[0]
        gender = name[1]
        lastname = rndname()[0]

        if gender == sex:

            return firstname, lastname

def random_job():
    with open("BuildigProfiles/jobs.txt", 'r') as f:
        lines = f.readlines()

    jobs = [l.replace("\n", "") for l in lines]

    return random.choice(jobs)

def get_random_password_string():

    length = random.randint(10,18)
    password_characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(password_characters) for i in range(length))
    print("Random string password is:", password)
    return password

