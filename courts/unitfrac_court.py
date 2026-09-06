#!/usr/bin/env python3
"""[UNIT FRACTION COURT] — the named fraction of a unit, over four different bases; CLOSED WORLD.

A show of the fraction world (tools/unitfrac.py) is a fraction WORD — «полчаса», «eine
Viertelstunde», «kwadrans», «anderhalf uur» — and the number of the smaller unit it names. The
court reads the word, and the word alone rebuilds the whole page: the number by the law (the base
divided by the denominator, the quarter tripled, the half added back), the counting form of the
smaller unit by the rule of the pack, and the ledger with the base of THAT unit. A page that
divides the kilogram by sixty, names the quarter with the word of the half, or adds the extra
minutes wrongly rebuilds into a different page and is a lie.

The census found zero lines carrying «полчаса» or «half an hour» in the whole свод before this
house, and the house of speed had to declare the hole out loud.
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "tools"))
import unitfrac as F  # noqa: E402
import closedworld  # noqa: E402
from closedworld import Слой  # noqa: E402 — the palata hands the world's name

ЗАМКНУТЫЕ_МИРЫ = frozenset({"unitfrac"})


def _судить(строка):
    return F.судить(строка)


судить = closedworld.замкнуть(_судить, ЗАМКНУТЫЕ_МИРЫ)


def main():
    import collections
    from genesis import worlds
    # ПРЕДСТАВЛЕННОЕ «НЕТ» (М-106): число дроби подменено; основа чужая; слово дроби чужое
    # (четверть названа половиной); ОСНОВА ЧАСА В ДОМЕ МЕТРА; обратное чтение лжёт именем;
    # сумма сложена неверно; знаменатель года взят от четверти; леджер расходится с ответом.
    подсадки = (
        "полчаса — это сколько минут? 20 минут: 60 ÷ 2 = 20.",
        "how many minutes is half an hour? 30 minutes: 50 ÷ 2 = 30.",
        "wie viele Minuten sind eine halbe Stunde? 15 Minuten: 60 ÷ 4 = 15.",
        "ile centymetrów to pół metra? 50 centymetrów: 60 ÷ 2 = 50.",
        "45 minutes is half an hour: 60 ÷ 4 × 3 = 45.",
        "mezz'ora e altri 10 minuti sono 50 minuti: 30 + 10 = 50.",
        "6 miesięcy to pół roku: 12 ÷ 4 = 6.",
        "combien de minutes fait trois quarts d'heure ? 45 minutes : 60 ÷ 4 × 3 = 40.",
    )
    пойманы = sum(1 for п in подсадки if _судить(п) == (True, False))
    if пойманы != len(подсадки):
        for п in подсадки:
            print(f"  ПОДСАДКА {_судить(п)}: {п[:150]}")
        print(f"ДРОБЬ ЕДИНИЦЫ FAIL: подсадок поймано {пойманы} из {len(подсадки)}")
        return 1
    итог = collections.Counter(); примеры = []
    пути = [п for п in worlds(kind="shows") if п.name == "genesis_unitfrac.txt"]
    if not пути:  # мир ещё не в манифесте — суд читает свой файл по имени
        свой = pathlib.Path(__file__).resolve().parents[1] / "datasets" / "genesis_unitfrac.txt"
        пути = [свой] if свой.exists() else []
        print("  мир не в манифесте — суд читает datasets/genesis_unitfrac.txt по имени")
    for путь in пути:
        for стр in путь.read_text(encoding="utf-8").splitlines():
            if not стр.strip() or стр.startswith("\x0c"):
                continue
            судимо, истинно = _судить(стр)
            итог["судимых" if судимо else "несудимых"] += 1
            if судимо and not истинно:
                итог["ложных"] += 1
                if len(примеры) < 5:
                    примеры.append(стр)
    for п in примеры:
        print(f"  ЛОЖЬ: {п[:150]}")
    поза = "PASS" if итог["ложных"] == 0 and итог["несудимых"] == 0 else "FAIL"
    print(f"ДРОБЬ ЕДИНИЦЫ {поза}: {итог['ложных']} ложных из {итог['судимых']} судимых, "
          f"несудимых {итог['несудимых']}; подсадок поймано {пойманы} из {len(подсадки)}")
    return 0 if поза == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
