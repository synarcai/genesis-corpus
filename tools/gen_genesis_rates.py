#!/usr/bin/env python3
"""GENESIS layer: TEMPORAL UNFOLDINGS (genus 8).

A rate is a fact of a PAIR (item, period) with the value carried
impersonally — holon's rate roads read `rate_facts = (item, unit,
rate)` and take no agent into the link; the agent belongs to the
episode, not to the rate. The target line shape is his, given as fact
rather than guess:

    5 × 4 = 20.
    ida walks 5 miles every day. how much in 4 days?
    ida walks 20 miles in 4 days.

THREE THINGS THE SHAPE INSISTS ON, EACH FOR A REASON:
  · the GLYPH AXIS rides in-layer as the weld — the road buys the
    multiplication from it, and without the weld the prose line has
    nothing to be checked against;
  · the question frame carries a SHOWN ANSWER. «how much in 4 days?»
    with no answer is not a frame at all, and the road cannot read it;
  · NO DIVISION IS SHOWN. The road reads the inverse by inference
    (total ÷ K through the OR-6 inversion over a bought ×). A division
    show is not merely unnecessary here but harmful — the langpack
    shipped 40 division shows of which 40 were false, because the
    machinery had no product to write them over.

VERB AND UNIT ARE DECLARED TOGETHER. A rate joins a doing to a thing,
and no census can tell which pairs are true of the world: «ida walks 5
teachers every day» would be grammatical and false, the same fault as
«own 5 teachers» and «keeps -1 coins». So the pairs are named, and the
units are the census lexicon of the benchmark (tools/gsm_items.py).
"""

from layer import emit


from gsm_items import PACKAGEABLE
from gsm_items import ITEMS as CENSUS
from plural import by_count, singular

NAMES = ["ida", "omar", "pia", "rosa", "sven",
         "tara", "umar", "vera"]
# (verb, units it truly takes) — the pairing is the declaration
DOINGS = [
    ("walks", ["miles", "kilometers"]),
    ("runs", ["miles", "yards"]),
    ("writes", ["pages", "reports"]),
    ("reads", ["pages", "books", "newspapers"]),
    ("bakes", ["cookies", "cupcakes", "batches"]),
    ("earns", ["dollars"]),
    ("saves", ["dollars", "pounds"]),
    ("packs", ["crates", "bandages", "cards"]),
    ("collects", ["shells", "stickers", "cards", "marbles"]),
    ("drinks", ["cups", "gallons", "ounces"]),
    ("eats", ["calories", "eggs", "sandwiches", "meals"]),
    ("plants", ["roses", "flowers"]),
]
# (period phrase, its plural for the span) — four surfaces of one genus
PERIODS = [("every day", "days"), ("every night", "nights"),
           ("each day", "days"), ("a day", "days")]
# (container, its plural) — упаковка как второй род ставки
CONTAINERS = [("pack", "packs"), ("box", "boxes"), ("crate", "crates"),
              ("batch", "batches")]
# THE PERIOD MUST LIVE WHERE NO DIGIT STANDS, or it is known only as
# «the word after a number» and the question frame cannot confirm it.
BARE = [
    "the {one} is a period.",
    "{a} waits for the {one}.",
    "what is a {one}?",
]


def pass_shows(pass_i):
    out = []
    unknown = [u for _, us in DOINGS for u in us if u not in CENSUS]
    assert not unknown, unknown
    i = 0
    for verb, units in DOINGS:
        for unit in units:
            seed = pass_i * 29 + i * 11
            i += 1
            a = NAMES[seed % len(NAMES)]
            rate = seed % 6 + 1          # 1..6
            k = seed % 8 + 2             # 2..9
            span, plural_span = PERIODS[seed % len(PERIODS)]
            total = rate * k
            out.append(f"{rate} × {k} = {total}.")
            out.append(
                f"{a} {verb} {rate} {by_count(rate, unit)} {span}. "
                f"how much in {k} {plural_span}? "
                f"{a} {verb} {total} {by_count(total, unit)} "
                f"in {k} {plural_span}."
            )
    # ВТОРОЙ РОД СТАВКИ: НЕ ПЕРИОД, А УПАКОВКА. Бенчмарк пишет «razors
    # come 4 to a pack» и «popsicles come 8 to a box» — это ставка между
    # ПРЕДМЕТОМ и ВМЕСТИЛИЩЕМ, той же формы, что ставка во времени, но с
    # иным вторым носителем. Перепись назвала глагол «come» стоящим
    # перед числом, и соблазн был велик добавить его четырёхместным —
    # но «ida comes 4 packs» ложно о мире (М-103): приходит не агент,
    # а товар, и приходит УПАКОВКОЙ.
    for j, (one, many) in enumerate(CONTAINERS):
        товары = sorted(PACKAGEABLE)
        unit = товары[(pass_i * 11 + j * 7) % len(товары)]
        rate = (pass_i + j) % 6 + 2          # 2..7
        k = (pass_i * 3 + j) % 5 + 2         # 2..6
        out.append(
            f"{unit} come {rate} to a {one}. "
            f"how many {unit} in {k} {many}? "
            f"{k} {many} hold {rate * k} {unit}."
        )
        out.append(f"a {one} holds {rate} {unit}.")
        out.append(f"the {one} is a container.")
        out.append(f"what is a {one}?")
    # THE PERIOD'S NUMBER-FREE LIFE IS EMITTED ONCE PER PASS, over
    # every distinct period word. Emitting it inside the verb loop
    # repeated one period and starved another — coverage by accident
    # instead of by construction.
    for j, one in enumerate(sorted(
        {singular(pl) for _, pl in PERIODS}
    )):
        for tpl in BARE:
            out.append(tpl.format(
                a=NAMES[(pass_i + j) % len(NAMES)], one=one,
            ))
    return out


def main():
    emit("datasets/genesis_rates.txt", pass_shows)


if __name__ == "__main__":
    main()
