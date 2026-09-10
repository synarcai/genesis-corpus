#!/usr/bin/env python3
"""КОВКА ДОМА СЛОЖЕНИЯ ДОЛЕЙ.

ЛЁГКИЙ И ТРУДНЫЙ СЛУЧАЙ ИДУТ В ОДНОМ ПРОХОДЕ: «1/5 + 2/5» и «1/2 + 1/3» суть минимальная пара —
в первом складываются числители при неизменном знаменателе, во втором до сложения надо сделать
знаменатели одинаковыми. Порознь первый учил бы складывать всё подряд.

ВЫЧИТАНИЕ И ВЫХОД ЗА ЕДИНИЦУ идут своей группой: оба суть продолжение одного хода — приведение
сделано, дальше счёт идёт по числителям, и итог бывает как меньше целого, так и больше.
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import addshareforms as F  # noqa: E402
from layer import emit_grouped, PASSES  # noqa: E402

ЦЕЛЬ = "datasets/genesis_addshare.txt"
ГРУППЫ = (("общий", "разные"), ("вычесть", "больше"))


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
