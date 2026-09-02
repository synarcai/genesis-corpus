#!/usr/bin/env python3
"""GENESIS layer: HOW A MACHINE HOLDS A NUMBER.

    13 in binary is 1101.        13 in hex is d.
    13 and 6 is 4.               13 or 6 is 15.
    13 xor 6 is 11.              13 shifted left by 2 is 52.
    1101 in binary is 13 in decimal.
    a byte holds 8 bits and 256 values.

A programmer meets the same number in several dresses and must know
they are one number. Bases and bit operations are the most exactly
checkable knowledge there is — and the corpus had NOT ONE show of
either: no hex, no bitwise and/or/xor, no shifts.

WHAT IS SHOWN AND WHY EACH:
  · BASES two, eight and sixteen, in both directions — writing a
    number in a base and reading it back — because a base is a
    translation, and a translation shown one way teaches a table;
  · AND, OR, XOR as operations on the SAME pair, so their difference
    is met rather than described: the same 13 and 6 give 4, 15 and 11;
  · SHIFTS, with their arithmetic meaning stated beside them («shifted
    left by 2 is 52» beside «13 × 4 = 52»), because a shift that is
    not tied to multiplication is a trick instead of a fact;
  · WIDTH — what a byte holds — since every bound a programmer meets
    later stands on it.

NEGATIVE NUMBERS ARE ABSENT DELIBERATELY. Two's complement needs a
declared width, and the same bits mean different numbers at different
widths: shown without the width, it is not a fact but a coincidence.
It waits for a layer that declares width in every show.
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import json  # noqa: E402

from langpack import count_form_index  # noqa: E402
from layer import emit  # noqa: E402
from plural import by_count  # noqa: E402

RU_PACK = json.loads(
    (pathlib.Path(__file__).resolve().parent
     / "langpacks/ru.json").read_text(encoding="utf-8"))
RU_RULE = {"forms": ["one", "few", "many"],
           "count_agreement": RU_PACK["count_agreement"]}
# ПРАВИЛО ЧИСЛА ЧИТАЕТСЯ ИЗ ПАКЕТА, а не переписывается: «4 бит» ложно,
# «4 бита» верно, и знает это описание русского языка.
ФОРМЫ = {"бит": ("бит", "бита", "бит"),
         "значение": ("значение", "значения", "значений")}


def ру(слово, k):
    return ФОРМЫ[слово][count_form_index(RU_PACK, RU_RULE, k)]

ЧИСЛА = [13, 6, 25, 40, 7, 100, 31, 64, 18, 255, 12, 9, 200, 33, 17, 48]
ПАРЫ = [(13, 6), (12, 10), (7, 3), (25, 9), (60, 15), (14, 7),
        (31, 16), (100, 36), (9, 5), (21, 12), (63, 21), (40, 24)]
СДВИГИ = [(13, 2), (5, 3), (7, 1), (3, 4), (9, 2), (11, 3),
          (6, 2), (25, 1), (2, 5), (17, 2)]
ШИРИНЫ = [(4, "nibble"), (8, "byte"), (16, "halfword"), (32, "word")]

# ИСКОМОЕ ОБЪЯВЛЯЕТ СВОЙ ВОПРОС ОДИН РАЗ, и вопрос берёт ТУ ЖЕ фразу
# предмета, какую берёт ответ. Замер вопросной поверхности назвал этот
# мир немым: 1200 строк, вопросов ноль — он сообщал, что 5 в двоичной
# записи это 101, и ни разу не спрашивал, чему равно 5 в двоичной.
СПРОСИТЬ = {
    "value": "what is {предмет}?",
    "значение": "чему равно {предмет}?",
}


def спросить(искомое, предмет, ответ):
    """Вопрос о предмете и ответ о нём же — одной строкой."""
    return f"{СПРОСИТЬ[искомое].format(предмет=предмет)} {ответ}"


def pass_shows(pass_i):
    out = []
    for i in range(12):
        n = ЧИСЛА[(pass_i * 3 + i) % len(ЧИСЛА)]
        a, b = ПАРЫ[(pass_i + i) % len(ПАРЫ)]
        s, k = СДВИГИ[(pass_i * 5 + i) % len(СДВИГИ)]
        бит, имя = ШИРИНЫ[(pass_i + i) % len(ШИРИНЫ)]
        # --- основания, в обе стороны
        for основание, запись in (("binary", f"{n:b}"),
                                  ("octal", f"{n:o}"),
                                  ("hex", f"{n:x}")):
            пред = f"{n} in {основание}"
            утв = f"{пред} is {запись}."
            out.append(утв)
            out.append(спросить("value", пред, утв))
            обр = f"{запись} in {основание}"
            утв_обр = f"{обр} is {n} in decimal."
            out.append(утв_обр)
            # ВОПРОС БЕЗ ЧИСЛА НЕ СВЯЗАТЬ С ОТВЕТОМ, И ПОТОМУ ОН НЕ
            # ЗАДАЁТСЯ. Связь половин пары держится величинами (общий
            # дом `tools/asking.py`), а шестнадцатеричное «ff» цифр не
            # содержит вовсе: вопрос «что такое ff в шестнадцатеричной?»
            # не проверить ничем, и он был бы поверхностью лишь на вид.
            if any(з.isdigit() for з in запись):
                out.append(спросить("value", обр, утв_обр))
        for имя_ru, запись in (("двоичной", f"{n:b}"),
                               ("шестнадцатеричной", f"{n:x}")):
            пред = f"{n} в {имя_ru} записи"
            утв = f"{пред} это {запись}."
            out.append(утв)
            out.append(спросить("значение", пред, утв))
        # --- три операции на ОДНОЙ паре, чтобы различие встретилось
        for слово, значение in (("and", a & b), ("or", a | b),
                                ("xor", a ^ b)):
            пред = f"{a} {слово} {b}"
            утв = f"{пред} is {значение}."
            out.append(утв)
            out.append(спросить("value", пред, утв))
        for слово, значение in (("и", a & b), ("или", a | b)):
            пред = f"{a} {слово} {b} побитово"
            утв = f"{пред} это {значение}."
            out.append(утв)
            out.append(спросить("значение", пред, утв))
        # --- сдвиг, всегда рядом со своим умножением
        сдв_л = f"{s} shifted left by {k}"
        сдв_п = f"{s << k} shifted right by {k}"
        сдв_ru = f"{s} сдвинутое влево на {k}"
        out.append(f"{сдв_л} is {s << k}.")
        out.append(спросить("value", сдв_л, f"{сдв_л} is {s << k}."))
        out.append(f"{s} × {2 ** k} = {s << k}.")
        out.append(f"{сдв_п} is {s}.")
        out.append(спросить("value", сдв_п, f"{сдв_п} is {s}."))
        out.append(f"{сдв_ru} это {s << k}.")
        out.append(спросить("значение", сдв_ru, f"{сдв_ru} это {s << k}."))
        # --- ширина
        out.append(f"a {имя} holds {бит} {by_count(бит, 'bits')} and "
                   f"{2 ** бит} values.")
        out.append(f"with {бит} bits you can write {2 ** бит} "
                   f"{by_count(2 ** бит, 'numbers')}.")
        out.append(f"{имя} держит {бит} {ру('бит', бит)} и "
                   f"{2 ** бит} {ру('значение', 2 ** бит)}.")
    # ОТКАЗ С ОСНОВАНИЕМ: цифры от двух до девяти в двоичной записи не
    # живут. Вопрос «какое число записано цифрой 7 в двоичной?» имеет
    # честный ответ «никакое, и вот почему» — основание вычислимо и
    # судимо тем же перебором цифр.
    for цифра in range(2, 10):
        out.append(f"what number is written {цифра} in binary? none: "
                   f"the digit {цифра} does not occur in binary.")
        out.append(f"какое число записано цифрой {цифра} в двоичной? "
                   f"такого нет: цифра {цифра} в двоичной записи не "
                   f"встречается.")
    return out


def main():
    emit("datasets/genesis_machine.txt", pass_shows)


if __name__ == "__main__":
    main()
