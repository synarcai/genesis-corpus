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

import sys
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from layer import emit_grouped  # noqa: E402

# ИСКОМОЕ ОБЪЯВЛЯЕТ СВОЙ ВОПРОС ОДИН РАЗ. Русский вопрос ставит предмет
# в родительный, английский — как есть; связка идёт за родом имени меры
# («чему равнА площадь», «чему равЕН периметр»), и потому вопрос
# объявляется при мере, а не при фигуре.
СПРОСИТЬ = {
    "area": "what is the area of {предмет}?",
    "perimeter": "what is the perimeter of {предмет}?",
    "volume": "what is the volume of {предмет}?",
    "surface": "what is the surface of {предмет}?",
    "hypotenuse": "what is the hypotenuse of {предмет}?",
    "площадь": "чему равна площадь {предмет}?",
    "периметр": "чему равен периметр {предмет}?",
    "объём": "чему равен объём {предмет}?",
    "поверхность": "чему равна поверхность {предмет}?",
    "гипотенуза": "чему равна гипотенуза {предмет}?",
}

# ФОРМУЛЫ РОДОВ — ЗАКОН ОТВЕТА ОТ ВЕЛИЧИН ВОПРОСА, объявлен при каждом вопросе
# (таблица родов declarations/GENERA.json — эталон суда охвата, holon 03.09).
ФОРМУЛЫ = {
    "area": "площадь = a × b",
    "perimeter": "периметр = 2 × (a + b)",
    "volume": "объём = a × b × c",
    "surface": "поверхность = 2 × (ab + bc + ca)",
    "hypotenuse": "c = √(a² + b²)",
    "площадь": "площадь = a × b",
    "периметр": "периметр = 2 × (a + b)",
    "объём": "объём = a × b × c",
    "поверхность": "поверхность = 2 × (ab + bc + ca)",
    "гипотенуза": "c = √(a² + b²)",
}
assert set(ФОРМУЛЫ) == set(СПРОСИТЬ), "формула у каждого вопроса"


def спросить(мера, предмет, ответ):
    """Вопрос об искомой мере ПРЕДМЕТА и ответ о нём же — одной строкой.

    Предмет приходит сюда той же строкой, какой он стоит в ответе:
    источник у вопроса и ответа один, и разойтись им негде.
    """
    return f"{СПРОСИТЬ[мера].format(предмет=предмет)} {ответ}"


# ТРОЙКИ НАЗВАНЫ, А НЕ НАЙДЕНЫ ПЕРЕБОРОМ: каждая проверена здесь же.
ТРОЙКИ = ((3, 4, 5), (6, 8, 10), (5, 12, 13), (9, 12, 15),
          (8, 15, 17), (7, 24, 25), (20, 21, 29), (12, 16, 20))
assert all(a * a + b * b == c * c for a, b, c in ТРОЙКИ)


def прямоугольники(шаг):
    вон = []
    for i in range(24):
        a, b = 2 + (i % 9) + шаг, 3 + (i % 7)
        en, ru = f"a rectangle {a} by {b}", f"прямоугольник {a} на {b}"
        ru_род = f"прямоугольника {a} на {b}"
        # ПРОМЕЖУТОЧНЫЕ ВЕЛИЧИНЫ В ОТВЕТЕ (коллегия 03.09, П-1): без «7 × 8 = 56» и
        # «2 × (7 + 8) = 30» композиция глубины два невыводима из показов.
        утв_en = f"{en} has area {a} × {b} = {a * b} and perimeter 2 × ({a} + {b}) = {2 * (a + b)}."
        утв_ru = (f"{ru} имеет площадь {a} × {b} = {a * b} "
                  f"и периметр 2 × ({a} + {b}) = {2 * (a + b)}.")
        вон.append(утв_en)
        вон.append(утв_ru)
        вон.append(спросить("area", en, утв_en))
        вон.append(спросить("perimeter", en, утв_en))
        вон.append(спросить("площадь", ru_род, утв_ru))
        вон.append(спросить("периметр", ru_род, утв_ru))
    return вон


def квадраты(шаг):
    вон = []
    for i in range(16):
        a = 2 + (i % 12) + шаг
        en, ru = f"a square with side {a}", f"квадрат со стороной {a}"
        ru_род = f"квадрата со стороной {a}"
        утв_en = f"{en} has area {a} × {a} = {a * a} and perimeter 4 × {a} = {4 * a}."
        утв_ru = f"{ru} имеет площадь {a} × {a} = {a * a} и периметр 4 × {a} = {4 * a}."
        вон.append(утв_en)
        вон.append(утв_ru)
        вон.append(спросить("area", en, утв_en))
        вон.append(спросить("площадь", ru_род, утв_ru))
        вон.append(спросить("периметр", ru_род, утв_ru))
    return вон


def треугольники(шаг):
    """Площадь через основание и высоту — только при чётном произведении."""
    вон = []
    for i in range(20):
        b, h = 2 + (i % 10) + шаг, 4 + (i % 6)
        if (b * h) % 2:
            b += 1
        en = f"a triangle with base {b} and height {h}"
        ru = f"треугольник с основанием {b} и высотой {h}"
        ru_род = f"треугольника с основанием {b} и высотой {h}"
        утв_en = f"{en} has area {b} × {h} ÷ 2 = {b * h // 2}."
        утв_ru = f"{ru} имеет площадь {b} × {h} ÷ 2 = {b * h // 2}."
        вон.append(утв_en)
        вон.append(утв_ru)
        вон.append(спросить("area", en, утв_en))
        вон.append(спросить("площадь", ru_род, утв_ru))
    return вон


def пифагор(шаг):
    вон = []
    for a, b, c in ТРОЙКИ:
        en = f"a right triangle with legs {a} and {b}"
        ru = f"прямоугольный треугольник с катетами {a} и {b}"
        ru_род = f"прямоугольного треугольника с катетами {a} и {b}"
        утв_en = f"{en} has hypotenuse {c}: {a}^2 + {b}^2 = {a * a + b * b} and {c}^2 = {c * c}."
        утв_ru = f"{ru} имеет гипотенузу {c}: {a}^2 + {b}^2 = {a * a + b * b} и {c}^2 = {c * c}."
        вон.append(утв_en)
        вон.append(утв_ru)
        вон.append(f"{a}^2 + {b}^2 = {c}^2.")
        вон.append(спросить("hypotenuse", en, утв_en))
        вон.append(спросить("гипотенуза", ru_род, утв_ru))
    return вон


def _полный_квадрат(n):
    """Целое ли число корень: суд отказа считает то же самое сам."""
    к = int(n ** 0.5)
    while к * к < n:
        к += 1
    return к * к == n


def отказ_гипотенузы(шаг):
    """Вопрос, чей честный ответ — «целого нет, и вот почему».

    МИР, УМЕЮЩИЙ ТОЛЬКО УТВЕРЖДАТЬ, УЧИТ СОГЛАШАТЬСЯ. Гипотенуза при
    катетах 2 и 3 существует, но целым числом не выражается, и корпус
    её не пишет — таков объявленный закон этого мира. Отказ называет
    ОСНОВАНИЕ числом: сумма квадратов и то, что она не полный квадрат.
    """
    вон = []
    for i in range(20):
        a = 2 + (шаг + i) % 9
        b = a + 1 + (шаг * 2 + i) % 7
        с = a * a + b * b
        if _полный_квадрат(с):
            continue
        вон.append(f"what is the hypotenuse of a right triangle with "
                   f"legs {a} and {b}? no whole answer for legs {a} "
                   f"and {b}: {a}^2 + {b}^2 = {с}, and {с} is not a "
                   f"perfect square.")
        вон.append(f"чему равна гипотенуза прямоугольного треугольника "
                   f"с катетами {a} и {b}? целого ответа нет для "
                   f"катетов {a} и {b}: {a}^2 + {b}^2 = {с}, а {с} не "
                   f"полный квадрат.")
    return вон


def тела(шаг):
    вон = []
    for i in range(20):
        a, b, c = 2 + (i % 5) + шаг, 3 + (i % 4), 2 + (i % 6)
        en_к, ru_к = f"a box {a} by {b} by {c}", f"коробка {a} на {b} на {c}"
        ru_к_род = f"коробки {a} на {b} на {c}"
        утв_к_en = (f"{en_к} has volume {a} × {b} × {c} = {a * b * c} and surface "
                    f"2 × ({a} × {b} + {b} × {c} + {a} × {c}) = {2 * (a * b + b * c + a * c)}.")
        утв_к_ru = (f"{ru_к} имеет объём {a} × {b} × {c} = {a * b * c} и поверхность "
                    f"2 × ({a} × {b} + {b} × {c} + {a} × {c}) = {2 * (a * b + b * c + a * c)}.")
        en_куб, ru_куб = f"a cube with edge {a}", f"куб с ребром {a}"
        ru_куб_род = f"куба с ребром {a}"
        утв_куб_en = f"{en_куб} has volume {a} × {a} × {a} = {a ** 3}."
        утв_куб_ru = f"{ru_куб} имеет объём {a} × {a} × {a} = {a ** 3}."
        вон.append(утв_к_en)
        вон.append(утв_к_ru)
        вон.append(утв_куб_en)
        вон.append(утв_куб_ru)
        вон.append(спросить("volume", en_к, утв_к_en))
        вон.append(спросить("surface", en_к, утв_к_en))
        вон.append(спросить("объём", ru_к_род, утв_к_ru))
        вон.append(спросить("поверхность", ru_к_род, утв_к_ru))
        вон.append(спросить("volume", en_куб, утв_куб_en))
        вон.append(спросить("объём", ru_куб_род, утв_куб_ru))
    return вон


ГРУППЫ = (прямоугольники, квадраты, треугольники, пифагор,
          отказ_гипотенузы, тела)


import laws  # noqa: E402


def pass_groups(pass_i):
    return [сделать(pass_i) for сделать in ГРУППЫ] + [laws.ступень("geometry")]


def main():
    emit_grouped("datasets/genesis_geometry.txt", pass_groups)


if __name__ == "__main__":
    main()
