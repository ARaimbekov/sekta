#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re

import requests
from bs4 import BeautifulSoup

import session_sect.utils as session_utils
import utils.exceptions as excepts
import utils.utils as utils


class SessionSect:
    def __init__(self, host: str, debugName: str):
        self.Host = host
        self.debugName = debugName
        self.s = requests.Session()

    def AskRoot(self):
        utils.log(f"[{self.debugName}] ...")

        resp = self.s.get(self.Host)
        session_utils.checkHttpCode(resp)

    def Register(self, name: str, password: str):
        utils.log(f"[{self.debugName}] ...")

        resp = self.s.get(self.Host+"/register")
        session_utils.checkHttpCode(resp)
        self.setCSRF(resp)

        self.Name = name
        self.Password = password

        resp = self.s.post(self.Host+"/register/", data=dict(
            csrfmiddlewaretoken=self.csrfToken,
            username=self.Name,
            password=self.Password,
            can_be_invited=True))
        session_utils.checkHttpCode(resp)

    def Login(self):
        utils.log(f"[{self.debugName}] ...")

        resp = self.s.get(self.Host+"/login")

        session_utils.checkHttpCode(resp)
        self.setCSRF(resp)

        resp = self.s.post(self.Host+"/login/", data=dict(
            csrfmiddlewaretoken=self.csrfToken,
            username=self.Name,
            password=self.Password))
        session_utils.checkHttpCode(resp)

        result = utils.find(
            resp.text,
            r'Добро пожаловать, (\d+)\.[0-9А-я ]+!</h3>',
            "User id not found after login")

        self.Id = int(result)

    def CreateSekta(self, name: str, description: str) -> int:
        utils.log(f"[{self.debugName}] ...")

        self.SectName = name
        self.SectDescription = description
        resp = self.s.get(self.Host+"/create_sekta")
        session_utils.checkHttpCode(resp)
        self.setCSRF(resp)

        resp = self.s.post(self.Host+"/create_sekta/", data=dict(
            csrfmiddlewaretoken=self.csrfToken,
            sektaname=self.SectName,
            description=description))
        session_utils.checkHttpCode(resp)

        self.SectId = int(utils.find(resp.text,
                                     r'<h2>(\d+)\..*<\/h2>',
                                     "Sect id not found after creation"))

        return self.SectId

    def Invite(self, userId: int, newName: str):
        utils.log(f"[{self.debugName}] ...")

        if self.SectId == None:
            raise excepts.MumbleException("User doesnt have own sekta")

        resp = self.s.get(self.Host+f"/sekta/{self.SectId}/invite")
        session_utils.checkHttpCode(resp)

        resp = self.s.get(self.Host+f"/sekta/{self.SectId}/invite_sektant", params=dict(
            csrfmiddlewaretoken=self.csrfToken,
            nickname=newName,
            sect=self.SectId,
            user=str(userId)))
        session_utils.checkHttpCode(resp)

    def GetMySect(self):
        utils.log(f"[{self.debugName}] ...")

        resp = self.s.get(self.Host+f"/sekta/{self.SectId}")
        session_utils.checkHttpCode(resp)

        utils.findExpected(resp.text,
                           r"<h2>\d+\. ([\w\d ]+)<\/h2>",
                           self.SectName,
                           "Sect name not found")

        utils.findExpected(resp.text,
                           r"<h3>Гуру: ([\w\d ]+)<\/h3>",
                           self.Name,
                           "Owner name of sect not found")

        self.Acolytes = re.findall(
            pattern=r"(.+) Тайное имя: \[b?'(.+)'\]",
            string=BeautifulSoup(resp.text, features="lxml").get_text())

        if len(self.Acolytes) == 0:
            raise excepts.MumbleException("Expected at least one acolyte")

        return self.Acolytes

    def CheckToken(self, token: str):
        utils.log(f"[{self.debugName}] ...")

        resp = self.s.get(self.Host+f"/sekta/{self.SectId}")
        session_utils.checkHttpCode(resp)

        utils.findExpected(resp.text,
                           r'Токен для вступления:<\/h3>\s*<h3>([a-f0-9\-]{36})<\/h3>',
                           token,
                           "Token for joining not found on sect page")

    def GetSectDescription(self) -> str:
        utils.log(f"[{self.debugName}] ...")

        resp = self.s.get(self.Host+f"/sekta/{self.SectId}")
        session_utils.checkHttpCode(resp)

        description = utils.find(resp.text,
                                 r"<div>(.+)<\/div>",
                                 "Sect description not found")

        return description

    def GetMySects(self):
        utils.log(f"[{self.debugName}] ...")

        resp = self.s.get(self.Host+"/my_sekts/")
        session_utils.checkHttpCode(resp)

        utils.findExpected(resp.text,
                           r"<a href=\"\/sekta\/\d+\">\s*<h3 class=\"panel-title\">([\d\w ]+)<\/h3>\s*<\/a>",
                           self.SectName,
                           "Sect name not found on 'My sects' page")

        match = re.search(r"<a href=\"\/sekta\/(\d+)\">", resp.text)
        self.SectId = int(match[1])

    def GetMySectsNoCheck(self):
        utils.log(f"[{self.debugName}] ...")

        resp = self.s.get(self.Host+"/my_sekts/")
        session_utils.checkHttpCode(resp)

        pattern = r"<a href=\"\/sekta\/(\d+)\">\s*<h3 class=\"panel-title\">([\d\w ]+)<\/h3>\s*<\/a>"
        match = re.search(pattern, resp.text)
        self.SectId = int(match[1])
        self.SectName = match[2]

    def GetAllSects(self):
        utils.log(f"[{self.debugName}] ...")

        resp = self.s.get(self.Host+"/all_sekts/")
        session_utils.checkHttpCode(resp)

        if self.SectName == None:
            return

        utils.findExpectedInMany(
            resp.text,
            r"<a href=\"\/sekta\/\d+\">\s*<h3 class=\"panel-title\">\d+\.\s+([\d\w ]+)<\/h3>\s*<\/a>",
            self.SectName,
            "Sect name not found in list of all owner sects")

    def Sacrifice(self, userId: int):
        utils.log(f"[{self.debugName}] ...")

        resp = self.s.get(self.Host+f"/sekta/{self.SectId}/sacrifice")
        session_utils.checkHttpCode(resp)

        resp = self.s.get(
            self.Host+f"/sekta/{self.SectId}/sacrifice_sektant",
            params=dict(user=userId))
        session_utils.checkHttpCode(resp)

    def Join(self, sectId: int, token: str, acolyteName: str):
        utils.log(f"[{self.debugName}] ...")

        resp = self.s.get(self.Host+f"/token/")
        session_utils.checkHttpCode(resp)

        match = re.search(r"csrfmiddlewaretoken\" value=\"(.+)\">", resp.text)

        if match == None:
            raise excepts.MumbleException("CSRF token expected")

        self.AcolyteName = acolyteName

        resp = self.s.post(self.Host+f"/token/", data=dict(
            csrfmiddlewaretoken=match.group(1),
            sekta=sectId,
            token=token,
            nickname=self.AcolyteName))
        session_utils.checkHttpCode(resp)

        resp = self.s.get(self.Host+f"/sekta/{sectId}")
        session_utils.checkHttpCode(resp)

    def Logout(self):
        utils.log(f"[{self.debugName}] ...")

        resp = self.s.get(self.Host+"/logout/")
        session_utils.checkHttpCode(resp)

        try:
            self.GetMySects()
        except excepts.MumbleException:
            return

        raise excepts.MumbleException("Logout doesnt worked")

    def setCSRF(self, resp: requests.Response) -> str:
        token = resp.cookies['csrftoken']

        if token == None:
            raise excepts.MumbleException("Getting CSRF failed", resp.text)

        self.csrfToken = token
        return self.csrfToken

    def InSect(self, acolytes: list):
        utils.log(f"[{self.debugName}] ...")

        for a in acolytes:
            if self.Name == a[0]:
                return

        raise excepts.MumbleException(
            f"Expected acolyte for sect_id = {self.Id}  in list {acolytes}")

    def IsDead(self, secretName: str, acolytes: list):
        utils.log(f"[{self.debugName}] ...")
        for a in acolytes:
            if secretName in a[1]:
                return

        raise excepts.MumbleException(
            f"Acolyte {self.Name} expected to be dead")
