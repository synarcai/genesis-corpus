#!/usr/bin/env python3
"""GENESIS layer: ОДНОШАГОВОЕ УРАВНЕНИЕ — see tools/onestepforms.py for the law.

THE SET IS FINITE AND IS CUT ACROSS THE PASSES, not repeated by them.
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import onestepforms as F  # noqa: E402
from layer import emit_grouped, PASSES  # noqa: E402

ЦЕЛЬ = "datasets/genesis_onestep.txt"


def род_группа(шаг, язык, род):
    свои = [с for с, (л, р) in F.ПОКАЗЫ.items() if л == язык and р == род]
    return свои[шаг::len(PASSES)]


def pass_groups(шаг):
    return [род_группа(шаг, язык, род)
            for язык in F.ЯЗЫКИ for род in F.РОДЫ]


def main():
    emit_grouped(ЦЕЛЬ, pass_groups)


if __name__ == "__main__":
    main()
