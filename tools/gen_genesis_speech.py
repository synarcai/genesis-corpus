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
# ВИНИТЕЛЬНЫЙ ОБЪЯВЛЕН ОТДЕЛЬНО. «она отдала 1 книга» — именительный
# там, где нужен винительный: ошибка, найденная omega-e9 глазами в моём
# же слое, и ровно того рода, о котором сам слой учит («верно по счёту,
# ложно по языку»). Женский род меняет окончание, средний и мужской
# неодушевлённый — нет, и это НАЗВАНО, а не выведено правилом.
# (именительный, два-четыре, пять+, ВИНИТЕЛЬНЫЙ ед., англ. ед., мн.)
ВЕЩИ = (("яблоко", "яблока", "яблок", "яблоко", "apple", "apples"),
        ("книга", "книги", "книг", "книгу", "book", "books"),
        ("ручка", "ручки", "ручек", "ручку", "pen", "pens"),
        ("монета", "монеты", "монет", "монету", "coin", "coins"),
        ("шарик", "шарика", "шариков", "шарик", "marble", "marbles"))


def ру_форма(вещь, n, винительный=False):
    """Форма вещи при счёте; винительный — только у единственного."""
    один, few, many = вещь[0], вещь[1], вещь[2]
    if винительный and n % 10 == 1 and n % 100 != 11:
        return вещь[3]
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
        ру = (
            f"у {род} было {было} {ру_форма(вещь, было)}. "
            f"{он_она} отдал{'а' if он_она == 'она' else ''} "
            f"{ушло} {ру_форма(вещь, ушло, винительный=True)}. "
            f"у {него_неё} осталось {стало} {ру_форма(вещь, стало)}."
        )
        ан = (
            f"{en} had {было} {вещь[5]}. "
            f"{he_she} gave away {ушло} "
            f"{вещь[4] if ушло == 1 else вещь[5]}. "
            f"{he_she} has {стало} {вещь[4] if стало == 1 else вещь[5]} left."
        )
        вон.append(ру)
        вон.append(ан)
        # ВОПРОС ПОРОЖДЁН ОТВЕТОМ, А НЕ ПРИПИСАН К НЕМУ. Обе половины
        # строит одна и та же тройка величин, и закон пары
        # (`tools/asking.py`) требует, чтобы числа вопроса были
        # НАЧАЛЬНЫМ ОТРЕЗКОМ чисел ответа: вопрос повторяет посылку и
        # спрашивает ровно то, что ответ добавляет.
        вон.append(
            f"у {род} было {было} {ру_форма(вещь, было)}. "
            f"{он_она} отдал{'а' if он_она == 'она' else ''} "
            f"{ушло} {ру_форма(вещь, ушло, винительный=True)}. "
            f"сколько {вещь[2]} у {него_неё} осталось? {ру}"
        )
        вон.append(
            f"{en} had {было} {вещь[5]}. "
            f"{he_she} gave away {ушло} "
            f"{вещь[4] if ушло == 1 else вещь[5]}. "
            f"how many {вещь[5]} does {he_she} have left? {ан}"
        )
        # ОТКАЗ С ОСНОВАНИЕМ: отдать больше, чем было, нельзя. Слой
        # показывал только сходящиеся рассказы и учил, что рассказ
        # сходится всегда; отказ здесь принадлежит РЕЧИ, ибо сказанное
        # грамматично, а события быть не могло.
        сверх = было + 1 + (i % 3)
        вон.append(
            f"у {род} было {было} {ру_форма(вещь, было)}. "
            f"{он_она} отдал{'а' if он_она == 'она' else ''} "
            f"{сверх} {ру_форма(вещь, сверх, винительный=True)} — нет "
            f"такого счёта: {сверх} больше {было}."
        )
        вон.append(
            f"{en} had {было} {вещь[5]}. "
            f"{he_she} gave away {сверх} "
            f"{вещь[4] if сверх == 1 else вещь[5]} — there is no such "
            f"count: {сверх} is greater than {было}."
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


def ПРОСТЫЕ_ДО(n):
    return [k for k in range(2, n)
            if all(k % d for d in range(2, int(k ** 0.5) + 1))]


def уступка(шаг):
    """«Хотя» — ПОБЕЖДЁННОЕ ОЖИДАНИЕ по объявленному правилу.

    Правило по умолчанию названо и ПРОВЕРЯЕМО: простые числа обычно
    нечётны — среди всех простых ровно одно исключение. Без объявленного
    правила «хотя» неотличимо от «и» (довод verum-6c), потому правило
    показывается рядом с исключением.
    """
    вон = []
    простые = ПРОСТЫЕ_ДО(60)
    нечётных = sum(1 for p in простые if p % 2)
    for i in range(8):
        вон.append(f"простые числа обычно нечётны: из {len(простые)} "
                   f"простых до 60 нечётны {нечётных}.")
        вон.append(f"хотя 2 простое, 2 чётно.")
        вон.append(f"primes are usually odd: of {len(простые)} primes "
                   f"below 60, {нечётных} are odd.")
        вон.append(f"although 2 is prime, 2 is even.")
    return вон


def существование(шаг):
    """«Хотя бы один» — свидетель вместо пробега."""
    вон = []
    for i in range(16):
        a = 2 + (i + шаг) % 7
        ряд = [a, a + 1, a + 2]
        чётные = [x for x in ряд if x % 2 == 0]
        если = ", ".join(str(x) for x in ряд)
        вон.append(f"хотя бы одно из чисел {если} чётно: это {чётные[0]}.")
        вон.append(f"at least one of {если} is even: it is {чётные[0]}.")
    return вон


def возможность(шаг):
    """«Может» — существует случай, где утверждение стоит."""
    вон = []
    пары = ((3, 5, 8), (1, 7, 8), (5, 7, 12), (9, 3, 12), (11, 5, 16),
            (13, 3, 16), (7, 9, 16), (1, 3, 4))
    for a, b, c in пары:
        вон.append(f"сумма двух нечётных может быть кратна 4: "
                   f"{a} + {b} = {c}.")
        вон.append(f"the sum of two odd numbers can be a multiple of 4: "
                   f"{a} + {b} = {c}.")
    return вон


def долженствование(шаг):
    """«Должен» — во ВСЕХ случаях названной области."""
    вон = []
    for i in range(8):
        верх = 10 + i * 2 + шаг
        область = [x for x in range(2, верх, 2)]
        вон.append(f"сумма двух чётных должна быть чётной: "
                   f"проверено на всех чётных до {верх}.")
        вон.append(f"the sum of two even numbers must be even: "
                   f"checked on all even numbers below {верх}.")
        assert all((x + y) % 2 == 0 for x in область for y in область)
    return вон


def тезис(шаг):
    """Заявленное утверждение и шаги, ведущие ИМЕННО к нему.

    Контроль, названный verum-6c: суд, проверяющий шаги, принимает
    безупречную цепь, доказавшую НЕ ТО, что обещано. Потому тезис и
    итог обязаны совпасть, а шаги — обосновать именно его.
    """
    вон = []
    for i in range(16):
        n = 6 + 2 * ((i + шаг) % 8)
        d = 2
        вон.append(f"тезис: {n} составное. шаг: {n} делится на {d}. "
                   f"шаг: {d} не равно 1 и {d} не равно {n}. "
                   f"итог: {n} составное.")
        вон.append(f"thesis: {n} is composite. step: {n} is divisible "
                   f"by {d}. step: {d} is not 1 and {d} is not {n}. "
                   f"hence: {n} is composite.")
    return вон


def стыки(шаг):
    """СТЫКИ ФОРМ — контрольные, а не учебные (замысел holon-e2).

    Композиция купленных форм есть ВЫВОД, а не заучивание: покупки
    глубины два не существует. Эти показы нужны ПРИБОРУ, чтобы отличить
    живой стык от мёртвого, и потому их мало — одна-две на стык.
    """
    вон = []
    for i in range(4):
        имя, род, он_она, него_неё, en, he_she = ЛИЦА[(i + шаг) % 6]
        вещь = ВЕЩИ[(i + шаг) % 5]
        n = 6 + 2 * i
        # СЛЕДОВАНИЕ над АНАФОРОЙ
        вон.append(f"у {род} {n} {ру_форма(вещь, n)}. "
                   f"значит у {него_неё} чётное число предметов.")
        вон.append(f"{en} has {n} {вещь[5]}. "
                   f"therefore {he_she} has an even count.")
        # КВАНТОР над ПРИДАТОЧНЫМ
        d = 4
        m = d * (2 + i)
        вон.append(f"все числа, которые делятся на {d}, чётны. "
                   f"{m} делится на {d}. значит {m} чётно.")
        вон.append(f"all numbers that are divisible by {d} are even. "
                   f"{m} is divisible by {d}. therefore {m} is even.")
        # СЛЕДОВАНИЕ над СЛЕДОВАНИЕМ
        k = 8 * (1 + i)
        вон.append(f"{k} делится на 4. значит {k} делится на 2. "
                   f"значит {k} чётно.")
        вон.append(f"{k} is divisible by 4. therefore {k} is divisible "
                   f"by 2. therefore {k} is even.")
        # ОТРИЦАНИЕ над КВАНТОРОМ
        ряд = [2 + 2 * i, 3 + 2 * i, 4 + 2 * i]
        нечёт = [x for x in ряд if x % 2]
        если = ", ".join(str(x) for x in ряд)
        вон.append(f"не все числа {если} чётны: {нечёт[0]} нечётно.")
        вон.append(f"not all of {если} are even: {нечёт[0]} is odd.")
        # АНАФОРА над ПЕРЕЧИСЛЕНИЕМ
        чёт = [2 + 2 * i, 4 + 2 * i, 6 + 2 * i]
        если2 = ", ".join(str(x) for x in чёт)
        вон.append(f"числа {если2} названы. они все чётны.")
        вон.append(f"the numbers {если2} are named. they are all even.")
        # ВОЗМОЖНОСТЬ над СУЩЕСТВОВАНИЕМ
        тройка = [3 + i, 4 + i, 5 + i]
        свид = [x for x in тройка if x % 2 == 0][0]
        если3 = ", ".join(str(x) for x in тройка)
        вон.append(f"может быть, что хотя бы одно из чисел {если3} "
                   f"чётно: это {свид}.")
        вон.append(f"it may be that at least one of {если3} is even: "
                   f"it is {свид}.")
    return вон


ГРУППЫ = (анафора, вывод, придаточное, квантор, номинализация, условия,
          уступка, существование, возможность, долженствование, тезис,
          стыки)


def pass_groups(pass_i):
    return [сделать(pass_i) for сделать in ГРУППЫ]


def main():
    emit_grouped("datasets/genesis_speech.txt", pass_groups)


if __name__ == "__main__":
    main()
