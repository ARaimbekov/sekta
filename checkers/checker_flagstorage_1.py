#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys

import requests

import session_sect.session as sect_session
import session_vacancy.session as vacancy_session
import utils.exceptions as excepts
import utils.utils as utils
from utils.generator import TextGenerator

SECT_PORT = 8000
VACANCY_PORT = 8033

"""
Arguments:
    1 -- action (check / put / get)
    2 -- host
    3 -- flag id
    4 -- flag
    5 -- vuln
"""


class Checker():

    def __init__(self):
        self.action, host, *args = sys.argv[1:]

        if self.action != "check":
            self.flagId, self.flag = args

        self.sectHost = f"http://{host}:{SECT_PORT}"
        self.vacancyHost = f"{host}:{VACANCY_PORT}"
        self.gen = TextGenerator(fileName="utils/word_storage.json")

    def main(self):
        try:
            if self.action == "check":
                self.check()
            elif self.action == "put":
                self.put()
            elif self.action == "get":
                try:
                    self.get()
                except excepts.MumbleException as e:
                    raise excepts.CorruptException(*e.Messages)
            else:
                message = f"Usage: {sys.argv[0]} check|put|get IP FLAGID FLAG"
                raise excepts.CheckerErrorException(message)

        except (excepts.DownException,
                excepts.MumbleException,
                excepts.CheckerErrorException) as exception:
            utils.die(exception.Status, *exception.Messages)

        except requests.exceptions.ConnectionError as e:
            print(f"{e.request.method} {e.request.url}\n" +
                  str(excepts.Status.DOWN) +
                  str(e), file=sys.stderr, flush=True)
            exit(code=excepts.Status.DOWN)

        except Exception as e:
            utils.die(excepts.Status.CHECKER_ERROR, e)

    def check(self):
        utils.log(f"run on {self.sectHost} and {self.vacancyHost}")
        owner = sect_session.SessionSect(self.sectHost, "owner")
        dummy = sect_session.SessionSect(self.sectHost, "dummy")
        dummy2 = sect_session.SessionSect(self.sectHost, "dummy2")
        vacancy = vacancy_session.SessionVacancy(self.vacancyHost, "vacancy")

        owner.AskRoot()
        owner.Register(self.gen.GenUserName(), self.gen.GenPassword())
        dummy.Register(self.gen.GenUserName(), self.gen.GenPassword())
        owner.Login()
        dummy.Login()

        sectName, sectDescription = self.gen.GenSectInfo()
        owner.CreateSekta(sectName, sectDescription)

        dummyAcolyteName = self.gen.GenUserName()
        owner.Invite(dummy.Id, dummyAcolyteName)

        owner.GetAllSects()
        owner.GetMySects()
        acolytes = owner.GetMySect()
        dummy.InSect(acolytes)

        owner.Sacrifice(dummy.Id)
        acolytes = owner.GetMySect()
        dummy.IsDead(dummyAcolyteName, acolytes)

        v = vacancy.Create(int(owner.SectId), self.gen.GenVacancyDescription())
        owner.CheckToken(v.Token)
        vacancy.List()
        vacancy.GetBad(vacancy.Vacancy.Id)
        vacancy.Edit(self.gen.GenVacancyDescription(), True)
        vacancy.Get(vacancy.Vacancy.Id)

        dummy2.Register(self.gen.GenUserName(), self.gen.GenPassword())
        dummy2.Login()
        dummy2.Join(vacancy.Vacancy.SectId,
                    vacancy.Vacancy.Token,
                    self.gen.GenUserName())
        owner.Logout()

    def put(self):
        utils.log(f"run on {self.sectHost} and {self.vacancyHost}")

        owner = sect_session.SessionSect(self.sectHost, "owner")
        dummy = sect_session.SessionSect(self.sectHost, "dummy")
        vacancy = vacancy_session.SessionVacancy(self.vacancyHost, "vacancy")

        owner.Register()
        owner.Login()

        dummy.Register()
        dummy.Login()

        sectName, sectDescription = self.gen.GenSectInfo()
        owner.CreateSekta(sectName, sectDescription)
        owner.Invite(dummy.Id, self.flag)

        acolytes = owner.GetMySect()
        for (name, encryptedSecretName) in acolytes:
            if name == dummy.Name:
                encryptedFlag = encryptedSecretName
                break

        vacancy.Create(owner.SectId)

        print(
            f"{self.flagId}#{owner.Name}#{owner.Password}#{encryptedFlag}", end="")

    def get(self):
        utils.log(f"run on {self.sectHost} and {self.vacancyHost}")
        utils.log(f"creds: flag_id = {self.flagId}\t flag={self.flag}")

        master = sect_session.SessionSect(self.sectHost, "master")

        args = self.flagId.split("#")
        master.Name = args[1]
        master.Password = args[2]
        encryptedFlag = args[3]

        master.Login()
        master.GetMySectsNoCheck()
        acolytes = master.GetMySect()

        for _, secretName in acolytes:
            if encryptedFlag == secretName:
                return

        raise excepts.CorruptException("flag not found")


if __name__ == "__main__":
    Checker().main()