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


def pass_groups(шаг):
    """Одна группа на ЯЗЫК — сборка живёт в доме, кузница её лишь зовёт."""
    return F.группы(шаг)


def main():
    emit_grouped(ЦЕЛЬ, pass_groups)


if __name__ == "__main__":
    main()
