#!/usr/bin/env python3
"""GENESIS layer: FOUNDATIONS OF INFORMATICS — and of control.

Six subjects of informatics and two of cybernetics stood absent from
the whole corpus. They are not advanced topics: they are the ideas
without which a programmer is a typist.

  · ENTROPY is why a message costs bits at all — the bridge between
    counting outcomes and paying for them;
  · THE AUTOMATON is state and transition, the smallest machine that
    REMEMBERS. It is executed here, not described;
  · THE GRAMMAR is a language given by rules rather than by a list —
    the first object that is infinite and finite at once;
  · DECIDABILITY is the discovery that some questions have no general
    algorithm. It cannot be computed, and so it is DECLARED beside the
    computable ones it qualifies (М-103);
  · THE TYPE is the genus of a value: 7 is whole, 7 ÷ 2 is not;
  · THE INVARIANT is what a loop preserves — the only honest way to
    know a loop without running it forever;
  · HOMEOSTASIS is a regulator holding a value inside bounds;
  · THE MODEL is Conant–Ashby: to control a system one must have a
    model of it, and an observer that cannot tell its states apart
    cannot control it.

EVERYTHING IS EXECUTED. The automaton is run, the grammar derived, the
loop unrolled, the clamp applied. Only decidability is declared, and it
is declared as declared.
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import compsciforms as F  # noqa: E402
from layer import emit_grouped  # noqa: E402

# ЦЕЛЬ ОБЪЯВЛЯЕТСЯ СТРОКОЙ: указатель родов ищет МИР ДОМА по ней и по ввозу кузницы.
ЦЕЛЬ = "datasets/genesis_compsci.txt"


def main():
    emit_grouped(ЦЕЛЬ, F.группы_страниц)


if __name__ == "__main__":
    main()
