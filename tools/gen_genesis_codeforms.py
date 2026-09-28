#!/usr/bin/env python3
"""GENESIS layer: CODE WITH BEHAVIOUR — see tools/codeforms.py for the law.

THE SET IS FINITE AND IS CUT ACROSS THE PASSES, not repeated by them: the house declares every show it has,
and a pass takes its own fifth — per language, as the dialogue act house (`gen_genesis_actturn`) does.
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import codeforms as C  # noqa: E402
from layer import emit_grouped, PASSES  # noqa: E402

ЦЕЛЬ = "datasets/genesis_codeforms.txt"


def язык_группа(шаг, язык):
    свои = [с for с, (л, _род, _код) in C.ПОКАЗЫ.items() if л == язык]
    return свои[шаг::len(PASSES)]


def pass_groups(шаг):
    return [язык_группа(шаг, язык) for язык in C.ЯЗЫКИ]


def main():
    emit_grouped(ЦЕЛЬ, pass_groups)


if __name__ == "__main__":
    main()
