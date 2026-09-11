#!/usr/bin/env python3
"""КОВКА ДОМА ДВУХ СМЫСЛОВ ДЕЛЕНИЯ.

ДВА ВИДА ЗАДАЧИ ИДУТ В ОДНОМ ПРОХОДЕ: «12 конфет на 4 учеников» и «12 конфет по 3 в коробку» суть
минимальная пара по вопросу — известно число частей или величина части. Порознь читатель решил
бы, что деление одно, и застрял бы на задаче другого вида.

ВСТРЕЧА И ПРИЧИНА идут своей группой: «у равенства два смысла» сводит оба вида в одну строку, а
«число одно, а вещи разные» говорит, откуда берётся различие — из ВОПРОСА, а не из счёта.
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import divsenseforms as F  # noqa: E402
from layer import emit_grouped, PASSES  # noqa: E402

ЦЕЛЬ = "datasets/genesis_divsense.txt"
ГРУППЫ = (("на части", "по содержанию"), ("два смысла", "вещь ответа"))


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
