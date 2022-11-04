#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
import random
import uuid

POOL = "ABCDEFGIJKLMNOPQRSTUVWXYZ0123456789"


class TextGenerator:
    def __init__(self, fileName: str):
        f = open(fileName)
        self.storage = json.load(f)
        f.close()

    def GenUserName(self) -> str:
        username = random.choice(self.storage['username'])
        randnum = str(random.randint(1, 999))
        return f"{username} {randnum}"

    def GenPassword(self) -> str:
        return str(uuid.uuid4())

    def GenSectInfo(self) -> tuple[str, str]:
        acolyte_alias = random.choice(self.storage['acolytes_alias'])
        idol = random.choice(self.storage['idol'])
        randNum = str(random.randint(1, 999))
        name = f"{acolyte_alias} of {idol} {randNum}"
        description = f"Group of {acolyte_alias}, who believe in {idol}"
        return name, description

    def GenVacancyDescription(self) -> str:
        require = random.choice(self.storage['vacancy']['require_alias'])

        adjectives = random.sample(
            self.storage['vacancy']["adjective"], random.randint(1, 3))
        adjectives = ", ".join(adjectives)

        benefits = random.sample(
            self.storage['vacancy']["benefit"], random.randint(2, 5))
        benefits = " + "+("\n + ".join(benefits))

        return f"{require} {adjectives} acolytes in our sect. Our benefits:\n{benefits}"

    def GenFlag(self) -> str:
        flag = ""
        for _ in range(31):
            i = random.randint(0, len(POOL)-1)
            flag += POOL[i]
        return flag + "="
