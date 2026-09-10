#!/usr/bin/env python3
"""КОВКА ДОМА ОДНОЙ ДОЛИ РАЗНЫМИ ЗАПИСЯМИ.

РАВНЫЕ И РАЗНЫЕ ИДУТ В ОДНОМ ПРОХОДЕ: они суть минимальная пара дома — «2 из 4» и «1 из 2»
отличаются всеми цифрами и суть одно, «1 из 2» и «1 из 3» отличаются одной и суть разное.
Порознь первое учило бы, что записи всегда равны, второе — что всегда различны.

ИМЯ И ДРОБЬ идут своей группой: обе связывают отношение с ИНОЙ записью — словом и дробью, — и
рядом друг с другом читаются одним законом о трёх именах одного числа.
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import sameshareforms as F  # noqa: E402
from layer import emit_grouped, PASSES  # noqa: E402

ЦЕЛЬ = "datasets/genesis_sameshare.txt"
ГРУППЫ = (("равные", "разные"), ("имя", "дробь"))


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
