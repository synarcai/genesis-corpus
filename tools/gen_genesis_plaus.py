#!/usr/bin/env python3
"""КОВКА ДОМА ПРАВДОПОДОБИЯ.

ВОЗМОЖНОЕ И НЕВОЗМОЖНОЕ ИДУТ В ОДНОМ ПРОХОДЕ: «ученик весит 33 килограмма» и «ученик не может
весить 363 килограмма» суть минимальная пара по границе — та же вещь, та же мера, и разница в
одном месте: вышло ли число за объявленный предел.

ДВА КРАЯ идут своей группой: слишком много и слишком мало. Порознь читатель сторожил бы одну
сторону и пропускал другую — а невозможное бывает и снизу.
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import plausforms as F  # noqa: E402
from layer import emit_grouped, PASSES  # noqa: E402

ЦЕЛЬ = "datasets/genesis_plaus.txt"
ГРУППЫ = (("правдоподобно", "счёт сошёлся"), ("слишком много", "слишком мало"))


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
