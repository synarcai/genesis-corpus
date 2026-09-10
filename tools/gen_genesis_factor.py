#!/usr/bin/env python3
"""КОВКА ДОМА РАЗЛОЖЕНИЯ И ДЕЛИМОСТИ.

ДВА ОТКАЗА ИДУТ В ОДНОМ ПРОХОДЕ: «пятёрки нет вовсе» и «второй двойки не хватает» суть
минимальная пара по ПРИЧИНЕ — вердикт один, а беды разные, и вторая коварнее: множитель виден,
а делимости нет. Порознь они читались бы двумя случаями, рядом — законом.

ДВА СОГЛАСИЯ идут своей группой: делитель есть либо сам множитель, либо произведение части
множителей, и это одна мысль на двух ступенях.
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import factorforms as F  # noqa: E402
from layer import emit_grouped, PASSES  # noqa: E402

ЦЕЛЬ = "datasets/genesis_factor.txt"
ГРУППЫ = (("нет вовсе", "не хватает"), ("множитель", "набор"))


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
