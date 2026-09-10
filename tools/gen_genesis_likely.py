#!/usr/bin/env python3
"""КОВКА ДОМА ШКАЛЫ УВЕРЕННОСТИ.

ДВЕ СТУПЕНИ ИДУТ В ОДНОМ ПРОХОДЕ: «вряд ли» и «скорее всего» суть одна шкала с двух сторон
границы, и порознь они читались бы двумя правилами. ГРАНИЦА идёт своей группой: «равно
возможно» есть та самая половина, о которой говорят обе ступени, и рядом с ними она была бы
третьим случаем, а не мерой.
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import likelyforms as F  # noqa: E402
from layer import emit_grouped, PASSES  # noqa: E402

ЦЕЛЬ = "datasets/genesis_likely.txt"
ГРУППЫ = (("вряд ли", "скорее всего"), ("поровну",))


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
