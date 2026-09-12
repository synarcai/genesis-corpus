#!/usr/bin/env python3
"""GENESIS layer: МЕДИАНА И СРЕДНЕЕ — see tools/medianforms.py for the law.

ОБЕ СТОРОНЫ ЛОВУШКИ ИДУТ ОДНОЙ ГРУППОЙ: «выброс двигает среднее» и «в ровном ряду они
совпали». Показанная порознь, первая учит не верить среднему вовсе, вторая — верить всегда.

    МЕРА, ВЕРНАЯ ПРИ РОВНОМ РЯДЕ, НЕ ЕСТЬ МЕРА ВЕРНАЯ: РОВНОСТЬ — УСЛОВИЕ, А НЕ ФОН.

ДВЕ МЕРЫ ОДНОГО РЯДА — одной группой: среднее и медиана, считанные порознь и ни разу не
сведённые, читаются как два имени одного. ЧЕМ МЕРИТЬ — отдельно: это довод, а не счёт.
ВОПРОС отдельно.
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import medianforms as F  # noqa: E402
from layer import emit_grouped, PASSES  # noqa: E402

ЦЕЛЬ = "datasets/genesis_median.txt"
ГРУППЫ = (("среднее ряда", "медиана ряда"),
          ("выброс двигает среднее", "выброс не двигает медианы", "ровный ряд"),
          ("медиана есть место", "чем мерить"),
          ("спрошенное",))


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
