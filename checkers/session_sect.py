#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from html.parser import HTMLParser
import re

import requests

from common import (MumbleException, checkHttpCode, find, findExpected,
                    findExpectedInMany, genName, log)
from bs4 import BeautifulSoup


class SessionSect:
    def __init__(self, host: str, debugName: str):
        self.Host = host
        self.debugName = debugName
        self.s = requests.Session()

    def AskRoot(self):
        log(f"[{self.debugName}]")

        resp = self.s.get(self.Host)
        checkHttpCode(resp)

    def Register(self):
        log(f"[{self.debugName}]")

        resp = self.s.get(self.Host+"/register")
        checkHttpCode(resp)
        self.setCSRF(resp)

        self.Name = self._genUsername()
        self.Password = self._genPassword()

        resp = self.s.post(self.Host+"/register/", data=dict(
            csrfmiddlewaretoken=self.csrfToken,
            username=self.Name,
            password=self.Password,
            can_be_invited=True))
        checkHttpCode(resp)

    def Login(self):
        log(f"[{self.debugName}]")

        resp = self.s.get(self.Host+"/login")

        checkHttpCode(resp)
        self.setCSRF(resp)

        resp = self.s.post(self.Host+"/login/", data=dict(
            csrfmiddlewaretoken=self.csrfToken,
            username=self.Name,
            password=self.Password))
        checkHttpCode(resp)

        result = find(r'Добро пожаловать, (\d+)\.[0-9A-z]+!</h3>', resp.text)
        self.Id = int(result)

    def CreateSekta(self, description: str) -> tuple[int,  str]:
        log(f"[{self.debugName}]")

        self.SectName = self._genSectName()

        resp = self.s.get(self.Host+"/create_sekta")
        checkHttpCode(resp)
        self.setCSRF(resp)

        resp = self.s.post(self.Host+"/create_sekta/", data=dict(
            csrfmiddlewaretoken=self.csrfToken,
            sektaname=self.SectName,
            description=description))
        checkHttpCode(resp)

        self.SectId = int(find(r'<h2>(\d+)\..*<\/h2>', resp.text))

        return self.SectId, self.SectName

    def Invite(self, userId: int, newName: str):
        log(f"[{self.debugName}]")

        if self.SectId == None:
            raise MumbleException("user doesnt have own sekta")

        resp = self.s.get(self.Host+f"/sekta/{self.SectId}/invite")
        checkHttpCode(resp)

        resp = self.s.get(self.Host+f"/sekta/{self.SectId}/invite_sektant", params=dict(
            csrfmiddlewaretoken=self.csrfToken,
            nickname=newName,
            sect=self.SectId,
            user=str(userId)))
        checkHttpCode(resp)

    def GetMySect(self):
        log(f"[{self.debugName}]")

        resp = self.s.get(self.Host+f"/sekta/{self.SectId}")
        checkHttpCode(resp)

        findExpected(resp.text, r"<h2>\d+\. ([\w\d ]+)<\/h2>", self.SectName)
        findExpected(resp.text, r"<h3>Гуру: ([\w\d ]+)<\/h3>", self.Name)

        self.Acolytes = re.findall(
            r"([\d\w]+) True name: \[[\"\'](.+)[\"\']", BeautifulSoup(resp.text, features="lxml").get_text())

        return self.Acolytes

    def CheckToken(self, token: str):
        log(f"[{self.debugName}]")

        resp = self.s.get(self.Host+f"/sekta/{self.SectId}")
        checkHttpCode(resp)

        findExpected(
            resp.text, r'Токен для вступления:<\/h3>\s*<h3>([a-f0-9\-]{36})<\/h3>', token)

    def GetSectDescription(self) -> str:
        log(f"[{self.debugName}]")

        resp = self.s.get(self.Host+f"/sekta/{self.SectId}")
        checkHttpCode(resp)

        match = re.search(r"<h3>Гуру: .+<\/h3>\s*<div>(.+)<\/div>", resp.text)
        return match[1]

    def GetMySects(self):
        log(f"[{self.debugName}]")

        resp = self.s.get(self.Host+"/my_sekts/")
        checkHttpCode(resp)

        findExpected(
            resp.text,
            r"<a href=\"\/sekta\/\d+\">\s*<h3 class=\"panel-title\">([\d\w]+)<\/h3>\s*<\/a>",
            self.SectName)

        match = re.search(r"<a href=\"\/sekta\/(\d+)\">", resp.text)
        self.SectId = match[1]

    def GetMySectsNoCheck(self):
        log(f"[{self.debugName}]")

        resp = self.s.get(self.Host+"/my_sekts/")
        checkHttpCode(resp)

        pattern = r"<a href=\"\/sekta\/(\d+)\">\s*<h3 class=\"panel-title\">([\d\w]+)<\/h3>\s*<\/a>"
        match = re.search(pattern, resp.text)
        self.SectId = match[1]
        self.SectName = match[2]

    def GetAllSects(self):
        log(f"[{self.debugName}]")

        resp = self.s.get(self.Host+"/all_sekts/")
        checkHttpCode(resp)

        if self.SectName != None:
            findExpectedInMany(
                resp.text,
                r"<a href=\"\/sekta\/\d+\">\s*<h3 class=\"panel-title\">\d+\.\s+([\d\w ]+)<\/h3>\s*<\/a>",
                self.SectName)

    def Sacrifice(self, userId: int):
        log(f"[{self.debugName}]")

        resp = self.s.get(self.Host+f"/sekta/{self.SectId}/sacrifice")
        checkHttpCode(resp)

        resp = self.s.get(
            self.Host+f"/sekta/{self.SectId}/sacrifice_sektant",
            params=dict(user=userId))
        checkHttpCode(resp)

    def Join(self, sectId: int, token: str):
        log(f"[{self.debugName}]")

        resp = self.s.get(self.Host+f"/token/")
        checkHttpCode(resp)

        match = re.search(r"csrfmiddlewaretoken\" value=\"(.+)\">", resp.text)

        if match == None:
            raise MumbleException("csrf token expected")

        self.AcolyteName = self._genUsername()

        resp = self.s.post(self.Host+f"/token/", data=dict(
            csrfmiddlewaretoken=match.group(1),
            sekta=sectId,
            token=token,
            nickname=self.AcolyteName))
        checkHttpCode(resp)

        resp = self.s.get(self.Host+f"/sekta/{sectId}")
        checkHttpCode(resp)

    def Logout(self):
        log(f"[{self.debugName}]")

        resp = self.s.get(self.Host+"/logout/")
        checkHttpCode(resp)

        try:
            self.GetMySects()
        except MumbleException:
            return

        raise MumbleException("logout doesnt worked")

    def setCSRF(self, resp: requests.Response) -> str:
        token = resp.cookies['csrftoken']

        if token == None:
            raise MumbleException("getting CSRF failed", resp.text)

        self.csrfToken = token
        return self.csrfToken

    def InSect(self, acolytes: list):
        log(f"[{self.debugName}]")

        for a in acolytes:
            if self.Name == a[0]:
                return

        raise MumbleException(f"{self.Id} expected acolyte in {acolytes}")

    def IsDead(self, secretName: str, acolytes: list):
        log(f"[{self.debugName}]")
        for a in acolytes:
            if secretName in a[1]:
                return

        raise MumbleException(f"{self.Name} expected to be dead")

    def _genUsername(self):
        return genName()

    def _genPassword(self):
        return genName()

    def _genSectName(self):
        return genName()
