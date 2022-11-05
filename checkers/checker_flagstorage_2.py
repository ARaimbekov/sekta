#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import random
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
                self.get()
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
        dummy = sect_session.SessionSect(host=self.sectHost, debugName="dummy")

        owner.AskRoot()
        owner.Register(self.gen.GenUserName(), self.gen.GenPassword())
        dummy.Register(self.gen.GenUserName(), self.gen.GenPassword())
        owner.Login()
        dummy.Login()

        sectName, sectDescription = self.gen.GenSectInfo()
        owner.CreateSekta(sectName, sectDescription)

    def put(self):
        utils.log(f"run on {self.sectHost} and {self.vacancyHost}")

        owner = sect_session.SessionSect(self.sectHost, "owner")
        vacancy = vacancy_session.SessionVacancy(self.vacancyHost, "vacancy")

        owner.Register(self.gen.GenUserName(), self.gen.GenPassword())
        owner.Login()
        sectName, _ = self.gen.GenSectInfo()
        owner.CreateSekta(sectName, self.flag)

        for _ in range(random.randint(2, 5)):
            dummy = sect_session.SessionSect(self.sectHost, "dummy")
            dummy.Register()
            dummy.Login()
            owner.Invite(dummy.Id, self.gen.GenUserName())

        vacancy.Create(owner.SectId, self.gen.GenVacancyDescription())

        print(f"{self.flagId}#{owner.Name}#{owner.Password}", end="")

    def get(self):
        utils.log(f"run on {self.sectHost} and {self.vacancyHost}")

        owner = sect_session.SessionSect(self.sectHost, "owner")

        args = self.flagId.split("#")
        owner.Name = args[1]
        owner.Password = args[2]

        owner.Login()
        owner.GetMySectsNoCheck()
        description = owner.GetSectDescription()

        if description != self.flag:
            raise excepts.CorruptException("flag not found")


if __name__ == "__main__":
    Checker().main()