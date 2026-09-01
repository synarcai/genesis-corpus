#!/usr/bin/env python3
"""GENESIS layer: CONVERSIONS (genus 10) — one unit told in another.

    1 day = 24 hours.
    a day has 24 hours.
    в сутках 24 часа.

A conversion is NOT arithmetic and must not be judged as such: the
numbers on the two sides are equal only TOGETHER WITH THEIR UNITS, and
`scripts/arith_court.py` was taught this the hard way — generalised to
two-sided equalities, it declared 375 honest conversions false in one
run. The court now stands aside from any equality carrying no
operation; this genus gets its own market instead.

THE RATIO IS SHOWN, NEVER STATED TWICE THE SAME WAY. Each fact appears
scaled («3 hours = 180 minutes»), so the link market reads a RATIO from
several instances rather than memorising one line.

RUSSIAN AGREEMENT IS NOT REIMPLEMENTED HERE. The 1 / 2-4 / 5+ rule
with its teens exception lives in tools/langpacks/ru.json as data, and
this layer READS it. A second copy would drift from the first the day
either was touched — the same reason the item lexicon became one file.
"""

from layer import emit


import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from langpack import count_form_index  # noqa: E402

RU_PACK = json.loads(
    (pathlib.Path(__file__).resolve().parent
     / "langpacks/ru.json").read_text(encoding="utf-8")
)
RU_RULE = {"forms": ["one", "few", "many"],
           "count_agreement": RU_PACK["count_agreement"]}

# (english singular, english plural, ratio, russian «в ЧЁМ»,
#  russian NOMINATIVE of that same word, russian target forms
#  one/few/many) — every fact true, none derived.
# ИМЕНИТЕЛЬНЫЙ ОБЪЯВЛЕН ОТДЕЛЬНО, а не отрезан от предложного: первая
# редакция брала второе слово из «в году» и печатала «году — это
# мера». Русскую форму нельзя получить отсечением, её называют.
FACTS = [
    ("day", "hours", 24, "в сутках", "сутки",
     ("час", "часа", "часов")),
    ("hour", "minutes", 60, "в часе", "час",
     ("минута", "минуты", "минут")),
    ("minute", "seconds", 60, "в минуте", "минута",
     ("секунда", "секунды", "секунд")),
    ("week", "days", 7, "в неделе", "неделя",
     ("день", "дня", "дней")),
    ("year", "months", 12, "в году", "год",
     ("месяц", "месяца", "месяцев")),
    ("dollar", "cents", 100, "в долларе", "доллар",
     ("цент", "цента", "центов")),
    ("foot", "inches", 12, "в футе", "фут",
     ("дюйм", "дюйма", "дюймов")),
    ("kilometer", "meters", 1000, "в километре", "километр",
     ("метр", "метра", "метров")),
]
EN_PLURAL = {"day": "days", "hour": "hours", "minute": "minutes",
             "week": "weeks", "year": "years", "dollar": "dollars",
             "foot": "feet", "kilometer": "kilometers"}
BARE = [
    "the {one} is a unit.",
    "what is a {one}?",
    "{ru_bare} — это мера.",
]


def ru_form(forms, k):
    return forms[count_form_index(RU_PACK, RU_RULE, k)]


def pass_shows(pass_i):
    out = []
    for i, (one, many, ratio, ru_in, ru_nom, ru_forms) in enumerate(FACTS):
        out.append(f"1 {one} = {ratio} {many}.")
        out.append(f"a {one} has {ratio} {many}.")
        out.append(f"{ru_in} {ratio} {ru_form(ru_forms, ratio)}.")
        k = (pass_i * 3 + i) % 8 + 2          # 2..9
        out.append(f"{k} {EN_PLURAL[one]} = {k * ratio} {many}.")
        out.append(
            f"{k} {EN_PLURAL[one]} are {k * ratio} {many}."
        )
    for one, _, _, _, ru_nom, _ in FACTS:
        for tpl in BARE:
            out.append(tpl.format(one=one, ru_bare=ru_nom))
    return out


def main():
    emit("datasets/genesis_conversions.txt", pass_shows)


if __name__ == "__main__":
    main()
