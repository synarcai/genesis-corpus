#!/usr/bin/env python3
"""[ОТКЛИК COURT] — the LAW inside the reply is checked against the NEIGHBOUR.

The house of replies never writes a behavioural law of its own: it quotes the
law of `tools/behaviorforms.py` verbatim. The court therefore does not trust
the house's own list — it splits the line at the declared colon and compares
the tail with `behaviorforms.страница(язык, "закон", род)` word for word.

That is the whole point of the world: an advice whose ground is a law of a
DIFFERENT genus («i am tired. what should i do? take a rest: when a person is
hungry, that person looks for food.») is true in both halves and false as a
whole — the same shape as М-263, and the only guard against it is reading the
two halves TOGETHER against the neighbour's declaration.

The world is CLOSED.
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "tools"))
import replyforms as F  # noqa: E402
import behaviorforms as B  # noqa: E402

import closedworld  # noqa: E402
from closedworld import Слой  # noqa: E402 — the palata hands the world's name

ЗАМКНУТЫЕ_МИРЫ = frozenset({"reply"})

# {(язык, состояние): [хвост, …]} — объявление, читаемое судом.
#
# ДВЕ ПОВЕРХНОСТИ ОДНОГО ДЕЛА, И СУД ЧИТАЕТ ОБЕ (16.09). Дом развёл совет и его основание
# второй поверхностью — «я устал. отдохни. почему? когда человек устал, он ошибается чаще» —
# и суд, знавший одну, назвал бы ложью 54 честные страницы, а ворота не записали бы мир.
#
#     СУД СОБИРАЕТ ХВОСТ ТЕМ ЖЕ ОБЪЯВЛЕНИЕМ, ЧТО И ДОМ, И ПОТОМУ ВТОРАЯ ПОВЕРХНОСТЬ НЕ
#     ТРЕБУЕТ ОТ НЕГО ВТОРОГО ЗНАНИЯ — лишь второго ХОДА по тому же знанию.
_ОЖИДАЕМОЕ = {}
for _яз, _я in F.ЯЗЫКИ_ДОМА.items():
    for _род, (_сост, _совет) in enumerate(_я["пары"]):
        _голова = _я["что"] if _род in F.ДЕЙСТВИЕ else _я["почему"]
        _закон = B.страница(_яз, "закон", _род)
        _д = _я.get("двоеточие", ": ")
        _ОЖИДАЕМОЕ[(_яз, _сост)] = (
            f"{_голова} {_совет}{_д}{_закон}",           # совет при голове рода
            f"{_совет}. {_я['почему']} {_закон}",        # совет и основание врозь
        )

_ЗАЧИНЫ = {(яз, сост) for яз, сост in _ОЖИДАЕМОЕ}


def _судить(строка):
    с = строка.strip()
    if not с:
        return False, False
    голова, _, хвост = с.partition(". ")
    ключи = [(яз, сост) for (яз, сост) in _ЗАЧИНЫ if сост == голова]
    if not ключи:
        return False, False                      # не зачин этого дома — не подсуден
    for ключ in ключи:
        if хвост in _ОЖИДАЕМОЕ[ключ]:
            return True, True
    return True, False                           # зачин наш, продолжение чужое


судить = closedworld.замкнуть(_судить, ЗАМКНУТЫЕ_МИРЫ)


def main():
    import collections
    from genesis import worlds
    # ПРЕДСТАВЛЕННОЕ «НЕТ» (М-106): закон чужого рода, чужой совет, снятый закон
    я = F.ЯЗЫКИ_ДОМА["ru"]
    сост, совет = я["пары"][0]
    подсадки = (f"{сост}. {я['что']} {совет}: {B.страница('ru', 'закон', 1)}",
                f"{сост}. {я['что']} {я['пары'][1][1]}: {B.страница('ru', 'закон', 0)}",
                f"{сост}. {я['что']} {совет}.")
    пойманы = sum(1 for п in подсадки if _судить(п) == (True, False))
    if пойманы != len(подсадки):
        for п in подсадки:
            print(f"  ПОДСАДКА {_судить(п)}: {п[:100]}")
        print(f"ОТКЛИК FAIL: подсадок поймано {пойманы} из {len(подсадки)}")
        return 1
    итог = collections.Counter(); примеры = []
    for путь in worlds(kind="shows"):
        if путь.name != "genesis_reply.txt":
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
    print(f"ОТКЛИК {поза}: {итог['ложных']} ложных из {итог['судимых']} судимых, "
          f"несудимых {итог['несудимых']}; подсадок поймано {пойманы} из {len(подсадки)}")
    return 0 if поза == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
