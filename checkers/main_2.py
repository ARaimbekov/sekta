#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import random
import sys

import requests

from common import (CheckerErrorException, CorruptException, DownException,
                    MumbleException, Status, die, genDescription, genName, log)
from session_sect import SessionSect
from session_vacancies import SessionVacancy

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
                raise CheckerErrorException(message)

        except (DownException, MumbleException, CheckerErrorException) as exception:
            die(exception.Status, *exception.Messages)

        except requests.exceptions.ConnectionError as e:
            print(f"{e.request.method} {e.request.url}\n" +
                  Status.DOWN +
                  str(e), file=sys.stderr, flush=True)
            exit(code=Status.DOWN)

        except Exception as e:
            die(Status.CHECKER_ERROR, e)

    def check(self):
        log(f"run on {self.sectHost} and {self.vacancyHost}")

        master = SessionSect(host=self.sectHost, debugName="master")
        master.AskRoot()
        master.Register()
        master.Login()

        dummy = SessionSect(host=self.sectHost, debugName="dummy")
        dummy.Register()
        dummy.Login()

        master.CreateSekta(genDescription())

    def put(self):
        log(f"run on {self.sectHost} and {self.vacancyHost}")

        master = SessionSect(host=self.sectHost, debugName="master")
        master.Register()
        master.Login()
        master.CreateSekta(self.flag)

        for _ in range(random.randint(2, 5)):
            dummy = SessionSect(host=self.sectHost, debugName="dummy")
            dummy.Register()
            dummy.Login()
            master.Invite(dummy.Id, genName)

        vacancy = SessionVacancy(
            host=self.vacancyHost,
            debugName="vacancy")
        vacancy.Create(master.SectId)

        print(f"{self.flagId}#{master.Name}#{master.Password}", end="")

    def get(self):
        log(f"run on {self.sectHost} and {self.vacancyHost}")

        master = SessionSect(host=self.sectHost, debugName="master")

        args = self.flagId.split("#")
        master.Name = args[1]
        master.Password = args[2]

        master.Login()
        master.GetMySectsNoCheck()
        description = master.GetSectDescription()

        if description != self.flag:
            raise CorruptException("flag not found")


if __name__ == "__main__":
    Checker().main()
