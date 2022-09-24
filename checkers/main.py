#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys

import requests

from common import (CheckerErrorException, DownException, MumbleException,
                    Status, die, genFlag, genName, log)
from session_sect import SessionSect
from session_vacancies import SessionVacancy

SECT_PORT = 8000
VACANCY_PORT = 8033


class Checker():

    def __init__(self):
        self.action, host, *args = sys.argv[1:]

        if self.action != "check":
            self.flag_id, self.flag, self.vuln = args

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

        except (DownException, MumbleException) as exception:
            die(exception.Status, *exception.Messages)

        except requests.exceptions.ConnectionError as e:
            print(f"{e.request.method} {e.request.url}\n" +
                  str(e), file=sys.stderr, flush=True)
            exit(code=Status.DOWN)

        except Exception as e:
            die(Status.CHECKER_ERROR, e)

    def check(self):
        master = SessionSect(host=self.sectHost, debugName="master")
        master.AskRoot()
        master.Register()
        master.Login()

        dummy = SessionSect(host=self.sectHost, debugName="dummy")
        dummy.Register()
        dummy.Login()

        master.CreateSekta(genName())
        dummySecretName = genFlag()
        master.Invite(dummy.Id, dummySecretName)

        master.GetAllSects()
        master.GetMySects()
        acolytes = master.GetMySect()
        dummy.InSect(acolytes)

        master.Sacrifice(dummy.Id)
        acolytes = master.GetMySect()
        dummy.IsDead(dummySecretName, acolytes)
        master.Logout()

        vacancy = SessionVacancy(
            host=self.vacancyHost,
            debugName="vacancy")

        vacancy.Create(master.SectId)
        vacancy.List()
        vacancy.GetBad(vacancy.Vacancy.Id)
        vacancy.Edit("dummy bunny", True)
        vacancy.Get(vacancy.Vacancy.Id)

        dummy2 = SessionSect(host=self.sectHost, debugName="dummy2")
        dummy2.Register()
        dummy2.Login()
        dummy2.Join(vacancy.Vacancy.SectId, vacancy.Vacancy.Token)

    def put(self):
        # log(f"Running PUT on {self.sektaChecker.Host}")
        # self.sektaChecker.Put(self.flag_id, genFlag())
        pass

    def get(self):
        # log(f"Running GET on {self.sektaHost} {self.vacancyHost} with {self.flag_id}:{self.flag}")
        die(Status.OK, "Not implemented")


if __name__ == "__main__":
    Checker().main()
