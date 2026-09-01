#!/usr/bin/env python3
"""THE DERIVER OF THE GSM8K ITEM LEXICON — so the list can be re-derived.

`tools/gsm_items.py` carries the item vocabulary of the benchmark and
said «census of 2026-09-01» while the census itself lived in a
scratchpad. DERIVED DATA WHOSE DERIVER IS NOT IN THE REPOSITORY CANNOT
BE RE-DERIVED: it becomes a hand-written list wearing the word
«measured». This file is that deriver, and it can check the list it
produced.

    python3 tools/gsm_census.py            # print the list
    python3 tools/gsm_census.py --court    # compare with gsm_items

TWO INDEPENDENT WITNESSES, then certification:
  · the word stands after a number at least LAW times;
  · the word stands in a NUMBER-FREE question frame («how many/much X»)
    — the law «the question confirms the item»: a word living only
    after a digit is a measure, not a thing;
  · the `plural` organ certifies it — an item is a word that HAS a
    singular, so «of», «in», «is», «were», «more», «total» fall away
    with no stop-list and no English in this file.

THE WINDOW IS NOT ADJACENCY, AND THIS WAS A DEFECT FOUND BY e9.
The first census demanded the item stand IMMEDIATELY after the number
and so measured the SURFACE, not the role: «zeke's team has 7 more
players than carlton» is a lawful comparative in which one word stands
between the count and the thing counted. Three items were lost to it —
players, jewels, spoons — and «players» is the very word the g1.47
form needs. The window now admits the words that legitimately come
between; it does not admit any word, because the two witnesses and the
organ still have to agree.
"""

import collections
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
from plural import SINGULAR, singular  # noqa: E402

LAW = 2  # LAW_OF_REPETITION, mirrored from silicon by lang_census
SUITES = ("t7_gsm8k_g1", "t7_gsm8k_g2")
# THE WORDS THAT MAY STAND BETWEEN A COUNT AND ITS THING: comparatives
# and determiners, and nothing else. Declared, so the window is a claim
# about English that can be argued with, not a regex nobody reads.
BETWEEN = ("more", "fewer", "other", "new", "different", "additional")
AFTER = re.compile(
    r"\b\d[\d,.]*\s+(?:(?:" + "|".join(BETWEEN) + r")\s+)?([a-z]+)"
)
ASKED = re.compile(r"how (?:many|much) ([a-z]+)")


def _suite(name):
    """Набор бенчмарка: свой, затем объявленный внешний корень.

    Наборы принадлежат архитектуре, а не корпусу. ОТСУТСТВИЕ ИСТОЧНИКА
    ЕСТЬ ОТКАЗ, А НЕ КРАХ (М-88): прежняя редакция падала трассой, и
    краткая смерть читается как находка.
    """
    свой = ROOT / f"bench/suites/{name}.jsonl"
    if свой.is_file():
        return свой
    from genesis import external_root
    чужой = external_root() / f"bench/suites/{name}.jsonl"
    return чужой if чужой.is_file() else None


def census():
    after, asked = collections.Counter(), collections.Counter()
    for name in SUITES:
        path = _suite(name)
        if path is None:
            print(f"GSM-CENSUS ОТКАЗ: набор {name} не найден ни в "
                  f"репозитории, ни по внешнему корню", file=sys.stderr)
            sys.exit(2)
        for line in path.read_text(encoding="utf-8").splitlines():
            if line.startswith("#"):
                continue
            try:
                text = json.loads(line)["ask"].lower()
            except (ValueError, KeyError):
                continue
            for w in AFTER.findall(text):
                after[w] += 1
            for w in ASKED.findall(text):
                asked[w] += 1
    return sorted(
        w for w in after
        if after[w] >= LAW and w in asked
        and (w in SINGULAR or singular(w) != w)
    )


def main():
    derived = census()
    if "--court" not in sys.argv:
        for w in derived:
            print(w)
        print(f"GSM-CENSUS ЛЕНТА: {len(derived)} предметов "
              f"(окно через {len(BETWEEN)} слов, кворум {LAW})", file=sys.stderr)
        return 0
    from gsm_items import ITEMS, WITHHELD
    shipped = set(ITEMS) | set(WITHHELD)
    lost = sorted(set(derived) - shipped)
    extra = sorted(shipped - set(derived))
    print(
        f"GSM-CENSUS {'PASS' if not (lost or extra) else 'FAIL'}: "
        f"{len(lost) + len(extra)} расхождений "
        f"({len(derived)} выведено, {len(ITEMS)} в слое, "
        f"{len(WITHHELD)} удержано)"
        + (f"\n  выведено, но не в слое: {lost}" if lost else "")
        + (f"\n  в слое, но не выведено: {extra}" if extra else "")
    )
    return 0 if not (lost or extra) else 1


if __name__ == "__main__":
    sys.exit(main())
