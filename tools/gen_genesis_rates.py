#!/usr/bin/env python3
"""GENESIS layer: RATE, MONEY AND TIME — the bridge a word problem walks.

A band of thirty questions died on one bridge. «Gerald earns 30 dollars
every day; how much in a week?» needs FOUR things at once, and the corpus
carried each of them apart and none of them together:

    СТАВКА     — «30 dollars EVERY day» ties a money unit to a time unit;
                 the pair (dollars, day) must be LIVED, not merely stated;
    ЧИСЛОФОРМА — «a week has 7 DAYS» but «7 days make a WEEK»: singular and
                 plural of the SAME unit on the SAME numbers, side by side.
                 This is where the band actually stopped: the organism knew
                 «day» and knew «days» and did not know they are one word;
    ПЕРЕВОД    — hour↔minute, day↔hour, week↔day, dollar↔cent, walked as a
                 relation and not memorised as a pair;
    ГЛАГОЛ ДЕНЕГ — cost / spend / have left, with the polarity that spending
                 SUBTRACTS; and «X and Y cost N» — a sum said by a verb.

ONE FACT, THREE SURFACES, SAME NUMBERS. The rate, the total and the question
stand together on one triple of numbers, in English and in Russian, because
the bridge is crossed by seeing the same numbers wear three clothes.

RUSSIAN PAYS ITS OWN PRICE, AND IT IS PAID HERE. «сколько минут в двух
часах?» needs the numeral in an oblique form («двух», declared by the pack)
AND the noun in the prepositional plural («часах»), which no house carried:
counting triples are AGREEMENT under a number, not case. The prepositional
plural is now DERIVED from the declared paradigm (`rugram.предложный_мн`),
and the question can finally be asked in Russian at all.

EVERY RELATION IS WALKED, NOT WRITTEN: `units.отношение` finds the factor
through the declared graph, and the court walks it again.
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import ratesforms as F  # noqa: E402
from layer import emit_grouped  # noqa: E402

ЦЕЛЬ = "datasets/genesis_rates.txt"


def main():
    emit_grouped(ЦЕЛЬ, F.группы_страниц)


if __name__ == "__main__":
    main()
