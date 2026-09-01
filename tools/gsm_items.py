#!/usr/bin/env python3
"""THE ITEM LEXICON OF GSM8K — one source, read by every layer.

Two layers needed the same list and would have drifted apart the first
time either was touched, so the list lives here alone.

DERIVED, NOT INVENTED, AND THE DERIVER IS IN THE REPOSITORY:
`tools/gsm_census.py` produces this list from bench/suites and can be
run against it (`--court`). A derived list whose deriver lives in a
scratchpad is a hand-written list wearing the word «measured».

A word earns its place by two independent witnesses — it stands after
a number at least LAW times AND in a NUMBER-FREE question frame — and
is then certified by the `plural` organ. The window between the count
and the thing admits the comparatives and determiners that lawfully
stand there («7 more players»): demanding adjacency measured the
SURFACE, not the role, and cost three true items.

WHAT IS DERIVED BUT NOT SHIPPED IS NAMED, NOT DROPPED. The court
compares the deriver's output against ITEMS plus WITHHELD, so a word
can leave the layer only with a written reason.
"""

ITEMS = [
    "acres", "apples", "apps", "balloons", "balls", "bananas",
    "bandages", "batches", "bolts", "books", "calories", "candies",
    "cards", "cars", "centimeters", "children", "chimichangas",
    "cookies", "crates", "cupcakes", "cups", "days", "degrees",
    "dollars", "eggs", "feet", "flowers", "friends", "gallons", "guns",
    "hours", "inches", "jewels", "kids", "kilograms", "kilometers",
    "lollipops", "marbles", "meals", "miles", "minutes", "newspapers",
    "ounces", "packs", "pages", "paintings", "pairs", "pens", "people",
    "pieces", "players", "points", "pounds", "puppies", "reports",
    "roses", "sandwiches", "seconds", "shells", "signatures", "spoons",
    "stickers", "students", "tablespoons", "teachers", "toys", "vlogs",
    "yards", "years",
]

# Derived by the census, kept OUT of the layers on purpose:
WITHHELD = {
    "fish": (
        "invariant — its singular IS its plural, and a corpus that "
        "certifies agreement by its own use cannot tell the two "
        "apart "
    ),
    "is": (
        "not a noun at all: the organ's -s fallback misfires on it "
        "(«is» -> «i»), and the two witnesses cannot see that "
    ),
    "times": (
        "a multiplier in this benchmark, not a thing counted («3 "
        "times as many»); shipping it would teach a false role "
    ),
}

# ANIMATE ITEMS TAKE DIFFERENT VERBS, AND NO CENSUS CAN SEE IT.
# «how many children do they hold?» and «ida bought 3 friends» are
# grammatical and false about the world — the same class of fault as
# «peter keeps -1 coins», and the same cure: name it, do not guess it.
# Animacy is not derivable from the two witnesses that earn an item its
# place (position after a number, life in a question frame), so it is
# DECLARED here, beside the list it qualifies, and a layer that pastes
# a possession verb onto these words is wrong by construction.
ANIMATE = {
    "children",
    "friends",
    "kids",
    "people",
    "players",
    "puppies",
    "students",
    "teachers",
}
