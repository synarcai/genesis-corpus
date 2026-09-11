#!/usr/bin/env python3
"""КОВКА ДОМА ПРОЦЕНТНОЙ РАЗНИЦЫ.

ДВА НАПРАВЛЕНИЯ СРАВНЕНИЯ ИДУТ В ОДНОМ ПРОХОДЕ: «100 больше 80 на 25 процентов» и «80 меньше 100
не на 25, а на 20» суть минимальная пара по основанию, и порознь первая внушала бы, что
сравнение процентом симметрично.

ДОЛЯ И ПРИЧИНА идут своей группой: «5 от 20 — это 25 процентов» даёт сам ход, а «один излишек
делится на разные основания» говорит, почему два хода дают разное.
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import pctdiffforms as F  # noqa: E402
from layer import emit_grouped, PASSES  # noqa: E402

ЦЕЛЬ = "datasets/genesis_pctdiff.txt"
ГРУППЫ = (("больше на", "меньше на"), ("доля в процентах", "основание"))


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
