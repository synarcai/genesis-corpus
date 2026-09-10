#!/usr/bin/env python3
"""КОВКА ДОМА САМОИСПРАВЛЕНИЯ.

ОШИБСЯ И НЕ ОШИБСЯ ИДУТ В ОДНОМ ПРОХОДЕ: они суть минимальная пара — проверка одна и та же, а
итог её разный. Порознь первое учило бы, что проверка всегда кончается покаянием, и проверка
стала бы обрядом.

ВЕРНЫЙ ОТВЕТ ПРИ НЕВЕРНОМ ХОДЕ идёт своей группой: он не о счёте, а о ходе, и рядом с первыми
двумя читался бы третьим случаем вместо отдельного закона.
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import amendforms as F  # noqa: E402
from layer import emit_grouped, PASSES  # noqa: E402

ЦЕЛЬ = "datasets/genesis_amend.txt"
ГРУППЫ = (("ошибся", "не ошибся"), ("ход",))


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
