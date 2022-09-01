#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
from common import log, die, Status
import requests
import lorem


def getCSRF(resp: requests.Response) -> str:
    return re.findall(r'value="([A-z0-9]+)">', resp.text)[0]


def dieHttp(self, resp: requests.Response, requestName: str):
    if 500 <= resp.status_code:
        die(Status.DOWN, f"status code 5xx on {requestName}", resp.text)
    elif 400 <= resp.status_code < 500:
        die(Status.MUMBLE,
            f"status code 4xx on {requestName}", resp.status_code, resp.text)
    else:
        die(Status.DOWN,
            f"unexpected behaviour on {requestName}", resp.text)


class SektaChecker:
    def __init__(self, host: str, port: int):
        self.Host = f"http://{host}:{port}"

    def check(self):
        log("run")

        master = Sektant(host=self.Host, name="master")
        master.askRoot()
        master.register()
        master.login()
        master.createSekta()

        dummy = Sektant(host=self.Host, name="dummy")
        dummy.askRoot()
        dummy.register()
        dummy.login()


class Sektant:
    def __init__(self, host: str, name: str):
        self.Host = host
        self.debugName = name
        self.s = requests.Session()

    def askRoot(self):
        log(f"[{self.debugName}] run")

        try:
            resp = self.s.get(self.Host)
        except Exception as e:
            die(Status.DOWN, " get:/ failed", str(e))

        if resp.status_code != 200:
            die(Status.DOWN, "get:/ failed", resp.text)

    def register(self):
        log(f"[{self.debugName}] run")

        try:
            resp = self.s.get(self.Host+"/register")
        except Exception as e:
            die(Status.DOWN, "get:register failed", str(e))

        if resp.status_code != 200:
            dieHttp(resp, "get:register")

        csrf = getCSRF(resp)

        self.Name = lorem.get_word(count=1)
        self.Password = lorem.get_word(count=1)

        try:
            resp = self.s.post(self.Host+"/register/", data=dict(
                csrfmiddlewaretoken=csrf,
                username=self.Name,
                password=self.Password,
                can_be_invited=True,
            ))
        except Exception as e:
            die(Status.DOWN, "post:register failed", str(e))

        if resp.status_code != 200:
            dieHttp(resp, "get:register")

    def login(self):
        log(f"[{self.debugName}] run")

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
                username=self.Name,
                password=self.Password,
            ))
        except Exception as e:
            die(Status.DOWN, "post:login failed", str(e))

        matches = re.findall(
            r'Добро пожаловать, (\d+)\.[0-9A-z]+!</h3>', resp.text)

        if len(matches) == 0:
            die(Status.MUMBLE,
                "post:login getting id failed",
                self.Name,
                self.Password,
                resp.text)

        self.userId = int(matches[0])

    def createSekta(self):
        log(f"[{self.debugName}] run")

        try:
            resp = self.s.get(self.Host+"/create_sekta")
        except Exception as e:
            die(Status.DOWN, "get:create_sekta failed", str(e))

        if resp.status_code != 200:
            dieHttp(resp, "get:create_sekta")

        csrf = getCSRF(resp)

        self.SektaName = lorem.get_word(count=1)

        try:
            resp = self.s.post(self.Host+"/create_sekta", data=dict(
                csrfmiddlewaretoken=csrf,
                sektaname=self.SektaName))
        except Exception as e:
            die(Status.DOWN, "post:create_sekta failed", str(e))

        if resp.status_code != 200:
            dieHttp(resp, "post:create_sekta")

        matches = re.findall(
            r'([0-9]+)/invite\'">Invite new followers', resp.text)

        if len(matches) == 0:
            die(Status.MUMBLE, "post:create_sekta getting id failed")

        self.SektaId = int(matches[0])