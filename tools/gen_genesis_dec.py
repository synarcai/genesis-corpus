#!/usr/bin/env python3
"""КОВКА ДОМА ДЕСЯТИЧНОЙ ДОЛИ.

ЗАПИСЬ И ЕЁ ГРАНИЦА ИДУТ В ОДНОМ ПРОХОДЕ: «0,75 = 3/4» и «1/6 конечной записи не имеет» суть
закон и его предел, и порознь первое внушало бы, что всякая доля записывается десятичной дробью.

ЛОВУШКА И ЛИШНИЙ НОЛЬ идут своей группой: обе о том, что цифры записи не равны величине — в
одной больше цифр при меньшем числе, в другой цифра прибавлена, а число то же.
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import decforms as F  # noqa: E402
from layer import emit_grouped, PASSES  # noqa: E402

ЦЕЛЬ = "datasets/genesis_dec.txt"
ГРУППЫ = (("запись доли", "граница"), ("сравнение", "лишний ноль"))


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
