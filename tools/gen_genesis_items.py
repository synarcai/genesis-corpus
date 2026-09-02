#!/usr/bin/env python3
"""GENESIS layer: THE LIVING ITEM LEXICON OF GSM8K.

The g1 band stood at 0 of 65 with the mechanism alive: the real items
of the benchmark (lollipops, crates, sandwiches, vlogs, tablespoons)
were never bought into the ITEM role, because no layer ever showed
them. A market cannot buy what was never shown.

THE VOCABULARY IS CENSUS-DERIVED, NOT INVENTED. A word earns its place
by TWO independent witnesses in bench/suites/t7_gsm8k_g*.jsonl:
  · it stands after a number at least LAW times, and
  · it stands in a NUMBER-FREE question frame («how many/much X»).
That second witness is the law «the question confirms the item»: a
word that only ever follows a digit is a measure, not a thing. The
`plural` organ then certifies it — an item is a word that HAS a
singular; `of`, `in`, `is`, `were`, `more`, `total` have none and fall
away without a stop-list and without a word of English in this file.

TWO DISCIPLINES, BOTH REQUIRED:
  · the FOUR-PLACE frame [agent verb NUMBER item], twice per item, so
    the episodic algebra has raw material sharing one (agent, item)
    key;
  · NUMBER-FREE life — the same item in sentences carrying no digit at
    all, singular and plural. Without it the item is known only as
    «what follows a number», and the question frame cannot confirm it.

ONE CENSUS WORD IS DELIBERATELY ABSENT, AND THE REASON IS A DEBT,
NOT A DODGE: «fish» is invariant — its singular IS its plural — and a
corpus that must certify agreement BY ITS OWN USE cannot tell the two
apart. scripts/agreement_court.py therefore reads «1 fish» as a
disagreement, and it is right to, given what it can see. Weakening
the court for one word would blind it to the 1700 real faults it was
built for. Invariant nouns need their own show discipline and a court
that can see invariance; until both exist, the word waits, named.

No glyph pairs in-layer (worlds must not mix inside one file); the
count chooses the form through the shared `plural` organ.
"""

from layer import emit


from gsm_items import ANIMATE, ITEMS
import verbthings  # noqa: E402
from plural import by_count, singular

# ИМЕНА, ЧУЖИЕ БЕНЧМАРКУ: агенты не должны совпадать с носителями
# вопросов, иначе слой начнёт узнаваться по имени, а не по роду.
NAMES = ["ida", "omar", "pia", "rosa", "sven",
         "tara", "umar", "vera"]

# Census of bench/suites/t7_gsm8k_g1+g2 (2026-09-01): after a number
# >= LAW times AND inside a number-free «how many/much X» frame, then
# certified by the `plural` organ. 66 items.
# (add-verb pair, ask, answer-verb) — real GSM8K prose verbs
ADD_PAIRS = [("counted", "found"), ("bought", "got")]
SUB_PAIRS = [("packed", "used"), ("picked", "gave")]
# A THING IS BOUGHT AND PACKED; A PERSON IS NOT. «ida bought 3 friends»
# is grammatical and false about the world, so animate items carry
# their own verbs and their own ask — the animacy itself is declared in
# gsm_items, where no census could have found it.
ADD_ANIM = [("counted", "met"), ("greeted", "met")]
SUB_ANIM = [("counted", "missed"), ("greeted", "missed")]
# (add-ask, add-verb, sub-tail, sub-ask, sub-verb)
ASK_THING = ("hold now", "holds", " away", "keep", "keeps")
ASK_ANIM = ("know now", "knows", "", "still know", "knows")
# NUMBER-FREE frames: the item must live where no digit stands
BARE_PLURAL = [
    "{a} likes the {it}.",
    "the {it} are on the table.",
    "what are the {it}?",
]
BARE_SINGULAR = [
    "the {one} is a thing.",
    "{a} looks at the {one}.",
]
# «what are the children?» asks after a thing; «who» asks after a
# person, and a table is not where people are kept.
BARE_PLURAL_ANIM = [
    "{a} likes the {it}.",
    "the {it} are here.",
    "who are the {it}?",
]
BARE_SINGULAR_ANIM = [
    "the {one} is a person.",
    "{a} looks at the {one}.",
]


def pass_shows(pass_i):
    out = []
    for i, it in enumerate(ITEMS):
        seed = pass_i * 31 + i * 7
        a = NAMES[seed % len(NAMES)]
        b = NAMES[(seed + 3) % len(NAMES)]
        one = singular(it)
        n = seed % 8 + 3          # 3..10
        m = seed % 4 + 1          # 1..4
        anim = it in ANIMATE
        add = ADD_ANIM if anim else ADD_PAIRS
        sub = SUB_ANIM if anim else SUB_PAIRS
        q1, a1, tail, q2, a2 = (
            ASK_ANIM if anim else ASK_THING)
        # A VERB TAKES ITS OWN KIND OF THINGS (tools/verbthings.py): the page
        # is per thing, so the PAIR follows the thing — «picked 4 miles» no more.
        add = [п for п in add if all(verbthings.берёт(г, it) for г in п)] or add
        sub = [п for п in sub if all(verbthings.берёт(г, it) for г in п)] or sub
        v1, v2 = add[seed % len(add)]
        s1, s2 = sub[seed % len(sub)]
        out.append(
            f"{a} {v1} {n} {by_count(n, it)}. "
            f"{a} {v2} {m} {by_count(m, it)} more. "
            f"how many {it} does {a} {q1}? "
            f"{a} {a1} {n + m} {by_count(n + m, it)}: {n} + {m} = {n + m}."
        )
        # NOBODY GIVES AWAY MORE THAN THEY HAVE (the heads layer showed
        # «keeps -1 coins» five times before this law was written down)
        gave = min(n, m)
        out.append(
            f"{b} {s1} {n} {by_count(n, it)}. "
            f"{b} {s2} {gave} {by_count(gave, it)}{tail}. "
            f"how many {it} does {b} {q2}? "
            f"{b} {a2} {n - gave} {by_count(n - gave, it)}: {n} − {gave} = {n - gave}."
        )
        for tpl in (BARE_PLURAL_ANIM if anim
                    else BARE_PLURAL):
            out.append(tpl.format(a=a, it=it))
        for tpl in (BARE_SINGULAR_ANIM if anim
                    else BARE_SINGULAR):
            out.append(tpl.format(a=b, one=one))
    return out


def main():
    emit("datasets/genesis_items.txt", pass_shows)


if __name__ == "__main__":
    main()
