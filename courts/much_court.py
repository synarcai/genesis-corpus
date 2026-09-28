#!/usr/bin/env python3
"""[КРАТНОЕ ВЕЩЕСТВО] — «twice as much money as»: ответ пересчитывается из опоры и кратности (25.09).

Мир `much` пишет на двух языках опору, кратное сравнение несчётного, вопрос и ответ со звеном: «Ben has 30
dollars. Carla has twice as much money as Ben. how much money does Carla have? Carla has 60 dollars: 2 × 30 =
60.» Суд — вторая рука: лица, русский родительный и род лица — у пакетов, формы при числе — у дверей, и
считает он сам.

    СЛОВО КРАТНОСТИ И ЗНАК ЗВЕНА — ОДНО УТВЕРЖДЕНИЕ, СКАЗАННОЕ ДВАЖДЫ: «half» ИЛИ «вдвое меньше» ПРИ «×» — ЛОЖЬ.

Слово кратности — группа образца («twice|half|N times», «вдвое больше|вдвое меньше|в N раз больше»), и суд
сверяет его со знаком и множителем звена; опора после «as»/«чем» — то же лицо, что названо первым; спрошенное
лицо — то же в вопросе и ответе; мера при каждом числе — своей формы; русский глагол — рода своего лица.

ГРАНИЦА: строка чужого мира этих образцов суду не подсудна; мир `much` замкнут.

    python3 courts/much_court.py
"""
# ПУСТОЙ-ОБХОД: no-such-corpus-file
import json
import pathlib
import re
import sys

КОРЕНЬ = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(КОРЕНЬ / "tools"))
import closedworld  # noqa: E402
import rugram  # noqa: E402 — формы при числе, винительный длительности, прошедшее по роду
from closedworld import Слой  # noqa: E402,F401 — палата подаёт имя мира лишь тому, кто ввёз Слой
from plural import by_count  # noqa: E402

ИМЯ_СУДА = "much"
ЗАМКНУТЫЕ_МИРЫ = frozenset({"much"})
# РУБЕЖ-ДОЛГА: ЛОЖНЫХ_РУБЕЖ = 0
ЛОЖНЫХ_РУБЕЖ = 0

_ПАКЕТЫ = {я: json.loads((КОРЕНЬ / "tools" / "langpacks" / f"{я}.json").read_text(encoding="utf-8"))
           for я in ("en", "ru")}
_ЛИЦА_RU = {и: ф for и, ф in _ПАКЕТЫ["ru"]["person_forms"].items() if ф.get("gen") and ф.get("gender")}
ПО_РОДИТЕЛЬНОМУ = {ф["gen"]: и for и, ф in _ЛИЦА_RU.items()}


def _альт(слова):
    return "(?:" + "|".join(re.escape(с) for с in sorted(set(слова), key=lambda с: (-len(с), с))) + ")"


И_EN = _альт(_ПАКЕТЫ["en"]["person_names"])
И_RU = _альт(_ЛИЦА_RU)
Г_RU = _альт(ПО_РОДИТЕЛЬНОМУ)
ч = r"\d+"
К_EN = r"(?P<k>twice|half|\d+ times)"
К_RU = r"(?P<k>вдвое больше|вдвое меньше|в \d+ раза? больше|в \d+ раз больше)"
ЗВЕНО = rf"(?P<x>{ч}) (?P<op>[×÷]) (?P<y>{ч}) = (?P<z>{ч})\.$"
ГЛ = r"потратила?"

ОБРАЗЦЫ = (
    ("en", "деньги", re.compile(
        rf"^(?P<p>{И_EN}) has (?P<n>{ч}) (?P<u1>dollars?)\. (?P<q>{И_EN}) has {К_EN} as much money as "
        rf"(?P<p2>{И_EN})\. how much money does (?P<q2>{И_EN}) have\? (?P<q3>{И_EN}) has (?P<m>{ч}) "
        rf"(?P<u2>dollars?): {ЗВЕНО}")),
    ("en", "вода", re.compile(
        rf"^(?P<p>{И_EN}) has (?P<n>{ч}) (?P<u1>litres?) of water\. (?P<q>{И_EN}) has {К_EN} as much water as "
        rf"(?P<p2>{И_EN})\. how much water does (?P<q2>{И_EN}) have\? (?P<q3>{И_EN}) has (?P<m>{ч}) "
        rf"(?P<u2>litres?) of water: {ЗВЕНО}")),
    ("en", "время", re.compile(
        rf"^(?P<p>{И_EN}) spent (?P<n>{ч}) (?P<u1>minutes?) on homework\. (?P<q>{И_EN}) spent {К_EN} as much "
        rf"time on homework as (?P<p2>{И_EN})\. how much time did (?P<q2>{И_EN}) spend on homework\? "
        rf"(?P<q3>{И_EN}) spent (?P<m>{ч}) (?P<u2>minutes?) on homework: {ЗВЕНО}")),
    ("ru", "деньги", re.compile(
        rf"^у (?P<pg>{Г_RU}) (?P<n>{ч}) (?P<u1>руб\w+)\. у (?P<qg>{Г_RU}) {К_RU} денег, чем у (?P<pg2>{Г_RU})\. "
        rf"сколько денег у (?P<qg2>{Г_RU})\? у (?P<qg3>{Г_RU}) (?P<m>{ч}) (?P<u2>руб\w+): {ЗВЕНО}")),
    ("ru", "вода", re.compile(
        rf"^у (?P<pg>{Г_RU}) (?P<n>{ч}) (?P<u1>литр\w*) воды\. у (?P<qg>{Г_RU}) {К_RU} воды, чем у "
        rf"(?P<pg2>{Г_RU})\. сколько воды у (?P<qg2>{Г_RU})\? у (?P<qg3>{Г_RU}) (?P<m>{ч}) (?P<u2>литр\w*) воды: "
        rf"{ЗВЕНО}")),
    ("ru", "время", re.compile(
        rf"^(?P<p>{И_RU}) (?P<v1>{ГЛ}) на уроки (?P<n>{ч}) (?P<u1>минут\w*)\. (?P<q>{И_RU}) (?P<v2>{ГЛ}) на уроки "
        rf"{К_RU} времени, чем (?P<p2>{И_RU})\. сколько времени (?P<q2>{И_RU}) (?P<v3>{ГЛ}) на уроки\? "
        rf"(?P<q3>{И_RU}) (?P<v4>{ГЛ}) на уроки (?P<m>{ч}) (?P<u2>минут\w*): {ЗВЕНО}")),
)
МЕРА_EN = {"деньги": "dollars", "вода": "litres", "время": "minutes"}
МЕРА_RU = {"деньги": "рубль", "вода": "литр"}


def _кратность(язык, k):
    """(множитель, знак) по слову кратности, или None."""
    if язык == "en":
        if k == "twice":
            return 2, "×"
        if k == "half":
            return 2, "÷"
        множ = int(k.split()[0])
        return (множ, "×") if множ >= 3 else None
    if k == "вдвое больше":
        return 2, "×"
    if k == "вдвое меньше":
        return 2, "÷"
    множ = int(k.split()[1])
    return (множ, "×") if множ >= 3 and k.split()[2] == rugram.форма("раз", множ) else None


def _глагол_лица(кто, глагол):
    ф = _ЛИЦА_RU.get(кто)
    return ф is not None and глагол == rugram.прошедшее_рода("потратил", "ж" if ф["gender"] == "f" else "м")


def _верно(язык, вещество, г):
    # лица: опора и спрошенный — разные, каждое названо одинаково во всех местах
    if "p" in г:
        if г["p"] != г["p2"] or not г["q"] == г["q2"] == г["q3"] or г["p"] == г["q"]:
            return False
        if язык == "ru" and not all(_глагол_лица(г[л], г[в]) for л, в in
                                    (("p", "v1"), ("q", "v2"), ("q2", "v3"), ("q3", "v4"))):
            return False
    elif г["pg"] != г["pg2"] or not г["qg"] == г["qg2"] == г["qg3"] or г["pg"] == г["qg"]:
        return False
    кр = _кратность(язык, г["k"])
    if кр is None:
        return False
    множ, зн = кр
    n, m, x, y, z = (int(г[к]) for к in ("n", "m", "x", "y", "z"))
    if г["op"] != зн or z != m or n < 1:
        return False
    if зн == "×" and not (x == множ and y == n and m == множ * n):
        return False
    if зн == "÷" and not (x == n and y == множ and n % множ == 0 and m == n // множ):
        return False
    # мера при каждом числе — своей формы
    if язык == "en":
        return г["u1"] == by_count(n, МЕРА_EN[вещество]) and г["u2"] == by_count(m, МЕРА_EN[вещество])
    if вещество == "время":
        return (г["u1"] == rugram.винительный_при_числе("минута", n)
                and г["u2"] == rugram.винительный_при_числе("минута", m))
    return г["u1"] == rugram.форма(МЕРА_RU[вещество], n) and г["u2"] == rugram.форма(МЕРА_RU[вещество], m)


def _судить(строка):
    с = строка.strip()
    if not с:
        return False, False
    for язык, вещество, образец in ОБРАЗЦЫ:
        м = образец.match(с)
        if м:
            return True, _верно(язык, вещество, м.groupdict())
    return False, False


судить = closedworld.замкнуть(_судить, ЗАМКНУТЫЕ_МИРЫ)


def _самопроверка():
    """Всякая страница дома истинна; порча итога, слова кратности и знака звена — ложь."""
    import gen_genesis_much as Д  # noqa: PLC0415 — подсадки от страниц дома, не от литерала сцены
    беды = [с for с in Д.ПОКАЗЫ if _судить(с) != (True, True)]
    порч = 0
    обмен = (("twice", "half"), ("half", "twice"), ("вдвое больше", "вдвое меньше"), ("вдвое меньше", "вдвое больше"))
    for i, с in enumerate(sorted(Д.ПОКАЗЫ)):
        if i % 3:
            continue
        м = re.search(r"= (\d+)\.$", с)
        порчи = [с[:м.start(1)] + f"{int(м.group(1)) + 1}.",
                 с.replace(" × ", " ÷ ", 1) if " × " in с else с.replace(" ÷ ", " × ", 1)]
        for a, b in обмен:
            if f" {a} " in с:
                порчи.append(с.replace(f" {a} ", f" {b} ", 1))
                break
        for порча in порчи:
            порч += 1
            if порча == с or _судить(порча) != (True, False):
                беды.append(f"порча прошла: {порча[:100]}")
    return беды, порч, len(Д.ПОКАЗЫ)


def main():
    import genesis
    беды, порч, страниц = _самопроверка()
    for б in беды[:3]:
        print(f"  САМОПРОВЕРКА: {б}")
    судимо = ложных = 0
    примеры = []
    for путь in genesis.worlds(kind="shows"):
        for строка in путь.read_text(encoding="utf-8", errors="replace").split("\n"):
            если, верно = судить(строка)[:2]
            if not если:
                continue
            судимо += 1
            if not верно:
                ложных += 1
                if len(примеры) < 5:
                    примеры.append(f"{путь.stem}: {строка.strip()[:90]}")
    for п in примеры:
        print(f"  {п}")
    поза = "PASS" if ложных <= ЛОЖНЫХ_РУБЕЖ and not беды else "FAIL"
    print(f"КРАТНОЕ ВЕЩЕСТВО {поза}: {ложных} ложных из {судимо} судимых (рубеж {ЛОЖНЫХ_РУБЕЖ}); страниц дома "
          f"{страниц}, порч самопроверки {порч}, бед {len(беды)}")
    return 0 if поза == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
