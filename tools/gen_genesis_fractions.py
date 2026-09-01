#!/usr/bin/env python3
"""GENESIS layer: PARTS OF A WHOLE (half / third / quarter / three quarters).

Built to holon's requested shape, three lines per show:

    6 ÷ 2 = 3.
    half of six is three.
    половина шести — три.

THE GLYPH AXIS IS THE WELD: the road buys the division from it, and
the two prose surfaces are welded to the same fact. The surfaces stand
on SEPARATE LINES, not one: a line carrying two scripts is a splice,
and the language census counts it as such — the information is the
same, the splice is not.

EVERY DIVISION SHOWN IS EXACT, and the assertion in this file says so
before a byte is written. The langpack shipped 40 division shows of
which 40 were false, because the machinery had no product to write
them over; here the bases are DERIVED from the divisor (multiples
only), so an inexact claim cannot be built at all.

THE FRACTION WORD LIVES WHERE NO DIGIT STANDS, by the law that proved
itself on the rates layer the same day: without number-free life a
word is known only as «what stands beside a number», and the parasite
«books per away» died exactly by that law in holon's court.
"""

from layer import emit


# (english word, russian word, divisor, numerator)
PARTS = [
    ("half", "половина", 2, 1),
    ("a third", "треть", 3, 1),
    ("a quarter", "четверть", 4, 1),
    ("three quarters", "три четверти", 4, 3),
]
EN = {1: "one", 2: "two", 3: "three", 4: "four", 5: "five",
      6: "six", 7: "seven", 8: "eight", 9: "nine", 10: "ten",
      11: "eleven", 12: "twelve", 13: "thirteen", 14: "fourteen",
      15: "fifteen", 16: "sixteen", 17: "seventeen",
      18: "eighteen", 19: "nineteen", 20: "twenty"}
RU_NOM = {1: "один", 2: "два", 3: "три", 4: "четыре", 5: "пять",
          6: "шесть", 7: "семь", 8: "восемь", 9: "девять",
          10: "десять", 11: "одиннадцать", 12: "двенадцать",
          13: "тринадцать", 14: "четырнадцать", 15: "пятнадцать",
          16: "шестнадцать", 17: "семнадцать", 18: "восемнадцать",
          19: "девятнадцать", 20: "двадцать"}
# THE WHOLE STANDS IN THE GENITIVE: «половина шести», not «половина
# шесть». Russian cannot say a part of a thing in any other case, and
# a guessed form would be a lie shown twice.
RU_GEN = {2: "двух", 3: "трёх", 4: "четырёх", 5: "пяти",
          6: "шести", 7: "семи", 8: "восьми", 9: "девяти",
          10: "десяти", 11: "одиннадцати", 12: "двенадцати",
          13: "тринадцати", 14: "четырнадцати", 15: "пятнадцати",
          16: "шестнадцати", 17: "семнадцати", 18: "восемнадцати",
          19: "девятнадцати", 20: "двадцати"}
BARE = [
    "{en} is a part of a whole.",
    "what is {en}?",
    "{ru} — это часть целого.",
    "что такое {ru}?",
]
LIMIT = 20


def pass_shows(pass_i):
    out = []
    for en, ru, div, num in PARTS:
        wholes = [w for w in range(div, LIMIT + 1) if w % div == 0]
        # the pass rotates which wholes are shown, so five passes
        # cover the range without repeating one show five times
        for j, whole in enumerate(wholes):
            if (j + pass_i) % 2:
                continue
            part = whole * num // div
            assert whole * num % div == 0, (whole, num, div)
            assert part in EN and whole in RU_GEN, (part, whole)
            if num == 1:
                out.append(f"{whole} ÷ {div} = {part}.")
            else:
                out.append(f"{whole} ÷ {div} × {num} = {part}.")
            out.append(f"{en} of {EN[whole]} is {EN[part]}.")
            out.append(f"{ru} {RU_GEN[whole]} — {RU_NOM[part]}.")
    for en, ru, _, _ in PARTS:
        for tpl in BARE:
            out.append(tpl.format(en=en, ru=ru))
    return out


def main():
    emit("datasets/genesis_fractions.txt", pass_shows)


if __name__ == "__main__":
    main()
