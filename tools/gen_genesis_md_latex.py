#!/usr/bin/env python3
"""GENESIS layer: MARKDOWN and LaTeX as NOTATION WITH MEANING.

The largest world of the corpus (≈5.7k lines) had NO generator: it was
produced once by a script that lived outside the repository and was
never committed. A world that cannot be re-derived cannot be checked
for reproducibility, cannot get its vocabulary read by a court, and
freezes every defect it happens to contain. `markup_court` even reads
`gen_genesis_md_latex.py` for the layer's vocabulary — a file that did
not exist, so the whole world stood unjudged at 56%.

EVERY MARKUP LINE CARRIES ITS DECLARATION. A heading `### поле.` is
emitted together with `заголовок уровня три: поле.`; a table row with
the sentence naming its columns and values; a fence with the sentence
naming what the block holds. Neither line depends on the other's
POSITION — the pass shuffle separates them on purpose — but the layer
as a whole always contains both, and the court checks BOTH directions:
markup without a declaration is drift, a declaration without markup is
a lie.

ALL ARITHMETIC IS TRUE AND ALL OF IT IS COMPUTED HERE, never written
by hand: sums, differences, powers, exact roots, exact fractions and
index sums. A layer that states a number it did not compute teaches
the organism to trust a number nobody checked.
"""

import sys
import pathlib
from fractions import Fraction

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import lexicon  # noqa: E402
from layer import emit_grouped  # noqa: E402

# СИНОНИМ НАЗВАН, А НЕ ВЗЯТ МОЛЧА: слой зовёт гору «hill», и дом пар
# это ПРОВЕРЯЕТ — второй перевод, не объявленный там, оборвёт сборку.
СЛОВА = lexicon.набор(
    ["поле", "схема", "знание", "закон", "мера", "сила", "город",
     "гора", "время", "вода", "число", "форма", "материя", "звук",
     "точка", "свет", "слово", "линия", "мост", "круг", "лес"],
    {"гора": "hill", "материя": "matter"},
)
RU_LEVEL = ["один", "два", "три"]
EN_LEVEL = ["one", "two", "three"]
RU_COUNT = ["одного", "двух", "трёх"]
EN_COUNT = ["one", "two", "three"]
# буквы, объявленные знаковыми именами в пакетах языков
БУКВЫ = ["x", "y", "a", "b", "z"]


def заголовки(шаг):
    """Заголовок и объявление его уровня — обоими языками.

    УРОВЕНЬ ПРИНАДЛЕЖИТ СЛОВУ, А НЕ ПРОХОДУ. Плавая от прохода к
    проходу, слово вставало во всём слое сразу на три уровня — и
    вопрос «на каком уровне это слово стоит» терял ответ, а с ним и
    остроту: суду нечего было бы опровергать.
    """
    вон = []
    for i, (ру, ан) in enumerate(СЛОВА):
        ур = i % 3
        вон.append(("#" * (ур + 1) + f" {ру}.",
                    f"заголовок уровня {RU_LEVEL[ур]}: {ру}."))
        вон.append(("#" * (ур + 1) + f" {ан}.",
                    f"heading level {EN_LEVEL[ур]}: {ан}."))
    return вон


def списки(шаг):
    """Перечень и объявление его длины."""
    вон = []
    for i in range(len(СЛОВА)):
        ру = [СЛОВА[(i + k * 5 + шаг) % len(СЛОВА)][0] for k in range(2)]
        ан = [СЛОВА[(i + k * 5 + шаг) % len(СЛОВА)][1] for k in range(2)]
        вон.append(("\n".join(f"- {с}." for с in ру),
                    f"список из {RU_COUNT[1]} пунктов: "
                    f"{' и '.join(ру)}."))
        вон.append(("\n".join(f"{k + 1}. {с}." for k, с in enumerate(ан)),
                    f"numbered list of {EN_COUNT[1]} items: "
                    f"{' and '.join(ан)}."))
    return вон


def таблицы(шаг):
    """Строка таблицы и объявление её столбцов и значений."""
    вон = []
    for i in range(len(СЛОВА)):
        а, б = СЛОВА[(i + шаг) % len(СЛОВА)], СЛОВА[(i + 3 + шаг) % len(СЛОВА)]
        n, m = (i * 3 + шаг) % 9 + 1, (i * 5 + шаг) % 9 + 1
        вон.append((f"| {а[0]} | {б[0]} |\n| {n} | {m} |",
                    f"таблица: столбцы {а[0]} и {б[0]}; "
                    f"строка значений {n} и {m}."))
        вон.append((f"| {а[1]} | {б[1]} |\n| {n} | {m} |",
                    f"table: columns {а[1]} and {б[1]}; "
                    f"value row {n} and {m}."))
    return вон


def блоки(шаг):
    """Код-блок и объявление того, что он держит."""
    вон = []
    for i, (ру, ан) in enumerate(СЛОВА):
        n = (i * 7 + шаг) % 9 + 1
        вон.append((f"```\nlet {ан} = {n};\n```",
                    f"код-блок из одной строки: let {ан} = {n};"))
        вон.append((f"```\nlet {ан} = {n};\n```",
                    f"a code block of one line: let {ан} = {n};"))
    return вон


def стили(шаг):
    """Нажим, курсив, код — маркер, имя стиля и содержимое разом."""
    вон = []
    имена = (("**", "жирное", "bold"), ("*", "курсив", "italic"),
             ("`", "код", "code"))
    for i, (ру, ан) in enumerate(СЛОВА):
        м, ру_имя, ан_имя = имена[(i + шаг) % 3]
        вон.append((f"{м}{ру}{м} читается как {ру_имя} {ру}.",))
        вон.append((f"{м}{ан}{м} is read as {ан_имя} {ан}.",))
    return вон


def ссылки(шаг):
    """Ссылка и объявление её текста и цели."""
    вон = []
    for i, (_, ан) in enumerate(СЛОВА):
        цель = СЛОВА[(i + 4 + шаг) % len(СЛОВА)][1]
        адрес = f"https://example.org/{цель}"
        вон.append((f"[{ан}]({адрес})",
                    f"ссылка с текстом {ан} ведёт на {адрес}."))
    return вон


def формулы(шаг):
    """LaTeX-арифметика: всё вычислено, ни одно число не написано."""
    вон = []
    for i in range(len(СЛОВА)):
        a, b = (i * 2 + шаг) % 12 + 2, (i * 3 + шаг) % 9 + 1
        вон.append((f"$ {a} + {b} = {a + b} $.",
                    f"{a} плюс {b} равно {a + b}."))
        вон.append((f"$ {a} - {b} = {a - b} $.",
                    f"{a} minus {b} is {a - b}."))
        с = (i + шаг) % 3 + 2
        вон.append((f"$ {с}^{2} = {с ** 2} $.",
                    f"{с} в степени 2 равно {с ** 2}."))
        квадрат = ((i + шаг) % 8 + 2) ** 2
        вон.append((f"$ \\sqrt{{{квадрат}}} = {int(квадрат ** 0.5)} $.",
                    f"корень из {квадрат} равен {int(квадрат ** 0.5)}."))
        верх = (i + шаг) % 4 + 2
        сумма = верх * (верх + 1) // 2
        вон.append((f"$ \\sum_{{i=1}}^{{{верх}}} i = {сумма} $.",
                    f"сумма i от 1 до {верх} равно {сумма}."))
        ч, зн = (i + шаг) % 8 + 1, (i * 2 + шаг) % 8 + 2
        доля = Fraction(ч, зн)
        вон.append((f"$ \\frac{{{ч}}}{{{зн}}} $ читается как "
                    f"{ч} делить {зн}.",
                    f"$ \\frac{{{ч}}}{{{зн}}} = "
                    f"\\frac{{{доля.numerator}}}{{{доля.denominator}}} $."))
    return вон


def тождества(шаг):
    """Законы с буквами: переместительность и квадрат суммы."""
    вон = []
    for i in range(len(СЛОВА)):
        п, в = БУКВЫ[(i + шаг) % 5], БУКВЫ[(i + шаг + 2) % 5]
        вон.append((f"$ {п} + {в} = {в} + {п} $.",
                    f"$ {п} \\cdot {в} = {в} \\cdot {п} $."))
        вон.append((f"$ ({п} + {в})^2 = {п}^2 + 2 {п} {в} + {в}^2 $.",
                    f"$ {п} \\cdot ({в} + {п}) = "
                    f"{п} \\cdot {в} + {п} \\cdot {п} $."))
    return вон


def записи(шаг):
    """Имена знаков разметки и записи — из объявленных пакетов."""
    имена = (("#", "заголовок", "heading"),
             ("**", "жирно", "bold"),
             ("`", "код", "code"),
             ("|", "столбец таблицы", "table column"),
             ("^", "степень", "power"),
             ("_", "индекс", "index"),
             ("\\frac", "дробь", "fraction"))
    вон = []
    for знак, ру, ан in имена:
        вон.append((f"знак {знак} читается как {ру}.",
                    f"the sign {знак} is read as {ан}."))
    for б in БУКВЫ[:2]:
        имя = {"x": "икс", "y": "игрек"}[б]
        вон.append((f"буква {б} читается как {имя}.",))
    # ЧТЕНИЕ ЗАПИСИ ВСЛУХ — по той же грамматике, что объявлена в
    # пакетах и которой судит суд логики: слот произносится
    # объявленным именем буквы, а без объявления — как написан.
    ГОЛОС = {"x": "икс", "y": "игрек"}
    for i in range(len(СЛОВА)):
        а = БУКВЫ[(i + шаг) % 2]
        вон.append((f"$ {а} \\in A $ читается как "
                    f"{ГОЛОС[а]} принадлежит A.",
                    f"$ A \\subset B $ читается как A входит в B."))
    return вон


ГРУППЫ = (заголовки, списки, таблицы, блоки, стили, ссылки,
          формулы, тождества, записи)


def pass_groups(pass_i):
    """Каждая группа перемешивается отдельно — пары не рвутся."""
    группы = []
    for сделать in ГРУППЫ:
        показы = []
        for пара in сделать(pass_i):
            показы.extend(пара)
        группы.append(показы)
    return группы


def main():
    emit_grouped("datasets/genesis_md_latex.txt", pass_groups)


if __name__ == "__main__":
    main()
