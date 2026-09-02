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
# РОД И РОДИТЕЛЬНЫЙ — ТАБЛИЦЕЙ ГЕНЕРАТОРА (пакет держит именительный; формы
# падежей держат таблицы генераторов, суды читают их той же рукой): «у
# Веры было», «Вера отдала» — третий слой дал рамки с падежом и глаголом.
ЖЕНСКИЕ_RU = {n.capitalize() for n, ф in _RU["person_forms"].items() if ф["gender"] == "f"}
РОДИТЕЛЬНЫЙ_RU = {n.capitalize(): ф["gen"].capitalize() for n, ф in _RU["person_forms"].items()}
assert set(ИМЕНА_RU) <= set(РОДИТЕЛЬНЫЙ_RU)


# ЧЕРЕДОВАНИЕ ОСНОВЫ НАЗВАНО ПОИМЁННО: «испёк → испекла» правилом «+а» не дать.
НЕПРАВИЛЬНЫЕ_RU = {"испёк": "испекла", "нашёл": "нашла"}


def гл(имя, прошедшее):
    """Глагол прошедшего времени по роду имени: «отдал» → «отдала»."""
    if имя not in ЖЕНСКИЕ_RU:
        return прошедшее
    return НЕПРАВИЛЬНЫЕ_RU.get(прошедшее, прошедшее + "а")


def кого(имя):
    return РОДИТЕЛЬНЫЙ_RU[имя]
ВЕЩИ = (("pens", "ручка"), ("books", "книга"), ("apples", "яблоко"), ("coins", "монета"), ("cards", "карта"))


def ч(n):
    return str(n).replace("-", "−")


def ру(вещь, n):
    return rugram.форма(вещь, n)


def _ру_вопрос(шаг, i):
    """RU-форма чередуется: повествование / вопрос с ответом-уравнением (М-146:
    у каждой рамки на каждом языке обязана быть вопросная поверхность)."""
    return (шаг * 7 + i) % 2 == 1


# ---------- 1. total number of ----------
def п_сумма(шаг, i):
    """ПАРАМЕТРЫ СЕМЕЙСТВА — ОДНА ФУНКЦИЯ на показ, стенд и суд: имена, вещь,
    числа и ответ выводятся здесь, а показы и стенд лишь пишут их."""
    a, b = ИМЕНА_EN[(шаг + i) % len(ИМЕНА_EN)], ИМЕНА_EN[(шаг + i * 3 + 1) % len(ИМЕНА_EN)]
    if b == a:
        b = ИМЕНА_EN[(ИМЕНА_EN.index(a) + 1) % len(ИМЕНА_EN)]
    ра, рб = ИМЕНА_RU[(шаг + i) % len(ИМЕНА_RU)], ИМЕНА_RU[(шаг + i * 3 + 1) % len(ИМЕНА_RU)]
    if рб == ра:
        рб = ИМЕНА_RU[(ИМЕНА_RU.index(ра) + 1) % len(ИМЕНА_RU)]
    en, вещь = ВЕЩИ[(шаг + i) % len(ВЕЩИ)]
    x, y = 2 + (шаг * 5 + i * 3) % 12, 2 + (шаг * 7 + i) % 9
    return dict(a=a, b=b, ра=ра, рб=рб, en=en, вещь=вещь, x=x, y=y, ответ=x + y)


def сумма(шаг, i):
    п = п_сумма(шаг, i)
    a, b, ра, рб, en, вещь, x, y, s = п["a"], п["b"], п["ра"], п["рб"], п["en"], п["вещь"], п["x"], п["y"], п["ответ"]
    ф = (шаг + i) % 4
    if ф == 0:
        return f"{a} has {x} {by_count(x, en)} and {b} has {y} {by_count(y, en)}; the total number of {en} is {s}: {x} + {y} = {s}."
    if ф == 1 and _ру_вопрос(шаг, i):
        return f"если {ра} имеет {x} {ру(вещь, x)}, а {рб} имеет {y} {ру(вещь, y)}, сколько {ру(вещь, 5)} у них всего? {x} + {y} = {s}."
    if ф == 1:
        return f"{ра} имеет {x} {ру(вещь, x)}, {рб} имеет {y} {ру(вещь, y)}; всего у них {s} {ру(вещь, s)}: {x} + {y} = {s}."
    if ф == 2:
        return f"{a} has {x} {by_count(x, en)} and {b} has {y} {by_count(y, en)}; the total number of {en} is not {s + 1}: it is {s}."
    # ОТВЕТ НАЧИНАЕТСЯ ВЕЛИЧИНАМИ ВОПРОСА В ИХ ПОРЯДКЕ (дом пары: величины
    # вопроса суть начальный отрезок величин ответа) и кончается итогом.
    return f"{a} has {x} {by_count(x, en)} and {b} has {y} {by_count(y, en)}. what's the total number of {en}? {x} + {y} = {s}."


# ---------- 2. temperature in degrees ----------
def п_температура(шаг, i):
    t0 = -6 + (шаг * 3 + i) % 15
    d = 2 + (шаг + i * 5) % 12
    падение = (шаг + i) % 2 == 0
    return dict(t0=t0, d=d, падение=падение, ответ=t0 - d if падение else t0 + d)


def температура(шаг, i):
    п = п_температура(шаг, i)
    t0, d, падение, t1 = п["t0"], п["d"], п["падение"], п["ответ"]
    ф = (шаг + i) % 4
    if ф == 0:
        return (f"the temperature was {ч(t0)} {by_count(abs(t0), 'degrees')} and {'fell' if падение else 'rose'} by {d} {by_count(d, 'degrees')}; "
                f"the temperature in degrees is now {ч(t1)}: {ч(t0)} {'−' if падение else '+'} {d} = {ч(t1)}.")
    if ф == 1 and _ру_вопрос(шаг, i):
        return (f"если температура была {ч(t0)} {ру('градус', abs(t0))} и {'упала' if падение else 'поднялась'} на {d} {ру('градус', d)}, "
                f"какова температура теперь? {ч(t0)} {'−' if падение else '+'} {d} = {ч(t1)}.")
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
def п_процент(шаг, i):
    всего = (20, 25, 40, 50, 60, 80, 100)[(шаг + i) % 7]
    доли = [k for k in range(1, всего) if (k * 100) % всего == 0]
    часть = доли[(шаг * 3 + i) % len(доли)]
    return dict(всего=всего, часть=часть, ответ=часть * 100 // всего)


def процент(шаг, i):
    п = п_процент(шаг, i)
    всего, часть, p = п["всего"], п["часть"], п["ответ"]
    ф = (шаг + i) % 4
    if ф == 0:
        return (f"the class has {всего} pupils and {часть} of them are girls; the percentage of girls is {p} %: "
                f"{часть} ÷ {всего} × 100 = {p}.")
    if ф == 1 and _ру_вопрос(шаг, i):
        return (f"если в классе {всего} {ру('ученик', всего)}, из них {часть} — {ру('девочка', часть)}, какова доля девочек в процентах? "
                f"{всего} {ру('ученик', всего)} и {часть} {ру('девочка', часть)}: {часть} ÷ {всего} × 100 = {p}.")
    if ф == 1:
        return (f"в классе {всего} {ру('ученик', всего)}, из них {часть} — {ру('девочка', часть)}; доля девочек — {p} %: "
                f"{часть} ÷ {всего} × 100 = {p}.")
    if ф == 2:
        return (f"the class has {всего} pupils and {часть} of them are girls; the percentage of girls is not {p + 5} %: it is {p} %.")
    return (f"the class has {всего} pupils and {часть} of them are girls. what percentage of the class are girls? "
            f"{всего} pupils and {часть} girls: {часть} ÷ {всего} × 100 = {p} %.")


# ---------- 4. weight in pounds ----------
def п_фунты(шаг, i):
    ф_ = 1 + (шаг * 3 + i) % 9
    return dict(унц=ф_ * 16, ответ=ф_)


def фунты(шаг, i):
    п = п_фунты(шаг, i)
    унц, ф_ = п["унц"], п["ответ"]
    ф = (шаг + i) % 4
    if ф == 0:
        return f"the parcel weighs {унц} ounces and a pound is 16 ounces; the weight in pounds is {ф_}: {унц} ÷ 16 = {ф_}."
    if ф == 1 and _ру_вопрос(шаг, i):
        return f"если посылка весит {унц} {ру('унция', унц)}, а в фунте 16 унций, каков вес в фунтах? {унц} ÷ 16 = {ф_}."
    if ф == 1:
        return (f"посылка весит {унц} {ру('унция', унц)}, а в фунте 16 унций; вес в фунтах — {ф_} {ру('фунт', ф_)}: "
                f"{унц} ÷ 16 = {ф_}.")
    if ф == 2:
        return f"the parcel weighs {унц} ounces and a pound is 16 ounces; the weight in pounds is not {ф_ + 1}: it is {ф_}."
    return f"the parcel weighs {унц} ounces and a pound is 16 ounces. what is the weight in pounds? {унц} ounces: {унц} ÷ 16 = {ф_}."


# ---------- 5. water depth ----------
def п_глубина(шаг, i):
    w, l = 2 + (шаг + i) % 5, 2 + (шаг * 2 + i * 3) % 6
    h = 1 + (шаг * 5 + i) % 6
    return dict(w=w, l=l, v=w * l * h, ответ=h)


def глубина(шаг, i):
    п = п_глубина(шаг, i)
    w, l, v, h = п["w"], п["l"], п["v"], п["ответ"]
    ф = (шаг + i) % 4
    if ф == 0:
        return (f"the tank is {w} feet wide and {l} feet long and holds {v} cubic feet of water; "
                f"the tank's water depth is {h} {by_count(h, 'feet')}: {v} ÷ ({w} × {l}) = {h}.")
    if ф == 1 and _ру_вопрос(шаг, i):
        return (f"если бак шириной {w} {ру('фут', w)} и длиной {l} {ру('фут', l)} вмещает {v} кубических футов воды, "
                f"какова глубина воды в баке? {w} на {l} при {v}: {v} ÷ ({w} × {l}) = {h}.")
    if ф == 1:
        return (f"бак шириной {w} {ру('фут', w)} и длиной {l} {ру('фут', l)} вмещает {v} кубических футов воды; "
                f"глубина воды в баке — {h} {ру('фут', h)}: {v} ÷ ({w} × {l}) = {h}.")
    if ф == 2:
        return (f"the tank is {w} feet wide and {l} feet long and holds {v} cubic feet of water; "
                f"the tank's water depth is not {h + 1} feet: it is {h} {by_count(h, 'feet')}.")
    return (f"the tank is {w} feet wide and {l} feet long and holds {v} cubic feet of water. "
            f"what is the tank's water depth? {w} by {l} holding {v}: {v} ÷ ({w} × {l}) = {h} {by_count(h, 'feet')}.")


# ---------- 6. probability expressed as ----------
def п_вероятность(шаг, i):
    r, b = 1 + (шаг + i) % 6, 1 + (шаг * 3 + i * 2) % 7
    return dict(r=r, b=b, n=r + b, ответ=f"{r}/{r + b}")


def вероятность(шаг, i):
    п = п_вероятность(шаг, i)
    r, b, n = п["r"], п["b"], п["n"]
    ф = (шаг + i) % 4
    if ф == 0:
        return (f"a bag holds {r} red {by_count(r, 'marbles')} and {b} blue {by_count(b, 'marbles')}; "
                f"the probability of drawing a red marble, expressed as a fraction, is {r}/{n}: {r} red out of {n}.")
    if ф == 1 and _ру_вопрос(шаг, i):
        return (f"если в мешке {r} {ру('шар', r)} красных и {b} {ру('шар', b)} синих, какова вероятность вынуть красный шар, "
                f"выраженная дробью? {r} красных и {b} синих: {r}/{n}.")
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
def п_четверти(шаг, i):
    k = (1, 2, 3)[(шаг + i) % 3]
    q = 3 + (шаг * 3 + i) % 9
    return dict(k=k, часть=k * q, ответ=4 * q,
                слово=("one quarter", "two quarters", "three quarters")[k - 1],
                ру_слово=("четверть", "две четверти", "три четверти")[k - 1])


def четверти(шаг, i):
    п = п_четверти(шаг, i)
    k, часть, целое, слово, ру_слово = п["k"], п["часть"], п["ответ"], п["слово"], п["ру_слово"]
    ф = (шаг + i) % 4
    if ф == 0:
        return f"if {часть} is {слово} of the class, the class has {целое} pupils: {часть} ÷ {k} × 4 = {целое}."
    if ф == 1 and _ру_вопрос(шаг, i):
        return f"если {часть} — это {ру_слово} класса, сколько учеников в классе? {часть} ÷ {k} × 4 = {целое}."
    if ф == 1:
        return f"если {часть} — это {ру_слово} класса, в классе {целое} {ру('ученик', целое)}: {часть} ÷ {k} × 4 = {целое}."
    if ф == 2:
        return f"if {часть} is {слово} of the class, the class does not have {целое + 4} pupils: it has {целое}."
    return f"if {часть} is {слово} of the class, how many pupils does the class have? {часть} ÷ {k} × 4 = {целое}."


# ---------- 8. originally / missing / people on ----------
def п_дополнение(шаг, i):
    было = 10 + (шаг * 7 + i * 3) % 40
    ушло = 1 + (шаг * 3 + i) % 9
    род = (шаг + i) % 3
    return dict(было=было, ушло=ушло, род=род,
                ответ=(было - ушло) if род != 1 else ушло)


def дополнение(шаг, i):
    п = п_дополнение(шаг, i)
    было, ушло, род = п["было"], п["ушло"], п["род"]
    осталось = было - ушло
    ф = (шаг + i) % 4
    if род == 0:
        if ф == 0:
            return f"there were originally {было} cars in the lot and {ушло} drove away; {осталось} {by_count(осталось, 'cars')} remain: {было} − {ушло} = {осталось}."
        if ф == 1 and _ру_вопрос(шаг, i):
            return f"если на стоянке изначально было {было} {ру('машина', было)}, а {ушло} уехали, сколько машин осталось? {было} − {ушло} = {осталось}."
        if ф == 1:
            return f"на стоянке изначально было {было} {ру('машина', было)}, {ушло} уехали; осталось {осталось} {ру('машина', осталось)}: {было} − {ушло} = {осталось}."
        if ф == 2:
            return f"there were originally {было} cars in the lot and {ушло} drove away; {осталось + 1} cars do not remain: {осталось} remain."
        return f"if there were originally {было} cars in the lot and {ушло} drove away, how many cars remain? {было} − {ушло} = {осталось}."
    if род == 1:
        if ф == 0:
            return f"the set has {было} pieces and {осталось} are in the box; {ушло} {by_count(ушло, 'pieces')} {'are' if ушло != 1 else 'is'} missing: {было} − {осталось} = {ушло}."
        if ф == 1 and _ру_вопрос(шаг, i):
            return f"если в наборе {было} {ру('деталь', было)}, а в коробке {осталось} {ру('деталь', осталось)}, сколько деталей не хватает? {было} − {осталось} = {ушло}."
        if ф == 1:
            return f"в наборе {было} {ру('деталь', было)}, в коробке {осталось} {ру('деталь', осталось)}; не хватает {ушло} {ру('деталь', ушло)}: {было} − {осталось} = {ушло}."
        if ф == 2:
            return f"the set has {было} pieces and {осталось} are in the box; {ушло + 1} pieces are not missing: {ушло} {'are' if ушло != 1 else 'is'} missing."
        return f"the set has {было} pieces and {осталось} are in the box. how many pieces are missing? {было} − {осталось} = {ушло}."
    if ф == 0:
        return f"there were {было} people on the bus and {ушло} got off; {осталось} people are on the bus now: {было} − {ушло} = {осталось}."
    if ф == 1 and _ру_вопрос(шаг, i):
        return f"если в автобусе было {было} {ру('человек', было)}, а {ушло} вышли, сколько человек в автобусе теперь? {было} − {ушло} = {осталось}."
    if ф == 1:
        return f"в автобусе было {было} {ру('человек', было)}, {ушло} вышли; теперь в автобусе {осталось} {ру('человек', осталось)}: {было} − {ушло} = {осталось}."
    if ф == 2:
        return f"there were {было} people on the bus and {ушло} got off; the number of people on the bus now is not {осталось + 1}: it is {осталось}."
    return f"if there were {было} people on the bus and {ушло} got off, how many people are on the bus now? {было} − {ушло} = {осталось}."


# ---------- 9. whole population lives in ----------
def п_население(шаг, i):
    доля = (2, 4, 5, 10)[(шаг + i) % 4]
    часть = 100 * (2 + (шаг * 3 + i) % 9)
    return dict(доля=доля, всего=часть * доля, ответ=часть,
                слово=("half", "a quarter", "a fifth", "a tenth")[(2, 4, 5, 10).index(доля)],
                ру_слово=("половина", "четверть", "пятая часть", "десятая часть")[(2, 4, 5, 10).index(доля)])


def население(шаг, i):
    п = п_население(шаг, i)
    всего, доля, часть, слово, ру_слово = п["всего"], п["доля"], п["ответ"], п["слово"], п["ру_слово"]
    ф = (шаг + i) % 4
    if ф == 0:
        return f"the town has {всего} people and {слово} of the whole population lives in the centre; {часть} people live in the centre: {всего} ÷ {доля} = {часть}."
    if ф == 1 and _ру_вопрос(шаг, i):
        return f"если в городе {всего} {ру('человек', всего)}, и {ру_слово} всего населения живёт в центре, сколько человек живёт в центре? {всего} ÷ {доля} = {часть}."
    if ф == 1:
        return f"в городе {всего} {ру('человек', всего)}, и {ру_слово} всего населения живёт в центре; в центре живёт {часть} {ру('человек', часть)}: {всего} ÷ {доля} = {часть}."
    if ф == 2:
        return f"the town has {всего} people and {слово} of the whole population lives in the centre; the number living in the centre is not {часть + 100}: it is {часть}."
    return f"if the town has {всего} people and {слово} of the whole population lives in the centre, how many people live in the centre? {всего} people: {всего} ÷ {доля} = {часть}."


# ---------- 10. number of boys on ----------
def п_команда(шаг, i):
    м, д = 3 + (шаг * 3 + i) % 10, 2 + (шаг + i * 5) % 9
    return dict(м=м, д=д, ответ=м + д)


def команда(шаг, i):
    п = п_команда(шаг, i)
    м, д, s = п["м"], п["д"], п["ответ"]
    ф = (шаг + i) % 4
    if ф == 0:
        return f"the number of boys on the team is {м} and the number of girls is {д}; the team has {s} players: {м} + {д} = {s}."
    if ф == 1 and _ру_вопрос(шаг, i):
        return f"если в команде {м} {ру('мальчик', м)} и {д} {ру('девочка', д)}, сколько человек в команде? {м} + {д} = {s}."
    if ф == 1:
        return f"в команде {м} {ру('мальчик', м)} и {д} {ру('девочка', д)}; всего в команде {s} {ру('человек', s)}: {м} + {д} = {s}."
    if ф == 2:
        return f"the number of boys on the team is {м} and the number of girls is {д}; the team does not have {s + 1} players: it has {s}."
    return f"if the number of boys on the team is {м} and the number of girls is {д}, how many players does the team have? {м} + {д} = {s}."


# ---------- 11. three times as much ----------
def п_кратно(шаг, i):
    k = (2, 3, 4)[(шаг + i) % 3]
    цена = 1000 * (5 + (шаг * 7 + i * 3) % 26)
    return dict(k=k, цена=цена, ответ=k * цена, слово=("twice", "three times", "four times")[k - 2],
                ру_слово=("вдвое", "втрое", "вчетверо")[k - 2])


def кратно(шаг, i):
    п = п_кратно(шаг, i)
    k, цена, дом, слово, ру_ = п["k"], п["цена"], п["ответ"], п["слово"], п["ру_слово"]
    ф = (шаг + i) % 4
    if ф == 0:
        return f"the car cost {цена} dollars and the house cost {слово} as much as the car; the house cost {дом} dollars: {цена} × {k} = {дом}."
    if ф == 1 and _ру_вопрос(шаг, i):
        return f"если машина стоила {цена} {ру('доллар', цена)}, а дом стоил {ру_} дороже машины, сколько стоил дом? {цена} {ру('доллар', цена)}: {цена} × {k} = {дом}."
    if ф == 1:
        return f"машина стоила {цена} {ру('доллар', цена)}, а дом стоил {ру_} дороже машины; дом стоил {дом} {ру('доллар', дом)}: {цена} × {k} = {дом}."
    if ф == 2:
        return f"the car cost {цена} dollars and the house cost {слово} as much as the car; the house did not cost {дом + цена} dollars: it cost {дом}."
    return f"if the car cost {цена} dollars and the house cost {слово} as much as the car, how much did the house cost? {цена} × {k} = {дом} dollars."


# ---------- 12. final design ----------
def п_проект(шаг, i):
    старт = 4 + (шаг * 3 + i) % 12
    k = 2 + (шаг + i) % 2
    минус = 1 + (шаг * 5 + i) % 5
    return dict(старт=старт, k=k, минус=минус, ответ=старт * k - минус)


def проект(шаг, i):
    п = п_проект(шаг, i)
    старт, k, минус, итог = п["старт"], п["k"], п["минус"], п["ответ"]
    слово = "doubled" if k == 2 else "tripled"
    ру_ = "удвоили" if k == 2 else "утроили"
    ф = (шаг + i) % 4
    if ф == 0:
        return f"the design started with {старт} panels, was {слово} and then reduced by {минус}; the final design has {итог} panels: {старт} × {k} − {минус} = {итог}."
    if ф == 1 and _ру_вопрос(шаг, i):
        return f"если проект начался с {старт} {ру('панель', старт)}, его {ру_} и потом убавили на {минус}, сколько панелей в итоговом проекте? {старт} × {k} − {минус} = {итог}."
    if ф == 1:
        return f"проект начался с {старт} {ру('панель', старт)}, его {ру_} и потом убавили на {минус}; в итоговом проекте {итог} {ру('панель', итог)}: {старт} × {k} − {минус} = {итог}."
    if ф == 2:
        return f"the design started with {старт} panels, was {слово} and then reduced by {минус}; the final design does not have {итог + минус} panels: it has {итог}."
    return f"if the design started with {старт} panels, was {слово} and then reduced by {минус}, how many panels does the final design have? {старт} × {k} − {минус} = {итог}."


# ---------- 13. circumference of the earth ----------
def п_окружность(шаг, i):
    скорость = 100 * (4 + (шаг * 3 + i) % 9)
    часы = 10 + (шаг + i * 7) % 40
    return dict(скорость=скорость, ответ=часы, длина=скорость * часы)


def окружность(шаг, i):
    п = п_окружность(шаг, i)
    L, v, t = п["длина"], п["скорость"], п["ответ"]
    ф = (шаг + i) % 4
    if ф == 0:
        return f"the circumference of the earth is taken as {L} miles and the plane flies {v} miles per hour; the flight around the earth takes {t} hours: {L} ÷ {v} = {t}."
    if ф == 1 and _ру_вопрос(шаг, i):
        return f"если длину окружности земли берут за {L} {ру('миля', L)}, а самолёт летит {v} {ру('миля', v)} в час, сколько часов занимает полёт вокруг земли? {L} ÷ {v} = {t}."
    if ф == 1:
        return f"длину окружности земли берут за {L} {ру('миля', L)}, самолёт летит {v} {ру('миля', v)} в час; полёт вокруг земли занимает {t} {ру('час', t)}: {L} ÷ {v} = {t}."
    if ф == 2:
        return f"the circumference of the earth is taken as {L} miles and the plane flies {v} miles per hour; the flight around the earth does not take {t + 1} hours: it takes {t}."
    return f"if the circumference of the earth is {L} miles and the plane flies {v} miles per hour, how many hours does the flight around the earth take? {L} ÷ {v} = {t}."


# ---------- 14. ropes: total and average ----------
def п_верёвки(шаг, i):
    n = 2 + (шаг + i) % 4
    среднее = 3 + (шаг * 3 + i) % 12
    return dict(n=n, ответ=среднее, всего=n * среднее)


def верёвки(шаг, i):
    п = п_верёвки(шаг, i)
    n, a, всего = п["n"], п["ответ"], п["всего"]
    ф = (шаг + i) % 4
    if ф == 0:
        return f"the {n} ropes had a total length of {всего} meters; the average rope is {a} meters long: {всего} ÷ {n} = {a}."
    if ф == 1 and _ру_вопрос(шаг, i):
        return f"если общая длина верёвок {всего} {ру('метр', всего)}, а верёвок {n}, какова длина средней верёвки? {всего} ÷ {n} = {a}."
    if ф == 1:
        return f"{n} {ру('верёвка', n)} имели общую длину {всего} {ру('метр', всего)}; средняя верёвка длиной {a} {ру('метр', a)}: {всего} ÷ {n} = {a}."
    if ф == 2:
        return f"the {n} ropes had a total length of {всего} meters; the average rope is not {a + 1} meters long: it is {a} meters."
    return f"if the total length of the ropes is {всего} meters and there are {n} ropes, how long is the average rope? {всего} ÷ {n} = {a} meters."


# ---------- 15. together A, B and C ----------
def п_трое(шаг, i):
    a = 3 + (шаг * 3 + i) % 10
    больше = 1 + (шаг + i * 3) % 6
    k = 2 + (шаг + i) % 2
    return dict(a=a, больше=больше, k=k, b=a + больше, c=k * a, ответ=a + (a + больше) + k * a)


def трое(шаг, i):
    п = п_трое(шаг, i)
    a, б, k, b, c, s = п["a"], п["больше"], п["k"], п["b"], п["c"], п["ответ"]
    x, y, z = ИМЕНА_EN[(шаг + i) % len(ИМЕНА_EN)], ИМЕНА_EN[(шаг + i + 1) % len(ИМЕНА_EN)], ИМЕНА_EN[(шаг + i + 2) % len(ИМЕНА_EN)]
    рx, рy, рz = ИМЕНА_RU[(шаг + i) % len(ИМЕНА_RU)], ИМЕНА_RU[(шаг + i + 1) % len(ИМЕНА_RU)], ИМЕНА_RU[(шаг + i + 2) % len(ИМЕНА_RU)]
    слово = "twice" if k == 2 else "three times"
    ру_ = "вдвое" if k == 2 else "втрое"
    ф = (шаг + i) % 4
    if ф == 0:
        return f"{x} has {a} books, {y} has {б} more books than {x}, and {z} has {слово} as many books as {x}; together {x}, {y} and {z} have {s} books: {a} + ({a} + {б}) + {k} × {a} = {s}."
    if ф == 1 and _ру_вопрос(шаг, i):
        return f"если {рx} имеет {a} {ру('книга', a)}, {рy} имеет на {б} {ру('книга', б)} больше, чем {рx}, а {рz} имеет {ру_} больше книг, чем {рx}, сколько книг у них вместе? {a} + ({a} + {б}) + {k} × {a} = {s}."
    if ф == 1:
        return f"{рx} имеет {a} {ру('книга', a)}, {рy} имеет на {б} {ру('книга', б)} больше, чем {рx}, а {рz} имеет {ру_} больше книг, чем {рx}; вместе у них {s} {ру('книга', s)}: {a} + ({a} + {б}) + {k} × {a} = {s}."
    if ф == 2:
        return f"{x} has {a} books, {y} has {б} more books than {x}, and {z} has {слово} as many books as {x}; together they do not have {s + 1} books: they have {s}."
    return f"if {x} has {a} books, {y} has {б} more books than {x}, and {z} has {слово} as many books as {x}, how many books do they have together? {a} + ({a} + {б}) + {k} × {a} = {s}."


# ---------- 16. makes # candles: rate × time ----------
def п_ставка(шаг, i):
    в_час = 2 + (шаг * 3 + i) % 9
    часы = 2 + (шаг + i * 3) % 7
    return dict(в_час=в_час, часы=часы, ответ=в_час * часы)


def ставка(шаг, i):
    п = п_ставка(шаг, i)
    r, t, s = п["в_час"], п["часы"], п["ответ"]
    имя, ру_имя = ИМЕНА_EN[(шаг + i) % len(ИМЕНА_EN)], ИМЕНА_RU[(шаг + i) % len(ИМЕНА_RU)]
    ф = (шаг + i) % 4
    if ф == 0:
        return f"{имя} makes {r} candles an hour and works {t} hours; {имя} makes {s} candles: {r} × {t} = {s}."
    if ф == 1 and _ру_вопрос(шаг, i):
        return f"если {ру_имя} делает {r} {ру('свеча', r)} в час и работает {t} {ру('час', t)}, сколько свечей делает {ру_имя}? {r} × {t} = {s}."
    if ф == 1:
        return f"{ру_имя} делает {r} {ру('свеча', r)} в час и работает {t} {ру('час', t)}; {ру_имя} делает {s} {ру('свеча', s)}: {r} × {t} = {s}."
    if ф == 2:
        return f"{имя} makes {r} candles an hour and works {t} hours; {имя} does not make {s + r} candles: {имя} makes {s}."
    return f"if {имя} makes {r} candles an hour and works {t} hours, how many candles does {имя} make? {r} × {t} = {s}."


# ---------- 17. post-it notes: several subtractions ----------
def п_листки(шаг, i):
    было = 60 + (шаг * 7 + i * 3) % 40
    раз = 5 + (шаг + i) % 12
    два = 3 + (шаг * 3 + i) % 10
    return dict(было=было, раз=раз, два=два, ответ=было - раз - два)


def листки(шаг, i):
    п = п_листки(шаг, i)
    было, раз, два, s = п["было"], п["раз"], п["два"], п["ответ"]
    имя, ру_имя = ИМЕНА_EN[(шаг + i) % len(ИМЕНА_EN)], ИМЕНА_RU[(шаг + i) % len(ИМЕНА_RU)]
    ф = (шаг + i) % 4
    if ф == 0:
        return f"{имя} had {было} post-it notes, used {раз} on the fridge and {два} on the door; {имя} has {s} post-it notes left: {было} − {раз} − {два} = {s}."
    if ф == 1 and _ру_вопрос(шаг, i):
        return f"если у {кого(ру_имя)} было {было} {ру('листок', было)}, {раз} ушли на холодильник и {два} на дверь, сколько листков осталось? {было} − {раз} − {два} = {s}."
    if ф == 1:
        return f"у {кого(ру_имя)} было {было} {ру('листок', было)}, {раз} ушли на холодильник и {два} на дверь; осталось {s} {ру('листок', s)}: {было} − {раз} − {два} = {s}."
    if ф == 2:
        return f"{имя} had {было} post-it notes, used {раз} on the fridge and {два} on the door; {имя} does not have {s + два} post-it notes left: {имя} has {s}."
    return f"if {имя} had {было} post-it notes, used {раз} on the fridge and {два} on the door, how many post-it notes does {имя} have left? {было} − {раз} − {два} = {s}."


# ---------- SVAMP: how many more did A V1 than V2 ----------
def п_разница(шаг, i):
    x, y = 4 + (шаг * 3 + i) % 12, 2 + (шаг + i * 5) % 9
    if y >= x:
        y = x - 1
    return dict(x=x, y=y, ответ=x - y)


def разница(шаг, i):
    п = п_разница(шаг, i)
    x, y, d = п["x"], п["y"], п["ответ"]
    имя, ру_имя = ИМЕНА_EN[(шаг + i) % len(ИМЕНА_EN)], ИМЕНА_RU[(шаг + i) % len(ИМЕНА_RU)]
    ф = (шаг + i) % 4
    if ф == 0:
        return f"{имя} planted {x} trees in the morning and {y} trees in the afternoon; {имя} planted {d} more trees in the morning than in the afternoon: {x} − {y} = {d}."
    if ф == 1 and _ру_вопрос(шаг, i):
        return f"если {ру_имя} утром {гл(ру_имя, 'посадил')} {x} {ру('дерево', x)}, а днём {y} {ру('дерево', y)}, на сколько деревьев больше утром, чем днём? {x} − {y} = {d}."
    if ф == 1:
        return f"{ру_имя} утром {гл(ру_имя, 'посадил')} {x} {ру('дерево', x)}, а днём {y} {ру('дерево', y)}; утром на {d} {ру('дерево', d)} больше, чем днём: {x} − {y} = {d}."
    if ф == 2:
        return f"{имя} planted {x} trees in the morning and {y} trees in the afternoon; {имя} did not plant {d + 1} more trees in the morning than in the afternoon: {d} more."
    return f"if {имя} planted {x} trees in the morning and {y} trees in the afternoon, how many more trees did {имя} plant in the morning than in the afternoon? {x} − {y} = {d}."


# ---------- SVAMP: price, discount, how much to pay ----------
def п_скидка(шаг, i):
    цена = 20 + (шаг * 7 + i * 3) % 80
    скидка = 5 + (шаг + i) % 15
    return dict(цена=цена, скидка=скидка, ответ=цена - скидка)


def скидка(шаг, i):
    п = п_скидка(шаг, i)
    ц, с, п_ = п["цена"], п["скидка"], п["ответ"]
    ф = (шаг + i) % 4
    if ф == 0:
        return f"each pack costs {ц} dollars and there is a discount of {с} dollars on each pack; you have to pay {п_} dollars for each pack: {ц} − {с} = {п_}."
    if ф == 1 and _ру_вопрос(шаг, i):
        return f"если каждая пачка стоит {ц} {ру('доллар', ц)}, и на каждую пачку скидка {с} {ру('доллар', с)}, сколько надо заплатить за каждую пачку? {ц} − {с} = {п_}."
    if ф == 1:
        return f"каждая пачка стоит {ц} {ру('доллар', ц)}, и на каждую пачку скидка {с} {ру('доллар', с)}; за каждую пачку надо заплатить {п_} {ру('доллар', п_)}: {ц} − {с} = {п_}."
    if ф == 2:
        return f"each pack costs {ц} dollars and there is a discount of {с} dollars on each pack; you do not have to pay {ц} dollars for each pack: you pay {п_}."
    return f"if each pack costs {ц} dollars and there is a discount of {с} dollars on each pack, how much do you have to pay for each pack? {ц} dollars: {ц} − {с} = {п_} dollars."


# ---------- SVAMP: left / in all / altogether ----------
def п_всего(шаг, i):
    x, y = 3 + (шаг * 3 + i) % 12, 2 + (шаг + i * 5) % 9
    род = (шаг + i) % 3
    return dict(x=x, y=y, род=род, ответ=x + y if род != 2 else x - min(y, x - 1))


def всего(шаг, i):
    п = п_всего(шаг, i)
    x, y, род = п["x"], п["y"], п["род"]
    имя, ру_имя = ИМЕНА_EN[(шаг + i) % len(ИМЕНА_EN)], ИМЕНА_RU[(шаг + i) % len(ИМЕНА_RU)]
    en, вещь = ВЕЩИ[(шаг + i) % len(ВЕЩИ)]
    ф = (шаг + i) % 4
    if род == 2:
        y = min(y, x - 1)
        s = x - y
        if ф == 0:
            return f"{имя} had {x} {by_count(x, en)} and gave away {y}; {имя} has {s} {by_count(s, en)} left: {x} − {y} = {s}."
        if ф == 1 and _ру_вопрос(шаг, i):
            return f"если у {кого(ру_имя)} было {x} {ру(вещь, x)}, а {ру_имя} {гл(ру_имя, 'отдал')} {y}, сколько {ру(вещь, 5)} осталось? {x} {ру(вещь, x)}: {x} − {y} = {s}."
        if ф == 1:
            return f"у {кого(ру_имя)} было {x} {ру(вещь, x)}, {ру_имя} {гл(ру_имя, 'отдал')} {y}; осталось {s} {ру(вещь, s)}: {x} − {y} = {s}."
        if ф == 2:
            return f"{имя} had {x} {by_count(x, en)} and gave away {y}; {имя} does not have {s + 1} {en} left: {имя} has {s}."
        return f"if {имя} had {x} {by_count(x, en)} and gave away {y}, how many {en} are left? {x} − {y} = {s}."
    s = x + y
    слово = "in all" if род == 0 else "altogether"
    if ф == 0:
        return f"{имя} has {x} {by_count(x, en)} in one box and {y} {by_count(y, en)} in another; {имя} has {s} {en} {слово}: {x} + {y} = {s}."
    if ф == 1 and _ру_вопрос(шаг, i):
        return f"если у {кого(ру_имя)} {x} {ру(вещь, x)} в одной коробке и {y} {ру(вещь, y)} в другой, сколько всего {ру(вещь, 5)} у {кого(ру_имя)}? {x} + {y} = {s}."
    if ф == 1:
        return f"у {кого(ру_имя)} {x} {ру(вещь, x)} в одной коробке и {y} {ру(вещь, y)} в другой; всего у {кого(ру_имя)} {s} {ру(вещь, s)}: {x} + {y} = {s}."
    if ф == 2:
        return f"{имя} has {x} {by_count(x, en)} in one box and {y} {by_count(y, en)} in another; {имя} does not have {s + 1} {en} {слово}: {имя} has {s}."
    return f"if {имя} has {x} {by_count(x, en)} in one box and {y} {by_count(y, en)} in another, how many {en} does {имя} have {слово}? {x} + {y} = {s}."


# ---------- SVAMP: how many groups of N ----------
def п_группы(шаг, i):
    n = 2 + (шаг + i) % 6
    групп = 2 + (шаг * 3 + i) % 9
    return dict(n=n, всего=n * групп, ответ=групп)


def группы(шаг, i):
    п = п_группы(шаг, i)
    n, всего_, g = п["n"], п["всего"], п["ответ"]
    ф = (шаг + i) % 4
    if ф == 0:
        return f"there are {всего_} pupils and they stand in groups of {n}; there are {g} groups: {всего_} ÷ {n} = {g}."
    if ф == 1 and _ру_вопрос(шаг, i):
        return f"если {всего_} {ру('ученик', всего_)} стоят группами по {n}, сколько групп? {всего_} ÷ {n} = {g}."
    if ф == 1:
        return f"{всего_} {ру('ученик', всего_)} стоят группами по {n}; групп {g}: {всего_} ÷ {n} = {g}."
    if ф == 2:
        return f"there are {всего_} pupils and they stand in groups of {n}; there are not {g + 1} groups: there are {g}."
    return f"if there are {всего_} pupils and they stand in groups of {n}, how many groups are there? {всего_} ÷ {n} = {g}."


# ======================= ТРЕТИЙ СЛОЙ (03.09): роды SVAMP по массе e9 и остаток g1 =======================
# Замер e9 (SVAMP-s1, 726 проб, поставочный FULL 46a6683b): (1) «how many more X … than …»
# ≈90 проб — крупнейший род; (2) «how many X did A V» при отвлекающих числах — отбор или
# остаток; (3) «how many pupils/boys are there in the class»; (4) «how much money …».
# Остаток g1 вне второго слоя: сдача (g1.38), прибыль при дробной цене (g1.58), завышение
# на процент (g1.45), половина и всего (g1.10). Закон каждой рамки — один на показ, стенд
# и суд; слова родов — таблицами здесь, суд читает их своим замкнутым множеством.

# --- 22. how many more … than …: четыре очертания одного закона d = x − y > 0 ---
БОЛЬШЕ_A = (  # одна вещь на двух случаях: (глагол прош., основа, вещь, вещь RU, глагол RU)
    ("received", "receive", "emails", "письмо", "получил"),
    ("ate", "eat", "cookies", "печенье", "съел"),
    ("played with", "play with", "kids", None, None),
)
КОГДА = (("in the morning", "in the afternoon", "утром", "днём"),
         ("on monday", "on tuesday", "в понедельник", "во вторник"))
БОЛЬШЕ_B = (  # две вещи одним делом: (глагол прош., основа, вещь1, вещь2, глагол RU, RU1, RU2)
    ("used", "use", "cups of flour", "cups of sugar", "использовал", ("чашка", " муки"), ("чашка", " сахара")),
    ("made", "make", "cakes", "pastries", "испёк", ("торт", ""), ("булочка", "")),
    ("read", "read", "pages of math", "pages of reading", "прочитал", ("страница", " математики"), ("страница", " чтения")),
    ("bought", "buy", "bottles of regular soda", "bottles of diet soda", None, None, None),
)
БОЛЬШЕ_C = (  # «there were A and B где»: (A, B, где, A RU, B RU, где RU)
    ("storks", "birds", "on the fence", "аист", "воробей", "на заборе"),
    ("red flowers", "white flowers", "in the garden", None, None, None),
)
БОЛЬШЕ_D = (  # деньги: (на что 1, на что 2, RU 1, RU 2)
    ("on the shirt", "on the hat", "на рубашку", "на шляпу"),
    ("on books", "on pens", "на книги", "на ручки"),
)


def п_больше(шаг, i):
    x = 4 + (шаг * 3 + i) % 12
    y = 2 + (шаг + i * 5) % (x - 2)
    очертание = (шаг + i) % 4
    k = (шаг * 3 + i) // 4
    ряд = (БОЛЬШЕ_A, БОЛЬШЕ_B, БОЛЬШЕ_C, БОЛЬШЕ_D)[очертание]
    return dict(x=x, y=y, очертание=очертание, слова=ряд[k % len(ряд)], ответ=x - y)


def больше(шаг, i):
    п = п_больше(шаг, i)
    x, y, d, оч = п["x"], п["y"], п["ответ"], п["очертание"]
    имя, ру_имя = ИМЕНА_EN[(шаг + i) % len(ИМЕНА_EN)], ИМЕНА_RU[(шаг + i) % len(ИМЕНА_RU)]
    ф = ((шаг + i) // 4 + шаг) % 4
    k = (шаг * 3 + i) // 4
    if оч == 0:
        г, г0, в, в_ру, г_ру = п["слова"]
        к1, к2, р1, р2 = КОГДА[k % len(КОГДА)]
        if ф == 0:
            return f"{имя} {г} {x} {в} {к1} and {y} {в} {к2}; {имя} {г} {d} more {в} {к1} than {к2}: {x} − {y} = {d}."
        if ф == 1 and _ру_вопрос(шаг, i) and в_ру is not None:
            return f"если {ру_имя} {гл(ру_имя, г_ру)} {р1} {x} {ру(в_ру, x)}, а {р2} {y} {ру(в_ру, y)}, на сколько {ру(в_ру, 5)} больше {р1}, чем {р2}? {x} {ру(в_ру, x)} {р1}: {x} − {y} = {d}."
        if ф == 1:
            if в_ру is None:
                return f"if {имя} {г} {x} {в} {к1} and {y} {в} {к2}, how many fewer {в} did {имя} {г0} {к2} than {к1}? {x} − {y} = {d}."
            return f"{ру_имя} {гл(ру_имя, г_ру)} {р1} {x} {ру(в_ру, x)}, а {р2} {y} {ру(в_ру, y)}; {р1} на {d} {ру(в_ру, d)} больше, чем {р2}: {x} − {y} = {d}."
        if ф == 2:
            return f"{имя} {г} {x} {в} {к1} and {y} {в} {к2}; {имя} did not {г0} {d + 1} more {в} {к1} than {к2}: {d} more."
        return f"if {имя} {г} {x} {в} {к1} and {y} {в} {к2}, how many more {в} did {имя} {г0} {к1} than {к2}? {x} − {y} = {d}."
    if оч == 1:
        г, г0, в1, в2, г_ру, р1, р2 = п["слова"]
        if ф == 0:
            return f"{имя} {г} {x} {в1} and {y} {в2}; {имя} {г} {d} more {в1} than {в2}: {x} − {y} = {d}."
        if ф == 1 and _ру_вопрос(шаг, i) and г_ру is not None:
            return f"если {ру_имя} {гл(ру_имя, г_ру)} {x} {ру(р1[0], x)}{р1[1]} и {y} {ру(р2[0], y)}{р2[1]}, на сколько {ру(р1[0], 5)}{р1[1]} больше, чем {ру(р2[0], 5)}{р2[1]}? {x} − {y} = {d}."
        if ф == 1:
            if г_ру is None:
                return f"if {имя} {г} {x} {в1} and {y} {в2}, how many fewer {в2} than {в1} did {имя} {г0}? {x} − {y} = {d}."
            return f"{ру_имя} {гл(ру_имя, г_ру)} {x} {ру(р1[0], x)}{р1[1]} и {y} {ру(р2[0], y)}{р2[1]}; {ру(р1[0], 5)}{р1[1]} на {d} больше, чем {ру(р2[0], 5)}{р2[1]}: {x} − {y} = {d}."
        if ф == 2:
            return f"{имя} {г} {x} {в1} and {y} {в2}; {имя} did not {г0} {d + 1} more {в1} than {в2}: {d} more."
        return f"if {имя} {г} {x} {в1} and {y} {в2}, how many more {в1} than {в2} did {имя} {г0}? {x} − {y} = {d}."
    if оч == 2:
        a, b, где, a_ру, b_ру, где_ру = п["слова"]
        if ф == 0:
            return f"there were {x} {a} and {y} {b} {где}; there were {d} more {a} than {b}: {x} − {y} = {d}."
        if ф == 1 and _ру_вопрос(шаг, i) and a_ру is not None:
            return f"если {где_ру} было {x} {ру(a_ру, x)} и {y} {ру(b_ру, y)}, на сколько {ру(a_ру, 5)} больше, чем {ру(b_ру, 5)}? {x} − {y} = {d}."
        if ф == 1:
            if a_ру is None:
                return f"if there were {x} {a} and {y} {b} {где}, how many fewer {b} than {a} were there? {x} − {y} = {d}."
            return f"{где_ру} было {x} {ру(a_ру, x)} и {y} {ру(b_ру, y)}; {ру(a_ру, 5)} на {d} больше, чем {ру(b_ру, 5)}: {x} − {y} = {d}."
        if ф == 2:
            return f"there were {x} {a} and {y} {b} {где}; there were not {d + 1} more {a} than {b}: {d} more."
        return f"if there were {x} {a} and {y} {b} {где}, how many more {a} than {b} were there? {x} − {y} = {d}."
    на1, на2, р1, р2 = п["слова"]
    if ф == 0:
        return f"{имя} spent {x} dollars {на1} and {y} dollars {на2}; {имя} spent {d} {by_count(d, 'dollars')} more {на1} than {на2}: {x} − {y} = {d}."
    if ф == 1 and _ру_вопрос(шаг, i):
        return f"если {ру_имя} {гл(ру_имя, 'потратил')} {x} {ру('доллар', x)} {р1} и {y} {ру('доллар', y)} {р2}, на сколько долларов больше потрачено {р1}, чем {р2}? {x} − {y} = {d}."
    if ф == 1:
        return f"{ру_имя} {гл(ру_имя, 'потратил')} {x} {ру('доллар', x)} {р1} и {y} {ру('доллар', y)} {р2}; {р1} на {d} {ру('доллар', d)} больше, чем {р2}: {x} − {y} = {d}."
    if ф == 2:
        return f"{имя} spent {x} dollars {на1} and {y} dollars {на2}; {имя} did not spend {d + 1} dollars more {на1} than {на2}: {d} more."
    return f"if {имя} spent {x} dollars {на1} and {y} dollars {на2}, how much more money did {имя} spend {на1} than {на2}? {x} − {y} = {d} {by_count(d, 'dollars')}."


# --- 23. отбор среди отвлекающих чисел: how many X did A V in the afternoon ---
ОТБОР = (  # (глагол прош., основа, вещь, глагол RU, вещь RU)
    ("received", "receive", "emails", "получил", "письмо"),
    ("sold", "sell", "books", "продал", "книга"),
    ("cut", "cut", "roses", "срезал", "роза"),
    ("found", "find", "bottle caps", None, None),
    ("played with", "play with", "kids", None, None),
)
СРОКИ = ("in the morning", "in the afternoon", "in the evening")
СРОКИ_RU = ("утром", "днём", "вечером")


def п_отбор(шаг, i):
    a = 3 + (шаг * 3 + i) % 12
    b = a + 1 + (шаг + i * 5) % 7
    c = 2 + (шаг + i * 3) % (a - 2)
    if c in (a, b):
        c = b + 2
    срок = (шаг + i) % 3
    return dict(a=a, b=b, c=c, срок=срок, слова=ОТБОР[(шаг * 3 + i) // 4 % len(ОТБОР)], ответ=(a, b, c)[срок])


def отбор(шаг, i):
    п = п_отбор(шаг, i)
    a, b, c, срок, отв = п["a"], п["b"], п["c"], п["срок"], п["ответ"]
    имя, ру_имя = ИМЕНА_EN[(шаг + i) % len(ИМЕНА_EN)], ИМЕНА_RU[(шаг + i) % len(ИМЕНА_RU)]
    г, г0, в, г_ру, в_ру = п["слова"]
    когда = СРОКИ[срок]
    ф = ((шаг + i) // 4 + шаг) % 4
    чужое = (a, b, c)[(срок + 1) % 3]
    if ф == 0:
        return f"{имя} {г} {a} {в} in the morning, {b} in the afternoon and {c} in the evening; {когда} {имя} {г} {отв} {в}."
    if ф == 1 and _ру_вопрос(шаг, i) and в_ру is not None:
        return f"если {ру_имя} {гл(ру_имя, г_ру)} утром {a} {ру(в_ру, a)}, днём {b} и вечером {c}, сколько {ру(в_ру, 5)} {ру_имя} {гл(ру_имя, г_ру)} {СРОКИ_RU[срок]}? {отв} {СРОКИ_RU[срок]}."
    if ф == 1:
        if в_ру is None:
            return f"if {имя} {г} {a} {в} in the morning, {b} in the afternoon and {c} in the evening, how many {в} did {имя} {г0} in all? {a} + {b} + {c} = {a + b + c}."
        return f"{ру_имя} {гл(ру_имя, г_ру)} утром {a} {ру(в_ру, a)}, днём {b} и вечером {c}; {СРОКИ_RU[срок]} {ру_имя} {гл(ру_имя, г_ру)} {отв} {ру(в_ру, отв)}."
    if ф == 2:
        return f"{имя} {г} {a} {в} in the morning, {b} in the afternoon and {c} in the evening; {имя} did not {г0} {чужое} {в} {когда}: {имя} {г} {отв}."
    return f"if {имя} {г} {a} {в} in the morning, {b} in the afternoon and {c} in the evening, how many {в} did {имя} {г0} {когда}? {отв} {когда}."


# --- 24. остаток при отвлекающем: how many cakes would the baker still have ---
def п_остаток(шаг, i):
    n = 10 + (шаг * 7 + i * 3) % 40
    m = 5 + (шаг + i * 5) % 30
    k = 2 + (шаг * 3 + i) % 8
    свои = (шаг + i) % 2 == 1  # продано СВОЁ (торты) или чужое (булочки)
    return dict(n=n, m=m, k=k, свои=свои, ответ=n - k if свои else n)


def остаток(шаг, i):
    п = п_остаток(шаг, i)
    n, m, k, свои, r = п["n"], п["m"], п["k"], п["свои"], п["ответ"]
    что = "cakes" if свои else "pastries"
    что_ру = ру("торт", k) if свои else ру("булочка", k)
    основание = f"{n} − {k} = {r}" if свои else "the pastries sold are not cakes"
    ф = ((шаг + i) // 2 + шаг) % 4
    if ф == 0:
        return f"the baker made {n} cakes and {m} pastries and sold {k} {что}; the baker still has {r} cakes: {основание}."
    if ф == 1 and _ру_вопрос(шаг, i):
        return (f"если пекарь испёк {n} {ру('торт', n)} и {m} {ру('булочка', m)} и продал {k} {что_ру}, сколько тортов осталось? "
                f"{n} {ру('торт', n)}; {m} {ру('булочка', m)} не в счёт; {n} − {k} = {r}." if свои else
                f"если пекарь испёк {n} {ру('торт', n)} и {m} {ру('булочка', m)} и продал {k} {что_ру}, сколько тортов осталось? "
                f"{n} {ру('торт', n)}: проданы булочки, не торты.")
    if ф == 1:
        осн_ру = f"{n} − {k} = {r}" if свои else "проданы булочки, не торты"
        return f"пекарь испёк {n} {ру('торт', n)} и {m} {ру('булочка', m)} и продал {k} {что_ру}; тортов осталось {r}: {осн_ру}."
    if ф == 2:
        return f"the baker made {n} cakes and {m} pastries and sold {k} {что}; the baker does not still have {r + 1} cakes: the baker has {r}."
    if свои:
        return f"if the baker made {n} cakes and {m} pastries and sold {k} cakes, how many cakes would the baker still have? {n} cakes; the {m} pastries do not count; {n} − {k} = {r}."
    return f"if the baker made {n} cakes and {m} pastries and sold {k} pastries, how many cakes would the baker still have? {n} cakes; the pastries sold are not cakes."


# --- 25. класс: сумма и разность носителей ---
def п_класс(шаг, i):
    g, b = 5 + (шаг * 3 + i) % 12, 4 + (шаг + i * 5) % 11
    род = (шаг + i) % 2
    return dict(g=g, b=b, s=g + b, род=род, ответ=g + b if род == 0 else b)


def класс(шаг, i):
    п = п_класс(шаг, i)
    g, b, s, род = п["g"], п["b"], п["s"], п["род"]
    ф = ((шаг + i) // 2 + шаг) % 4
    if род == 0:
        if ф == 0:
            return f"there are {g} girls and {b} boys in the class; the class has {s} pupils: {g} + {b} = {s}."
        if ф == 1 and _ру_вопрос(шаг, i):
            return f"если в классе {g} {ру('девочка', g)} и {b} {ру('мальчик', b)}, сколько учеников в классе? {g} + {b} = {s}."
        if ф == 1:
            return f"в классе {g} {ру('девочка', g)} и {b} {ру('мальчик', b)}; в классе {s} {ру('ученик', s)}: {g} + {b} = {s}."
        if ф == 2:
            return f"there are {g} girls and {b} boys in the class; the class does not have {s + 1} pupils: it has {s}."
        return f"if there are {g} girls and {b} boys in the class, how many pupils are there in the class? {g} + {b} = {s}."
    if ф == 0:
        return f"there are {s} pupils in the class and {g} of them are girls; there are {b} boys in the class: {s} − {g} = {b}."
    if ф == 1 and _ру_вопрос(шаг, i):
        return f"если в классе {s} {ру('ученик', s)}, из них {g} {ру('девочка', g)}, сколько мальчиков в классе? {s} − {g} = {b}."
    if ф == 1:
        return f"в классе {s} {ру('ученик', s)}, из них {g} {ру('девочка', g)}; в классе {b} {ру('мальчик', b)}: {s} − {g} = {b}."
    if ф == 2:
        return f"there are {s} pupils in the class and {g} of them are girls; there are not {b + 1} boys in the class: there are {b}."
    return f"if there are {s} pupils in the class and {g} of them are girls, how many boys are there in the class? {s} − {g} = {b}."


# --- 26. деньги: потратил n × p; осталось a − b ---
def п_деньги(шаг, i):
    род = (шаг + i) % 2
    n, p = 2 + (шаг + i * 3) % 8, 3 + (шаг * 3 + i) % 12
    a = 20 + (шаг * 7 + i * 3) % 60
    b = 5 + (шаг + i * 5) % 14
    return dict(род=род, n=n, p=p, a=a, b=b, ответ=n * p if род == 0 else a - b)


def деньги(шаг, i):
    п = п_деньги(шаг, i)
    род, n, p, a, b, отв = п["род"], п["n"], п["p"], п["a"], п["b"], п["ответ"]
    имя, ру_имя = ИМЕНА_EN[(шаг + i) % len(ИМЕНА_EN)], ИМЕНА_RU[(шаг + i) % len(ИМЕНА_RU)]
    en, вещь = ВЕЩИ[(шаг + i) % len(ВЕЩИ)]
    ф = ((шаг + i) // 2 + шаг) % 4
    if род == 0:
        if ф == 0:
            return f"{имя} bought {n} {by_count(n, en)} at {p} dollars each; {имя} spent {отв} dollars: {n} × {p} = {отв}."
        if ф == 1 and _ру_вопрос(шаг, i):
            return f"если {ру_имя} {гл(ру_имя, 'купил')} {n} {ру(вещь, n)} по {p} {ру('доллар', p)}, сколько денег {ру_имя} {гл(ру_имя, 'потратил')}? {n} × {p} = {отв}."
        if ф == 1:
            return f"{ру_имя} {гл(ру_имя, 'купил')} {n} {ру(вещь, n)} по {p} {ру('доллар', p)}; {ру_имя} {гл(ру_имя, 'потратил')} {отв} {ру('доллар', отв)}: {n} × {p} = {отв}."
        if ф == 2:
            return f"{имя} bought {n} {by_count(n, en)} at {p} dollars each; {имя} did not spend {отв + p} dollars: {имя} spent {отв}."
        return f"if {имя} bought {n} {by_count(n, en)} at {p} dollars each, how much money did {имя} spend? {n} × {p} = {отв} dollars."
    if ф == 0:
        return f"{имя} had {a} dollars and spent {b} dollars; {имя} has {отв} dollars left: {a} − {b} = {отв}."
    if ф == 1 and _ру_вопрос(шаг, i):
        return f"если у {кого(ру_имя)} было {a} {ру('доллар', a)}, а {ру_имя} {гл(ру_имя, 'потратил')} {b} {ру('доллар', b)}, сколько денег осталось? {a} − {b} = {отв}."
    if ф == 1:
        return f"у {кого(ру_имя)} было {a} {ру('доллар', a)}, {ру_имя} {гл(ру_имя, 'потратил')} {b} {ру('доллар', b)}; осталось {отв} {ру('доллар', отв)}: {a} − {b} = {отв}."
    if ф == 2:
        return f"{имя} had {a} dollars and spent {b} dollars; {имя} does not have {отв + 1} dollars left: {имя} has {отв}."
    return f"if {имя} had {a} dollars and spent {b} dollars, how much money is left? {a} − {b} = {отв} dollars."


# --- 27. сдача: n купюр по b за вещь ценой p (g1.38) ---
def п_сдача(шаг, i):
    n = 2 + (шаг + i) % 4
    b = (5, 10, 20, 50)[(шаг * 3 + i) % 4]
    p = n * b - (2 + (шаг + i * 3) % (n * b - 2))
    return dict(n=n, b=b, p=p, ответ=n * b - p)


def сдача(шаг, i):
    п = п_сдача(шаг, i)
    n, b, p, c = п["n"], п["b"], п["p"], п["ответ"]
    имя, ру_имя = ИМЕНА_EN[(шаг + i) % len(ИМЕНА_EN)], ИМЕНА_RU[(шаг + i) % len(ИМЕНА_RU)]
    ф = (шаг + i) % 4
    if ф == 0:
        return f"{имя} gave the craftsman {n} {b}-dollar bills for a hat worth {p} dollars; the change is {c} dollars: {n} × {b} − {p} = {c}."
    if ф == 1 and _ру_вопрос(шаг, i):
        return f"если {ру_имя} {гл(ру_имя, 'дал')} мастеру {n} {ру('купюра', n)} по {b} {ру('доллар', b)} за шляпу ценой {p} {ру('доллар', p)}, какова сдача? {n} × {b} − {p} = {c}."
    if ф == 1:
        return f"{ру_имя} {гл(ру_имя, 'дал')} мастеру {n} {ру('купюра', n)} по {b} {ру('доллар', b)} за шляпу ценой {p} {ру('доллар', p)}; сдача {c} {ру('доллар', c)}: {n} × {b} − {p} = {c}."
    if ф == 2:
        return f"{имя} gave the craftsman {n} {b}-dollar bills for a hat worth {p} dollars; the change is not {c + 1} dollars: it is {c}."
    return f"if {имя} gave the craftsman {n} {b}-dollar bills for a hat worth {p} dollars, how much change did {имя} get? {n} × {b} − {p} = {c} dollars."


# --- 28. прибыль при цене a/b от закупочной (g1.58) ---
ДРОБИ = ((11, 8), (5, 4), (7, 5), (3, 2), (9, 8))


def п_прибыль(шаг, i):
    a, b = ДРОБИ[(шаг + i) % len(ДРОБИ)]
    p = b * (3 + (шаг * 3 + i) % 12)
    return dict(a=a, b=b, p=p, ответ=p * a // b - p)


def прибыль(шаг, i):
    п = п_прибыль(шаг, i)
    a, b, p, r = п["a"], п["b"], п["p"], п["ответ"]
    имя, ру_имя = ИМЕНА_EN[(шаг + i) % len(ИМЕНА_EN)], ИМЕНА_RU[(шаг + i) % len(ИМЕНА_RU)]
    ф = (шаг + i) % 4
    if ф == 0:
        return f"{имя} bought the magazines at {p} dollars and sells them at {a}/{b} of the price; the profit is {r} dollars: {p} × {a} ÷ {b} − {p} = {r}."
    if ф == 1 and _ру_вопрос(шаг, i):
        return f"если {ру_имя} {гл(ру_имя, 'купил')} журналы за {p} {ру('доллар', p)} и продаёт их за {a}/{b} цены, какова прибыль? {p} × {a} ÷ {b} − {p} = {r}."
    if ф == 1:
        return f"{ру_имя} {гл(ру_имя, 'купил')} журналы за {p} {ру('доллар', p)} и продаёт их за {a}/{b} цены; прибыль {r} {ру('доллар', r)}: {p} × {a} ÷ {b} − {p} = {r}."
    if ф == 2:
        return f"{имя} bought the magazines at {p} dollars and sells them at {a}/{b} of the price; the profit is not {r + 1} dollars: it is {r}."
    return f"if {имя} bought the magazines at {p} dollars and sells them at {a}/{b} of the price, what is the profit? {p} × {a} ÷ {b} − {p} = {r} dollars."


# --- 29. завышение на q процентов (g1.45) ---
ЗАВЫШЕНИЯ = ((20, 5), (25, 4), (50, 2), (10, 10))  # (проценты, шаг истинного числа)


def п_завышение(шаг, i):
    q, кратно = ЗАВЫШЕНИЯ[(шаг + i) % len(ЗАВЫШЕНИЯ)]
    r = кратно * (4 + (шаг * 3 + i) % 12)
    return dict(q=q, n=r * (100 + q) // 100, ответ=r)


def завышение(шаг, i):
    п = п_завышение(шаг, i)
    q, n, r = п["q"], п["n"], п["ответ"]
    имя, ру_имя = ИМЕНА_EN[(шаг + i) % len(ИМЕНА_EN)], ИМЕНА_RU[(шаг + i) % len(ИМЕНА_RU)]
    ф = (шаг + i) % 4
    if ф == 0:
        return f"{имя} reported {n} people at the concert, overstating the number by {q} percent; {r} people really attended: {n} × 100 ÷ (100 + {q}) = {r}."
    if ф == 1 and _ру_вопрос(шаг, i):
        return f"если {ру_имя} {гл(ру_имя, 'сообщил')}, что на концерте было {n} {ру('человек', n)}, завысив число на {q} {ру('процент', q)}, сколько человек было на самом деле? {n} × 100 ÷ (100 + {q}) = {r}."
    if ф == 1:
        return f"{ру_имя} {гл(ру_имя, 'сообщил')}, что на концерте было {n} {ру('человек', n)}, завысив число на {q} {ру('процент', q)}; на самом деле было {r} {ру('человек', r)}: {n} × 100 ÷ (100 + {q}) = {r}."
    if ф == 2:
        return f"{имя} reported {n} people at the concert, overstating the number by {q} percent; the real number is not {n}: it is {r}."
    return f"if {имя} reported {n} people at the concert, overstating the number by {q} percent, how many people really attended? {n} × 100 ÷ (100 + {q}) = {r}."


# --- 30. половина / кратно и всего (g1.10) ---
КРАТНОСТИ_ВСЕГО = (("half as many", "вдвое меньше", 2, True), ("twice as many", "вдвое больше", 2, False),
                   ("three times as many", "втрое больше", 3, False))


def п_половина(шаг, i):
    слово, слово_ру, k, делить = КРАТНОСТИ_ВСЕГО[(шаг + i) % 3]
    n = 2 * (3 + (шаг * 3 + i) % 12) if делить else 3 + (шаг * 3 + i) % 12
    жуки = n // k if делить else n * k
    return dict(слово=слово, слово_ру=слово_ру, k=k, делить=делить, n=n, ответ=n + жуки)


def половина(шаг, i):
    п = п_половина(шаг, i)
    слово, слово_ру, k, делить, n, t = п["слово"], п["слово_ру"], п["k"], п["делить"], п["n"], п["ответ"]
    осн = f"{n} + {n} ÷ {k} = {t}" if делить else f"{n} + {n} × {k} = {t}"
    ф = (шаг + i) % 4
    if ф == 0:
        return f"there were {n} ants and {слово} bugs as ants in the garden; there were {t} insects in all: {осн}."
    if ф == 1 and _ру_вопрос(шаг, i):
        return f"если в саду было {n} {ру('муравей', n)} и {слово_ру} жуков, сколько всего муравьёв и жуков? {осн}."
    if ф == 1:
        return f"в саду было {n} {ру('муравей', n)} и {слово_ру} жуков; всего муравьёв и жуков {t}: {осн}."
    if ф == 2:
        return f"there were {n} ants and {слово} bugs as ants in the garden; there were not {t + 1} insects in all: there were {t}."
    return f"if there were {n} ants and {слово} bugs as ants in the garden, how many insects were there in all? {осн}."


СЕМЕЙСТВА = (сумма, температура, процент, фунты, глубина, вероятность, четверти, дополнение,
             население, команда, кратно, проект, окружность, верёвки, трое, ставка, листки,
             разница, скидка, всего, группы,
             больше, отбор, остаток, класс, деньги, сдача, прибыль, завышение, половина)


def pass_groups(шаг):
    return [[семья(шаг, i) for i in range(16)] for семья in СЕМЕЙСТВА]


def main():
    emit_grouped(ЦЕЛЬ, pass_groups)


if __name__ == "__main__":
    main()
