#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import inspect
import os
import re
import sys

import utils.exceptions as excepts

# DEBUG -- logs to stderr, TRACE -- verbose log


DEBUG = os.getenv("DEBUG", True)
TRACE = os.getenv("TRACE", False)


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def log(obj):
    if DEBUG and obj:
        caller = inspect.stack()[1].function
        print(f"{bcolors.OKCYAN}[{caller}]{bcolors.ENDC} {obj}", file=sys.stderr, flush=True)
    return obj


def die(code: excepts.Status, *msg: str):
    errMessage = f""" {bcolors.FAIL}
    ERROR OCCURED
    STATUS CODE: {code}
    ERRORS:
    """

    print(errMessage, file=sys.stderr, flush=True)

    for m in msg:
        print(f"(!) {m}", file=sys.stderr, flush=True)
        print("", file=sys.stderr, flush=True)

    print(bcolors.ENDC, file=sys.stderr, flush=True)

    exit(code.value)


def find(text: str,
         pattern: str,
         description: str):

    match = re.search(pattern, text)

    if match == None:

        if description == "":
            description = "Finding pattern failed"

        raise excepts.MumbleException(
            f"Description: {description}",
            f"Pattern: {pattern}",
            f"Text: {text}")

    return match[1]


def findExpected(text: str,
                 pattern: str,
                 expected: str,
                 description: str):

    received = find(text, pattern, description)

    if expected != received:

        if description == "":
            description = "Finding expected in received text failed"

        raise excepts.MumbleException(
            f"Description: {description}",
            f"Expected: {expected}",
            f"Received: {received}",
            f"Text: {text}")


def findExpectedInMany(text: str,
                       pattern: str,
                       expected: str,
                       description: str):

    matches = re.findall(pattern, text)

    for match in matches:
        if match == expected:
            return

    if description == "":
        description = "finding expected in received text failed"

    raise excepts.MumbleException(
        f"Description: {description}",
        f"Expected: {expected}",
        f"Received: {matches}",
        f"Text: {text}")
