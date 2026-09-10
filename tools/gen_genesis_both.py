#!/usr/bin/env python3
"""КОВКА ДОМА ДВУХ УСЛОВИЙ.

ДВЕ НЕУДАЧИ ИДУТ В ОДНОМ ПРОХОДЕ: «первое условие не выполнено» и «второе условие не
выполнено» суть минимальная пара — вердикт один, а подводит разное. Порознь они читались бы
двумя случаями, рядом — законом: довольно ОДНОГО невыполненного.

УДАЧА И ПОЛНАЯ НЕУДАЧА идут своей группой: они суть края таблицы, и без них клетки неполны.
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import bothforms as F  # noqa: E402
from layer import emit_grouped, PASSES  # noqa: E402

ЦЕЛЬ = "datasets/genesis_both.txt"
ГРУППЫ = (("первое", "второе"), ("оба", "ни одного"))


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
