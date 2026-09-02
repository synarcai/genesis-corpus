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

# THE «YES» OF A UNIVERSAL IS A BOUNDED CHECK, NEVER AN EXAMPLE ALONE (Т-3 of
# the expressiveness college, holon + omega-f2 03.09): «yes: 84 = 2 × 2 × 3 × 7»
# would teach proving by example; the corpus says what an executor can honestly
# do — «yes: no counterexample among 1..1000; example: 84 = 2 × 2 × 3 × 7» — and
# the court recomputes the bound by the universal's predicate (ПРЕДИКАТЫ), it
# does not believe the word. The bound is one declared number of the house.
ГРАНИЦА = 1000
ОСНОВАНИЕ = {
    "en": "no counterexample among 1..{N}; example: ",
    "ru": "контрпримера среди 1..{N} нет; пример: ",
    "de": "kein Gegenbeispiel unter 1..{N}; Beispiel: ",
    "fr": "aucun contre-exemple parmi 1..{N} ; exemple : ",
    "es": "ningún contraejemplo entre 1..{N}; ejemplo: ",
    "it": "nessun controesempio tra 1..{N}; esempio: ",
    "pl": "brak kontrprzykładu wśród 1..{N}; przykład: ",
    "tr": "1..{N} arasında karşı örnek yok; örnek: ",
    "pt": "nenhum contraexemplo entre 1..{N}; exemplo: ",
    "nl": "geen tegenvoorbeeld onder 1..{N}; voorbeeld: ",
}

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


def основание(я):
    return ОСНОВАНИЕ[я].format(N=ГРАНИЦА)


def вопрос(строка, кандидаты):
    """The question of a universal from its statement (a show of the corpus)."""
    я, голова, хвост, ложь = разобрать(строка, кандидаты)
    _, двоеточие, (пред, суф), да, нет = ЯЗЫКИ[я][:5]
    if ложь:
        return f"{пред}{голова}{суф} {нет}{двоеточие}{хвост}"
    return f"{пред}{голова}{суф} {да}{двоеточие}{основание(я)}{хвост}"


def вопрос_образца(образец, кандидаты):
    """The same law over a court pattern: the head and the tail are regex
    already, the wrapper is escaped as text."""
    assert образец.startswith("^") and образец.endswith("$"), образец[:40]
    я, голова, хвост, ложь = разобрать(образец[1:-1], кандидаты)
    _, двоеточие, (пред, суф), да, нет = ЯЗЫКИ[я][:5]
    if ложь:
        return "^" + re.escape(пред) + голова + re.escape(f"{суф} {нет}{двоеточие}") + хвост + "$"
    return "^" + re.escape(пред) + голова + re.escape(f"{суф} {да}{двоеточие}{основание(я)}") + хвост + "$"


# THE COURT RECOMPUTES THE BOUND: one predicate per universal, keyed by the
# court's judge name (the same names across the ten languages' courts).
def _простое(n):
    return n > 1 and all(n % d for d in range(2, int(n ** 0.5) + 1))


def _разложение_верно(n):
    m, p, произв = n, 2, 1
    while m > 1:
        while m % p == 0:
            произв *= p; m //= p
        p += 1
    return произв == n


def _сумма_цифр(n):
    return sum(int(c) for c in str(n))


ПРЕДИКАТЫ = {
    "_произведение": lambda N: all(_разложение_верно(n) for n in range(2, N + 1)),
    "_цифры_на_три": lambda N: all((n % 3 == 0) == (_сумма_цифр(n) % 3 == 0) for n in range(1, N + 1)),
    "_общ_сумма": lambda N: all(sum(2 * i - 1 for i in range(1, k + 1)) == k * k for k in range(1, N + 1)),
    "_общ_условное": lambda N: all(((e + m) % 2 == 0) == (m % 2 == 0) for e in range(0, N + 1, 2) for m in range(1, N + 1)),
    "_общ_инъекция": lambda N: all(k * 1 != k * 2 for k in range(1, N + 1)),
    "_общ_квадрат": lambda N: all((n * n) % 2 == n % 2 for n in range(1, N + 1)),
}
_ПРОВЕРЕНО = {}


def граница_верна(судья):
    """«No counterexample among 1..N» holds for this universal — computed once
    by its predicate; a universal without a predicate cannot claim it."""
    for имя, предикат in ПРЕДИКАТЫ.items():
        if судья.__name__.startswith(имя):
            if имя not in _ПРОВЕРЕНО:
                _ПРОВЕРЕНО[имя] = bool(предикат(ГРАНИЦА))
            return _ПРОВЕРЕНО[имя]
    raise KeyError(f"no predicate for the universal judged by {судья.__name__}")


def с_границей(судья):
    """The judge of the «yes» question: the instance as before AND the bound."""
    def судить(м):
        return bool(судья(м)) and граница_верна(судья)
    судить.__name__ = судья.__name__
    return судить


def вопросные_формы(формы, кандидаты):
    """[(question pattern, judge)] derived from the statement forms of a
    universal: the «no» keeps its judge, the «yes» gets the bound."""
    вон = []
    for о, п in формы:
        ложь = any(ЯЗЫКИ[я][0] in о for я in кандидаты)
        вон.append((вопрос_образца(о, кандидаты), п if ложь else с_границей(п)))
    return вон


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
            вон.append(families.слить([(о, п)] + вопросные_формы([(о, п)], кандидаты)))
        else:
            вон.append((re.compile(о), п))
    return tuple(вон)
