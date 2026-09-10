#!/usr/bin/env python3
"""КОВКА ДОМА ПРИКИДКИ.

ПРИКИДКА И ЕЁ ЦЕНА ИДУТ В ОДНОМ ПРОХОДЕ: «около 400» и «точно 378, и прикидка больше на 22»
суть одно умение, сказанное с двух сторон. Порознь первое читалось бы небрежностью, а второе —
придиркой.

ЛОВЛЯ И СУММА идут своей группой: первая показывает, ради чего всё — прикидка отвергает ответ
по числу знаков; вторая говорит, что тот же ход годен не только для произведения.
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import estimforms as F  # noqa: E402
from layer import emit_grouped, PASSES  # noqa: E402

ЦЕЛЬ = "datasets/genesis_estim.txt"
ГРУППЫ = (("произведение", "точно"), ("ловит", "сумма"))


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
