#!/usr/bin/env python3
"""КУЗНИЦА МИРА ОДНОГО СЛУЧАЯ: страницы дома `onecase`.

Куплен НУЛЁМ 14.09: «пример не доказывает» — 0 строк при 6 о контрпримере. Корпус
показывает примеры тысячами и ни разу не говорит, ЧЕГО ПРИМЕР СТОИ́Т.
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import onecase as F  # noqa: E402
from layer import PASSES, emit_grouped  # noqa: E402

ЦЕЛЬ = "datasets/genesis_onecase.txt"


def язык_группа(шаг, язык):
    свои = [с for с, (л, _р) in F.ПОКАЗЫ.items() if л == язык]
    return свои[шаг::len(PASSES)]


def pass_groups(шаг):
    return [язык_группа(шаг, язык) for язык in F.ЯЗЫКИ]


def main():
    emit_grouped(ЦЕЛЬ, pass_groups)


if __name__ == "__main__":
    main()
