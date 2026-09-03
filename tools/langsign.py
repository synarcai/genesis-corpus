#!/usr/bin/env python3
"""THE SIGN OF THE LANGUAGE — which pack's function words a line carries.

A court of one language must not judge a line of another: the English count
court read German «2 mal 3 hat die Fläche» as «3 hat» → «hats», Dutch «310
cent» as a missing «s». The packs declare their FUNCTION WORDS (articles,
copulas, conjunctions, question words); the language of a line is the pack
whose function words it carries most, and no language when no pack leads —
a line of bare numbers, or a tie («is» is English and Dutch alike). Courts
of one language ask this house before judging.
"""
import json
import pathlib
import re

ПАКЕТЫ = pathlib.Path(__file__).resolve().parent / "langpacks"
СЛОВО = re.compile(r"[^\W\d_]+(?:'[^\W\d_]+)?")


def _слова():
    вон = {}
    for путь in sorted(ПАКЕТЫ.glob("*.json")):
        try:
            пакет = json.loads(путь.read_text(encoding="utf-8"))
        except ValueError:
            continue
        слова = пакет.get("function_words")
        if isinstance(слова, list) and слова:
            вон[путь.stem] = frozenset(w.lower() for w in слова)
    return вон


СЛОВА = _слова()


def счёт(строка):
    """{язык: number of its function words in the line}."""
    слова = [w.lower() for w in СЛОВО.findall(строка)]
    return {язык: sum(1 for w in слова if w in набор) for язык, набор in СЛОВА.items()}


def язык(строка):
    """The pack that leads by function words, or None on silence or a tie."""
    с = счёт(строка)
    if not с:
        return None
    лучшие = sorted(с.items(), key=lambda kv: -kv[1])
    if лучшие[0][1] == 0 or (len(лучшие) > 1 and лучшие[1][1] == лучшие[0][1]):
        return None
    return лучшие[0][0]
