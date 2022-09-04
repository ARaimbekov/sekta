#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from sektaChecker.user import User
from common import CheckerException, Status, log, getRandomName


class SektaChecker:
    def __init__(self, host: str, port: int):
        self.Host = f"http://{host}:{port}"

    def check(self):
        log(" ")

        master = User(host=self.Host, name="master")
        master.askRoot()
        master.register()
        master.login()
        master.createSekta()

        dummy = User(host=self.Host, name="dummy")
        dummy.askRoot()
        dummy.register()
        dummy.login()

        dummy2 = User(host=self.Host, name="dummy2")
        dummy2.askRoot()
        dummy2.register()
        dummy2.login()

        dummySecretName = "DYMMY"+getRandomName()
        dummy2SecretName = "DYMMY2"+getRandomName()

        master.invite(dummy.Id, dummySecretName)
        master.invite(dummy2.Id,  dummy2SecretName)

        master.getAllSects()
        master.getMySects()
        acolytes = master.getMySect()
        self.checkAcolyteInSect(dummy, acolytes)
        self.checkAcolyteInSect(dummy2, acolytes)

        master.sacrifice(dummy.Id)
        master.sacrifice(dummy2.Id)

        acolytes = master.getMySect()
        self.checkAcolyteIsDead(dummy, dummySecretName, acolytes)
        self.checkAcolyteIsDead(dummy2, dummy2SecretName, acolytes)

        master.logout()

        try:
            master.getMySects()
            raise CheckerException(Status.MUMBLE, "logout doesnt worked")
        except CheckerException as e:
            if e.Status != Status.MUMBLE:
                raise e

    def checkAcolyteInSect(self, acolyte: User, acolytes: list):

        for a in acolytes:
            if acolyte.Name == a[0]:
                return

        raise CheckerException(
            Status.MUMBLE, f"{acolyte} expected to be acolyte in {acolytes}")

    def checkAcolyteIsDead(self, acolyte: User, secretName: str, acolytes: list):
        for a in acolytes:
            if secretName in a[1]:
                return

        raise CheckerException(
            Status.MUMBLE, f"{acolyte.Name} expected to be dead", acolytes)
