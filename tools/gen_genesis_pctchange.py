#!/usr/bin/env python3
"""КОВКА ДОМА ИЗМЕНЕНИЯ НА ПРОЦЕНТ.

РОСТ И УБЫЛЬ ИДУТ В ОДНОМ ПРОХОДЕ: те же числа, тот же процент, и разница в одном знаке — это
минимальная пара по направлению, и порознь каждая была бы половиной действия.

ЛОВУШКА И ЕЁ ПРИЧИНА идут своей группой: «вышло меньше прежнего» и «второй процент взят от
другого числа» суть ЧТО и ПОЧЕМУ. Порознь первое было бы фокусом, второе — арифметикой без повода.
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import pctchangeforms as F  # noqa: E402
from layer import emit_grouped, PASSES  # noqa: E402

ЦЕЛЬ = "datasets/genesis_pctchange.txt"
ГРУППЫ = (("рост", "убыль"), ("туда-обратно", "основание"))


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
