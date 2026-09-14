#!/usr/bin/env python3
"""КУЗНИЦА МИРА ДВУХ ОТКАЗОВ: страницы дома `noanswer`.

Куплен НУЛЁМ 14.09: «деление на ноль» — 0 строк. Корпус делит тысячами строк и ни разу
не говорит, что деление бывает НЕВЫПОЛНИМО.
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import noanswer as F  # noqa: E402
from layer import PASSES, emit_grouped  # noqa: E402

ЦЕЛЬ = "datasets/genesis_noanswer.txt"


def язык_группа(шаг, язык):
    свои = [с for с, (л, _р) in F.ПОКАЗЫ.items() if л == язык]
    return свои[шаг::len(PASSES)]


def pass_groups(шаг):
    return [язык_группа(шаг, язык) for язык in F.ЯЗЫКИ]


def main():
    emit_grouped(ЦЕЛЬ, pass_groups)


if __name__ == "__main__":
    main()
