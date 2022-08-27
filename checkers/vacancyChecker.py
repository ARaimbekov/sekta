#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import uuid
import grpc
import vacancies_pb2_grpc
import vacancies_pb2
from common import log, die, Status
import lorem


class VacancyChecker:

    def __init__(self, host: str):
        host = "localhost:8033"
        channel = grpc.insecure_channel(host)
        self.stub = vacancies_pb2_grpc.VacanciesStub(channel)
        self.nameGen = lorem.sentence(count=1, comma=(0, 2), word_range=(3, 5))
        self.descriptionGen = lorem.sentence(
            count=1, comma=(0, 2), word_range=(6, 12))

    def check(self):
        log("run")
        self.vacancy = self.checkCreate()
        self.checkList()
        self.checkFailGet()
        self.vacancy = self.checkEdit()
        self.checkGet()

    def checkCreate(self):
        log("run")

        req = vacancies_pb2.CreateRequest(
            name=next(self.nameGen),
            description=next(self.descriptionGen),
            token=str(uuid.uuid4()),
            is_active=False
        )

        try:
            vacancy = self.stub.Create(req)
        except Exception as exception:
            die(Status.DOWN, "requesting create failed", str(exception))

        try:
            assert req.name == vacancy.name, "wrong name"
            assert req.description == vacancy.description, "wrong desrciption"
            assert req.token == vacancy.token, "wrong token"
        except AssertionError as err:
            die(Status.MUMBLE, str(err))

        return vacancy

    def checkList(self):
        log("run")

        try:
            resp = self.stub.List(vacancies_pb2.ListRequest())
        except Exception as exception:
            die(Status.DOWN, "requesting List failed", str(exception))

        vacancies = resp.vacancies

        try:
            vacancies[0].name
        except Exception:
            die(Status.MUMBLE, "field 'name' expected")

        try:
            vacancies[0].description
        except Exception:
            die(Status.MUMBLE, "field 'description' expected")

        try:
            vacancies[0].is_active
        except Exception:
            die(Status.MUMBLE, "field 'is_active' expected")

    def checkFailGet(self):
        log("run")

        try:
            self.stub.Get(vacancies_pb2.GetRequest(id=self.vacancy.id))
            die(Status.MUMBLE, "request expected to fail")
        except Exception as exception:
            if "vacancy not found or not activated" not in str(exception):
                die(Status.DOWN, "requesting Get failed", str(exception))

    def checkEdit(self):
        log("run")

        req = vacancies_pb2.Vacancy(
            id=self.vacancy.id,
            name=self.vacancy.name,
            description=next(self.descriptionGen),
            is_active=True,
            token=self.vacancy.token)

        try:
            vacancy = self.stub.Edit(req)
        except Exception as exception:
            die(Status.DOWN, "requesting Edit failed", str(exception))

        try:
            assert req.name == vacancy.name, "wrong name"
            assert req.description == vacancy.description, "wrong desrciption"
            assert req.is_active == vacancy.is_active, "wrong is_active"
            assert req.token == vacancy.token, "wrong token"
        except AssertionError as err:
            die(Status.MUMBLE, str(err))

        return vacancy

    def checkGet(self):
        log("run")

        req = vacancies_pb2.GetRequest(id=self.vacancy.id)
        try:
            vacancy = self.stub.Get(req)
        except Exception as exception:
            if "vacancy not found or not activated" in str(exception):
                die(Status.MUMBLE, "expected to be activated", str(exception))
            else:
                die(Status.DOWN, "requesting Get failed", str(exception))

        try:
            assert self.vacancy.name == vacancy.name, "wrong name"
            assert self.vacancy.description == vacancy.description, "wrong desrciption"
            assert self.vacancy.is_active == vacancy.is_active, "wrong is_active"
            assert self.vacancy.token == vacancy.token, "wrong token"
        except AssertionError as err:
            die(Status.MUMBLE, str(err))
