#!/usr/bin/env python3
"""WHERE ONE WORD ENDS AND THE NEXT BEGINS — declared, not assumed.

Every parser in the park assumed the space. On «三加二等于五。» the
language census and the arithmetic court both saw ONE token — the whole
sentence — and so could judge nothing at all. The rest of the
architecture was already blind to script (a pack declares its writing
system, its range, its probe, its agreement rule), and this was the one
place where an alphabet was still presumed.

THE SEGMENTER READS WHAT THE LANGUAGE DECLARED ABOUT ITSELF. A pack
carries its numerals, its operator words and the forms of its classes;
those ARE its vocabulary, and the segmenter cuts by LONGEST MATCH over
exactly them, falling back to a single character. A word the pack never
declared is not invented here — it is left as characters, and whatever
judges the line will simply not judge what it cannot read. That is the
honest failure: silence, not a guess.

Scripts that write without spaces are named by the pack
(`"segmentation": "longest-match"`); everything else keeps the space,
because for a space-writing language the space IS the declaration.
"""

import re

SPACED = re.compile(r"\d+|[^\W\d_]+|[+\-*/×÷=−⋅]")
GLYPHS = set("+-*/×÷=−⋅")


def spaced_tokens(text):
    """Runs of letters, runs of digits, and operator glyphs."""
    return SPACED.findall(text)


def matched_tokens(text, vocabulary):
    """Longest declared word wins; anything else is one character.

    Digits keep their runs — a numeral written with figures is one
    value in every script — and declared words are tried longest
    first, so «等于» is one token and not «等» plus «于».
    """
    if not vocabulary:
        return spaced_tokens(text)
    longest = max(len(w) for w in vocabulary)
    out, i, n = [], 0, len(text)
    while i < n:
        ch = text[i]
        if ch.isdigit() and ch.isascii():
            j = i
            while j < n and text[j].isdigit() and text[j].isascii():
                j += 1
            out.append(text[i:j])
            i = j
            continue
        if ch in GLYPHS:
            out.append(ch)
            i += 1
            continue
        if ch.isspace():
            i += 1
            continue
        взято = None
        for length in range(min(longest, n - i), 0, -1):
            кусок = text[i:i + length]
            if кусок in vocabulary:
                взято = кусок
                break
        if взято:
            out.append(взято)
            i += len(взято)
        elif ch.isalpha():
            out.append(ch)
            i += 1
        else:
            i += 1
    return out


def tokens(text, vocabulary=(), spaced=True):
    """The one entry point: the caller says which discipline applies."""
    return (spaced_tokens(text) if spaced
            else matched_tokens(text, set(vocabulary)))
