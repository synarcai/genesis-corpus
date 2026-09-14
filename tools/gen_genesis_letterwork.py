#!/usr/bin/env python3
"""КУЗНИЦА МИРА ДЕЛА НАД БУКВАМИ: страницы дома `letterwork`.

Куплен НУЛЁМ 14.09: «палиндром» — 0, «анаграмма» — 0, «сдвиг на N букв» — 0. Дом букв
(`letters`, 360 страниц) умеет СЧИТАТЬ буквы — и только считать.
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import letterwork as F  # noqa: E402
from layer import PASSES, emit_grouped  # noqa: E402

ЦЕЛЬ = "datasets/genesis_letterwork.txt"


def язык_группа(шаг, язык):
    свои = [с for с, (л, _р) in F.ПОКАЗЫ.items() if л == язык]
    return свои[шаг::len(PASSES)]


def pass_groups(шаг):
    return [язык_группа(шаг, язык) for язык in F.ЯЗЫКИ]


def main():
    emit_grouped(ЦЕЛЬ, pass_groups)


if __name__ == "__main__":
    main()
