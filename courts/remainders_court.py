#!/usr/bin/env python3
"""[ОСТАТОК] — страницы дома деления с остатком, судимые замкнутым миром и пересчётом.

ПОВОД (24.09, прибор [ПОДСАДКА СЛОВОМ]). Мир `remainders` не был ничьим: «28 divide by 9 is 3
remainder 1: 9 × 3 = 27, 28 − 27 = 1» проходил палату истиной — арифметика читает леджер после
двоеточия, а слово действия перед ним не читал никто. Дом объявляет все свои страницы
(`gen_genesis_remainders.ПОКАЗЫ`), и суд берёт закон у него, а не пишет рамки второй раз.

    СТРОКА МИРА, КАКОЙ ДОМ НЕ ПИШЕТ, ЕСТЬ ЛОЖЬ ЭТОГО МИРА: замкнутый мир говорит о своём,
    и порча одного слова страницы есть порча страницы.

ПЕРЕСЧЁТ, А НЕ ВЕРА ПЕРЕЧНЮ: страница перечня судится своими числами — тождество «a = b × q + r»
требует и равенства, и остатка меньше делителя; «a divided by b is q remainder r» и «a
разделить на b будет q, остаток r» — того же, что даёт деление.

ГРАНИЦА: строка чужого мира, какой перечень не порождает и какая не расходится с ним одним
словом, суду не подсудна.

    python3 courts/remainders_court.py
"""
# ПУСТОЙ-ОБХОД: no-such-corpus-file
import pathlib
import re
import sys

КОРЕНЬ = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(КОРЕНЬ / "tools"))

import closedworld  # noqa: E402
from closedworld import Слой  # noqa: E402,F401 — палата подаёт имя мира лишь тому, кто ввёз Слой
import gen_genesis_remainders as R  # noqa: E402 — дом, объявивший страницы остатка

ИМЯ_СУДА = "remainders"
ЗАМКНУТЫЕ_МИРЫ = frozenset({"remainders"})

_ПО_ДЛИНЕ = {}
for _п in R.ПОКАЗЫ:
    _ПО_ДЛИНЕ.setdefault(len(_п.split(" ")), []).append(_п.split(" "))

_ТОЖДЕСТВО = re.compile(r"(?<![\d.])(\d+) = (\d+) × (\d+) \+ (\d+)(?![\d.])")
_ДЕЛЕНИЕ = re.compile(r"(?<![\d.])(\d+) (?:divided by|разделить на) (\d+) (?:is|будет) (\d+),? "
                      r"(?:remainder|остаток) (\d+)(?![\d.])")


def _порча_одним_словом(с):
    """Строка С ЧИСЛАМИ, разошедшаяся с показом РОВНО ОДНИМ словом, есть порча этой страницы.

    БЕЗ ЧИСЕЛ ПРАВИЛО НЕ ИДЁТ: «what is a foot?» соседнего мира расходится с «what is a
    remainder?» одним словом и порчей не является; строку без чисел в своём мире стережёт
    замыкание, а не сличение.
    """
    if not re.search(r"\d", с):
        return False
    слова = с.split(" ")
    for свои in _ПО_ДЛИНЕ.get(len(слова), ()):
        if sum(x != y for x, y in zip(свои, слова)) == 1:
            return True
    return False


def _деление_верно(a, b, q, r):
    return b > 0 and 0 <= r < b and a == b * q + r


def _судить(строка):
    с = строка.strip()
    if not с:
        return False, False
    if с not in R.ПОКАЗЫ:
        return (True, False) if _порча_одним_словом(с) else (False, False)
    for a, b, q, r in _ТОЖДЕСТВО.findall(с):
        if not _деление_верно(int(a), int(b), int(q), int(r)):
            return True, False
    for a, b, q, r in _ДЕЛЕНИЕ.findall(с):
        if not _деление_верно(int(a), int(b), int(q), int(r)):
            return True, False
    return True, True


судить = closedworld.замкнуть(_судить, ЗАМКНУТЫЕ_МИРЫ)


def _самопроверка():
    """Всякая страница дома истинна; порча слова действия и порча частного — ложь."""
    беды = [с for с in R.ПОКАЗЫ if _судить(с) != (True, True)]
    образец = next(с for с in R.ПОКАЗЫ if " divided by " in с and ":" in с)
    for порча in (образец.replace(" divided by ", " divide by ", 1),
                  re.sub(r" is (\d+) remainder", lambda м: f" is {int(м.group(1)) + 1} remainder", образец, count=1)):
        if _судить(порча)[1] is not False:
            беды.append(f"порча прошла: {порча[:80]}")
    return беды


def main():
    import genesis
    беды = _самопроверка()
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
    поза = "PASS" if ложных == 0 and not беды else "FAIL"
    print(f"ОСТАТОК {поза}: {ложных} ложных из {судимо} судимых (рубеж 0); страниц дома "
          f"{len(R.ПОКАЗЫ)}, бед самопроверки {len(беды)}")
    return 0 if поза == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
