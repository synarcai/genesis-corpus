#!/usr/bin/env python3
"""THE HOUSE OF SPEED — the unit that is a RATIO of two units (06.09).

The census found ZERO lines in the свод carrying «km/h» in any of its nine spellings. The
corpus has rates («five roubles an hour») and it has units and their conversion, but it never
writes the unit that is itself a ratio — and the ratio is where the three questions of a rate
become one law: distance is speed times time, time is distance over speed, speed is distance
over time. A market that has bought only the first cannot answer the other two, and d5's
measure names the money-and-rate road as the second-largest gate of the reader's silence.

WHAT THE HOUSE SHOWS: one journey and the same three questions over it, each the inverse of
another, with the ratio unit written as the languages write it («км/ч», «km/h», «km/u»), the
distance in its abbreviation («180 км») and the time in a counted word («3 часа», «3 godziny»)
— an abbreviation needs no count form, and a counted word needs its own, so the page carries
both kinds of unit at once.

EVERY PAGE DIVIDES EXACTLY: a speed and a time whose product is whole, and a distance that the
speed divides without remainder. The house does not show the fraction of an hour — that is the
neighbouring market of shares, and mixing them would teach neither.

WHAT IS BORROWED: nine languages, the counting rule of the packs (through the house of the
pair) and the hour word of the house of the clock — one declaration, several readers. Declared
here: the ratio unit of each language, the abbreviation of the kilometre, and the frames of a
journey.

WHAT IS NOT MEASURED, NAMED: acceleration, a speed that changes on the way, and any unit but
the kilometre per hour.
"""
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import asking  # noqa: E402 — the house of the pair declares which openers a question may wear
import clockforms as CF  # noqa: E402 — the hour word with its count forms
import svampforms as S  # noqa: E402 — the count cell of a pack

ЯЗЫКИ = ("ru", "en", "de", "fr", "es", "it", "pt", "nl", "pl")
# ЕДИНИЦА-ОТНОШЕНИЕ И СОКРАЩЕНИЕ КИЛОМЕТРА — как их пишет каждый язык
СКОРОСТЬ_ЕД = {"ru": "км/ч", "en": "km/h", "de": "km/h", "fr": "km/h", "es": "km/h",
               "it": "km/h", "pt": "km/h", "nl": "km/u", "pl": "km/h"}
КМ = {"ru": "км", "en": "km", "de": "km", "fr": "km", "es": "km", "it": "km", "pt": "km",
      "nl": "km", "pl": "km"}
# ПАРЫ (скорость, часы): произведение целое, и деление обратно тоже целое
ПАРЫ = ((60, 3), (80, 2), (45, 4), (90, 3), (70, 5), (55, 6), (120, 2), (65, 4),
        (75, 3), (50, 7), (110, 4), (85, 2), (95, 3), (40, 8), (100, 5), (130, 2))
РЕЧЬ = {
    "ru": dict(идёт="поезд идёт {V} {ЕД}.",
               вопрос_путь="сколько километров он пройдёт за {T}?", ответ_путь="{S} {КМ}",
               прошёл="поезд прошёл {S} {КМ} со скоростью {V} {ЕД}.",
               вопрос_время="за сколько часов он прошёл этот путь?", ответ_время="за {T}",
               прошёл2="поезд прошёл {S} {КМ} за {T}.",
               вопрос_скорость="сколько километров в час он идёт?", ответ_скорость="{V} {ЕД}",
               двоеточие=": "),
    "en": dict(идёт="the train goes {V} {ЕД}.",
               вопрос_путь="how far will it go in {T}?", ответ_путь="{S} {КМ}",
               прошёл="the train went {S} {КМ} at {V} {ЕД}.",
               вопрос_время="in how many hours did it go that far?", ответ_время="in {T}",
               прошёл2="the train went {S} {КМ} in {T}.",
               вопрос_скорость="how many kilometres per hour does it go?", ответ_скорость="{V} {ЕД}",
               двоеточие=": "),
    "de": dict(идёт="der Zug fährt {V} {ЕД}.",
               вопрос_путь="wie weit fährt er in {T}?", ответ_путь="{S} {КМ}",
               прошёл="der Zug fuhr {S} {КМ} mit {V} {ЕД}.",
               вопрос_время="in wie vielen Stunden fuhr er so weit?", ответ_время="in {T}",
               прошёл2="der Zug fuhr {S} {КМ} in {T}.",
               вопрос_скорость="wie viele Kilometer pro Stunde fährt er?", ответ_скорость="{V} {ЕД}",
               двоеточие=": "),
    "fr": dict(идёт="le train roule à {V} {ЕД}.",
               вопрос_путь="quelle distance parcourt-il en {T} ?", ответ_путь="{S} {КМ}",
               прошёл="le train a parcouru {S} {КМ} à {V} {ЕД}.",
               вопрос_время="en combien d'heures a-t-il parcouru cette distance ?", ответ_время="en {T}",
               прошёл2="le train a parcouru {S} {КМ} en {T}.",
               вопрос_скорость="combien de kilomètres par heure fait-il ?", ответ_скорость="{V} {ЕД}",
               двоеточие=" : "),
    "es": dict(идёт="el tren va a {V} {ЕД}.",
               вопрос_путь="¿qué distancia recorre en {T}?", ответ_путь="{S} {КМ}",
               прошёл="el tren recorrió {S} {КМ} a {V} {ЕД}.",
               вопрос_время="¿en cuántas horas recorrió esa distancia?", ответ_время="en {T}",
               прошёл2="el tren recorrió {S} {КМ} en {T}.",
               вопрос_скорость="¿cuántos kilómetros por hora va?", ответ_скорость="{V} {ЕД}",
               двоеточие=": "),
    "it": dict(идёт="il treno va a {V} {ЕД}.",
               вопрос_путь="quanta strada fa in {T}?", ответ_путь="{S} {КМ}",
               прошёл="il treno ha fatto {S} {КМ} a {V} {ЕД}.",
               вопрос_время="in quante ore ha fatto questa strada?", ответ_время="in {T}",
               прошёл2="il treno ha fatto {S} {КМ} in {T}.",
               вопрос_скорость="quanti chilometri all'ora fa?", ответ_скорость="{V} {ЕД}",
               двоеточие=": "),
    "pt": dict(идёт="o comboio vai a {V} {ЕД}.",
               вопрос_путь="que distância percorre em {T}?", ответ_путь="{S} {КМ}",
               прошёл="o comboio percorreu {S} {КМ} a {V} {ЕД}.",
               вопрос_время="em quantas horas percorreu essa distância?", ответ_время="em {T}",
               прошёл2="o comboio percorreu {S} {КМ} em {T}.",
               вопрос_скорость="quantos quilómetros por hora faz?", ответ_скорость="{V} {ЕД}",
               двоеточие=": "),
    "nl": dict(идёт="de trein rijdt {V} {ЕД}.",
               вопрос_путь="hoe ver rijdt hij in {T}?", ответ_путь="{S} {КМ}",
               прошёл="de trein reed {S} {КМ} met {V} {ЕД}.",
               вопрос_время="in hoeveel uur reed hij zo ver?", ответ_время="in {T}",
               прошёл2="de trein reed {S} {КМ} in {T}.",
               вопрос_скорость="hoeveel kilometer per uur rijdt hij?", ответ_скорость="{V} {ЕД}",
               двоеточие=": "),
    "pl": dict(идёт="pociąg jedzie {V} {ЕД}.",
               вопрос_путь="ile kilometrów przejedzie w {T}?", ответ_путь="{S} {КМ}",
               прошёл="pociąg przejechał {S} {КМ} z prędkością {V} {ЕД}.",
               вопрос_время="w ile godzin przejechał tę drogę?", ответ_время="w {T}",
               прошёл2="pociąg przejechał {S} {КМ} w {T}.",
               вопрос_скорость="ile kilometrów na godzinę jedzie?", ответ_скорость="{V} {ЕД}",
               двоеточие=": "),
}
ФОРМЫ = ("путь", "время", "скорость")


def _часы(язык, n):
    """«3 часа», «3 godziny» — счётное слово часа берётся у дома часов, а не объявляется вновь."""
    return "%d %s" % (n, S._счёт(CF.ЧАС[язык], n, язык))


def рамка(язык, форма):
    р = РЕЧЬ[язык]
    ед, км = СКОРОСТЬ_ЕД[язык], КМ[язык]
    def подставь(ключ):
        return р[ключ].replace("{ЕД}", ед).replace("{КМ}", км)
    if форма == "путь":
        # ПУТЬ ЕСТЬ СКОРОСТЬ, УМНОЖЕННАЯ НА ВРЕМЯ
        return (подставь("идёт") + " " + подставь("вопрос_путь") + " " + подставь("ответ_путь")
                + р["двоеточие"] + "{V} {зн} {t} = {S}.")
    if форма == "время":
        # ВРЕМЯ ЕСТЬ ПУТЬ, ДЕЛЁННЫЙ НА СКОРОСТЬ
        return (подставь("прошёл") + " " + подставь("вопрос_время") + " " + подставь("ответ_время")
                + р["двоеточие"] + "{S} {зн} {V} = {t}.")
    # СКОРОСТЬ ЕСТЬ ПУТЬ, ДЕЛЁННЫЙ НА ВРЕМЯ
    return (подставь("прошёл2") + " " + подставь("вопрос_скорость") + " " + подставь("ответ_скорость")
            + р["двоеточие"] + "{S} {зн} {t} = {V}.")


ЗНАК_ФОРМЫ = {"путь": "×", "время": "÷", "скорость": "÷"}


def страница(язык, форма, v, t):
    s = v * t
    return рамка(язык, форма).format(V=v, S=s, t=t, T=_часы(язык, t), зн=ЗНАК_ФОРМЫ[форма])


def _показы():
    вон = {}
    for язык in ЯЗЫКИ:
        for v, t in ПАРЫ:
            for форма in ФОРМЫ:
                вон[страница(язык, форма, v, t)] = (язык, форма)
    return вон


ПОКАЗЫ = _показы()


def _альт(слова):
    return "(?:" + "|".join(re.escape(с) for с in sorted({с for с in слова if с}, key=lambda с: (-len(с), с))) + ")"


def _образец(язык, шаблон):
    часы = _альт(CF.ЧАС[язык])
    # ЗНАК ДЕЙСТВИЯ — ДЫРА, А НЕ БУКВА (М-489): «60 ÷ 3 = 180» обязано быть ЛОЖЬЮ, а не
    # немотой, иначе суд слеп ровно на той порче, ради которой поставлен
    дыры = {"V": r"\d+", "S": r"\d+", "t": r"\d+", "T": r"\d+ " + часы, "зн": r"[+−×÷]"}
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


def _вердикт(язык, форма, зн):
    # ЗНАК ЕСТЬ ЧАСТЬ ЗАКОНА, А НЕ УКРАШЕНИЕ: путь есть умножение, время и скорость — деление
    if зн.get("зн") != ЗНАК_ФОРМЫ[форма]:
        return False
    v, s, t = int(зн["V"]), int(зн["S"]), int(зн["t"])
    if min(v, s, t) < 1:
        return False
    # ТРИ ВОПРОСА — ОДИН ЗАКОН: путь есть скорость на время, и обратное деление точно
    if v * t != s:
        return False
    # СЧЁТНОЕ СЛОВО ЧАСА ЕСТЬ ФОРМА СВОЕГО ЧИСЛА, И ЧИСЛО ТО ЖЕ, ЧТО В ЛЕДЖЕРЕ
    if зн["T"] != _часы(язык, t):
        return False
    return True


def судить(строка):
    """(судимо, истинно): a page of a frame of the house whose ratio recomputes; else silence."""
    с = строка.strip()
    if с in ПОКАЗЫ:
        return True, True
    for образ, язык, форма in ОБРАЗЦЫ:
        м = образ.match(с)
        if not м:
            continue
        зн = _значения(м)
        if зн is None:
            return True, False
        return True, _вердикт(язык, форма, зн)
    return False, False


def _самопроверка():
    for показ in ПОКАЗЫ:
        assert судить(показ) == (True, True), показ
    мутанты = 0
    for язык in ЯЗЫКИ:
        v, t = 60, 3
        п = страница(язык, "путь", v, t)
        assert судить(п) == (True, True), п
        # (1) ПУТЬ СЛОЖЕН ВМЕСТО УМНОЖЕНИЯ
        битая = п.replace("= 180.", "= 63.").replace("180 " + КМ[язык], "63 " + КМ[язык])
        assert судить(битая) == (True, False), битая
        # (2) ВРЕМЯ: делено на путь вместо скорости
        в = страница(язык, "время", v, t)
        assert судить(в) == (True, True), в
        битая = в.replace("÷ 60 = 3", "÷ 60 = 4").replace(_часы(язык, 3), _часы(язык, 4))
        assert судить(битая) == (True, False), битая
        # (3) СКОРОСТЬ: путь делён неверно
        с = страница(язык, "скорость", v, t)
        assert судить(с) == (True, True), с
        битая = с.replace("= 60.", "= 90.").replace("60 " + СКОРОСТЬ_ЕД[язык], "90 " + СКОРОСТЬ_ЕД[язык])
        assert судить(битая) == (True, False), битая
        мутанты += 3
        # (4) СЧЁТНОЕ СЛОВО ЧАСА — ФОРМА ЧУЖОГО ЧИСЛА
        своя, чужая = S._счёт(CF.ЧАС[язык], 3, язык), S._счёт(CF.ЧАС[язык], 1, язык)
        if своя != чужая:
            битая = п.replace("3 " + своя, "3 " + чужая)
            assert судить(битая) == (True, False), битая
            мутанты += 1
        # (5) ЗАЧИН ВОПРОСА ОБЪЯВЛЕН ДОМОМ ПАРЫ
        for стр in (п, в, с):
            вопрос = стр[:стр.index("?") + 1].split(". ")[-1]
            assert asking.зачин_объявлен(вопрос) is not False, (язык, вопрос)
    for язык in ЯЗЫКИ:
        print("  ", страница(язык, "путь", 60, 3))
    for язык in ("ru", "en", "pl"):
        print("  ", страница(язык, "время", 80, 2))
        print("  ", страница(язык, "скорость", 45, 4))
    по_форме = {}
    for _, (язык, форма) in ПОКАЗЫ.items():
        по_форме[форма] = по_форме.get(форма, 0) + 1
    print(f"  мутантов поймано: {мутанты}")
    print(f"  дом пишет показов: {len(ПОКАЗЫ)} (языков {len(ЯЗЫКИ)}, форм {len(ФОРМЫ)}, образцов {len(ОБРАЗЦЫ)}): "
          + ", ".join(f"{ф} {к}" for ф, к in по_форме.items()))


if __name__ == "__main__":
    _самопроверка()
