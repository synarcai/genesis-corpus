#!/usr/bin/env python3
"""[BEFORE-TAIL COURT] — the act runs backwards, or the page lies; CLOSED WORLD.

A show of the before-tail world (tools/beforetails.py) is one story asked BACKWARDS: an act
(gave away, bought, spent), the state after it, and a question that ends with a tail pointing
before the act — «to begin with», «in the beginning», «initially», «at the start», «before
that» — five tails per language, because the market must buy the WORDS and not one phrase.

The court reads each line back through the house's frames. A page is true when the act is
INVERTED by the sign of its kind (what was given away is added back, what was bought is taken
away, what was spent is added back to what is left), when the answer is the initial state and
not the state after the act (a reader that hears the tail as noise answers the latter, and
that is the first intrusion here), when each count form is the form of ITS number, and when
the money on the page carries its sign and its three numbers agree. A line of a frame that
breaks any of these is a lie; a line of no frame is a lie of the closed world.
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "tools"))
import beforetails as F  # noqa: E402
import closedworld  # noqa: E402
from closedworld import Слой  # noqa: E402 — the palata hands the world's name

ЗАМКНУТЫЕ_МИРЫ = frozenset({"beforetails"})


def _судить(строка):
    return F.судить(строка)


судить = closedworld.замкнуть(_судить, ЗАМКНУТЫЕ_МИРЫ)


def main():
    import collections
    from genesis import worlds
    # ПРЕДСТАВЛЕННОЕ «НЕТ» (М-106): хвост прочитан как шум (ответ равен оставшемуся); акт
    # повторён вместо обращения; деньги не восстановлены; счётная форма чужого числа.
    подсадки = (
        "i gave away 3 apples. i have 7 apples left. how many apples did i have to begin with? 7 apples: 7 + 3 = 7.",
        "i bought 4 books. now i have 11 books. how many books did i have initially? 15 books: 11 − 4 = 15.",
        "i spent $25. i have $76 left. how much money did i have at the start? $100: 76 + 25 = 100.",
        "я отдал 3 яблока. у меня осталось 7 яблок. сколько яблок у меня было сначала? 7 яблок: 7 + 3 = 7.",
        "я купил 4 книги. теперь у меня 11 книг. сколько книг у меня было изначально? 15 книг: 11 − 4 = 15.",
        "oddałem 3 jabłka. zostało mi 7 jabłek. ile jabłek miałem na początku? 10 jabłka: 7 + 3 = 10.",
        "ich habe 3 Äpfel weggegeben. mir sind 7 Äpfel geblieben. wie viele Äpfel hatte ich zu Beginn? 10 Äpfel: 7 + 3 = 11.",
        "j'ai donné 3 pommes. il me reste 7 pommes. combien de pommes avais-je au début ? 7 pommes : 7 + 3 = 7.",
    )
    пойманы = sum(1 for п in подсадки if _судить(п) == (True, False))
    if пойманы != len(подсадки):
        for п in подсадки:
            print(f"  ПОДСАДКА {_судить(п)}: {п[:150]}")
        print(f"ХВОСТ FAIL: подсадок поймано {пойманы} из {len(подсадки)}")
        return 1
    итог = collections.Counter(); примеры = []
    пути = [п for п in worlds(kind="shows") if п.name == "genesis_beforetails.txt"]
    if not пути:  # мир ещё не в манифесте — суд читает свой файл по имени
        свой = pathlib.Path(__file__).resolve().parents[1] / "datasets" / "genesis_beforetails.txt"
        пути = [свой] if свой.exists() else []
        print("  мир не в манифесте — суд читает datasets/genesis_beforetails.txt по имени")
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
    print(f"ХВОСТ {поза}: {итог['ложных']} ложных из {итог['судимых']} судимых, "
          f"несудимых {итог['несудимых']}; подсадок поймано {пойманы} из {len(подсадки)}")
    return 0 if поза == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
