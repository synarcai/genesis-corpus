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

import sys
import pathlib
from fractions import Fraction

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from layer import emit_grouped  # noqa: E402

ДЛИНА = 4

# ИСКОМОЕ ОБЪЯВЛЯЕТ СВОЙ ВОПРОС ОДИН РАЗ, и вопрос берёт ту же фразу
# предмета, какую берёт ответ. Русская связка идёт за родом искомого
# («чему равнА сумма», «чему равЕН предел»), и потому вопрос объявлен
# при искомом, а не при предмете.
СПРОСИТЬ = {
    "gives": "what does {предмет} give?",
    "term": "what is {предмет}?",
    "sum": "what is the sum of {предмет}?",
    "limit": "what is the limit of {предмет}?",
    "series": "what is the sum of the whole series {предмет} ...?",
    "change": ("for f(t) = t^{степень}, what is the change "
               "from {a} to {b}?"),
    "derivative": "what is {предмет}?",
    "даёт": "что даёт {предмет}?",
    "член": "чему равен {предмет}?",
    "сумма": "чему равна сумма {предмет}?",
    "предел": "чему равен предел последовательности {предмет}?",
    "ряд": "чему равна сумма всего ряда {предмет} ...?",
    "изменение": ("для f(t) = t^{степень}, чему равно изменение "
                  "от {a} до {b}?"),
    "производная": "чему равна {предмет}?",
}


def спросить(искомое, ответ, **части):
    """Вопрос об искомом и ответ о нём же — одной строкой.

    Части вопроса приходят теми же переменными, из которых собран
    ответ: у вопроса и ответа один источник, и разойтись им негде.
    """
    return f"{СПРОСИТЬ[искомое].format(**части)} {ответ}"


def арифметические(шаг):
    """Прогрессия названа началом и шагом; члены выведены."""
    вон = []
    for i in range(24):
        a, d = 2 + i + шаг, 2 + (i % 5)
        члены = [a + k * d for k in range(ДЛИНА)]
        если = " ".join(str(x) for x in члены)
        n = ДЛИНА + 1
        en = f"the arithmetic progression from {a} with step {d}"
        ru = f"арифметическая прогрессия от {a} с шагом {d}"
        утв_en, утв_ru = f"{en} gives {если}.", f"{ru} даёт {если}."
        вон.append(утв_en)
        вон.append(утв_ru)
        вон.append(спросить("gives", утв_en, предмет=en))
        вон.append(спросить("даёт", утв_ru, предмет=ru))
        # ПОКАЗ САМОДОСТАТОЧЕН: «её член номер 5» без своей прогрессии
        # не значит ничего, а перестановка проходов разводит соседей.
        чл_en = (f"term number {n} of the progression from {a} "
                 f"with step {d}")
        чл_ru = f"член номер {n} прогрессии от {a} с шагом {d}"
        утв_чл_en = f"{чл_en} is {a + (n - 1) * d}."
        утв_чл_ru = f"{чл_ru} равен {a + (n - 1) * d}."
        вон.append(утв_чл_en)
        вон.append(утв_чл_ru)
        вон.append(спросить("term", утв_чл_en, предмет=чл_en))
        вон.append(спросить("член", утв_чл_ru, предмет=чл_ru))
        утв_с_en = f"the sum of {если} is {sum(члены)}."
        утв_с_ru = f"сумма {если} равна {sum(члены)}."
        вон.append(утв_с_en)
        вон.append(утв_с_ru)
        вон.append(спросить("sum", утв_с_en, предмет=если))
        вон.append(спросить("сумма", утв_с_ru, предмет=если))
    return вон


def геометрические(шаг):
    """Отношение вместо разности — тот же закон, другое действие."""
    вон = []
    for i in range(20):
        a, q = 1 + (i % 5) + шаг, 2 + (i % 3)
        члены = [a * q ** k for k in range(ДЛИНА)]
        если = " ".join(str(x) for x in члены)
        en = f"the geometric progression from {a} with ratio {q}"
        ru = f"геометрическая прогрессия от {a} со знаменателем {q}"
        утв_en, утв_ru = f"{en} gives {если}.", f"{ru} даёт {если}."
        вон.append(утв_en)
        вон.append(утв_ru)
        вон.append(спросить("gives", утв_en, предмет=en))
        вон.append(спросить("даёт", утв_ru, предмет=ru))
    return вон


def пределы(шаг):
    """Бесконечный процесс с конечным итогом — на точных дробях."""
    вон = []
    for i in range(16):
        q = 2 + (i % 4)
        члены = [Fraction(1, q ** k) for k in range(1, ДЛИНА + 1)]
        если = " ".join(f"{x.numerator}/{x.denominator}" for x in члены)
        утв_п_en = f"the sequence {если} has limit 0."
        утв_п_ru = f"последовательность {если} имеет предел 0."
        вон.append(утв_п_en)
        вон.append(утв_п_ru)
        вон.append(спросить("limit", утв_п_en, предмет=f"the sequence {если}"))
        вон.append(спросить("предел", утв_п_ru, предмет=если))
        # сумма геометрического ряда: a/(1-q) при a = 1/q
        сумма = Fraction(1, q - 1)
        утв_р_en = (f"the sum of the whole series {если} ... is "
                    f"{сумма.numerator}/{сумма.denominator}.")
        утв_р_ru = (f"сумма всего ряда {если} ... равна "
                    f"{сумма.numerator}/{сумма.denominator}.")
        вон.append(утв_р_en)
        вон.append(утв_р_ru)
        вон.append(спросить("series", утв_р_en, предмет=если))
        вон.append(спросить("ряд", утв_р_ru, предмет=если))
    return вон


def отказ_предела(шаг):
    """Вопрос, чей честный ответ — «предела нет, и вот почему».

    ПРЕДЕЛ ЕСТЬ УТВЕРЖДЕНИЕ О ПОВЕДЕНИИ, А НЕ ИМЯ ПОСЛЕДНЕГО ЧЛЕНА.
    Растущая последовательность предела не имеет, и отказ называет
    основание тем же, чем суд его проверит: члены РАСТУТ. Мир,
    умеющий только утверждать, учит соглашаться.
    """
    вон = []
    for i in range(12):
        a, q = 2 + (шаг + i) % 7, 2 + (i % 3)
        члены = [a * q ** k for k in range(ДЛИНА)]
        если = " ".join(str(x) for x in члены)
        вон.append(f"what is the limit of the sequence {если}? no "
                   f"limit for {если}: the terms grow, they do not "
                   f"shrink.")
        вон.append(f"чему равен предел последовательности {если}? "
                   f"предела нет у {если}: члены растут, а не убывают.")
    return вон


def производные(шаг):
    """Скорость изменения — разностным отношением и законом степени."""
    вон = []
    for i in range(20):
        x = 1 + (i % 8) + шаг
        # f(t) = t^2: точное разностное отношение на шаге 1
        было, стало = x * x, (x + 1) * (x + 1)
        изм_en = f"for f(t) = t^2 the change from {x} to {x + 1}"
        изм_ru = f"для f(t) = t^2 изменение от {x} до {x + 1}"
        утв_и_en = f"{изм_en} is {стало - было}."
        утв_и_ru = f"{изм_ru} равно {стало - было}."
        вон.append(утв_и_en)
        вон.append(утв_и_ru)
        вон.append(спросить("change", утв_и_en, степень=2, a=x, b=x + 1))
        вон.append(спросить("изменение", утв_и_ru, степень=2, a=x, b=x + 1))
        for степень, значение in ((2, 2 * x), (3, 3 * x * x)):
            пр_en = f"the derivative of t^{степень} at {x}"
            пр_ru = f"производная t^{степень} в точке {x}"
            утв_en = f"{пр_en} is {значение}."
            утв_ru = f"{пр_ru} равна {значение}."
            вон.append(утв_en)
            вон.append(утв_ru)
            вон.append(спросить("derivative", утв_en, предмет=пр_en))
            вон.append(спросить("производная", утв_ru, предмет=пр_ru))
    return вон


ГРУППЫ = (арифметические, геометрические, пределы,
          отказ_предела, производные)


def pass_groups(pass_i):
    return [сделать(pass_i) for сделать in ГРУППЫ]


def main():
    emit_grouped("datasets/genesis_sequences.txt", pass_groups)


if __name__ == "__main__":
    main()
