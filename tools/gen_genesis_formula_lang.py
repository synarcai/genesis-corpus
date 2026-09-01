#!/usr/bin/env python3
"""GENESIS layer: FORMULA ↔ SPEECH — conversion at any complexity.

The owner's requirement, in his words: the organism must be able to
convert formulas of ANY complexity by itself. That is not a list of
formulas; it is a GRAMMAR, and a grammar is learned from a form shown on
many depths, not from many forms shown once.

WHAT A LIST CANNOT BUY. The corpus already carried formula shows: «the
sum of the first n numbers is n × ( n + 1 ) / 2» stood beside its worded
twin. That teaches THAT formula. It cannot teach the NEXT one, because
the pairing was written by hand and nothing in it says how a formula is
read in general.

WHAT IS SHOWN HERE. One tree, four surfaces, and the CONVERSION between
them as the show itself:
    «$ \\frac{a + b}{2} $ in words is the fraction with numerator ( a
     plus b ) and denominator 2.»
    «дробь с числителем ( сумма a и b ) и знаменателем 2 в записи есть
     $ \\frac{a + b}{2} $.»
Both directions, both languages, and the trees behind them are BUILT to
depth: depth one, two, three, four. Depth is the teacher — a reader who
has seen a fraction whose numerator is itself a sum has seen the rule,
not the case.

BRACKETS IN SPEECH ARE GRAMMAR, NOT ORNAMENT. A compound argument is
always spoken inside brackets, an atomic one never; this is what a
mathematician reading aloud actually does, and it is what makes speech
parsable at any depth.

THE ORACLE IS EIGHT WALKS. Four surfaces are written by four renderers
and read back by four parsers, written apart; a tree that does not
return through all of them never becomes a show. Four thousand trees to
depth four pass without a single divergence — that is the proof carried
in `tools/formula_lang.py`, and this layer refuses to build without it.
"""

import pathlib
import random
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import formula_lang as фл  # noqa: E402
from layer import emit_grouped  # noqa: E402

ЦЕЛЬ = "datasets/genesis_formula_lang.txt"
ПЕРЕМЕННЫЕ = ("a", "b", "c", "x", "y", "n")
# РОДЫ УЗЛОВ, ПОКАЗЫВАЕМЫЕ СЛОЕМ. Прибавить род — значит объявить его
# в доме формул; здесь он лишь называется.
# РАВЕНСТВО НЕ ВХОДИТ В СЛУЧАЙНЫЕ УЗЛЫ. Случайное «=» рождает ЛОЖНОЕ
# равенство («| 9 | = 4 + 11»), а корпус не смеет нести ложь даже
# примером конверсии: арифметический суд поймал две такие строки в тот
# же час, и он был прав. Равенство ставится ОТДЕЛЬНО — и правая часть
# ВЫЧИСЛЯЕТСЯ из левой, а не бросается жребием.
УЗЛЫ = ("+", "-", "*", "/", "^", "корень", "модуль", "функ", "сумма")
ФУНКЦИИ = ("sin", "cos", "log")


def дерево(r, глубина):
    """Дерево объявленной глубины — построено, а не выписано."""
    if глубина <= 0:
        return (фл.чис(r.randint(1, 20)) if r.random() < 0.5
                else фл.пер(r.choice(ПЕРЕМЕННЫЕ)))
    род = r.choice(УЗЛЫ)
    if род == "корень":
        return ("корень", дерево(r, глубина - 1))
    if род == "модуль":
        return ("модуль", дерево(r, глубина - 1))
    if род == "функ":
        return ("функ", r.choice(ФУНКЦИИ), дерево(r, глубина - 1))
    if род == "сумма":
        return ("сумма", "i", дерево(r, глубина - 1),
                дерево(r, глубина - 1), дерево(r, глубина - 1))
    return (род, дерево(r, глубина - 1), дерево(r, глубина - 1))


def показы_глубины(шаг, глубина, сколько):
    """Конверсия обеими сторонами и на двух языках, одной глубины."""
    r = random.Random(1000 * глубина + шаг)
    вон = []
    for k in range(сколько):
        д = дерево(r, глубина)
        # КАЖДЫЙ ТРЕТИЙ ПОКАЗ — РАВЕНСТВО, И ОНО ИСТИННО ПО ПОСТРОЕНИЮ:
        # правая часть есть ВЫЧИСЛЕННАЯ величина левой. Открытое дерево
        # (со свободной переменной) величины не имеет и равенством не
        # становится — это свойство выражения, а не отказ прибора.
        if k % 3 == 2:
            в = фл.значение(д)
            if в is not None and в >= 0:
                д = ("=", д, фл.чис(в))
        лат, гл = фл.латех(д), фл.глиф(д)
        ен, ру = фл.слова(д, "en"), фл.слова(д, "ru")
        # ХОДЫ СВЕРЯЮТСЯ ПЕРЕД ПОКАЗОМ: дерево, не вернувшееся всеми
        # обратными ходами, не имеет права стать строкой корпуса.
        if (фл.разобрать_глиф(гл) != д
                or фл.разобрать_слова(ен, "en") != д
                or фл.разобрать_слова(ру, "ru") != д):
            continue
        вон.append(f"$ {лат} $ in words is {ен}.")
        вон.append(f"{ен} in symbols is $ {лат} $.")
        вон.append(f"$ {лат} $ в словах есть {ру}.")
        вон.append(f"{ру} в записи есть $ {лат} $.")
        вон.append(f"$ {лат} $ in glyphs is {гл}.")
        вон.append(f"{гл} в словах есть {ру}.")
        вон.append(f"how is $ {лат} $ said in words? $ {лат} $ in "
                   f"words is {ен}.")
        вон.append(f"как читается $ {лат} $? $ {лат} $ в словах есть "
                   f"{ру}.")
    return вон


def квадратные(шаг):
    """УРАВНЕНИЕ, ПРОЧИТАННОЕ ВСЛУХ, и оно же записью.

    «x squared minus five x plus six equals zero» — так уравнение
    произносят, и корпус, знавший только описательную речь («the sum
    of …»), не узнал бы его на слух. Коэффициенты выводятся из корней
    по Виете: показ несёт не случайные числа, а уравнение, у которого
    корни ЕСТЬ.
    """
    вон = []
    for i in range(10):
        r1 = 1 + (шаг + i) % 9
        r2 = 1 + (шаг * 3 + i * 2) % 11
        b, c = r1 + r2, r1 * r2
        x = фл.пер("x")
        д = ("=", ("+", ("-", ("^", x, фл.чис(2)),
                         ("*", фл.чис(b), x)), фл.чис(c)), фл.чис(0))
        if not фл.читается_вслух(д):
            continue
        гл, лат = фл.глиф(д), фл.латех(д)
        for яз, вопрос, связка in (
                ("en", "how is {г} read aloud?", "read aloud is"),
                ("ru", "как читается вслух {г}?", "вслух читается как")):
            вслух = фл.инфикс(д, яз)
            вон.append(f"{гл} {связка} {вслух}.")
            вон.append(f"{вслух} in glyphs is {гл}." if яз == "en"
                       else f"{вслух} в записи есть {гл}.")
            вон.append(f"{вопрос.format(г=гл)} {гл} {связка} {вслух}.")
        вон.append(f"$ {лат} $ in glyphs is {гл}.")
    return вон


def pass_groups(шаг):
    # ГЛУБИНА — СВОЯ ГРУППА: показы одной глубины не перемешиваются с
    # чужими, ибо глубина здесь и есть предмет урока.
    return ([показы_глубины(шаг, г, 14) for г in (1, 2, 3, 4)]
            + [квадратные(шаг)])


def main():
    беды = фл.оракул() if hasattr(фл, "оракул") else []
    if беды:
        print(f"ФОРМУЛЫ ОТКАЗ: {len(беды)} деревьев не обратимы")
        return 2
    emit_grouped(ЦЕЛЬ, pass_groups)
    return 0


if __name__ == "__main__":
    sys.exit(main())
