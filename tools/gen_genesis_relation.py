#!/usr/bin/env python3
"""GENESIS layer: RELATION — the metalanguage of structure, at a structure.

A corpus can name numbers, words and formulas and still be unable to say
what CONTAINS what, what CORRESPONDS to what, what is EQUIVALENT to what
and what STANDS at which level. Measured from outside: the tables of
contents of seven prose corpora name «связь» 169 times, «структура» 115,
«hierarchy» 47, «closure» 28, «correspondence»/«соответствие» 24 — and
not one of those words was shown by a single show. Prose is unreadable
without them.

THE LAW OF THIS WORLD: A WORD SHOWN WITHOUT CHECKABLE CONTENT IS A
LABEL. Every relation here stands at a REAL structure which the court
WALKS AND RECOUNTS — a declared tree of eighteen nodes, seven relations
on four numbers, remainder classes on twelve numbers, the divisibility
order on the divisors of twelve, a directed graph of seven nodes. Not a
single answer is written down; every one is walked out. «Transitive» is
either a triple that closes or a triple that does not, and the show says
WHICH triple.

BOTH LANGUAGES CARRY EVERY KIND. «hierarchy», «relation», «transitive»,
«equivalence», «class», «correspondence», «order», «path», «level»,
«closure» are missing from the corpus exactly as their Russian twins
are, and a world that showed structure in one language only would have
taught that structure is a property of English.

WHAT A SHOW OWES BESIDES ITS ANSWER — THE VIOLATOR. Every property is
shown twice: with a case that confirms it and with a case that breaks
it, and the breaking case NAMES ITS WITNESS («1 stands to 2 and 2
stands to 3, but 1 does not stand to 3»). A corpus that only shows
relations that ARE transitive teaches that all relations are; a corpus
that only shows paths that exist teaches that a path always exists.
Refusals here are first-class and carry their ground: no such edge, no
path at all, no greatest element, not one-to-one.

THE ORACLE IS TWO OPPOSITE WALKS, ONE PAIR PER KIND — level counted up
against depth counted down, a witness against set algebra, remainder
buckets against connected pieces, the order rule against reachability
over covers, a walk forward against a walk backward. Nothing is written
here to be compared with itself.
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import relation as о  # noqa: E402 — оракул встречных ходов
import relforms as F  # noqa: E402
from layer import emit_grouped  # noqa: E402

# ЦЕЛЬ ОБЪЯВЛЯЕТСЯ СТРОКОЙ: её читают и указатель родов, и мера воспроизводимости.
ЦЕЛЬ = "datasets/genesis_relation.txt"

# ОРАКУЛ ОСТАЁТСЯ ЗДЕСЬ: ворота перед письмом суть дело кузницы, а не закон страницы.


def main():
    беды = о.оракул()
    if беды:
        print(f"СТРОЕНИЕ ОТКАЗ: {len(беды)} расхождений на встречных "
              f"ходах — слой не собран: {беды[:2]}")
        return 2
    emit_grouped(ЦЕЛЬ, F.группы)
    return 0


if __name__ == "__main__":
    sys.exit(main())
