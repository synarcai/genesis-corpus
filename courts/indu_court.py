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

THE BORDER IS TAKEN FROM THE SUBJECT, NOT FROM THE WINDOW (М-180-f2). Reading
content rather than frames, the first wave of this court claimed EIGHTEEN lines
of Boole's «Analysis» and called eleven of them false: «$$ t_1t_2 = 0 … $$»
parses as arithmetic when the subscripts are read as digits. The prose was not
harmed — a shelf world is not written through the gates — but a court that
judges a neighbour's book is a court that has lost its subject. So a line is
claimed only if it carries a DECLARED MARKER of this house (a question head, a
primality wording, a refusal opener) or if it carries NO LETTERS AT ALL, being
a pure row of equalities. Boole's lines carry letters and no marker; the
house's own pure-equation cases carry no letters; nothing else changes.
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
ПРОСТО = ("— простое", "is prime", "ist eine primzahl", "est premier", "es primo",
          "è primo", "é primo", "is een priemgetal", "jest liczbą pierwszą")
НЕ_ПРОСТО = ("не просто", "is not prime", "ist keine primzahl", "n'est pas premier", "no es primo",
             "non è primo", "não é primo", "is geen priemgetal", "nie jest liczbą pierwszą")
# ПОДЛЕЖАЩЕЕ ПРОСТОТЫ ЕСТЬ ГОЛОЕ ЧИСЛО ПОСЛЕ ПОСЛЕДНЕГО РАЗДЕЛИТЕЛЯ, а не
# последнее число перед словом. «2^n − 1 is prime for every prime n» кончается
# цифрой 1, и суд, читавший последнее число, объявлял единицу непростой и
# всякое ОБЩЕЕ утверждение — ложью. Общее утверждение о переменной не
# проверяется вовсе: проверять в нём нечего, а молчать о непроверяемом суд
# обязан.
_ЧИСЛО_ПЕРЕД = re.compile(r"^\s*(\d+)\s*$")
_ВЫРАЖЕНИЕ = re.compile(r"[\d\s+\-−×÷*/^²!()]+")


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


# «/» И «*» — ЗНАКИ СОСЕДНИХ МИРОВ (деление столбиком «946 / 22 = 43», нотация «30 / 5 = 6»,
# металогика «104 = 20 * 5 + 4»): суд, читающий чистый ряд равенств, обязан считать их, а не
# рвать плечо на них — рваное плечо «22» против «43» звало ложью честную строку (05.09,
# пересборка под потолком закрыла ворота трёх миров).
_ВЛЕВО = re.compile(r"[\d\s+\-−×÷*/^²!()]+$")
_ВПРАВО = re.compile(r"^[\d\s+\-−×÷*/^²!()]+")
_ОБРЫВОК = re.compile(r"^[+\-−×÷*/^]")   # плечо, начатое двоичным знаком, оборвано буквой: «x + 32»


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
        # ПЛЕЧО, НАЧАТОЕ ЗНАКОМ, — ОБРЫВОК: пробег влево остановился на букве внутри
        # выражения («x^2 - 12 x + 32 = 0» давал плечо «+ 32» против «0»); равенство с
        # переменной пропускается целиком, а не судится по своему хвосту
        if _ОБРЫВОК.match(л.group().strip()):
            continue
        a, b = _вычислить(л.group()), _вычислить(п_.group())
        if a is not None and b is not None:
            вон.append((a, b))
    return вон


def _метки():
    """Объявленные метки дома: зачины вопроса, отказа, согласия и слова простоты."""
    вон = set(ПРОСТО) | set(НЕ_ПРОСТО)
    for с in F.СЛОВА.values():
        for ключ in ("вопрос", "нет", "да", "нет_голое"):
            рамка = с.get(ключ)
            if not рамка:
                continue
            for кусок in re.split(r"\{\w+\}", рамка):
                кусок = кусок.strip(" .:,?!«»").lower()
                # ВОСЕМЬ БУКВ — НЕ ВКУС, А ЗАМЕР: рамка, разрезанная по дырам,
                # даёт и распознавательные куски («does it follow that»), и
                # союзы («and», «it gives»). Союз «and» из отказа сделал
                # подсудной английскую прозу Буля; порог в восемь знаков режет
                # союзы и оставляет зачины.
                if len(кусок) >= 8:
                    вон.add(кусок)
    return tuple(sorted(вон, key=len, reverse=True))


# ИМЯ С ПОДЧЁРКОМ — НЕ СТИЛЬ, А ГРАНИЦА ВИДИМОСТИ: прибор ШИРОТЫ ВОПРОСА
# читает ОБЪЯВЛЕННЫЕ ИМЕНА судов и считает всякий ряд строк РОДАМИ. Метки
# суда родами не являются — это его внутренний признак подсудности, — и,
# названные заглавно, они подняли долг корпуса на тридцать девять родов
# без вопросной поверхности. Подчёрк говорит прибору: это не объявление.
_МЕТКИ = _метки()
# ЧИСТЫЙ РЯД РАВЕНСТВ — только цифры и знаки счёта. Отсутствия БУКВ мало:
# «$$ 1 = 0, $$» букв не имеет, но есть разметка чужой книги, и суд назвал её
# ложью — верно арифметически и неверно по предмету.
#
# ПРОВЕРКА НАБОРОМ ЗНАКОВ, А НЕ ОБРАЗЦОМ, И ЭТО НЕ ВКУС. Прибор ШИРОТЫ ВОПРОСА
# читает ОБЪЯВЛЕННЫЕ ОБРАЗЦЫ судов и считает каждый РОДОМ; образец «чистый
# ряд» подходит ко всякой арифметической строке корпуса, и, будучи объявлен,
# он один поднял долг на ТРИДЦАТЬ ДЕВЯТЬ родов без вопросной поверхности.
# Подчёрк в имени не помог: прибор читает не имена, а образцы. Набор знаков
# образцом не является — и делает ровно то же.
_ЗНАКИ_РЯДА = frozenset("0123456789 +-−×÷*/^²!().,=:;")   # «*» и «/» — знаки соседних миров (05.09)


def _наше(с):
    низ = с.lower()
    if any(м in низ for м in _МЕТКИ):
        return True
    return all(ч in _ЗНАКИ_РЯДА for ч in с)


def _судить(строка):
    с = строка.strip()
    if not с or not _наше(с):
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
                "9 — простое.",
                "946 / 22 = 44.",          # ASCII-деление считается, а не рвёт плечо
                "104 = 20 * 5 + 3.")       # ASCII-умножение — то же
    # ЧЕСТНЫЕ СТРОКИ СОСЕДНИХ МИРОВ — ИСТИНА, А НЕ ОБРЫВОК (05.09): деление столбиком, нотация,
    # уравнение с переменной, чьё плечо «+ 32» прежде судилось против «0»
    for честная in ("946 / 22 = 43.", "30 / 5 = 6.",
                    "every value satisfies x^2 - 12 x + 32 = 0 is false: at x = 9 it gives 81 - 108 + 32 = 5, and 5 is not 0."):
        if _судить(честная) != (True, True):
            print(f"  ЧЕСТНАЯ СТРОКА НАЗВАНА {_судить(честная)}: {честная[:100]}")
            print("ПОСПЕШНОСТЬ FAIL: честная строка соседнего мира не истина")
            return 1
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
