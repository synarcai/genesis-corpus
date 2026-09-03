#!/usr/bin/env python3
"""GENESIS layer: CALENDAR — cyclic arithmetic in its applied genus.

Neither a weekday nor a month appeared anywhere in the corpus. This is
not a decoration missing: the week is the first CYCLIC structure a
child meets, and «what day comes four days after Wednesday» is
congruence modulo 7 wearing clothes. A corpus that teaches `17 mod 5`
and cannot answer that question has taught the symbol and not the
thing.

THE CYCLE IS COMPUTED, NEVER LISTED. Day names and month lengths are
declared (they are facts of a calendar, not derivable), but every
answer is derived from them by modular arithmetic — the same operation
the number layer shows bare.
"""

import sys
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import units  # noqa: E402
from layer import emit_grouped  # noqa: E402

# ПАДЕЖ НАЗЫВАЕТСЯ, А НЕ ОТСЕКАЕТСЯ. «после понедельник» и «через 3
# дней» — ошибки того рода, что суд согласования ловит немедленно, и
# корпус, их содержащий, учит неверному языку с полной судимостью.
# Родительный дан рядом с именительным, как всюду в корпусе.
ДНИ_RU = ("понедельник", "вторник", "среда", "четверг",
          "пятница", "суббота", "воскресенье")
ДНИ_RU_РОД = ("понедельника", "вторника", "среды", "четверга",
              "пятницы", "субботы", "воскресенья")
# ТВОРИТЕЛЬНЫЙ ПОСЛЕ «ПЕРЕД» И РОД СВЯЗКИ — оба названы. «перед суббота
# был пятница» неверно дважды: падеж и род. Ни то, ни другое не
# выводится из формы, и оба стоят рядом с именительным.
ДНИ_RU_ТВОР = ("понедельником", "вторником", "средой", "четвергом",
               "пятницей", "субботой", "воскресеньем")
ДНИ_RU_БЫЛ = ("был", "был", "была", "был", "была", "была", "было")
ДЕНЬ_СЧЁТ = ("день", "дня", "дней")
МЕСЯЦ_СЧЁТ = ("месяц", "месяца", "месяцев")
ПЕРВЫЕ = ("первый", "первые")
ДНИ_EN = ("monday", "tuesday", "wednesday", "thursday",
          "friday", "saturday", "sunday")
МЕСЯЦЫ_RU = ("январь", "февраль", "март", "апрель", "май", "июнь",
             "июль", "август", "сентябрь", "октябрь", "ноябрь", "декабрь")
МЕСЯЦЫ_RU_РОД = ("января", "февраля", "марта", "апреля", "мая", "июня",
                 "июля", "августа", "сентября", "октября", "ноября",
                 "декабря")
# ТВОРИТЕЛЬНЫЙ МЕСЯЦЕВ — для вопроса «какой месяц перед апрелем?».
# Объявлен рукой и сверен парадигмой ниже, как и творительный дней.
МЕСЯЦЫ_RU_ТВОР = ("январём", "февралём", "мартом", "апрелем", "маем",
                  "июнем", "июлем", "августом", "сентябрём",
                  "октябрём", "ноябрём", "декабрём")
МЕСЯЦЫ_EN = ("january", "february", "march", "april", "may", "june",
             "july", "august", "september", "october", "november",
             "december")
# ДЛИНЫ ОБЪЯВЛЕНЫ ФАКТОМ: их нельзя вывести, их знают. Февраль назван
# в невисокосном году — и это СКАЗАНО, а не умолчано.
ДЛИНЫ = (31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31)
assert len(ДНИ_RU) == len(ДНИ_EN) == len(ДНИ_RU_РОД) == 7
assert len(МЕСЯЦЫ_RU_РОД) == len(МЕСЯЦЫ_RU_ТВОР) == 12
assert len(ДНИ_RU_ТВОР) == len(ДНИ_RU_БЫЛ) == 7
assert len(МЕСЯЦЫ_RU) == len(МЕСЯЦЫ_EN) == len(ДЛИНЫ) == 12
assert sum(ДЛИНЫ) == 365
# ВСТРОЕННЫЙ ОРАКУЛ: то же самое сказано ДВАЖДЫ и разными руками —
# здесь семьёй календаря, там парадигмой русской грамматики. Две
# независимые записи одного факта ловят описку в любой из них; сборка
# отказывает, а не выпускает мир с неверным падежом.
_г = __import__("rugram")
for _и, _д in enumerate(ДНИ_RU):
    assert ДНИ_RU_РОД[_и] == _г.ПАРАДИГМЫ[_д][1], _д
    assert ДНИ_RU_ТВОР[_и] == _г.ПАРАДИГМЫ[_д][4], _д
for _и, _м in enumerate(МЕСЯЦЫ_RU):
    assert МЕСЯЦЫ_RU_РОД[_и] == _г.ПАРАДИГМЫ[_м][1], _м
    assert МЕСЯЦЫ_RU_ТВОР[_и] == _г.ПАРАДИГМЫ[_м][4], _м


def леджер_круга(i, k, язык):
    """THE LEDGER OF THE CYCLE (holon 03.09, ONE-CARRIER — the head of the
    answer stays, the chain after the colon is its witness; NOT YET WRITTEN in
    en/ru — the market of cycles reads it first, see дни()): the day numbers
    of the week are declared («monday is day number 1 of the week»), so the
    step is arithmetic on them — «2 + 3 = 5, day 5 is friday», and over the
    edge «6 + 3 = 9, 9 − 7 = 2, day 2 is tuesday»."""
    s = i + 1 + k
    j = s - 7 if s > 7 else s
    имя = ДНИ_EN[j - 1] if язык == "en" else ДНИ_RU[j - 1]
    шаги = [f"{i + 1} + {k} = {s}"] + ([f"{s} − 7 = {j}"] if s > 7 else [])
    хвост = f"day {j} is {имя}" if язык == "en" else f"день {j} — {имя}"
    return ", ".join(шаги + [хвост])


def дни(шаг):
    """Сдвиг по кругу недели — сравнение по модулю семь в одежде."""
    вон = []
    for i in range(7):
        for k in (1, 2, 3, 4, 5, 6):
            j = (i + k) % 7
            # ФОРМА ИДЁТ ЗА ЧИСЛОМ И ПО-АНГЛИЙСКИ: «1 days after» —
            # ошибка, которую суд согласования поймал в тот же прогон.
            # THE LEDGER OF THE CYCLE (леджер_круга) WAITS FOR THE MARKET OF
            # CYCLES (holon 03.09: the wheel is read from the whole telling and
            # stumbles on the numbers of the chain — his road first; the eight
            # languages of calendar_langs already carry it)
            вон.append(f"{k} {'day' if k == 1 else 'days'} after "
                       f"{ДНИ_EN[i]} comes {ДНИ_EN[j]}.")
            вон.append(f"через {k} {units.ру_форма(ДЕНЬ_СЧЁТ, k)} после "
                       f"{ДНИ_RU_РОД[i]} наступает {ДНИ_RU[j]}.")
    return вон


def соседи(шаг):
    вон = []
    for i in range(7):
        сл, пр = (i + 1) % 7, (i - 1) % 7
        вон.append(f"the day after {ДНИ_EN[i]} is {ДНИ_EN[сл]}.")
        вон.append(f"день после {ДНИ_RU_РОД[i]} — это {ДНИ_RU[сл]}.")
        вон.append(f"the day before {ДНИ_EN[i]} is {ДНИ_EN[пр]}.")
        вон.append(f"день перед {ДНИ_RU[i]} — это {ДНИ_RU[пр]}.")
        вон.append(f"{ДНИ_EN[i]} is day number {i + 1} of the week.")
        вон.append(f"{ДНИ_RU[i]} — день номер {i + 1} недели.")
    return вон


def вопросы(шаг):
    """ЗНАНИЕ, У КОТОРОГО НЕТ ВОПРОСНОЙ ПОВЕРХНОСТИ, НЕ ОТВЕЧАЕТ.

    Проба на обученном организме дала немоту ровно на вопросах:
    «what day comes after tuesday?», «какой день после пятницы?» — при
    том что круг недели живёт в корпусе сотнями показов. Утверждение
    сообщает; отвечает вопрос со своим ответом. Здесь тот же круг
    сказан второй поверхностью, и косвенные формы («после пятницы» —
    родительный, «перед пятницей» — творительный) взяты из семей,
    сверенных с парадигмой русской грамматики.
    """
    вон = []
    for i in range(7):
        сл, пр = (i + 1) % 7, (i - 1) % 7
        вон.append(f"what day comes after {ДНИ_EN[i]}? after "
                   f"{ДНИ_EN[i]} comes {ДНИ_EN[сл]}.")
        вон.append(f"what day comes before {ДНИ_EN[i]}? before "
                   f"{ДНИ_EN[i]} comes {ДНИ_EN[пр]}.")
        вон.append(f"какой день после {ДНИ_RU_РОД[i]}? после "
                   f"{ДНИ_RU_РОД[i]} — {ДНИ_RU[сл]}.")
        вон.append(f"какой день перед {ДНИ_RU_ТВОР[i]}? перед "
                   f"{ДНИ_RU_ТВОР[i]} — {ДНИ_RU[пр]}.")
        for k in (2, 3, 4, 5):
            j = (i + k) % 7
            вон.append(f"what day is {k} days after {ДНИ_EN[i]}? "
                       f"{k} days after {ДНИ_EN[i]} comes {ДНИ_EN[j]}.")
            ф = units.ру_форма(ДЕНЬ_СЧЁТ, k)
            вон.append(f"какой день через {k} {ф} после "
                       f"{ДНИ_RU_РОД[i]}? через {k} {ф} после "
                       f"{ДНИ_RU_РОД[i]} — {ДНИ_RU[j]}.")
    for i in range(12):
        сл, пр = (i + 1) % 12, (i - 1) % 12
        вон.append(f"what month comes after {МЕСЯЦЫ_EN[i]}? after "
                   f"{МЕСЯЦЫ_EN[i]} comes {МЕСЯЦЫ_EN[сл]}.")
        вон.append(f"what month comes before {МЕСЯЦЫ_EN[i]}? before "
                   f"{МЕСЯЦЫ_EN[i]} comes {МЕСЯЦЫ_EN[пр]}.")
        вон.append(f"какой месяц после {МЕСЯЦЫ_RU_РОД[i]}? после "
                   f"{МЕСЯЦЫ_RU_РОД[i]} — {МЕСЯЦЫ_RU[сл]}.")
        вон.append(f"какой месяц перед {МЕСЯЦЫ_RU_ТВОР[i]}? перед "
                   f"{МЕСЯЦЫ_RU_ТВОР[i]} — {МЕСЯЦЫ_RU[пр]}.")
    return вон


def месяцы(шаг):
    вон = []
    for i in range(12):
        вон.append(f"{МЕСЯЦЫ_EN[i]} is month number {i + 1} "
                   f"and has {ДЛИНЫ[i]} days.")
        вон.append(f"{МЕСЯЦЫ_RU[i]} — месяц номер {i + 1}, в нём "
                   f"{ДЛИНЫ[i]} {units.ру_форма(ДЕНЬ_СЧЁТ, ДЛИНЫ[i])}.")
        сл = (i + 1) % 12
        вон.append(f"the month after {МЕСЯЦЫ_EN[i]} is {МЕСЯЦЫ_EN[сл]}.")
        вон.append(f"месяц после {МЕСЯЦЫ_RU_РОД[i]} — "
                   f"это {МЕСЯЦЫ_RU[сл]}.")
    return вон


def годом(шаг):
    """Год как сумма месяцев — счёт, а не заученное число."""
    вон = []
    for i in range(12):
        сумма = sum(ДЛИНЫ[:i + 1])
        # СЧЁТ ПРАВИТ ФОРМОЙ И СЛОВА, И ГЛАГОЛА: «the first month … has»,
        # «the first 2 months … have» — суд английского числа нашёл в
        # этом мире «the first 1 months», единственную ложь языка свода.
        вон.append(("the first month of a common year has" if i == 0 else
                    f"the first {i + 1} months of a common year have")
                   + f" {сумма} days in all.")
        сколько = i + 1
        вон.append(f"{ПЕРВЫЕ[0] if сколько == 1 else ПЕРВЫЕ[1]} {сколько} "
                   f"{units.ру_форма(МЕСЯЦ_СЧЁТ, сколько)} обычного года "
                   f"дают {сумма} {units.ру_форма(ДЕНЬ_СЧЁТ, сумма)} всего.")
    вон.append("a common year has 365 days and 52 full weeks.")
    вон.append("обычный год имеет 365 дней и 52 полных недели.")
    return вон


def колесо_парой(шаг):
    """РУССКОЕ КОЛЕСО ГРУППОВЫМ РОДОМ (по запросу holon-e2).

    Два предложения одной строкой: сегодняшний день назван, следующий
    выведен — и связь между ними живёт ВНУТРИ показа, как в слое речи.
    Падеж после «после» родительный, и он объявлен, а не отсечён:
    мост падежей, которого ждало русское колесо.
    """
    вон = []
    for i in range(7):
        сл = (i + 1) % 7
        пр = (i - 1) % 7
        вон.append(f"сегодня {ДНИ_RU[i]}. после {ДНИ_RU_РОД[i]} — "
                   f"{ДНИ_RU[сл]}.")
        вон.append(f"сегодня {ДНИ_RU[i]}. перед {ДНИ_RU_ТВОР[i]} "
                   f"{ДНИ_RU_БЫЛ[пр]} {ДНИ_RU[пр]}.")
        вон.append(f"today is {ДНИ_EN[i]}. after {ДНИ_EN[i]} comes "
                   f"{ДНИ_EN[сл]}.")
        вон.append(f"today is {ДНИ_EN[i]}. before {ДНИ_EN[i]} was "
                   f"{ДНИ_EN[пр]}.")
    return вон


ГРУППЫ = (дни, соседи, вопросы, месяцы, годом, колесо_парой)


def pass_groups(pass_i):
    return [сделать(pass_i) for сделать in ГРУППЫ]


def main():
    emit_grouped("datasets/genesis_calendar.txt", pass_groups)


if __name__ == "__main__":
    main()
