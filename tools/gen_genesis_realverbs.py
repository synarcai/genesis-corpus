#!/usr/bin/env python3
"""GENESIS layer: REAL VERB GENERA of GSM8K prose.

32's census gave the target lexicon (words after the
two heads: did/does/hours/miles/dollars/people/
cookies/pieces...). This layer shows the REAL verbs
(eats/buys/reads/runs/sells/makes/finds/uses) in the
same four-place discipline the detector buys:
[agent verb NUMBER item], three-verb episodes sharing
one (agent, item) key so the algebra market keeps its
raw material. Instances vary by pass; no glyph pairs
in-layer (worlds must not mix inside one file).
"""

from layer import emit
import verbthings  # noqa: E402


from plural import by_count


NAMES = ["cynthia", "james", "sara", "tom",
         "wanda", "carlos", "nina", "raj"]
# ИМЯ ОБЪЯВЛЕНО ПАКЕТОМ (дом имён, М-131): суд читает имя группой и сверяет
# с пакетом; имя, которого пакет не знает, не вправе войти в показ.
import json as _json
import pathlib as _pathlib
_ИМЕНА_ПАКЕТА = set(_json.loads((_pathlib.Path(__file__).resolve().parent / "langpacks"
                                  / "en.json").read_text(encoding="utf-8"))["person_names"])
assert set(NAMES) <= _ИМЕНА_ПАКЕТА, "имя не объявлено пакетом en"
ITEMS = ["cookies", "pages", "miles", "eggs",
         "cards", "shells", "pencils", "seeds"]
# (start, change, end) verb triples per genus:
# start + got-kind = has-kind; start − used = keeps
# (start, add-verb) and (start, remove-verb)
# pairs; asks: holds (after adding) / keeps
# (after removing)
ADD_PAIRS = [
    ("collected", "found"),
    ("wrote", "added"),
]
SUB_PAIRS = [
    ("baked", "sold"),
    ("packed", "used"),
]


def pass_shows(pi):
    base = pi * 31
    out = []
    for i in range(len(NAMES) * 6):
        nm = NAMES[(base + i) % len(NAMES)]
        # pair choice decoupled from polarity
        # (synchronized %2 starved baked/sold)
        (av1, av2) = ADD_PAIRS[
            ((base + i) // 2)
                % len(ADD_PAIRS)
        ]
        (sv1, sv2) = SUB_PAIRS[
            ((base + i) // 2)
                % len(SUB_PAIRS)
        ]
        a = (base + i * 5) % 9 + 4   # 4..12
        b = (base + i * 3) % 3 + 1   # 1..3
        # A VERB TAKES ITS OWN KIND OF THINGS (tools/verbthings.py): the thing
        # is drawn among those the show's verbs admit («wrote 8 pencils» no more).
        it = verbthings.подобрать((av1, av2) if (base + i) % 2 == 0 else (sv1, sv2), ITEMS, base + i * 3)
        # both polarities per triple: the change
        # verb v2 ADDS in one genus and REMOVES
        # in another — the algebra buys each law
        # from its own shows
        add = (base + i) % 2 == 0
        # ОТВЕТ И ЕГО КУЗНИЦА — ДВЕ ПОВЕРХНОСТИ ОДНОГО ФАКТА (М-166): 240
        # вычисленных ответов без шага. Разряд чередования — третий: нулевой
        # держит знак, первый — пару глаголов.
        forge = ((base + i) // 4) % 2 == 0
        if add:
            c = a + b
            out.append(
                f"{nm} {av1} {a} {by_count(a, it)}. "
                f"{nm} {av2} {b} {by_count(b, it)} "
                f"more. how many {it} does {nm} "
                f"hold now? {nm} holds {c} "
                f"{by_count(c, it)}"
                f"{f': {a} + {b} = {c}' if forge else ''}."
            )
        else:
            c = a - b
            out.append(
                f"{nm} {sv1} {a} {by_count(a, it)}. "
                f"{nm} {sv2} {b} {by_count(b, it)} "
                f"away. how many {it} does {nm} "
                f"keep? {nm} keeps {c} "
                f"{by_count(c, it)}"
                f"{f': {a} − {b} = {c}' if forge else ''}."
            )
    return out


def main():
    emit("datasets/genesis_realverbs.txt", pass_shows)


if __name__ == "__main__":
    main()
