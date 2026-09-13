#!/usr/bin/env python3
"""GENESIS layer: RUSSIAN VERB FRAMES — the missing link of ru-anaphora.

Asked by omega-e9 with the reason MEASURED, not guessed: the pronoun
market bought «he/she» on the English side (held 60/60, ref 0) and the
Russian side stayed outside it — «он/она» could not be bought because
the Russian VERBS of the story frames were never bought either. A form
is bought by MASS IN ITS FRAME, and the Russian frames had no mass.

SAME MASS AS THE ENGLISH `verbal` WORLD: ten verbs, four frames, five
passes. Same frames, so the two sides are comparable surface by surface
— that is what lets a market see them as one relation rather than two.

THREE AGREEMENTS AT ONCE, AND ALL THREE DECLARED, NOT DERIVED:
  · the ACCUSATIVE of the object («написала 1 книгу», not «1 книга») —
    the very defect omega-e9 found by eye in my speech layer;
  · the COUNT form of the noun (1 / 2-4 / 5+), read from the pack;
  · the GENDER of the past tense («вера написала», «пётр написал») —
    Russian marks the actor's gender in the verb itself, and no other
    language of the corpus does.
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import ruverbsforms as F  # noqa: E402
from layer import emit_grouped  # noqa: E402

ЦЕЛЬ = "datasets/genesis_ruverbs.txt"


def main():
    emit_grouped(ЦЕЛЬ, F.группы)


if __name__ == "__main__":
    main()
