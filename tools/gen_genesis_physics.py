#!/usr/bin/env python3
"""GENESIS layer: THE FOUNDATIONS OF PHYSICS.

    a body covering 60 metres in 12 seconds has speed 5 metres per second.
    тело, прошедшее 60 метров за 12 секунд, имеет скорость 5 метров в секунду.
    force = mass × acceleration; 7 kilograms × 3 metres per second squared = 21 newtons.
    speed is measured in metres per second.

PHYSICS ENTERS A CORPUS AS TWO THINGS AT ONCE, and both are checkable:
a RELATION between quantities (v = s / t, F = m × a, U = I × R) and a
DIMENSION — what the quantity is measured in. A corpus giving the
number without the unit teaches arithmetic; one giving the unit without
the relation teaches vocabulary; the organism needs both in one show.

EVERY VALUE IS WHOLE BY CONSTRUCTION. Distances are multiples of their
times, forces are products, kinetic masses are even — nothing is
rounded. A corpus stating «3.33 metres per second» for ten over three
teaches a rounding as a truth. Where a law needs a real constant
(E = m c², gravitation), THE LAW IS NOT SHOWN: constants are a genus of
their own and need their own court before their shows.

SEVEN LAWS as integer relations — speed, force, work, power, density,
Ohm, kinetic energy — plus the PREFIXES (kilo, centi, milli), which are
conversions and are judged as such, and the DIMENSION table, checked
against its own declaration.
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import units
from layer import emit  # noqa: E402

ДВИЖЕНИЕ = [(60, 12), (100, 20), (84, 7), (45, 15), (72, 8),
            (90, 30), (56, 14), (120, 24), (63, 9), (40, 5)]
СИЛА = [(7, 3), (5, 4), (12, 2), (9, 5), (6, 8),
        (11, 3), (4, 9), (15, 2), (8, 6), (10, 7)]
РАБОТА = [(20, 3), (15, 4), (30, 2), (12, 5), (25, 4),
          (18, 6), (40, 3), (14, 5), (35, 2), (16, 7)]
ПЛОТНОСТЬ = [(48, 6), (35, 7), (72, 8), (90, 9), (44, 4),
             (60, 5), (84, 12), (36, 3), (100, 10), (56, 8)]
ОМ = [(3, 12), (5, 8), (2, 25), (7, 6), (4, 15),
      (6, 9), (9, 4), (8, 7), (10, 3), (12, 5)]
КИНЕТИКА = [(4, 3), (6, 5), (8, 2), (10, 4), (12, 3),
            (2, 7), (14, 2), (16, 3), (18, 2), (20, 5)]
ИЗМЕРЯЕТСЯ = [
    ("speed", "metres per second", "скорость", "метрах в секунду"),
    ("force", "newtons", "сила", "ньютонах"),
    ("work", "joules", "работа", "джоулях"),
    ("power", "watts", "мощность", "ваттах"),
    ("mass", "kilograms", "масса", "килограммах"),
    ("length", "metres", "длина", "метрах"),
    ("time", "seconds", "время", "секундах"),
    ("current", "amperes", "ток", "амперах"),
    ("voltage", "volts", "напряжение", "вольтах"),
    ("resistance", "ohms", "сопротивление", "омах"),
]


# ПРИСТАВКА ЕСТЬ ЗАКОН, А НЕ ПЯТЬ ФАКТОВ. Эти строки стояли написанными
# от руки — и русская сторона миллиметра в них ПРОПАЛА: пять строк там,
# где закон даёт шесть. Пропуск, невидимый глазу в списке, виден сразу,
# как только список стал выводом. Письмо здесь британское, у слоя
# единиц — американское; оба истинны и оба объявлены.
ПИСЬМО = "brit"
ОСНОВА = "metre"


def приставочные():
    """«1 X = N Y» для каждой приставки, обоими языками."""
    пары = []
    for пр, пр_ru, множитель in units.ПРИСТАВКИ:
        имя = пр + ОСНОВА
        большая, меньшая = ((имя, ОСНОВА) if множитель >= 1
                            else (ОСНОВА, имя))
        сколько = int(units.отношение(большая, меньшая))
        пары.append((f"1 {units.англ(большая, False, ПИСЬМО)} = "
                     f"{сколько} {units.англ(меньшая, True, ПИСЬМО)}.",
                     f"1 {units.рус(большая, 1)} = "
                     f"{сколько} {units.рус(меньшая, сколько)}."))
    return [en for en, _ in пары] + [ru for _, ru in пары]


ПРИСТАВОЧНЫЕ = приставочные()


def pass_shows(pass_i):
    out = []
    for i in range(10):
        s, t = ДВИЖЕНИЕ[(pass_i + i) % len(ДВИЖЕНИЕ)]
        m, a = СИЛА[(pass_i * 3 + i) % len(СИЛА)]
        f, d = РАБОТА[(pass_i * 5 + i) % len(РАБОТА)]
        mm, v = ПЛОТНОСТЬ[(pass_i * 7 + i) % len(ПЛОТНОСТЬ)]
        cur, r = ОМ[(pass_i + i * 3) % len(ОМ)]
        km, kv = КИНЕТИКА[(pass_i * 2 + i) % len(КИНЕТИКА)]
        out.append(f"a body covering {s} metres in {t} seconds has speed "
                   f"{s // t} metres per second.")
        out.append(f"тело, прошедшее {s} метров за {t} секунд, имеет "
                   f"скорость {s // t} метров в секунду.")
        out.append(f"speed = distance / time; {s} / {t} = {s // t}.")
        out.append(f"force = mass × acceleration; {m} kilograms × {a} "
                   f"metres per second squared = {m * a} newtons.")
        out.append(f"сила = масса × ускорение; {m} килограммов × {a} "
                   f"метров на секунду в квадрате = {m * a} ньютонов.")
        out.append(f"work = force × distance; {f} newtons × {d} metres = "
                   f"{f * d} joules.")
        out.append(f"работа = сила × путь; {f} ньютонов × {d} метров = "
                   f"{f * d} джоулей.")
        out.append(f"power = work / time; {f * d} joules / {d} seconds = "
                   f"{f} watts.")
        out.append(f"мощность = работа / время; {f * d} джоулей / {d} "
                   f"секунд = {f} ватт.")
        out.append(f"density = mass / volume; {mm} kilograms / {v} cubic "
                   f"metres = {mm // v} kilograms per cubic metre.")
        out.append(f"плотность = масса / объём; {mm} килограммов / {v} "
                   f"кубометров = {mm // v} килограммов на кубометр.")
        out.append(f"voltage = current × resistance; {cur} amperes × {r} "
                   f"ohms = {cur * r} volts.")
        out.append(f"напряжение = ток × сопротивление; {cur} ампер × {r} "
                   f"ом = {cur * r} вольт.")
        out.append(f"kinetic energy = mass × speed squared / 2; {km} × "
                   f"{kv} × {kv} / 2 = {km * kv * kv // 2} joules.")
        out.append(f"кинетическая энергия = масса × квадрат скорости / 2; "
                   f"{km} × {kv} × {kv} / 2 = {km * kv * kv // 2} джоулей.")
        out.extend(ПРИСТАВОЧНЫЕ)
        en_имя, en_ед, ru_имя, ru_ед = ИЗМЕРЯЕТСЯ[
            (pass_i * 3 + i) % len(ИЗМЕРЯЕТСЯ)]
        out.append(f"{en_имя} is measured in {en_ед}.")
        out.append(f"{ru_имя} измеряется в {ru_ед}.")
    return out


def main():
    emit("datasets/genesis_physics.txt", pass_shows)


if __name__ == "__main__":
    main()
