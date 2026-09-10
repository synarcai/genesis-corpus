#!/usr/bin/env python3
"""КОВКА ДОМА ПРИЗНАКОВ ДЕЛИМОСТИ.

ТРИ ВИДА ПРИЗНАКА ИДУТ ТРЕМЯ ГРУППАМИ, И ВСЯКАЯ НЕСЁТ СВОЁ ДА И СВОЁ НЕТ: хвост смотрит на ОДНУ
цифру, сумма — на ВСЕ, пара — на ДВЕ. Порознь «да» и «нет» одного вида читались бы двумя
правилами; вместе — одним правилом с двумя исходами.

Разводить же виды по разным проходам НАДО: показанные вперемешку, они внушали бы, что признак
всякий раз новый, тогда как их ровно три и они разного устройства.
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import divruleforms as F  # noqa: E402
from layer import emit_grouped, PASSES  # noqa: E402

ЦЕЛЬ = "datasets/genesis_divrule.txt"
ГРУППЫ = (("хвост да", "хвост нет"), ("сумма да", "сумма нет"), ("пара да", "пара нет"))


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
