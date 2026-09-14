#!/usr/bin/env python3
"""КУЗНИЦА МИРА ОКРУГЛЕНИЯ ПО ДЕЛУ: страницы дома `roundneed`.

Куплен НУЛЁМ 14.09: округление ВВЕРХ в своде есть (77 строк «коробок нужно»), округление
ВНИЗ — «сколько целых» — 0 строк, а обе стороны рядом — нигде.
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import roundneed as F  # noqa: E402
from layer import PASSES, emit_grouped  # noqa: E402

ЦЕЛЬ = "datasets/genesis_roundneed.txt"


def язык_группа(шаг, язык):
    свои = [с for с, (л, _р) in F.ПОКАЗЫ.items() if л == язык]
    return свои[шаг::len(PASSES)]


def pass_groups(шаг):
    return [язык_группа(шаг, язык) for язык in F.ЯЗЫКИ]


def main():
    emit_grouped(ЦЕЛЬ, pass_groups)


if __name__ == "__main__":
    main()
