#!/usr/bin/env python3
"""КОВКА ДОМА ПРАВИЛА ЗНАКОВ.

ОДИН МИНУС И ДВА МИНУСА ИДУТ В ОДНОМ ПРОХОДЕ: «(−3) × 4» и «(−3) × (−4)» суть минимальная пара
по числу знаков, и разница между ними — в одном месте: сколько минусов в произведении. Порознь
первое внушало бы, что минус всегда портит ответ, второе — что минус ничего не значит.

ДЕЛЕНИЕ И ЛЕСТНИЦА идут своей группой: одна говорит, что правило не принадлежит умножению,
другая — ОТКУДА оно взялось. Правило без вывода читатель обязан запомнить.
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import signrulforms as F  # noqa: E402
from layer import emit_grouped, PASSES  # noqa: E402

ЦЕЛЬ = "datasets/genesis_signrul.txt"
ГРУППЫ = (("минус на плюс", "минус на минус"), ("деление знаком", "лестница"))


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
