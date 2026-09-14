#!/usr/bin/env python3
"""КУЗНИЦА МИРА ЛОЖНОЙ ДИЛЕММЫ: страницы дома `dilemma`.

Куплен НУЛЁМ 14.09, последним из шестидесяти шести семейств пробы: «ложная дилемма» —
0 строк. Что САМ ПЕРЕЧЕНЬ ВЫХОДОВ БЫВАЕТ НЕПОЛОН, корпус не говорит нигде.
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import dilemma as F  # noqa: E402
from layer import PASSES, emit_grouped  # noqa: E402

ЦЕЛЬ = "datasets/genesis_dilemma.txt"


def язык_группа(шаг, язык):
    свои = [с for с, (л, _р) in F.ПОКАЗЫ.items() if л == язык]
    return свои[шаг::len(PASSES)]


def pass_groups(шаг):
    return [язык_группа(шаг, язык) for язык in F.ЯЗЫКИ]


def main():
    emit_grouped(ЦЕЛЬ, pass_groups)


if __name__ == "__main__":
    main()
