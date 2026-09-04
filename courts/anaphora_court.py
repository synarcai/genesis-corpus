#!/usr/bin/env python3
"""[АНАФОРА COURT] — the remainder, the count forms AND the gender of the frame.

Three oracles on one line:

  · the subtraction is recomputed;
  · each of the three count forms must be the form the nature house gives for
    ITS number («7 шаров», «2 шара», «5 шаров»);
  · the frame's gender must match the NAME: a feminine name may not stand in a
    masculine frame. Where a language drops the subject the two frames coincide
    word for word, and then the check is silent — silence there is not a hole
    but the shape of that language.

The third is what the world is for. A corpus that put «ella dio» into Spanish
would teach unidiomatic speech, and one that put nothing would teach no
reference at all; the house declares WHICH languages carry the second mention
in the verb, and the court holds it to that declaration.

The world is CLOSED.
"""
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "tools"))
import anaphoraforms as F  # noqa: E402
import natureforms as N  # noqa: E402

import closedworld  # noqa: E402
from closedworld import Слой  # noqa: E402 — the palata hands the world's name

ЗАМКНУТЫЕ_МИРЫ = frozenset({"anaphora"})
_ДЫРА = re.compile(r"\{(\w+)\}")


def _образцы():
    вон = []
    for язык in F.ЯЗЫКИ:
        формы = sorted({N.вещь(язык, в, n) for в in F.ВЕЩИ[язык] for n in range(0, 41)},
                       key=len, reverse=True)
        альт = "(?:" + "|".join(re.escape(ф) for ф in формы) + ")"
        # ИМЯ СВЯЗАНО ОБОИМИ РЯДАМИ, А ПРОВЕРЯЕТСЯ ПО РАМКЕ. Первая проба
        # связывала дыру имени рядом СВОЕГО рода, и строка «у Анны … он отдал»
        # не подходила ни к женскому образцу (рамка мужская), ни к мужскому
        # (имя женское) — то есть мир, чей смысл в СОГЛАСИИ имени с рамкой,
        # молчал ровно там, где они расходятся. Имя ловится любое, согласие
        # проверяется после.
        все_имена = F.ИМЕНА[язык][0] + F.ИМЕНА[язык][1]
        if язык == "ru":
            все_имена = tuple(F.ИМЕНА_РОДИТЕЛЬНЫЙ[и] for и in все_имена)
        имя_альт = "(" + "|".join(re.escape(и) for и in
                                  sorted(все_имена, key=len, reverse=True)) + ")"
        for k, форма in enumerate(F.ФОРМЫ):
            свои = F.ИМЕНА[язык][k]
            if язык == "ru":
                свои = tuple(F.ИМЕНА_РОДИТЕЛЬНЫЙ[и] for и in свои)
            рамка = F.РАМКИ[язык][форма]
            куски, конец = [], 0
            for м in _ДЫРА.finditer(рамка):
                куски.append(re.escape(рамка[конец:м.start()]))
                имя = м.group(1)
                куски.append(имя_альт if имя == "и" else (альт if имя.startswith("в") else r"(\d+)"))
                конец = м.end()
            куски.append(re.escape(рамка[конец:]))
            # РАМКА, НЕ РАЗЛИЧАЮЩАЯ РОДА, НЕ ВПРАВЕ ЕГО И ТРЕБОВАТЬ. Там, где
            # язык опускает подлежащее, женская и мужская рамки совпадают слово
            # в слово, и род в строке не выражен ничем — значит проверять его
            # не по чему, и суд принимает оба ряда имён. Молчание тут не дыра, а
            # ФОРМА ЯЗЫКА, и требовать от неё различия значило бы судить
            # испанский по русской мерке.
            различает = F.РАМКИ[язык]["ж"] != F.РАМКИ[язык]["м"]
            годные = frozenset(свои) if различает else frozenset(все_имена)
            вон.append((язык, форма, годные, re.compile("^" + "".join(куски) + "$")))
    return tuple(вон)


ОБРАЗЦЫ = _образцы()


def _судить(строка):
    с = строка.strip()
    if not с:
        return False, False
    for язык, форма, свои_имена, образец in ОБРАЗЦЫ:
        м = образец.match(с)
        if not м:
            continue
        группы = list(м.groups())
        имя = группы[0]
        if имя not in свои_имена:
            return True, False      # имя одного рода в рамке другого
        числа = [int(г) for г in группы[1:]]
        # рамка несёт a, b, c и затем a − b = c: пять чисел, три различных
        if len(числа) < 5:
            return True, False
        a, b, c = числа[0], числа[1], числа[2]
        if (числа[3], числа[4], числа[5] if len(числа) > 5 else c) != (a, b, c):
            return True, False
        if c != a - b or c < 2:
            return True, False
        # ФОРМЫ ВЕЩЕЙ: каждая при своём числе
        вещи = F.ВЕЩИ[язык]
        for кусок, n in zip(_слова_вещей(с, язык, форма), (a, b, c)):
            if кусок is not None and not any(N.вещь(язык, в, n) == кусок for в in вещи):
                return True, False
        return True, True
    return False, False


def _слова_вещей(с, язык, форма):
    """Слова вещей в порядке дыр рамки — вынимаются повторным разбором."""
    рамка = F.РАМКИ[язык][форма]
    имена = [м.group(1) for м in _ДЫРА.finditer(рамка)]
    части = re.split(r"\{\w+\}", рамка)
    место, вон = 0, []
    for кусок, имя in zip(части, имена):
        найдено = с.find(кусок, место)
        if найдено < 0:
            return вон
        место = найдено + len(кусок)
        конец = место
        while конец < len(с) and с[конец] not in " ,.:;?!":
            конец += 1
        if имя.startswith("в"):
            вон.append(с[место:конец])
        место = конец
    return вон


судить = closedworld.замкнуть(_судить, ЗАМКНУТЫЕ_МИРЫ)


def main():
    import collections
    from genesis import worlds
    a, b = F.ПАРЫ[0]
    в = F.ВЕЩИ["ru"][0]
    и = F.ИМЕНА_РОДИТЕЛЬНЫЙ[F.ИМЕНА["ru"][0][0]]
    я = F.РАМКИ["ru"]
    подсадки = (я["ж"].format(и=и, a=a, b=b, c=a - b + 1, ва=N.вещь("ru", в, a),
                              вб=N.вещь("ru", в, b), вс=N.вещь("ru", в, a - b + 1)),
                я["ж"].format(и=и, a=a, b=b, c=a - b, ва=N.вещь("ru", в, b),
                              вб=N.вещь("ru", в, b), вс=N.вещь("ru", в, a - b)),
                я["м"].format(и=и, a=a, b=b, c=a - b, ва=N.вещь("ru", в, a),
                              вб=N.вещь("ru", в, b), вс=N.вещь("ru", в, a - b)))
    пойманы = sum(1 for п in подсадки if _судить(п) == (True, False))
    if пойманы != len(подсадки):
        for п in подсадки:
            print(f"  ПОДСАДКА {_судить(п)}: {п[:110]}")
        print(f"АНАФОРА FAIL: подсадок поймано {пойманы} из {len(подсадки)}")
        return 1
    итог = collections.Counter(); примеры = []
    for путь in worlds(kind="shows"):
        if путь.name != "genesis_anaphora.txt":
            continue
        for стр in путь.read_text(encoding="utf-8").splitlines():
            if not стр.strip() or стр.startswith("\x0c"):
                continue
            судимо, истинно = судить(стр)
            итог["судимых" if судимо else "несудимых"] += 1
            if судимо and not истинно:
                итог["ложных"] += 1
                if len(примеры) < 5:
                    примеры.append(стр)
    for п in примеры:
        print(f"  ЛОЖЬ: {п[:120]}")
    поза = "PASS" if итог["ложных"] == 0 and итог["несудимых"] == 0 else "FAIL"
    print(f"АНАФОРА {поза}: {итог['ложных']} ложных из {итог['судимых']} судимых, "
          f"несудимых {итог['несудимых']}; подсадок поймано {пойманы} из {len(подсадки)}")
    return 0 if поза == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
