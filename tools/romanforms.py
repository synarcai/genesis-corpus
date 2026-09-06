#!/usr/bin/env python3
"""THE HOUSE OF THE ROMAN NUMERAL — a third notation, and the law that reads it (06.09).

The census found ZERO lines in the свод carrying a roman numeral in any world: the corpus writes
numbers as digits and as words of nine languages, but never as the notation every book still uses
for a century, a chapter and a king. The gap is worth a house not for the letters but for the LAW
inside them: a sign that stands before a bigger sign is SUBTRACTED — the only place in all our
markets where the ORDER of two symbols decides the sign of their arithmetic. Everywhere else the
value of a token is its own; here it is its own only until the token to its right is larger.

WHAT THE HOUSE SHOWS, three frames over one number:
  запись     — the number asked for, the numeral answered, and the numeral broken into its parts;
  чтение     — the numeral given, the number asked for, and the same parts as the ledger;
  вычитание  — the law itself: the smaller sign, the larger sign it stands before, and the
               difference the pair is worth.
The letters are the SAME in nine languages — only the frame around them is translated. That is
the cheapest possible show of a law that is not any language's property, and it is why this house
holds nine languages at the price other houses pay for one.

THE JUDGE RECOMPUTES: it renders the number greedily by the table (C, XC, L, XL, X, IX, V, IV, I)
and demands the shown numeral be EXACTLY that — so «XIIII» for 14 is a lie even though its letters
add up, because the canonical form is the market's form. Then it cuts the numeral into tokens and
demands the ledger be their values in their order, summing to the number.

WHAT IS NOT MEASURED, NAMED: numerals above C, the medieval non-canonical forms (IIII on clock
faces), the bar of thousands, and the ORDINAL reading of a numeral («Chapter IV» = the fourth).
"""
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import asking  # noqa: E402 — the house of the pair declares which openers a question may wear

ЯЗЫКИ = ("ru", "en", "de", "fr", "es", "it", "pt", "nl", "pl")
# ТАБЛИЦА ЗНАКОВ — жадная, сверху вниз: пара вычитания есть ОДИН знак, а не два
ТАБЛИЦА = ((100, "C"), (90, "XC"), (50, "L"), (40, "XL"), (10, "X"), (9, "IX"),
           (5, "V"), (4, "IV"), (1, "I"))
ЗНАЧЕНИЕ = {з: в for в, з in ТАБЛИЦА}
ВЫЧЕТ = {"XC": ("X", "C", 10, 100), "XL": ("X", "L", 10, 50),
         "IX": ("I", "X", 1, 10), "IV": ("I", "V", 1, 5)}
# ЧИСЛА ЛЕДЖЕРА — у каждого не меньше двух знаков, иначе «сумма» была бы «100 = 100»
ЧИСЛА = (3, 6, 13, 14, 19, 24, 27, 30, 38, 44, 49, 58, 61, 76, 84, 95, 99)
# ЧИСЛА ЗАКОНА ВЫЧИТАНИЯ — ровно одна пара вычитания в записи, иначе «меньший знак» двусмыслен
ВЫЧИТАЕМЫЕ = (4, 9, 14, 19, 24, 40, 84, 90, 95)
ФОРМЫ = ("запись", "чтение", "вычитание")
РЕЧЬ = {
    "ru": dict(вопрос_записи="как записать {n} римскими цифрами?",
               дано="римская запись {R}.", вопрос_числа="какое это число?",
               закон="в записи {R} меньший знак {a} стоит перед большим знаком {b} и вычитается",
               двоеточие=": "),
    "en": dict(вопрос_записи="how is {n} written in roman numerals?",
               дано="the roman numeral {R}.", вопрос_числа="what number is this?",
               закон="in {R} the smaller sign {a} stands before the larger sign {b} and is subtracted",
               двоеточие=": "),
    "de": dict(вопрос_записи="wie schreibt man {n} in römischen Ziffern?",
               дано="die römische Zahl {R}.", вопрос_числа="welche Zahl ist das?",
               закон="in {R} steht das kleinere Zeichen {a} vor dem größeren Zeichen {b} und wird abgezogen",
               двоеточие=": "),
    "fr": dict(вопрос_записи="comment écrit-on {n} en chiffres romains ?",
               дано="le nombre romain {R}.", вопрос_числа="quel nombre est-ce ?",
               закон="dans {R} le signe plus petit {a} est placé devant le signe plus grand {b} et se soustrait",
               двоеточие=" : "),
    "es": dict(вопрос_записи="¿cómo se escribe {n} en números romanos?",
               дано="el número romano {R}.", вопрос_числа="¿qué número es este?",
               закон="en {R} el signo menor {a} está delante del signo mayor {b} y se resta",
               двоеточие=": "),
    "it": dict(вопрос_записи="come si scrive {n} in numeri romani?",
               дано="il numero romano {R}.", вопрос_числа="che numero è questo?",
               закон="in {R} il segno minore {a} sta davanti al segno maggiore {b} e si sottrae",
               двоеточие=": "),
    "pt": dict(вопрос_записи="como se escreve {n} em algarismos romanos?",
               дано="o número romano {R}.", вопрос_числа="que número é este?",
               закон="em {R} o sinal menor {a} está antes do sinal maior {b} e subtrai-se",
               двоеточие=": "),
    "nl": dict(вопрос_записи="hoe schrijft men {n} in Romeinse cijfers?",
               дано="het Romeinse getal {R}.", вопрос_числа="welk getal is dit?",
               закон="in {R} staat het kleinere teken {a} voor het grotere teken {b} en wordt afgetrokken",
               двоеточие=": "),
    "pl": dict(вопрос_записи="jak zapisać {n} cyframi rzymskimi?",
               дано="liczba rzymska {R}.", вопрос_числа="jaka to liczba?",
               закон="w {R} mniejszy znak {a} stoi przed większym znakiem {b} i odejmuje się",
               двоеточие=": "),
}


def римское(n):
    """The canonical numeral: greedy over the table — the market's one spelling of a number."""
    вон, остаток = [], n
    for в, з in ТАБЛИЦА:
        while остаток >= в:
            вон.append(з)
            остаток -= в
    return "".join(вон)


def знаки(римская):
    """The numeral cut into its tokens, in order; None if the string is not a canonical numeral."""
    вон, i = [], 0
    while i < len(римская):
        for в, з in ТАБЛИЦА:
            if римская.startswith(з, i):
                вон.append(з)
                i += len(з)
                break
        else:
            return None
    return вон if "".join(вон) == римская and римское(sum(ЗНАЧЕНИЕ[з] for з in вон)) == римская else None


def леджер(n):
    """«10 + 4» — the values of the tokens in the order the numeral writes them."""
    return " + ".join(str(ЗНАЧЕНИЕ[з]) for з in знаки(римское(n)))


def _пара(n):
    """The one subtractive token of the numeral: (smaller, larger, value of smaller, value of larger)."""
    пары = [з for з in знаки(римское(n)) if з in ВЫЧЕТ]
    return ВЫЧЕТ[пары[0]] if len(пары) == 1 else None


def рамка(язык, форма):
    р = РЕЧЬ[язык]
    if форма == "запись":
        # ЧИСЛО СПРОШЕНО — ЗАПИСЬ ОТВЕЧЕНА И РАЗОБРАНА
        return р["вопрос_записи"] + " {R}" + р["двоеточие"] + "{L} = {n}."
    if форма == "чтение":
        # ЗАПИСЬ ДАНА — ЧИСЛО СОБРАНО ИЗ ТЕХ ЖЕ ЧАСТЕЙ
        return р["дано"] + " " + р["вопрос_числа"] + " {n}" + р["двоеточие"] + "{L} = {n}."
    # ЗАКОН ПОРЯДКА: МЕНЬШИЙ ЗНАК ПЕРЕД БОЛЬШИМ ВЫЧИТАЕТСЯ
    return р["закон"] + р["двоеточие"] + "{vb} − {va} = {r}."


def страница(язык, форма, n):
    if форма == "вычитание":
        a, b, va, vb = _пара(n)
        return рамка(язык, форма).format(R=римское(n), a=a, b=b, va=va, vb=vb, r=vb - va)
    return рамка(язык, форма).format(n=n, R=римское(n), L=леджер(n))


def _показы():
    вон = {}
    for язык in ЯЗЫКИ:
        for n in ЧИСЛА:
            for форма in ("запись", "чтение"):
                вон[страница(язык, форма, n)] = (язык, форма)
        for n in ВЫЧИТАЕМЫЕ:
            вон[страница(язык, "вычитание", n)] = (язык, "вычитание")
    return вон


ПОКАЗЫ = _показы()


def _образец(язык, шаблон):
    дыры = {"n": r"\d+", "R": r"[IVXLC]+", "L": r"\d+(?: \+ \d+)+", "a": r"[IVXLC]",
            "b": r"[IVXLC]", "va": r"\d+", "vb": r"\d+", "r": r"\d+"}
    счёт, куски = {}, []
    for кусок in re.split(r"(\{[^}]+\})", шаблон):
        if кусок.startswith("{"):
            дыра = кусок[1:-1]
            счёт[дыра] = счёт.get(дыра, 0) + 1
            куски.append(f"(?P<h_{дыра}__{счёт[дыра]}>{дыры[дыра]})")
        else:
            куски.append(re.escape(кусок))
    return re.compile("^" + "".join(куски) + "$")


ОБРАЗЦЫ = [(_образец(язык, рамка(язык, форма)), язык, форма) for язык in ЯЗЫКИ for форма in ФОРМЫ]


def _значения(м):
    вон = {}
    for ключ, знач in м.groupdict().items():
        дыра, _ = ключ[2:].rsplit("__", 1)
        if дыра in вон and вон[дыра] != знач:
            return None
        вон[дыра] = знач
    return вон


def _вердикт(форма, зн):
    if форма == "вычитание":
        a, b = зн["a"], зн["b"]
        if a + b not in ВЫЧЕТ:
            return False
        _, _, va, vb = ВЫЧЕТ[a + b]
        # ПОРЯДОК РЕШАЕТ ЗНАК: меньший перед большим, и разность их значений
        return (int(зн["va"]) == va and int(зн["vb"]) == vb and va < vb
                and int(зн["r"]) == vb - va and (a + b) in зн["R"] and знаки(зн["R"]) is not None
                and [з for з in знаки(зн["R"]) if з in ВЫЧЕТ] == [a + b])
    n, р = int(зн["n"]), зн["R"]
    if n < 1 or n > 100:
        return False
    # ЗАПИСЬ ЕСТЬ КАНОНИЧЕСКАЯ ЗАПИСЬ ЭТОГО ЧИСЛА
    if римское(n) != р:
        return False
    # ЛЕДЖЕР ЕСТЬ ЗНАЧЕНИЯ ЗНАКОВ В ИХ ПОРЯДКЕ, И ИХ СУММА ЕСТЬ ЧИСЛО
    доли = [int(д) for д in зн["L"].split(" + ")]
    return доли == [ЗНАЧЕНИЕ[з] for з in знаки(р)] and sum(доли) == n


def судить(строка):
    """(судимо, истинно): a page of a frame of the house whose numeral recomputes; else silence."""
    с = строка.strip()
    if с in ПОКАЗЫ:
        return True, True
    for образ, _язык, форма in ОБРАЗЦЫ:
        м = образ.match(с)
        if not м:
            continue
        зн = _значения(м)
        if зн is None:
            return True, False
        return True, _вердикт(форма, зн)
    return False, False


def _самопроверка():
    assert римское(14) == "XIV" and римское(99) == "XCIX" and римское(40) == "XL"
    assert знаки("XIIII") is None and знаки("IL") is None and знаки("XIV") == ["X", "IV"]
    for показ in ПОКАЗЫ:
        assert судить(показ) == (True, True), показ
    мутанты = 0
    for язык in ЯЗЫКИ:
        з = страница(язык, "запись", 14)
        # (1) ЗАПИСЬ ЧУЖОГО ЧИСЛА
        битая = з.replace("XIV", "XVI")
        assert судить(битая) == (True, False), битая
        # (2) НЕКАНОНИЧЕСКАЯ ЗАПИСЬ — БУКВЫ СХОДЯТСЯ, ФОРМА РЫНКА НЕТ
        битая = з.replace("XIV", "XIIII").replace("10 + 4", "10 + 1 + 1 + 1 + 1")
        assert судить(битая) == (True, False), битая
        # (3) ДОЛЯ ЛЕДЖЕРА ПОДМЕНЕНА
        битая = з.replace("10 + 4 = 14", "10 + 5 = 14")
        assert судить(битая) == (True, False), битая
        # (4) СУММА ЛЕДЖЕРА НЕ ЧИСЛО
        битая = з.replace("= 14.", "= 15.")
        assert судить(битая) == (True, False), битая
        ч = страница(язык, "чтение", 27)
        assert судить(ч) == (True, True), ч
        # (5) ЧТЕНИЕ: порядок долей нарушен (сумма та же)
        битая = ч.replace("10 + 10 + 5 + 1 + 1", "5 + 10 + 10 + 1 + 1")
        assert судить(битая) == (True, False), битая
        в = страница(язык, "вычитание", 14)
        assert судить(в) == (True, True), в
        # (6) РАЗНОСТЬ ПАРЫ ПОДМЕНЕНА
        битая = в.replace("5 − 1 = 4.", "5 − 1 = 3.")
        assert судить(битая) == (True, False), битая
        # (7) ЗАКОН НАЗЫВАЕТ ПАРУ, КОТОРОЙ В ЗАПИСИ НЕТ
        битая = в.replace("XIV", "XIX")
        assert судить(битая) == (True, False), битая
        # (8) ЗНАКИ ПАРЫ ПОМЕНЯНЫ МЕСТАМИ — «V перед I» не пара вычитания
        битая = рамка(язык, "вычитание").format(R="XIV", a="V", b="I", va=5, vb=1, r=4)
        assert судить(битая) == (True, False), битая
        мутанты += 8
        # (9) ЗАЧИН ВОПРОСА ОБЪЯВЛЕН ДОМОМ ПАРЫ
        for стр in (з, ч):
            вопрос = [ч2 for ч2 in стр.split(". ") if "?" in ч2][0]
            вопрос = вопрос[:вопрос.index("?") + 1]
            assert asking.зачин_объявлен(вопрос) is not False, (язык, вопрос)
    for язык in ЯЗЫКИ:
        print("  ", страница(язык, "запись", 44))
    for язык in ("ru", "en", "pl"):
        print("  ", страница(язык, "чтение", 99))
        print("  ", страница(язык, "вычитание", 90))
    по_форме = {}
    for _, (_язык, форма) in ПОКАЗЫ.items():
        по_форме[форма] = по_форме.get(форма, 0) + 1
    print(f"  мутантов поймано: {мутанты}")
    print(f"  дом пишет показов: {len(ПОКАЗЫ)} (языков {len(ЯЗЫКИ)}, форм {len(ФОРМЫ)}, образцов {len(ОБРАЗЦЫ)}): "
          + ", ".join(f"{ф} {к}" for ф, к in по_форме.items()))


if __name__ == "__main__":
    _самопроверка()
