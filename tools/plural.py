#!/usr/bin/env python3
"""THE COUNT CHOOSES THE FORM — and the forms live in the language pack.

The English layers of GENESIS showed «1 eggs» 1700 times and «1 egg»
not once, so by the law of repetition the organism owned the WRONG
agreement and never met the right one. The fault was uniform across
six generators: each carried a flat list of PLURAL items and pasted it
after any count.

THE FORMS ARE DATA, NOT A RULE, because a rule guesses wrong on this
very vocabulary: «calories» is «calorie», yet the common -ies→-y rule
yields «calory», and «people»/«feet» obey nothing at all. A guessed
form is a lie shown twice, which is exactly what is owned.

AND THEY LIVE IN `tools/langpacks/en.json`, NOT HERE. They were kept in
this file while the same facts also stood in the pack's noun classes —
two homes for one fact, and the two had already begun to part: the
pack knew «mice» and «leaves», this organ did not. A fact of English
belongs to the description of English; this module is the ORGAN that
applies it, and it reads what the pack declares.

The -s fallback stands for words the map does not name, and it is not
trusted: scripts/agreement_court.py judges the WRITTEN corpus with no
knowledge of English at all — deliberately not through this organ — so
a wrong fallback is caught in the text rather than believed in code.
"""

import json
import pathlib

PACK = (pathlib.Path(__file__).resolve().parent
        / "langpacks/en.json")


def _load():
    """plural -> singular, read from the pack, checked against it.

    The pack's morph classes state the same pairs a second time (a
    class is a paradigm, and this is its flat index). They are asserted
    equal here rather than trusted: one file, two readings, and a
    silent disagreement between them would put a false form in a corpus
    nobody re-reads.
    """
    pack = json.loads(PACK.read_text(encoding="utf-8"))
    forms = pack.get("noun_forms", {})
    single = {plural: one for one, plural in forms.items()}
    for name in ("noun_count", "noun_irreg"):
        cls = pack.get("morph_classes", {}).get(name, {})
        for one, plural in cls.get("lexemes", {}).values():
            if forms.get(one) != plural:
                raise ValueError(
                    f"{PACK.name}: class {name} says "
                    f"{one}->{plural}, noun_forms says "
                    f"{one}->{forms.get(one)}"
                )
    return single


SINGULAR = _load()


def singular(plural):
    """The named form, else the -s fallback (never a cleverer guess)."""
    if plural in SINGULAR:
        return SINGULAR[plural]
    if plural.endswith("es") and plural[:-2].endswith(
        ("s", "x", "z", "ch", "sh")
    ):
        return plural[:-2]
    return plural[:-1] if plural.endswith("s") else plural


def by_count(n, plural):
    """The form a count of `n` takes. One is singular; all else plural
    — including zero, which English counts as plural («0 eggs»)."""
    return singular(plural) if abs(n) == 1 else plural
