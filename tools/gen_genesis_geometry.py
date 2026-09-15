#!/usr/bin/env python3
"""GENESIS layer: GEOMETRY — measure of a figure, derived not measured.

The syllabus court named area, volume and the Pythagorean theorem
absent. A corpus that knows units but not FIGURES knows how to say a
length and not how to earn one: the area of a rectangle is not
measured, it is DERIVED from two lengths, and that derivation is the
first place where multiplication means something other than repeated
counting.

PYTHAGORAS IS SHOWN ON EXACT TRIPLES ONLY. A hypotenuse of √2 is true
and unwritable here: the corpus states what it can check, and an
approximation named as an equality would be a lie of the same kind as
«5 ÷ 2 = 2».

ВОПРОС ВЫВОДИТСЯ ИЗ ТОЙ ЖЕ ФРАЗЫ ПРЕДМЕТА, ЧТО И ОТВЕТ. Мир, только
сообщающий, учит УЗНАВАТЬ утверждение, а не ОТВЕЧАТЬ на вопрос: замер
вопросной поверхности назвал геометрию немой — 1120 строк, вопросов
ноль. Предмет («прямоугольник 4 на 5») строится ОДИН раз и подставляется
и в утверждение, и в вопрос; вторая запись предмета разошлась бы с
первой в первой же строке, и суд, читающий только ответ, назвал бы это
истиной (так и вышло в языке формул: «how is |16| said in words? |15|
in words is …»).

ОТКАЗ С ОСНОВАНИЕМ — ТОТ ЖЕ РОД, ЧТО И ОТВЕТ. «Чему равна гипотенуза
при катетах 2 и 3?» имеет честный ответ «целого нет, и вот почему»:
2² + 3² = 13, а 13 не полный квадрат. Отказ здесь ВЫЧИСЛЕН, а не
объявлен, и потому судим тем же ходом, что и утверждение.
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import geomforms as F  # noqa: E402
from layer import emit_grouped  # noqa: E402

# ЦЕЛЬ ОБЪЯВЛЯЕТСЯ СТРОКОЙ, А НЕ ВПИСЫВАЕТСЯ В ВЫЗОВ: указатель родов ищет
# МИР ДОМА по этой самой строке и по ввозу кузницы. Путь, отданный литералом
# внутрь `emit_grouped`, оставляет дом БЕЗ МИРА, и указатель честно пишет None.
#
#     ВВОЗ ЕСТЬ СВЯЗЬ, НО НАЙТИ ЕЁ УКАЗАТЕЛЬ МОЖЕТ ЛИШЬ ТАМ, ГДЕ ОБЪЯВЛЕНА ЦЕЛЬ.
ЦЕЛЬ = "datasets/genesis_geometry.txt"

# ПЕРЕБОР ЖИВЁТ В ДОМЕ (13.09). Ступень законов, стоявшая ПОДЛЕ кортежа, объявлена там
# отдельным родом, а не потеряна.


def main():
    emit_grouped(ЦЕЛЬ, F.группы_страниц)


if __name__ == "__main__":
    main()
