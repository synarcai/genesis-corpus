#!/usr/bin/env python3
"""КУЗНИЦА МИРА ОДНОГО СЛОВА В ДВУХ СМЫСЛАХ: страницы дома `homonym`.

Куплен НУЛЁМ 14.09: «омоним» — 4 строки на 451 367, и все четыре поминают слово, а не
показывают дело. Что ОДНО слово бывает ДВУМЯ вещами, корпус не говорит нигде.
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import homonym as F  # noqa: E402
from layer import PASSES, emit_grouped  # noqa: E402

ЦЕЛЬ = "datasets/genesis_homonym.txt"


def язык_группа(шаг, язык):
    свои = [с for с, (л, _р) in F.ПОКАЗЫ.items() if л == язык]
    return свои[шаг::len(PASSES)]


def pass_groups(шаг):
    return [язык_группа(шаг, язык) for язык in F.ЯЗЫКИ]


def main():
    emit_grouped(ЦЕЛЬ, pass_groups)


if __name__ == "__main__":
    main()
