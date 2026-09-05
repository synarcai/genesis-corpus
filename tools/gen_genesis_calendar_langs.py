#!/usr/bin/env python3
"""GENESIS layer: THE WEEK IN EIGHT LANGUAGES — «k days after X comes Y».

The owner's word: every language in surplus. The calendar world's cycle
shows («3 days after tuesday comes friday», «через 3 дня после понедельника
наступает четверг») are the shows from which the organism buys the weekly
cycle (holon's ЦИКЛ: positions from the constraints Y = X + k mod n, no
names, no seven); this world gives the same shows in de/fr/es/it/pt/nl/pl/tr,
statement and question answered by the statement (М-153). The house of
weekday phrases (tools/calforms.py) holds the names with the oblique forms
the phrase bends them into; the court counts the cycle itself.
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import calforms as F  # noqa: E402
from layer import emit_grouped  # noqa: E402

ЦЕЛЬ = "datasets/genesis_calendar_langs.txt"


def язык_группа(шаг, язык):
    """Every start day once per pass as a statement and once as a question;
    the count k of a start day walks 1..6 with the pass (2·day + pass mod 6),
    so a question frame carries five distinct k over the five passes
    (М-148 (1); holon's TSV 21e865b: mass<4-distinct)."""
    вон = []
    for j in range(7):
        i = (шаг * 3 + j) % 7
        вон.append(F.утверждение(язык, i, 1 + (2 * i + шаг) % 6))
        i2 = (i + 3) % 7
        вон.append(F.вопрос(язык, i2, 1 + (2 * i2 + шаг + 3) % 6))
        вон.append(F.сосед(язык, (j + шаг) % 7))
        вон.append(F.вчера(язык, (j + шаг) % 7, "вчера"))
        вон.append(F.вчера(язык, (j + шаг) % 7, "завтра"))
        вон.append(F.вчера(язык, (j + шаг) % 7, "послезавтра"))
        вон.append(F.вчера(язык, (j + шаг) % 7, "позавчера"))
    return вон


def pass_groups(шаг):
    return [язык_группа(шаг, язык) for язык in F.ЯЗЫКИ]


def main():
    emit_grouped(ЦЕЛЬ, pass_groups)


if __name__ == "__main__":
    main()
