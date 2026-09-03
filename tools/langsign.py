#!/usr/bin/env python3
"""THE SIGN OF THE LANGUAGE — which pack's function words a line carries.

A court of one language must not judge a line of another: the English count
court read German «2 mal 3 hat die Fläche» as «3 hat» → «hats», Dutch «310
cent» as a missing «s». The packs declare their FUNCTION WORDS (articles,
copulas, conjunctions, question words); the language of a line is the pack
whose function words it carries most, and no language when no pack leads —
a line of bare numbers, or a tie («is» is English and Dutch alike). Courts
of one language ask this house before judging.
"""
import json
import pathlib
import re

ПАКЕТЫ = pathlib.Path(__file__).resolve().parent / "langpacks"
СЛОВО = re.compile(r"[^\W\d_]+(?:'[^\W\d_]+)?")


def _слова():
    вон = {}
    for путь in sorted(ПАКЕТЫ.glob("*.json")):
        try:
            пакет = json.loads(путь.read_text(encoding="utf-8"))
        except ValueError:
            continue
        слова = пакет.get("function_words")
        if isinstance(слова, list) and слова:
            # the tails of contractions («'s», «'ve») never stand alone — not signs
            хвосты = {w.lower() for w in (пакет.get("contraction_tails") or ())}
            вон[путь.stem] = frozenset(w.lower() for w in слова if w.lower() not in хвосты)
    return вон


def _заполнители():
    """The declared fillers of the houses of phrases — unit names, things,
    days, share names — are signs of their language too (04.09: «2 kilometer
    is 2000 meter» carries one function word, «is», which English shares;
    the units say Dutch). English signs are the BRITISH unit spellings of the
    house of units (metre, kilometre) and the pack's nouns; the American
    «meter/kilometer» would tie with Dutch."""
    вон = {}
    def _в(язык, x):
        if isinstance(x, str):
            if x and x not in ("m", "f", "n"):
                вон.setdefault(язык, set()).add(x.lower())
        elif isinstance(x, (list, tuple)):
            for y in x:
                _в(язык, y)
        elif isinstance(x, dict):
            for y in x.values():
                _в(язык, y)
    try:
        import holes, calforms, cmpforms, unitforms, physforms, shareforms, moneyforms, units, rugram, searchforms, moneystory
    except Exception:
        return вон
    for язык, дни in holes.ДНИ.items():
        _в(язык, дни)
    for язык, рамки in holes.РАМКИ.items():
        for р in рамки:
            _в(язык, р.get("места")); _в(язык, р.get("вещи"))
    for язык, я in calforms.ЯЗЫКИ.items():
        _в(язык, я.get("дни")); _в(язык, я.get("косв"))
    for дом in (cmpforms.ВЕЩИ, unitforms.ЕДИНИЦЫ, physforms.ЕДИНИЦЫ, shareforms.ИМЕНА):
        for язык, x in дом.items():
            _в(язык, x)
    for язык, я in moneyforms.ЯЗЫКИ.items():
        _в(язык, я.get("б")); _в(язык, я.get("м"))
    # the house of search: the parts («ein Fünftel») and the word of the found prime («ist prim»)
    for язык, я in moneystory.ЯЗЫКИ.items():
        for вещь in я["вещи"]:
            for w in вещь.split():
                _в(язык, w)
        _в(язык, я["он"])
    for язык, части in searchforms.ЧАСТИ.items():
        _в(язык, части); _в(язык, searchforms.ЯЗЫКИ[язык]["прост"].replace("{p} ", ""))
    for имя in units.ФОРМЫ_ВСЕХ:
        for много in (False, True):
            try:
                _в("en", units.англ(имя, много, письмо="brit"))
            except Exception:
                pass
    for ключ, формы in rugram.СЧЁТНЫЕ.items():
        _в("ru", ключ); _в("ru", формы)
    return вон


СЛОВА = _слова()
for _язык, _набор in _заполнители().items():
    СЛОВА[_язык] = frozenset(СЛОВА.get(_язык, frozenset()) | _набор)


_КРАЙ_СЛОВА = re.compile(r"[^\W\d_.,;:?!¿¡]")


def _слова(строка):
    """The words of the line that can carry a sign. A ONE-LETTER WORD counts
    only between words (03.09: «is {a e} ⊂ {a b e}» read its set elements as
    the articles of four languages, «формула a^2 + b^2 = c^2 при a = 3» its
    variables): a single letter beside a digit, a bracket or an operator is
    notation, not a word."""
    вон = []
    for м in СЛОВО.finditer(строка):
        w = м.group()
        if len(w) == 1:
            до = строка[:м.start()].rstrip()
            после = строка[м.end():].lstrip()
            if (до and _КРАЙ_СЛОВА.match(до[-1]) is None and not до[-1].isalpha()) or (после and not после[0].isalpha() and после[0] not in ".,;:?!¿¡"):
                continue
        вон.append(w.lower())
    return вон


def счёт(строка):
    """{язык: number of its function words in the line}."""
    слова = _слова(строка)
    return {язык: sum(1 for w in слова if w in набор) for язык, набор in СЛОВА.items()}


def язык(строка):
    """The pack that leads by function words, or None on silence or a tie."""
    с = счёт(строка)
    if not с:
        return None
    лучшие = sorted(с.items(), key=lambda kv: -kv[1])
    if лучшие[0][1] == 0 or (len(лучшие) > 1 and лучшие[1][1] == лучшие[0][1]):
        return None
    return лучшие[0][0]


def чужой(строка, свой="en"):
    """True when some other language's sign is at least as strong as the
    given language's and not zero — a court of that language must not judge."""
    с = счёт(строка)
    мой = с.get(свой, 0)
    return any(v > 0 and v >= мой for язык, v in с.items() if язык != свой)
