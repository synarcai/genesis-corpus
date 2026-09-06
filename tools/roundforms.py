#!/usr/bin/env python3
"""THE HOUSE OF ROUNDING — the rule of the half is DECLARED, not derived (06.09).

The census found THREE lines of rounding in the whole свод. Rounding is the one everyday
arithmetic whose answer is not forced by the numbers alone: forty-three goes to forty and
forty-seven to fifty because the nearer end wins, but forty-FIVE stands at equal distance from
both, and what happens then is a CONVENTION — this corpus declares «the half goes up», and
declares it on the page, in every language, so that no reader has to guess which school it was
taught in.

THREE SHAPES, AND THE THIRD IS THE WHOLE POINT.

    THE NEARER END. «43 to the nearest ten: 40, because 43 − 40 = 3 and 50 − 43 = 7.» The
    ledger names BOTH distances: rounding is a comparison, not a truncation, and a page that
    merely drops the last digit would answer 40 for 47 as well.

    THE HUNDRED. The same law one step up («437 to the nearest hundred: 400»), so that the
    base of rounding is seen as a base and not as «the last digit».

    THE HALF. «45 to the nearest ten: 50, the half goes up» — the declared rule, named on the
    page as a rule and not smuggled in as arithmetic.

WHAT IS BORROWED: nine languages and the openers of the house of the pair. Declared here: the
verb of rounding and the name of each base in every language, and the sentence of the rule of
the half.

WHAT IS NOT MEASURED, NAMED: rounding down or up by fiat («floor», «ceiling»), rounding of a
fraction, and the banker's rule (half to even) — a corpus may declare only one convention at a
time, and the one it declares must be visible.
"""
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import asking  # noqa: E402 — the house of the pair declares which openers a question may wear

ЯЗЫКИ = ("ru", "en", "de", "fr", "es", "it", "pt", "nl", "pl")
ОСНОВЫ = (10, 100)
# ЧИСЛА ДЛЯ ДЕСЯТКОВ: ни одно не кончается нулём и не есть половина (те стоят особо)
ДЕСЯТКИ = (43, 47, 61, 68, 72, 79, 84, 26, 31, 58, 93, 17, 34, 66, 89, 22)
СОТНИ = (437, 462, 518, 673, 741, 826, 154, 289, 361, 594, 638, 972, 213, 748, 385, 906)
ПОЛОВИНЫ_10 = (45, 65, 25, 85, 35, 75, 15, 95)
ПОЛОВИНЫ_100 = (450, 650, 250, 850, 350, 750, 150, 950)
РЕЧЬ = {
    "ru": dict(вопрос="сколько будет {N}, если округлить {ДО}?", ответ="{R}",
               до={10: "до десятков", 100: "до сотен"},
               потому="{N} − {L} = {a}, {H} − {N} = {b}", правило="половина идёт вверх",
               двоеточие=": "),
    "en": dict(вопрос="what is {N} rounded {ДО}?", ответ="{R}",
               до={10: "to the nearest ten", 100: "to the nearest hundred"},
               потому="{N} − {L} = {a}, {H} − {N} = {b}", правило="the half goes up",
               двоеточие=": "),
    "de": dict(вопрос="wie lautet {N} gerundet {ДО}?", ответ="{R}",
               до={10: "auf Zehner", 100: "auf Hunderter"},
               потому="{N} − {L} = {a}, {H} − {N} = {b}", правило="die Hälfte geht nach oben",
               двоеточие=": "),
    "fr": dict(вопрос="quel est {N} arrondi {ДО} ?", ответ="{R}",
               до={10: "à la dizaine", 100: "à la centaine"},
               потому="{N} − {L} = {a}, {H} − {N} = {b}", правило="la moitié monte",
               двоеточие=" : "),
    "es": dict(вопрос="¿cuánto es {N} redondeado {ДО}?", ответ="{R}",
               до={10: "a la decena", 100: "a la centena"},
               потому="{N} − {L} = {a}, {H} − {N} = {b}", правило="la mitad sube",
               двоеточие=": "),
    "it": dict(вопрос="quanto fa {N} arrotondato {ДО}?", ответ="{R}",
               до={10: "alla decina", 100: "al centinaio"},
               потому="{N} − {L} = {a}, {H} − {N} = {b}", правило="la metà sale",
               двоеточие=": "),
    "pt": dict(вопрос="quanto é {N} arredondado {ДО}?", ответ="{R}",
               до={10: "à dezena", 100: "à centena"},
               потому="{N} − {L} = {a}, {H} − {N} = {b}", правило="a metade sobe",
               двоеточие=": "),
    "nl": dict(вопрос="hoeveel is {N} afgerond {ДО}?", ответ="{R}",
               до={10: "op tientallen", 100: "op honderdtallen"},
               потому="{N} − {L} = {a}, {H} − {N} = {b}", правило="de helft gaat omhoog",
               двоеточие=": "),
    "pl": dict(вопрос="ile wynosi {N} zaokrąglone {ДО}?", ответ="{R}",
               до={10: "do dziesiątek", 100: "do setek"},
               потому="{N} − {L} = {a}, {H} − {N} = {b}", правило="połowa idzie w górę",
               двоеточие=": "),
}
ФОРМЫ = ("ближе", "половина")


def _края(n, осн):
    """Нижний и верхний края основания: между ними и лежит число."""
    низ = (n // осн) * осн
    return низ, низ + осн


def рамка(язык, форма, осн):
    р = РЕЧЬ[язык]
    вопрос = р["вопрос"].replace("{ДО}", р["до"][осн])
    если = р["потому"]
    if форма == "ближе":
        # ЛЕДЖЕР НАЗЫВАЕТ ОБА РАССТОЯНИЯ: округление есть СРАВНЕНИЕ, а не отбрасывание цифры
        return вопрос + " {R}" + р["двоеточие"] + если + "."
    # ПОЛОВИНА: расстояния равны, и решает ОБЪЯВЛЕННОЕ правило
    return вопрос + " {R}" + р["двоеточие"] + если + ", " + р["правило"] + "."


def страница(язык, форма, n, осн):
    низ, верх = _края(n, осн)
    a, b = n - низ, верх - n
    r = верх if b <= a else низ
    return рамка(язык, форма, осн).format(N=n, R=r, L=низ, H=верх, a=a, b=b)


def _показы():
    вон = {}
    for язык in ЯЗЫКИ:
        for n in ДЕСЯТКИ:
            вон[страница(язык, "ближе", n, 10)] = (язык, "ближе")
        for n in СОТНИ:
            вон[страница(язык, "ближе", n, 100)] = (язык, "ближе")
        for n in ПОЛОВИНЫ_10:
            вон[страница(язык, "половина", n, 10)] = (язык, "половина")
        for n in ПОЛОВИНЫ_100:
            вон[страница(язык, "половина", n, 100)] = (язык, "половина")
    return вон


ПОКАЗЫ = _показы()


def _образец(язык, форма, осн):
    дыры = {"N": r"\d+", "R": r"\d+", "L": r"\d+", "H": r"\d+", "a": r"\d+", "b": r"\d+"}
    счёт, куски = {}, []
    for кусок in re.split(r"(\{[^}]+\})", рамка(язык, форма, осн)):
        if кусок.startswith("{"):
            дыра = кусок[1:-1]
            счёт[дыра] = счёт.get(дыра, 0) + 1
            куски.append(f"(?P<h_{дыра}__{счёт[дыра]}>{дыры[дыра]})")
        else:
            куски.append(re.escape(кусок))
    return re.compile("^" + "".join(куски) + "$")


ОБРАЗЦЫ = [(_образец(язык, форма, осн), язык, форма, осн)
           for язык in ЯЗЫКИ for форма in ФОРМЫ for осн in ОСНОВЫ]


def _значения(м):
    вон = {}
    for ключ, знач in м.groupdict().items():
        дыра, _ = ключ[2:].rsplit("__", 1)
        if дыра in вон and вон[дыра] != знач:
            return None
        вон[дыра] = знач
    return вон


def _вердикт(форма, осн, зн):
    n, r, L, H = (int(зн[к]) for к in ("N", "R", "L", "H"))
    a, b = int(зн["a"]), int(зн["b"])
    низ, верх = _края(n, осн)
    # КРАЯ СУТЬ КРАЯ ЭТОГО ОСНОВАНИЯ, А РАССТОЯНИЯ — ИХ РАЗНОСТИ
    if (L, H) != (низ, верх) or a != n - низ or b != верх - n:
        return False
    if форма == "половина":
        # ПОЛОВИНА ЕСТЬ РАВЕНСТВО РАССТОЯНИЙ, И ТОГДА ПРАВИЛО ОБЪЯВЛЕНО: вверх
        return a == b and r == верх
    if a == b:
        return False          # равные расстояния судит форма половины, а не эта
    return r == (верх if b < a else низ)


def судить(строка):
    """(судимо, истинно): a page of a frame of the house whose rounding compares; else silence."""
    с = строка.strip()
    if с in ПОКАЗЫ:
        return True, True
    for образ, язык, форма, осн in ОБРАЗЦЫ:
        м = образ.match(с)
        if not м:
            continue
        зн = _значения(м)
        if зн is None:
            return True, False
        return True, _вердикт(форма, осн, зн)
    return False, False


def _самопроверка():
    for показ in ПОКАЗЫ:
        assert судить(показ) == (True, True), показ
    мутанты = 0
    for язык in ЯЗЫКИ:
        # (1) ОТБРОШЕНА ЦИФРА ВМЕСТО СРАВНЕНИЯ: 47 → 40
        п = страница(язык, "ближе", 47, 10)
        assert судить(п) == (True, True), п
        битая = п.replace("? 50", "? 40")
        assert судить(битая) == (True, False), битая
        # (2) РАССТОЯНИЕ ПОСЧИТАНО НЕВЕРНО
        битая = п.replace("50 − 47 = 3", "50 − 47 = 4")
        assert судить(битая) == (True, False), битая
        # (3) ПОЛОВИНА УШЛА ВНИЗ ВОПРЕКИ ОБЪЯВЛЕННОМУ ПРАВИЛУ
        пол = страница(язык, "половина", 45, 10)
        assert судить(пол) == (True, True), пол
        битая = пол.replace("? 50", "? 40")
        assert судить(битая) == (True, False), битая
        # (4) СОТНИ: взят не тот край
        с100 = страница(язык, "ближе", 437, 100)
        assert судить(с100) == (True, True), с100
        битая = с100.replace("? 400", "? 500")
        assert судить(битая) == (True, False), битая
        мутанты += 4
        # (5) ЗАЧИН ВОПРОСА ОБЪЯВЛЕН ДОМОМ ПАРЫ
        for стр in (п, пол, с100):
            вопрос = стр[:стр.index("?") + 1].split(". ")[-1]
            assert asking.зачин_объявлен(вопрос) is not False, (язык, вопрос)
    for язык in ЯЗЫКИ:
        print("  ", страница(язык, "ближе", 43, 10))
    for язык in ("ru", "en", "pl"):
        print("  ", страница(язык, "половина", 45, 10))
        print("  ", страница(язык, "ближе", 437, 100))
    по_форме = {}
    for _, (язык, форма) in ПОКАЗЫ.items():
        по_форме[форма] = по_форме.get(форма, 0) + 1
    print(f"  мутантов поймано: {мутанты}")
    print(f"  дом пишет показов: {len(ПОКАЗЫ)} (языков {len(ЯЗЫКИ)}, форм {len(ФОРМЫ)}, оснований {len(ОСНОВЫ)}, "
          f"образцов {len(ОБРАЗЦЫ)}): " + ", ".join(f"{ф} {к}" for ф, к in по_форме.items()))


if __name__ == "__main__":
    _самопроверка()
