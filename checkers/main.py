#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import traceback

from common import Status, die, log
from vacancyChecker import VacancyChecker


MAIN_PORT = 8083
VACANCY_PORT = 8033


class Checker():

    def __init__(self):
        self.action, host, *args = sys.argv[1:]

        if not host.startswith("http"):
            self.mainHost = f"http://{host}:{MAIN_PORT}/"
            self.vacancyHost = f"http://{host}:{VACANCY_PORT}/"

        if self.action != "check":
            self.flag_id, self.flag, self.vuln = args

        self.vacancyChecker = VacancyChecker(self.vacancyHost)

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
                die(Status.CHECKER_ERROR, message)

        except Exception as e:
            message = f"Exception: {e}\nStack:\n {traceback.format_exc()}",
            die(Status.CHECKER_ERROR, e)

    def check(self):
        log(f"Running CHECK on {self.mainHost} {self.vacancyHost}")
        self.vacancyChecker.check()

    def put(self):
        log(f"Running PUT on {self.mainHost} {self.vacancyHost} with {self.flag_id}:{self.flag}")

    def get(self):
        log(f"Running GET on {self.mainHost} {self.vacancyHost} with {self.flag_id}:{self.flag}")
        die(Status.OK, "Not implemented")


if __name__ == "__main__":
    Checker().main()
