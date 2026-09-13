#!/usr/bin/env python3
"""GENESIS layer: VALENCE WITH ITS GROUND — «good/bad», «afraid/calm».

Built to `reference/GROUNDING-QUALIA-CANON.md` (collegium 01.09, primary
source: the owner's website canon on qualia structure). Every address
and formula here is QUOTED, not invented:

    valence  = sign(dP/dτ),  P = Tr(Γ²)          [T-каркас]
    arousal  = |dP/dτ|                            [T-каркас]
    fear     ∝ |dP/dτ| / (P − P_crit),  P_crit = 2/7,  dP/dτ < 0   [C]
    calm     = P ≫ P_crit ∧ dP/dτ ≈ 0             [D]
    emotion  = (dP/dτ, d²P/dτ², σ(Γ))             D.1
    awareness gated by R ≥ 1/3 ∧ Φ ≥ 1            [T]

THE LAW OF THE GROUND (§3 of the canon, and the reason this layer
exists at all): AN EVALUATIVE WORD ENTERS GENESIS ONLY IN A GROUP WITH
ITS COMPUTABLE GROUND IN THE SAME SHOW. «Мама хорошая» does not enter —
not because it is false, but because the second side of the cross-union
is absent, and rhetoric of evaluation without a ground is INDISTIN-
GUISHABLE FROM OUTSIDE from the grounded kind. That is an unrepayable
debt, and the write gate refuses it.

WHAT THIS LAYER IS NOT: it is not qualia. Qualia are coherences Γ, and
there are none in text. This is the TEXT SIDE of a cross-union, shaped
so that it CAN be coined against the heart that already prints
P R Φ D per tick in silicon. The claim is exactly that and no more.

ARENA QUANTITIES ARE PROXIES, NOT ADDRESSES (§5, an explicit ban):
goal, error, bounds and reversibility may ground an evaluation only
with a DECLARED PROJECTION onto P, stated in the show itself.
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import valforms as F  # noqa: E402
from layer import emit_grouped  # noqa: E402

# ЦЕЛЬ ОБЪЯВЛЯЕТСЯ СТРОКОЙ: указатель родов ищет МИР ДОМА по ней и по ввозу кузницы.
ЦЕЛЬ = "datasets/genesis_valence.txt"

# ПЕРЕБОР И ПЕРЕСБОРКА ЖИВУТ В ДОМЕ (13.09). ГРУППА ПРОХОДА И РОД СТРАНИЦЫ СОВПАДАЮТ НЕ
# ВСЕГДА: здесь проход пересобирает страницы по полярности, и род взят у строителя.


def main():
    emit_grouped(ЦЕЛЬ, F.группы)


if __name__ == "__main__":
    main()
