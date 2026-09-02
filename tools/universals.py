"""A UNIVERSAL IS ASKED BY ITS OWN «IS IT TRUE THAT» (М-146, М-147; 03.09).

A universal claim — «all odd numbers are prime is false: 9 is odd and
9 = 3 × 3», «every square of an odd number is odd: 3 × 3 = 9» — stood in ten
languages as a statement only, and the width-of-question instrument called
every such frame a debt. Its question is not a second text: it is DERIVED
from the statement by one law, here, for the generators and the courts
alike — the head of the claim is wrapped in the language's «is it true
that», and the verdict word opens the answer: the false universal answers
«no» with its counterexample, the true one «yes» with its instance.

The table below is everything a language contributes: the marker that
closes a false claim, the colon of its writing, the question wrapper and
the two verdict words, and the sign by which the language is told from its
neighbour in a two-language world.
"""
import re

import families

ЯЗЫКИ = {
    #        marker of falsity      colon   question wrapper (prefix, suffix)   yes      no       sign of the language
    "en": (" is false: ",           ": ",   ("is it true that ", "?"),         "yes",   "no",    r" is "),
    "ru": (" — ложь: ",             ": ",   ("верно ли, что ", "?"),           "да",    "нет",   r"[а-яё]"),
    # de, nl: a «dass/dat» clause would move the verb to the end; the claim is
    # quoted after a colon and the question opens with the pack's declared
    # question word («ist», «is» — courts/script_court.py reads the opening).
    "de": (" ist falsch: ",         ": ",   ("ist es wahr: ", "?"),            "ja",    "nein",  r" ist "),
    "fr": (" est faux : ",          " : ",  ("est-il vrai que ", " ?"),        "oui",   "non",   r" est "),
    "es": (" es falso: ",           ": ",   ("¿es cierto que ", "?"),          "sí",    "no",    r" es "),
    "it": (" è falso: ",            ": ",   ("è vero che ", "?"),              "sì",    "no",    r" è "),
    "pl": (" to fałsz: ",           ": ",   ("czy to prawda, że ", "?"),       "tak",   "nie",   r" jest | to |liczb|każd|wszystk"),
    "tr": (" demek yanlıştır: ",    ": ",   ("", " demek doğru mudur?"),       "evet",  "hayır", r"(?:dır|dir|dur|dür|tır|tir|tur|tür)\b|yanlış|demek|sayı"),
    "pt": (" é falso: ",            ": ",   ("é verdade que ", "?"),           "sim",   "não",   r" é "),
    "nl": (" is onwaar: ",          ": ",   ("is het waar: ", "?"),            "ja",    "nee",   r" is "),
}


def язык(строка, кандидаты):
    """Which of the world's languages a claim is written in — by its falsity
    marker first, then by the language's sign; two signs at once or none is
    an error the caller must see, never a guess."""
    for я in кандидаты:
        if ЯЗЫКИ[я][0] in строка:
            return я
    свои = [я for я in кандидаты if re.search(ЯЗЫКИ[я][5], строка)]
    if len(свои) != 1:
        raise ValueError(f"language of «{строка[:60]}» among {кандидаты}: {свои}")
    return свои[0]


def разобрать(строка, кандидаты):
    """(язык, голова, хвост, ложь) — the claim's head, its witness and whether
    the claim was declared false."""
    я = язык(строка, кандидаты)
    ложь, двоеточие = ЯЗЫКИ[я][0], ЯЗЫКИ[я][1]
    if ложь in строка:
        голова, хвост = строка.split(ложь, 1)
        return я, голова, хвост, True
    голова, хвост = строка.split(двоеточие, 1)
    return я, голова, хвост, False


def вопрос(строка, кандидаты):
    """The question of a universal from its statement (a show of the corpus)."""
    я, голова, хвост, ложь = разобрать(строка, кандидаты)
    _, двоеточие, (пред, суф), да, нет = ЯЗЫКИ[я][:5]
    return f"{пред}{голова}{суф} {нет if ложь else да}{двоеточие}{хвост}"


def вопрос_образца(образец, кандидаты):
    """The same law over a court pattern: the head and the tail are regex
    already, the wrapper is escaped as text."""
    assert образец.startswith("^") and образец.endswith("$"), образец[:40]
    я, голова, хвост, ложь = разобрать(образец[1:-1], кандидаты)
    _, двоеточие, (пред, суф), да, нет = ЯЗЫКИ[я][:5]
    return "^" + re.escape(пред) + голова + re.escape(f"{суф} {нет if ложь else да}{двоеточие}") + хвост + "$"


def с_вопросами(строки, кандидаты):
    """The statements of a universal, each followed by its question."""
    вон = []
    for с in строки:
        вон.append(с)
        вон.append(вопрос(с, кандидаты))
    return вон


РОДЫ_УНИВЕРСАЛИЙ = ("_контр", "_общ", "_произведение", "_цифры_на_три")


def универсалия(судья):
    """A court's judge of a universal: the counterexample (контр) and the
    generalization (общ, and the two named ones) — by the court's own names."""
    return судья.__name__.startswith(РОДЫ_УНИВЕРСАЛИЙ)


def правила(образцы, кандидаты):
    """(compiled pattern, judge) pairs for a court: every universal pattern is
    welded with its derived question into ONE family (М-146: the family is the
    genus — the width-of-question instrument sees a genus with a question,
    not a statement without one); the other patterns are compiled as they are."""
    вон = []
    for о, п in образцы:
        if универсалия(п):
            вон.append(families.слить([(о, п), (вопрос_образца(о, кандидаты), п)]))
        else:
            вон.append((re.compile(о), п))
    return tuple(вон)
