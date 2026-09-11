#!/usr/bin/env python3
"""КОВКА ДОМА МАСШТАБА.

ДВА НАПРАВЛЕНИЯ ХОДА ИДУТ В ОДНОМ ПРОХОДЕ: «с карты на землю» и «с земли на карту» суть
минимальная пара по направлению — умножают на масштаб или делят на него. Порознь читатель выучил
бы одно направление и застрял в обратной задаче.

ЛОВУШКА И СМЫСЛ ЗАПИСИ идут своей группой: «1 : 2000 мельче, чем 1 : 1000» и «всякая длина
уменьшена в 1000 раз» — первое показывает обратность, второе говорит, что значит сама запись.
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import mapscaleforms as F  # noqa: E402
from layer import emit_grouped, PASSES  # noqa: E402

ЦЕЛЬ = "datasets/genesis_mapscale.txt"
ГРУППЫ = (("на землю", "на карту"), ("мельче", "во сколько"))


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
