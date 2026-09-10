#!/usr/bin/env python3
"""КОВКА ДОМА ВЕРОЯТНОСТИ.

ДОЛЯ И ДОПОЛНЕНИЕ ИДУТ В ОДНОМ ПРОХОДЕ: они суть минимальная пара — числа те же, вопрос иной,
— и порознь читались бы двумя примерами, а рядом читаются законом. Края ряда (невозможное и
достоверное) идут своей группой: они об ином — о том, что вероятность бывает нулём и единицей.
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import chanceforms as F  # noqa: E402
from layer import emit_grouped, PASSES  # noqa: E402

ЦЕЛЬ = "datasets/genesis_chance.txt"
ГРУППЫ = (("доля", "дополнение"), ("невозможное", "достоверное"))


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
