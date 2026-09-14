#!/usr/bin/env python3
"""КУЗНИЦА МИРА ПУТИ ПО ДОРОГАМ: страницы дома `roadpath`.

Куплен НУЛЁМ 14.09: «как пройти от» / «how to get from» — 0 строк. Корпус знает
расстояние, порядок и связь ДВУХ, но СЕТИ связей, где до места добираются ЧЕРЕЗ другое, — нет.
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import roadpath as F  # noqa: E402
from layer import PASSES, emit_grouped  # noqa: E402

ЦЕЛЬ = "datasets/genesis_roadpath.txt"


def язык_группа(шаг, язык):
    свои = [с for с, (л, _р) in F.ПОКАЗЫ.items() if л == язык]
    return свои[шаг::len(PASSES)]


def pass_groups(шаг):
    return [язык_группа(шаг, язык) for язык in F.ЯЗЫКИ]


def main():
    emit_grouped(ЦЕЛЬ, pass_groups)


if __name__ == "__main__":
    main()
