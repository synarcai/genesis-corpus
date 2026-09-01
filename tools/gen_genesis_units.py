#!/usr/bin/env python3
"""GENESIS layer: QUANTITIES, UNITS, FRACTIONS (М-4 of
the GSM8K collegium).

What GSM8K needs and the corpus lacks: unit conversions
as facts plus applied mass, fractions ("half of"),
division with remainder, money-rate shows. School shape
laws: bare shows, three surfaces (glyph / RU / EN),
deterministic coprime shuffles, form-feed seams.
"""

import units
from layer import emit_grouped


# ПОРЯДОК СВОЙ, ОТНОШЕНИЯ ОБЩИЕ. Здесь жила ВТОРАЯ
# таблица переводов (два факта повторяли соседний
# слой) и ТРЕТЬЯ копия русского согласования — та
# самая, от которой сосед прямо предостерегал в
# своей же шапке. Слой называет, ЧТО показывает и
# КАКИМ письмом; отношения и формы читаются из
# `tools/units.py`. Русские падежные формы нужны
# по-прежнему: организм живёт точными формами, и
# бесподежный показ не отвечает прожитому вопросу
# («2 часа равно», не «2 час равно»).
ПОРЯДОК = ("hour", "minute", "metre", "kilometre",
           "kilogram", "week", "dozen")
ПИСЬМО = "amer"


def conversions():
    """(формы ру, ед. англ, мн. англ, ру мн. части,
    англ мн. части, во сколько раз)."""
    for имя in ПОРЯДОК:
        часть = next(б for (а, б) in units.РЁБРА
                     if а == имя)
        yield (units.ФОРМЫ_ВСЕХ[имя][1],
               units.англ(имя, False, ПИСЬМО),
               units.англ(имя, True, ПИСЬМО),
               units.рус(часть, 5),
               units.англ(часть, True, ПИСЬМО),
               int(units.отношение(имя, часть)))


RU_NUM = ["ноль", "один", "два", "три", "четыре",
          "пять", "шесть", "семь", "восемь",
          "девять", "десять"]
EN_NUM = ["zero", "one", "two", "three", "four",
          "five", "six", "seven", "eight", "nine",
          "ten"]


def conversion_shows():
    out = []
    for (ruf, en, enp, rus, ens, f) in conversions():
        out.append(
            f"один {ruf[0]} равно {f} {rus}."
        )
        out.append(f"one {en} equals {f} {ens}.")
        for k in (2, 3, 5):
            out.append(
                f"{k} {units.ру_форма(ruf, k)} равно "
                f"{k * f} {rus}."
            )
            out.append(
                f"{k} {enp} equal {k * f} {ens}."
            )
    return out


def fraction_shows():
    out = []
    for n in range(2, 11):
        d = 2 * n
        out.append(
            f"половина от {d} равно {n}."
        )
        out.append(f"half of {d} equals {n}.")
        out.append(f"{d} ÷ 2 = {n}.")
    for n in range(1, 7):
        d = 3 * n
        out.append(f"треть от {d} равно {n}.")
        out.append(
            f"a third of {d} equals {n}."
        )
        out.append(f"{d} ÷ 3 = {n}.")
    for n in range(1, 6):
        d = 4 * n
        out.append(
            f"четверть от {d} равно {n}."
        )
        out.append(
            f"a quarter of {d} equals {n}."
        )
        out.append(f"{d} ÷ 4 = {n}.")
    return out


def remainder_shows():
    out = []
    for a in range(5, 20):
        for b in (2, 3, 4):
            q, r = divmod(a, b)
            if r == 0:
                continue
            out.append(
                f"{a} делить {b} равно {q} "
                f"остаток {r}."
            )
            out.append(
                f"{a} divided by {b} equals {q} "
                f"remainder {r}."
            )
    return out


def rate_shows():
    out = []
    # ФОРМЫ РУБЛЯ ЧИТАЮТСЯ ИЗ ДОМА ЕДИНИЦ, а не пишутся здесь
    # вторым списком: рубль объявлен там вместе с копейкой.
    rub = units.ФОРМЫ_ВСЕХ["rouble"][1]
    for k in range(2, 7):
        for p in (2, 3, 5):
            out.append(
                f"{k} по {p} {units.ру_форма(rub, p)} "
                f"равно {k * p} "
                f"{units.ру_форма(rub, k * p)}."
            )
            out.append(
                f"{k} items at {p} dollars "
                f"equal {k * p} dollars."
            )
    return out


def main():
    kinds = [
        conversion_shows(), fraction_shows(),
        remainder_shows(), rate_shows(),
    ]
    emit_grouped("datasets/genesis_units.txt", lambda _pi: kinds)


if __name__ == "__main__":
    main()
