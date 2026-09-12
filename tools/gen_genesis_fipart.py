#!/usr/bin/env python3
"""GENESIS layer: ФИНСКИЙ ПАРТИТИВ — see tools/fipartforms.py for the law.

ГРУППЫ СЛОЖЕНЫ ПО ТОМУ, ЧТО ИМЕННО ОНИ ОТНИМАЮТ.

«После числа партитив» и «это единственное, а не множественное» идут вместе: первое даёт
правило, второе отнимает вывод «значит, это множественное».

    ПРАВИЛО, ДАННОЕ БЕЗ СВОИХ ЛОЖНЫХ СЛЕДСТВИЙ, УЧИТ ИМ НАРАВНЕ С СОБОЮ.

«При единице именительный» и «сосед ставит множественное» — второй группой: обе о ГРАНИЦАХ,
одна внутрь языка (единица берёт словарную форму), другая наружу.

«Спрошено и отвечено» — третьей.
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import fipartforms as F  # noqa: E402
from layer import emit_grouped, PASSES  # noqa: E402

ЦЕЛЬ = "datasets/genesis_fipart.txt"
ГРУППЫ = (("после числа партитив", "это единственное, а не множественное"),
          ("при единице именительный", "сосед ставит множественное"),
          ("спрошено и отвечено",))


def pass_groups(шаг):
    вон = []
    for язык in F.ЯЗЫКИ:
        for роды in ГРУППЫ:
            свои = [с for с, (л, р) in F.ПОКАЗЫ.items() if л == язык and р in роды]
            вон.append(свои[шаг::len(PASSES)])
    return вон


def main():
    emit_grouped(ЦЕЛЬ, pass_groups)


if __name__ == "__main__":
    main()
