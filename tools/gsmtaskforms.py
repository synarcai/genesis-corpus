#!/usr/bin/env python3
"""ДОМ ЗАДАЧ ШКОЛЫ — тридцать пять семейств, и всякое есть род.

Мир `gsmforms` (2 591 строка) был крупнейшим бездомным миром свода после разбора остальных.
Роды его лежали в кузнице рядом имён-строителей (`СЕМЕЙСТВА`): сумма, температура, процент,
фунты, глубина, вероятность… — тридцать пять дел, и ни одно не выходило наружу.

    МИР, ЧЬИ СТРАНИЦЫ НЕ НАЗВАНЫ РОДОМ, ЧИТАЕТСЯ ТОЛЬКО ТЕМ, КТО ЧИТАЕТ КУЗНИЦУ.

РОД ЗДЕСЬ ЕСТЬ ИМЯ СТРОИТЕЛЯ, и это не лень именования, а факт: всякое семейство есть отдельное
умение — «сдача», «скидка», «остаток деления» суть разные действия над числами, а не три
поверхности одного.

СЦЕНЫ ПЕРЕПИСАНЫ 23.09 ПО СЛОВУ ВЛАДЕЛЬЦА: полоса — прибор, а не источник. Семейства родились
переписью немых конструкций полос (g1, SVAMP), и сцены их были писаны чтением самих задач —
земля и самолёт, дом и участок, листки на холодильнике, пекарь с булочками. Конструкция и
формула каждого рода остались; сцена, слова и сетки чисел — свои, выкладка ответа стоит на
каждой странице, отрицание тоже (подробно — у первого семейства).
"""
import json
import pathlib
import re
import sys

КОРЕНЬ = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(КОРЕНЬ / "tools"))
import rugram  # noqa: E402
from plural import by_count  # noqa: E402
_EN = json.loads((КОРЕНЬ / "tools" / "langpacks" / "en.json").read_text(encoding="utf-8"))
_RU = json.loads((КОРЕНЬ / "tools" / "langpacks" / "ru.json").read_text(encoding="utf-8"))
# выбор лиц — дома, письмо — пакета (05.09): сверка по строчному образу
ИМЕНА_EN = [n for n in _EN["person_names"] if n.lower() in ("ann", "ben", "carla", "dan", "elena", "felix", "grace", "hugo", "ida", "omar", "peter", "vera")]
# РУССКИЕ ИМЕНА В ИМЕНИТЕЛЬНОМ — рамки построены так, что иных падежей нет
# («Вера имеет 7 ручек»): так дом имён держит их одной таблицей.
ИМЕНА_RU = [n.capitalize() for n in _RU["person_names"] if n.lower() in ("вера", "петя", "маша", "коля", "аня", "дима", "лена", "юра")]
# РОД И РОДИТЕЛЬНЫЙ — ТАБЛИЦЕЙ ГЕНЕРАТОРА (пакет держит именительный; формы
# падежей держат таблицы генераторов, суды читают их той же рукой): «у
# Веры было», «Вера отдала» — третий слой дал рамки с падежом и глаголом.
ЖЕНСКИЕ_RU = {n.capitalize() for n, ф in _RU["person_forms"].items() if ф["gender"] == "f"}
РОДИТЕЛЬНЫЙ_RU = {n.capitalize(): ф["gen"].capitalize() for n, ф in _RU["person_forms"].items()}
assert set(ИМЕНА_RU) <= set(РОДИТЕЛЬНЫЙ_RU)


# ЧЕРЕДОВАНИЕ ОСНОВЫ НАЗВАНО ПОИМЁННО: «испёк → испекла» правилом «+а» не дать.
НЕПРАВИЛЬНЫЕ_RU = {"испёк": "испекла", "нашёл": "нашла"}

# РОД-УПРАЖНЕНИЕ ОБЪЯВЛЕН ВСЛУХ (14.09, ключ `--свод`: решено по КАЖДОМУ из тридцати трёх
# родов — дом самый многородный в корпусе). Все они суть ЗАДАЧИ ОДНОГО СКЛАДА при разных
# числах и разных предметах: процент от класса, группы по двое, скидка, сдача, прибыль,
# глубина, температура. Мысль в каждом роде одна — своё действие над числами задачи, — а
# имена, вещи и единицы лишь носят их.
#
# СЛУЧАЙ РЕДКИЙ, И ПОТОМУ НАЗВАН ВСЛУХ: «объявлено всё» есть ровно тот вид, какой принимает
# уклонение. Здесь он законен оттого, что дом ВЕСЬ есть рынок школьных задач (GSM8K): в нём
# по устройству нет и не может быть рода без чисел — ЗАДАЧА БЕЗ ЧИСЛА НЕ ЗАДАЧА.
#
# Плотность родов здесь от 11,4 до 1,0, и низкая у тех, где вместе с числами перебираются
# ИМЕНА и ВЕЩИ («сумма» 80 на 80, «отбор», «полосы»). Они ровны собою, но объявлены
# упражнением наравне с прочими: РОД, РОВНЫЙ СОБОЮ В ДОМЕ ОДНОГО ДЕЛА, ЕСТЬ ТОТ ЖЕ СЧЁТ С
# БОЛЕЕ ШИРОКИМ МАТЕРИАЛОМ, А НЕ ИНОЕ ДЕЛО.
ОЧЕРТАНИЕ_ПО_ПРИРОДЕ = (
    "больше", "вероятность", "верёвки", "всего", "глубина", "группы", "деньги", "дополнение",
    "завышение", "класс", "команда", "кратно", "листки", "население", "окружность",
    "остаток", "остаток_деления", "отбор", "половина", "полосы", "прибыль", "проект",
    "процент", "разница", "сдача", "скидка", "ставка", "сумма", "температура", "трое",
    "фунты", "части", "четверти")


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


def ру_косв(вещь, n):
    """Форма при числе ПОД ПРЕДЛОГОМ, требующим родительного («с 9 панелей»,
    «с 21 панели»): один — родительный единственного, прочие — множественного;
    счётная форма именительного здесь была бы ложью («с 2 панели»)."""
    return rugram.форма(вещь, 2) if n % 10 == 1 and n % 100 != 11 else rugram.форма(вещь, 5)


def _ру_вопрос(шаг, i):
    """RU-форма чередуется: повествование / вопрос с ответом-уравнением (М-146:
    у каждой рамки на каждом языке обязана быть вопросная поверхность).

    ФАЗА НЕЗАВИСИМА ОТ ВЫБОРА ФОРМЫ: чётность (шаг + i) уже выбирает форму
    ф == 1, и вторая чётность на тех же числах совпадала с ней — русское
    повествование не показывалось ни разу (таблица родов 03.09: ru/утверждение
    0 при ru/вопрос 20). Фаза берётся из следующего разряда."""
    return ((шаг + i) // 4) % 2 == 1


# СЦЕНЫ ДОМА ПЕРЕПИСАНЫ 23.09 (слово владельца: полоса — прибор, а не источник). Дом был писан
# чтением задач самих полос — «окружность земли», «листки на холодильнике», «сдача мастеру за
# шляпу», «журналы за 11/8 цены», «дом и участок», «пекарь продал булочки», «кузнечик прыгнул».
# Ныне у каждого семейства своя сцена при той же конструкции и той же формуле: пять поверхностей,
# сетки чисел дома, числа условия в тексте и выкладка ответа на странице. Отрицание несёт свою
# выкладку («… is not 17: it is 16, because 11 + 5 = 16»): дверь ядра учится на выровненных
# страницах, и страница без уравнения ей не показ.
#
#     КОНСТРУКЦИЯ ОСТАЁТСЯ, СЦЕНА ПОЛОСЫ УХОДИТ: семейство есть действие над числами, а не
#     история, в которой полоса его однажды рассказала.


def _есть(n):
    """Английская связка при числе: «1 is», «2 are»."""
    return "is" if abs(n) == 1 else "are"


def _ру_ед(n):
    """Русское единственное при числе: 1, 21, 31 … — но не 11."""
    return n % 10 == 1 and n % 100 != 11


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
        return (f"{a} has {x} {by_count(x, en)} and {b} has {y} {by_count(y, en)}; the total number of {en} is not {s + 1}: "
                f"it is {s}, because {x} + {y} = {s}.")
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
    знак = "−" if падение else "+"
    ф = (шаг + i) % 4
    if ф == 0:
        return (f"the temperature was {ч(t0)} {by_count(abs(t0), 'degrees')} and {'fell' if падение else 'rose'} by {d} {by_count(d, 'degrees')}; "
                f"the temperature in degrees is now {ч(t1)}: {ч(t0)} {знак} {d} = {ч(t1)}.")
    if ф == 1 and _ру_вопрос(шаг, i):
        return (f"если температура была {ч(t0)} {ру('градус', abs(t0))} и {'упала' if падение else 'поднялась'} на {d} {ру('градус', d)}, "
                f"какова температура теперь? {ч(t0)} {знак} {d} = {ч(t1)}.")
    if ф == 1:
        return (f"температура была {ч(t0)} {ру('градус', abs(t0))} и {'упала' if падение else 'поднялась'} на {d} {ру('градус', d)}; "
                f"теперь температура — {ч(t1)} {ру('градус', abs(t1))}: {ч(t0)} {знак} {d} = {ч(t1)}.")
    if ф == 2:
        чуж = t1 + (d if падение else -d)
        return (f"the temperature was {ч(t0)} {by_count(abs(t0), 'degrees')} and {'fell' if падение else 'rose'} by {d} {by_count(d, 'degrees')}; "
                f"the temperature in degrees is not {ч(чуж)}: it is {ч(t1)}, because {ч(t0)} {знак} {d} = {ч(t1)}.")
    return (f"the temperature was {ч(t0)} {by_count(abs(t0), 'degrees')} and {'fell' if падение else 'rose'} by {d} {by_count(d, 'degrees')}. "
            f"what is the temperature in degrees now? {ч(t0)} {знак} {d} = {ч(t1)}.")


# ---------- 3. percentage of: the orchard and its pear trees ----------
def п_процент(шаг, i):
    всего = (20, 25, 40, 50, 60, 80, 100)[(шаг + i) % 7]
    доли = [k for k in range(1, всего) if (k * 100) % всего == 0]
    часть = доли[(шаг * 3 + i) % len(доли)]
    return dict(всего=всего, часть=часть, ответ=часть * 100 // всего)


def процент(шаг, i):
    п = п_процент(шаг, i)
    всего, часть, p = п["всего"], п["часть"], п["ответ"]
    груши = "is a pear tree" if часть == 1 else "are pear trees"
    ф = (шаг + i) % 4
    if ф == 0:
        return (f"the orchard has {всего} {by_count(всего, 'trees')} and {часть} of them {груши}; the percentage of pear trees is {p} %: "
                f"{часть} ÷ {всего} × 100 = {p}.")
    if ф == 1 and _ру_вопрос(шаг, i):
        return (f"если в саду {всего} {ру('дерево', всего)}, из них {часть} {ру('груша', часть)}, какова доля груш в процентах? "
                f"{всего} {ру('дерево', всего)} и {часть} {ру('груша', часть)}: {часть} ÷ {всего} × 100 = {p}.")
    if ф == 1:
        return (f"в саду {всего} {ру('дерево', всего)}, из них {часть} {ру('груша', часть)}; доля груш — {p} %: "
                f"{часть} ÷ {всего} × 100 = {p}.")
    if ф == 2:
        return (f"the orchard has {всего} {by_count(всего, 'trees')} and {часть} of them {груши}; the percentage of pear trees is not {p + 5} %: "
                f"it is {p} %, because {часть} ÷ {всего} × 100 = {p}.")
    return (f"the orchard has {всего} {by_count(всего, 'trees')} and {часть} of them {груши}. what percentage of the trees are pear trees? "
            f"{всего} {by_count(всего, 'trees')} and {часть} {by_count(часть, 'pear trees')}: {часть} ÷ {всего} × 100 = {p} %.")


# ---------- 4. weight in pounds: a bag of apples ----------
def п_фунты(шаг, i):
    ф_ = 1 + (шаг * 3 + i) % 9
    return dict(унц=ф_ * 16, ответ=ф_)


def фунты(шаг, i):
    п = п_фунты(шаг, i)
    унц, ф_ = п["унц"], п["ответ"]
    ф = (шаг + i) % 4
    if ф == 0:
        return f"a bag of apples weighs {унц} {by_count(унц, 'ounces')} and a pound is 16 ounces; the weight in pounds is {ф_}: {унц} ÷ 16 = {ф_}."
    if ф == 1 and _ру_вопрос(шаг, i):
        return f"если мешок яблок весит {унц} {ру('унция', унц)}, а в фунте 16 унций, каков вес в фунтах? {унц} ÷ 16 = {ф_}."
    if ф == 1:
        return (f"мешок яблок весит {унц} {ру('унция', унц)}, а в фунте 16 унций; вес в фунтах — {ф_} {ру('фунт', ф_)}: "
                f"{унц} ÷ 16 = {ф_}.")
    if ф == 2:
        return (f"a bag of apples weighs {унц} {by_count(унц, 'ounces')} and a pound is 16 ounces; the weight in pounds is not {ф_ + 1}: "
                f"it is {ф_}, because {унц} ÷ 16 = {ф_}.")
    return (f"a bag of apples weighs {унц} {by_count(унц, 'ounces')} and a pound is 16 ounces. what is the weight in pounds? "
            f"{унц} {by_count(унц, 'ounces')}: {унц} ÷ 16 = {ф_}.")


# ---------- 5. depth from volume: sand in a pit ----------
def п_глубина(шаг, i):
    w, l = 2 + (шаг + i) % 5, 2 + (шаг * 2 + i * 3) % 6
    h = 1 + (шаг * 5 + i) % 6
    return dict(w=w, l=l, v=w * l * h, ответ=h)


def глубина(шаг, i):
    п = п_глубина(шаг, i)
    w, l, v, h = п["w"], п["l"], п["v"], п["ответ"]
    яма = (f"the pit is {w} {by_count(w, 'meters')} wide and {l} {by_count(l, 'meters')} long "
           f"and holds {v} {by_count(v, 'cubic meters')} of sand")
    ф = (шаг + i) % 4
    if ф == 0:
        return f"{яма}; the sand in the pit is {h} {by_count(h, 'meters')} deep: {v} ÷ ({w} × {l}) = {h}."
    if ф == 1 and _ру_вопрос(шаг, i):
        return (f"если яма шириной {w} {ру('метр', w)} и длиной {l} {ру('метр', l)} вмещает {v} {ру('кубический метр', v)} песка, "
                f"какой толщины слой песка в яме? {w} на {l} при {v}: {v} ÷ ({w} × {l}) = {h}.")
    if ф == 1:
        return (f"яма шириной {w} {ру('метр', w)} и длиной {l} {ру('метр', l)} вмещает {v} {ру('кубический метр', v)} песка; "
                f"слой песка в яме — {h} {ру('метр', h)}: {v} ÷ ({w} × {l}) = {h}.")
    if ф == 2:
        return (f"{яма}; the sand in the pit is not {h + 1} {by_count(h + 1, 'meters')} deep: "
                f"it is {h} {by_count(h, 'meters')} deep, because {v} ÷ ({w} × {l}) = {h}.")
    return f"{яма}. how deep is the sand in the pit? {w} by {l} holding {v}: {v} ÷ ({w} × {l}) = {h} {by_count(h, 'meters')}."


# ---------- 6. probability as a fraction: buttons in a jar ----------
def п_вероятность(шаг, i):
    r, b = 1 + (шаг + i) % 6, 1 + (шаг * 3 + i * 2) % 7
    return dict(r=r, b=b, n=r + b, ответ=f"{r}/{r + b}")


def вероятность(шаг, i):
    п = п_вероятность(шаг, i)
    r, b, n = п["r"], п["b"], п["n"]
    банка = f"a jar holds {r} black {by_count(r, 'buttons')} and {b} white {by_count(b, 'buttons')}"
    ф = (шаг + i) % 4
    if ф == 0:
        return (f"{банка}; the probability of taking a black button, written as a fraction, is {r}/{n}: "
                f"{r} + {b} = {n} buttons, {r} of them black.")
    if ф == 1 and _ру_вопрос(шаг, i):
        return (f"если в банке чёрных пуговиц {r}, а белых {b}, какова вероятность взять чёрную пуговицу, "
                f"записанная дробью? {r} + {b} = {n}: {r}/{n}.")
    if ф == 1:
        return (f"в банке чёрных пуговиц {r}, а белых {b}; вероятность взять чёрную пуговицу, записанная дробью, — {r}/{n}: "
                f"{r} + {b} = {n}, из них чёрных {r}.")
    if ф == 2:
        # ЧУЖАЯ ДОЛЯ — ЧИСЛИТЕЛЕМ СОСЕДА, а не белых: при r = b белых столько
        # же, и «не b/n» было бы ложью о верной дроби.
        чуж = r + 1 if r + 1 < n else r - 1
        return (f"{банка}; the probability of taking a black button, written as a fraction, is not {чуж}/{n}: "
                f"it is {r}/{n}, because {r} + {b} = {n}.")
    return f"{банка}. what is the probability of taking a black button, written as a fraction? {r} + {b} = {n}: {r}/{n}."


# ---------- 7. # quarters of: pages of a book ----------
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
        return f"if {часть} pages are {слово} of the book, the book has {целое} pages: {часть} ÷ {k} × 4 = {целое}."
    if ф == 1 and _ру_вопрос(шаг, i):
        return f"если {часть} {ру('страница', часть)} — это {ру_слово} книги, сколько страниц в книге? {часть} ÷ {k} × 4 = {целое}."
    if ф == 1:
        return (f"если {часть} {ру('страница', часть)} — это {ру_слово} книги, в книге {целое} {ру('страница', целое)}: "
                f"{часть} ÷ {k} × 4 = {целое}.")
    if ф == 2:
        return (f"if {часть} pages are {слово} of the book, the book does not have {целое + 4} pages: "
                f"it has {целое}, because {часть} ÷ {k} × 4 = {целое}.")
    return f"if {часть} pages are {слово} of the book, how many pages does the book have? {часть} ÷ {k} × 4 = {целое}."


# ---------- 8. originally / missing / at the party now ----------
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
        # утки на пруду: исходное и улетевшие
        уток = f"{осталось} {by_count(осталось, 'ducks')} {'remains' if осталось == 1 else 'remain'}"
        улетели = "улетела" if _ру_ед(ушло) else "улетели"
        if ф == 0:
            return f"there were originally {было} ducks on the pond and {ушло} flew away; {уток}: {было} − {ушло} = {осталось}."
        if ф == 1 and _ру_вопрос(шаг, i):
            return (f"если на пруду изначально было {было} {ру('утка', было)}, а {ушло} {улетели}, сколько уток осталось? "
                    f"{было} − {ушло} = {осталось}.")
        if ф == 1:
            return (f"на пруду изначально было {было} {ру('утка', было)}, {ушло} {улетели}; осталось {осталось} {ру('утка', осталось)}: "
                    f"{было} − {ушло} = {осталось}.")
        if ф == 2:
            return (f"there were originally {было} ducks on the pond and {ушло} flew away; {осталось + 1} ducks do not remain: "
                    f"{осталось} {'remains' if осталось == 1 else 'remain'}, because {было} − {ушло} = {осталось}.")
        return f"if there were originally {было} ducks on the pond and {ушло} flew away, how many ducks remain? {было} − {ушло} = {осталось}."
    if род == 1:
        # альбом марок: мест и вклеенных, недостающие
        вклеено = f"{осталось} {_есть(осталось)} glued in"
        ру_вклеено = "вклеена" if _ру_ед(осталось) else "вклеено"
        if ф == 0:
            return (f"the album has room for {было} stamps and {вклеено}; {ушло} {by_count(ушло, 'stamps')} {_есть(ушло)} missing: "
                    f"{было} − {осталось} = {ушло}.")
        # ЧИСЛО МЕСТ СТОИ́Т ПОСЛЕ ИМЕНИ («мест для марок в альбоме 21»): «место для 21 марки» верно
        # по-русски, но суд счёта (`langcount`) предлога не читает и ждёт счётной формы — страница
        # строится так, чтобы согласования при этом числе не было вовсе.
        if ф == 1 and _ру_вопрос(шаг, i):
            return (f"если мест для марок в альбоме {было}, а {ру_вклеено} {осталось} {ру('марка', осталось)}, "
                    f"сколько марок не хватает? {было} − {осталось} = {ушло}.")
        if ф == 1:
            return (f"мест для марок в альбоме {было}, {ру_вклеено} {осталось} {ру('марка', осталось)}; "
                    f"не хватает {ушло}: {было} − {осталось} = {ушло}.")
        if ф == 2:
            return (f"the album has room for {было} stamps and {вклеено}; {ушло + 1} stamps are not missing: "
                    f"{ушло} {_есть(ушло)} missing, because {было} − {осталось} = {ушло}.")
        return f"the album has room for {было} stamps and {вклеено}. how many stamps are missing? {было} − {осталось} = {ушло}."
    # гости на празднике: были и ушедшие домой
    ушли = "ушёл" if _ру_ед(ушло) else "ушли"
    if ф == 0:
        return (f"there were {было} guests at the party and {ушло} went home; {осталось} {by_count(осталось, 'guests')} {_есть(осталось)} "
                f"at the party now: {было} − {ушло} = {осталось}.")
    if ф == 1 and _ру_вопрос(шаг, i):
        return (f"если на празднике было {было} {ру('гость', было)}, а {ушло} {ушли} домой, сколько гостей на празднике теперь? "
                f"{было} − {ушло} = {осталось}.")
    if ф == 1:
        return (f"на празднике было {было} {ру('гость', было)}, {ушло} {ушли} домой; теперь на празднике {осталось} {ру('гость', осталось)}: "
                f"{было} − {ушло} = {осталось}.")
    if ф == 2:
        return (f"there were {было} guests at the party and {ушло} went home; the number of guests at the party now is not {осталось + 1}: "
                f"it is {осталось}, because {было} − {ушло} = {осталось}.")
    return (f"if there were {было} guests at the party and {ушло} went home, how many guests are at the party now? "
            f"{было} − {ушло} = {осталось}.")


# ---------- 9. a fraction of the whole: books of a library ----------
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
        return (f"the library has {всего} books and {слово} of all the books stand in the reading room; "
                f"{часть} books stand in the reading room: {всего} ÷ {доля} = {часть}.")
    if ф == 1 and _ру_вопрос(шаг, i):
        return (f"если в библиотеке {всего} {ру('книга', всего)}, и {ру_слово} всех книг стоит в читальном зале, "
                f"сколько книг стоит в читальном зале? {всего} ÷ {доля} = {часть}.")
    if ф == 1:
        return (f"в библиотеке {всего} {ру('книга', всего)}, и {ру_слово} всех книг стоит в читальном зале; "
                f"в читальном зале стоит {часть} {ру('книга', часть)}: {всего} ÷ {доля} = {часть}.")
    if ф == 2:
        return (f"the library has {всего} books and {слово} of all the books stand in the reading room; "
                f"the number of books in the reading room is not {часть + 100}: it is {часть}, because {всего} ÷ {доля} = {часть}.")
    return (f"if the library has {всего} books and {слово} of all the books stand in the reading room, "
            f"how many books stand in the reading room? {всего} books: {всего} ÷ {доля} = {часть}.")


# ---------- 10. the number of … on …: books and magazines on a shelf ----------
def п_команда(шаг, i):
    м, д = 3 + (шаг * 3 + i) % 10, 2 + (шаг + i * 5) % 9
    return dict(м=м, д=д, ответ=м + д)


def команда(шаг, i):
    п = п_команда(шаг, i)
    м, д, s = п["м"], п["д"], п["ответ"]
    ф = (шаг + i) % 4
    if ф == 0:
        return f"the number of books on the shelf is {м} and the number of magazines is {д}; the shelf holds {s} items: {м} + {д} = {s}."
    if ф == 1 and _ру_вопрос(шаг, i):
        return f"если на полке {м} {ру('книга', м)} и {д} {ру('журнал', д)}, сколько всего предметов на полке? {м} + {д} = {s}."
    if ф == 1:
        return f"на полке {м} {ру('книга', м)} и {д} {ру('журнал', д)}; всего на полке {s} {ру('предмет', s)}: {м} + {д} = {s}."
    if ф == 2:
        return (f"the number of books on the shelf is {м} and the number of magazines is {д}; the shelf does not hold {s + 1} items: "
                f"it holds {s}, because {м} + {д} = {s}.")
    return f"if the number of books on the shelf is {м} and the number of magazines is {д}, how many items does the shelf hold? {м} + {д} = {s}."


# ---------- 11. three times as much: the tractor and the barn ----------
def п_кратно(шаг, i):
    k = (2, 3, 4)[(шаг + i) % 3]
    цена = 1000 * (5 + (шаг * 7 + i * 3) % 26)
    return dict(k=k, цена=цена, ответ=k * цена, слово=("twice", "three times", "four times")[k - 2],
                ру_слово=("вдвое", "втрое", "вчетверо")[k - 2])


def кратно(шаг, i):
    п = п_кратно(шаг, i)
    k, цена, амбар, слово, ру_ = п["k"], п["цена"], п["ответ"], п["слово"], п["ру_слово"]
    ф = (шаг + i) % 4
    if ф == 0:
        return (f"the tractor cost {цена} {by_count(цена, 'dollars')} and the barn cost {слово} as much as the tractor; "
                f"the barn cost {амбар} {by_count(амбар, 'dollars')}: {цена} × {k} = {амбар}.")
    if ф == 1 and _ру_вопрос(шаг, i):
        return (f"если трактор стоил {цена} {ру('доллар', цена)}, а амбар стоил {ру_} дороже трактора, сколько стоил амбар? "
                f"{цена} {ру('доллар', цена)}: {цена} × {k} = {амбар}.")
    if ф == 1:
        return (f"трактор стоил {цена} {ру('доллар', цена)}, а амбар стоил {ру_} дороже трактора; "
                f"амбар стоил {амбар} {ру('доллар', амбар)}: {цена} × {k} = {амбар}.")
    if ф == 2:
        return (f"the tractor cost {цена} {by_count(цена, 'dollars')} and the barn cost {слово} as much as the tractor; "
                f"the barn did not cost {амбар + цена} {by_count(амбар + цена, 'dollars')}: it cost {амбар}, because {цена} × {k} = {амбар}.")
    return (f"if the tractor cost {цена} {by_count(цена, 'dollars')} and the barn cost {слово} as much as the tractor, "
            f"how much did the barn cost? {цена} × {k} = {амбар} {by_count(амбар, 'dollars')}.")


# ---------- 12. doubled, then reduced: an order of boxes ----------
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
        return (f"the order started with {старт} boxes, was {слово} and then reduced by {минус}; "
                f"the final order has {итог} boxes: {старт} × {k} − {минус} = {итог}.")
    if ф == 1 and _ру_вопрос(шаг, i):
        return (f"если заказ начинался с {старт} {ру_косв('коробка', старт)}, его {ру_} и потом убавили на {минус}, "
                f"сколько коробок в итоговом заказе? {старт} × {k} − {минус} = {итог}.")
    if ф == 1:
        return (f"заказ начинался с {старт} {ру_косв('коробка', старт)}, его {ру_} и потом убавили на {минус}; "
                f"в итоговом заказе {итог} {ру('коробка', итог)}: {старт} × {k} − {минус} = {итог}.")
    if ф == 2:
        return (f"the order started with {старт} boxes, was {слово} and then reduced by {минус}; "
                f"the final order does not have {итог + минус} boxes: it has {итог}, because {старт} × {k} − {минус} = {итог}.")
    return (f"if the order started with {старт} boxes, was {слово} and then reduced by {минус}, "
            f"how many boxes does the final order have? {старт} × {k} − {минус} = {итог}.")


# ---------- 13. a loop at a speed: the road around the lake ----------
# СЕТКА СВОЯ, И ВЕЛИЧИНЫ ВЕРНЫ СЦЕНЕ: велосипедист едет 8…20 километров в час два…девять часов.
def п_окружность(шаг, i):
    скорость = 8 + (шаг * 3 + i) % 13
    часы = 2 + (шаг + i * 7) % 8
    return dict(скорость=скорость, ответ=часы, длина=скорость * часы)


def окружность(шаг, i):
    п = п_окружность(шаг, i)
    L, v, t = п["длина"], п["скорость"], п["ответ"]
    дорога = (f"the road around the lake is {L} {by_count(L, 'kilometers')} long and the cyclist rides "
              f"{v} {by_count(v, 'kilometers')} per hour")
    ф = (шаг + i) % 4
    if ф == 0:
        return f"{дорога}; the ride around the lake takes {t} {by_count(t, 'hours')}: {L} ÷ {v} = {t}."
    if ф == 1 and _ру_вопрос(шаг, i):
        return (f"если дорога вокруг озера длиной {L} {ру('километр', L)}, а велосипедист едет {v} {ру('километр', v)} в час, "
                f"сколько часов занимает поездка вокруг озера? {L} ÷ {v} = {t}.")
    if ф == 1:
        return (f"дорога вокруг озера длиной {L} {ру('километр', L)}, велосипедист едет {v} {ру('километр', v)} в час; "
                f"поездка вокруг озера занимает {t} {ру('час', t)}: {L} ÷ {v} = {t}.")
    if ф == 2:
        return (f"{дорога}; the ride around the lake does not take {t + 1} {by_count(t + 1, 'hours')}: "
                f"it takes {t}, because {L} ÷ {v} = {t}.")
    return f"if {дорога}, how many hours does the ride around the lake take? {L} ÷ {v} = {t}."


# ---------- 14. total and average: the height of poles ----------
def п_верёвки(шаг, i):
    n = 2 + (шаг + i) % 4
    среднее = 3 + (шаг * 3 + i) % 12
    return dict(n=n, ответ=среднее, всего=n * среднее)


def верёвки(шаг, i):
    п = п_верёвки(шаг, i)
    n, a, всего = п["n"], п["ответ"], п["всего"]
    ф = (шаг + i) % 4
    if ф == 0:
        return f"the {n} poles had a total height of {всего} {by_count(всего, 'meters')}; the average pole is {a} {by_count(a, 'meters')} tall: {всего} ÷ {n} = {a}."
    if ф == 1 and _ру_вопрос(шаг, i):
        return f"если общая высота столбов {всего} {ру('метр', всего)}, а столбов {n}, какова высота среднего столба? {всего} ÷ {n} = {a}."
    if ф == 1:
        return (f"{n} {ру('столб', n)} имели общую высоту {всего} {ру('метр', всего)}; средний столб высотой {a} {ру('метр', a)}: "
                f"{всего} ÷ {n} = {a}.")
    if ф == 2:
        return (f"the {n} poles had a total height of {всего} {by_count(всего, 'meters')}; the average pole is not {a + 1} {by_count(a + 1, 'meters')} tall: "
                f"it is {a} {by_count(a, 'meters')}, because {всего} ÷ {n} = {a}.")
    return (f"if the total height of the poles is {всего} {by_count(всего, 'meters')} and there are {n} poles, "
            f"how tall is the average pole? {всего} ÷ {n} = {a} {by_count(a, 'meters')}.")


# ---------- 15. together A, B and C: shells ----------
def п_трое(шаг, i):
    a = 3 + (шаг * 3 + i) % 10
    больше = 2 + (шаг + i * 3) % 6
    k = 2 + (шаг + i) % 2
    return dict(a=a, больше=больше, k=k, b=a + больше, c=k * a, ответ=a + (a + больше) + k * a)


def трое(шаг, i):
    п = п_трое(шаг, i)
    a, б, k, s = п["a"], п["больше"], п["k"], п["ответ"]
    x, y, z = ИМЕНА_EN[(шаг + i) % len(ИМЕНА_EN)], ИМЕНА_EN[(шаг + i + 1) % len(ИМЕНА_EN)], ИМЕНА_EN[(шаг + i + 2) % len(ИМЕНА_EN)]
    р_x, р_y, р_z = ИМЕНА_RU[(шаг + i) % len(ИМЕНА_RU)], ИМЕНА_RU[(шаг + i + 1) % len(ИМЕНА_RU)], ИМЕНА_RU[(шаг + i + 2) % len(ИМЕНА_RU)]
    слово = "twice" if k == 2 else "three times"
    ру_ = "вдвое" if k == 2 else "втрое"
    выкладка = f"{a} + ({a} + {б}) + {k} × {a} = {s}"
    ф = (шаг + i) % 4
    if ф == 0:
        return (f"{x} has {a} {by_count(a, 'shells')}, {y} has {б} more shells than {x}, and {z} has {слово} as many shells as {x}; "
                f"together {x}, {y} and {z} have {s} {by_count(s, 'shells')}: {выкладка}.")
    if ф == 1 and _ру_вопрос(шаг, i):
        return (f"если {р_x} имеет {a} {ру('ракушка', a)}, {р_y} имеет на {б} {ру('ракушка', б)} больше, чем {р_x}, "
                f"а {р_z} имеет {ру_} больше ракушек, чем {р_x}, сколько ракушек у них вместе? {выкладка}.")
    if ф == 1:
        return (f"{р_x} имеет {a} {ру('ракушка', a)}, {р_y} имеет на {б} {ру('ракушка', б)} больше, чем {р_x}, "
                f"а {р_z} имеет {ру_} больше ракушек, чем {р_x}; вместе у них {s} {ру('ракушка', s)}: {выкладка}.")
    if ф == 2:
        return (f"{x} has {a} {by_count(a, 'shells')}, {y} has {б} more shells than {x}, and {z} has {слово} as many shells as {x}; "
                f"together they do not have {s + 1} {by_count(s + 1, 'shells')}: they have {s}, because {выкладка}.")
    return (f"if {x} has {a} {by_count(a, 'shells')}, {y} has {б} more shells than {x}, and {z} has {слово} as many shells as {x}, "
            f"how many shells do they have together? {выкладка}.")


# ---------- 16. rate × time: postcards signed in an hour ----------
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
        return f"{имя} signs {r} postcards an hour and works {t} {by_count(t, 'hours')}; {имя} signs {s} postcards: {r} × {t} = {s}."
    if ф == 1 and _ру_вопрос(шаг, i):
        return (f"если {ру_имя} подписывает {r} {ру('открытка', r)} в час и работает {t} {ру('час', t)}, "
                f"сколько открыток подписывает {ру_имя}? {r} × {t} = {s}.")
    if ф == 1:
        return (f"{ру_имя} подписывает {r} {ру('открытка', r)} в час и работает {t} {ру('час', t)}; "
                f"{ру_имя} подписывает {s} {ру('открытка', s)}: {r} × {t} = {s}.")
    if ф == 2:
        return (f"{имя} signs {r} postcards an hour and works {t} {by_count(t, 'hours')}; {имя} does not sign {s + r} postcards: "
                f"{имя} signs {s}, because {r} × {t} = {s}.")
    return f"if {имя} signs {r} postcards an hour and works {t} {by_count(t, 'hours')}, how many postcards does {имя} sign? {r} × {t} = {s}."


# ---------- 17. several subtractions: candies into bowls ----------
def п_листки(шаг, i):
    было = 60 + (шаг * 7 + i * 3) % 40
    раз = 5 + (шаг + i) % 12
    два = 3 + (шаг * 3 + i) % 10
    return dict(было=было, раз=раз, два=два, ответ=было - раз - два)


def листки(шаг, i):
    п = п_листки(шаг, i)
    было, раз, два, s = п["было"], п["раз"], п["два"], п["ответ"]
    имя, ру_имя = ИМЕНА_EN[(шаг + i) % len(ИМЕНА_EN)], ИМЕНА_RU[(шаг + i) % len(ИМЕНА_RU)]
    выкладка = f"{было} − {раз} − {два} = {s}"
    ф = (шаг + i) % 4
    if ф == 0:
        return f"{имя} had {было} candies, put {раз} in the red bowl and {два} in the blue bowl; {имя} has {s} candies left: {выкладка}."
    if ф == 1 and _ру_вопрос(шаг, i):
        return (f"если у {кого(ру_имя)} было {было} {ру('конфета', было)}, {раз} ушли в красную вазу и {два} в синюю, "
                f"сколько конфет осталось? {выкладка}.")
    if ф == 1:
        return (f"у {кого(ру_имя)} было {было} {ру('конфета', было)}, {раз} ушли в красную вазу и {два} в синюю; "
                f"осталось {s} {ру('конфета', s)}: {выкладка}.")
    if ф == 2:
        return (f"{имя} had {было} candies, put {раз} in the red bowl and {два} in the blue bowl; {имя} does not have {s + два} candies left: "
                f"{имя} has {s}, because {выкладка}.")
    return (f"if {имя} had {было} candies, put {раз} in the red bowl and {два} in the blue bowl, "
            f"how many candies does {имя} have left? {выкладка}.")


# ---------- 18. how many more on one day than on the other: posts painted ----------
# «ВЧЕРА» И «СЕГОДНЯ», А НЕ ДНИ НЕДЕЛИ: «Вера в субботу покрасила» закон соседа лица
# (`actors.порча_соседа`) зовёт порчей — за «лицо в» свод ставил лишь объявленное, и незнакомое
# «субботу» на этом месте неотличимо от обрезка имени. Закон прав; наречие места не занимает.
def п_разница(шаг, i):
    x, y = 4 + (шаг * 3 + i) % 12, 2 + (шаг + i * 5) % 9
    # РАЗНОСТЬ НЕ МЕНЬШЕ ДВУХ: «1 more posts» — ложь согласования, а «1 more»
    # в хвосте суд согласования EN читает как «один при множественном».
    if y >= x - 1:
        y = x - 2
    return dict(x=x, y=y, ответ=x - y)


def разница(шаг, i):
    п = п_разница(шаг, i)
    x, y, d = п["x"], п["y"], п["ответ"]
    имя, ру_имя = ИМЕНА_EN[(шаг + i) % len(ИМЕНА_EN)], ИМЕНА_RU[(шаг + i) % len(ИМЕНА_RU)]
    ф = (шаг + i) % 4
    if ф == 0:
        return (f"{имя} painted {x} {by_count(x, 'posts')} yesterday and {y} {by_count(y, 'posts')} today; "
                f"{имя} painted {d} more posts yesterday than today: {x} − {y} = {d}.")
    if ф == 1 and _ру_вопрос(шаг, i):
        return (f"если {ру_имя} вчера {гл(ру_имя, 'покрасил')} {x} {ру('столб', x)}, а сегодня {y} {ру('столб', y)}, "
                f"на сколько столбов больше вчера, чем сегодня? {x} − {y} = {d}.")
    if ф == 1:
        return (f"{ру_имя} вчера {гл(ру_имя, 'покрасил')} {x} {ру('столб', x)}, а сегодня {y} {ру('столб', y)}; "
                f"вчера на {d} {ру('столб', d)} больше, чем сегодня: {x} − {y} = {d}.")
    if ф == 2:
        return (f"{имя} painted {x} {by_count(x, 'posts')} yesterday and {y} {by_count(y, 'posts')} today; "
                f"{имя} did not paint {d + 1} more posts yesterday than today: {d} more, because {x} − {y} = {d}.")
    return (f"if {имя} painted {x} {by_count(x, 'posts')} yesterday and {y} {by_count(y, 'posts')} today, "
            f"how many more posts did {имя} paint yesterday than today? {x} − {y} = {d}.")


# ---------- 19. price and discount: a ticket for a pupil ----------
def п_скидка(шаг, i):
    цена = 20 + (шаг * 7 + i * 3) % 80
    скидка = 5 + (шаг + i) % 15
    return dict(цена=цена, скидка=скидка, ответ=цена - скидка)


def скидка(шаг, i):
    п = п_скидка(шаг, i)
    ц, с, п_ = п["цена"], п["скидка"], п["ответ"]
    билет = (f"a ticket costs {ц} {by_count(ц, 'dollars')} and pupils get a discount of {с} {by_count(с, 'dollars')} "
             f"on each ticket")
    ф = (шаг + i) % 4
    if ф == 0:
        return f"{билет}; a pupil pays {п_} {by_count(п_, 'dollars')} for a ticket: {ц} − {с} = {п_}."
    if ф == 1 and _ру_вопрос(шаг, i):
        return (f"если билет стоит {ц} {ру('доллар', ц)}, и ученикам на каждый билет скидка {с} {ру('доллар', с)}, "
                f"сколько ученик платит за билет? {ц} − {с} = {п_}.")
    if ф == 1:
        return (f"билет стоит {ц} {ру('доллар', ц)}, и ученикам на каждый билет скидка {с} {ру('доллар', с)}; "
                f"ученик платит за билет {п_} {ру('доллар', п_)}: {ц} − {с} = {п_}.")
    if ф == 2:
        return f"{билет}; a pupil does not pay {ц} {by_count(ц, 'dollars')} for a ticket: a pupil pays {п_}, because {ц} − {с} = {п_}."
    return (f"if {билет}, how much does a pupil pay for a ticket? {ц} {by_count(ц, 'dollars')}: "
            f"{ц} − {с} = {п_} {by_count(п_, 'dollars')}.")


# ---------- 20. left / in all / altogether ----------
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
            return f"{имя} had {x} {by_count(x, en)} and gave away {y}; {имя} does not have {s + 1} {en} left: {имя} has {s}, because {x} − {y} = {s}."
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
        return (f"{имя} has {x} {by_count(x, en)} in one box and {y} {by_count(y, en)} in another; {имя} does not have {s + 1} {en} {слово}: "
                f"{имя} has {s}, because {x} + {y} = {s}.")
    return f"if {имя} has {x} {by_count(x, en)} in one box and {y} {by_count(y, en)} in another, how many {en} does {имя} have {слово}? {x} + {y} = {s}."


# ---------- 21. how many groups of N: plates stacked in piles ----------
def п_группы(шаг, i):
    n = 2 + (шаг + i) % 6
    групп = 2 + (шаг * 3 + i) % 9
    return dict(n=n, всего=n * групп, ответ=групп)


def группы(шаг, i):
    п = п_группы(шаг, i)
    n, всего_, g = п["n"], п["всего"], п["ответ"]
    ф = (шаг + i) % 4
    # «ТАРЕЛОК 21» А НЕ «21 ТАРЕЛКА СЛОЖИЛИ»: число после имени снимает согласование сказуемого,
    # какого счётная форма не знает («21 тарелку сложили», «21 тарелка стоит»).
    if ф == 0:
        return f"there are {всего_} plates and they are stacked in piles of {n}; there are {g} piles: {всего_} ÷ {n} = {g}."
    if ф == 1 and _ру_вопрос(шаг, i):
        return f"если тарелок {всего_} и их сложили стопками по {n}, сколько стопок? {всего_} ÷ {n} = {g}."
    if ф == 1:
        return f"тарелок {всего_}, их сложили стопками по {n}; стопок {g}: {всего_} ÷ {n} = {g}."
    if ф == 2:
        return f"there are {всего_} plates and they are stacked in piles of {n}; there are not {g + 1} piles: there are {g}, because {всего_} ÷ {n} = {g}."
    return f"if there are {всего_} plates and they are stacked in piles of {n}, how many piles are there? {всего_} ÷ {n} = {g}."


# ---------- ОСТАТОК ДЕЛЕНИЯ: коробки не всегда полны ----------
# ЕДИНИЦА ПОКАЗЫВАЕТСЯ ОСТАТКОМ (08.09). Род «группы» делит НАЦЕЛО и потому не может
# показать «1 egg»: всего есть n × g, и при n ≥ 2 остатка нет вовсе. Здесь деление НЕПОЛНОЕ,
# остаток 1 ≤ r < n, и единица стои́т в нём естественно, а не крайним случаем.
#
#     ЧИСЛО, КОТОРОГО ДОМ НЕ ПОРОЖДАЕТ, ЕСТЬ ФОРМА, КОТОРОЙ ОН НЕ ПОКАЗЫВАЕТ.
#
# Леджер идёт ДВУМЯ ПРОСТЫМИ ШАГАМИ (n × g, затем всего − ng), ибо суд арифметики читает
# действие о двух числах.
def п_остаток_деления(шаг, i):
    n = 3 + (шаг + i) % 5
    групп = 2 + (шаг * 3 + i) % 8
    return dict(n=n, групп=групп, ответ=1 + (шаг * 5 + i) % (n - 1),
                всего=n * групп + 1 + (шаг * 5 + i) % (n - 1))


def остаток_деления(шаг, i):
    п = п_остаток_деления(шаг, i)
    n, T, g, r = п["n"], п["всего"], п["групп"], п["ответ"]
    ng = n * g
    # ВОПРОС ОБЕИМ СТОРОНАМ, А НЕ ОДНОЙ (08.09): русская сторона спрашивает тоже.
    ф = (шаг + i) % 4
    if ф == 0:
        return (f"there are {T} eggs and they are packed in boxes of {n}; there are {g} full boxes and "
                f"{r} {by_count(r, 'eggs')} left over: {n} × {g} = {ng}, {T} − {ng} = {r}.")
    if ф == 1:
        return (f"яиц {T}, их разложили по коробкам по {n}; полных коробок {g}, и осталось "
                f"{r} {ру('яйцо', r)}: {n} × {g} = {ng}, {T} − {ng} = {r}.")
    if ф == 2:
        return (f"если яиц {T} и их разложили по коробкам по {n}, сколько яиц останется? "
                f"{n} × {g} = {ng}, {T} − {ng} = {r}.")
    return (f"if there are {T} eggs and they are packed in boxes of {n}, how many eggs are left "
            f"over? {n} × {g} = {ng}, {T} − {ng} = {r}.")


# ======================= ТРЕТИЙ СЛОЙ (03.09): роды по массе переписи =======================
# Перепись e9 назвала конструкции, каких свод не держал: (1) «how many more X … than …» —
# крупнейший род; (2) «how many X did A V» при отвлекающих числах — отбор или остаток;
# (3) «how many … are there in …» по частям целого; (4) «how much money …». Дальше —
# сдача, прибыль при дробной цене, завышение на процент, половина и всего. Закон каждой рамки —
# один на показ, стенд и суд; слова родов — таблицами здесь, суд читает их своим замкнутым
# множеством. СЦЕНЫ СВОИ С 23.09: полосы, давшие роду имя, не дают ему больше ни слова.

# --- 22. how many more … than …: четыре очертания одного закона d = x − y > 0 ---
БОЛЬШЕ_A = (  # одна вещь на двух сроках: (глагол прош., основа, вещь, вещь RU, глагол RU)
    ("picked", "pick", "plums", "слива", "собрал"),
    ("washed", "wash", "plates", "тарелка", "вымыл"),
    ("wrote", "write", "letters", "письмо", "написал"),
    ("painted", "paint", "posts", "столб", "покрасил"),
    ("sold", "sell", "tickets", "билет", "продал"),
    ("baked", "bake", "pies", None, None),
    ("counted", "count", "ducks", "утка", "насчитал"),
    ("fed", "feed", "rabbits", None, None),
    ("collected", "collect", "shells", "ракушка", "собрал"),
    ("folded", "fold", "napkins", None, None),
    ("carried", "carry", "boxes", None, None),
    ("scored", "score", "points", None, None),
    ("found", "find", "mushrooms", None, None),
    ("drew", "draw", "pictures", None, None),
)
КОГДА = (("in the morning", "in the evening", "утром", "вечером"),
         ("on Saturday", "on Sunday", "в субботу", "в воскресенье"))
БОЛЬШЕ_B = (  # две вещи одним делом: (глагол прош., основа, вещь1, вещь2, глагол RU, RU1, RU2)
    ("bought", "buy", "kilograms of apples", "kilograms of plums", "купил", ("килограмм", " яблок"), ("килограмм", " слив")),
    # «write» берёт ПИСЬМЕННОЕ (`verbthings`): открытка там зовётся «cards», и «wrote postcards» дверь
    # отвергает по праву объявления — вещь берётся та, какую глагол берёт, а не та, что пришла на ум
    ("wrote", "write", "letters", "cards", "написал", ("письмо", ""), ("открытка", "")),
    ("painted", "paint", "tables", "posts", "покрасил", ("стол", ""), ("столб", "")),
    ("collected", "collect", "shells", "stones", "собрал", ("ракушка", ""), ("камень", "")),
    ("washed", "wash", "cups", "plates", "вымыл", ("чашка", ""), ("тарелка", "")),
    ("baked", "bake", "pies", "cakes", None, None, None),
    ("sold", "sell", "roses", "tulips", None, None, None),
    ("picked", "pick", "pears", "plums", "собрал", ("груша", ""), ("слива", "")),
)
# ДВА ДЕЯТЕЛЯ, ОДНО ДЕЛО: (деятель 1, деятель 2, глагол прош., основа, вещь)
БОЛЬШЕ_E = (
    ("the red team", "the blue team", "scored", "score", "points"),
    ("the old pump", "the new pump", "filled", "fill", "buckets"),
    ("the owl", "the fox", "caught", "catch", "mice"),
    ("the first boat", "the second boat", "carried", "carry", "passengers"),
    ("Grace", "Hugo", "baked", "bake", "pies"),
    ("Ida", "Omar", "sold", "sell", "tickets"),
)
БОЛЬШЕ_C = (  # «there were A and B где»: (A, B, где, A RU, B RU, где RU)
    ("apples", "pears", "in the basket", "яблоко", "груша", "в корзине"),
    ("ducks", "swans", "on the lake", None, None, None),
)
БОЛЬШЕ_D = (  # деньги: (на что 1, на что 2, RU 1, RU 2)
    ("on train tickets", "on lunch", "на билеты", "на обед"),
    ("on paint", "on brushes", "на краску", "на кисти"),
)


def п_больше(шаг, i):
    x = 4 + (шаг * 3 + i) % 12
    y = 2 + (шаг + i * 5) % (x - 3)  # y ≤ x − 2: разность не меньше двух
    очертание = (шаг + i) % 5
    k = (шаг * 3 + i) // 5
    ряд = (БОЛЬШЕ_A, БОЛЬШЕ_B, БОЛЬШЕ_C, БОЛЬШЕ_D, БОЛЬШЕ_E)[очертание]
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
            return f"{имя} {г} {x} {в} {к1} and {y} {в} {к2}; {имя} did not {г0} {d + 1} more {в} {к1} than {к2}: {d} more, because {x} − {y} = {d}."
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
            return f"{имя} {г} {x} {в1} and {y} {в2}; {имя} did not {г0} {d + 1} more {в1} than {в2}: {d} more, because {x} − {y} = {d}."
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
            return f"there were {x} {a} and {y} {b} {где}; there were not {d + 1} more {a} than {b}: {d} more, because {x} − {y} = {d}."
        return f"if there were {x} {a} and {y} {b} {где}, how many more {a} than {b} were there? {x} − {y} = {d}."
    if оч == 4:
        д1, д2, г, г0, в = п["слова"]
        if ф == 0:
            return f"{д1} {г} {x} {в} and {д2} {г} {y} {в}; {д1} {г} {d} more {в} than {д2}: {x} − {y} = {d}."
        if ф == 1:
            return f"if {д1} {г} {x} {в} and {д2} {г} {y} {в}, how many fewer {в} did {д2} {г0} than {д1}? {x} − {y} = {d}."
        if ф == 2:
            return f"{д1} {г} {x} {в} and {д2} {г} {y} {в}; {д1} did not {г0} {d + 1} more {в} than {д2}: {d} more, because {x} − {y} = {d}."
        return f"if {д1} {г} {x} {в} and {д2} {г} {y} {в}, how many more {в} did {д1} {г0} than {д2}? {x} − {y} = {d}."
    на1, на2, р1, р2 = п["слова"]
    if ф == 0:
        return f"{имя} spent {x} {by_count(x, 'dollars')} {на1} and {y} {by_count(y, 'dollars')} {на2}; {имя} spent {d} {by_count(d, 'dollars')} more {на1} than {на2}: {x} − {y} = {d}."
    if ф == 1 and _ру_вопрос(шаг, i):
        return f"если {ру_имя} {гл(ру_имя, 'потратил')} {x} {ру('доллар', x)} {р1} и {y} {ру('доллар', y)} {р2}, на сколько долларов больше потрачено {р1}, чем {р2}? {x} − {y} = {d}."
    if ф == 1:
        return f"{ру_имя} {гл(ру_имя, 'потратил')} {x} {ру('доллар', x)} {р1} и {y} {ру('доллар', y)} {р2}; {р1} на {d} {ру('доллар', d)} больше, чем {р2}: {x} − {y} = {d}."
    if ф == 2:
        return f"{имя} spent {x} {by_count(x, 'dollars')} {на1} and {y} {by_count(y, 'dollars')} {на2}; {имя} did not spend {d + 1} {by_count(d + 1, 'dollars')} more {на1} than {на2}: {d} more, because {x} − {y} = {d}."
    return f"if {имя} spent {x} {by_count(x, 'dollars')} {на1} and {y} {by_count(y, 'dollars')} {на2}, how much more money did {имя} spend {на1} than {на2}? {x} − {y} = {d} {by_count(d, 'dollars')}."


# --- 23. отбор среди отвлекающих чисел: how many X did A V on Tuesday ---
ОТБОР = (  # (глагол прош., основа, вещь, глагол RU, вещь RU)
    ("picked", "pick", "plums", "собрал", "слива"),
    ("washed", "wash", "cups", "вымыл", "чашка"),
    ("sold", "sell", "tickets", "продал", "билет"),
    ("counted", "count", "boats", None, None),
    ("fed", "feed", "rabbits", None, None),
)
СРОКИ = ("on Monday", "on Tuesday", "on Wednesday")
СРОКИ_RU = ("в понедельник", "во вторник", "в среду")


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
    дни = f"{a} {в} {СРОКИ[0]}, {b} {СРОКИ[1]} and {c} {СРОКИ[2]}"
    ф = ((шаг + i) // 4 + шаг) % 4
    чужое = (a, b, c)[(срок + 1) % 3]
    if ф == 0:
        return f"{имя} {г} {дни}; {когда} {имя} {г} {отв} {в}."
    if ф == 1 and _ру_вопрос(шаг, i) and в_ру is not None:
        return (f"если {ру_имя} {гл(ру_имя, г_ру)} {СРОКИ_RU[0]} {a} {ру(в_ру, a)}, {СРОКИ_RU[1]} {b} и {СРОКИ_RU[2]} {c}, "
                f"сколько {ру(в_ру, 5)} {ру_имя} {гл(ру_имя, г_ру)} {СРОКИ_RU[срок]}? {отв} {СРОКИ_RU[срок]}.")
    if ф == 1:
        if в_ру is None:
            return f"if {имя} {г} {дни}, how many {в} did {имя} {г0} in all? {a} + {b} + {c} = {a + b + c}."
        return (f"{ру_имя} {гл(ру_имя, г_ру)} {СРОКИ_RU[0]} {a} {ру(в_ру, a)}, {СРОКИ_RU[1]} {b} и {СРОКИ_RU[2]} {c}; "
                f"{СРОКИ_RU[срок]} {ру_имя} {гл(ру_имя, г_ру)} {отв} {ру(в_ру, отв)}.")
    if ф == 2:
        return f"{имя} {г} {дни}; {имя} did not {г0} {чужое} {в} {когда}: {имя} {г} {отв}."
    return f"if {имя} {г} {дни}, how many {в} did {имя} {г0} {когда}? {отв} {когда}."


# --- 24. остаток при отвлекающем: how many apples would the gardener still have ---
def п_остаток(шаг, i):
    n = 10 + (шаг * 7 + i * 3) % 40
    m = 5 + (шаг + i * 5) % 30
    k = 2 + (шаг * 3 + i) % 8
    свои = (шаг + i) % 2 == 1  # продано СВОЁ (яблоки) или чужое (груши)
    return dict(n=n, m=m, k=k, свои=свои, ответ=n - k if свои else n)


def остаток(шаг, i):
    п = п_остаток(шаг, i)
    n, m, k, свои, r = п["n"], п["m"], п["k"], п["свои"], п["ответ"]
    что = "apples" if свои else "pears"
    что_ру = ру("яблоко", k) if свои else ру("груша", k)
    основание = f"{n} − {k} = {r}" if свои else "the pears sold are not apples"
    сад = f"the gardener picked {n} apples and {m} pears and sold {k} {что}"
    # ПО-РУССКИ ДЕЯТЕЛЬ — ИМЯ ДОМА ИМЁН, А НЕ «САДОВНИК»: перед «собрал» свод ставит лицо, и
    # закон зачина (`actors.порча`) зовёт иное слово на этом месте порчей — по праву: купи он
    # «садовника», он перестал бы видеть «Вер собрал».
    ру_имя = ИМЕНА_RU[(шаг + i) % len(ИМЕНА_RU)]
    собрал, продал = гл(ру_имя, "собрал"), гл(ру_имя, "продал")
    ф = ((шаг + i) // 2 + шаг) % 4
    if ф == 0:
        return f"{сад}; the gardener still has {r} {by_count(r, 'apples')}: {основание}."
    if ф == 1 and _ру_вопрос(шаг, i):
        return (f"если {ру_имя} {собрал} {n} {ру('яблоко', n)} и {m} {ру('груша', m)} и {продал} {k} {что_ру}, сколько яблок осталось? "
                f"{n} {ру('яблоко', n)}; {m} {ру('груша', m)} не в счёт; {n} − {k} = {r}." if свои else
                f"если {ру_имя} {собрал} {n} {ру('яблоко', n)} и {m} {ру('груша', m)} и {продал} {k} {что_ру}, сколько яблок осталось? "
                f"{n} {ру('яблоко', n)}: проданы груши, не яблоки.")
    if ф == 1:
        осн_ру = f"{n} − {k} = {r}" if свои else "проданы груши, не яблоки"
        return f"{ру_имя} {собрал} {n} {ру('яблоко', n)} и {m} {ру('груша', m)} и {продал} {k} {что_ру}; яблок осталось {r}: {осн_ру}."
    if ф == 2:
        хвост = f", because {n} − {k} = {r}" if свои else ""
        return f"{сад}; the gardener does not still have {r + 1} apples: the gardener has {r}{хвост}."
    if свои:
        return (f"if {сад}, how many apples would the gardener still have? "
                f"{n} apples; the {m} pears do not count; {n} − {k} = {r}.")
    return f"if {сад}, how many apples would the gardener still have? {n} apples; the pears sold are not apples."


# --- 25. части целого: жители двух этажей ---
def п_класс(шаг, i):
    g, b = 5 + (шаг * 3 + i) % 12, 4 + (шаг + i * 5) % 11
    род = (шаг + i) % 2
    return dict(g=g, b=b, s=g + b, род=род, ответ=g + b if род == 0 else b)


def класс(шаг, i):
    п = п_класс(шаг, i)
    g, b, s, род = п["g"], п["b"], п["s"], п["род"]
    ф = ((шаг + i) // 2 + шаг) % 4
    if род == 0:
        этажи = f"there are {g} residents on the first floor and {b} on the second floor"
        if ф == 0:
            return f"{этажи}; the house has {s} residents: {g} + {b} = {s}."
        if ф == 1 and _ру_вопрос(шаг, i):
            return f"если на первом этаже {g} {ру('житель', g)}, а на втором {b}, сколько жителей в доме? {g} + {b} = {s}."
        if ф == 1:
            return f"на первом этаже {g} {ру('житель', g)}, а на втором {b}; в доме {s} {ру('житель', s)}: {g} + {b} = {s}."
        if ф == 2:
            return f"{этажи}; the house does not have {s + 1} residents: it has {s}, because {g} + {b} = {s}."
        return f"if {этажи}, how many residents does the house have? {g} + {b} = {s}."
    дом = f"the house has {s} residents and {g} of them live on the first floor"
    if ф == 0:
        return f"{дом}; {b} residents live on the second floor: {s} − {g} = {b}."
    if ф == 1 and _ру_вопрос(шаг, i):
        return f"если в доме {s} {ру('житель', s)}, из них {g} живут на первом этаже, сколько жителей на втором этаже? {s} − {g} = {b}."
    if ф == 1:
        return f"в доме {s} {ру('житель', s)}, из них {g} живут на первом этаже; на втором этаже {b} {ру('житель', b)}: {s} − {g} = {b}."
    if ф == 2:
        return f"{дом}; the number of residents on the second floor is not {b + 1}: it is {b}, because {s} − {g} = {b}."
    return f"if {дом}, how many residents live on the second floor? {s} − {g} = {b}."


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
            return f"{имя} bought {n} {by_count(n, en)} at {p} {by_count(p, 'dollars')} each; {имя} spent {отв} {by_count(отв, 'dollars')}: {n} × {p} = {отв}."
        if ф == 1 and _ру_вопрос(шаг, i):
            return f"если {ру_имя} {гл(ру_имя, 'купил')} {n} {ру(вещь, n)} по {p} {ру('доллар', p)}, сколько денег {ру_имя} {гл(ру_имя, 'потратил')}? {n} × {p} = {отв}."
        if ф == 1:
            return f"{ру_имя} {гл(ру_имя, 'купил')} {n} {ру(вещь, n)} по {p} {ру('доллар', p)}; {ру_имя} {гл(ру_имя, 'потратил')} {отв} {ру('доллар', отв)}: {n} × {p} = {отв}."
        if ф == 2:
            return (f"{имя} bought {n} {by_count(n, en)} at {p} {by_count(p, 'dollars')} each; {имя} did not spend {отв + p} {by_count(отв + p, 'dollars')}: "
                    f"{имя} spent {отв}, because {n} × {p} = {отв}.")
        return f"if {имя} bought {n} {by_count(n, en)} at {p} {by_count(p, 'dollars')} each, how much money did {имя} spend? {n} × {p} = {отв} {by_count(отв, 'dollars')}."
    if ф == 0:
        return f"{имя} had {a} {by_count(a, 'dollars')} and spent {b} {by_count(b, 'dollars')}; {имя} has {отв} {by_count(отв, 'dollars')} left: {a} − {b} = {отв}."
    if ф == 1 and _ру_вопрос(шаг, i):
        return f"если у {кого(ру_имя)} было {a} {ру('доллар', a)}, а {ру_имя} {гл(ру_имя, 'потратил')} {b} {ру('доллар', b)}, сколько денег осталось? {a} − {b} = {отв}."
    if ф == 1:
        return f"у {кого(ру_имя)} было {a} {ру('доллар', a)}, {ру_имя} {гл(ру_имя, 'потратил')} {b} {ру('доллар', b)}; осталось {отв} {ру('доллар', отв)}: {a} − {b} = {отв}."
    if ф == 2:
        return (f"{имя} had {a} {by_count(a, 'dollars')} and spent {b} {by_count(b, 'dollars')}; {имя} does not have {отв + 1} {by_count(отв + 1, 'dollars')} left: "
                f"{имя} has {отв}, because {a} − {b} = {отв}.")
    return f"if {имя} had {a} {by_count(a, 'dollars')} and spent {b} {by_count(b, 'dollars')}, how much money is left? {a} − {b} = {отв} {by_count(отв, 'dollars')}."


# --- 27. сдача: n купюр по b за вещь ценой p — лампа ---
def п_сдача(шаг, i):
    n = 2 + (шаг + i) % 4
    b = (5, 10, 20, 50)[(шаг * 3 + i) % 4]
    p = n * b - (2 + (шаг + i * 3) % (n * b - 2))
    return dict(n=n, b=b, p=p, ответ=n * b - p)


def сдача(шаг, i):
    п = п_сдача(шаг, i)
    n, b, p, c = п["n"], п["b"], п["p"], п["ответ"]
    имя, ру_имя = ИМЕНА_EN[(шаг + i) % len(ИМЕНА_EN)], ИМЕНА_RU[(шаг + i) % len(ИМЕНА_RU)]
    лампа = f"a lamp costs {p} {by_count(p, 'dollars')} and {имя} hands over {n} {b}-dollar bills"
    ф = (шаг + i) % 4
    if ф == 0:
        return f"{лампа}; the change is {c} {by_count(c, 'dollars')}: {n} × {b} − {p} = {c}."
    if ф == 1 and _ру_вопрос(шаг, i):
        return (f"если лампа стоит {p} {ру('доллар', p)}, а {ру_имя} даёт {n} {ру('купюра', n)} по {b} {ру('доллар', b)}, "
                f"какова сдача? {n} × {b} − {p} = {c}.")
    if ф == 1:
        return (f"лампа стоит {p} {ру('доллар', p)}, {ру_имя} даёт {n} {ру('купюра', n)} по {b} {ру('доллар', b)}; "
                f"сдача {c} {ру('доллар', c)}: {n} × {b} − {p} = {c}.")
    if ф == 2:
        return f"{лампа}; the change is not {c + 1} {by_count(c + 1, 'dollars')}: it is {c}, because {n} × {b} − {p} = {c}."
    return f"if {лампа}, how much change does {имя} get? {n} × {b} − {p} = {c} {by_count(c, 'dollars')}."


# --- 28. прибыль при цене a/b от закупочной — велосипед ---
# ДРОБИ СВОИ: одиннадцать восьмых, стоявшие здесь, были дробью самой задачи полосы.
ДРОБИ = ((5, 4), (7, 5), (3, 2), (9, 8), (4, 3))


def п_прибыль(шаг, i):
    a, b = ДРОБИ[(шаг + i) % len(ДРОБИ)]
    p = b * (3 + (шаг * 3 + i) % 12)
    return dict(a=a, b=b, p=p, ответ=p * a // b - p)


def прибыль(шаг, i):
    п = п_прибыль(шаг, i)
    a, b, p, r = п["a"], п["b"], п["p"], п["ответ"]
    имя, ру_имя = ИМЕНА_EN[(шаг + i) % len(ИМЕНА_EN)], ИМЕНА_RU[(шаг + i) % len(ИМЕНА_RU)]
    магазин = f"{имя} bought a bicycle for {p} {by_count(p, 'dollars')} and sells it at {a}/{b} of that price"
    выкладка = f"{p} × {a} ÷ {b} − {p} = {r}"
    ф = (шаг + i) % 4
    if ф == 0:
        return f"{магазин}; the profit is {r} {by_count(r, 'dollars')}: {выкладка}."
    if ф == 1 and _ру_вопрос(шаг, i):
        return (f"если {ру_имя} {гл(ру_имя, 'купил')} велосипед за {p} {ру('доллар', p)} и продаёт его за {a}/{b} этой цены, "
                f"какова прибыль? {выкладка}.")
    if ф == 1:
        return (f"{ру_имя} {гл(ру_имя, 'купил')} велосипед за {p} {ру('доллар', p)} и продаёт его за {a}/{b} этой цены; "
                f"прибыль {r} {ру('доллар', r)}: {выкладка}.")
    if ф == 2:
        return f"{магазин}; the profit is not {r + 1} {by_count(r + 1, 'dollars')}: it is {r}, because {выкладка}."
    return f"if {магазин}, what is the profit? {выкладка} {by_count(r, 'dollars')}."


# --- 29. завышение на q процентов — гости праздника ---
ЗАВЫШЕНИЯ = ((20, 5), (25, 4), (50, 2), (10, 10))  # (проценты, шаг истинного числа)


def п_завышение(шаг, i):
    q, кратно = ЗАВЫШЕНИЯ[(шаг + i) % len(ЗАВЫШЕНИЯ)]
    r = кратно * (4 + (шаг * 3 + i) % 12)
    return dict(q=q, n=r * (100 + q) // 100, ответ=r)


def завышение(шаг, i):
    п = п_завышение(шаг, i)
    q, n, r = п["q"], п["n"], п["ответ"]
    имя, ру_имя = ИМЕНА_EN[(шаг + i) % len(ИМЕНА_EN)], ИМЕНА_RU[(шаг + i) % len(ИМЕНА_RU)]
    слова = f"{имя} said {n} guests came to the party, overstating the number by {q} percent"
    выкладка = f"{n} × 100 ÷ (100 + {q}) = {r}"
    ф = (шаг + i) % 4
    if ф == 0:
        return f"{слова}; {r} guests really came: {выкладка}."
    if ф == 1 and _ру_вопрос(шаг, i):
        return (f"если {ру_имя} {гл(ру_имя, 'сказал')}, что гостей на празднике было {n}, но {гл(ру_имя, 'завысил')} число "
                f"на {q} {ру('процент', q)}, сколько гостей было на самом деле? {выкладка}.")
    if ф == 1:
        return (f"{ру_имя} {гл(ру_имя, 'сказал')}, что гостей на празднике было {n}, но {гл(ру_имя, 'завысил')} число "
                f"на {q} {ру('процент', q)}; на самом деле гостей было {r}: {выкладка}.")
    if ф == 2:
        return f"{слова}; the real number is not {n}: it is {r}, because {выкладка}."
    return f"if {слова}, how many guests really came? {выкладка}."


# --- 30. половина / кратно и всего — яблоки и груши в корзине ---
КРАТНОСТИ_ВСЕГО = (("half as many", "вдвое меньше", 2, True), ("twice as many", "вдвое больше", 2, False),
                   ("three times as many", "втрое больше", 3, False))


def п_половина(шаг, i):
    слово, слово_ру, k, делить = КРАТНОСТИ_ВСЕГО[(шаг + i) % 3]
    n = 2 * (3 + (шаг * 3 + i) % 12) if делить else 3 + (шаг * 3 + i) % 12
    груш = n // k if делить else n * k
    return dict(слово=слово, слово_ру=слово_ру, k=k, делить=делить, n=n, ответ=n + груш)


def половина(шаг, i):
    п = п_половина(шаг, i)
    слово, слово_ру, k, делить, n, t = п["слово"], п["слово_ру"], п["k"], п["делить"], п["n"], п["ответ"]
    осн = f"{n} + {n} ÷ {k} = {t}" if делить else f"{n} + {n} × {k} = {t}"
    корзина = f"there were {n} apples and {слово} pears as apples in the basket"
    ф = (шаг + i) % 4
    if ф == 0:
        return f"{корзина}; there were {t} apples and pears in all: {осн}."
    if ф == 1 and _ру_вопрос(шаг, i):
        return f"если в корзине было {n} {ру('яблоко', n)} и {слово_ру} груш, сколько всего яблок и груш? {осн}."
    if ф == 1:
        return f"в корзине было {n} {ру('яблоко', n)} и {слово_ру} груш; всего яблок и груш {t}: {осн}."
    if ф == 2:
        return f"{корзина}; there were not {t + 1} apples and pears in all: there were {t}, because {осн}."
    return f"if {корзина}, how many apples and pears were there in all? {осн}."


# ---------- 31. part and its multiple give the whole: the boat and the trailer ----------
def п_части(шаг, i):
    k = (2, 3, 4)[(шаг + i) % 3]
    лот = 10 * (2 + (шаг * 7 + i * 3) % 12)
    # the multiplier by word on even shows, by number on odd
    слово = ("twice", "three times", "four times")[k - 2] if i % 2 == 0 else f"{k} times"
    return dict(k=k, лот=лот, дом=лот * k, всего=лот * (k + 1), слово=слово,
                ру_слово=("вдвое", "втрое", "вчетверо")[k - 2], ответ=лот)


def части(шаг, i):
    п = п_части(шаг, i)
    k, прицеп, лодка, всего, слово, ру_ = п["k"], п["лот"], п["дом"], п["всего"], п["слово"], п["ру_слово"]
    # the whole opens the ledger (М-145: the answer opens with the question's first quantity);
    # the link «k + 1» that made the divisor stands after it. ДВА МЕСТА ЗАКОНУ НЕ ОТДАНЫ (08.09):
    # слово «dollars» стои́т ПОСЛЕ ЛЕДЖЕРА, а не после счёта, и число, правящее формой, было бы
    # ответом, а не последним числом цепи; долг — в самой фразе, где мера прилипла к леджеру.
    прицеп_осн = f"{всего} ÷ {k + 1} = {прицеп}, {k} + 1 = {k + 1}"
    лодка_осн = f"{всего} ÷ {k + 1} = {прицеп}, {прицеп} × {k} = {лодка}"
    пара = f"a boat and a trailer cost {всего} {by_count(всего, 'dollars')} and the boat cost {слово} as much as the trailer"
    ф = (шаг + i) % 4
    if ф == 0:
        return f"{пара}; the trailer cost {прицеп} {by_count(прицеп, 'dollars')}: {прицеп_осн}."
    if ф == 1 and _ру_вопрос(шаг, i):
        return (f"если лодка и прицеп стоили {всего} {ру('доллар', всего)}, а лодка стоила {ру_} дороже прицепа, сколько стоил прицеп? "
                f"{прицеп} {ру('доллар', прицеп)}: {прицеп_осн}.")
    if ф == 1:
        return (f"лодка и прицеп стоили {всего} {ру('доллар', всего)}, а лодка стоила {ру_} дороже прицепа; "
                f"прицеп стоил {прицеп} {ру('доллар', прицеп)}: {прицеп_осн}.")
    if ф == 2:
        return f"{пара}; the boat cost {лодка} {by_count(лодка, 'dollars')}: {лодка_осн}."
    if ((шаг + i) // 4) % 2 == 0:
        return f"if {пара}, how much did the trailer cost? {прицеп_осн} {by_count(прицеп, 'dollars')}."
    return f"if {пара}, how much did the boat cost? {лодка_осн} {by_count(лодка, 'dollars')}."


# ГЛАГОЛЫ ПОЛОС ТОЧКАМИ (e9 04.09, семейство 22: рынок глаголов историй голосует только по
# УТВЕРЖДЕНИЯМ, М-138, а все показы «V N» стояли внутри вопросов и отрицаний). Каждому глаголу —
# утвердительные показы точками, ≥ 2 деятелей и ≥ 2 вещей на глагол: (глагол прош., основа,
# деятели — None значит имена пакета, вещи). Десять глаголов, по два слота на каждый за пять
# проходов. ГЛАГОЛЫ И ВЕЩИ СВОИ С 23.09: прыжки кузнечика, отжимания и выброшенные крышки были
# сценами самой полосы.
ПОЛОСЫ = (
    ("climbed", "climb", ("the goat", "the dog", "the fox"), ("steps", "meters")),
    ("baked", "bake", None, ("pies", "loaves")),
    ("painted", "paint", None, ("posts", "boards")),
    ("picked", "pick", None, ("plums", "pears")),
    ("won", "win", None, ("matches", "races")),
    ("sent", "send", None, ("parcels", "postcards")),
    ("lost", "lose", None, ("buttons", "keys")),
    ("watched", "watch", None, ("films", "plays")),
    ("sold", "sell", ("the bakery", "the cafe", "the shop"), ("cakes",)),
    ("washed", "wash", None, ("cups", "plates")),
)


def п_полосы(шаг, i):
    x = 4 + (шаг * 3 + i) % 12
    y = 2 + (шаг + i * 5) % (x - 3)  # y ≤ x − 2
    слот = шаг * 4 + i // 4          # four forms of one verb in a row
    г, г0, деятели, вещи = ПОЛОСЫ[слот % len(ПОЛОСЫ)]
    if деятели is None:
        д1, д2 = ИМЕНА_EN[слот % len(ИМЕНА_EN)], ИМЕНА_EN[(слот + 5) % len(ИМЕНА_EN)]
    else:
        д1, д2 = деятели[слот % len(деятели)], деятели[(слот + 1) % len(деятели)]
    в = вещи[(слот // len(ПОЛОСЫ)) % len(вещи)]  # the second slot of a verb takes its second thing
    return dict(x=x, y=y, д1=д1, д2=д2, г=г, г0=г0, в=в, ф=i % 4)


# РУССКИЕ ПОЛОСЫ (15.09, последний долг щербатости). Глаголы и вещи взяты СВОИ, а не
# переведённые: английская полоса требовала зверя, чьё имя склоняется, и русская полоса
# берёт вместо зверей ИМЕНА дома, а вместо мер — страницы, письма и монеты, объявленные
# пакетом счётными формами.
#
#     ГЛАГОЛ ПОЛОСЫ СОГЛАСУЕТСЯ С ИМЕНЕМ, А ИМЯ ИМЕЕТ РОД. Оттого всякий глагол объявлен
#     ЗДЕСЬ парой прошедшего, и склеивать «прочитала» из «прочитал» + «а» не нужно: помощник
#     `гл` уже знает и правило, и его исключения.
# МНОЖЕСТВЕННОЕ ПРОШЕДШЕЕ ОБЪЯВЛЕНО ТАМ, ГДЕ ПРАВИЛО ЛОМАЕТСЯ: «нашёл → нашли» теряет «ё»
# вместе с беглой гласной, как и женское «нашла». Прочие основы дома берут правило «-л → -ли».
МНОЖЕСТВЕННОЕ_RU = {"нашёл": "нашли", "испёк": "испекли"}

ПОЛОСЫ_RU = (
    ("прочитал", "прочитать", "страница"),
    ("написал", "написать", "письмо"),
    ("отправил", "отправить", "открытка"),
    ("нашёл", "найти", "монета"),
    ("посмотрел", "посмотреть", "фильм"),
    ("выиграл", "выиграть", "игра"),
    ("купил", "купить", "книга"),
    ("надул", "надуть", "шарик"),
)


def полосы(шаг, i):
    # РОД ЕСТЬ ДЕЛО, А НЕ ЯЗЫК: русская полоса идёт в ТОТ ЖЕ род, что английская.
    if _ру_вопрос(шаг, i):
        return полосы_ru(шаг, i)
    п = п_полосы(шаг, i)
    x, y = п["x"], п["y"]
    d, s = x - y, x + y
    д1, д2, г, г0, в, ф = п["д1"], п["д2"], п["г"], п["г0"], п["в"], п["ф"]
    факты = f"{д1} {г} {x} {в}. {д2} {г} {y} {в}."
    if ф == 0:
        return f"{факты} {д1} {г} {d} more {в} than {д2}: {x} − {y} = {d}."
    if ф == 1:
        return f"{факты} {д2} {г} {d} fewer {в} than {д1}: {x} − {y} = {d}."
    if ф == 2:
        return f"{факты} together they {г} {s} {в}: {x} + {y} = {s}."
    return f"{факты} how many more {в} did {д1} {г0} than {д2}? {x} − {y} = {d}."


def полосы_ru(шаг, i):
    """Та же полоса по-русски: два деятеля, одно дело, четыре поверхности."""
    п = п_полосы(шаг, i)
    x, y = п["x"], п["y"]
    d, s = x - y, x + y
    слот = шаг * 4 + i // 4
    гл_пр, гл_инф, вещь = ПОЛОСЫ_RU[слот % len(ПОЛОСЫ_RU)]
    и1 = ИМЕНА_RU[слот % len(ИМЕНА_RU)]
    и2 = ИМЕНА_RU[(слот + 3) % len(ИМЕНА_RU)]
    ф = i % 4
    факты = (f"{и1} {гл(и1, гл_пр)} {x} {ру(вещь, x)}. "
             f"{и2} {гл(и2, гл_пр)} {y} {ру(вещь, y)}.")
    if ф == 0:
        return (f"{факты} {и1} {гл(и1, гл_пр)} на {d} {ру(вещь, d)} больше, "
                f"чем {и2}: {x} − {y} = {d}.")
    if ф == 1:
        return (f"{факты} {и2} {гл(и2, гл_пр)} на {d} {ру(вещь, d)} меньше, "
                f"чем {и1}: {x} − {y} = {d}.")
    if ф == 2:
        # МНОЖЕСТВЕННОЕ ПРОШЕДШЕЕ НЕ ЕСТЬ ФОРМА ПО РОДУ ИМЕНИ: «вместе они написали» берёт
        # окончание «-и», какого помощник `гл` не знает вовсе.
        мн = МНОЖЕСТВЕННОЕ_RU.get(гл_пр, гл_пр + "и" if гл_пр.endswith("л") else гл_пр)
        return f"{факты} вместе они {мн} {s} {ру(вещь, s)}: {x} + {y} = {s}."
    return (f"{факты} на сколько {ру(вещь, 5)} больше {гл(и1, гл_пр)} {и1}, "
            f"чем {и2}? {x} − {y} = {d}.")


# ФОРМУЛЫ СЕМЕЙСТВ — ЗАКОН ОТВЕТА ОТ ВЕЛИЧИН ВОПРОСА (заказ holon 03.09: таблица
# родов с формулами как эталон суда охвата — какие рамки ДОЛЖНЫ купиться, и
# ложь есть купленная рамка с чужой формулой). Имена величин — имена полей
# функции параметров п_*; формула — то, что пересчитывает суд семейства.
ФОРМУЛЫ = {
    "сумма": "ответ = x + y", "температура": "ответ = t0 ± d (падение: −)", "процент": "ответ = часть × 100 ÷ всего",
    "фунты": "ответ = унц ÷ 16", "глубина": "ответ = v ÷ (w × l)", "вероятность": "ответ = r/(r + b)",
    "четверти": "ответ = часть ÷ k × 4", "дополнение": "ответ = было − ушло", "население": "ответ = всего ÷ доля",
    "команда": "ответ = м + д", "кратно": "ответ = цена × k", "проект": "ответ = старт × k − минус",
    "окружность": "ответ = длина ÷ скорость", "верёвки": "ответ = всего ÷ n", "трое": "ответ = a + (a + больше) + k × a",
    "ставка": "ответ = в_час × часы", "листки": "ответ = было − раз − два", "разница": "ответ = x − y",
    "скидка": "ответ = цена − скидка", "всего": "ответ = x + y (в одной и другой) | x − y (отдал)", "группы": "ответ = всего ÷ n",
    "остаток_деления": "ответ = всего − n × (всего ÷ n), 1 ≤ ответ < n",
    "больше": "ответ = x − y", "отбор": "ответ = величина названного срока (a | b | c)", "остаток": "ответ = n − k (проданы яблоки) | n (проданы груши)",
    "класс": "ответ = g + b | s − g", "деньги": "ответ = n × p | a − b", "сдача": "ответ = n × b − p",
    "прибыль": "ответ = p × a ÷ b − p", "завышение": "ответ = n × 100 ÷ (100 + q)", "половина": "ответ = n + n ÷ k (половина) | n + n × k (кратно)",
    "части": "ответ = всего ÷ (k + 1) (прицеп) | всего ÷ (k + 1) × k (лодка)",
    "полосы": "ответ = x − y (more | fewer) | x + y (together)",
}

СЕМЕЙСТВА = (сумма, температура, процент, фунты, глубина, вероятность, четверти, дополнение,
             население, команда, кратно, проект, окружность, верёвки, трое, ставка, листки,
             разница, скидка, всего, группы, остаток_деления,
             больше, отбор, остаток, класс, деньги, сдача, прибыль, завышение, половина, части, полосы)


# РЕШЕНИЕ СЛОВАМИ (коллегия 03.09, бедность текста): к каждому второму
# вопросу с ответом-уравнением — предложение ответа со связкой: «… 5 + 3 = 8.
# so the answer is 8.» / «… 5 + 3 = 8. значит ответ: 8.» Уравнение уже несёт
# шаги (скобками), ответное предложение закрывает леджер словом.
ОТВЕТ_ПРЕДЛОЖЕНИЕМ = {"en": "so the answer is {n}.", "ru": "значит ответ: {n}."}
ПОСЛЕДНЕЕ_ЧИСЛО = re.compile(r"(−?\d+)\.$")


def язык_показа(показ):
    """Язык страницы — ПО ПИСЬМУ, и это объявленное правило дома, а не догадка прибора (15.09).

    ДОМ ЖИВЁТ ЭТИМ ПРАВИЛОМ С ПЕРВОГО ДНЯ: `с_ответом` выбирает по нему форму предложения
    ответа («значит, ответ: 8» или «so the answer is 8»), и всякая страница мира прошла через
    него. Правило было верно делом — и не было названо именем.

        ПРАВИЛО, ПО КОТОРОМУ ДОМ УЖЕ ЖИВЁТ, ЕСТЬ ОБЪЯВЛЕНИЕ, ДАЖЕ ЕСЛИ ОНО НЕ НАЗВАНО ОТДЕЛЬНО.
        Поднять его до имени — не выдумать новое, а перестать прятать старое.

    ОГОВОРКА, БЕЗ КОТОРОЙ ПРАВИЛО ЛОЖНО: письмо различает языки лишь там, где алфавиты
    РАЗНЫЕ. У этого дома их два — русский и английский, — и кириллица делит их надёжно. Дому с
    девятью латинскими языками такое правило не годилось бы вовсе, и потому оно объявлено
    ЗДЕСЬ, при доме, а не вынесено в общее место.
    """
    return "ru" if re.search(r"[а-яё]", показ) else "en"


# ПРЕДЛОЖЕНИЕ ОТВЕТА ПОВТОРЯЕТ ОТВЕТ, А НЕ ПОСЛЕДНЕЕ ЧИСЛО (23.09). Правило брало последнее
# число страницы и десять страниц мира писали «сколько стоил участок? 50 долларов: 250 ÷ 5 = 50,
# 4 + 1 = 5. значит ответ: 5.» — последний шаг был ЗВЕНОМ (делителем, выведенным после), а суд
# сверял предложение с последним шагом и звал ложь истиной.
#
#     ШАГ, ЧЕЙ ИТОГ УЖЕ СТОЯЛ ЧИСЛОМ В ПРЕЖНЕМ ШАГЕ, ЕСТЬ ЗВЕНО, А НЕ ОТВЕТ; ДРОБЬ — ОТВЕТ, НО
#     НЕ ЧИСЛО. Ни того, ни другого предложение ответа повторять не вправе.
ЧИСЛО_ШАГА = re.compile(r"−?\d+")


def ответ_не_последний(хвост):
    """Последний шаг — звено («650 ÷ 5 = 130, 4 + 1 = 5») или ответ — дробь («4 + 1 = 5: 4/5»)."""
    if re.search(r"\d/\d", хвост):
        return True
    шаги = [ш for ш in хвост.split(", ") if " = " in ш]
    if len(шаги) < 2:
        return False
    итог = ЧИСЛО_ШАГА.findall(шаги[-1].rsplit(" = ", 1)[1])
    прежние = {ч for ш in шаги[:-1] for ч in ЧИСЛО_ШАГА.findall(ш.rsplit(" = ", 1)[0])}
    return bool(итог) and итог[0] in прежние


def с_ответом(показ, шаг, i):
    """Вопрос с уравнением получает предложение ответа (каждый второй)."""
    if "?" not in показ or (шаг * 5 + i) % 2 == 0:
        return показ
    хвост = показ.split("? ")[-1]
    м = ПОСЛЕДНЕЕ_ЧИСЛО.search(показ)
    if not м or " = " not in хвост or ответ_не_последний(хвост):
        return показ
    return показ + " " + ОТВЕТ_ПРЕДЛОЖЕНИЕМ[язык_показа(показ)].format(n=м.group(1))


assert set(ФОРМУЛЫ) == {с.__name__ for с in СЕМЕЙСТВА}, "формула у каждого семейства"

# ------------------------------------------------------------------ ОБЪЯВЛЕНИЕ ДОМА

РОДЫ = tuple(с.__name__ for с in СЕМЕЙСТВА)

ЗАЧЕМ_РОДА = {и: f"семейство задач «{и}»: вопрос с ответом-уравнением" for и in РОДЫ}


# ИМЯ «ГРУППЫ» ЗАНЯТО СТРОИТЕЛЕМ СЕМЕЙСТВА, И ЭТО ЕГО ЗАКОННОЕ МЕСТО (16.09): род зовётся
# по имени функции (`РОДЫ = tuple(с.__name__ …)`), и семейство «группы» — задача о том,
# сколько выйдет групп из целого. Функция ПРОХОДА, назвавшаяся так же, затеняла строителя:
# кортеж `СЕМЕЙСТВА` держал его и потому работал, а имя модуля указывало на другое.
#
#     ДВА ЗНАНИЯ ПОД ОДНИМ СЛОВОМ РАБОТАЮТ, ПОКА ОДНО ИЗ НИХ ВЗЯТО ЗАРАНЕЕ. Уступает имя
#     тот, у кого оно НЕ ЕСТЬ объявление: род объявлен именем строителя, проход — ничем.
def группы_прохода(шаг):
    """[[страница]] — ровно те группы и в том порядке, какими кузница кормит `emit_grouped`."""
    return [[с_ответом(семья(шаг, i), шаг, i) for i in range(16)] for семья in СЕМЕЙСТВА]


def перебор_страниц(шаг):
    """[(страница, род)] — те же группы, но каждая под именем своего строителя."""
    вон = []
    for имя, группа in zip(РОДЫ, группы_прохода(шаг)):
        for с in группа:
            вон.append((с, имя))
    return вон


def _показы():
    """Словарь ПОСТРОЧНО: свод построчен, а показ бывает многострочен."""
    from layer import PASSES                              # noqa: PLC0415
    вон = {}
    for шаг in range(len(PASSES)):
        for с, род in перебор_страниц(шаг):
            for строка in с.split("\n"):
                if строка.rstrip():
                    вон.setdefault(строка.rstrip(), (язык_показа(строка), род))
    return вон


ПОКАЗЫ = _показы()


def _самопроверка_страниц():
    assert set(ЗАЧЕМ_РОДА) == set(РОДЫ), "глосса рода разошлась с объявлением"
    assert all("\n" not in к for к in ПОКАЗЫ), "словарь показов обязан быть построчным"
    пустые = set(РОДЫ) - {р for _я, р in ПОКАЗЫ.values()}
    assert not пустые, f"род объявлен и не кован: {sorted(пустые)}"
    из_перебора = sorted(с for с, _р in перебор_страниц(0))
    из_групп = sorted(с for г in группы_прохода(0) for с in г)
    assert из_перебора == из_групп, "пересборка потеряла или выдумала страницы"


_самопроверка_страниц()
