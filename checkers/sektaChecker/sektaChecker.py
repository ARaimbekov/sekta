#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import random
from sektaChecker.session import Session
from common import CheckerException, Status, genFlag, log, genName


class SektaChecker:
    def __init__(self, host: str, port: int):
        self.Host = f"http://{host}:{port}"

    def Check(self):
        log(" ")

        master = Session(host=self.Host, name="master")
        master.askRoot()
        master.register()
        master.login()
        master.createSekta(genName())

        dummy = Session(host=self.Host, name="dummy")
        dummy.askRoot()
        dummy.register()
        dummy.login()

        dummy2 = Session(host=self.Host, name="dummy2")
        dummy2.askRoot()
        dummy2.register()
        dummy2.login()

        dummySecretName = genFlag()
        dummy2SecretName = genFlag()

        master.invite(dummy.Id, dummySecretName)
        master.invite(dummy2.Id,  dummy2SecretName)

        master.getAllSects()
        master.getMySects()
        acolytes = master.getMySect()
        self.__checkAcolyteInSect(dummy, acolytes)
        self.__checkAcolyteInSect(dummy2, acolytes)

        master.sacrifice(dummy.Id)
        master.sacrifice(dummy2.Id)

        acolytes = master.getMySect()
        self.__checkAcolyteIsDead(dummy, dummySecretName, acolytes)
        self.__checkAcolyteIsDead(dummy2, dummy2SecretName, acolytes)

        master.logout()

        try:
            master.getMySects()
            raise CheckerException(Status.MUMBLE, "logout doesnt worked")
        except CheckerException as e:
            if e.Status != Status.MUMBLE:
                raise e

    def Put(self, flagId: int, flag: str):
        master = Session(host=self.Host, name="master")
        master.register()
        master.login()
        master.createSekta(genName())

        dummy = Session(host=self.Host, name="dummy")
        dummy.register()
        dummy.login()
        master.invite(dummy.Id, flag)

        for _ in range(random.randint(5, 5)):
            dummy = Session(host=self.Host, name="dummy")
            dummy.register()
            dummy.login()
            master.invite(dummy.Id, genName())

        return master.SectName

    def Get(self, flagId: int, flag: str):
        pass

    def __checkAcolyteInSect(self, acolyte: Session, acolytes: list):

        for a in acolytes:
            if acolyte.Name == a[0]:
                return

        raise CheckerException(
            Status.MUMBLE, f"{acolyte} expected to be acolyte in {acolytes}")

    def __checkAcolyteIsDead(self, acolyte: Session, secretName: str, acolytes: list):
        for a in acolytes:
            if secretName in a[1]:
                return

        raise CheckerException(
            Status.MUMBLE, f"{acolyte.Name} expected to be dead", acolytes)
