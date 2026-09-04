#!/usr/bin/env python3
"""[СОВМЕСТНЫЙ СЧЁТ COURT] — the sum, the difference AND the form of the thing.

Two oracles at once, and the second is the rarer one:

  · ARITHMETIC — the sum, the difference and the zero are recomputed;
  · THE COUNT FORM — the word standing after each number must be the form the
    nature house gives for THAT number («7 яблок», «4 яблока», «11 яблок»).

The second matters because this world speaks in the first and second person and
therefore repeats the same thing at three different counts in one line. A house
that guessed a form instead of asking `natureforms.вещь` would produce «7
яблока» — true by arithmetic and false by speech — and no arithmetic court
would ever see it.

The world is CLOSED.
"""
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "tools"))
import jointforms2 as F  # noqa: E402
import natureforms as N  # noqa: E402

import closedworld  # noqa: E402
from closedworld import Слой  # noqa: E402 — the palata hands the world's name

ЗАМКНУТЫЕ_МИРЫ = frozenset({"joint2"})
_ДЫРА = re.compile(r"\{(\w+)\}")


def _образцы():
    вон = []
    for язык in F.ЯЗЫКИ:
        формы_вещей = sorted({N.вещь(язык, в, n) for в in F.ВЕЩИ[язык]
                              for n in range(0, 41)}, key=len, reverse=True)
        альт = "(?:" + "|".join(re.escape(ф) for ф in формы_вещей) + ")"
        for форма in F.ФОРМЫ:
            # ВЕЖЛИВЫЙ РЕГИСТР — вторая рамка того же рода; язык без различия
            # её не держит, и образца ему не строится
            if форма.endswith("_вы"):
                if язык in F.БЕЗ_РАЗЛИЧИЯ_РЕГИСТРА:
                    continue
                рамка = F.ВЕЖЛИВЫЕ[язык][форма[:-3]]
            else:
                рамка = F.РАМКИ[язык][форма]
            дыры, куски, конец = [], [], 0
            for м in _ДЫРА.finditer(рамка):
                куски.append(re.escape(рамка[конец:м.start()]))
                имя = м.group(1)
                дыры.append(имя)
                куски.append(альт if имя.startswith("в") else r"(\d+)")
                конец = м.end()
            куски.append(re.escape(рамка[конец:]))
            вон.append((язык, форма, tuple(дыры), re.compile("^" + "".join(куски) + "$")))
    return tuple(вон)


ОБРАЗЦЫ = _образцы()


def _верно(язык, форма, п):
    if форма.endswith("_вы"):
        форма = форма[:-3]
    a = п["a"]
    # ФОРМА ВЕЩИ ПРИ КАЖДОМ ЧИСЛЕ — вторая половина суда
    вещи = F.ВЕЩИ[язык]
    def годна(слово, n):
        return any(N.вещь(язык, в, n) == слово for в in вещи)
    if форма == "поровну":
        return годна(п["ва"], a)
    b = п["b"]
    if not (годна(п["ва"], a) and годна(п["вб"], b)):
        return False
    if форма == "вместе":
        c = п["c"]
        return c == a + b and годна(п["вс"], c)
    return п["d"] == a - b


def _судить(строка):
    с = строка.strip()
    if not с:
        return False, False
    for язык, форма, дыры, образец in ОБРАЗЦЫ:
        м = образец.match(с)
        if not м:
            continue
        поля, свои = {}, list(м.groups())
        # дыры вещей в образце не захвачены группами — читаем их из рамки
        числа = [з for з in свои]
        for имя, значение in zip([д for д in дыры if not д.startswith("в")], числа):
            значение = int(значение)
            if поля.setdefault(имя, значение) != значение:
                return True, False
        # слова вещей вынимаются повторным разбором той же рамки
        рамка = (F.ВЕЖЛИВЫЕ[язык][форма[:-3]] if форма.endswith("_вы")
                 else F.РАМКИ[язык][форма])
        части = re.split(r"\{\w+\}", рамка)
        имена = [м2.group(1) for м2 in _ДЫРА.finditer(рамка)]
        место, ок = 0, True
        for кусок, имя in zip(части, имена):
            место = с.find(кусок, место) + len(кусок)
            конец = место
            while конец < len(с) and с[конец] not in " ,.:;?!":
                конец += 1
            хвост = с[место:конец]
            if имя.startswith("в"):
                # слово вещи может нести пробел («ein Fahrrad» не наш случай, но
                # немецкие формы бывают из одного слова) — берём до разделителя
                поля.setdefault(имя, хвост)
            место = конец
        if not ок:
            return True, False
        return True, _верно(язык, форма, поля)
    return False, False


судить = closedworld.замкнуть(_судить, ЗАМКНУТЫЕ_МИРЫ)


def main():
    import collections
    from genesis import worlds
    я = F.РАМКИ["ru"]
    a, b = F.ПАРЫ[0]
    в = F.ВЕЩИ["ru"][0]
    подсадки = (я["вместе"].format(a=a, b=b, c=a + b + 1, ва=N.вещь("ru", в, a),
                                   вб=N.вещь("ru", в, b), вс=N.вещь("ru", в, a + b + 1)),
                я["разница"].format(a=a, b=b, d=a - b + 1, ва=N.вещь("ru", в, a), вб=N.вещь("ru", в, b)),
                я["вместе"].format(a=a, b=b, c=a + b, ва=N.вещь("ru", в, b),
                                   вб=N.вещь("ru", в, b), вс=N.вещь("ru", в, a + b)))
    пойманы = sum(1 for п in подсадки if _судить(п) == (True, False))
    if пойманы != len(подсадки):
        for п in подсадки:
            print(f"  ПОДСАДКА {_судить(п)}: {п[:110]}")
        print(f"СОВМЕСТНЫЙ СЧЁТ FAIL: подсадок поймано {пойманы} из {len(подсадки)}")
        return 1
    итог = collections.Counter(); примеры = []
    for путь in worlds(kind="shows"):
        if путь.name != "genesis_joint2.txt":
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
    print(f"СОВМЕСТНЫЙ СЧЁТ {поза}: {итог['ложных']} ложных из {итог['судимых']} судимых, "
          f"несудимых {итог['несудимых']}; подсадок поймано {пойманы} из {len(подсадки)}")
    return 0 if поза == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
