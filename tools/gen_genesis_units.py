#!/usr/bin/env python3
"""GENESIS layer: QUANTITIES, UNITS, FRACTIONS (М-4 of
the GSM8K collegium).

What GSM8K needs and the corpus lacks: unit conversions
as facts plus applied mass, fractions ("half of"),
division with remainder, money-rate shows. School shape
laws: bare shows, three surfaces (glyph / RU / EN),
deterministic coprime shuffles, form-feed seams.
"""

from layer import emit_grouped


# RU units carry their case forms: (one, few 2-4,
# many 5+) — the organism lives on exact word
# forms, a caseless show never matches a lived
# question («2 часа равно», not «2 час равно»).
CONVERSIONS = [
    # ((ru_one, ru_few, ru_many), en, en_pl,
    #  ru_sub_many, en_sub, factor)
    (("час", "часа", "часов"), "hour", "hours",
     "минут", "minutes", 60),
    (("минута", "минуты", "минут"), "minute",
     "minutes", "секунд", "seconds", 60),
    (("метр", "метра", "метров"), "meter",
     "meters", "сантиметров", "centimeters",
     100),
    (("километр", "километра", "километров"),
     "kilometer", "kilometers", "метров",
     "meters", 1000),
    (("килограмм", "килограмма",
      "килограммов"), "kilogram", "kilograms",
     "граммов", "grams", 1000),
    (("неделя", "недели", "недель"), "week",
     "weeks", "дней", "days", 7),
    (("дюжина", "дюжины", "дюжин"), "dozen",
     "dozens", "штук", "items", 12),
]


def ru_form(forms, k):
    one, few, many = forms
    if k % 10 == 1 and k % 100 != 11:
        return one
    if k % 10 in (2, 3, 4) and k % 100 not in (
        12, 13, 14,
    ):
        return few
    return many

RU_NUM = ["ноль", "один", "два", "три", "четыре",
          "пять", "шесть", "семь", "восемь",
          "девять", "десять"]
EN_NUM = ["zero", "one", "two", "three", "four",
          "five", "six", "seven", "eight", "nine",
          "ten"]


def conversion_shows():
    out = []
    for (ruf, en, enp, rus, ens, f) in CONVERSIONS:
        out.append(
            f"один {ruf[0]} равно {f} {rus}."
        )
        out.append(f"one {en} equals {f} {ens}.")
        for k in (2, 3, 5):
            out.append(
                f"{k} {ru_form(ruf, k)} равно "
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
    rub = ("рубль", "рубля", "рублей")
    for k in range(2, 7):
        for p in (2, 3, 5):
            out.append(
                f"{k} по {p} {ru_form(rub, p)} "
                f"равно {k * p} "
                f"{ru_form(rub, k * p)}."
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
