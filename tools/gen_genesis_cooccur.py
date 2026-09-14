#!/usr/bin/env python3
"""КУЗНИЦА МИРА СОВПАДЕНИЯ И ПРИЧИНЫ: страницы дома `cooccur`.

Куплен НУЛЁМ 14.09: «совпадение, а не причина» / «correlation is not» — 0 строк. Корпус
умеет спрашивать «почему?», но не говорит, что ИЗ СОВМЕСТНОГО ДВИЖЕНИЯ ПРИЧИНА НЕ СЛЕДУЕТ.
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import cooccur as F  # noqa: E402
from layer import PASSES, emit_grouped  # noqa: E402

ЦЕЛЬ = "datasets/genesis_cooccur.txt"


def язык_группа(шаг, язык):
    свои = [с for с, (л, _р) in F.ПОКАЗЫ.items() if л == язык]
    return свои[шаг::len(PASSES)]


def pass_groups(шаг):
    return [язык_группа(шаг, язык) for язык in F.ЯЗЫКИ]


def main():
    emit_grouped(ЦЕЛЬ, pass_groups)


if __name__ == "__main__":
    main()
