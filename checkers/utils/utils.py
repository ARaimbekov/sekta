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


def log(obj):
    if DEBUG and obj:
        caller = inspect.stack()[1].function
        print(f"[{caller}] {obj}", file=sys.stderr, flush=True)
    return obj


def die(code: excepts.Status, *msg: str):
    print(code, file=sys.stderr, flush=True)

    for m in msg:
        print(m, file=sys.stderr, flush=True)
    exit(code.value)


def find(pattern: str, text: str):
    match = re.search(pattern, text)

    if match == None:
        raise excepts.MumbleException(
            f"finding pattern '{pattern}' in text failed")

    return match[1]


def findExpected(text: str, pattern: str, expected: str):
    match = re.search(pattern, text)

    if match == None:
        raise excepts.MumbleException(
            f"pattern '{pattern}' not found in text",
            text)

    if match[1] != expected:
        raise excepts.MumbleException(
            "finding expected in received text failed",
            f"Expected: {expected}",
            f"Received: {match[1]}",
            text)


def findExpectedInMany(text: str, pattern: str, expected: str):
    matches = re.findall(pattern, text)

    for match in matches:
        if match == expected:
            return

    raise excepts.MumbleException(
        "finding expected in received text failed",
        f"Expected: {expected}",
        f"Received: {matches}",
        text)
