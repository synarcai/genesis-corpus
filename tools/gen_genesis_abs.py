#!/usr/bin/env python3
"""КОВКА ДОМА МОДУЛЯ ЧИСЛА.

ИМЯ И ЕГО ГРАНИЦА ИДУТ В ОДНОМ ПРОХОДЕ: «|−5| = 5» и «|−5| = |5|, хотя −5 и 5 разные числа» —
первая страница даёт имя расстоянию, вторая говорит, что по нему нельзя вернуться к числу.

ДВЕ ЛОВУШКИ идут своей группой: модуль суммы не есть сумма модулей, и у меньшего числа модуль
больше. Обе о том, что модуль ТЕРЯЕТ ЗНАК, и обе порознь внушали бы обратное.
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import absforms as F  # noqa: E402
from layer import emit_grouped, PASSES  # noqa: E402

ЦЕЛЬ = "datasets/genesis_abs.txt"
ГРУППЫ = (("расстояние", "равные модули"), ("модуль суммы", "порядок"))


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
