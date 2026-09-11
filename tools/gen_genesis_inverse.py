#!/usr/bin/env python3
"""КОВКА ДОМА ОБРАТНОЙ ЗАДАЧИ.

ПРЯМАЯ И ОБРАТНАЯ ИДУТ В ОДНОМ ПРОХОДЕ И НА ОДНОЙ ТРОЙКЕ ЧИСЕЛ: меняются местами известное и
искомое, а числа остаются. Разные тройки развели бы стороны одного дела.

ДВА ДЕЙСТВИЯ идут своими группами: сложение с вычитанием и умножение с делением. Одна пара
показала бы свойство сложения; две пары показывают ЗАКОН об обратном действии.
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import inverseforms as F  # noqa: E402
from layer import emit_grouped, PASSES  # noqa: E402

ЦЕЛЬ = "datasets/genesis_inverse.txt"
ГРУППЫ = (("прямая сумма", "обратная сумма"), ("прямое деление", "обратное деление"))


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
