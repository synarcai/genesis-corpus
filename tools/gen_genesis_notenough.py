#!/usr/bin/env python3
"""КУЗНИЦА МИРА НЕХВАТКИ ДАННЫХ: страницы дома `notenough`.

Куплен НУЛЁМ 14.09, и это самый дорогой ноль дня: «лишнее число в задаче» — 63 строки,
«данных не хватает» — 0. Корпус научил ОТБРАСЫВАТЬ ЛИШНЕЕ и ни разу — ОСТАНАВЛИВАТЬСЯ.
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import notenough as F  # noqa: E402
from layer import PASSES, emit_grouped  # noqa: E402

ЦЕЛЬ = "datasets/genesis_notenough.txt"


def язык_группа(шаг, язык):
    свои = [с for с, (л, _р) in F.ПОКАЗЫ.items() if л == язык]
    return свои[шаг::len(PASSES)]


def pass_groups(шаг):
    return [язык_группа(шаг, язык) for язык in F.ЯЗЫКИ]


def main():
    emit_grouped(ЦЕЛЬ, pass_groups)


if __name__ == "__main__":
    main()
