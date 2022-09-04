#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
from common import CheckerException, checkHttpCode, find, findExpected, findExpectedInMany, getRandomName, log, Status
import requests


class User:
    def __init__(self, host: str, name: str):
        self.Host = host
        self.debugName = name
        self.s = requests.Session()

    def askRoot(self):
        log(f"[{self.debugName}]")

        resp = self.s.get(self.Host)
        checkHttpCode(resp, "get:/")

    def register(self):
        log(f"[{self.debugName}]")

        resp = self.s.get(self.Host+"/register")
        checkHttpCode(resp, "get:register")
        self.setCSRF(resp)

        self.Name = getRandomName()
        self.Password = getRandomName()

        resp = self.s.post(self.Host+"/register/", data=dict(
            csrfmiddlewaretoken=self.csrfToken,
            username=self.Name,
            password=self.Password,
            can_be_invited=True))
        checkHttpCode(resp, "get:register")

    def login(self):
        log(f"[{self.debugName}]")

        resp = self.s.get(self.Host+"/login")
        checkHttpCode(resp, "get:login")
        self.setCSRF(resp)

        resp = self.s.post(self.Host+"/login/", data=dict(
            csrfmiddlewaretoken=self.csrfToken,
            username=self.Name,
            password=self.Password))
        checkHttpCode(resp, "get:login")

        result = find(r'Добро пожаловать, (\d+)\.[0-9A-z]+!</h3>', resp.text)
        self.Id = int(result)

    def logout(self):
        log(f"[{self.debugName}]")

        url = self.Host+"/logout/"

        resp = self.s.get(url)

        checkHttpCode(resp, "get:"+url)

    def createSekta(self):
        log(f"[{self.debugName}]")

        resp = self.s.get(self.Host+"/create_sekta")
        checkHttpCode(resp, "get:create_sekta")
        self.setCSRF(resp)

        self.SectName = getRandomName()

        resp = self.s.post(self.Host+"/create_sekta", data=dict(
            csrfmiddlewaretoken=self.csrfToken,
            sektaname=self.SectName))
        checkHttpCode(resp, "post:create_sekta")

        result = find(r'([0-9]+)/invite\'">Invite new followers', resp.text)
        self.SektaId = int(result)

    def invite(self, userId: int, newName: str):
        log(f"[{self.debugName}]")

        if self.SektaId == None:
            raise CheckerException(Status.MUMBLE, "user doesnt have own sekta")

        url = self.Host+f"/sekta/{self.SektaId}/invite"
        resp = self.s.get(url)
        checkHttpCode(resp, "get:"+url)

        url = self.Host+f"/sekta/{self.SektaId}/invite_sektant"
        resp = self.s.get(url, params=dict(
            csrfmiddlewaretoken=self.csrfToken,
            nickname=newName,
            sect=self.SektaId,
            user=str(userId)))
        checkHttpCode(resp, "get: "+url)

    def getMySect(self):
        log(f"[{self.debugName}]")

        url = self.Host+f"/sekta/{self.SektaId}"
        resp = self.s.get(url)
        checkHttpCode(resp, "get:"+url)

        findExpected(resp.text, r"<h2>([\w\d ]+)<\/h2>", self.SectName)
        findExpected(resp.text, r"<h3>Гуру: ([\w\d ]+)<\/h3>", self.Name)

        self.Acolytes = re.findall(
            r"<li>\s*([\w \d]+) True name:\s*\[(.+)\]\s*<\/li>", resp.text)

        return self.Acolytes

    def getMySects(self):
        log(f"[{self.debugName}]")

        url = self.Host+"/my_sekts/"
        resp = self.s.get(url)
        checkHttpCode(resp, "get:"+url)

        findExpected(
            resp.text,
            r"<a href=\"\/sekta\/\d+\">\s*<h3 class=\"panel-title\">([\d\w]+)<\/h3>\s*<\/a>",
            self.SectName)

    def getAllSects(self):
        log(f"[{self.debugName}]")

        url = self.Host+"/all_sekts/"
        resp = self.s.get(url)
        checkHttpCode(resp, "get:"+url)

        if self.SectName != None:
            findExpectedInMany(
                resp.text,
                r"<a href=\"\/sekta\/\d+\">\s*<h3 class=\"panel-title\">\d+\.\s+([\d\w ]+)<\/h3>\s*<\/a>",
                self.SectName)

    def sacrifice(self, userId: int):
        url = self.Host+f"/sekta/{self.SektaId}/sacrifice"
        resp = self.s.get(url)
        checkHttpCode(resp, "get:"+url)

        url = self.Host+f"/sekta/{self.SektaId}/sacrifice_sektant"
        resp = self.s.get(url, params=dict(user=userId))
        checkHttpCode(resp, "get:"+url)

    def setCSRF(self, resp: requests.Response) -> str:
        token = resp.cookies['csrftoken']

        if token == None:
            raise CheckerException(
                Status.MUMBLE, "getting CSRF failed", resp.text)

        self.csrfToken = token
        return self.csrfToken
