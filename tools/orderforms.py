#!/usr/bin/env python3
"""THE HOUSE OF ORDER — sorting is not comparing twice (06.09).

The census found ZERO lines in the свод with «in ascending order» or «по возрастанию». The
corpus compares two numbers (which is greater, by how much, how many times), and it names the
greatest and the least of three — but it never puts a whole set IN ORDER, and ordering is not
a repetition of comparison: it is one operation over the set, and its answer is a SEQUENCE, not
a number.

FOUR QUESTIONS OVER ONE SET, and the last two are what make the first two more than a habit:

    THE ORDER ITSELF, up and down: «the numbers: 7, 3, 9. how do they go in ascending order?
    3, 7, 9.» — and the same set descending, so that neither direction is the default.

    THE PLACE IN THE ORDER: «which number is the second largest? 7» — a question that cannot be
    answered by finding a maximum, and that a reader who learnt «biggest» alone will miss.

    THE ONE IN THE MIDDLE: «which number is between the other two? 7: 3 < 7 < 9» — the ledger
    writes the chain of signs, so that «between» is shown as a relation of THREE and not as a
    second-place synonym.

WHAT IS BORROWED: nine languages and the openers of the house of the pair. Declared here: the
words of ascending and descending order, of the place in an order, and of standing between.

WHAT IS NOT MEASURED, NAMED: sets of more than four numbers, ties inside a set (two equal
numbers have no second place, and the house writes none), and the ordering of anything but
numbers.
"""
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import asking  # noqa: E402 — the house of the pair declares which openers a question may wear

ЯЗЫКИ = ("ru", "en", "de", "fr", "es", "it", "pt", "nl", "pl")
# ТРОЙКИ И ЧЕТВЁРКИ: все числа различны, порядок перемешан
ТРОЙКИ = ((7, 3, 9), (12, 25, 18), (44, 31, 57), (6, 19, 11), (83, 62, 71), (28, 47, 35),
          (96, 74, 85), (15, 39, 22), (58, 41, 66), (9, 27, 14), (73, 52, 88), (33, 17, 45),
          (61, 94, 79), (24, 8, 16), (55, 37, 68), (91, 46, 82))
ЧЕТВЁРКИ = ((7, 3, 9, 5), (12, 25, 18, 30), (44, 31, 57, 23), (6, 19, 11, 27),
            (83, 62, 71, 95), (28, 47, 35, 16), (96, 74, 85, 52), (15, 39, 22, 48))
РЕЧЬ = {
    "ru": dict(числа="числа: {СПИСОК}.", вопрос_вверх="как они идут по возрастанию?",
               вопрос_вниз="как они идут по убыванию?", вопрос_второе="какое число второе по величине?",
               вопрос_между="какое число стоит между двумя другими?", двоеточие=": "),
    "en": dict(числа="the numbers: {СПИСОК}.", вопрос_вверх="how do they go in ascending order?",
               вопрос_вниз="how do they go in descending order?", вопрос_второе="which number is the second largest?",
               вопрос_между="which number is between the other two?", двоеточие=": "),
    "de": dict(числа="die Zahlen: {СПИСОК}.", вопрос_вверх="wie gehen sie aufsteigend?",
               вопрос_вниз="wie gehen sie absteigend?", вопрос_второе="welche Zahl ist die zweitgrößte?",
               вопрос_между="welche Zahl liegt zwischen den beiden anderen?", двоеточие=": "),
    "fr": dict(числа="les nombres : {СПИСОК}.", вопрос_вверх="comment vont-ils par ordre croissant ?",
               вопрос_вниз="comment vont-ils par ordre décroissant ?",
               вопрос_второе="quel nombre est le deuxième plus grand ?",
               вопрос_между="quel nombre est entre les deux autres ?", двоеточие=" : "),
    "es": dict(числа="los números: {СПИСОК}.", вопрос_вверх="¿cómo van en orden ascendente?",
               вопрос_вниз="¿cómo van en orden descendente?", вопрос_второе="¿qué número es el segundo mayor?",
               вопрос_между="¿qué número está entre los otros dos?", двоеточие=": "),
    "it": dict(числа="i numeri: {СПИСОК}.", вопрос_вверх="come vanno in ordine crescente?",
               вопрос_вниз="come vanno in ordine decrescente?", вопрос_второе="quale numero è il secondo più grande?",
               вопрос_между="quale numero sta fra gli altri due?", двоеточие=": "),
    "pt": dict(числа="os números: {СПИСОК}.", вопрос_вверх="como vão por ordem crescente?",
               вопрос_вниз="como vão por ordem decrescente?", вопрос_второе="que número é o segundo maior?",
               вопрос_между="que número está entre os outros dois?", двоеточие=": "),
    "nl": dict(числа="de getallen: {СПИСОК}.", вопрос_вверх="hoe gaan ze oplopend?",
               вопрос_вниз="hoe gaan ze aflopend?", вопрос_второе="welk getal is het op een na grootste?",
               вопрос_между="welk getal ligt tussen de andere twee?", двоеточие=": "),
    "pl": dict(числа="liczby: {СПИСОК}.", вопрос_вверх="jak idą rosnąco?",
               вопрос_вниз="jak idą malejąco?", вопрос_второе="która liczba jest druga co do wielkości?",
               вопрос_между="która liczba jest między dwiema pozostałymi?", двоеточие=": "),
}
ФОРМЫ = ("вверх", "вниз", "второе", "между")


def _список(числа):
    return ", ".join(str(ч) for ч in числа)


def рамка(язык, форма, сколько):
    """The page: a set, a question over it, and an answer that is a SEQUENCE or a member."""
    р = РЕЧЬ[язык]
    начало = р["числа"].replace("{СПИСОК}", ", ".join("{n%d}" % i for i in range(сколько)))
    if форма == "вверх":
        return начало + " " + р["вопрос_вверх"] + " " + ", ".join("{u%d}" % i for i in range(сколько)) + "."
    if форма == "вниз":
        return начало + " " + р["вопрос_вниз"] + " " + ", ".join("{d%d}" % i for i in range(сколько)) + "."
    if форма == "второе":
        return начало + " " + р["вопрос_второе"] + " {v}."
    # МЕЖДУ — отношение ТРЁХ, и цепь знаков это показывает
    return начало + " " + р["вопрос_между"] + " {m}" + р["двоеточие"] + "{u0} < {m} < {u2}."


def страница(язык, форма, числа):
    вверх = sorted(числа)
    вниз = sorted(числа, reverse=True)
    поля = {}
    for i, ч in enumerate(числа):
        поля["n%d" % i] = ч
    for i, ч in enumerate(вверх):
        поля["u%d" % i] = ч
    for i, ч in enumerate(вниз):
        поля["d%d" % i] = ч
    поля["v"] = вниз[1]
    поля["m"] = вверх[1] if len(числа) == 3 else вверх[1]
    return рамка(язык, форма, len(числа)).format(**поля)


def _показы():
    вон = {}
    for язык in ЯЗЫКИ:
        for числа in ТРОЙКИ:
            for форма in ФОРМЫ:
                вон[страница(язык, форма, числа)] = (язык, форма)
        for числа in ЧЕТВЁРКИ:
            for форма in ("вверх", "вниз", "второе"):
                вон[страница(язык, форма, числа)] = (язык, форма)
    return вон


ПОКАЗЫ = _показы()


def _образец(язык, форма, сколько):
    дыры = {"v": r"\d+", "m": r"\d+"}
    for i in range(сколько):
        дыры["n%d" % i] = r"\d+"
        дыры["u%d" % i] = r"\d+"
        дыры["d%d" % i] = r"\d+"
    счёт, куски = {}, []
    for кусок in re.split(r"(\{[^}]+\})", рамка(язык, форма, сколько)):
        if кусок.startswith("{"):
            дыра = кусок[1:-1]
            счёт[дыра] = счёт.get(дыра, 0) + 1
            куски.append(f"(?P<h_{дыра}__{счёт[дыра]}>{дыры[дыра]})")
        else:
            куски.append(re.escape(кусок))
    return re.compile("^" + "".join(куски) + "$")


ОБРАЗЦЫ = [(_образец(язык, форма, сколько), язык, форма, сколько)
           for язык in ЯЗЫКИ for сколько in (3, 4) for форма in ФОРМЫ
           if not (сколько == 4 and форма == "между")]


def _значения(м):
    вон = {}
    for ключ, знач in м.groupdict().items():
        дыра, _ = ключ[2:].rsplit("__", 1)
        if дыра in вон and вон[дыра] != знач:
            return None
        вон[дыра] = знач
    return вон


def _вердикт(форма, сколько, зн):
    числа = [int(зн["n%d" % i]) for i in range(сколько)]
    if len(set(числа)) != сколько or min(числа) < 1:
        return False          # равные числа дом не пишет: у них нет второго места
    вверх, вниз = sorted(числа), sorted(числа, reverse=True)
    if форма == "вверх":
        return [int(зн["u%d" % i]) for i in range(сколько)] == вверх
    if форма == "вниз":
        return [int(зн["d%d" % i]) for i in range(сколько)] == вниз
    if форма == "второе":
        # ВТОРОЕ ПО ВЕЛИЧИНЕ НЕ ЕСТЬ НАИБОЛЬШЕЕ И НЕ ЕСТЬ НАИМЕНЬШЕЕ
        return int(зн["v"]) == вниз[1]
    # МЕЖДУ: названное число обязано стоять посередине, и цепь знаков — его края
    m = int(зн["m"])
    if m != вверх[1]:
        return False
    return int(зн["u0"]) == вверх[0] and int(зн["u2"]) == вверх[2]


def судить(строка):
    """(судимо, истинно): a page of a frame of the house whose order recomputes; else silence."""
    с = строка.strip()
    if с in ПОКАЗЫ:
        return True, True
    for образ, язык, форма, сколько in ОБРАЗЦЫ:
        м = образ.match(с)
        if not м:
            continue
        зн = _значения(м)
        if зн is None:
            return True, False
        return True, _вердикт(форма, сколько, зн)
    return False, False


def _хвост(с):
    """Начало ответа: после последнего вопросительного знака (у языков он с пробелом)."""
    м = list(re.finditer(r"[?？]\s", с))
    return м[-1].end() if м else 0


def _порча(с, было, стало):
    """Порча кладётся в ОТВЕТ, а не в перечень чисел вопроса."""
    хв = _хвост(с)
    return с[:хв] + с[хв:].replace(было, стало, 1)


def _самопроверка():
    for показ in ПОКАЗЫ:
        assert судить(показ) == (True, True), показ
    мутанты = 0
    for язык in ЯЗЫКИ:
        числа = (7, 3, 9)
        в = страница(язык, "вверх", числа)
        assert судить(в) == (True, True), в
        # (1) ПОРЯДОК НЕ ТОТ
        битая = _порча(в, "3, 7, 9", "3, 9, 7")
        assert судить(битая) == (True, False), битая
        # (2) УБЫВАНИЕ ЗАПИСАНО ВОЗРАСТАНИЕМ
        н = страница(язык, "вниз", числа)
        assert судить(н) == (True, True), н
        битая = _порча(н, "9, 7, 3", "3, 7, 9")
        assert судить(битая) == (True, False), битая
        # (3) ВТОРОЕ ПО ВЕЛИЧИНЕ НАЗВАНО НАИБОЛЬШИМ
        вт = страница(язык, "второе", числа)
        assert судить(вт) == (True, True), вт
        битая = _порча(вт, "7", "9")
        assert судить(битая) == (True, False), битая
        # (4) МЕЖДУ: названо крайнее
        м_ = страница(язык, "между", числа)
        assert судить(м_) == (True, True), м_
        битая = _порча(м_, "7", "9")
        assert судить(битая) == (True, False), битая
        мутанты += 4
        # (5) ЧЕТВЁРКА: второе по величине среди четырёх
        ч = страница(язык, "второе", (7, 3, 9, 5))
        assert судить(ч) == (True, True), ч
        битая = _порча(ч, "7", "5")
        assert судить(битая) == (True, False), битая
        мутанты += 1
        # (6) ЗАЧИН ВОПРОСА ОБЪЯВЛЕН ДОМОМ ПАРЫ
        for стр in (в, н, вт, м_):
            вопрос = стр[:стр.index("?") + 1].split(". ")[-1]
            assert asking.зачин_объявлен(вопрос) is not False, (язык, вопрос)
    for язык in ЯЗЫКИ:
        print("  ", страница(язык, "вверх", (7, 3, 9)))
    for язык in ("ru", "en", "pl"):
        print("  ", страница(язык, "второе", (12, 25, 18)))
        print("  ", страница(язык, "между", (44, 31, 57)))
    по_форме = {}
    for _, (язык, форма) in ПОКАЗЫ.items():
        по_форме[форма] = по_форме.get(форма, 0) + 1
    print(f"  мутантов поймано: {мутанты}")
    print(f"  дом пишет показов: {len(ПОКАЗЫ)} (языков {len(ЯЗЫКИ)}, форм {len(ФОРМЫ)}, образцов {len(ОБРАЗЦЫ)}): "
          + ", ".join(f"{ф} {к}" for ф, к in по_форме.items()))


if __name__ == "__main__":
    _самопроверка()
