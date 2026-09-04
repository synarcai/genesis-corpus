#!/usr/bin/env python3
"""GENESIS layer: EVERYDAY SPEECH — the first word a person writes.

The owner's order (04.09, through holon): he tried the organism alive and
wrote it «привет». The organism was SILENT, and silent again to «ты не
знаешь, что такое привет?». The defect is not in the roads — in the whole
svod (309 132 lines, 135 worlds) the number of greetings was EXACTLY ZERO. A
product whose first word cannot be answered has no first word.

The layer writes the declared set of the house (tools/dialogueforms.py) in
nine languages of the attack: pairs of the everyday («привет.
здравствуйте.», «спасибо. не за что.»), definitions of the everyday («что
такое привет? привет — это приветствие.»), the name and the fan of questions
that ask it, the answer to «кто ты?», and POLITE IGNORANCE («что такое
кваркозавр? я не знаю, что такое кваркозавр.») — the honest answer that
silence is not.

THE SET IS FINITE AND IS CUT ACROSS THE PASSES, not repeated by them: the
house declares every show it has, and a pass takes its own fifth. Repeating a
closed set five times would buy nothing and would weigh five times as much.
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import dialogueforms as F  # noqa: E402
from layer import emit_grouped, PASSES  # noqa: E402

ЦЕЛЬ = "datasets/genesis_dialogue.txt"


def язык_группа(шаг, язык):
    свои = [с for с, (л, _) in F.ПОКАЗЫ.items() if л == язык]
    return свои[шаг::len(PASSES)]


def pass_groups(шаг):
    return [язык_группа(шаг, язык) for язык in F.ЯЗЫКИ]


def main():
    emit_grouped(ЦЕЛЬ, pass_groups)


if __name__ == "__main__":
    main()
