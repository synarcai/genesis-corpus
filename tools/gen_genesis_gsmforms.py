#!/usr/bin/env python3
"""ШКОЛЬНЫЕ ФОРМЫ g1 — покрытие немых семейств вопросов GSM8K.

Слово владельца (03.09, через коллегию): полоса g1 (65 задач GSM8K) —
к 100 % в кратчайший срок. Прибор e9 FORM-MUTE назвал семейства вопросов,
чья форма показа с ответом не встречается ни в одном мире; порядок
частоты — порядок корпуса. Здесь каждое семейство получает ПОВЕСТВОВАНИЕ
в школьной форме истории с ОСНОВАНИЕМ после двоеточия (счёт, который суд
пересчитывает), обеими полярностями там, где есть вердикт, с явными
дельтами и отношениями («на 5 больше, чем», «втрое», «в сумме»,
«осталось»), и ВОПРОС с ответом в той же строке — на немногих
родах-учителях (М-129: форма вопроса живёт на немногих родах).

Семейства первого среза (по частоте у e9):
  1 total number of  — сумма по носителям
  2 temperature in degrees — ниже нуля (знаковый мир, Д-5)
  3 percentage of — процент от доли (только целые проценты)
  4 weight in pounds — унции в фунты (16 унций = 1 фунт)
  5 water depth — объём ÷ площадь дна
  6 probability expressed as — доля как вероятность (дробью)
  7 # quarters of — доля от целого назад к целому
  8 originally / missing / people on — дополнение: исходное − ушедшее
Имена — из домов имён пакетов (actors: person_names:en, person_names:ru);
числа — по остаткам от номера прохода и показа, ни одно не вписано рукой;
только целые итоги (граница whole_only).
"""
import json
import pathlib
import sys

КОРЕНЬ = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(КОРЕНЬ / "tools"))
import rugram  # noqa: E402
from layer import emit_grouped  # noqa: E402
from plural import by_count  # noqa: E402

ЦЕЛЬ = "datasets/genesis_gsmforms.txt"
_EN = json.loads((КОРЕНЬ / "tools" / "langpacks" / "en.json").read_text(encoding="utf-8"))
_RU = json.loads((КОРЕНЬ / "tools" / "langpacks" / "ru.json").read_text(encoding="utf-8"))
ИМЕНА_EN = [n for n in _EN["person_names"] if n in ("ann", "ben", "carla", "dan", "elena", "felix", "grace", "hugo", "ida", "omar", "peter", "vera")]
# РУССКИЕ ИМЕНА В ИМЕНИТЕЛЬНОМ — рамки построены так, что иных падежей нет
# («Вера имеет 7 ручек»): так дом имён держит их одной таблицей.
ИМЕНА_RU = [n.capitalize() for n in _RU["person_names"] if n in ("вера", "петя", "маша", "коля", "аня", "дима", "лена", "юра")]
ВЕЩИ = (("pens", "ручка"), ("books", "книга"), ("apples", "яблоко"), ("coins", "монета"), ("cards", "карта"))


def ч(n):
    return str(n).replace("-", "−")


def ру(вещь, n):
    return rugram.форма(вещь, n)


# ---------- 1. total number of ----------
def сумма(шаг, i):
    a, b = ИМЕНА_EN[(шаг + i) % len(ИМЕНА_EN)], ИМЕНА_EN[(шаг + i * 3 + 1) % len(ИМЕНА_EN)]
    if b == a:
        b = ИМЕНА_EN[(ИМЕНА_EN.index(a) + 1) % len(ИМЕНА_EN)]
    ра, рб = ИМЕНА_RU[(шаг + i) % len(ИМЕНА_RU)], ИМЕНА_RU[(шаг + i * 3 + 1) % len(ИМЕНА_RU)]
    if рб == ра:
        рб = ИМЕНА_RU[(ИМЕНА_RU.index(ра) + 1) % len(ИМЕНА_RU)]
    en, вещь = ВЕЩИ[(шаг + i) % len(ВЕЩИ)]
    x, y = 2 + (шаг * 5 + i * 3) % 12, 2 + (шаг * 7 + i) % 9
    s = x + y
    ф = (шаг + i) % 4
    if ф == 0:
        return f"{a} has {x} {by_count(x, en)} and {b} has {y} {by_count(y, en)}; the total number of {en} is {s}: {x} + {y} = {s}."
    if ф == 1:
        return f"{ра} имеет {x} {ру(вещь, x)}, {рб} имеет {y} {ру(вещь, y)}; всего у них {s} {ру(вещь, s)}: {x} + {y} = {s}."
    if ф == 2:
        return f"{a} has {x} {by_count(x, en)} and {b} has {y} {by_count(y, en)}; the total number of {en} is not {s + 1}: it is {s}."
    # ОТВЕТ НАЧИНАЕТСЯ ВЕЛИЧИНАМИ ВОПРОСА В ИХ ПОРЯДКЕ (дом пары: величины
    # вопроса суть начальный отрезок величин ответа) и кончается итогом.
    return f"{a} has {x} {by_count(x, en)} and {b} has {y} {by_count(y, en)}. what's the total number of {en}? {x} + {y} = {s}."


# ---------- 2. temperature in degrees ----------
def температура(шаг, i):
    t0 = -6 + (шаг * 3 + i) % 15
    d = 2 + (шаг + i * 5) % 12
    падение = (шаг + i) % 2 == 0
    t1 = t0 - d if падение else t0 + d
    ф = (шаг + i) % 4
    if ф == 0:
        return (f"the temperature was {ч(t0)} {by_count(abs(t0), 'degrees')} and {'fell' if падение else 'rose'} by {d} {by_count(d, 'degrees')}; "
                f"the temperature in degrees is now {ч(t1)}: {ч(t0)} {'−' if падение else '+'} {d} = {ч(t1)}.")
    if ф == 1:
        return (f"температура была {ч(t0)} {ру('градус', abs(t0))} и {'упала' if падение else 'поднялась'} на {d} {ру('градус', d)}; "
                f"теперь температура — {ч(t1)} {ру('градус', abs(t1))}: {ч(t0)} {'−' if падение else '+'} {d} = {ч(t1)}.")
    if ф == 2:
        чуж = t1 + (d if падение else -d)
        return (f"the temperature was {ч(t0)} {by_count(abs(t0), 'degrees')} and {'fell' if падение else 'rose'} by {d} {by_count(d, 'degrees')}; "
                f"the temperature in degrees is not {ч(чуж)}: it is {ч(t1)}.")
    return (f"the temperature was {ч(t0)} {by_count(abs(t0), 'degrees')} and {'fell' if падение else 'rose'} by {d} {by_count(d, 'degrees')}. "
            f"what is the temperature in degrees now? {ч(t0)} {'−' if падение else '+'} {d} = {ч(t1)}.")


# ---------- 3. percentage of ----------
def процент(шаг, i):
    всего = (20, 25, 40, 50, 60, 80, 100)[(шаг + i) % 7]
    доли = [k for k in range(1, всего) if (k * 100) % всего == 0]
    часть = доли[(шаг * 3 + i) % len(доли)]
    p = часть * 100 // всего
    ф = (шаг + i) % 4
    if ф == 0:
        return (f"the class has {всего} pupils and {часть} of them are girls; the percentage of girls is {p} %: "
                f"{часть} ÷ {всего} × 100 = {p}.")
    if ф == 1:
        return (f"в классе {всего} {ру('ученик', всего)}, из них {часть} — {ру('девочка', часть)}; доля девочек — {p} %: "
                f"{часть} ÷ {всего} × 100 = {p}.")
    if ф == 2:
        return (f"the class has {всего} pupils and {часть} of them are girls; the percentage of girls is not {p + 5} %: it is {p} %.")
    return (f"the class has {всего} pupils and {часть} of them are girls. what percentage of the class are girls? "
            f"{всего} pupils and {часть} girls: {часть} ÷ {всего} × 100 = {p} %.")


# ---------- 4. weight in pounds ----------
def фунты(шаг, i):
    ф_ = 1 + (шаг * 3 + i) % 9
    унц = ф_ * 16
    ф = (шаг + i) % 4
    if ф == 0:
        return f"the parcel weighs {унц} ounces and a pound is 16 ounces; the weight in pounds is {ф_}: {унц} ÷ 16 = {ф_}."
    if ф == 1:
        return (f"посылка весит {унц} {ру('унция', унц)}, а в фунте 16 унций; вес в фунтах — {ф_} {ру('фунт', ф_)}: "
                f"{унц} ÷ 16 = {ф_}.")
    if ф == 2:
        return f"the parcel weighs {унц} ounces and a pound is 16 ounces; the weight in pounds is not {ф_ + 1}: it is {ф_}."
    return f"the parcel weighs {унц} ounces and a pound is 16 ounces. what is the weight in pounds? {унц} ÷ 16 = {ф_}."


# ---------- 5. water depth ----------
def глубина(шаг, i):
    w, l = 2 + (шаг + i) % 5, 2 + (шаг * 2 + i * 3) % 6
    h = 1 + (шаг * 5 + i) % 6
    v = w * l * h
    ф = (шаг + i) % 4
    if ф == 0:
        return (f"the tank is {w} feet wide and {l} feet long and holds {v} cubic feet of water; "
                f"the tank's water depth is {h} {by_count(h, 'feet')}: {v} ÷ ({w} × {l}) = {h}.")
    if ф == 1:
        return (f"бак шириной {w} {ру('фут', w)} и длиной {l} {ру('фут', l)} вмещает {v} кубических футов воды; "
                f"глубина воды в баке — {h} {ру('фут', h)}: {v} ÷ ({w} × {l}) = {h}.")
    if ф == 2:
        return (f"the tank is {w} feet wide and {l} feet long and holds {v} cubic feet of water; "
                f"the tank's water depth is not {h + 1} feet: it is {h} {by_count(h, 'feet')}.")
    return (f"the tank is {w} feet wide and {l} feet long and holds {v} cubic feet of water. "
            f"what is the tank's water depth? {w} by {l} holding {v}: {v} ÷ ({w} × {l}) = {h} {by_count(h, 'feet')}.")


# ---------- 6. probability expressed as ----------
def вероятность(шаг, i):
    r, b = 1 + (шаг + i) % 6, 1 + (шаг * 3 + i * 2) % 7
    n = r + b
    ф = (шаг + i) % 4
    if ф == 0:
        return (f"a bag holds {r} red {by_count(r, 'marbles')} and {b} blue {by_count(b, 'marbles')}; "
                f"the probability of drawing a red marble, expressed as a fraction, is {r}/{n}: {r} red out of {n}.")
    if ф == 1:
        return (f"в мешке {r} {ру('шар', r)} красных и {b} {ру('шар', b)} синих; "
                f"вероятность вынуть красный шар, выраженная дробью, — {r}/{n}: {r} красных из {n}.")
    if ф == 2:
        # ЧУЖАЯ ДОЛЯ — ЧИСЛИТЕЛЕМ СОСЕДА, а не синих: при r = b синих столько
        # же, и «не b/n» было бы ложью о верной дроби.
        чуж = r + 1 if r + 1 < n else r - 1
        return (f"a bag holds {r} red {by_count(r, 'marbles')} and {b} blue {by_count(b, 'marbles')}; "
                f"the probability of drawing a red marble, expressed as a fraction, is not {чуж}/{n}: it is {r}/{n}.")
    return (f"a bag holds {r} red {by_count(r, 'marbles')} and {b} blue {by_count(b, 'marbles')}. "
            f"what is the probability of drawing a red marble, expressed as a fraction? {r} red and {b} blue make {n}: {r}/{n}.")


# ---------- 7. # quarters of ----------
def четверти(шаг, i):
    k = (1, 2, 3)[(шаг + i) % 3]
    q = 3 + (шаг * 3 + i) % 9
    часть, целое = k * q, 4 * q
    слово = ("one quarter", "two quarters", "three quarters")[k - 1]
    ру_слово = ("четверть", "две четверти", "три четверти")[k - 1]
    ф = (шаг + i) % 4
    if ф == 0:
        return f"if {часть} is {слово} of the class, the class has {целое} pupils: {часть} ÷ {k} × 4 = {целое}."
    if ф == 1:
        return f"если {часть} — это {ру_слово} класса, в классе {целое} {ру('ученик', целое)}: {часть} ÷ {k} × 4 = {целое}."
    if ф == 2:
        return f"if {часть} is {слово} of the class, the class does not have {целое + 4} pupils: it has {целое}."
    return f"if {часть} is {слово} of the class, how many pupils does the class have? {часть} ÷ {k} × 4 = {целое}."


# ---------- 8. originally / missing / people on ----------
def дополнение(шаг, i):
    было = 10 + (шаг * 7 + i * 3) % 40
    ушло = 1 + (шаг * 3 + i) % 9
    осталось = было - ушло
    род = (шаг + i) % 3
    ф = (шаг + i) % 4
    if род == 0:
        if ф == 0:
            return f"there were originally {было} cars in the lot and {ушло} drove away; {осталось} {by_count(осталось, 'cars')} remain: {было} − {ушло} = {осталось}."
        if ф == 1:
            return f"на стоянке изначально было {было} {ру('машина', было)}, {ушло} уехали; осталось {осталось} {ру('машина', осталось)}: {было} − {ушло} = {осталось}."
        if ф == 2:
            return f"there were originally {было} cars in the lot and {ушло} drove away; {осталось + 1} cars do not remain: {осталось} remain."
        return f"if there were originally {было} cars in the lot and {ушло} drove away, how many cars remain? {было} − {ушло} = {осталось}."
    if род == 1:
        if ф == 0:
            return f"the set has {было} pieces and {осталось} are in the box; {ушло} {by_count(ушло, 'pieces')} {'are' if ушло != 1 else 'is'} missing: {было} − {осталось} = {ушло}."
        if ф == 1:
            return f"в наборе {было} {ру('деталь', было)}, в коробке {осталось} {ру('деталь', осталось)}; не хватает {ушло} {ру('деталь', ушло)}: {было} − {осталось} = {ушло}."
        if ф == 2:
            return f"the set has {было} pieces and {осталось} are in the box; {ушло + 1} pieces are not missing: {ушло} {'are' if ушло != 1 else 'is'} missing."
        return f"the set has {было} pieces and {осталось} are in the box. how many pieces are missing? {было} − {осталось} = {ушло}."
    if ф == 0:
        return f"there were {было} people on the bus and {ушло} got off; {осталось} people are on the bus now: {было} − {ушло} = {осталось}."
    if ф == 1:
        return f"в автобусе было {было} {ру('человек', было)}, {ушло} вышли; теперь в автобусе {осталось} {ру('человек', осталось)}: {было} − {ушло} = {осталось}."
    if ф == 2:
        return f"there were {было} people on the bus and {ушло} got off; the number of people on the bus now is not {осталось + 1}: it is {осталось}."
    return f"if there were {было} people on the bus and {ушло} got off, how many people are on the bus now? {было} − {ушло} = {осталось}."


СЕМЕЙСТВА = (сумма, температура, процент, фунты, глубина, вероятность, четверти, дополнение)


def pass_groups(шаг):
    return [[семья(шаг, i) for i in range(16)] for семья in СЕМЕЙСТВА]


def main():
    emit_grouped(ЦЕЛЬ, pass_groups)


if __name__ == "__main__":
    main()
