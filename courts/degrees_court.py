#!/usr/bin/env python3
"""[DEGREES COURT] — the three degrees of one property, and the irregular said aloud; CLOSED WORLD.

A show of the degrees world (tools/degrees.py) is one property in three frames: the row of its
three degrees, the transitive chain of three men ending in the superlative, and the converse
through the ANTONYM. The court reads the words back to their property: a row that mixes two
properties, a superlative borrowed from another, an irregularity declared where the language has
none (or hidden where it has one), a chain answering with the middle man, a converse said with
the same word instead of the opposite — each is a lie about the language, and each is judged.

The census found twenty-nine lines carrying a comparative adjective in the whole свод before this
house.
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "tools"))
import degrees as F  # noqa: E402
import closedworld  # noqa: E402
from closedworld import Слой  # noqa: E402 — the palata hands the world's name

ЗАМКНУТЫЕ_МИРЫ = frozenset({"degrees"})


def _судить(строка):
    return F.судить(строка)


судить = closedworld.замкнуть(_судить, ЗАМКНУТЫЕ_МИРЫ)


def main():
    import collections
    from genesis import worlds
    # ПРЕДСТАВЛЕННОЕ «НЕТ» (М-106): ряд смешал два признака; превосходная чужая; НЕПРАВИЛЬНОСТЬ
    # ОБЪЯВЛЕНА ТАМ, ГДЕ ЕЁ НЕТ; неправильность СКРЫТА там, где она есть; цепь отвечает средним
    # именем; вопрос цепи о чужом признаке; обратное не обращено; обращение чужим словом.
    подсадки = (
        "высокий, ниже, самый высокий — три степени одного признака.",
        "tall, taller, the shortest — three degrees of one property.",
        "schnell, schneller, am schnellsten — drei Stufen einer Eigenschaft, und die zweite folgt nicht aus der ersten.",
        "good, better, the best — three degrees of one property.",
        "Ваня выше, чем Дима. Дима выше, чем Иван. кто самый высокий? Дима: Ваня выше, чем Дима, а Дима выше, чем Иван.",
        "Jonas ist schneller als Paul. Paul ist schneller als Felix. wer ist am größten? Jonas: Jonas ist schneller als Paul, und Paul ist schneller als Felix.",
        "Jan jest wyższy niż Piotr. więc Piotr jest wyższy niż Jan.",
        "Ваня быстрее, чем Дима. значит, Дима ниже, чем Ваня.",
    )
    пойманы = sum(1 for п in подсадки if _судить(п) == (True, False))
    if пойманы != len(подсадки):
        for п in подсадки:
            print(f"  ПОДСАДКА {_судить(п)}: {п[:150]}")
        print(f"СТЕПЕНИ FAIL: подсадок поймано {пойманы} из {len(подсадки)}")
        return 1
    итог = collections.Counter(); примеры = []
    пути = [п for п in worlds(kind="shows") if п.name == "genesis_degrees.txt"]
    if not пути:  # мир ещё не в манифесте — суд читает свой файл по имени
        свой = pathlib.Path(__file__).resolve().parents[1] / "datasets" / "genesis_degrees.txt"
        пути = [свой] if свой.exists() else []
        print("  мир не в манифесте — суд читает datasets/genesis_degrees.txt по имени")
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
    print(f"СТЕПЕНИ {поза}: {итог['ложных']} ложных из {итог['судимых']} судимых, "
          f"несудимых {итог['несудимых']}; подсадок поймано {пойманы} из {len(подсадки)}")
    return 0 if поза == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
