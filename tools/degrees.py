#!/usr/bin/env python3
"""THE HOUSE OF THE DEGREES OF COMPARISON — the same property said three times (06.09).

The census found TWENTY-NINE lines carrying a comparative adjective («сильнее», «stronger»,
«stärker», «plus fort») in the whole свод. The corpus compares NUMBERS on every page and almost
never compares by a PROPERTY — and the property is where the languages keep one of their oldest
irregularities: good–better–best, gut–besser–am besten, bon–meilleur–le meilleur, dobry–lepszy–
najlepszy. A reader that has read a million comparisons of numbers and no comparison of a
quality cannot follow the simplest human sentence about two people.

WHAT THE HOUSE SHOWS, three frames over one property:
  ряд      — the three degrees in a row, and where the second does NOT follow from the first the
             page SAYS SO («и вторая не выводится из первой»): the irregularity is taught, not
             hidden among regular rows;
  цепь     — the transitive chain to the superlative («Иван выше, чем Пётр. Пётр выше, чем Павел.
             кто самый высокий?»), whose answer is a NAME and whose ground is the two comparisons
             — the same law of transitivity the house of place shows on an axis, here on a scale;
  обратное — the converse through the ANTONYM: if the first is taller than the second, the second
             is SHORTER than the first. The converse of a comparison is not the same word negated
             but the OPPOSITE word, and that is a fact about the pair, not about the sentence.

THREE PAIRS carry it: tall/short, fast/slow, good/bad — the last because its comparative is
irregular in seven of the nine languages, and German and Dutch make only ONE of the two irregular
(«gut → besser» but «schlecht → schlechter»), which is exactly the shape a reader must see.

WHAT IS DECLARED HERE: the three degrees of six adjectives in nine languages, with the flag of
irregularity on each; the names are the corpus's own (tools/actors.py).

WHAT IS NOT MEASURED, NAMED: the FEMININE of the superlative (Russian «самая высокая», Polish
«najwyższa» — the house speaks of men only, and the gendered degree is a named entrance), the
attributive superlative beside a noun («the tallest boy»), and the comparison of two properties
of one thing («longer than it is wide»).
"""
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import asking  # noqa: E402 — the house of the pair declares which openers a question may wear
import svampforms as F  # noqa: E402 — the corpus's own names live in its house of actors

ЯЗЫКИ = ("ru", "en", "de", "fr", "es", "it", "pt", "nl", "pl")
ПАРЫ = (("высокий", "низкий"), ("быстрый", "медленный"), ("хороший", "плохой"))
ПРИЗНАКИ = tuple(п for пара in ПАРЫ for п in пара)
# ТРИ СТЕПЕНИ И ПРИЗНАК НЕПРАВИЛЬНОСТИ: (положительная, сравнительная, превосходная, неправильна)
СЛОВА = {
    "ru": {"высокий": ("высокий", "выше", "самый высокий", False),
           "низкий": ("низкий", "ниже", "самый низкий", False),
           "быстрый": ("быстрый", "быстрее", "самый быстрый", False),
           "медленный": ("медленный", "медленнее", "самый медленный", False),
           "хороший": ("хороший", "лучше", "самый лучший", True),
           "плохой": ("плохой", "хуже", "самый худший", True)},
    "en": {"высокий": ("tall", "taller", "the tallest", False),
           "низкий": ("short", "shorter", "the shortest", False),
           "быстрый": ("fast", "faster", "the fastest", False),
           "медленный": ("slow", "slower", "the slowest", False),
           "хороший": ("good", "better", "the best", True),
           "плохой": ("bad", "worse", "the worst", True)},
    "de": {"высокий": ("groß", "größer", "am größten", False),
           "низкий": ("klein", "kleiner", "am kleinsten", False),
           "быстрый": ("schnell", "schneller", "am schnellsten", False),
           "медленный": ("langsam", "langsamer", "am langsamsten", False),
           "хороший": ("gut", "besser", "am besten", True),
           "плохой": ("schlecht", "schlechter", "am schlechtesten", False)},
    "fr": {"высокий": ("grand", "plus grand", "le plus grand", False),
           "низкий": ("petit", "plus petit", "le plus petit", False),
           "быстрый": ("rapide", "plus rapide", "le plus rapide", False),
           "медленный": ("lent", "plus lent", "le plus lent", False),
           "хороший": ("bon", "meilleur", "le meilleur", True),
           "плохой": ("mauvais", "pire", "le pire", True)},
    "es": {"высокий": ("alto", "más alto", "el más alto", False),
           "низкий": ("bajo", "más bajo", "el más bajo", False),
           "быстрый": ("rápido", "más rápido", "el más rápido", False),
           "медленный": ("lento", "más lento", "el más lento", False),
           "хороший": ("bueno", "mejor", "el mejor", True),
           "плохой": ("malo", "peor", "el peor", True)},
    "it": {"высокий": ("alto", "più alto", "il più alto", False),
           "низкий": ("basso", "più basso", "il più basso", False),
           "быстрый": ("veloce", "più veloce", "il più veloce", False),
           "медленный": ("lento", "più lento", "il più lento", False),
           "хороший": ("buono", "migliore", "il migliore", True),
           "плохой": ("cattivo", "peggiore", "il peggiore", True)},
    "pt": {"высокий": ("alto", "mais alto", "o mais alto", False),
           "низкий": ("baixo", "mais baixo", "o mais baixo", False),
           "быстрый": ("rápido", "mais rápido", "o mais rápido", False),
           "медленный": ("lento", "mais lento", "o mais lento", False),
           "хороший": ("bom", "melhor", "o melhor", True),
           "плохой": ("mau", "pior", "o pior", True)},
    "nl": {"высокий": ("groot", "groter", "het grootst", False),
           "низкий": ("klein", "kleiner", "het kleinst", False),
           "быстрый": ("snel", "sneller", "het snelst", False),
           "медленный": ("langzaam", "langzamer", "het langzaamst", False),
           "хороший": ("goed", "beter", "het best", True),
           "плохой": ("slecht", "slechter", "het slechtst", False)},
    "pl": {"высокий": ("wysoki", "wyższy", "najwyższy", False),
           "низкий": ("niski", "niższy", "najniższy", False),
           "быстрый": ("szybki", "szybszy", "najszybszy", False),
           "медленный": ("wolny", "wolniejszy", "najwolniejszy", False),
           "хороший": ("dobry", "lepszy", "najlepszy", True),
           "плохой": ("zły", "gorszy", "najgorszy", True)},
}
РЕЧЬ = {
    "ru": dict(ряд="{П}, {С}, {В} — три степени одного признака",
               неправильно=", и вторая не выводится из первой",
               сравнение="{A} {С}, чем {B}", вопрос="кто {В}?", значит="значит",
               вывод="значит, {A} {С}, чем {B}", двоеточие=": ", и=", а "),
    "en": dict(ряд="{П}, {С}, {В} — three degrees of one property",
               неправильно=", and the second does not follow from the first",
               сравнение="{A} is {С} than {B}", вопрос="who is {В}?", значит="so",
               вывод="so {A} is {С} than {B}", двоеточие=": ", и=", and "),
    "de": dict(ряд="{П}, {С}, {В} — drei Stufen einer Eigenschaft",
               неправильно=", und die zweite folgt nicht aus der ersten",
               сравнение="{A} ist {С} als {B}", вопрос="wer ist {В}?", значит="also",
               вывод="also ist {A} {С} als {B}", двоеточие=": ", и=", und "),
    "fr": dict(ряд="{П}, {С}, {В} — trois degrés d'une même qualité",
               неправильно=", et le deuxième ne suit pas du premier",
               сравнение="{A} est {С} que {B}", вопрос="qui est {В} ?", значит="donc",
               вывод="donc {A} est {С} que {B}", двоеточие=" : ", и=", et "),
    "es": dict(ряд="{П}, {С}, {В} — tres grados de una misma cualidad",
               неправильно=", y el segundo no se deriva del primero",
               сравнение="{A} es {С} que {B}", вопрос="¿quién es {В}?", значит="así que",
               вывод="así que {A} es {С} que {B}", двоеточие=": ", и=", y "),
    "it": dict(ряд="{П}, {С}, {В} — tre gradi di una stessa qualità",
               неправильно=", e il secondo non deriva dal primo",
               сравнение="{A} è {С} di {B}", вопрос="chi è {В}?", значит="quindi",
               вывод="quindi {A} è {С} di {B}", двоеточие=": ", и=", e "),
    "pt": dict(ряд="{П}, {С}, {В} — três graus de uma mesma qualidade",
               неправильно=", e o segundo não deriva do primeiro",
               сравнение="{A} é {С} do que {B}", вопрос="quem é {В}?", значит="portanto",
               вывод="portanto {A} é {С} do que {B}", двоеточие=": ", и=", e "),
    "nl": dict(ряд="{П}, {С}, {В} — drie trappen van één eigenschap",
               неправильно=", en de tweede volgt niet uit de eerste",
               сравнение="{A} is {С} dan {B}", вопрос="wie is {В}?", значит="dus",
               вывод="dus is {A} {С} dan {B}", двоеточие=": ", и=", en "),
    "pl": dict(ряд="{П}, {С}, {В} — trzy stopnie jednej cechy",
               неправильно=", a drugi nie wynika z pierwszego",
               сравнение="{A} jest {С} niż {B}", вопрос="kto jest {В}?", значит="więc",
               вывод="więc {A} jest {С} niż {B}", двоеточие=": ", и=", a "),
}
ФОРМЫ = ("ряд", "цепь", "обратное")


def имена(язык, сколько=3):
    """The corpus's own names, men only — the gendered degree is a named entrance, not a hole."""
    return [и for и, род, _ in F.A.ЛИЦА[язык] if род == "m"][:сколько]


def степени(язык, признак):
    return СЛОВА[язык][признак][:3]


def неправилен(язык, признак):
    return СЛОВА[язык][признак][3]


def противо(признак):
    for а, б in ПАРЫ:
        if признак == а:
            return б
        if признак == б:
            return а
    return None


def страница(язык, форма, признак, сдвиг=0):
    р, (П, С, В) = РЕЧЬ[язык], степени(язык, признак)
    если = р["неправильно"] if неправилен(язык, признак) else ""
    if форма == "ряд":
        return р["ряд"].format(П=П, С=С, В=В) + если + "."
    имена_ = имена(язык)
    A, B, C = имена_[сдвиг % 3], имена_[(сдвиг + 1) % 3], имена_[(сдвиг + 2) % 3]
    if форма == "цепь":
        # ПЕРЕХОДНОСТЬ ПРИЗНАКА: выше высокого — самый высокий, и основание названо
        первое = р["сравнение"].format(A=A, С=С, B=B)
        второе = р["сравнение"].format(A=B, С=С, B=C)
        return (первое + ". " + второе + ". " + р["вопрос"].format(В=В) + " " + A
                + р["двоеточие"] + первое + р["и"] + второе + ".")
    # ОБРАТНОЕ: обращение сравнения есть ПРОТИВОПОЛОЖНОЕ СЛОВО, а не отрицание.
    # Вывод несёт СВОЙ порядок слов: немецкий и голландский после «also»/«dus» ставят
    # глагол перед подлежащим, славянские и романские — нет, и это часть объявления языка.
    Спр = степени(язык, противо(признак))[1]
    return (р["сравнение"].format(A=A, С=С, B=B) + ". "
            + р["вывод"].format(A=B, С=Спр, B=A) + ".")


def _показы():
    вон = {}
    for язык in ЯЗЫКИ:
        for признак in ПРИЗНАКИ:
            вон[страница(язык, "ряд", признак)] = (язык, "ряд")
            for сдвиг in range(3):
                вон[страница(язык, "цепь", признак, сдвиг)] = (язык, "цепь")
            вон[страница(язык, "обратное", признак)] = (язык, "обратное")
    return вон


ПОКАЗЫ = _показы()


def _альт(слова):
    сорт = sorted({с for с in слова if с}, key=lambda с: (-len(с), с))
    return "(?:" + "|".join(re.escape(с) for с in сорт) + ")"


def _дыры(язык):
    имён = _альт(имена(язык))
    return {"A": имён, "B": имён, "C1": имён, "C2": имён,
            "П": _альт(степени(язык, п)[0] for п in ПРИЗНАКИ),
            "С": _альт(степени(язык, п)[1] for п in ПРИЗНАКИ),
            "С2": _альт(степени(язык, п)[1] for п in ПРИЗНАКИ),
            "В": _альт(степени(язык, п)[2] for п in ПРИЗНАКИ)}


def рамка(язык, форма, неправильна):
    р = РЕЧЬ[язык]
    если = р["неправильно"] if неправильна else ""
    if форма == "ряд":
        return р["ряд"] + если + "."
    if форма == "цепь":
        первое = р["сравнение"].format(A="{A}", С="{С}", B="{B}")
        второе = р["сравнение"].format(A="{B}", С="{С}", B="{C1}")
        return (первое + ". " + второе + ". " + р["вопрос"] + " {A}" + р["двоеточие"]
                + первое + р["и"] + второе + ".")
    return (р["сравнение"].format(A="{A}", С="{С}", B="{B}") + ". "
            + р["вывод"].format(A="{B}", С="{С2}", B="{A}") + ".")


def _образец(язык, форма, неправильна):
    дыры, счёт, куски = _дыры(язык), {}, []
    for кусок in re.split(r"(\{[^}]+\})", рамка(язык, форма, неправильна)):
        if кусок.startswith("{"):
            дыра = кусок[1:-1]
            счёт[дыра] = счёт.get(дыра, 0) + 1
            куски.append(f"(?P<h_{дыра}__{счёт[дыра]}>{дыры[дыра]})")
        else:
            куски.append(re.escape(кусок))
    return re.compile("^" + "".join(куски) + "$")


ОБРАЗЦЫ = [(_образец(язык, форма, н), язык, форма, н)
           for язык in ЯЗЫКИ for форма in ФОРМЫ for н in (False, True)]


def _значения(м):
    вон = {}
    for ключ, знач in м.groupdict().items():
        дыра, _ = ключ[2:].rsplit("__", 1)
        if дыра in вон and вон[дыра] != знач:
            return None
        вон[дыра] = знач
    return вон


def _признак(язык, ступень, слово):
    for п in ПРИЗНАКИ:
        if степени(язык, п)[ступень] == слово:
            return п
    return None


def _вердикт(язык, форма, неправильна, зн):
    if форма == "ряд":
        п = _признак(язык, 0, зн["П"])
        # РЯД ЕСТЬ РЯД ОДНОГО ПРИЗНАКА, И ПРИЗНАК НЕПРАВИЛЬНОСТИ ЕСТЬ ФАКТ ЯЗЫКА
        return (п is not None and (зн["С"], зн["В"]) == степени(язык, п)[1:]
                and неправилен(язык, п) == неправильна)
    if неправильна:  # прочие рамки признака неправильности не несут
        return False
    п = _признак(язык, 1, зн["С"])
    if п is None:
        return False
    if форма == "цепь":
        # ЦЕПЬ: превосходная того же признака, и три имени различны
        имена_ = (зн["A"], зн["B"], зн["C1"])
        return len(set(имена_)) == 3 and зн["В"] == степени(язык, п)[2]
    # ОБРАТНОЕ: вторая сравнительная есть сравнительная ПРОТИВОПОЛОЖНОГО слова
    return зн["A"] != зн["B"] and зн["С2"] == степени(язык, противо(п))[1]


def судить(строка):
    """(судимо, истинно): a page of the degrees whose words are one property's own; else silence."""
    с = строка.strip()
    if с in ПОКАЗЫ:
        return True, True
    for образ, язык, форма, неправильна in ОБРАЗЦЫ:
        м = образ.match(с)
        if not м:
            continue
        зн = _значения(м)
        if зн is None:
            return True, False
        return True, _вердикт(язык, форма, неправильна, зн)
    return False, False


def _самопроверка():
    for показ in ПОКАЗЫ:
        assert судить(показ) == (True, True), показ
    мутанты = 0
    for язык in ЯЗЫКИ:
        П, С, В = степени(язык, "высокий")
        Пн, Сн, Вн = степени(язык, "низкий")
        р = страница(язык, "ряд", "высокий")
        # (1) РЯД СМЕШАЛ ДВА ПРИЗНАКА
        битая = р.replace(", " + С + ",", ", " + Сн + ",", 1)
        assert судить(битая) == (True, False), битая
        # (2) ПРЕВОСХОДНАЯ ОТ ЧУЖОГО ПРИЗНАКА
        битая = р.replace(В, Вн)
        assert судить(битая) == (True, False), битая
        ц = страница(язык, "цепь", "высокий")
        assert судить(ц) == (True, True), ц
        # (3) ЦЕПЬ ОТВЕЧАЕТ СРЕДНИМ ИМЕНЕМ ВМЕСТО КРАЙНЕГО
        A, B, _C = имена(язык)
        битая = ц.replace("? " + A, "? " + B, 1)
        assert судить(битая) == (True, False), битая
        о = страница(язык, "обратное", "высокий")
        assert судить(о) == (True, True), о
        # (4) ОБРАТНОЕ НЕ ОБРАЩЕНО: то же слово вместо противоположного
        голова, хвост = о.split(". ", 1)
        битая = голова + ". " + хвост.replace(Сн, С, 1)
        assert судить(битая) == (True, False), битая
        мутанты += 4
        # (5) НЕПРАВИЛЬНОСТЬ ОБЪЯВЛЕНА ТАМ, ГДЕ ЕЁ НЕТ
        если = РЕЧЬ[язык]["неправильно"]
        битая = р[:-1] + если + "."
        assert судить(битая) == (True, False), битая
        мутанты += 1
        # (6) ЗАЧИН ВОПРОСА ОБЪЯВЛЕН ДОМОМ ПАРЫ
        вопрос = [ч for ч in ц.split(". ") if "?" in ч][0]
        вопрос = вопрос[:вопрос.index("?") + 1]
        assert asking.зачин_объявлен(вопрос) is not False, (язык, вопрос)
    for язык in ЯЗЫКИ:
        print("  ", страница(язык, "ряд", "хороший"))
    for язык in ("ru", "de", "pl"):
        print("  ", страница(язык, "цепь", "быстрый"))
        print("  ", страница(язык, "обратное", "высокий"))
    по_форме = {}
    for _, (_я, форма) in ПОКАЗЫ.items():
        по_форме[форма] = по_форме.get(форма, 0) + 1
    неправильных = sum(1 for я in ЯЗЫКИ for п in ПРИЗНАКИ if неправилен(я, п))
    print(f"  мутантов поймано: {мутанты}; неправильных степеней объявлено: {неправильных}")
    print(f"  дом пишет показов: {len(ПОКАЗЫ)} (языков {len(ЯЗЫКИ)}, признаков {len(ПРИЗНАКИ)}, "
          f"образцов {len(ОБРАЗЦЫ)}): " + ", ".join(f"{ф} {к}" for ф, к in по_форме.items()))


if __name__ == "__main__":
    _самопроверка()
