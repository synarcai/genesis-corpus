#!/usr/bin/env python3
"""КОВКА ДОМА ПОРЯДКА ДЕЙСТВИЙ.

ПРАВИЛО И ЕГО ОТМЕНА ИДУТ В ОДНОМ ПРОХОДЕ: «2 + 3 × 4 = 14» и «( 2 + 3 ) × 4 = 20» суть
минимальная пара — числа одни и те же, ответы разные, и вся разница в двух скобках. Порознь
они читались бы двумя правилами, рядом — одним.

ОШИБКА И РАВНОЕ СТАРШИНСТВО идут своей группой: первая показывает, что даёт неверный ход,
вторая — что старшинство не всеобще, и обе поправляют то, что первая пара могла бы внушить.
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import precforms as F  # noqa: E402
from layer import emit_grouped, PASSES  # noqa: E402

ЦЕЛЬ = "datasets/genesis_prec.txt"
ГРУППЫ = (("старшинство", "скобки"), ("ошибка", "равные"))


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
