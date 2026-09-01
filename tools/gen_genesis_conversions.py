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

_НЕМОЕ_H = ("hour", "honest", "heir")


def артикль(слово):
    """«a» или «an» — по звуку, с которого слово начинается."""
    if слово[0] in "aeiou" or слово.startswith(_НЕМОЕ_H):
        return "an"
    return "a"


from layer import emit


import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import units  # noqa: E402

# ПОРЯДОК СВОЙ, ОТНОШЕНИЯ ОБЩИЕ. Восемь фактов жили здесь, семь — в
# слое единиц, пять приставочных — в слое физики; три дома одного
# знания расходятся в день, когда тронут любой из них. Слой называет,
# ЧТО показывает и КАКИМ письмом; отношения, формы и предложный падеж
# читаются из `tools/units.py` — оттуда же их берёт суд единиц.
# ИМЕНИТЕЛЬНЫЙ ОБЪЯВЛЕН ОТДЕЛЬНО, а не отрезан от предложного: первая
# редакция брала второе слово из «в году» и печатала «году — это
# мера». Русскую форму нельзя получить отсечением, её называют.
ПОРЯДОК = ("day", "hour", "minute", "week", "year", "dollar",
           "foot", "kilometre")
ПИСЬМО = "amer"

FACTS = []
EN_PLURAL = {}
for _имя in ПОРЯДОК:
    _часть = next(б for (а, б) in units.РЁБРА if а == _имя)
    _ru_in, _ru_nom = units.В_ЧЁМ[_имя]
    _ед = units.англ(_имя, False, ПИСЬМО)
    FACTS.append((_ед, units.англ(_часть, True, ПИСЬМО),
                  int(units.отношение(_имя, _часть)),
                  _ru_in, _ru_nom, units.ФОРМЫ_ВСЕХ[_часть][1]))
    EN_PLURAL[_ед] = units.англ(_имя, True, ПИСЬМО)

BARE = [
    "the {one} is a unit.",
    "what is a {one}?",
    "{ru_bare} — это мера.",
]


def ru_form(forms, k):
    return units.ру_форма(forms, k)


def pass_shows(pass_i):
    out = []
    for i, (one, many, ratio, ru_in, ru_nom, ru_forms) in enumerate(FACTS):
        out.append(f"1 {one} = {ratio} {many}.")
        # АРТИКЛЬ ИДЁТ ЗА ЗВУКОМ: «an hour», не «a hour». Слой учил
        # этому пять строк подряд, и поймал его НОВЫЙ суд ставок —
        # старый мир вычищен задним числом, как и «жирное свет».
        out.append(f"{артикль(one)} {one} has {ratio} {many}.")
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
