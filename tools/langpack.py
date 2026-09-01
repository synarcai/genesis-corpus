#!/usr/bin/env python3
"""LANGPACK: one generic engine, a language as DATA.

The owner's program: GENESIS must own every living
language. The hundredth language must cost ONE pack,
zero engine edits.

A pack carries 32's three first-class fields (his
sufficiency verdict conditions):
  1. morph_classes — inventory of INFLECTION CLASSES,
     each shown on >=LAW DIFFERENT lexemes (one lexeme
     through all cases teaches the lexeme, not the
     class);
  2. show_kinds — kinds of showing (arithmetic /
     definition / narration / ...), each carrying
     lexicon ABSENT from sibling kinds (volume without
     new kinds buys weight, not coverage);
  3. core_pairing — concepts that MUST be shown both
     in this language and in the core, or the bridge
     has nothing to buy.

The engine emits bare shows, varies INSTANCES across
passes (32's knowledge-trail number: the x1 layer
bought +9464 owned types, x22 layers bought zero),
seams with form-feeds, and prints М-95 verdicts
`N of M` for every field before writing a byte.

Usage:
  python3 tools/langpack.py tools/langpacks/ru.json \
      [--core datasets/school_biling_v2c.txt] \
      [--out datasets/genesis_lang_ru.txt]
"""

import argparse
import json
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from segment import tokens  # noqa: E402

LAW = 2  # LAW_OF_REPETITION, mirrored from silicon


def gcd(a, b):
    while b:
        a, b = b, a % b
    return a


def shuffle(items, mult, shift):
    n = len(items)
    if n == 0:
        return []
    step = next(
        k for k in range(mult, mult + n)
        if gcd(k, n) == 1
    )
    return [items[(i * step + shift) % n]
            for i in range(n)]


def judge_morph_classes(pack):
    """Field 1 (32's structure verdict): per-class
    need (classes are incommensurable), full
    paradigm declared, and every class REACHABLE
    from at least one template (verb_past shipped
    zero lines through that hole)."""
    bad = []
    mc = pack.get("morph_classes", {})
    default_need = (
        pack.get("lexeme_source", {})
        .get("need_per_class", LAW)
    )
    tpl_text = " ".join(
        t
        for k in pack.get(
            "show_kinds", {}
        ).values()
        for t in k.get("templates", [])
    )
    for name, cls in mc.items():
        need = cls.get("need", default_need)
        n = len(cls.get("lexemes", {}))
        cells = cls.get(
            "paradigm_cells",
            len(cls.get("forms", [])),
        )
        shown_cells = len(cls.get("forms", []))
        reachable = (
            f"lex:{name}:" in tpl_text
        )
        why = []
        if n < max(LAW, need):
            why.append(
                f"lexemes {n}<{max(LAW, need)}"
            )
        if shown_cells < cells:
            why.append(
                f"cells {shown_cells}/{cells} "
                f"(a sample is not a paradigm)"
            )
        if not reachable:
            why.append(
                "UNREACHABLE from templates"
            )
        if cls.get("plural_by_count") and not (
            cls.get("count_agreement")
            or pack.get("count_agreement")
        ):
            why.append(
                "asks agreement BY COUNT with no "
                "count_agreement declared"
            )
        if why:
            bad.append((name, why))
    print(
        f"LANGPACK-MORPH\t"
        f"{len(mc) - len(bad)} of {len(mc)} "
        f"classes sound"
        + (f"\tpoor={bad}" if bad else "")
    )
    return not bad


def judge_irregulars(pack, body):
    """Field: irregulars are a CLOSED list that
    obeys no class — unshown ones regularize
    («идил»); every one must live >=LAW times in
    the generated body."""
    irr = pack.get("irregulars", [])
    if not irr:
        print(
            "LANGPACK-IRR\tREFUSED\t"
            "no irregulars declared — a real "
            "language always carries some"
        )
        return False
    missing = [
        w for w in irr
        if body.count(w) < LAW
    ]
    print(
        f"LANGPACK-IRR\t"
        f"{len(irr) - len(missing)} of "
        f"{len(irr)} irregulars lived >={LAW}"
        + (f"\tmissing={missing}"
           if missing else "")
    )
    return not missing


def judge_graphemes(pack, body):
    """Field: the script inventory is DECLARED so
    «every grapheme >=LAW» is checkable, not
    observable."""
    inv = pack.get("graphemes", "")
    if not inv:
        print(
            "LANGPACK-GRAPH\tREFUSED\t"
            "no grapheme inventory declared"
        )
        return False
    missing = [
        g for g in inv
        if body.count(g) < LAW
    ]
    print(
        f"LANGPACK-GRAPH\t"
        f"{len(inv) - len(missing)} of "
        f"{len(inv)} graphemes lived >={LAW}"
        + (f"\tmissing={missing}"
           if missing else "")
    )
    return not missing


def judge_refusals(pack, kind_bodies):
    """Refusal kind (32's form): quarantine by
    LEXICON (a marker no other kind carries — the
    disjointness court holds it in), shows go in
    PAIRS with a lawful twin differing by exactly
    one thing (a lone ungrammatical show poisons;
    a pair teaches the BOUNDARY), reasons come
    from a closed list. The one court: no lawful
    twin may coincide with a show of any other
    kind — else one string stands as both norm
    and half a counterexample."""
    ref = [
        (n, k)
        for n, k in pack.get(
            "show_kinds", {}
        ).items()
        if k.get("refusal")
    ]
    if not ref:
        print(
            "LANGPACK-REFUSAL\tREFUSED\t"
            "no refusal kind declared (t6 needs "
            "typed boundaries, not one flat no)"
        )
        return False
    reasons_ok = True
    twin_clash = []
    allowed = {"agreement", "unanswerable",
               "type_mismatch"}
    other_bodies = "\n".join(
        b for n, b in kind_bodies.items()
        if not pack["show_kinds"][n].get(
            "refusal"
        )
    )
    n_pairs = 0
    for name, k in ref:
        for pr in k.get("pairs", []):
            n_pairs += 1
            if pr.get("reason") not in allowed:
                reasons_ok = False
            twin = pr.get("good", "")
            if twin and twin in other_bodies:
                twin_clash.append(twin[:30])
    print(
        f"LANGPACK-REFUSAL\t{n_pairs} pairs, "
        f"reasons_typed={reasons_ok}, "
        f"twin_clashes={len(twin_clash)}"
        + (f"\t{twin_clash[:3]}"
           if twin_clash else "")
    )
    return (n_pairs >= LAW and reasons_ok
            and not twin_clash)


def judge_cross_kind(pack, kind_bodies):
    """Field: a share of lexemes must appear in
    >=2 kinds (in different forms) — a word met
    only in arithmetic is learnt as arithmetic."""
    share = pack.get("cross_kind_share", 0.0)
    mc = pack.get("morph_classes", {})
    all_forms = {}
    for cname, cls in mc.items():
        for lex, forms in cls.get(
            "lexemes", {}
        ).items():
            all_forms[lex] = set(forms)
    crossed = 0
    for lex, forms in all_forms.items():
        kinds_in = sum(
            1
            for body in kind_bodies.values()
            if any(f in body for f in forms)
        )
        if kinds_in >= 2:
            crossed += 1
    total = len(all_forms)
    needed = int(share * total + 0.5)
    print(
        f"LANGPACK-CROSS\t{crossed} of {total} "
        f"lexemes live in >=2 kinds "
        f"(declared share needs {needed})"
    )
    return crossed >= needed


def judge_show_kinds(pack):
    """Field 2: kind lexicons pairwise disjoint."""
    kinds = pack.get("show_kinds", {})
    names = sorted(kinds)
    clashes = []
    for i, a in enumerate(names):
        la = set(kinds[a].get("lexicon", []))
        for b in names[i + 1:]:
            lb = set(kinds[b].get("lexicon", []))
            inter = la & lb
            if inter:
                clashes.append(
                    (a, b, sorted(inter)[:4])
                )
    total = len(names) * (len(names) - 1) // 2
    print(
        f"LANGPACK-KINDS\t"
        f"{total - len(clashes)} of {total} "
        f"kind pairs disjoint"
        + (f"\tclashes={clashes}" if clashes
           else "")
    )
    return not clashes


DO = {
    "+": lambda a, b: a + b,
    "-": lambda a, b: a - b,
    "*": lambda a, b: a * b,
    # an inexact division stated as exact is a
    # FALSE claim, not an unjudgeable one
    "/": lambda a, b: (
        None if b == 0 or a % b else a // b
    ),
}


def arith_lexicon(pack):
    """The engine stays language-blind: the value
    words come from the pack's `numerals`, the
    operators from a kind's declared `ops`. Glyphs
    need no declaration — they are universal."""
    words = {
        str(v).lower(): int(k)
        for k, v in pack.get(
            "numerals", {}
        ).items()
        if str(k).lstrip("-").isdigit()
    }
    ops = {
        "+": "+", "-": "-", "*": "*",
        "\u00d7": "*", "/": "/", "\u00f7": "/",
    }
    eqs = {"="}
    compose = "single"
    for kind in pack.get(
        "show_kinds", {}
    ).values():
        for w, sym in (
            kind.get("ops") or {}
        ).items():
            if sym == "=":
                eqs.add(w.lower())
            else:
                ops[w.lower()] = sym
        compose = kind.get(
            "numeral_compose", compose
        )
    return words, ops, eqs, compose


def judge_arithmetic(pack, kind_bodies):
    """Field 8 (truth): the pair judge counts
    OCCURRENCES, so a word can be bought by a false
    show — «делить» was greened by 40 shows of
    which 40 stated `(n+m)/m = n`. Occurrence is
    not truth, and truth is judged here.

    Lines that carry an equality word but do not
    parse are NAMED, never silently dropped: a
    court that hides its blindness reads as clean.
    The REFUSAL kind is excluded at the source
    rather than counted as blindness — «¬ книга
    плюс дом равно?» states no equality by design,
    and a constant five in `unparsed` would blunt
    the one number that must mean alarm.
    """
    words, ops, eqs, compose = arith_lexicon(pack)
    if not eqs - {"="} and not words:
        print(
            "LANGPACK-ARITH\tREFUSED\t"
            "pack declares no numerals and no "
            "equality word — nothing to judge"
        )
        return False
    true_n = total = unparsed = 0
    false_shows = []
    judged = "\n".join(
        text
        for name, text in kind_bodies.items()
        if not pack["show_kinds"][name].get(
            "refusal"
        )
    )
    # THE THIRD PARSER WITH THE SAME ASSUMPTION. On Chinese this judge
    # read only the glyph template — 50 equalities of 250 — because the
    # worded ones carry no spaces. It cuts by the pack's own vocabulary
    # where the pack declares that discipline.
    spaced = pack.get("segmentation", "by-space") != "longest-match"
    vocab = pack_vocabulary(pack)
    for line in judged.splitlines():
        seq = []
        for tok in tokens(line, vocab, spaced=spaced):
            t = tok.lower()
            if tok.isdigit():
                seq.append(("v", int(tok)))
            elif t in words:
                seq.append(("v", words[t]))
            elif t in ops:
                seq.append(("o", ops[t]))
            elif t in eqs:
                seq.append(("e", 0))
        if not any(k == "e" for k, _ in seq):
            continue
        if compose == "additive":
            merged = []
            for kind, val in seq:
                if (
                    kind == "v"
                    and merged
                    and merged[-1][0] == "v"
                ):
                    merged[-1] = (
                        "v", merged[-1][1] + val
                    )
                else:
                    merged.append((kind, val))
            seq = merged
        if "".join(k for k, _ in seq) != "vovev":
            unparsed += 1
            continue
        a, sym, b, c = (
            seq[0][1], seq[1][1],
            seq[2][1], seq[4][1],
        )
        total += 1
        if DO[sym](a, b) == c:
            true_n += 1
        elif len(false_shows) < 4:
            false_shows.append(line.strip())
    print(
        f"LANGPACK-ARITH\t{true_n} of {total} "
        f"stated equalities true"
        + (
            f"\tunparsed={unparsed}"
            if unparsed else ""
        )
        + (
            f"\tfalse={false_shows}"
            if false_shows else ""
        )
    )
    return true_n == total


def pack_vocabulary(pack):
    """Every word the pack declares — its own dictionary.

    A language that writes without spaces can only be cut by what it
    has said about itself; this gathers exactly that: numerals,
    operator words, and every form of every class.
    """
    words = {str(v) for v in pack.get("numerals", {}).values()}
    for kind in pack.get("show_kinds", {}).values():
        words |= {str(w) for w in (kind.get("ops") or {})}
        words |= {str(w) for w in kind.get("lexicon", [])}
    for cls in pack.get("morph_classes", {}).values():
        for forms in cls.get("lexemes", {}).values():
            words |= {str(f) for f in forms}
    return {w for w in words if w}


def judge_once(pack, body):
    """Field 9: a layer must not utter a word ONCE.

    The law of repetition says one occurrence is chance and two own the
    fact. A word shown a single time therefore costs the corpus weight
    and buys nothing — it is noise with a spelling. The German pack
    showed «dreißig», «einundzwanzig» and «fünfundzwanzig» once each:
    products reachable by exactly one (n, m) pair out of the seeding,
    declared honestly and taught to nobody.

    The judge counts WORDS OF THE LANGUAGE — runs of letters — and
    stays blind to which language that is: the alphabet comes from the
    pack's own `graphemes`, so the hundredth language needs no rule
    here either. Digits and marks are not words and are not counted.
    """
    alphabet = set(pack.get("graphemes", ""))
    if not alphabet:
        print("LANGPACK-ONCE\tREFUSED\tpack declares no graphemes")
        return False
    # THIS JUDGE ASSUMED THE SPACE TOO. On Chinese it glued «一乘一等于
    # 一» into a single «word» and reported 106 of 194 — a number about
    # its own blindness, not about the layer. Where the pack declares
    # its segmentation, the cut is made by the pack's own vocabulary.
    spaced = pack.get("segmentation", "by-space") != "longest-match"
    counts = {}
    for w in tokens(body.lower(), pack_vocabulary(pack), spaced=spaced):
        if any(ch in alphabet for ch in w):
            counts[w] = counts.get(w, 0) + 1
    once = sorted(w for w, k in counts.items() if k < LAW)
    print(
        f"LANGPACK-ONCE\t{len(counts) - len(once)} of "
        f"{len(counts)} words live >={LAW}"
        + (f"\tonce={once[:6]}" if once else "")
    )
    return not once


def judge_core_pairing(pack, core_text, body):
    """Field 3 (32's signature condition): a pair
    has TWO ends — the concept must LIVE on both
    sides in its LIVED form (a one-ended pair is
    not a pair: «делить» was declared and shown
    zero times in the language while the judge
    greened). The verdict names WHAT it counted
    on each side — an honest number under a
    wrong name still lies. Identity pairs are
    controls; at least one pair must hold
    DIFFERENT strings of one concept, or the
    bridge claim is unfalsifiable."""
    pairing = pack.get("core_pairing", [])
    if core_text is None:
        print(
            f"LANGPACK-PAIRING\tREFUSED\t"
            f"no core given, {len(pairing)} "
            f"concepts unjudged"
        )
        return False
    core_missing = []
    lang_missing = []
    non_identity = 0
    for c in pairing:
        cf = c.get("core_form", c["core"])
        lf = c.get(
            "lang_form", c["lang_word"]
        )
        if cf not in core_text:
            core_missing.append(c["core"])
        if lf not in body:
            lang_missing.append(
                c["lang_word"]
            )
        if cf != lf:
            non_identity += 1
    n = len(pairing)
    print(
        f"LANGPACK-PAIRING\t"
        f"core-side {n - len(core_missing)} of "
        f"{n}, lang-side "
        f"{n - len(lang_missing)} of {n}, "
        f"non-identity {non_identity} of {n}"
        + (f"\tcore_missing={core_missing}"
           if core_missing else "")
        + (f"\tlang_missing={lang_missing}"
           if lang_missing else "")
    )
    return (
        not core_missing
        and not lang_missing
        and non_identity >= 1
    )


def instantiate(template, ctx):
    out = template
    for k, v in ctx.items():
        out = out.replace("{" + k + "}", str(v))
    return out


def count_form_index(pack, cls, k):
    """Which paradigm cell a count of `k` selects.

    THE RULE IS DATA. This engine promises in its own docstring that
    the hundredth language costs ONE pack and ZERO engine edits, and
    then carried Russian inside it: 1 / 2-4 / 5+ with the teens
    exception, written in Python. A language whose agreement differed
    could not be added without editing the engine — the promise was
    false for exactly the reason the engine exists.

    A pack declares an ordered list; the first matching rule wins:

        "count_agreement": [
          {"mod": 100, "in": [11, 12, 13, 14], "form": "many"},
          {"mod": 10,  "in": [1],              "form": "one"},
          {"mod": 10,  "in": [2, 3, 4],        "form": "few"},
          {"form": "many"}
        ]

    English declares two rules, Russian four, Arabic as many as its
    duals and paucals need. The engine reads; it does not know.
    """
    forms = cls.get("forms", [])
    rules = (
        cls.get("count_agreement")
        or pack.get("count_agreement")
        or []
    )
    for rule in rules:
        value = k % rule["mod"] if "mod" in rule else k
        if "in" not in rule or value in rule["in"]:
            name = rule["form"]
            if name in forms:
                return forms.index(name)
    return len(forms) - 1


def gen_refusal_kind(kind):
    shows = []
    m = kind.get("marker", "¬ ")
    for pr in kind.get("pairs", []):
        shows.append(m + pr["bad"])
        shows.append(pr["good"])
    return shows


WITHHELD = []


def gen_kind(pack, kind_name, kind, pass_i):
    if kind.get("refusal"):
        return gen_refusal_kind(kind)
    """Bare shows of one kind, instances varied by
    pass. Templates use {n}/{m}/{sum}, {lex:CLS:F}
    (form F of a pass-picked lexeme of class CLS),
    {num:X} (numeral word)."""
    shows = []
    withheld = WITHHELD
    numerals = pack.get("numerals", {})
    mc = pack.get("morph_classes", {})
    for ti, template in enumerate(
        kind.get("templates", [])
    ):
        # A TEMPLATE WITH NOTHING TO VARY HAS ONE INSTANCE.
        # The instance loop exists to vary instances; a constant
        # template ran through it whole and came out as N identical
        # lines — «книга есть у маши. шар есть у юры.» stood forty
        # times where five would have bought it. Repetition beyond
        # the pass discipline buys weight, not facts, and this is
        # where three language layers were losing 10-15% of their
        # lines to it.
        сколько = (
            kind.get("instances_per_pass", 6)
            if "{" in template else 1
        )
        for j in range(сколько):
            seed = (pass_i * 37 + ti * 11 + j * 7)
            n = seed % 9 + 1
            m = seed % 5 + 1
            ctx = {
                "n": n,
                "m": m,
                "sum": n + m,
                "num:n": numerals.get(
                    str(n), str(n)
                ),
                "num:m": numerals.get(
                    str(m), str(m)
                ),
                "num:sum": numerals.get(
                    str(n + m), str(n + m)
                ),
                # a MULTIPLICATIVE pair beside the
                # additive one: without `prod` the
                # only inverse a template could
                # write was `sum`, and a division
                # show over `sum` is false by
                # construction (40 of 40 shipped)
                "prod": n * m,
                "num:prod": numerals.get(
                    str(n * m), str(n * m)
                ),
            }
            for cls_name, cls in mc.items():
                lex = sorted(cls["lexemes"])
                # frequency law: core lexemes
                # show often, tail >= LAW
                tiers = cls.get("tiers", {})
                core_lex = [
                    w for w in lex
                    if tiers.get(w) != "tail"
                ] or lex
                pool = (
                    core_lex
                    if (seed + ti) % 3
                    else lex
                )
                pick = pool[
                    (seed + ti) % len(pool)
                ]
                forms = cls["lexemes"][pick]
                fnames = cls.get(
                    "forms",
                    [str(i) for i in
                     range(len(forms))],
                )
                for fi, fname in enumerate(
                    fnames
                ):
                    ctx[
                        f"lex:{cls_name}:{fname}"
                    ] = forms[fi]
                if cls.get(
                    "plural_by_count"
                ):
                    ctx[
                        f"lex:{cls_name}:by_n"
                    ] = forms[
                        count_form_index(
                            pack, cls, n
                        )
                    ]
                    ctx[
                        f"lex:{cls_name}:by_sum"
                    ] = forms[
                        count_form_index(
                            pack, cls, n + m
                        )
                    ]
            s = instantiate(template, ctx)
            if "{" not in s:
                # A TEACHING LAYER MUST NOT UTTER THE
                # EXAM. The pack declares the questions
                # its language is examined on; a show
                # carrying one would turn the exam into
                # a memory test, and the park's leak
                # court judges exactly that (it caught
                # «тринадцать минус пять равно» here on
                # the day this layer was born).
                # Withheld shows are COUNTED, never
                # dropped in silence.
                if any(
                    r in s
                    for r in pack.get("reserved", [])
                ):
                    withheld.append(s)
                else:
                    shows.append(s)
    return shows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("pack")
    ap.add_argument("--core", default=None)
    ap.add_argument("--out", default=None)
    args = ap.parse_args()
    pack = json.load(
        open(args.pack, encoding="utf-8")
    )
    core_text = (
        open(args.core, encoding="utf-8",
             errors="ignore").read()
        if args.core else None
    )
    ok1 = judge_morph_classes(pack)
    ok2 = judge_show_kinds(pack)

    passes = [(7, 5), (11, 2), (13, 9), (17, 4),
              (19, 12)]
    blocks = []
    n_shows = 0
    kind_bodies = {}
    for pi, (mult, shift) in enumerate(passes):
        for kname, kind in sorted(
            pack.get("show_kinds", {}).items()
        ):
            shows = gen_kind(
                pack, kname, kind, pi
            )
            n_shows += len(shows)
            if shows:
                blk = "\n".join(
                    shuffle(shows, mult, shift)
                )
                blocks.append(blk)
                # A SEPARATOR, NOT A CONCATENATION:
                # blocks carry no trailing newline,
                # so pass i's last line and pass
                # i+1's first line used to be glued
                # into one. The truth court found it
                # by naming its own blindness
                # (unparsed=4 = the four seams of
                # five arithmetic passes).
                prev = kind_bodies.get(kname, "")
                kind_bodies[kname] = (
                    f"{prev}\n{blk}" if prev
                    else blk
                )
    body = "\n\x0c\n".join(blocks) + "\n"
    ok3 = judge_core_pairing(
        pack, core_text, body
    )
    ok4 = judge_irregulars(pack, body)
    ok5 = judge_graphemes(pack, body)
    ok6 = judge_cross_kind(pack, kind_bodies)
    ok7 = judge_refusals(pack, kind_bodies)
    ok8 = judge_arithmetic(pack, kind_bodies)
    ok9 = judge_once(pack, body)
    print(
        f"LANGPACK-RESERVED\t{len(WITHHELD)} shows "
        f"withheld of {len(pack.get('reserved', []))} "
        f"exam questions declared"
    )
    out = args.out or (
        f"datasets/genesis_lang_"
        f"{pack.get('lang', 'xx')}.txt"
    )
    fields = [ok1, ok2, ok3, ok4, ok5,
              ok6, ok7, ok8, ok9]
    green = all(fields)
    # THE DOCSTRING'S OWN LAW, NOW KEPT: judges run
    # "before writing a byte". The body used to be
    # written whatever the verdict, so a red pack
    # still shipped its corpus and the exit code
    # was the only thing that knew.
    if green:
        with open(
            out, "w", encoding="utf-8"
        ) as f:
            f.write(body)
    print(
        f"LANGPACK-OUT\t{out if green else '-'}\t"
        f"{len(body)} bytes\t{n_shows} shows\t"
        f"fields_green={sum(map(int, fields))}"
        f" of {len(fields)}"
        + ("" if green else "\tNOT WRITTEN")
    )
    sys.exit(0 if green else 1)


if __name__ == "__main__":
    main()
