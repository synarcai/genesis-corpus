#!/usr/bin/env python3
"""THE SIGNED WORLD — a number below zero is still a number (05.09).

Д-5 of the collegium's ranked defects. The corpus counts things, and things do not go below
nought: every market of goods, files, acts and shares lives on the natural numbers, and the
only signed numbers in the whole свод stand inside algebra («is −5 a root of x² + 16x + 60?»).
An organism that has never met a temperature below zero has no reason to believe that
addition can cross it — and no way to answer «it was −5, it got 8 degrees warmer, what is it
now?».

WHAT THIS HOUSE SHOWS. Two everyday frames where a language writes the minus sign without
apology — the thermometer and the floors of a house — and four movements over them:

    UPWARD ACROSS ZERO. «in the morning it was −5 degrees. it became 8 degrees warmer. how
    many degrees is it now? 3: −5 + 8 = 3.»

    DOWNWARD ACROSS ZERO. «in the morning it was 3 degrees. it became 8 degrees colder. how
    many degrees is it now? −5: 3 − 8 = −5.»

    THE DIFFERENCE THROUGH ZERO, which is the hard one and the point of the house: «how much
    warmer is 3 than −5? by 8: 3 − (−5) = 8.» Subtracting a negative is where a reader that
    learnt «minus makes smaller» breaks, and the ledger says plainly that it does not.

    THE LIFT FROM THE UNDERGROUND. «the lift is on floor −2. it goes up 5 floors. on which
    floor is it? 3: −2 + 5 = 3.» — the same arithmetic in a frame with no degrees in it, so
    that the sign is bought as a property of NUMBER, not as a word of weather.

THE COUNT FORM FOLLOWS THE ABSOLUTE VALUE, and that is written, not guessed: «−5 градусов»,
«−1 градус», «−2 градуса», «−5 stopni», «−2 stopnie». A language bends its noun by how many,
and «how many» knows no sign.

WHAT IS BORROWED: nine languages and the counting rule of the packs (through the house of the
pair). Declared here: the degree and the floor with their count forms, the frames of a morning
and a lift, the words of warmer and colder and of going up and down, and the openers of the
four questions.

WHAT IS NOT MEASURED, NAMED: multiplication by a negative, a negative count of things (there
is no such thing and the house does not pretend), and the zero itself as a special value —
zero here is a number the road passes through, not a subject.
"""
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import asking  # noqa: E402 — the house of the pair declares which openers a question may wear
import svampforms as S  # noqa: E402 — the count cell of a pack

ЯЗЫКИ = ("ru", "en", "de", "fr", "es", "it", "pt", "nl", "pl")
# ПАРЫ ТЕМПЕРАТУР: (что было, на сколько сдвинулось) — движение всегда ПЕРЕСЕКАЕТ ноль,
# иначе показ не о знаке, а о том же счёте
ВВЕРХ = ((-5, 8), (-3, 7), (-9, 12), (-2, 6), (-7, 10), (-4, 9), (-6, 11), (-1, 5),
         (-8, 13), (-12, 15), (-10, 14), (-11, 16), (-5, 6), (-3, 9), (-9, 10), (-2, 8),
         (-7, 12), (-4, 5), (-6, 7), (-1, 13), (-8, 9), (-13, 17), (-14, 18), (-15, 19),
         (-16, 20), (-17, 21), (-18, 22), (-19, 23), (-20, 24), (-2, 11), (-3, 14), (-4, 16),
         (-5, 18), (-6, 20), (-7, 22), (-9, 24), (-10, 12), (-11, 13), (-12, 17), (-13, 15))
ВНИЗ = ((3, 8), (4, 7), (2, 11), (6, 9), (5, 12), (1, 6), (7, 13), (8, 10),
        (9, 14), (10, 16), (12, 15), (11, 17), (3, 5), (4, 9), (2, 7), (6, 11),
        (5, 8), (1, 4), (7, 10), (8, 15), (9, 12), (13, 18), (14, 19), (15, 21),
        (16, 22), (17, 24), (18, 26), (19, 28), (20, 30), (2, 9), (3, 12), (4, 14),
        (6, 16), (7, 18), (8, 20), (9, 22), (10, 24), (11, 26), (12, 28), (14, 30))
# ЭТАЖИ: лифт из подземного этажа вверх
ЭТАЖИ = ((-2, 5), (-1, 4), (-3, 7), (-2, 9), (-4, 6), (-1, 8), (-3, 5), (-5, 9),
         (-2, 3), (-1, 6), (-3, 4), (-4, 9), (-5, 7), (-1, 11), (-2, 12), (-6, 8),
         (-7, 9), (-8, 10), (-9, 11), (-7, 12), (-8, 13), (-4, 14), (-3, 15), (-5, 16))
ГРАДУС = {
    "ru": ("градус", "градуса", "градусов"), "en": ("degree", "degrees"),
    "de": ("Grad", "Grad"), "fr": ("degré", "degrés"), "es": ("grado", "grados"),
    "it": ("grado", "gradi"), "pt": ("grau", "graus"), "nl": ("graad", "graden"),
    "pl": ("stopień", "stopnie", "stopni"),
}
ЭТАЖ = {
    "ru": ("этаж", "этажа", "этажей"), "en": ("floor", "floors"), "de": ("Etage", "Etagen"),
    "fr": ("étage", "étages"), "es": ("piso", "pisos"), "it": ("piano", "piani"),
    "pt": ("andar", "andares"), "nl": ("verdieping", "verdiepingen"),
    "pl": ("piętro", "piętra", "pięter"),
}
РЕЧЬ = {
    "ru": dict(утром="утром было {t} {Гt}.", теплее="стало на {d} {Гd} теплее.",
               холоднее="стало на {d} {Гd} холоднее.",
               вопрос_градус="сколько градусов стало?", ответ_градус="{v} {Гv}",
               вопрос_разность="на сколько {a} теплее, чем {b}?", ответ_разность="на {r}",
               лифт="лифт на {t} этаже.", вверх="лифт поднялся на {d} {Эd}.",
               вопрос_этаж="на каком этаже лифт?", ответ_этаж="на {v} этаже",
               двоеточие=": ", вопрос="?"),
    "en": dict(утром="in the morning it was {t} {Гt}.", теплее="it became {d} {Гd} warmer.",
               холоднее="it became {d} {Гd} colder.",
               вопрос_градус="how many degrees is it now?", ответ_градус="{v} {Гv}",
               вопрос_разность="by how much is {a} warmer than {b}?", ответ_разность="by {r}",
               лифт="the lift is on floor {t}.", вверх="the lift goes up {d} {Эd}.",
               вопрос_этаж="on which floor is the lift?", ответ_этаж="on floor {v}",
               двоеточие=": ", вопрос="?"),
    "de": dict(утром="am Morgen waren es {t} {Гt}.", теплее="es wurde um {d} {Гd} wärmer.",
               холоднее="es wurde um {d} {Гd} kälter.",
               вопрос_градус="wie viel Grad sind es jetzt?", ответ_градус="{v} {Гv}",
               вопрос_разность="um wie viel ist {a} wärmer als {b}?", ответ_разность="um {r}",
               лифт="der Aufzug ist auf Etage {t}.", вверх="der Aufzug fährt {d} {Эd} hoch.",
               вопрос_этаж="auf welcher Etage ist der Aufzug?", ответ_этаж="auf Etage {v}",
               двоеточие=": ", вопрос="?"),
    "fr": dict(утром="le matin il faisait {t} {Гt}.", теплее="il a fait {d} {Гd} de plus.",
               холоднее="il a fait {d} {Гd} de moins.",
               вопрос_градус="combien de degrés fait-il maintenant ?", ответ_градус="{v} {Гv}",
               вопрос_разность="de combien {a} est-il plus chaud que {b} ?", ответ_разность="de {r}",
               лифт="l'ascenseur est à l'étage {t}.", вверх="l'ascenseur monte de {d} {Эd}.",
               вопрос_этаж="à quel étage est l'ascenseur ?", ответ_этаж="à l'étage {v}",
               двоеточие=" : ", вопрос=" ?"),
    "es": dict(утром="por la mañana hacía {t} {Гt}.", теплее="subió {d} {Гd}.",
               холоднее="bajó {d} {Гd}.",
               вопрос_градус="¿cuántos grados hace ahora?", ответ_градус="{v} {Гv}",
               вопрос_разность="¿cuánto más caliente es {a} que {b}?", ответ_разность="{r}",
               лифт="el ascensor está en el piso {t}.", вверх="el ascensor sube {d} {Эd}.",
               вопрос_этаж="¿en qué piso está el ascensor?", ответ_этаж="en el piso {v}",
               двоеточие=": ", вопрос="?"),
    "it": dict(утром="la mattina c'erano {t} {Гt}.", теплее="è salito di {d} {Гd}.",
               холоднее="è sceso di {d} {Гd}.",
               вопрос_градус="quanti gradi ci sono adesso?", ответ_градус="{v} {Гv}",
               вопрос_разность="di quanto {a} è più caldo di {b}?", ответ_разность="di {r}",
               лифт="l'ascensore è al piano {t}.", вверх="l'ascensore sale di {d} {Эd}.",
               вопрос_этаж="a che piano è l'ascensore?", ответ_этаж="al piano {v}",
               двоеточие=": ", вопрос="?"),
    "pt": dict(утром="de manhã estavam {t} {Гt}.", теплее="subiu {d} {Гd}.",
               холоднее="desceu {d} {Гd}.",
               вопрос_градус="quantos graus estão agora?", ответ_градус="{v} {Гv}",
               вопрос_разность="quanto {a} é mais quente do que {b}?", ответ_разность="{r}",
               лифт="o elevador está no andar {t}.", вверх="o elevador sobe {d} {Эd}.",
               вопрос_этаж="em que andar está o elevador?", ответ_этаж="no andar {v}",
               двоеточие=": ", вопрос="?"),
    "nl": dict(утром="'s ochtends was het {t} {Гt}.", теплее="het werd {d} {Гd} warmer.",
               холоднее="het werd {d} {Гd} kouder.",
               вопрос_градус="hoeveel graden is het nu?", ответ_градус="{v} {Гv}",
               вопрос_разность="hoeveel warmer is {a} dan {b}?", ответ_разность="{r}",
               лифт="de lift is op verdieping {t}.", вверх="de lift gaat {d} {Эd} omhoog.",
               вопрос_этаж="op welke verdieping is de lift?", ответ_этаж="op verdieping {v}",
               двоеточие=": ", вопрос="?"),
    "pl": dict(утром="rano było {t} {Гt}.", теплее="zrobiło się cieplej o {d} {Гd}.",
               холоднее="zrobiło się chłodniej o {d} {Гd}.",
               вопрос_градус="ile stopni jest teraz?", ответ_градус="{v} {Гv}",
               вопрос_разность="o ile {a} jest cieplej niż {b}?", ответ_разность="o {r}",
               лифт="winda jest na piętrze {t}.", вверх="winda jedzie {d} {Эd} w górę.",
               вопрос_этаж="na którym piętrze jest winda?", ответ_этаж="na piętrze {v}",
               двоеточие=": ", вопрос="?"),
}
ФОРМЫ = ("потеплело", "похолодало", "разность_через_ноль", "лифт")
МИНУС = "−"          # знак корпуса, а не ASCII-дефис


def _знак(n):
    """«−5» пишется знаком корпуса; ноль без знака (дом через него проходит, а не стоит)."""
    return f"{МИНУС}{abs(n)}" if n < 0 else str(n)


def _первый(n):
    """ПЕРВОЕ СЛАГАЕМОЕ ЛЕДЖЕРА, ЕСЛИ ОНО ОТРИЦАТЕЛЬНО, СТОИТ В СКОБКАХ — и это не украшение.
    «на 3 этаже: −2 + 5 = 3» читается арифметически как «3 − 2 + 5 = 3», ибо минус между двумя
    числами есть знак действия, а двоеточие ему не преграда: суд арифметики звал ложью 112
    честных строк семи языков ровно по этой причине (замер 05.09). Скобка снимает двусмыслицу
    там, где она рождается, и попутно показывает сложение с отрицательным: «(−2) + 5 = 3»."""
    return f"({_знак(n)})" if n < 0 else str(n)


def _счётная(язык, таблица, n):
    """СЧЁТНАЯ ФОРМА ИДЁТ ПО МОДУЛЮ: «сколько» знака не знает («−5 градусов», «−1 градус»)."""
    return S._счёт(таблица[язык], abs(n), язык)


def рамка(язык, форма):
    р = РЕЧЬ[язык]
    if форма == "потеплело":
        return (р["утром"] + " " + р["теплее"] + " " + р["вопрос_градус"] + " "
                + р["ответ_градус"] + р["двоеточие"] + "{t0} + {d} = {v}.")
    if форма == "похолодало":
        return (р["утром"] + " " + р["холоднее"] + " " + р["вопрос_градус"] + " "
                + р["ответ_градус"] + р["двоеточие"] + "{t0} − {d} = {v}.")
    if форма == "разность_через_ноль":
        # ВЫЧИТАНИЕ ОТРИЦАТЕЛЬНОГО — ГЛАВНЫЙ ПОКАЗ ДОМА: «минус делает меньше» здесь ломается
        return (р["вопрос_разность"] + " " + р["ответ_разность"] + р["двоеточие"]
                + "{a} − ({b}) = {r}.")
    # ЛЕДЖЕР ЛИФТА СТОИТ ОТДЕЛЬНЫМ ПРЕДЛОЖЕНИЕМ, А НЕ ЗА ДВОЕТОЧИЕМ, И ЭТО ЗАМЕР: ответ
    # этажа кончается ЧИСЛОМ («auf Etage 3», «na piętrze 3»), и двоеточие после числа суд
    # арифметики читает как знак деления семи языков — 112 честных строк он звал ложью.
    # У градусов той беды нет: там перед двоеточием стоит слово («3 Grad:»).
    return (р["лифт"] + " " + р["вверх"] + " " + р["вопрос_этаж"] + " "
            + р["ответ_этаж"] + ". {t0} + {d} = {v}.")


def страница(язык, форма, t=0, d=0, a=0, b=0):
    р = РЕЧЬ[язык]
    if форма == "разность_через_ноль":
        r = a - b
        поля = dict(a=_знак(a), b=_знак(b), r=r)
        return рамка(язык, форма).format(**поля)
    if форма == "лифт":
        v = t + d
        поля = dict(t=_знак(t), t0=_первый(t), d=d, v=_знак(v), Эd=_счётная(язык, ЭТАЖ, d))
        return рамка(язык, форма).format(**поля)
    v = t + d if форма == "потеплело" else t - d
    поля = dict(t=_знак(t), t0=_первый(t), d=d, v=_знак(v), Гt=_счётная(язык, ГРАДУС, t),
                Гd=_счётная(язык, ГРАДУС, d), Гv=_счётная(язык, ГРАДУС, v))
    return рамка(язык, форма).format(**поля)


def _показы():
    вон = {}
    for язык in ЯЗЫКИ:
        for t, d in ВВЕРХ:
            вон[страница(язык, "потеплело", t=t, d=d)] = (язык, "потеплело")
            # РАЗНОСТЬ ЧЕРЕЗ НОЛЬ БЕРЁТ ТЕ ЖЕ ЧИСЛА С ДРУГОЙ СТОРОНЫ: 3 против −5
            вон[страница(язык, "разность_через_ноль", a=t + d, b=t)] = (язык, "разность_через_ноль")
        for t, d in ВНИЗ:
            вон[страница(язык, "похолодало", t=t, d=d)] = (язык, "похолодало")
        for t, d in ЭТАЖИ:
            вон[страница(язык, "лифт", t=t, d=d)] = (язык, "лифт")
    return вон


ПОКАЗЫ = _показы()


def _альт(слова):
    return "(?:" + "|".join(re.escape(с) for с in sorted({с for с in слова if с}, key=lambda с: (-len(с), с))) + ")"


def _образец(язык, шаблон):
    подписанное = r"(?:" + re.escape(МИНУС) + r")?\d+"
    в_скобках = r"(?:\(" + re.escape(МИНУС) + r"\d+\)|\d+)"
    дыры = {"t": подписанное, "t0": в_скобках, "v": подписанное, "a": подписанное, "b": подписанное,
            "d": r"\d+", "r": r"\d+",
            "Гt": _альт(ГРАДУС[язык]), "Гd": _альт(ГРАДУС[язык]), "Гv": _альт(ГРАДУС[язык]),
            "Эd": _альт(ЭТАЖ[язык])}
    счёт, куски = {}, []
    for кусок in re.split(r"(\{[^}]+\})", шаблон):
        if кусок.startswith("{"):
            дыра = кусок[1:-1]
            счёт[дыра] = счёт.get(дыра, 0) + 1
            куски.append(f"(?P<h_{дыра}__{счёт[дыра]}>{дыры[дыра]})")
        else:
            куски.append(re.escape(кусок))
    return re.compile("^" + "".join(куски) + "$")


ОБРАЗЦЫ = [(_образец(язык, рамка(язык, форма)), язык, форма)
           for язык in ЯЗЫКИ for форма in ФОРМЫ]


def _значения(м):
    вон = {}
    for ключ, знач in м.groupdict().items():
        дыра, _ = ключ[2:].rsplit("__", 1)
        if дыра in вон and вон[дыра] != знач:
            return None
        вон[дыра] = знач
    return вон


def _цел(с):
    с = с.strip("()")
    return -int(с[len(МИНУС):]) if с.startswith(МИНУС) else int(с)


def _вердикт(язык, форма, зн):
    if форма == "разность_через_ноль":
        a, b, r = _цел(зн["a"]), _цел(зн["b"]), int(зн["r"])
        # РАЗНОСТЬ ЧЕРЕЗ НОЛЬ ЕСТЬ РАЗНОСТЬ, И ОНА ПОЛОЖИТЕЛЬНА ЛИШЬ КОГДА a ВЫШЕ b
        return r == a - b and r > 0 and b < 0 < a
    t, d, v = _цел(зн["t"]), int(зн["d"]), _цел(зн["v"])
    if d < 1:
        return False
    # ПЕРВОЕ СЛАГАЕМОЕ ЛЕДЖЕРА ЕСТЬ ТО ЖЕ ЧИСЛО, ЧТО В ИСТОРИИ, И В СКОБКАХ, ЕСЛИ ОТРИЦАТЕЛЬНО
    if "t0" in зн and (_цел(зн["t0"]) != t or зн["t0"] != _первый(t)):
        return False
    if форма == "лифт":
        # ЛИФТ ИДЁТ ИЗ ПОДЗЕМНОГО ЭТАЖА ВВЕРХ И ПЕРЕСЕКАЕТ НОЛЬ
        if зн["Эd"] != _счётная(язык, ЭТАЖ, d):
            return False
        return v == t + d and t < 0 < v
    # СЧЁТНАЯ ФОРМА ГРАДУСА ИДЁТ ПО МОДУЛЮ ЕГО ЧИСЛА
    for дыра, число in (("Гt", t), ("Гd", d), ("Гv", v)):
        if дыра in зн and зн[дыра] != _счётная(язык, ГРАДУС, число):
            return False
    if форма == "потеплело":
        # ДВИЖЕНИЕ ПЕРЕСЕКАЕТ НОЛЬ: иначе показ не о знаке, а о том же счёте
        return v == t + d and t < 0 < v
    return v == t - d and v < 0 < t


def судить(строка):
    """(судимо, истинно): a page of a frame of the house whose signed sum recomputes."""
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
        # (1) СУММА ЧЕРЕЗ НОЛЬ НЕ СХОДИТСЯ
        п = страница(язык, "потеплело", t=-5, d=8)
        assert судить(п) == (True, True), п
        битая = п.replace("= 3.", "= 4.")
        assert судить(битая) == (True, False), битая
        # (2) РАЗНОСТЬ ВНИЗ НЕ СХОДИТСЯ
        х = страница(язык, "похолодало", t=3, d=8)
        assert судить(х) == (True, True), х
        битая = х.replace("= " + МИНУС + "5.", "= " + МИНУС + "4.")
        assert судить(битая) == (True, False), битая
        # (3) ВЫЧИТАНИЕ ОТРИЦАТЕЛЬНОГО ПРОЧИТАНО КАК СЛОЖЕНИЕ ЗНАКОВ («минус делает меньше»)
        р = страница(язык, "разность_через_ноль", a=3, b=-5)
        assert судить(р) == (True, True), р
        битая = р.replace("= 8.", "= 2.")
        assert судить(битая) == (True, False), битая
        # (4) ЛИФТ ПРИЕХАЛ НЕ ТУДА
        л = страница(язык, "лифт", t=-2, d=5)
        assert судить(л) == (True, True), л
        битая = л.replace("= 3.", "= 7.")
        assert судить(битая) == (True, False), битая
        мутанты += 4
        # (5) СЧЁТНАЯ ФОРМА ГРАДУСА — ФОРМА ЧУЖОГО ЧИСЛА
        своя, чужая = _счётная(язык, ГРАДУС, 5), _счётная(язык, ГРАДУС, 1)
        if своя != чужая:
            битая = п.replace(МИНУС + "5 " + своя, МИНУС + "5 " + чужая, 1)
            assert судить(битая) == (True, False), битая
            мутанты += 1
        # (6) ЗАЧИН ВОПРОСА ОБЪЯВЛЕН ДОМОМ ПАРЫ
        for стр in (п, х, р, л):
            вопрос = стр[:стр.index("?") + 1].split(". ")[-1]
            assert asking.зачин_объявлен(вопрос) is not False, (язык, вопрос)
    for язык in ЯЗЫКИ:
        print("  ", страница(язык, "потеплело", t=-5, d=8))
    for язык in ("ru", "en", "de", "pl"):
        print("  ", страница(язык, "похолодало", t=3, d=8))
        print("  ", страница(язык, "разность_через_ноль", a=3, b=-5))
        print("  ", страница(язык, "лифт", t=-2, d=5))
    по_форме = {}
    for _, (язык, форма) in ПОКАЗЫ.items():
        по_форме[форма] = по_форме.get(форма, 0) + 1
    print(f"  мутантов поймано: {мутанты}")
    print(f"  дом пишет показов: {len(ПОКАЗЫ)} (языков {len(ЯЗЫКИ)}, форм {len(ФОРМЫ)}, образцов {len(ОБРАЗЦЫ)}): "
          + ", ".join(f"{ф} {к}" for ф, к in по_форме.items()))


if __name__ == "__main__":
    _самопроверка()
