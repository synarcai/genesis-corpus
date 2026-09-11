#!/usr/bin/env python3
"""КОВКА ДОМА УСЛОВИЙ ЗАДАЧИ.

ПОЛНОТА И ЕЁ НЕДОСТАЧА ИДУТ В ОДНОМ ПРОХОДЕ: «данных хватает» и «ответа нет» суть минимальная
пара по полноте — та же задача, тот же вопрос, и разница в одном месте: сказано ли о втором.

ЛИШНЕЕ И ЕГО ИМЯ идут своей группой: одна страница показывает лишнее число, другая называет его
и говорит, почему оно лишнее. Порознь первая была бы приговором без разбора.
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import needforms as F  # noqa: E402
from layer import emit_grouped, PASSES  # noqa: E402

ЦЕЛЬ = "datasets/genesis_need.txt"
ГРУППЫ = (("хватает", "не хватает"), ("лишнее", "какое лишнее"))


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
