#!/usr/bin/env python3
"""КОВКА ДОМА ДРОБИ И ЕДИНИЦЫ.

ТРИ СРАВНЕНИЯ С ЕДИНИЦЕЙ ИДУТ В ОДНОМ ПРОХОДЕ: «больше», «меньше» и «ровно» суть полный ряд, и
порознь третье потерялось бы — читатель делит дроби надвое, а «3/3» оказывается меж двух стульев.

РАЗБОР НА ЦЕЛОЕ И ДОЛЮ идёт своей группой: он не сравнивает, а ОТВЕЧАЕТ, что́ значит «больше
единицы», — и рядом со сравнениями читался бы четвёртым сравнением вместо ответа на них.
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import wholeshareforms as F  # noqa: E402
from layer import emit_grouped, PASSES  # noqa: E402

ЦЕЛЬ = "datasets/genesis_wholeshare.txt"
ГРУППЫ = (("больше", "меньше", "ровно"), ("целых",))


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
