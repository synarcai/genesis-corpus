#!/usr/bin/env python3
"""КУЗНИЦА МИРА СРЕДНЕГО И РАЗБРОСА: страницы дома `spread`.

Куплен НУЛЁМ 14.09: «среднее скрывает разброс» — 0 строк. Мир среднего СЧИТАЕТ среднее
и умеет это хорошо; что среднее СКРЫВАЕТ, корпус не говорит нигде.
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import spread as F  # noqa: E402
from layer import PASSES, emit_grouped  # noqa: E402

ЦЕЛЬ = "datasets/genesis_spread.txt"


def язык_группа(шаг, язык):
    свои = [с for с, (л, _р) in F.ПОКАЗЫ.items() if л == язык]
    return свои[шаг::len(PASSES)]


def pass_groups(шаг):
    return [язык_группа(шаг, язык) for язык in F.ЯЗЫКИ]


def main():
    emit_grouped(ЦЕЛЬ, pass_groups)


if __name__ == "__main__":
    main()
