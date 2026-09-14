#!/usr/bin/env python3
"""КУЗНИЦА МИРА ДОВОДА О ГОВОРЯЩЕМ: страницы дома `adhominem`.

Куплен НУЛЁМ 14.09, последним из шестидесяти пяти семейств пробы: «к человеку» /
«ad hominem» — 0 строк. Довод, взятый НЕ О ПРЕДМЕТЕ ВОВСЕ, корпус не называет нигде.
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import adhominem as F  # noqa: E402
from layer import PASSES, emit_grouped  # noqa: E402

ЦЕЛЬ = "datasets/genesis_adhominem.txt"


def язык_группа(шаг, язык):
    свои = [с for с, (л, _р) in F.ПОКАЗЫ.items() if л == язык]
    return свои[шаг::len(PASSES)]


def pass_groups(шаг):
    return [язык_группа(шаг, язык) for язык in F.ЯЗЫКИ]


def main():
    emit_grouped(ЦЕЛЬ, pass_groups)


if __name__ == "__main__":
    main()
