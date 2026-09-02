"""A PARAPHRASE IS A SECOND DECLARED FORM OF THE GENUS (Т-4 of the
expressiveness college, 03.09; М-146).

«What's 47 + 38?», «compute 47 + 38» were silent: the frame's rigidity is the
transformer's main advantage over the organism, and the market of frame
equivalence needs a falsifier — two formulations of one question over the
same pair (numbers → answer). The second formulation is not a synonym list
of a generator: it is a form of the language pack (`ask_forms` of
langpacks/<lang>.json, one list per genus, «{}» a hole for a number), and
this house turns the pack's forms into shows and into court patterns by one
law. The mass of the pair is not divided — every form carries the whole
pair (rule 2 of М-148).

    формы(язык, род)              → the pack's forms of the genus
    перефразы(строки, языки, роды) → shows + their paraphrases
    образцы(образцы, языки, роды)  → court patterns of the other forms
"""
import json
import pathlib
import re

ЯЗЫКОВЫЕ = pathlib.Path(__file__).resolve().parent / "langpacks"
ДЫРА = "{}"
ЧИСЛО = r"(\d+)"
_ПАКЕТЫ = {}


def формы(язык, род):
    """The declared question forms of a genus in a language (may be empty)."""
    if язык not in _ПАКЕТЫ:
        _ПАКЕТЫ[язык] = json.loads((ЯЗЫКОВЫЕ / f"{язык}.json").read_text(encoding="utf-8"))
    return list(_ПАКЕТЫ[язык].get("ask_forms", {}).get(род, ()))


def образец(форма):
    """The regex text of a form: the text escaped, every hole a number.

    Spaces, hyphens and apostrophes are left as they are: the courts write
    them raw in their patterns, and the first form must be found there as
    a prefix, character for character."""
    def чисто(ч):
        return re.escape(ч).replace("\\ ", " ").replace("\\-", "-").replace("\\'", "'")
    return ЧИСЛО.join(чисто(ч) for ч in форма.split(ДЫРА))


def перефразы(строки, языки, роды):
    """Every show whose question is the FIRST form of a genus is followed by
    the same answer under the other forms of the pack."""
    правила = []
    for язык in языки:
        for род in роды:
            ф = формы(язык, род)
            if len(ф) > 1:
                правила.append((re.compile("^" + образец(ф[0]) + " (.*)$"), ф[1:]))
    вон = []
    for с in строки:
        вон.append(с)
        for первая, другие in правила:
            m = первая.match(с)
            if m:
                числа, ответ = m.groups()[:-1], m.groups()[-1]
                for форма in другие:
                    вон.append(форма.format(*числа) + " " + ответ)
                break
    return вон


def образцы(образцы_, языки, роды):
    """Court patterns for the other forms: a pattern of the first form,
    «^<form0> <answer>$», yields «^<form_k> <answer>$» with the same judge."""
    вон = []
    for язык in языки:
        for род in роды:
            ф = формы(язык, род)
            if len(ф) < 2:
                continue
            голова = "^" + образец(ф[0]) + " "
            for о, п in образцы_:
                if о.startswith(голова):
                    ответ = о[len(голова):]
                    for форма in ф[1:]:
                        вон.append(("^" + образец(форма) + " " + ответ, п))
    return вон
