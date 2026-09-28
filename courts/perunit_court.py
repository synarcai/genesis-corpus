#!/usr/bin/env python3
"""[СТАВКА НА ЕДИНИЦУ] — итог есть ставка, умноженная на число единиц; всякая форма счёта — пакета.

Страница мира `perunit` (tools/perunitforms.py) спрашивает одно отношение с трёх концов на одной
тройке чисел: итог («each box has 6 apples. how many apples are in 4 boxes? 24 apples: 4 × 6 =
24.»), число единиц («… how many boxes are there? 4 boxes: 24 ÷ 6 = 4.») и саму ставку («… how
many apples are in each box? 6 apples: 24 ÷ 4 = 6.») — в четырёх формах ставки (слово ставки
впереди числа, позади него, «per box» и цена «at 3 dollars each») на десяти языках. Суд читает
страницу тем же домом и пересчитывает: итог обязан быть произведением ставки на число единиц,
всякое повторённое число — тем же числом, форма счёта вещи, вместилища и валюты — той, какую
правило пакета выбирает при своём числе, польский и украинский глагол при числе — в ячейке своего
числа («są 3 jabłka», «jest 6 jabłek»). МИР ЗАМКНУТ.
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "tools"))
import perunitforms as F  # noqa: E402
import closedworld  # noqa: E402
from closedworld import Слой  # noqa: E402 — палата подаёт имя мира лишь тому, кто ввёз Слой

ЗАМКНУТЫЕ_МИРЫ = frozenset({"perunit"})


def _судить(строка):
    return F.судить(строка)


судить = closedworld.замкнуть(_судить, ЗАМКНУТЫЕ_МИРЫ)


def main():
    import collections
    from genesis import worlds
    # ПРЕДСТАВЛЕННОЕ «НЕТ» (М-106): итог не произведение; знак действия не тот; форма счёта
    # итога не по числу; вместилище при числе не по числу; польская связка не по числу ставки;
    # делится не итог
    подсадки = (
        "each box has 6 apples. how many apples are in 4 boxes? 25 apples: 4 × 6 = 25.",
        "each box has 6 apples. how many apples are in 4 boxes? 24 apples: 4 ÷ 6 = 24.",
        "в каждой коробке 6 яблок. сколько яблок в 4 коробках? 24 яблок: 4 × 6 = 24.",
        "24 яблока разложили по коробкам, в каждой коробке 6 яблок. сколько получилось коробок? 4 коробок: 24 ÷ 6 = 4.",
        "w każdej skrzynce jest 3 jabłka. ile jabłek jest w 8 skrzynkach? 24 jabłka: 8 × 3 = 24.",
        "24 apples are packed equally into 4 boxes. how many apples are in each box? 4 apples: 24 ÷ 6 = 4.",
        "на коробку припадає 3 яблука. скільки яблук у 5 коробках? 15 яблук: 5 × 3 = 15.",
        "4 books are sold at 7 dollars each. how much do they cost in all? 28 dollar: 4 × 7 = 28.",
        "5 jabłek kosztują razem 15 złotych. ile kosztuje każde jabłko? 3 złote: 15 ÷ 5 = 3.",
    )
    пойманы = sum(1 for п in подсадки if _судить(п) == (True, False))
    if пойманы != len(подсадки):
        for п in подсадки:
            print(f"  ПОДСАДКА {_судить(п)}: {п[:110]}")
        print(f"СТАВКА НА ЕДИНИЦУ FAIL: подсадок поймано {пойманы} из {len(подсадки)}")
        return 1
    итог = collections.Counter()
    примеры = []
    for путь in worlds(kind="shows"):
        if путь.name != "genesis_perunit.txt":
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
    поза = "PASS" if итог["ложных"] == 0 and итог["несудимых"] == 0 and итог["судимых"] else "FAIL"
    print(f"СТАВКА НА ЕДИНИЦУ {поза}: {итог['ложных']} ложных из {итог['судимых']} судимых, "
          f"несудимых {итог['несудимых']}; подсадок поймано {пойманы} из {len(подсадки)}")
    return 0 if поза == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
