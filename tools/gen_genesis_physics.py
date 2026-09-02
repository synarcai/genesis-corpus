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
import rugram
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

# ИСКОМОЕ ОБЪЯВЛЯЕТ СВОЙ ВОПРОС ОДИН РАЗ, и вопрос берёт ТЕ ЖЕ
# величины, из которых собран ответ. Замер вопросной поверхности назвал
# физику немой: 1150 строк, вопросов ноль — она сообщала, что тело,
# прошедшее 60 метров за 12 секунд, имеет скорость 5, и ни разу не
# спрашивала, какова эта скорость.
СПРОСИТЬ = {
    "speed": "what speed has a body covering {s} metres in {t} seconds?",
    "скорость": ("какова скорость тела, прошедшего {s} {метры} "
                 "за {t} {секунды}?"),
    "law": "what does {закон} give for {x} and {y}?",
    "закон": "что даёт {закон} при {x} и {y}?",
}


def спросить(искомое, ответ, **части):
    """Вопрос и ответ одной строкой; величины у них одни и те же."""
    return f"{СПРОСИТЬ[искомое].format(**части)} {ответ}"


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
        ск_en = (f"a body covering {s} metres in {t} seconds has speed "
                 f"{s // t} metres per second.")
        ск_ru = (f"тело, прошедшее {s} {rugram.форма('метр', s)} за "
                 f"{t} {rugram.форма('секунда', t)}, имеет скорость "
                 f"{s // t} {rugram.форма('метр', s // t)} в секунду.")
        out.append(ск_en)
        out.append(ск_ru)
        out.append(спросить("speed", ск_en, s=s, t=t))
        out.append(спросить("скорость", ск_ru, s=s, t=t,
                            метры=rugram.форма("метр", s),
                            секунды=rugram.форма("секунда", t)))
        закон_ск = f"speed = distance / time; {s} / {t} = {s // t}."
        out.append(закон_ск)
        out.append(спросить("law", закон_ск, закон="speed = distance / time",
                            x=s, y=t))
        сил_en = (f"force = mass × acceleration; {m} kilograms × {a} "
                  f"metres per second squared = {m * a} newtons.")
        out.append(сил_en)
        out.append(спросить("law", сил_en,
                            закон="force = mass × acceleration", x=m, y=a))
        out.append(f"сила = масса × ускорение; "
                   f"{m} {rugram.форма('килограмм', m)} × "
                   f"{a} {rugram.форма('метр', a)} на секунду в квадрате = "
                   f"{m * a} {rugram.форма('ньютон', m * a)}.")
        раб_en = (f"work = force × distance; {f} newtons × {d} metres = "
                  f"{f * d} joules.")
        out.append(раб_en)
        out.append(спросить("law", раб_en, закон="work = force × distance",
                            x=f, y=d))
        раб_ru = (f"работа = сила × путь; "
                  f"{f} {rugram.форма('ньютон', f)} × "
                  f"{d} {rugram.форма('метр', d)} = "
                  f"{f * d} {rugram.форма('джоуль', f * d)}.")
        out.append(раб_ru)
        out.append(спросить("закон", раб_ru, закон="работа = сила × путь",
                            x=f, y=d))
        out.append(f"power = work / time; {f * d} joules / {d} seconds = "
                   f"{f} watts.")
        out.append(f"мощность = работа / время; {f * d} "
                   f"{rugram.форма('джоуль', f * d)} / {d} "
                   f"{rugram.форма('секунда', d)} = {f} "
                   f"{rugram.форма('ватт', f)}.")
        out.append(f"density = mass / volume; {mm} kilograms / {v} cubic "
                   f"metres = {mm // v} kilograms per cubic metre.")
        out.append(f"плотность = масса / объём; "
                   f"{mm} {rugram.форма('килограмм', mm)} / "
                   f"{v} {rugram.форма('кубометр', v)} = "
                   f"{mm // v} {rugram.форма('килограмм', mm // v)} "
                   f"на кубометр.")
        напр_en = (f"voltage = current × resistance; {cur} amperes × {r} "
                   f"ohms = {cur * r} volts.")
        out.append(напр_en)
        out.append(спросить("law", напр_en,
                            закон="voltage = current × resistance",
                            x=cur, y=r))
        out.append(f"напряжение = ток × сопротивление; {cur} "
                   f"{rugram.форма('ампер', cur)} × {r} {rugram.форма('ом', r)} = "
                   f"{cur * r} {rugram.форма('вольт', cur * r)}.")
        out.append(f"kinetic energy = mass × speed squared / 2; {km} × "
                   f"{kv} × {kv} / 2 = {km * kv * kv // 2} joules.")
        out.append(f"кинетическая энергия = масса × квадрат скорости / 2; "
                   f"{km} × {kv} × {kv} / 2 = {km * kv * kv // 2} "
                   f"{rugram.форма('джоуль', km * kv * kv // 2)}.")
        out.extend(ПРИСТАВОЧНЫЕ)
        en_имя, en_ед, ru_имя, ru_ед = ИЗМЕРЯЕТСЯ[
            (pass_i * 3 + i) % len(ИЗМЕРЯЕТСЯ)]
        out.append(f"{en_имя} is measured in {en_ед}.")
        out.append(f"{ru_имя} измеряется в {ru_ед}.")
        # ОТКАЗ С ОСНОВАНИЕМ. Скорость при пути, не делящемся на время,
        # существует, но целым числом не выражается, и корпус её не
        # пишет: приближение, названное равенством, есть ложь того же
        # рода, что «5 ÷ 2 = 2». Основание названо числом и судимо.
        путь, срок = s + 1, t
        if путь % срок:
            # ВЕЛИЧИНА СТОИТ В ИМЕНИТЕЛЬНОМ, А НЕ ПОСЛЕ ПРЕДЛОГА:
            # «для 73 метра» было бы неверно (предлог требует
            # родительного, а счётная форма даёт «метра»), и мир учил
            # бы неверному управлению с полной судимостью. Оборот
            # переписан так, чтобы счётная форма стояла там, где она и
            # права, — при числе.
            out.append(f"what speed has a body covering {путь} metres "
                       f"in {срок} seconds? no whole answer: {путь} "
                       f"metres in {срок} seconds do not give a whole "
                       f"speed, {путь} is not divisible by {срок}.")
            # СКАЗУЕМОЕ ИДЁТ ЗА ЧИСЛОМ, А НЕ ЗА СЛОВОМ «МЕТРЫ»: «61
            # метр не даёт», но «73 метра не дают». Единственность
            # ВЫВОДИТСЯ из того же дома форм — если форма при этом
            # числе совпала с формой при единице, число ведёт себя как
            # один. Второй список чисел-исключений разошёлся бы с
            # первым в тот же день.
            один = (rugram.форма("метр", путь)
                    == rugram.форма("метр", 1))
            дают = "не даёт" if один else "не дают"
            out.append(f"какова скорость тела, прошедшего {путь} "
                       f"{rugram.форма('метр', путь)} за {срок} "
                       f"{rugram.форма('секунда', срок)}? целого "
                       f"ответа нет: {путь} "
                       f"{rugram.форма('метр', путь)} за {срок} "
                       f"{rugram.форма('секунда', срок)} {дают} целой "
                       f"скорости, {путь} не делится на {срок} "
                       f"нацело.")
    return out


def main():
    emit("datasets/genesis_physics.txt", pass_shows)


if __name__ == "__main__":
    main()
