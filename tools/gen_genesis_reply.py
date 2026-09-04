#!/usr/bin/env python3
"""GENESIS layer: ОТКЛИК — see tools/replyforms.py for the law.

THE SET IS FINITE AND IS CUT ACROSS THE PASSES, not repeated by them.
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import replyforms as F  # noqa: E402
from layer import emit_grouped, PASSES  # noqa: E402

ЦЕЛЬ = "datasets/genesis_reply.txt"


def язык_группа(шаг, язык):
    свои = [с for с, (л, _) in F.ПОКАЗЫ.items() if л == язык]
    return свои[шаг::len(PASSES)]


def pass_groups(шаг):
    return [язык_группа(шаг, язык) for язык in F.ЯЗЫКИ]


def main():
    emit_grouped(ЦЕЛЬ, pass_groups)


if __name__ == "__main__":
    main()
