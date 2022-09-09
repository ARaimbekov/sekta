#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import traceback

from common import CheckerException, Status, die, log
from sektaChecker.sektaChecker import SektaChecker
from vacancyChecker.vacancyChecker import VacancyChecker
import requests

SEKTA_PORT = 8000
VACANCY_PORT = 8033


class Checker():

    def __init__(self):
        self.action, host, *args = sys.argv[1:]

        if self.action != "check":
            self.flag_id, self.flag, self.vuln = args

        self.sektaChecker = SektaChecker(host, SEKTA_PORT)
        self.vacancyChecker = VacancyChecker(host, VACANCY_PORT)

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
                raise CheckerException(Status.CHECKER_ERROR, message)

        except CheckerException as exception:
            print(exception, file=sys.stderr, flush=True)
            exit(code=exception.Status.value)

        except requests.exceptions.ConnectionError as e:
            print(f"{e.request.method} {e.request.url}\n" +
                  str(e), file=sys.stderr, flush=True)
            exit(code=Status.DOWN)

        # except Exception as e:
        #     message = f"Exception: {e}\nStack:\n {traceback.format_exc()}",
        #     die(Status.CHECKER_ERROR, e)

    def check(self):
        log(f"Running CHECK on {self.sektaChecker.Host}")
        self.sektaChecker.Check()
        self.vacancyChecker.check()

    def put(self):
        log(f"Running PUT on {self.sektaChecker.Host}")
        self.sektaChecker.Put(self.flag_id, self.flag)

    def get(self):
        log(f"Running GET on {self.sektaHost} {self.vacancyHost} with {self.flag_id}:{self.flag}")
        die(Status.OK, "Not implemented")


if __name__ == "__main__":
    Checker().main()
