#!/usr/bin/env python3
"""КУЗНИЦА МИРА ЧТЕНИЯ ТАБЛИЦЫ: страницы дома `gridread`.

Куплен НУЛЁМ 14.09: «на пересечении» / «at the intersection of» — ни одной строки на
447 451, при 3 085 упоминаниях слова «таблица» как ИМЕНИ ЧУЖОЙ ВЕЩИ, а не как дела.
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import gridread as F  # noqa: E402
from layer import PASSES, emit_grouped  # noqa: E402

ЦЕЛЬ = "datasets/genesis_grid.txt"


def язык_группа(шаг, язык):
    свои = [с for с, (л, _р) in F.ПОКАЗЫ.items() if л == язык]
    return свои[шаг::len(PASSES)]


def pass_groups(шаг):
    return [язык_группа(шаг, язык) for язык in F.ЯЗЫКИ]


def main():
    emit_grouped(ЦЕЛЬ, pass_groups)


if __name__ == "__main__":
    main()
