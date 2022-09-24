#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import inspect
import os
import random
import re
import sys
# DEBUG -- logs to stderr, TRACE -- verbose log
from enum import Enum

import lorem
import requests

DEBUG = os.getenv("DEBUG", True)
TRACE = os.getenv("TRACE", False)
POOL = "ABCDEFGIJKLMNOPQRSTUVWXYZ0123456789"


class Status(Enum):
    OK = 101
    CORRUPT = 102
    MUMBLE = 103
    DOWN = 104
    CHECKER_ERROR = 110


class DownException(Exception):

    def __init__(self, *messages: str):
        self.Status = Status.DOWN
        self.Messages = messages
        super().__init__(self.Messages)

    def __str__(self):
        resultMessage = f"Status Code: {self.Status}\n"

        for message in self.Messages:
            resultMessage += str(message) + "\n"

        return resultMessage


class MumbleException(Exception):
    def __init__(self, *messages: str):
        self.Status = Status.MUMBLE
        self.Messages = messages
        super().__init__(self.Messages)

    def __str__(self):
        resultMessage = f"Status Code: {self.Status}\n"

        for message in self.Messages:
            resultMessage += str(message) + "\n"

        return resultMessage


class CheckerErrorException(Exception):
    def __init__(self, *messages: str):
        self.Status = Status.CHECKER_ERROR
        self.Messages = messages
        super().__init__(self.Messages)

    def __str__(self):
        resultMessage = f"Status Code: {self.Status}\n"

        for message in self.Messages:
            resultMessage += str(message) + "\n"

        return resultMessage


def log(obj):
    if DEBUG and obj:
        caller = inspect.stack()[1].function
        print(f"[{caller}] {obj}", file=sys.stderr, flush=True)
    return obj


def die(code: Status, *msg: str):
    print(code, file=sys.stderr, flush=True)

    for m in msg:
        print(m, file=sys.stderr, flush=True)
    exit(code.value)


def genName() -> str:
    return lorem.get_word(count=1) + str(random.randint(1, 999999))


def genFlag() -> str:
    flag = ""
    for _ in range(31):
        i = random.randint(0, len(POOL)-1)
        flag += POOL[i]
    return flag + "="


def checkHttpCode(resp: requests.Response):
    if 200 <= resp.status_code < 300:
        return

    if 500 <= resp.status_code:
        raise DownException(
            f"status code {resp.status_code} on {resp.url}",
            resp.text)

    if 400 <= resp.status_code < 500:
        raise MumbleException(
            f"status code {resp.status_code} on {resp.url}",
            resp.text)

    raise DownException(f"unexpected behaviour on {resp.url}", resp.text)


def find(pattern: str, text: str):
    match = re.search(pattern, text)

    if match == None:
        raise MumbleException(f"finding pattern '{pattern}' in text failed")

    return match[1]


def findExpected(text: str, pattern: str, expected: str):
    match = re.search(pattern, text)

    if match == None:
        raise MumbleException(
            f"pattern '{pattern}' not found in text",
            text)

    if match[1] != expected:
        raise MumbleException(
            "finding expected in received text failed",
            f"Expected: {expected}",
            f"Received: {match[1]}",
            text)


def findExpectedInMany(text: str, pattern: str, expected: str):
    matches = re.findall(pattern, text)

    for match in matches:
        if match == expected:
            return

    raise MumbleException(
        "finding expected in received text failed",
        f"Expected: {expected}",
        f"Received: {matches}",
        text)
