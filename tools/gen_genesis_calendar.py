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
МЕСЯЦЫ_EN = ("january", "february", "march", "april", "may", "june",
             "july", "august", "september", "october", "november",
             "december")
# ДЛИНЫ ОБЪЯВЛЕНЫ ФАКТОМ: их нельзя вывести, их знают. Февраль назван
# в невисокосном году — и это СКАЗАНО, а не умолчано.
ДЛИНЫ = (31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31)
assert len(ДНИ_RU) == len(ДНИ_EN) == len(ДНИ_RU_РОД) == 7
assert len(МЕСЯЦЫ_RU_РОД) == 12
assert len(ДНИ_RU_ТВОР) == len(ДНИ_RU_БЫЛ) == 7
assert len(МЕСЯЦЫ_RU) == len(МЕСЯЦЫ_EN) == len(ДЛИНЫ) == 12
assert sum(ДЛИНЫ) == 365


def дни(шаг):
    """Сдвиг по кругу недели — сравнение по модулю семь в одежде."""
    вон = []
    for i in range(7):
        for k in (1, 2, 3, 4, 5, 6):
            j = (i + k) % 7
            # ФОРМА ИДЁТ ЗА ЧИСЛОМ И ПО-АНГЛИЙСКИ: «1 days after» —
            # ошибка, которую суд согласования поймал в тот же прогон.
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
        вон.append(f"the first {i + 1} months of a common year "
                   f"have {сумма} days in all.")
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


ГРУППЫ = (дни, соседи, месяцы, годом, колесо_парой)


def pass_groups(pass_i):
    return [сделать(pass_i) for сделать in ГРУППЫ]


def main():
    emit_grouped("datasets/genesis_calendar.txt", pass_groups)


if __name__ == "__main__":
    main()
