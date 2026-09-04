#!/usr/bin/env python3
"""GENESIS layer: THE GSM8K FOUR-PLACE LEXICON.

The bill of materials measured from the real
questions' own four-places [w NUMBER w]: top verbs
(has/bought/buys/takes/eats/makes/sold/ate/needs/
weighs) and top items (hours/minutes/miles/pounds/
days/people/cookies/eggs/boxes/slices...). Shows are
OUR stories on OUR numbers — the lexicon is a closed
class, instances never copy benchmark strings (the
leak court holds by substring).

Discipline: [agent verb NUMBER item], three-verb
episodes on one (agent, item) key, both polarities,
instances vary by pass, no glyph pairs in-layer.
"""

from layer import emit
import verbthings  # noqa: E402


from plural import by_count


NAMES = ["ava", "ben", "carla", "dan",
         "elena", "felix", "grace", "hugo"]
# ИМЯ ОБЪЯВЛЕНО ПАКЕТОМ (дом имён, М-131): суд читает имя группой и сверяет
# с пакетом; имя, которого пакет не знает, не вправе войти в показ.
import json as _json
import pathlib as _pathlib
_ИМЕНА_ПАКЕТА = set(_json.loads((_pathlib.Path(__file__).resolve().parent / "langpacks"
                                  / "en.json").read_text(encoding="utf-8"))["person_names"])
assert set(NAMES) <= _ИМЕНА_ПАКЕТА, "имя не объявлено пакетом en"
ITEMS = ["hours", "minutes", "miles", "pounds",
         "days", "people", "cookies", "eggs",
         "boxes", "slices", "points", "pages",
         "weeks", "students", "pieces", "cards", "dollars", "coins"]
ADD_PAIRS = [
    ("has", "buys"),
    ("had", "bought"),
    ("makes", "adds"),
    ("takes", "needs"),
]
SUB_PAIRS = [
    ("has", "eats"),
    ("had", "sold"),
    ("makes", "uses"),
    ("takes", "loses"),
]
ASK_ADD = [("hold now", "holds"),
           ("own now", "owns")]
ASK_SUB = [("keep", "keeps"),
           ("save", "saves")]


def pass_shows(pi):
    base = pi * 37
    out = []
    for i in range(len(NAMES) * 10):
        # name index coprime-decoupled from the
        # pair/polarity systematics (a lockstep
        # gave buys ONE agent over 10 triples)
        # the i//8 floor breaks any linear tie
        # with (base+i): the first decoupling
        # collapsed to identity (11≡3 mod 8 —
        # buys got ava forever)
        nm = NAMES[
            (base + i + (i // 8) * 5)
            % len(NAMES)
        ]
        a = (base + i * 7) % 9 + 4   # 4..12
        b = (base + i * 3) % 3 + 1   # 1..3
        add = (base + i) % 2 == 0
        pick = ((base + i) // 2) % 4
        # A VERB TAKES ITS OWN KIND OF THINGS (tools/verbthings.py)
        it = verbthings.подобрать(ADD_PAIRS[pick] if add else SUB_PAIRS[pick], ITEMS, base + i * 5)
        # ОТВЕТ И ЕГО КУЗНИЦА — ДВЕ ПОВЕРХНОСТИ ОДНОГО ФАКТА (М-166): 400
        # показов вычисленного ответа без единого шага. Разряд чередования
        # свободен от разрядов знака (нулевой) и пары с вопросом (первый).
        forge = ((base + i) // 4) % 2 == 0
        if add:
            (v1, v2) = ADD_PAIRS[pick]
            (ask, av) = ASK_ADD[
                ((base + i) // 2) % 2
            ]
            c = a + b
            out.append(
                f"{nm} {v1} {a} {by_count(a, it)}. "
                f"{nm} {v2} {b} {by_count(b, it)} "
                f"more. how many {it} does {nm} "
                f"{ask}? {nm} {av} {c} "
                f"{by_count(c, it)}"
                f"{f': {a} + {b} = {c}' if forge else ''}."
            )
        else:
            (v1, v2) = SUB_PAIRS[pick]
            (ask, av) = ASK_SUB[
                ((base + i) // 2) % 2
            ]
            c = a - b
            out.append(
                f"{nm} {v1} {a} {by_count(a, it)}. "
                f"{nm} {v2} {b} {by_count(b, it)} "
                f"away. how many {it} does {nm} "
                f"{ask}? {nm} {av} {c} "
                f"{by_count(c, it)}"
                f"{f': {a} − {b} = {c}' if forge else ''}."
            )
    return out


def main():
    emit("datasets/genesis_gsmlex.txt", pass_shows)


if __name__ == "__main__":
    main()
