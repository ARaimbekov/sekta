#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from http.client import HTTPException
import re
from common import log, die, Status
import requests
import lorem


def getCSRF(resp: requests.Response) -> str:
    return re.findall(r'value="([A-z0-9]+)">', resp.text)[0]


def dieHttp(resp: requests.Response, requestName: str):
    if 500 <= resp.status_code:
        die(Status.DOWN, f"status code 5xx on {requestName}", resp.text)
    elif 400 <= resp.status_code < 500:
        die(Status.MUMBLE, f"status code 4xx on {requestName}", resp.text)
    else:
        die(Status.DOWN, f"unexpected behaviour on {requestName}", resp.text)


class SektaChecker:

    def __init__(self, host: str, port: int):
        self.Host = f"http://{host}:{port}"
        self.s = requests.Session()

    def check(self):
        log("run")
        self.checkRoot()
        self.checkRegister()
        self.checkLogin()
        self.checkCreateSekta()

    def checkRoot(self):
        log("run")

        try:
            resp = self.s.get(self.Host)
        except Exception as e:
            die(Status.DOWN, "get:/ failed", str(e))

        if resp.status_code != 200:
            die(Status.DOWN, "get:/ failed", resp.text)

    def checkRegister(self):
        log("run")

        try:
            resp = self.s.get(self.Host+"/register")
        except Exception as e:
            die(Status.DOWN, "get:register failed", str(e))

        if resp.status_code != 200:
            dieHttp(resp, "get:register")

        csrf = getCSRF(resp)

        self.user_name = lorem.get_word(count=1)
        self.user_password = lorem.get_word(count=1)

        try:
            resp = self.s.post(self.Host+"/register/", data=dict(
                csrfmiddlewaretoken=csrf,
                username=self.user_name,
                password=self.user_password,
                can_be_invited=True,
            ))
        except Exception as e:
            die(Status.DOWN, "post:register failed", str(e))

    def checkLogin(self):
        log("run")

        try:
            resp = self.s.get(self.Host+"/login")
        except Exception as e:
            die(Status.DOWN, "get:login failed", str(e))

        if resp.status_code != 200:
            dieHttp(resp, "get:login")

        csrf = getCSRF(resp)

        try:
            resp = self.s.post(self.Host+"/login/", data=dict(
                csrfmiddlewaretoken=csrf,
                username=self.user_name,
                password=self.user_password,
            ))
        except Exception as e:
            die(Status.DOWN, "post:login failed", str(e))

        self.user_id = re.findall(
            r'Добро пожаловать, (\d+)\.[0-9A-z]+!</h3>', resp.text)[0]

    def checkCreateSekta(self):
        log("run")

        try:
            resp = self.s.get(self.Host+"/create_sekta")
        except Exception as e:
            die(Status.DOWN, "get:create_sekta failed", str(e))

        if resp.status_code != 200:
            dieHttp(resp, "get:create_sekta")

        csrf = getCSRF(resp)

        try:
            resp = self.s.post(self.Host+"/create_sekta", data=dict(
                csrfmiddlewaretoken=csrf,
                sektaname=lorem.get_word(count=1),))
        except Exception as e:
            die(Status.DOWN, "post:create_sekta failed", str(e))

        if resp.status_code != 200:
            dieHttp(resp, "post:create_sekta")

        self.sekta_id = re.findall(
            r'([0-9]+)/invite\'">Invite new followers', resp.text)[0]
