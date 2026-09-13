#!/usr/bin/env python3
"""GENESIS layer: SEQUENCES — progression, limit, rate of change.

Three subjects the syllabus court named absent: progression, limit, and
derivative. They are one family: a sequence with a law, what it tends
to, and how fast it changes. Without them the corpus knows numbers but
not PROCESSES, and every science is about processes.

EXACTNESS IS KEPT BY CHOICE OF EXAMPLE, NOT BY ROUNDING. The limit is
shown on sequences whose terms are exact fractions and whose limit is
an integer; the derivative on polynomials where the difference
quotient is exact. A corpus that says «approximately» teaches
approximation, and the arithmetic court would rightly call it false.

ВОПРОС ВЫВОДИТСЯ ИЗ ТОЙ ЖЕ ФРАЗЫ ПРЕДМЕТА, ЧТО И ОТВЕТ. Замер вопросной
поверхности назвал этот мир немым: 1840 строк, вопросов ноль. Предмет —
«арифметическая прогрессия от 5 с шагом 3», «последовательность 1/2 1/4
1/8» — строится ОДИН раз и подставляется и в утверждение, и в вопрос.
Две записи предмета разошлись бы в первой же строке, и суд, читающий
только ответ, назвал бы расхождение истиной.

ОТКАЗ С ОСНОВАНИЕМ: «чему равен предел последовательности 2 4 8 16?» —
предела нет, и основание вычислимо: члены РАСТУТ. Мир, умеющий только
утверждать, учит соглашаться; мир, умеющий отказать по основанию,
учит различать.
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import seriesforms as F  # noqa: E402
from layer import emit_grouped  # noqa: E402

# ЦЕЛЬ ОБЪЯВЛЯЕТСЯ СТРОКОЙ, А НЕ ВПИСЫВАЕТСЯ В ВЫЗОВ: указатель родов ищет МИР ДОМА по этой
# самой строке и по ввозу кузницы.
ЦЕЛЬ = "datasets/genesis_sequences.txt"


def main():
    emit_grouped(ЦЕЛЬ, F.группы)


if __name__ == "__main__":
    main()
