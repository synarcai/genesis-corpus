#!/usr/bin/env python3
"""GENESIS layer: THE AGGREGATE GENUS.

An aggregate is a FACT OF A PLURAL BEARER: «ava
and ben hold 8 coins» — the bearer is the set
{ava, ben}. The market buys the LIST WORD («and»)
by the shows' own arithmetic: the plural fact's
value must equal the sum of the bearers' own
adjacent facts (quorum, one refutation kills).
Question surfaces (together / in all /
altogether / combined) ride as tails — the
bought list word alone carries the genus.

Discipline: two base facts, the aggregate ask,
the plural-bearer answer. Singular agreement by
count (plural.by_count); i//8 decoupling.
"""

from layer import emit


from gsm_items import ANIMATE
from gsm_items import ITEMS as CENSUS_ITEMS
from plural import by_count

NAMES_HOUSE = ["ava", "ben", "carla", "dan",
         "elena", "felix", "grace", "hugo"]
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
# THE AGGREGATE GENUS MUST NOT BE BOUGHT ON EIGHT
# WORDS. The layer's own eight are kept (they are
# the ones the sibling worlds already show, and a
# genus shared across worlds is worth more than a
# genus alone), and the census lexicon of the real
# benchmark joins them: 66 items the g1 band
# actually asks about.
LOCAL = ["apples", "cookies", "coins", "books",
         "eggs", "pages", "points", "cards"]
ITEMS = LOCAL + [w for w in CENSUS_ITEMS
                 if w not in LOCAL]
# (question tail, answer verb, plural subject) —
# «they» is the surface GSM8K actually uses, and
# it keeps the list word in the ANSWER, where the
# market reads it.
# A THING IS HELD AND OWNED; A PERSON IS NOT. Merging the census
# lexicon brought animate items into this layer, and 36 shows said
# «own 5 teachers» — grammatical and false about the world. Animate
# bearers of the aggregate keep only the surfaces built on «have»,
# and the animacy itself is declared in gsm_items, where no census
# could have found it.
ASKS = [("hold together", "hold", False),
        ("own in all", "own", False),
        ("hold altogether", "hold", False),
        ("own combined", "own", False),
        ("have in total", "have", False),
        ("have altogether", "have", True),
        ("hold in all", "hold", True),
        ("own together", "own", True)]


def pass_shows(pi):
    base = pi * 47
    out = []
    for i in range(len(NAMES) * 9):
        a = NAMES[
            (base + i + (i // 8) * 5)
            % len(NAMES)
        ]
        b = NAMES[
            (base + i + (i // 8) * 5 + 3
             + i % 3)
            % len(NAMES)
        ]
        if a == b:
            continue
        it = ITEMS[
            (base + i * 5) % len(ITEMS)
        ]
        # 1..9 and 1..6: the old strides let the
        # first addend take only {2,3,5,7,8}, so
        # four of nine counts were never shown in
        # the leading place — «1» among them, the
        # one that chooses the singular.
        x = (base + i * 7) % 9 + 1
        y = (base + i * 5) % 6 + 1
        pool = ([q for q in ASKS if q[1] == "have"]
                if it in ANIMATE else ASKS)
        (ask, av, pron) = pool[
            ((base + i) // 2) % len(pool)
        ]
        who = "they" if pron else f"{a} and {b}"
        # ОТВЕТ И ЕГО КУЗНИЦА — ДВЕ ПОВЕРХНОСТИ ОДНОГО ФАКТА (М-166). Сумма
        # агрегата вычисляется из чисел вопроса, а шага не стояло ни одного
        # из 430 показов. Кузница берётся чередованием по номеру и на своём
        # разряде у каждой из двух волн: у пары свободен нулевой (вопрос
        # берётся со второго), у тройки — второй, ибо тройка идёт шагом
        # четыре и нулевой разряд в ней постоянен.
        forge = (base + i) % 2 == 0
        out.append(
            f"{a} has {x} {by_count(x, it)}. "
            f"{b} has {y} {by_count(y, it)}. "
            f"how many {it} do {who} "
            f"{ask}? {a} and {b} {av} "
            f"{x + y} {by_count(x + y, it)}"
            f"{f': {x} + {y} = {x + y}' if forge else ''}."
        )
        # the TRIPLE wave: bearers meet by
        # adjacency (life's comma is cut) with
        # the list word before the last — the
        # chain genus, not a second pair
        if i % 4 == 0:
            c = NAMES[
                (base + i + 5) % len(NAMES)
            ]
            if c not in (a, b):
                z = (base + i) % 4 + 1
                s = x + y + z
                forge3 = ((base + i) // 4) % 2 == 0
                # ДВА ШАГА: смежность режется дважды, и кузница обязана
                # показать промежуточную сумму, а не только итог.
                steps3 = f": {x} + {y} = {x + y}, {x + y} + {z} = {s}"
                out.append(
                    f"{a} has {x} "
                    f"{by_count(x, it)}. "
                    f"{b} has {y} "
                    f"{by_count(y, it)}. "
                    f"{c} has {z} "
                    f"{by_count(z, it)}. "
                    f"how many {it} do "
                    f"{a} {b} and {c} "
                    f"{ask}? {a} {b} and "
                    f"{c} {av} {s} "
                    f"{by_count(s, it)}"
                    f"{steps3 if forge3 else ''}."
                )
    return out


def main():
    emit("datasets/genesis_aggregate.txt", pass_shows)


if __name__ == "__main__":
    main()
