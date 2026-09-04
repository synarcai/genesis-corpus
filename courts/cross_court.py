#!/usr/bin/env python3
"""[ПЕРЕКРЁСТОК COURT] — the word and the sign must name THE SAME operation.

Two things are recomputed on every line:

  · the value: «17 + 25 = 42» is counted;
  · the AGREEMENT OF THE TWO NOTATIONS: the word standing in the question and
    the sign standing in the answer must be the same operation of the same
    language.

The second is the whole reason the world exists. A line whose question says
«plus» and whose answer counts «×» would be true by arithmetic and false as a
bridge between two notations — and the bridge is what this world teaches.

The world is CLOSED.
"""
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "tools"))
import crossforms as F  # noqa: E402

import closedworld  # noqa: E402
from closedworld import Слой  # noqa: E402 — the palata hands the world's name

ЗАМКНУТЫЕ_МИРЫ = frozenset({"cross"})


def _образцы():
    """ОДИН ОБРАЗЕЦ НА ЯЗЫК, где СЛОВО и ЗНАК захвачены порознь.

    Первая проба ставила по образцу на действие, связывая слово со знаком
    жёстко, — и строка «17 плюс 25? 17 × 25 = 425» не подходила НИ К ОДНОМУ:
    к «плюс» из-за знака, к «умножить» из-за слова. Подсадка не ловилась, и
    мир, чей смысл в СОГЛАСИИ двух записей, молчал ровно там, где они
    расходятся. Слово и знак читаются отдельно, согласие проверяется потом.
    """
    вон = []
    for язык, с in F.СЛОВА.items():
        пр = с.get("пробел_перед_знаком", "")
        головы = "(?:" + "|".join(re.escape(г) for г in с["головы"]) + ")"
        слова = "|".join(re.escape(с[и]) for _, и, _ in
                         sorted(F.ДЕЙСТВИЯ, key=lambda д: len(с[д[1]]), reverse=True))
        знаки = "|".join(re.escape(з) for з, _, _ in F.ДЕЙСТВИЯ)
        вон.append((язык, "слово", re.compile(
            "^" + головы + r" (\d+) (" + слова + r") (\d+)" + re.escape(пр) +
            r"\? (\d+) (" + знаки + r") (\d+) = (\d+)\.$")))
        # ИМЯ ДЕЙСТВИЯ — третья запись той же оси; вопрос объявлен целиком, и
        # потому образец строится из него, а не из головы со словом
        for знак, имя, _ in F.ДЕЙСТВИЯ:
            вопрос = F.ИМЕНА[язык][имя]
            голова, _, хвост = вопрос.partition("{a}")
            середина, _, конец = хвост.partition("{b}")
            вон.append((язык, "имя:" + знак, re.compile(
                "^" + re.escape(голова) + r"(\d+)" + re.escape(середина) + r"(\d+)" +
                re.escape(конец) + r" (\d+) (" + знаки + r") (\d+) = (\d+)\.$")))
    return tuple(вон)


ОБРАЗЦЫ = _образцы()


def _судить(строка):
    с = строка.strip()
    if not с:
        return False, False
    for язык, вид, образец in ОБРАЗЦЫ:
        м = образец.match(с)
        if not м:
            continue
        if вид.startswith("имя:"):
            a, b, a2, знак, b2, v = (int(г) if г.isdigit() else г for г in м.groups())
            if (a, b) != (a2, b2):
                return True, False
            if знак != вид[4:]:
                return True, False      # имя действия и знак называют РАЗНОЕ
            if знак == "÷" and (b == 0 or a % b):
                return True, False
            return True, v == F.значение(знак, a, b)
        a, слово, b, a2, знак, b2, v = м.groups()
        a, b, a2, b2, v = int(a), int(b), int(a2), int(b2), int(v)
        if (a, b) != (a2, b2):
            return True, False      # вопрос и ответ о разных числах
        по_слову = {F.СЛОВА[язык][и]: з for з, и, _ in F.ДЕЙСТВИЯ}
        if по_слову.get(слово) != знак:
            return True, False      # слово и знак называют РАЗНЫЕ действия
        if знак == "÷" and (b == 0 or a % b):
            return True, False
        return True, v == F.значение(знак, a, b)
    return False, False


судить = closedworld.замкнуть(_судить, ЗАМКНУТЫЕ_МИРЫ)


def main():
    import collections
    from genesis import worlds
    с = F.СЛОВА["ru"]
    # ПРЕДСТАВЛЕННОЕ «НЕТ» (М-106): неверное значение; слово и знак о РАЗНЫХ
    # действиях; числа вопроса и ответа разные.
    подсадки = (f"{с['головы'][0]} 17 {с['плюс']} 25? 17 + 25 = 43.",
                f"{с['головы'][0]} 17 {с['плюс']} 25? 17 × 25 = 425.",
                f"{с['головы'][0]} 17 {с['плюс']} 25? 18 + 25 = 43.",
                # ИМЯ ДЕЙСТВИЯ ПРОТИВ ЗНАКА: сумма, посчитанная умножением
                F.ИМЕНА["ru"]["плюс"].format(a=17, b=25) + " 17 × 25 = 425.")
    пойманы = sum(1 for п in подсадки if _судить(п) == (True, False))
    if пойманы != len(подсадки):
        for п in подсадки:
            print(f"  ПОДСАДКА {_судить(п)}: {п[:110]}")
        print(f"ПЕРЕКРЁСТОК FAIL: подсадок поймано {пойманы} из {len(подсадки)}")
        return 1
    итог = collections.Counter(); примеры = []
    for путь in worlds(kind="shows"):
        if путь.name != "genesis_cross.txt":
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
    print(f"ПЕРЕКРЁСТОК {поза}: {итог['ложных']} ложных из {итог['судимых']} судимых, "
          f"несудимых {итог['несудимых']}; подсадок поймано {пойманы} из {len(подсадки)}")
    return 0 if поза == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
