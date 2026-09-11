#!/usr/bin/env python3
"""КОВКА ДОМА ТОЧКИ НА ПЛОСКОСТИ.

СМЫСЛ И ЗАКОН ИДУТ В ОДНОМ ПРОХОДЕ: «первое число — вправо, второе — вверх» даёт паре смысл, а
«(3, 2) и (2, 3) различны» — закон о порядке. Порознь закон был бы объявлением без основания.

ДВА НАПРАВЛЕНИЯ ХОДА идут своей группой: вправо меняет первое число, вверх — второе, и это
минимальная пара по направлению. Порознь читатель решил бы, что первое число и есть расстояние.
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import pointforms as F  # noqa: E402
from layer import emit_grouped, PASSES  # noqa: E402

ЦЕЛЬ = "datasets/genesis_point.txt"
ГРУППЫ = (("чтение пары", "порядок"), ("вправо", "вверх"))


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
