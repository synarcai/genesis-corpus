#!/usr/bin/env python3
"""GENESIS layer: ПРИЧИНА ОТКАЗА — see tools/refusalwhyforms.py for the law.

ГРУППЫ СЛОЖЕНЫ ПО ТОМУ, ЧТО ИМЕННО ОНИ ОТНИМАЮТ.

«Отказ, замена и причина» идёт первым и один: он даёт ФАКТ — что отвергнуто, что поставлено
взамен и каким словом названа причина.

«Один закон, много языков» — вторым: он отнимает вывод «у каждого языка свои запреты».

    ПРАВИЛО, ДАННОЕ БЕЗ СВОИХ ЛОЖНЫХ СЛЕДСТВИЙ, УЧИТ ИМ НАРАВНЕ С СОБОЮ.

«Спрошено и отвечено» — третьей.
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import refusalwhyforms as F  # noqa: E402
from layer import emit_grouped, PASSES  # noqa: E402

ЦЕЛЬ = "datasets/genesis_refusalwhy.txt"
ГРУППЫ = (("отказ, замена и причина",),
          ("один закон, много языков",),
          ("спрошено и отвечено",))


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
