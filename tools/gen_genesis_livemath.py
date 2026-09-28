#!/usr/bin/env python3
"""GENESIS layer: LIVE PROBLEMS — see tools/livemath.py for the house and tools/livemath_law.py for the law.

THE SET IS FINITE AND IS CUT ACROSS THE PASSES, not repeated by them: the house declares every
show it has (a problem of the source and its eight variants), and a pass takes its own fifth.
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import livemath as F  # noqa: E402
from layer import emit, PASSES  # noqa: E402

ЦЕЛЬ = "datasets/genesis_livemath.txt"


def pass_shows(шаг):
    показы = sorted(F.ПОКАЗЫ, key=lambda с: F.ПРОИСХОЖДЕНИЕ[с])
    return показы[шаг::len(PASSES)]


def main():
    emit(ЦЕЛЬ, pass_shows)


if __name__ == "__main__":
    main()
