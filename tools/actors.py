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

КОРЕНЬ = pathlib.Path(__file__).resolve().parents[1]
МАНИФЕСТ = КОРЕНЬ / "datasets" / "GENESIS-MANIFEST.json"


class Слой:
    """Протокол палаты: создаётся пустым и впитывает файл мира."""

    def __init__(self):
        self.деятели = ()

    def впитать(self, путь):
        try:
            м = json.loads(МАНИФЕСТ.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            return
        имя = pathlib.Path(путь).name
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
