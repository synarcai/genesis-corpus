#!/usr/bin/env python3
"""GENESIS layer: THE WIDE GSM8K LEXICON WAVE.

Census-ranked verbs and items of the real questions
(bought/buys/takes/eats/weighs/sold/ate/makes/needs/
scored/spends/gets/read/uses × hours…books), shown in
the four-place discipline, PLUS the possessive genus:
«janet s ducks lay 16 eggs» — the acting noun (ducks)
agents the episode; the owner rides as color. Shows
are OUR stories on OUR numbers.
"""

from layer import emit
import verbthings  # noqa: E402


from plural import by_count


NAMES_HOUSE = ["ava", "ben", "carla", "dan", "elena",
         "felix", "grace", "hugo", "iris",
         "janet", "kyle", "lena"]
# ИМЯ ОБЪЯВЛЕНО ПАКЕТОМ (дом имён, М-131): суд читает имя группой и сверяет
# с пакетом; имя, которого пакет не знает, не вправе войти в показ.
import json as _json
import pathlib as _pathlib
_ИМЕНА_ПАКЕТА = set(_json.loads((_pathlib.Path(__file__).resolve().parent / "langpacks"
                                  / "en.json").read_text(encoding="utf-8"))["person_names"])
# РЕГИСТР ИМЕНИ ЧИТАЕТСЯ ИЗ ПАКЕТА (05.09): список дома выбирает лица, пакет
# объявляет их письмо; «ann» дома есть «Ann» пакета, и в показ входит пакетное.
_ПО_СТРОЧНОМУ = {и.lower(): и for и in _ИМЕНА_ПАКЕТА}
NAMES = [_ПО_СТРОЧНОМУ.get(и.lower(), и) for и in NAMES_HOUSE]
assert set(NAMES) <= _ИМЕНА_ПАКЕТА, "имя не объявлено пакетом en"
PETS = ["ducks", "hens", "cats", "goats"]
ITEMS = ["hours", "minutes", "years", "miles",
         "feet", "pounds", "days", "people",
         "weeks", "inches", "students",
         "pieces", "points", "degrees",
         "cookies", "eggs", "boxes", "slices",
         "dollars", "seconds", "apples",
         "cups", "gallons", "pages", "packs",
         "calories", "months", "bananas",
         "books", "cards"]
ADD_PAIRS = [("gets", "buys"),
             ("scored", "adds"),
             ("makes", "earns"),
             ("reads", "writes")]
SUB_PAIRS = [("gets", "spends"),
             ("makes", "sells"),
             ("takes", "drops"),
             ("weighs", "loses")]
ASKS_ADD = [("hold now", "holds"),
            ("own now", "owns")]
ASKS_SUB = [("keep", "keeps"),
            ("save", "saves")]


def pass_shows(pi):
    base = pi * 41
    out = []
    for i in range(len(NAMES) * 12):
        nm = NAMES[
            (base + i + (i // 8) * 5)
            % len(NAMES)
        ]
        a = (base + i * 5) % 9 + 4
        b = (base + i * 3) % 3 + 1
        add = (base + i) % 2 == 0
        pick = ((base + i) // 2) % 4
        # A VERB TAKES ITS OWN KIND OF THINGS (tools/verbthings.py)
        itm = verbthings.подобрать(ADD_PAIRS[pick] if add else SUB_PAIRS[pick], ITEMS, base + i * 7)
        # ОТВЕТ И ЕГО КУЗНИЦА — ДВЕ ПОВЕРХНОСТИ ОДНОГО ФАКТА (М-166). Ответ
        # этого рода ВЫЧИСЛЯЕТСЯ из двух чисел вопроса, а шага не стояло ни
        # одного из 900: рынок мог купить соответствие, но не исполнителя.
        # Кузница встаёт РЯДОМ с голым ответом чередованием по номеру, и
        # разряд её свободен от разрядов глагола, вопроса и знака.
        forge = ((base + i) // 8) % 2 == 0
        if add:
            (v1, v2) = ADD_PAIRS[pick]
            (ask, av) = ASKS_ADD[
                ((base + i) // 4) % 2
            ]
            c = a + b
            out.append(
                f"{nm} {v1} {a} {by_count(a, itm)}. "
                f"{nm} {v2} {b} {by_count(b, itm)} "
                f"more. how many {itm} does {nm} "
                f"{ask}? {nm} {av} {c} "
                f"{by_count(c, itm)}"
                f"{f': {a} + {b} = {c}' if forge else ''}."
            )
        else:
            (v1, v2) = SUB_PAIRS[pick]
            (ask, av) = ASKS_SUB[
                ((base + i) // 4) % 2
            ]
            c = a - b
            out.append(
                f"{nm} {v1} {a} {by_count(a, itm)}. "
                f"{nm} {v2} {b} {by_count(b, itm)} "
                f"away. how many {itm} does {nm} "
                f"{ask}? {nm} {av} {c} "
                f"{by_count(c, itm)}"
                f"{f': {a} − {b} = {c}' if forge else ''}."
            )
        # possessive genus: the acting noun
        # agents; lay/give live here
        if i % 4 == 0:
            pet = PETS[
                (base + i) % len(PETS)
            ]
            a2 = (base + i * 3) % 8 + 3
            b2 = (base + i) % 3 + 1
            out.append(
                f"{nm} s {pet} lay {a2} "
                f"{by_count(a2, 'eggs')}. "
                f"{nm} s {pet} lay {b2} "
                f"{by_count(b2, 'eggs')} "
                f"more. how many eggs do the "
                f"{pet} hold now? the {pet} "
                f"holds {a2 + b2} eggs"
                f"{f': {a2} + {b2} = {a2 + b2}' if forge else ''}."
            )
    return out


def main():
    emit("datasets/genesis_gsmwide.txt", pass_shows)


if __name__ == "__main__":
    main()
