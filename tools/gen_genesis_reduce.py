#!/usr/bin/env python3
"""КОВКА ДОМА СОКРАЩЕНИЯ ДРОБИ.

СОКРАЩЕНИЕ И ЕГО НЕВОЗМОЖНОСТЬ ИДУТ В ОДНОМ ПРОХОДЕ: «нельзя» здесь не отказ от работы, а её
ИТОГ — разложение выполнено, общего множителя не нашлось, — и рядом с «сокращается» это читается
одним законом, а порознь двумя случаями.

НЕПОЛНОЕ СОКРАЩЕНИЕ И ПРОВЕРКА РАВЕНСТВА идут своей группой: первое говорит, что действие не
кончено, второе — что оно ничего не испортило. Обе суть проверки уже сделанного, и место им
рядом.
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import reduceforms as F  # noqa: E402
from layer import emit_grouped, PASSES  # noqa: E402

ЦЕЛЬ = "datasets/genesis_reduce.txt"
ГРУППЫ = (("сокращается", "нельзя"), ("не до конца", "та же доля"))


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
