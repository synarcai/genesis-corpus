#!/usr/bin/env python3
"""КОВКА ДОМА УМНОЖЕНИЯ ДОЛЕЙ.

РОСТ И УБЫЛЬ ИДУТ В ОДНОМ ПРОХОДЕ: «2/5 × 3» и «1/2 × 1/3» суть минимальная пара по
направлению, и разница между ними — в одном месте: умножается ли знаменатель. Порознь первое
внушало бы, что умножение всегда увеличивает.

ВОЗВРАТ К ЦЕЛОМУ И ВЫХОД ЗА ЕДИНИЦУ идут своей группой: оба говорят, где кончается доля, — одна
страница возвращает к единице, другая переходит за неё.
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import mulshareforms as F  # noqa: E402
from layer import emit_grouped, PASSES  # noqa: E402

ЦЕЛЬ = "datasets/genesis_mulshare.txt"
ГРУППЫ = (("на число", "доля доли"), ("единица", "больше"))


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
