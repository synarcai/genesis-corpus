#!/usr/bin/env python3
"""КУЗНИЦА МИРА РАССАДКИ ПО ОГРАНИЧЕНИЯМ: страницы дома `whodwells`.

Куплен НУЛЁМ 14.09: «кто где живёт» / «who lives where» — 0 строк. Мир вывода держит ОДИН
ход; вывода из НЕСКОЛЬКИХ ограничений разом, где ни одно само по себе ничего не решает,
корпус не показывал нигде.
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import whodwells as F  # noqa: E402
from layer import PASSES, emit_grouped  # noqa: E402

ЦЕЛЬ = "datasets/genesis_whodwells.txt"


def язык_группа(шаг, язык):
    свои = [с for с, (л, _р) in F.ПОКАЗЫ.items() if л == язык]
    return свои[шаг::len(PASSES)]


def pass_groups(шаг):
    return [язык_группа(шаг, язык) for язык in F.ЯЗЫКИ]


def main():
    emit_grouped(ЦЕЛЬ, pass_groups)


if __name__ == "__main__":
    main()
