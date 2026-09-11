#!/usr/bin/env python3
"""КОВКА ДОМА ЗНАКОВОГО СЛОЖЕНИЯ.

ДВА ВЫЧИТАНИЯ ИДУТ В ОДНОМ ПРОХОДЕ: «5 − 8 = −3» и «5 − (−3) = 8» суть минимальная пара по знаку
вычитаемого, и разница между ними — в одном месте: стои́т ли за минусом скобка. Порознь первое
внушало бы, что вычитание всегда уменьшает.

СЛОЖЕНИЕ И НОЛЬ идут своей группой: «оба влево» уводит от нуля в одну сторону, «уничтожение»
возвращает к нему ровно. Одна мера — шаги от нуля — держит обе страницы.
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import signaddforms as F  # noqa: E402
from layer import emit_grouped, PASSES  # noqa: E402

ЦЕЛЬ = "datasets/genesis_signadd.txt"
ГРУППЫ = (("через ноль", "минус минуса"), ("оба влево", "уничтожение"))


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
