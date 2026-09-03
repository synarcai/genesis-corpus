#!/usr/bin/env python3
"""THE CLOSED WORLD — a line of a world every line of which is a shape of
its court, and which that court does not recognise, is a lie.

The gate demands that every line be judged by SOME court; a corrupted line
of the rates world («th book costs 26 dollars…», «he ha 56 dollars…») was
judged by the count court alone and passed (mutation 04.09). Where the
world's own court covers all of the world's honest lines, silence of that
court on a line of that world is not honest silence but a shape the world
never wrote. A court declares its closed worlds by name; the palata hands
it the layer of the file being judged (the world's name, read from the
manifest — the gate's temporary «<world>.txt.ворота» included).
"""
import json
import pathlib

КОРЕНЬ = pathlib.Path(__file__).resolve().parents[1]
МАНИФЕСТ = КОРЕНЬ / "datasets" / "GENESIS-MANIFEST.json"


class Слой:
    """Протокол палаты: создаётся пустым и впитывает файл мира."""

    def __init__(self):
        self.мир = None

    def впитать(self, путь):
        имя = pathlib.Path(путь).name
        for суффикс in (".ворота",):
            if имя.endswith(суффикс):
                имя = имя[:-len(суффикс)]
        try:
            м = json.loads(МАНИФЕСТ.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            return
        for мир in м.get("worlds", ()):
            if pathlib.Path(мир.get("file", "")).name == имя:
                self.мир = мир.get("name")
                return


def замкнут(слой, миры):
    """Is the file being judged one of the court's closed worlds?"""
    return слой is not None and getattr(слой, "мир", None) in миры
