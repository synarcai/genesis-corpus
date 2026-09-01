#!/usr/bin/env python3
"""GENESIS layer: CONNECTED SPEECH — the joints of reasoning.

THE OWNER NAMED THE DEFECT: after training on GENESIS the speech is
poor. The diagnosis is self-accusing — poverty of speech is the DIRECT
CONSEQUENCE of what bought us total judgeability. The whole corpus is
SHOWS: self-sufficient atoms. The law «a show carries everything it
needs» was applied twice today to fix generators whose line leaned on a
neighbour. That law gave 100% coverage and it forbade the corpus to
JOIN. The organism learned atoms and never learned connection.

MEASURED, NOT GUESSED (omega-e9, 3000 bytes of generated stream):
92 sentences → 64 forms, 30% repeats; ONE frame («how many cookies»)
is 24% of the whole stream; 55% are question frames; NOT ONE coherent
chain fact→question→answer; and the decisive fact — outside bought
genera the organism is COMPLETELY MUTE (60 of 65). It does not produce
forms it was never judged on.

THE LAW IS NOT BROKEN BUT RAISED A FLOOR (holon-e2): the atom becomes a
GROUP, self-sufficient AT THE LEVEL OF THE GROUP. Here a group is ONE
LINE holding two to four sentences — judgeability is preserved (the
court judges the whole line), and connection appears exactly inside it.

FORM AND SUBJECT ARE TOLD APART BY EXECUTION (holon-e2): a SUBJECT has
its own table of facts; a FORM takes as its operand the VERDICT OF A
SUB-COURT. Anaphora, quantifier, connective, modality are FORMS.

EVERY FORM IS BOUGHT BY A COURT THAT EXECUTES IT — and, by verum-6c's
law, a form is bought only when the court executes it AND REJECTS ITS
COUNTERFEIT. A court that never said «no» measured nothing.
"""

import sys
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from layer import emit_grouped  # noqa: E402

# РОД ИМЕНИ ОБЪЯВЛЕН, А НЕ УГАДАН ПО ОКОНЧАНИЮ: местоимение обязано
# согласоваться с единственным доступным антецедентом, и «Пётр… она»
# есть ложь о языке при верной арифметике.
# (имя, РОДИТЕЛЬНЫЙ, местоимение, «у него/неё», англ., he/she)
# Родительный назван, а не отсечён: «у вера» — ошибка того же рода,
# что «после понедельник», и она прошла бы сквозь любой счётный суд.
ЛИЦА = (("вера", "веры", "она", "неё", "vera", "she"),
        ("анна", "анны", "она", "неё", "anna", "she"),
        ("мария", "марии", "она", "неё", "maria", "she"),
        ("пётр", "петра", "он", "него", "peter", "he"),
        ("иван", "ивана", "он", "него", "ivan", "he"),
        ("юрий", "юрия", "он", "него", "yuri", "he"))
ВЕЩИ = (("яблоко", "яблока", "яблок", "apple", "apples"),
        ("книга", "книги", "книг", "book", "books"),
        ("ручка", "ручки", "ручек", "pen", "pens"),
        ("монета", "монеты", "монет", "coin", "coins"),
        ("шарик", "шарика", "шариков", "marble", "marbles"))


def ру_форма(вещь, n):
    один, few, many = вещь[0], вещь[1], вещь[2]
    if n % 10 == 1 and n % 100 != 11:
        return один
    if n % 10 in (2, 3, 4) and n % 100 not in (12, 13, 14):
        return few
    return many


def анафора(шаг):
    """Местоимение вместо имени — связь через предложение."""
    вон = []
    for i in range(24):
        имя, род, он_она, него_неё, en, he_she = ЛИЦА[(i + шаг) % 6]
        вещь = ВЕЩИ[(i + шаг) % 5]
        было = 4 + (i % 7)
        ушло = 1 + (i % 3)
        стало = было - ушло
        вон.append(
            f"у {род} было {было} {ру_форма(вещь, было)}. "
            f"{он_она} отдал{'а' if он_она == 'она' else ''} "
            f"{ушло} {ру_форма(вещь, ушло)}. "
            f"у {него_неё} осталось {стало} {ру_форма(вещь, стало)}."
        )
        вон.append(
            f"{en} had {было} {вещь[4]}. "
            f"{he_she} gave away {ушло} "
            f"{вещь[3] if ушло == 1 else вещь[4]}. "
            f"{he_she} has {стало} {вещь[3] if стало == 1 else вещь[4]} left."
        )
    return вон


def вывод(шаг):
    """«Значит» — связка следования, судимая выводимостью."""
    вон = []
    for i in range(24):
        n = 4 + i + шаг * 2
        d = 2 if n % 2 == 0 else 3
        if n % d:
            n += d - n % d
        вон.append(f"{n} делится на {d}. значит {n} кратно {d}.")
        вон.append(f"{n} is divisible by {d}. therefore {n} "
                   f"is a multiple of {d}.")
        if n % 2 == 0:
            вон.append(f"{n} делится на 2. значит {n} чётно.")
            вон.append(f"{n} is divisible by 2. therefore {n} is even.")
    return вон


def придаточное(шаг):
    """«Который» — предикат внутри имени, исполнимый судом."""
    вон = []
    for i in range(20):
        d = 2 + (i % 4)
        n = d * (2 + (i + шаг) % 6)
        вон.append(f"{n} есть число, которое делится на {d}. "
                   f"{n} ÷ {d} = {n // d}.")
        вон.append(f"{n} is a number that is divisible by {d}. "
                   f"{n} ÷ {d} = {n // d}.")
    return вон


def квантор(шаг):
    """«Все» и «ни один» — пробег с под-судом."""
    вон = []
    for i in range(16):
        a = 2 * (1 + (i + шаг) % 6)
        ряд = [a, a + 2, a + 4]
        один = ряд[(i + шаг) % 3]
        если = ", ".join(str(x) for x in ряд)
        вон.append(f"все числа {если} чётны. {один} — одно из них. "
                   f"значит {один} чётно.")
        вон.append(f"all of {если} are even. {один} is one of them. "
                   f"therefore {один} is even.")
        нечёт = [x + 1 for x in ряд]
        если2 = ", ".join(str(x) for x in нечёт)
        один2 = нечёт[(i + шаг) % 3]
        вон.append(f"ни одно из чисел {если2} не чётно. "
                   f"{один2} — одно из них. значит {один2} не чётно.")
        вон.append(f"none of {если2} are even. {один2} is one of them. "
                   f"therefore {один2} is not even.")
    return вон


def номинализация(шаг):
    """Действие, названное предметом, — вторая поверхность факта."""
    вон = []
    имена = (("сложение", "и", "addition", "and", lambda a, b: a + b, "+"),
             ("умножение", "на", "multiplication", "by",
              lambda a, b: a * b, "×"))
    for i in range(20):
        ру, союз, en, by, действие, глиф = имена[(i + шаг) % 2]
        a, b = 2 + (i % 8) + шаг, 3 + (i % 6)
        вон.append(f"{ру} {a} {союз} {b} даёт {действие(a, b)}. "
                   f"{a} {глиф} {b} = {действие(a, b)}.")
        вон.append(f"the {en} of {a} {by} {b} gives {действие(a, b)}. "
                   f"{a} {глиф} {b} = {действие(a, b)}.")
    return вон


def условия(шаг):
    """Четыре клетки достаточного и необходимого (замысел verum-6c).

    Один свидетель даёт противоположные вердикты двум утверждениям — и
    это в точности то, что значит «разные понятия», ПОКАЗАННОЕ, а не
    объявленное. Четыре клетки, а не две: иначе выучится одна ось.
    """
    вон = []
    for i in range(12):
        k = 2 + (i + шаг) % 4          # делимость на 2k достаточна для чётности
        d = 2 * k
        свидетель = 2 * (1 + (i + шаг) % 5)
        while свидетель % d == 0:
            свидетель += 2
        кратное = d * (1 + (i + шаг) % 3)
        вон.append(f"делимости на {d} достаточно для чётности: "
                   f"{кратное} делится на {d} и {кратное} чётно.")
        вон.append(f"делимость на {d} не необходима для чётности: "
                   f"{свидетель} чётно и на {d} не делится.")
        вон.append(f"divisibility by {d} is sufficient for evenness: "
                   f"{кратное} is divisible by {d} and {кратное} is even.")
        вон.append(f"divisibility by {d} is not necessary for evenness: "
                   f"{свидетель} is even and not divisible by {d}.")
        # ЧЕТВЁРТАЯ КЛЕТКА: и достаточно, и необходимо
        вон.append("делимости на 2 достаточно для чётности и она "
                   "необходима для неё.")
        вон.append("divisibility by 2 is sufficient for evenness and "
                   "necessary for it.")
    return вон


ГРУППЫ = (анафора, вывод, придаточное, квантор, номинализация, условия)


def pass_groups(pass_i):
    return [сделать(pass_i) for сделать in ГРУППЫ]


def main():
    emit_grouped("datasets/genesis_speech.txt", pass_groups)


if __name__ == "__main__":
    main()
