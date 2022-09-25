#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import copy

import grpc

import vacancyChecker.vacancies_pb2 as v
import vacancyChecker.vacancies_pb2_grpc as v_grpc
from common import DownException, MumbleException, genDescription, log


class Vacancy:
    def __init__(self, id: int, sectId: int, description: str, isActive: bool, token: str) -> None:
        self.Id = id
        self.SectId = sectId
        self.Description = description
        self.IsActive = isActive
        self.Token = token


class SessionVacancy:
    def __init__(self, host: str, debugName: str):
        self.Host = host
        self.debugName = debugName
        channel = grpc.insecure_channel(self.Host)
        self.stub = v_grpc.VacanciesStub(channel)

    def Create(self, sect_id: int) -> Vacancy:
        log(f"[{self.debugName}]")

        description = self._genDescription()

        req = v.CreateRequest(
            sect_id=sect_id,
            description=description,
        )

        try:
            resp = self.stub.Create(req)
        except Exception as e:
            raise DownException("create method failed", str(e))

        self.Vacancy = Vacancy(
            id=resp.id,
            sectId=resp.sect_id,
            description=resp.description,
            isActive=resp.is_active,
            token=resp.token,
        )

        try:
            assert self.Vacancy.SectId == sect_id, "wrong sect id"
            assert self.Vacancy.Description == description, "wrong desrciption"
        except AssertionError as e:
            raise MumbleException(str(e))

        return self.Vacancy

    def GetBad(self, vacancyId: int):
        log(f"[{self.debugName}]")

        req = v.GetRequest(id=vacancyId)

        try:
            self.stub.Get(req)
        except Exception:
            return

        raise MumbleException("get method expected to fail")

    def Edit(self, description: str, isActive: bool):
        log(f"[{self.debugName}]")

        req = v.Vacancy(
            id=self.Vacancy.Id,
            description=description,
            is_active=isActive,
            token=self.Vacancy.Token)

        try:
            resp = self.stub.Edit(req)
        except Exception as e:
            raise DownException("edit method failed", str(e))

        self.Vacancy.Description = resp.description
        self.Vacancy.IsActive = resp.is_active

        try:
            assert description == self.Vacancy.Description, "wrong desrciption"
            assert isActive == self.Vacancy.IsActive, "wrong is active"
        except AssertionError as e:
            raise MumbleException(
                str(e),
                "Expected",
                description,
                isActive,
                "Received",
                self.Vacancy.Description,
                self.Vacancy.IsActive)

    def Get(self, vacancyId: int):
        log(f"[{self.debugName}]")

        req = v.GetRequest(id=vacancyId)

        try:
            resp = self.stub.Get(req)
        except Exception as e:
            raise DownException("get method failed", str(e))

        receivedVacancy = Vacancy(
            id=resp.id,
            sectId=resp.sect_id,
            description=resp.description,
            isActive=resp.is_active,
            token=resp.token)

        try:
            assert vars(self.Vacancy) == vars(receivedVacancy), "wrong vacancy"
        except AssertionError as e:
            raise MumbleException(e,
                                  "Expected:", vars(self.Vacancy),
                                  "Received:", vars(receivedVacancy))

    def List(self):
        log(f"[{self.debugName}]")

        try:
            resp = self.stub.List(v.ListRequest())
        except Exception as e:
            raise DownException("list method failed", str(e))

        if len(resp.vacancies) == 0:
            raise MumbleException('list method expect at least 1 vacancy')

        firstVacancy = Vacancy(
            id=resp.vacancies[0].id,
            sectId=resp.vacancies[0].sect_id,
            description=resp.vacancies[0].description,
            isActive=resp.vacancies[0].is_active,
            token=resp.vacancies[0].token)

        noTokenVacancy = copy.copy(self.Vacancy)
        noTokenVacancy.Token = ""

        try:
            assert vars(noTokenVacancy) == vars(firstVacancy), "wrong vacancy"
        except AssertionError as e:
            raise MumbleException(e,
                                  "Expected:", vars(self.Vacancy),
                                  "Received:", vars(firstVacancy))

    def _genDescription(self):
        return genDescription()
