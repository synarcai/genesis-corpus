#!/usr/bin/env python3
"""[ПОСПЕШНОСТЬ COURT] — every arithmetic claim of the line is RECOMPUTED.

The third world judged by computation rather than by membership. This court
does not read the house's frames at all: it reads the LINE, finds every claim
it can check, and checks it.

  · «lhs = rhs» where both sides are purely numeric (digits with + − × ÷ ^ ² !)
    — evaluated and compared;
  · «V is prime» in any of the five declared wordings — V must be prime;
  · «V is not prime» — V must be composite.

A claim carrying a variable («n × n») is not numeric and is skipped: the court
checks what it can compute and stays silent about the rest. The strength is
that a swapped digit anywhere — a case, the counterexample, its factorisation —
is caught without the court knowing what the house meant to say.
"""
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "tools"))
import induforms as F  # noqa: E402

import closedworld  # noqa: E402
from closedworld import Слой  # noqa: E402 — the palata hands the world's name

ЗАМКНУТЫЕ_МИРЫ = frozenset({"indu"})

# СЛОВА ПРОСТОТЫ пяти языков — объявлены домом, читаются судом
# ИГЛЫ СТРОЧНЫЕ, ИБО СРАВНЕНИЕ ИДЁТ ПО СТРОЧНОЙ СТРОКЕ. Немецкое «ist eine
# Primzahl» с большой буквы не находилось в строчном тексте, и весь немецкий
# ряд голых чисел выпадал из суда — молча, как несудимый.
ПРОСТО = ("— простое", "is prime", "ist eine primzahl", "est premier", "es primo")
НЕ_ПРОСТО = ("не просто", "is not prime", "ist keine primzahl", "n'est pas premier", "no es primo")
# ПОДЛЕЖАЩЕЕ ПРОСТОТЫ ЕСТЬ ГОЛОЕ ЧИСЛО ПОСЛЕ ПОСЛЕДНЕГО РАЗДЕЛИТЕЛЯ, а не
# последнее число перед словом. «2^n − 1 is prime for every prime n» кончается
# цифрой 1, и суд, читавший последнее число, объявлял единицу непростой и
# всякое ОБЩЕЕ утверждение — ложью. Общее утверждение о переменной не
# проверяется вовсе: проверять в нём нечего, а молчать о непроверяемом суд
# обязан.
_ЧИСЛО_ПЕРЕД = re.compile(r"^\s*(\d+)\s*$")
_ВЫРАЖЕНИЕ = re.compile(r"[\d\s+\-−×÷^²!()]+")


def _вычислить(текст):
    """Значение чисто числового выражения, или None. Знаки — те, что пишет дом."""
    т = текст.strip()
    if not т or not any(c.isdigit() for c in т):
        return None
    if not _ВЫРАЖЕНИЕ.fullmatch(т):
        return None
    т = т.replace("−", "-").replace("×", "*").replace("÷", "/").replace("^", "**")
    т = re.sub(r"(\d+)²", r"(\1**2)", т)
    т = re.sub(r"(\d+)!", lambda м: str(_факт(int(м.group(1)))), т)
    try:
        значение = eval(т, {"__builtins__": {}}, {})   # только цифры и знаки — см. образец выше
    except (SyntaxError, ZeroDivisionError, TypeError, NameError):
        return None
    return значение


def _факт(n):
    ф = 1
    for i in range(2, n + 1):
        ф *= i
    return ф


_ВЛЕВО = re.compile(r"[\d\s+\-−×÷^²!()]+$")
_ВПРАВО = re.compile(r"^[\d\s+\-−×÷^²!()]+")


def _равенства(предложение):
    """[(значение слева, значение справа)] по каждому «=».

    ПЛЕЧО РАВЕНСТВА БЕРЁТСЯ ПРОБЕГОМ ОТ ЗНАКА, А НЕ РАЗБИЕНИЕМ СТРОКИ, и это
    не мелочь: «нет: при n = 40 выходит 1681, а 1681 = 41 × 41.» при разбиении
    даёт куском «40 выходит 1681, а 1681», который не вычисляется, — и
    РАЗЛОЖЕНИЕ КОНТРПРИМЕРА, главное число показа, оставалось непроверенным.
    Пробег влево от «=» останавливается на первой букве: у «n = 40» плечо
    пусто, и равенство с переменной честно пропускается.
    """
    вон = []
    for м in re.finditer("=", предложение):
        л = _ВЛЕВО.search(предложение[:м.start()])
        п_ = _ВПРАВО.match(предложение[м.end():])
        if not л or not п_:
            continue
        a, b = _вычислить(л.group()), _вычислить(п_.group())
        if a is not None and b is not None:
            вон.append((a, b))
    return вон


def _судить(строка):
    с = строка.strip()
    if not с:
        return False, False
    предложения = [п.strip().rstrip(".?!") for п in re.split(r"(?<=[.?])\s+", с) if п.strip()]
    проверено = 0
    for п in предложения:
        for a, b in _равенства(п):
            проверено += 1
            if a != b:
                return True, False
        низ = п.lower()
        for слово in НЕ_ПРОСТО:
            if слово in низ:
                м = _ЧИСЛО_ПЕРЕД.match(re.split(r"[=:,;]", п[:низ.index(слово)])[-1])
                if м:
                    проверено += 1
                    if F.просто(int(м.group(1))):
                        return True, False
                break
        else:
            for слово in ПРОСТО:
                if слово in низ:
                    м = _ЧИСЛО_ПЕРЕД.match(re.split(r"[=:,;]", п[:низ.index(слово)])[-1])
                    if м:
                        проверено += 1
                        if not F.просто(int(м.group(1))):
                            return True, False
                    break
    return (True, True) if проверено else (False, False)


судить = closedworld.замкнуть(_судить, ЗАМКНУТЫЕ_МИРЫ)


def main():
    import collections
    from genesis import worlds
    # ПРЕДСТАВЛЕННОЕ «НЕТ» (М-106): подменённый случай, подменённое разложение,
    # составное, названное простым — все три ловятся ПЕРЕСЧЁТОМ.
    подсадки = ("0² + 0 + 41 = 42 — простое.",
                "нет: при n = 40 выходит 1681, а 1681 = 40 × 42.",
                "1 + 3 + 5 = 4 × 4.",
                "9 — простое.")
    пойманы = sum(1 for п in подсадки if _судить(п) == (True, False))
    if пойманы != len(подсадки):
        for п in подсадки:
            print(f"  ПОДСАДКА {_судить(п)}: {п}")
        print(f"ПОСПЕШНОСТЬ FAIL: подсадок поймано {пойманы} из {len(подсадки)}")
        return 1
    итог = collections.Counter(); примеры = []
    for путь in worlds(kind="shows"):
        if путь.name != "genesis_indu.txt":
            continue
        for с in путь.read_text(encoding="utf-8").splitlines():
            if not с.strip() or с.startswith("\x0c"):
                continue
            судимо, истинно = судить(с)
            итог["судимых" if судимо else "несудимых"] += 1
            if судимо and not истинно:
                итог["ложных"] += 1
                if len(примеры) < 5:
                    примеры.append(с)
    for п in примеры:
        print(f"  ЛОЖЬ: {п[:120]}")
    поза = "PASS" if итог["ложных"] == 0 and итог["несудимых"] == 0 else "FAIL"
    print(f"ПОСПЕШНОСТЬ {поза}: {итог['ложных']} ложных из {итог['судимых']} судимых, "
          f"несудимых {итог['несудимых']}; подсадок поймано {пойманы} из {len(подсадки)}")
    return 0 if поза == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
