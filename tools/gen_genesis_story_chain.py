#!/usr/bin/env python3
"""GENESIS layer: THE THREE-PART CHAIN — one bearer, one thing, three verbs.

A market law is bought only INSIDE ONE EPISODE. Two shows saying «Tom
picked 12 apples» and «Tom keeps 7 apples» do not compose into the law
«keeps = picked − gave», because nothing in either says they are the
same episode. The law lives in the SHOW, or it does not live.

    Tom picked 12 apples and gave away 5; Tom keeps 7 apples.
    Том взял 12 яблок и отдал 5; у Тома осталось 7 яблок.

THREE VERBS, NOT TWO, AND ALL THREE DIFFERENT. Two verbs give a
difference; three give a LAW with a name for its result — «keeps»,
«holds», «has left». The third verb is what makes the episode close.

THE THIRD FACT CARRIES ITS BEARER EXPLICITLY. «Tom keeps 7 apples», not
«7 apples remain»: the agentless form belongs to another genus, and a
market frame mixing the two buys neither. This is not style — it is the
difference between a fact about Tom and a fact about apples.

BOTH POLARITIES OF THE OUTCOME. Taking away and adding are not one law
said twice: «picked, gave, keeps» subtracts; «had, found, holds» adds.
A corpus showing only subtraction teaches that episodes shrink.

NUMBERS STAY SMALL AND WHOLE (≤ 50 for every member, including the
result), because the law is checked through the school table of links,
and a rare large number lies outside that table and gives no vote —
it would be shown, not learned.
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import story_chainforms as F  # noqa: E402
from layer import emit_grouped  # noqa: E402

ЦЕЛЬ = "datasets/genesis_story_chain.txt"


def main():
    emit_grouped(ЦЕЛЬ, F.группы)


if __name__ == "__main__":
    main()
