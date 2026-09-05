#!/usr/bin/env python3
"""GENESIS layer: HOLDINGS WITHOUT A VERB — see tools/holdforms.py for the law.

THE SET IS FINITE AND IS CUT ACROSS THE PASSES, not repeated by them: the
house declares every show it has, and a pass takes its own fifth.
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import holdforms as F  # noqa: E402
from layer import emit_grouped, PASSES  # noqa: E402

ЦЕЛЬ = "datasets/genesis_holdforms.txt"


def язык_группа(шаг, язык):
    свои = [с for с, (л, _) in F.ПОКАЗЫ.items() if л == язык]
    return свои[шаг::len(PASSES)]


def pass_groups(шаг):
    return [язык_группа(шаг, язык) for язык in F.РАМКИ]


def main():
    emit_grouped(ЦЕЛЬ, pass_groups)


if __name__ == "__main__":
    main()
