#!/usr/bin/env python3
"""[ПЕРЕПИСЬ COURT] — both writings are RECOMPUTED and compared.

The fourth world judged by computation. Each frame becomes a pattern whose
holes are ARITHMETIC WRITINGS («5 + 5», «2 × 5») and numbers; on a match every
writing is evaluated and the claim is recomputed:

  воп  «how else can {a} be written? {b}: both are {v}»  —  a = b = v
  нет  «are {a} and {c} the same? no: {a} = {v}, {c} = {w}»  —  a = v, c = w, v ≠ w

The last condition is the one that matters: a refusal naming EQUAL values would
deny a true rewriting while showing the correct test — the same shape of lie the
likeness court guards against. The world is CLOSED.
"""
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "tools"))
import rewriteforms as F  # noqa: E402

import closedworld  # noqa: E402
from closedworld import Слой  # noqa: E402 — the palata hands the world's name

ЗАМКНУТЫЕ_МИРЫ = frozenset({"rewrite"})
_ДЫРА = re.compile(r"\{(\w+)\}")
_ЗАПИСЬ = r"([\d]+(?:\s*[+\-−×÷]\s*[\d]+)*)"


def _образцы():
    вон = []
    for язык in F.ЯЗЫКИ:
        for форма in F.ФОРМЫ:
            рамка = F.РАМКИ[язык][форма]
            дыры, куски, конец = [], [], 0
            for м in _ДЫРА.finditer(рамка):
                куски.append(re.escape(рамка[конец:м.start()]))
                имя = м.group(1)
                дыры.append(имя)
                if имя in ("a", "b", "c"):
                    куски.append(_ЗАПИСЬ)
                elif имя == "з":
                    # ЗАКОН СВЯЗАН ОБЪЯВЛЕННЫМ РЯДОМ: перепись, названная чужим
                    # законом, подсудна и ложна, а не молчалива
                    куски.append("(" + "|".join(re.escape(з) for з in
                                                sorted(F.ЗАКОНЫ[язык].values(), key=len, reverse=True)) + ")")
                else:
                    куски.append(r"(\d+)")
                конец = м.end()
            куски.append(re.escape(рамка[конец:]))
            вон.append((язык, форма, tuple(дыры), re.compile("^" + "".join(куски) + "$")))
    return tuple(вон)


ОБРАЗЦЫ = _образцы()


def _верно(форма, поля):
    try:
        a = F.значение(поля["a"])
        if форма == "воп":
            # закон обязан быть ТЕМ, что объявлен для этой тройки
            for _a, _b, _c, имя in F.ТРОЙКИ:
                if _a == поля["a"] and _b == поля["b"]:
                    if поля.get("з") != F.ЗАКОНЫ[поля["язык"]][имя]:
                        return False
                    break
            return a == F.значение(поля["b"]) == поля["v"]
        c = F.значение(поля["c"])
        return a == поля["v"] and c == поля["w"] and поля["v"] != поля["w"]
    except (SyntaxError, ZeroDivisionError, TypeError, ValueError, KeyError):
        return False


def _судить(строка):
    с = строка.strip()
    if not с:
        return False, False
    for язык, форма, дыры, образец in ОБРАЗЦЫ:
        м = образец.match(с)
        if not м:
            continue
        поля, сходится = {"язык": язык}, True
        for имя, кусок in zip(дыры, м.groups()):
            значение = int(кусок) if имя in ("v", "w") else кусок
            if имя in поля and поля[имя] != значение:
                сходится = False
                break
            поля[имя] = значение
        if not сходится:
            return True, False
        return True, _верно(форма, поля)
    return False, False


судить = closedworld.замкнуть(_судить, ЗАМКНУТЫЕ_МИРЫ)


def main():
    import collections
    from genesis import worlds
    # ПРЕДСТАВЛЕННОЕ «НЕТ» (М-106): чужая вторая запись, подменённое значение,
    # и отказ, называющий РАВНЫЕ значения (он отверг бы верную перепись).
    подсадки = ("чем ещё можно записать 5 + 5? 3 × 5: сложить число с собой значит взять его дважды, и то и другое есть 10.",
                "чем ещё можно записать 5 + 5? 2 × 5: сложить число с собой значит взять его дважды, и то и другое есть 11.",
                "5 + 5 и 2 × 5 — одно и то же? нет: 5 + 5 = 10, а 2 × 5 = 10.",
                # ЧУЖОЙ ЗАКОН при верной переписи: удвоение названо перестановкой
                "чем ещё можно записать 5 + 5? 2 × 5: порядок множителей не меняет "
                "произведения, и то и другое есть 10.")
    пойманы = sum(1 for п in подсадки if _судить(п) == (True, False))
    if пойманы != len(подсадки):
        for п in подсадки:
            print(f"  ПОДСАДКА {_судить(п)}: {п[:100]}")
        print(f"ПЕРЕПИСЬ FAIL: подсадок поймано {пойманы} из {len(подсадки)}")
        return 1
    итог = collections.Counter(); примеры = []
    for путь in worlds(kind="shows"):
        if путь.name != "genesis_rewrite.txt":
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
    print(f"ПЕРЕПИСЬ {поза}: {итог['ложных']} ложных из {итог['судимых']} судимых, "
          f"несудимых {итог['несудимых']}; подсадок поймано {пойманы} из {len(подсадки)}")
    return 0 if поза == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
