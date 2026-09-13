#!/usr/bin/env python3
"""GENESIS layer: VERBAL EQUALITY AND PAST TENSE — two tails asked by e9.

Requested by omega-e9 from the band side, with the reason measured, not
guessed:

  · «IS» AS THE COPULA OF EQUALITY. The school layer's bought equality
    family is equals / = / равно; «is» was never bought because the
    corpus almost never shows it in that role. «5 plus 3 is 8» is the
    same statement as «5 plus 3 equals 8», and the organism cannot know
    that until both are shown of the SAME facts;
  · THE PAST TENSE IN THE MARKET'S OWN FRAME. Only «writes» was bought;
    «wrote» had sixty lines and did not carry. A form is bought by
    MASS IN ITS FRAME, not by existing somewhere.

BOTH SURFACES OF ONE FACT STAND SIDE BY SIDE. That is the corpus's own
law of bridges: two writings of a single fact, judged by one count, are
what let a market learn that they are one.
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import verbalforms as F  # noqa: E402
from layer import emit_grouped  # noqa: E402

# ЦЕЛЬ ОБЪЯВЛЯЕТСЯ СТРОКОЙ: указатель родов ищет МИР ДОМА по ней и по ввозу кузницы.
ЦЕЛЬ = "datasets/genesis_verbal.txt"


def main():
    emit_grouped(ЦЕЛЬ, F.группы)


if __name__ == "__main__":
    main()
