#!/usr/bin/env python3
"""ДЕЯТЕЛИ МИРА — объявление читается судом из манифеста.

Дом имён (М-131, обобщён 03.09): имена лиц объявлены пакетом языка
(`langpacks/<lang>.json`, `person_names`), а МИР объявляет в манифесте,
что его деятели — лица пакета (`actors: ["person_names:en", …]`). Суд,
получив слой мира, знает, вправе ли он звать чужое имя ложью: в мире,
объявившем деятелей, слово на месте лица, которого пакет не знает, есть
ложь записи; в мире, не объявившем, — чужая рамка, и суд молчит.
"""
import json
import pathlib

import closedworld

КОРЕНЬ = pathlib.Path(__file__).resolve().parents[1]
МАНИФЕСТ = КОРЕНЬ / "datasets" / "GENESIS-MANIFEST.json"


class Слой(closedworld.Слой):
    """Протокол палаты: создаётся пустым и впитывает файл мира.

    СЛОЙ ОДИН, А ПОЛЕЙ У НЕГО ДВА (06.09). Палата кладёт в `слои[имя]` РОВНО ОДИН
    предмет, и суд, читающий деятелей, не может взять вторым слоем имя мира: два
    слоя в одном имени столкнулись бы молча. Потому имя мира едет здесь же — оно
    берётся тем же чтением манифеста по имени файла, что и деятели, и стоит в
    поле `мир`, которое читает `closedworld.замкнут`.

    Замыкание есть надстройка над чтением, а не замена ему: суд, читающий слой,
    получает его целиком, а обёртка `closedworld.замкнуть_слоем` слой ПЕРЕДАЁТ.
    """

    def __init__(self):
        super().__init__()      # поле `мир` — для закона замкнутого мира
        self.деятели = ()

    def впитать(self, путь):
        super().впитать(путь)   # имя мира из манифеста
        try:
            м = json.loads(МАНИФЕСТ.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            return
        # THE GATE JUDGES A TEMPORARY «<world>.ворота» — the world's name is
        # the part before that suffix (04.09: the actor law never fired at
        # the gate, «маш купила» passed there and was caught only by the
        # instruments).
        имя = pathlib.Path(путь).name
        if имя.endswith(".ворота"):
            имя = имя[:-len(".ворота")]
        for мир in м.get("worlds", ()):
            if pathlib.Path(мир.get("file", "")).name == имя:
                а = мир.get("actors") or ()
                self.деятели = tuple([а] if isinstance(а, str) else а)
                return

    def лица(self, язык):
        """Объявил ли мир деятелями лица пакета этого языка."""
        return f"person_names:{язык}" in self.деятели


def имена(язык):
    """Объявленные имена лиц пакета языка (множество, нижний регистр)."""
    пакет = КОРЕНЬ / "tools" / "langpacks" / f"{язык}.json"
    try:
        return frozenset(json.loads(пакет.read_text(encoding="utf-8")).get("person_names", ()))
    except (OSError, ValueError):
        return frozenset()
