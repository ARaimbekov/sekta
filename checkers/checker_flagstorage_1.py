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
            utils.die(
                excepts.Status.DOWN,
                f"URL:{e.request.method} {e.request.url}\n",
                e)

        except Exception as e:
            utils.die(excepts.Status.CHECKER_ERROR, e)

    def check(self):
        utils.log(f"run on {self.sectHost} and {self.vacancyHost}")
        owner = sect_session.SessionSect(self.sectHost, "owner")
        acolyte = sect_session.SessionSect(self.sectHost, "acolyte")
        acolyte_2 = sect_session.SessionSect(self.sectHost, "acolyte 2")
        vacancyOwner = vacancy_session.SessionVacancy(
            self.vacancyHost, "vacancy owner")

        owner.AskRoot()
        owner.Register(self.gen.GenUserName(), self.gen.GenPassword())
        acolyte.Register(self.gen.GenUserName(), self.gen.GenPassword())
        owner.Login()
        acolyte.Login()

        sectName, sectDescription = self.gen.GenSectInfo()
        owner.CreateSekta(sectName, sectDescription)

        vacancyOwner.Create(owner.SectId, self.gen.GenVacancyDescription())
        owner.CheckToken(vacancyOwner.Vacancy.Token)
        vacancyOwner.List()
        vacancyOwner.GetBad(vacancyOwner.Vacancy.Id)
        vacancyOwner.Edit(self.gen.GenVacancyDescription(), True)
        vacancyOwner.Get(vacancyOwner.Vacancy.Id)

        dummyAcolyteName = self.gen.GenUserName()
        owner.Invite(acolyte.Id, dummyAcolyteName)

        owner.GetAllSects()
        owner.GetMySects()
        acolytes = owner.GetMySect()

        acolyte.InSect(acolytes)
        owner.Sacrifice(acolyte.Id)
        acolytes = owner.GetMySect()
        acolyte.IsDead(dummyAcolyteName, acolytes)

        acolyte_2.Register(self.gen.GenUserName(), self.gen.GenPassword())
        acolyte_2.Login()
        acolyte_2.Join(vacancyOwner.Vacancy.SectId,
                       vacancyOwner.Vacancy.Token,
                       self.gen.GenUserName())
        owner.Logout()

    def put(self):
        utils.log(f"run on {self.sectHost} and {self.vacancyHost}")

        owner = sect_session.SessionSect(self.sectHost, "owner")
        acolyte = sect_session.SessionSect(self.sectHost, "acolyte")
        vacancyOwner = vacancy_session.SessionVacancy(
            self.vacancyHost, "vacancy owner")

        owner.Register(self.gen.GenUserName(), self.gen.GenPassword())
        owner.Login()

        acolyte.Register(self.gen.GenUserName(), self.gen.GenPassword())
        acolyte.Login()

        sectName, sectDescription = self.gen.GenSectInfo()
        owner.CreateSekta(sectName, sectDescription)
        owner.Invite(acolyte.Id, self.flag)

        acolytes = owner.GetMySect()
        for (name, encryptedSecretName) in acolytes:
            if name == acolyte.Name:
                encryptedFlag = encryptedSecretName
                break

        vacancyOwner.Create(owner.SectId, self.gen.GenVacancyDescription())

        ownerName = owner.Name.replace(" ", "_")

        print(
            f"{self.flagId}#{ownerName}#{owner.Password}#{encryptedFlag}",
            end="",
            flush=True,
        )

    def get(self):
        utils.log(f"run on {self.sectHost} and {self.vacancyHost}")
        utils.log(f"""creds:
                flag_id = {self.flagId}
                flag={self.flag}
            """)

        owner = sect_session.SessionSect(self.sectHost, "owner")

        args = self.flagId.split("#")
        owner.Name = args[1].replace("_", " ")
        owner.Password = args[2]
        encryptedFlag = args[3]

        owner.Login()
        owner.GetMySectsNoCheck()
        acolytes = owner.GetMySect()

        for _, secretName in acolytes:
            if encryptedFlag == secretName:
                return

        raise excepts.CorruptException("flag not found")


if __name__ == "__main__":
    Checker().main()
