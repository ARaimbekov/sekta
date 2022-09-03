#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# DEBUG -- logs to stderr, TRACE -- verbose log
from enum import Enum
import inspect
import os
import sys
import lorem
import re
import random
import requests

DEBUG = os.getenv("DEBUG", True)
TRACE = os.getenv("TRACE", False)


class Status(Enum):
    OK = 101
    CORRUPT = 102
    MUMBLE = 103
    DOWN = 104
    CHECKER_ERROR = 110


class CheckerException(Exception):

    def __init__(self, status: Status, *messages: str):
        self.Status = status
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


def getRandomName() -> str:
    return lorem.get_word(count=1) + str(random.randint(1, 999999))


def checkHttpCode(resp: requests.Response, requestName: str):
    if 200 <= resp.status_code < 300:
        return

    if 500 <= resp.status_code:
        status = Status.DOWN
    elif 400 <= resp.status_code < 500:
        status = Status.MUMBLE
    else:
        raise CheckerException(Status.DOWN,
                               f"unexpected behaviour on {requestName}", resp.text)

    raise CheckerException(
        status, f"status code {resp.status_code} on {requestName}", resp.text)


def find(pattern: str, text: str,):
    match = re.search(pattern, text)

    if match == None:
        raise CheckerException(
            Status.MUMBLE, f"finding pattern '{pattern}' in text failed")

    return match[1]


def findExpected(text: str, pattern: str, expected: str):
    match = re.search(pattern, text)

    if match == None:
        raise CheckerException(
            Status.MUMBLE, f"pattern '{pattern}' not found in text")

    if match[1] != expected:
        raise CheckerException(Status.MUMBLE,
                               "finding expected in received text failed",
                               f"Expected: {expected}",
                               f"Received: {match[1]}")


def findExpectedInMany(text: str, pattern: str, expected: str):
    matches = re.findall(pattern, text)

    for match in matches:
        if match == expected:
            return

    raise CheckerException(Status.MUMBLE,
                           "finding expected in received text failed",
                           f"Expected: {expected}",
                           f"Received: {matches}")
