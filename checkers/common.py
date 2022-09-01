#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# DEBUG -- logs to stderr, TRACE -- verbose log
from enum import Enum
import inspect
import os
import sys


class Status(Enum):
    OK = 101
    CORRUPT = 102
    MUMBLE = 103
    DOWN = 104
    CHECKER_ERROR = 110


DEBUG = os.getenv("DEBUG", True)
TRACE = os.getenv("TRACE", False)


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
