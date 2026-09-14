#!/usr/bin/env python3
"""КУЗНИЦА МИРА СРАВНЕНИЯ ДАТ: страницы дома `datecmp`.

Куплен НУЛЁМ 14.09: «какая дата» / «which date» — 0 строк. «Раньше» в своде есть (152),
но всё это ВРЕМЯ СУТОК; о том, какая из двух ДАТ раньше, не сказано нигде.
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import datecmp as F  # noqa: E402
from layer import PASSES, emit_grouped  # noqa: E402

ЦЕЛЬ = "datasets/genesis_datecmp.txt"


def язык_группа(шаг, язык):
    свои = [с for с, (л, _р) in F.ПОКАЗЫ.items() if л == язык]
    return свои[шаг::len(PASSES)]


def pass_groups(шаг):
    return [язык_группа(шаг, язык) for язык in F.ЯЗЫКИ]


def main():
    emit_grouped(ЦЕЛЬ, pass_groups)


if __name__ == "__main__":
    main()
