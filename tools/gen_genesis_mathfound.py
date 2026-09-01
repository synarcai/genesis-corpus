#!/usr/bin/env python3
"""GENESIS layer: FOUNDATIONS OF MATHEMATICS — and the named case.

Five subjects of mathematics and one of language stood absent or thin.

  · A FUNCTION is a correspondence taken as ONE OBJECT — the first time
    a rule becomes a thing that can itself be argued about;
  · INJECTION and BIJECTION are the two questions one asks of any
    correspondence, and their difference is shown by a WITNESS, not by
    a definition: one pair of inputs with the same output kills
    injectivity and kills nothing else;
  · CARDINALITY is the discovery that infinities are comparable: the
    even numbers are as many as the naturals because n ↔ 2n pairs them
    off, and that pairing is exhibited, not asserted;
  · PROOF BY CONTRADICTION is the shape of argument that assumes what
    it denies. It is shown with every step computable;
  · THE NAMED CASE closes a gap the corpus carried from the start: it
    showed case forms IN USE («после понедельника», «в часе») and NEVER
    NAMED THEM. To show a form without its name is to leave the reader
    without the word by which the knowledge is found anywhere else.
"""

import sys
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import rugram  # noqa: E402
import units  # noqa: E402
from layer import emit_grouped  # noqa: E402


def функции(шаг):
    """Соответствие как ОДИН предмет, применённое к точке."""
    вон = []
    for i in range(16):
        k = 2 + (i + шаг) % 4
        область = [1 + (i % 3), 2 + (i % 3), 3 + (i % 3)]
        точка = область[(i + шаг) % 3]
        если = " ".join(str(x) for x in область)
        вон.append(f"функция f на множестве {{{если}}} задана правилом "
                   f"f(x) = {k}x; f({точка}) = {k * точка}.")
        вон.append(f"the function f on the set {{{если}}} is given by "
                   f"f(x) = {k}x; f({точка}) = {k * точка}.")
    return вон


def соответствия(шаг):
    """Инъекция и её опровержение ОДНИМ свидетелем."""
    вон = []
    for i in range(10):
        k = 2 + (i + шаг) % 3
        область = [1 + (i % 4), 2 + (i % 4), 3 + (i % 4)]
        если = " ".join(str(x) for x in область)
        вон.append(f"функция f(x) = {k}x на множестве {{{если}}} "
                   f"инъективна: разные входы дают разные выходы.")
        вон.append(f"the function f(x) = {k}x on {{{если}}} is "
                   f"injective: different inputs give different outputs.")
        a, b = 1 + (i % 4), 3 + (i % 4)
        вон.append(f"функция f(x) = x mod 2 на множестве "
                   f"{{{a} {a + 1} {b} {b + 1}}} не инъективна: "
                   f"f({a}) = f({b}).")
        вон.append(f"the function f(x) = x mod 2 on "
                   f"{{{a} {a + 1} {b} {b + 1}}} is not injective: "
                   f"f({a}) = f({b}).")
    return вон


def мощность(шаг):
    """Мощность конечного и счётность бесконечного."""
    вон = []
    буквы = "a b c d e f g h".split()
    for n in range(1, 9):
        если = " ".join(буквы[:n])
        вон.append(f"мощность множества {{{если}}} равна {n}.")
        вон.append(f"the cardinality of the set {{{если}}} is {n}.")
    for i in range(6):
        n = 1 + i
        вон.append(f"чётные числа счётны: {n} отвечает {2 * n}, "
                   f"и это биекция с натуральными.")
        вон.append(f"the even numbers are countable: {n} maps to "
                   f"{2 * n}, and this is a bijection with the naturals.")
    return вон


def от_противного(шаг):
    """Допущение, ведущее к противоречию, — с вычислимым шагом."""
    вон = []
    for i in range(10):
        n = 3 + 2 * ((i + шаг) % 6)
        k, r = divmod(n, 2)
        вон.append(f"допустим, {n} чётно. тогда {n} = 2k для целого k. "
                   f"но {n} = 2 × {k} + {r}. противоречие: {n} нечётно.")
        вон.append(f"suppose {n} is even. then {n} = 2k for a whole k. "
                   f"but {n} = 2 × {k} + {r}. contradiction: "
                   f"{n} is odd.")
    return вон


def индукция(шаг):
    """Основание, шаг и покрытая ими цепь."""
    вон = []
    for i in range(6):
        верх = 3 + i
        сумма = верх * (верх + 1) // 2
        вон.append(f"индукция: основание n = 1 верно, шаг от n к n+1 "
                   f"верен, значит верно до n = {верх}; сумма первых "
                   f"{верх} чисел равна {сумма}.")
        вон.append(f"induction: the base n = 1 holds, the step from n "
                   f"to n+1 holds, hence it holds up to n = {верх}; the "
                   f"sum of the first {верх} numbers is {сумма}.")
    return вон


# ЧИСЛОВАЯ РАМКА ЕСТЬ СЕСТРА ПАДЕЖНОЙ, И РАМКА ОДНА С ПАРАМЕТРОМ, А
# НЕ ДВЕ. У английского нет падежа, но есть ЧИСЛО; у русского есть
# оба. Разница языков — в ПОРЯДКЕ СЛОВ шаблона (у английского имя
# формы стоит первым, у русского третьим), и это свойство ЯЗЫКА,
# объявленное шаблоном, а не повод завести вторую рамку.
ЧИСЛОВАЯ_РАМКА = {
    "en": ("the plural of {один} is {много}.",
           "the singular of {много} is {один}."),
    "ru": ("множественное число слова {один} — {много}.",
           "единственное число слова {много} — {один}."),
}


def числа(шаг):
    """Единственное и множественное, названные, а не только показанные.

    Форма выводится ПРАВИЛОМ письма и сверяется с объявленной парой:
    единица, чьё множественное правилу не подчиняется и в исключениях
    не названа, в показ НЕ ВЫХОДИТ — честное молчание вместо
    правдоподобной формы.
    """
    вон = []
    имена = sorted(units.ФОРМЫ_ВСЕХ)
    for i, имя in enumerate(имена):
        try:
            один, много = units.англ(имя), units.англ(имя, True)
        except (KeyError, IndexError):
            continue
        if units.мн_правилом(один) != много:
            continue
        мн_шаб, ед_шаб = ЧИСЛОВАЯ_РАМКА["en"]
        вон.append(мн_шаб.format(один=один, много=много))
        вон.append(ед_шаб.format(один=один, много=много))
        if (шаг + i) % 3 == 0:
            вон.append(f"what is the plural of {один}? the plural of "
                       f"{один} is {много}.")
            вон.append(f"what is the singular of {много}? the singular "
                       f"of {много} is {один}.")
    for один, много in sorted(units.МН_ИСКЛЮЧЕНИЯ.items()):
        вон.append(f"the plural of {один} is {много}, not "
                   f"{один + 's'}: it does not follow the rule.")
    return вон


def падежи(шаг):
    """Падеж НАЗВАН, а не только показан в работе."""
    вон = []
    for слово, формы in rugram.ПАРАДИГМЫ.items():
        for падеж_в, форма in zip(rugram.ПАДЕЖИ_В, формы):
            вон.append(f"слово {слово} в {падеж_в} падеже — {форма}.")
    # ИМЯ РЯДА СКАЗАНО ОДИН РАЗ ЗА ПРОХОД, А НЕ ПРИ КАЖДОМ СЛОВЕ:
    # парадигм стало двадцать девять, и повтор одной строки двадцать
    # девять раз есть мёртвая поверхность — сердце выучивает её
    # наизусть, и цена чтения исчезает.
    вон.append(f"падежей шесть: {', '.join(rugram.ПАДЕЖИ)}.")
    return вон


ГРУППЫ = (функции, соответствия, мощность, от_противного, индукция,
          падежи, числа)


def pass_groups(pass_i):
    return [сделать(pass_i) for сделать in ГРУППЫ]


def main():
    emit_grouped("datasets/genesis_mathfound.txt", pass_groups)


if __name__ == "__main__":
    main()
