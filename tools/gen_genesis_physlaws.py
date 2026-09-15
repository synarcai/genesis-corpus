#!/usr/bin/env python3
"""GENESIS layer: PHYSICAL LAWS — dimension, conservation, pressure, wave.

The syllabus court named four subjects absent. Each is a DIFFERENT KIND
of physical reasoning, and their absence left the corpus with formulas
and without physics:

  · DIMENSION is the check that costs nothing and catches everything:
    a law whose sides disagree in dimension is wrong before any number
    is put in. The corpus knew units and never checked a law BY them;
  · CONSERVATION is the first argument from what does NOT change — the
    shape of reasoning that carries the whole of physics;
  · PRESSURE is force over area: the first quantity that is a RATIO of
    two others, and therefore the first place where a unit is derived
    rather than named;
  · WAVE ties period and frequency as reciprocals — the first inverse
    proportion with physical meaning.

EVERY NUMBER IS EXACT. Frequencies are chosen so that period × frequency
is whole; pressures so that force divides the area exactly. A corpus
that rounds teaches rounding, and the arithmetic court would rightly
call it false.
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import physlawforms as F  # noqa: E402
from layer import emit_grouped  # noqa: E402

# ЦЕЛЬ ОБЪЯВЛЯЕТСЯ СТРОКОЙ: указатель родов ищет МИР ДОМА по ней и по ввозу кузницы.
ЦЕЛЬ = "datasets/genesis_physlaws.txt"


def main():
    emit_grouped(ЦЕЛЬ, F.группы_страниц)


if __name__ == "__main__":
    main()
