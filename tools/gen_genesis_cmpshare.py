#!/usr/bin/env python3
"""КОВКА ДОМА СРАВНЕНИЯ ДОЛЕЙ.

ДВА ЧАСТНЫХ ПРАВИЛА ИДУТ В ОДНОМ ПРОХОДЕ: «один знаменатель» и «один числитель» суть
минимальная пара ПО НАПРАВЛЕНИЮ — в первом большее число даёт большую долю, во втором меньшее.
Порознь первое обобщилось бы на второе, и читатель решил бы, что 1/5 больше 1/3.

ОБЩИЙ СЛУЧАЙ И РАВЕНСТВО идут своей группой: приведение к общему знаменателю работает всюду, а
равенство долей показывает, что сравнение не обязано кончаться перевесом.
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import cmpshareforms as F  # noqa: E402
from layer import emit_grouped, PASSES  # noqa: E402

ЦЕЛЬ = "datasets/genesis_cmpshare.txt"
ГРУППЫ = (("один знаменатель", "один числитель"), ("общий знаменатель", "равные"))


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
