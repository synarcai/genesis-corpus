#!/usr/bin/env python3
"""[SVAMP SHAPES COURT] — the story's numbers are the ledger's, and the ledger holds; RECHECKED.

A show of the SVAMP-shapes world (tools/svampforms.py) is one of the eight
shapes the live band showed mute: the hidden «some», the heads of the total,
the oblique pronoun, the hypothetical act, the time words, transfer with a
direction, the unit before the number, goods outside the lexicon — in English
and Russian, each with its ledger. The court reads each line through the same
frames: a page of the house is true; a line of its frame whose ledger does not
hold, or whose story numbers are not the ledger's, is a lie. The world is CLOSED.
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "tools"))
import svampforms as F  # noqa: E402
import closedworld  # noqa: E402
from closedworld import Слой  # noqa: E402 — the palata hands the world's name

ЗАМКНУТЫЕ_МИРЫ = frozenset({"svamp"})


def _судить(строка):
    return F.судить(строка)


судить = closedworld.замкнуть(_судить, ЗАМКНУТЫЕ_МИРЫ)


def main():
    import collections
    from genesis import worlds
    # ПРЕДСТАВЛЕННОЕ «НЕТ» (М-106): кузница не сходится; число истории не число кузницы; цена не произведение
    подсадки = (
        "Ann had 12 coins. she gave some of them away. now she has 7 coins left. how many coins did she give away? 5: 12 − 7 = 6.",
        "Ann had 12 coins. she gave 5 of them to Anna. how many coins does she have now? 7: 12 − 4 = 8.",
        "a coin costs $ 3. how much do 4 coins cost? $ 12: 4 × 3 = 13.",
        "у Вани было 12 шаров. он отдал 5 из них Вере. сколько шаров у него теперь? 7: 12 − 5 = 8.",
        # ДОЛИ И ЦЕПОЧКИ (05.09): делитель не есть знаменатель слова доли; заявленный ответ не есть итог
        # леджера; шаг цепочки не опирается на итог предыдущего
        "Ann has 12 coins. a third of them are red. how many coins are red? 4: 12 ÷ 4 = 3.",
        "Ann has 12 coins. she gives away 5. how many coins does Ann own now? Ann owns 6 coins: 12 − 5 = 7.",
        "Ann has 12 coins. half of them are red. how many coins are not red? step 1: 12 ÷ 2 = 6. step 2: 12 − 5 = 7. total: 7.",
    )
    пойманы = sum(1 for п in подсадки if _судить(п) == (True, False))
    if пойманы != len(подсадки):
        for п in подсадки:
            print(f"  ПОДСАДКА {_судить(п)}: {п[:110]}")
        print(f"ФОРМЫ SVAMP FAIL: подсадок поймано {пойманы} из {len(подсадки)}")
        return 1
    итог = collections.Counter(); примеры = []
    for путь in worlds(kind="shows"):
        if путь.name != "genesis_svamp.txt":
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
    print(f"ФОРМЫ SVAMP {поза}: {итог['ложных']} ложных из {итог['судимых']} судимых, "
          f"несудимых {итог['несудимых']}; подсадок поймано {пойманы} из {len(подсадки)}")
    return 0 if поза == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
