#!/usr/bin/env python3
"""GENESIS layer: CALENDAR — cyclic arithmetic in its applied genus.

Neither a weekday nor a month appeared anywhere in the corpus. This is
not a decoration missing: the week is the first CYCLIC structure a
child meets, and «what day comes four days after Wednesday» is
congruence modulo 7 wearing clothes. A corpus that teaches `17 mod 5`
and cannot answer that question has taught the symbol and not the
thing.

THE CYCLE IS COMPUTED, NEVER LISTED. Day names and month lengths are
declared (they are facts of a calendar, not derivable), but every
answer is derived from them by modular arithmetic — the same operation
the number layer shows bare.
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import calendarforms as F  # noqa: E402
from layer import emit_grouped  # noqa: E402

# ЦЕЛЬ ОБЪЯВЛЯЕТСЯ СТРОКОЙ: указатель родов ищет МИР ДОМА по ней и по ввозу кузницы.
ЦЕЛЬ = "datasets/genesis_calendar.txt"


def main():
    emit_grouped(ЦЕЛЬ, F.группы)


if __name__ == "__main__":
    main()
