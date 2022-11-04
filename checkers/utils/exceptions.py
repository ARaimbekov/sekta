#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from enum import Enum


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


class CorruptException(Exception):
    def __init__(self, *messages: str):
        self.Status = Status.CORRUPT
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
