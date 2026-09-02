#!/usr/bin/env python3
"""GENESIS layer: PHYSICAL LAWS — dimension, conservation, pressure, wave.

The syllabus court named four subjects absent. Each is a DIFFERENT KIND
of physical reasoning, and their absence left the corpus with formulas
and without physics:

  · DIMENSION is the check that costs nothing and catches everything:
    a law whose sides disagree in dimension is wrong before any number
    is put in. The corpus knew units and never checked a law BY them;
  · CONSERVATION is the first argument from what does NOT change — the
    shape of reasoning that carries the whole of physics;
  · PRESSURE is force over area: the first quantity that is a RATIO of
    two others, and therefore the first place where a unit is derived
    rather than named;
  · WAVE ties period and frequency as reciprocals — the first inverse
    proportion with physical meaning.

EVERY NUMBER IS EXACT. Frequencies are chosen so that period × frequency
is whole; pressures so that force divides the area exactly. A corpus
that rounds teaches rounding, and the arithmetic court would rightly
call it false.
"""

import sys
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import rugram
from layer import emit_grouped  # noqa: E402

# РАЗМЕРНОСТЬ ОБЪЯВЛЕНА ФОРМУЛОЙ ЧЕРЕЗ ОСНОВНЫЕ: длина, масса, время.
# Её нельзя вывести из имени величины — её знают.
# ПРЕДЛОЖНЫЙ ПАДЕЖ НАЗВАН, А НЕ ВЫВЕДЕН: «измеряется в метрах», не «в
# метр». Русскую форму нельзя получить отсечением, её называют.
РАЗМЕРНОСТИ = (
    ("скорость", "speed", "L / T", "метрах в секунду",
     "metre per second"),
    ("ускорение", "acceleration", "L / T^2",
     "метрах на секунду в квадрате", "metre per second squared"),
    ("сила", "force", "M L / T^2", "ньютонах", "newton"),
    ("работа", "work", "M L^2 / T^2", "джоулях", "joule"),
    ("мощность", "power", "M L^2 / T^3", "ваттах", "watt"),
    ("давление", "pressure", "M / (L T^2)", "паскалях", "pascal"),
    ("импульс", "momentum", "M L / T",
     "килограмм-метрах в секунду", "kilogram metre per second"),
)


# ИСКОМОЕ ОБЪЯВЛЯЕТ СВОЙ ВОПРОС ОДИН РАЗ, и вопрос берёт ТЕ ЖЕ
# величины, из которых собран ответ. Замер вопросной поверхности назвал
# этот мир немым: 990 строк, вопросов ноль.
СПРОСИТЬ = {
    "law": "what does {закон} give for {x} and {y}?",
    "закон": "что даёт {закон} при {x} и {y}?",
}


def спросить(искомое, ответ, **части):
    """Вопрос и ответ одной строкой; величины у них одни и те же."""
    return f"{СПРОСИТЬ[искомое].format(**части)} {ответ}"


def размерности(шаг):
    вон = []
    for ру, en, форм, ру_пред, en_ед in РАЗМЕРНОСТИ:
        вон.append(f"размерность величины {ру} есть {форм}; "
                   f"измеряется в {ру_пред}.")
        вон.append(f"the dimension of {en} is {форм}; "
                   f"it is measured in {en_ед}.")
    return вон


def сохранение(шаг):
    """Что не рождается и не исчезает — довод от неизменного."""
    вон = []
    for i in range(16):
        a, b = 3 + (i + шаг) % 7, 5 + (i * 2 + шаг) % 9
        итог = a + b
        вон.append(f"импульс сохраняется: было {a} и {b}, стало "
                   f"{итог}, сумма не изменилась.")
        вон.append(f"momentum is conserved: {a} and {b} before, "
                   f"{итог} after, the sum did not change.")
        e1, e2 = 4 + (i + шаг) % 6, 6 + (i + шаг) % 8
        целое, часть = max(e1, e2), min(e1, e2)
        остаток = целое - часть
        вон.append(f"энергия сохраняется: {целое} "
                   f"{rugram.форма('джоуль', целое)} разделились на {часть} и "
                   f"{остаток} {rugram.форма('джоуль', остаток)}.")
        вон.append(f"energy is conserved: {max(e1, e2)} joules split "
                   f"into {min(e1, e2)} and "
                   f"{max(e1, e2) - min(e1, e2)} joules.")
    return вон


def давление(шаг):
    """Сила на площадь — первая величина как ОТНОШЕНИЕ двух других."""
    вон = []
    for i in range(20):
        площадь = 2 + (i + шаг) % 6
        p = 3 + (i + шаг) % 8
        сила = p * площадь
        утв_ru = (f"давление = сила ÷ площадь; {сила} "
                  f"{rugram.форма('ньютон', сила)} ÷ {площадь} "
                  f"{rugram.форма('квадратный метр', площадь)} = {p} "
                  f"{rugram.форма('паскаль', p)}.")
        утв_en = (f"pressure = force ÷ area; {сила} newtons ÷ "
                  f"{площадь} square metres = {p} pascals.")
        вон.append(утв_ru)
        вон.append(утв_en)
        вон.append(спросить("закон", утв_ru,
                            закон="давление = сила ÷ площадь",
                            x=сила, y=площадь))
        вон.append(спросить("law", утв_en,
                            закон="pressure = force ÷ area",
                            x=сила, y=площадь))
        # ОТКАЗ С ОСНОВАНИЕМ: сила, не делящаяся на площадь, целого
        # давления не даёт, и мир его не пишет — приближение, названное
        # равенством, есть ложь того же рода, что «5 ÷ 2 = 2».
        # СКАЗУЕМОЕ ИДЁТ ЗА ЧИСЛОМ: «21 ньютон не даёт», но «25
        # ньютонов не дают»; единственность выводится из того же дома
        # форм, а не из второго списка чисел.
        косая = сила + 1
        if косая % площадь:
            один = (rugram.форма("ньютон", косая)
                    == rugram.форма("ньютон", 1))
            вон.append(f"что даёт давление = сила ÷ площадь при "
                       f"{косая} и {площадь}? целого ответа нет: "
                       f"{косая} {rugram.форма('ньютон', косая)} на "
                       f"{площадь} "
                       f"{rugram.форма('квадратный метр', площадь)} "
                       f"{'не даёт' if один else 'не дают'} целого "
                       f"давления, {косая} не делится на {площадь} "
                       f"нацело.")
            вон.append(f"what does pressure = force ÷ area give for "
                       f"{косая} and {площадь}? no whole answer: "
                       f"{косая} newtons over {площадь} square metres "
                       f"do not give a whole pressure, {косая} is not "
                       f"divisible by {площадь}.")
    return вон


def волна(шаг):
    """Период и частота обратны: их произведение есть единица."""
    вон = []
    for i in range(20):
        период = 1 + (i + шаг) % 8
        частота = 60 // период if 60 % период == 0 else 12
        период = 60 // частота
        # ПРЕДЛОГ ТРЕБУЕТ СВОЕГО ПАДЕЖА, и «в 1 секунда» неверно, как
        # неверно «a period of 1 seconds». Оборот выбран такой, где
        # падеж есть именительный счётный, — форма тогда одна и верна.
        вон.append(f"период — {период} {rugram.форма('секунда', период)}; "
                   f"частота — {частота} "
                   f"{rugram.форма('колебание', частота)} в минуту; "
                   f"{период} × {частота} = 60.")
        вон.append(f"the period is {период} "
                   f"{'second' if период == 1 else 'seconds'}; the "
                   f"frequency is {частота} per minute; "
                   f"{период} × {частота} = 60.")
        скорость = 3 + (i + шаг) % 5
        длина = скорость * период
        вон.append(f"скорость волны = длина ÷ период; {длина} "
                   f"{rugram.форма('метр', длина)} ÷ {период} "
                   f"{rugram.форма('секунда', период)} = {скорость} "
                   f"{rugram.форма('метр', скорость)} в секунду.")
        вон.append(f"wave speed = length ÷ period; {длина} metres ÷ "
                   f"{период} {'second' if период == 1 else 'seconds'} "
                   f"= {скорость} metres per second.")
    return вон


ГРУППЫ = (размерности, сохранение, давление, волна)


def pass_groups(pass_i):
    return [сделать(pass_i) for сделать in ГРУППЫ]


def main():
    emit_grouped("datasets/genesis_physlaws.txt", pass_groups)


if __name__ == "__main__":
    main()
