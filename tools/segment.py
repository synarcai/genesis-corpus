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

BARE_WORD = r"[^\W\d_]+"
SPACED = re.compile(r"\d+|" + BARE_WORD + r"|[+\-*/×÷=−⋅]")
GLYPHS = set("+-*/×÷=−⋅")


БУКВА = r"[^\W\d_]"


def внутрисловные(словарь):
    r"""Знаки, стоящие ВНУТРИ объявленных слов, — ВЫВЕДЕНЫ, не объявлены.

    Украинское «п'ятнадцять» — одно слово, и апостроф в нём не граница,
    а буква по должности: суд пласта, резавший по [^\W\d_]+, видел «п»
    и «ятнадцять» и звал второе необъявленным. Тот же знак живёт во
    французском «l'homme», в английском «don't», в каталонском «l·l»,
    в хорватском и в турецком «Ali'nin» — и ни один из этих случаев не
    должен стоить нового поля в пакете.

    ЗНАК, ЖИВУЩИЙ МЕЖДУ ДВУМЯ БУКВАМИ ОБЪЯВЛЕННОГО СЛОВА, ТЕМ САМЫМ
    ОБЪЯВЛЕН. Пакет уже сказал всё, что нужно, назвав свои слова;
    прибору остаётся прочесть сказанное, а не спросить ещё раз. Это тот
    же род, что и разбиение письма без пробелов: письмо есть свойство
    языка, и язык о нём УЖЕ высказался — словарём.
    """
    знаки = set()
    for слово in словарь:
        for i, ch in enumerate(слово[1:-1], 1):
            if not (ch.isalnum() or ch == "_") and not ch.isspace():
                до, после = слово[i - 1], слово[i + 1]
                if до.isalpha() and после.isalpha():
                    знаки.add(ch)
    return знаки


def word_re(словарь=()):
    """Образец СЛОВА этого письма: буквы со знаками, живущими внутри.

    Без словаря — старое правило (одни буквы), ибо без объявления
    внутрисловных знаков нет.
    """
    знаки = внутрисловные(словарь)
    if not знаки:
        return re.compile(BARE_WORD, re.UNICODE)
    класс = "[" + "".join(re.escape(з) for з in sorted(знаки)) + "]"
    return re.compile(f"{BARE_WORD}(?:{класс}{BARE_WORD})*", re.UNICODE)


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
