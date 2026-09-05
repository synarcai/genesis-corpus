#!/usr/bin/env python3
"""THE HOUSE OF THE NUMBER LINE — the simplest questions a person checks a
speaker with, in nine languages: the neighbour of a number, which of two is
bigger, counting up and down, even or odd.

Born from the third band of conversation (BESEDA-3, 05.09): all four genera
were mute in all nine languages — the corpus compared horses with dogs and
proved parity in English derivations, but nobody had asked it «what number
comes after 9?». Every answer here is RECOMPUTED by the court from the
integers of the question, and every answer carries its ground: the bigger
number by the difference («9 − 7 = 2»), parity by the division («7 = 2 × 3 + 1»),
the neighbour and the row by the line itself. Generator and court read one
table; the world is CLOSED — a line of it that no frame reads is a lie.

    python3 tools/numberline.py    # self-check with mutants
"""
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

# per language: the question and the answer of every form; {n} the number,
# {m} its neighbour, {a}/{b} the two of the question, {c}/{d} the bigger/smaller,
# {r} their difference, {h} the half, {ряд} the row «1, 2, 3»
ЯЗЫКИ = {
    "ru": dict(
        на_сколько=("на сколько {c} больше {d}?", "на {r}: {c} − {d} = {r}."),
        словом=("как пишется число {n} словом?", "{N}."),
        половина=("сколько будет половина от {n}?", "{h}: {n} ÷ 2 = {h}."),
        возраст=("мне {a} {Га}. сколько мне будет через {k} {Гk}?", "{s} {Гs}: {a} + {k} = {s}."),
        после=("какое число идёт после {n}?", "после {n} идёт {m}."),
        перед=("какое число идёт перед {n}?", "перед {n} идёт {m}."),
        больше=("что больше: {a} или {b}?", "{c} больше: {c} − {d} = {r}."),
        меньше=("что меньше: {a} или {b}?", "{d} меньше: {c} − {d} = {r}."),
        счёт=("сосчитай от {a} до {b}.", "{ряд}."),
        обратно=("сосчитай обратно от {b} до {a}.", "{ряд}."),
        чёт=("{n} — чётное или нечётное число?", "чётное: {n} = 2 × {h}.", "нечётное: {n} = 2 × {h} + 1."),
    ),
    "en": dict(
        на_сколько=("how much more is {c} than {d}?", "{r} more: {c} − {d} = {r}."),
        словом=("how do you write the number {n} in words?", "{N}."),
        # the share court owns «half of X is Y» — the answer is written in its frame
        половина=("what is half of {n}?", "half of {n} is {h}: {n} ÷ 2 = {h}."),
        возраст=("i am {a} {Га} old. how old will i be in {k} {Гk}?", "{s} {Гs} old: {a} + {k} = {s}."),
        после=("what number comes after {n}?", "after {n} comes {m}."),
        перед=("what number comes before {n}?", "before {n} comes {m}."),
        больше=("which is bigger: {a} or {b}?", "{c} is bigger: {c} − {d} = {r}."),
        меньше=("which is smaller: {a} or {b}?", "{d} is smaller: {c} − {d} = {r}."),
        счёт=("count from {a} to {b}.", "{ряд}."),
        обратно=("count down from {b} to {a}.", "{ряд}."),
        чёт=("is {n} an even or an odd number?", "even: {n} = 2 × {h}.", "odd: {n} = 2 × {h} + 1."),
    ),
    "de": dict(
        на_сколько=("um wie viel ist {c} größer als {d}?", "um {r}: {c} − {d} = {r}."),
        словом=("wie schreibt man die Zahl {n} in Worten?", "{N}."),
        половина=("was ist die Hälfte von {n}?", "{h}: {n} ÷ 2 = {h}."),
        возраст=("ich bin {a} {Га} alt. wie alt werde ich in {k} {Гk} sein?", "{s} {Гs}: {a} + {k} = {s}."),
        после=("welche Zahl kommt nach {n}?", "nach {n} kommt {m}."),
        перед=("welche Zahl kommt vor {n}?", "vor {n} kommt {m}."),
        больше=("was ist größer: {a} oder {b}?", "{c} ist größer: {c} − {d} = {r}."),
        меньше=("was ist kleiner: {a} oder {b}?", "{d} ist kleiner: {c} − {d} = {r}."),
        счёт=("zähle von {a} bis {b}.", "{ряд}."),
        обратно=("zähle rückwärts von {b} bis {a}.", "{ряд}."),
        чёт=("ist {n} eine gerade oder eine ungerade Zahl?", "gerade: {n} = 2 × {h}.", "ungerade: {n} = 2 × {h} + 1."),
    ),
    "fr": dict(
        на_сколько=("de combien {c} est-il plus grand que {d} ?", "de {r} : {c} − {d} = {r}."),
        словом=("comment écrit-on le nombre {n} en lettres ?", "{N}."),
        половина=("combien fait la moitié de {n} ?", "{h} : {n} ÷ 2 = {h}."),
        возраст=("j'ai {a} {Га}. quel âge aurai-je dans {k} {Гk} ?", "{s} {Гs} : {a} + {k} = {s}."),
        после=("quel nombre vient après {n} ?", "après {n} vient {m}."),
        перед=("quel nombre vient avant {n} ?", "avant {n} vient {m}."),
        больше=("lequel est le plus grand : {a} ou {b} ?", "{c} est le plus grand : {c} − {d} = {r}."),
        меньше=("lequel est le plus petit : {a} ou {b} ?", "{d} est le plus petit : {c} − {d} = {r}."),
        счёт=("compte de {a} à {b}.", "{ряд}."),
        обратно=("compte à rebours de {b} à {a}.", "{ряд}."),
        чёт=("{n} est-il un nombre pair ou impair ?", "pair : {n} = 2 × {h}.", "impair : {n} = 2 × {h} + 1."),
    ),
    "es": dict(
        # «{r} más» читалось бы судом арифметики как «{r} +» — «más» есть знак пакета; «en {r}» им не является
        на_сколько=("¿cuánto mayor es {c} que {d}?", "en {r}: {c} − {d} = {r}."),
        словом=("¿cómo se escribe el número {n} en letras?", "{N}."),
        половина=("¿cuánto es la mitad de {n}?", "{h}: {n} ÷ 2 = {h}."),
        возраст=("tengo {a} {Га}. ¿cuántos años tendré dentro de {k} {Гk}?", "{s} {Гs}: {a} + {k} = {s}."),
        после=("¿qué número viene después del {n}?", "después del {n} viene el {m}."),
        перед=("¿qué número viene antes del {n}?", "antes del {n} viene el {m}."),
        больше=("¿cuál es mayor: {a} o {b}?", "{c} es mayor: {c} − {d} = {r}."),
        меньше=("¿cuál es menor: {a} o {b}?", "{d} es menor: {c} − {d} = {r}."),
        счёт=("cuenta del {a} al {b}.", "{ряд}."),
        обратно=("cuenta hacia atrás del {b} al {a}.", "{ряд}."),
        чёт=("¿{n} es un número par o impar?", "par: {n} = 2 × {h}.", "impar: {n} = 2 × {h} + 1."),
    ),
    "it": dict(
        на_сколько=("di quanto {c} è maggiore di {d}?", "di {r}: {c} − {d} = {r}."),
        словом=("come si scrive il numero {n} in lettere?", "{N}."),
        половина=("quanto fa la metà di {n}?", "{h}: {n} ÷ 2 = {h}."),
        возраст=("ho {a} {Га}. quanti anni avrò tra {k} {Гk}?", "{s} {Гs}: {a} + {k} = {s}."),
        # the article bends before a vowel-initial number word: «dopo l'8», «dopo il 9»
        после=("che numero viene dopo {IL}{n}?", "dopo {IL}{n} viene {IM}{m}."),
        перед=("che numero viene prima {DEL}{n}?", "prima {DEL}{n} viene {IM}{m}."),
        больше=("quale è maggiore: {a} o {b}?", "{c} è maggiore: {c} − {d} = {r}."),
        меньше=("quale è minore: {a} o {b}?", "{d} è minore: {c} − {d} = {r}."),
        счёт=("conta da {a} a {b}.", "{ряд}."),
        обратно=("conta all'indietro da {b} a {a}.", "{ряд}."),
        чёт=("{n} è un numero pari o dispari?", "pari: {n} = 2 × {h}.", "dispari: {n} = 2 × {h} + 1."),
    ),
    "pt": dict(
        # «{r} a mais» — «mais» есть знак пакета («+»); «em {r}» знаком не читается
        на_сколько=("quanto é que {c} é maior do que {d}?", "em {r}: {c} − {d} = {r}."),
        словом=("como se escreve o número {n} por extenso?", "{N}."),
        половина=("quanto é a metade de {n}?", "{h}: {n} ÷ 2 = {h}."),
        возраст=("tenho {a} {Га}. quantos anos terei daqui a {k} {Гk}?", "{s} {Гs}: {a} + {k} = {s}."),
        после=("que número vem depois do {n}?", "depois do {n} vem o {m}."),
        перед=("que número vem antes do {n}?", "antes do {n} vem o {m}."),
        больше=("qual é maior: {a} ou {b}?", "{c} é maior: {c} − {d} = {r}."),
        меньше=("qual é menor: {a} ou {b}?", "{d} é menor: {c} − {d} = {r}."),
        счёт=("conta de {a} a {b}.", "{ряд}."),
        обратно=("conta para trás de {b} a {a}.", "{ряд}."),
        чёт=("{n} é um número par ou ímpar?", "par: {n} = 2 × {h}.", "ímpar: {n} = 2 × {h} + 1."),
    ),
    "nl": dict(
        на_сколько=("hoeveel is {c} meer dan {d}?", "{r} meer: {c} − {d} = {r}."),
        словом=("hoe schrijf je het getal {n} in letters?", "{N}."),
        половина=("wat is de helft van {n}?", "{h}: {n} ÷ 2 = {h}."),
        возраст=("ik ben {a} {Га} oud. hoe oud ben ik over {k} {Гk}?", "{s} {Гs}: {a} + {k} = {s}."),
        после=("welk getal komt na {n}?", "na {n} komt {m}."),
        перед=("welk getal komt voor {n}?", "voor {n} komt {m}."),
        больше=("wat is groter: {a} of {b}?", "{c} is groter: {c} − {d} = {r}."),
        меньше=("wat is kleiner: {a} of {b}?", "{d} is kleiner: {c} − {d} = {r}."),
        счёт=("tel van {a} tot {b}.", "{ряд}."),
        обратно=("tel terug van {b} tot {a}.", "{ряд}."),
        чёт=("is {n} een even of een oneven getal?", "even: {n} = 2 × {h}.", "oneven: {n} = 2 × {h} + 1."),
    ),
    "pl": dict(
        на_сколько=("o ile {c} jest większe od {d}?", "o {r}: {c} − {d} = {r}."),
        словом=("jak zapisać liczbę {n} słownie?", "{N}."),
        половина=("ile to połowa z {n}?", "{h}: {n} ÷ 2 = {h}."),
        возраст=("mam {a} {Га}. ile będę mieć lat za {k} {Гk}?", "{s} {Гs}: {a} + {k} = {s}."),
        после=("jaka liczba jest po {n}?", "po {n} jest {m}."),
        перед=("jaka liczba jest przed {n}?", "przed {n} jest {m}."),
        больше=("co jest większe: {a} czy {b}?", "{c} jest większe: {c} − {d} = {r}."),
        меньше=("co jest mniejsze: {a} czy {b}?", "{d} jest mniejsze: {c} − {d} = {r}."),
        счёт=("policz od {a} do {b}.", "{ряд}."),
        обратно=("policz wstecz od {b} do {a}.", "{ряд}."),
        чёт=("{n} to liczba parzysta czy nieparzysta?", "parzysta: {n} = 2 × {h}.", "nieparzysta: {n} = 2 × {h} + 1."),
    ),
}

ФОРМЫ = ("после", "перед", "больше", "меньше", "счёт", "обратно", "чёт", "на_сколько", "словом", "половина", "возраст")

# THE YEAR BENDS BY THE COUNT, and the rule is the pack's (count_agreement),
# not this file's: Russian «1 год / 3 года / 7 лет», Polish «rok / lata / lat»,
# the rest one plural. The forms are named by the pack's own names.
import json as _json
_ПАКЕТЫ = pathlib.Path(__file__).resolve().parent / "langpacks"
ГОД = {"ru": {"one": "год", "few": "года", "many": "лет"}, "pl": {"one": "rok", "few": "lata", "many": "lat"},
       "en": {"one": "year", "many": "years"}, "de": {"one": "Jahr", "many": "Jahre"}, "fr": {"one": "an", "many": "ans"},
       "es": {"one": "año", "many": "años"}, "it": {"one": "anno", "many": "anni"}, "pt": {"one": "ano", "many": "anos"},
       "nl": {"one": "jaar", "many": "jaar"}}
_ПАКЕТ = {}


def _пакет(язык):
    if язык not in _ПАКЕТ:
        _ПАКЕТ[язык] = _json.loads((_ПАКЕТЫ / f"{язык}.json").read_text(encoding="utf-8"))
    return _ПАКЕТ[язык]


def год(язык, k):
    """The count form of «year» for k by the pack's agreement rule."""
    import langpack
    формы = list(ГОД[язык])
    i = langpack.count_form_index(_пакет(язык), {"forms": формы}, k)
    return ГОД[язык][формы[i]]


def числом(язык, n):
    """The numeral of n as the pack declares it, or None."""
    ч = _пакет(язык).get("numerals") or {}
    return ч.get(str(n))


ВОЗРАСТА = ((5, 1), (7, 3), (9, 2), (12, 5), (7, 1), (12, 3))
ВЕРХ = 20          # the line the house walks: 1..20
ДЛИНА_РЯДА = (3, 4, 5, 6)   # rows counted up or down

# ITALIAN ARTICLE BEFORE A DIGIT is the article before its WORD: «l'uno»,
# «l'otto», «l'undici», «il nove». Declared, not derived from spelling.
_ГЛАСНЫЕ_IT = frozenset({1, 8, 11, 18})


def _it(n):
    return ("l'" if n in _ГЛАСНЫЕ_IT else "il ",
            "dell'" if n in _ГЛАСНЫЕ_IT else "del ")


def _поля(n=None, m=None, a=None, b=None, ряд=None, язык=None, k=None):
    п = {}
    if n is not None:
        п.update(n=n, m=m, h=n // 2, IL=_it(n)[0], DEL=_it(n)[1])
        if язык is not None:
            п.update(N=числом(язык, n))
    if k is not None:
        s = a + k
        п.update(a=a, k=k, s=s, Га=год(язык, a), Гk=год(язык, k), Гs=год(язык, s))
        return п
    if m is not None:
        п.update(IM=_it(m)[0])
    if a is not None:
        c, d = max(a, b), min(a, b)
        п.update(a=a, b=b, c=c, d=d, r=c - d)
    if ряд is not None:
        п.update(ряд=", ".join(str(x) for x in ряд))
    return п


# THE QUESTION AFTER THE COUNTING TASK — «count from 1 to 5. what do we get?
# 1, 2, 3, 4, 5.» An imperative carries no question by nature, and the width
# of asking (scripts/ask_width.py) counts a genus without a question surface
# as a debt; the house of tasks answers it with one declared question per
# language, and this house reads THE SAME table rather than declaring a second.
import taskforms as _T
ВОПРОС_ПОСЛЕ = _T.ВОПРОСЫ
ПОВЕЛЕНИЯ = ("счёт", "обратно")


def страница(язык, форма, вопросом=False, **чем):
    я = ЯЗЫКИ[язык][форма]
    п = _поля(язык=язык, **чем)
    if форма == "словом" and п.get("N") is None:
        return None            # numeral not declared by the pack — no page
    if форма == "чёт":
        ответ = я[1] if п["n"] % 2 == 0 else я[2]
    else:
        ответ = я[1]
    между = f" {ВОПРОС_ПОСЛЕ[язык]}" if вопросом else ""
    return f"{я[0].format(**п)}{между} {ответ.format(**п)}"


def пары(язык):
    """The pairs of «bigger/smaller»: two partners per number — one far along
    the line, one two steps away («7 or 9») — never itself."""
    for a in range(1, ВЕРХ + 1):
        b = (a * 7 + 3) % ВЕРХ + 1
        if b == a:
            b = b % ВЕРХ + 1
        yield a, b
        if a + 2 <= ВЕРХ and a + 2 != b:
            yield a, a + 2


def _показы():
    вон = {}
    for язык in ЯЗЫКИ:
        for n in range(1, ВЕРХ):
            вон[страница(язык, "после", n=n, m=n + 1)] = (язык, "после")
        for n in range(2, ВЕРХ + 1):
            вон[страница(язык, "перед", n=n, m=n - 1)] = (язык, "перед")
        for a, b in пары(язык):
            вон[страница(язык, "больше", a=a, b=b)] = (язык, "больше")
            вон[страница(язык, "меньше", a=b, b=a)] = (язык, "меньше")
        for a in range(1, 11):
            for k in ДЛИНА_РЯДА:
                if a + k - 1 > 10:
                    continue
                ряд = list(range(a, a + k))
                for вопросом in (False, True):
                    вон[страница(язык, "счёт", вопросом, a=a, b=a + k - 1, ряд=ряд)] = (язык, "счёт")
                    вон[страница(язык, "обратно", вопросом, a=a, b=a + k - 1, ряд=ряд[::-1])] = (язык, "обратно")
        for n in range(1, ВЕРХ + 1):
            вон[страница(язык, "чёт", n=n)] = (язык, "чёт")
            с = страница(язык, "словом", n=n)
            if с is not None:
                вон[с] = (язык, "словом")
            if n % 2 == 0:
                вон[страница(язык, "половина", n=n)] = (язык, "половина")
        for a, b in пары(язык):
            c, d = max(a, b), min(a, b)
            вон[страница(язык, "на_сколько", a=c, b=d)] = (язык, "на_сколько")
        for a, k in ВОЗРАСТА:
            вон[страница(язык, "возраст", a=a, k=k)] = (язык, "возраст")
    return вон


ПОКАЗЫ = _показы()

ДЫРЫ = {"n": r"(?P<n>\d+)", "m": r"(?P<m>\d+)", "a": r"(?P<a>\d+)", "b": r"(?P<b>\d+)",
        "c": r"(?P<c>\d+)", "d": r"(?P<d>\d+)", "r": r"(?P<r>\d+)", "h": r"(?P<h>\d+)",
        "ряд": r"(?P<ряд>\d+(?:, \d+)+)", "IL": r"(?:il |l')", "DEL": r"(?:del |dell')", "IM": r"(?:il |l')",
        "k": r"(?P<k>\d+)", "s": r"(?P<s>\d+)", "N": r"(?P<N>[^\W\d_]+(?:[ -][^\W\d_]+)*)",
        "Га": r"(?P<Га>[^\W\d_]+)", "Гk": r"(?P<Гk>[^\W\d_]+)", "Гs": r"(?P<Гs>[^\W\d_]+)"}


def _образец(шаблон, видены=None):
    """A frame becomes a regex: every hole is named ONCE; a repeated hole
    becomes a back-reference, so «{c} … {c}» must carry the same number.
    The set of seen holes is shared between the question and the answer
    of one page, so the answer's {n} is the question's {n}."""
    видены = set() if видены is None else видены
    куски = []
    for кусок in re.split(r"(\{[^}]+\})", шаблон):
        if кусок.startswith("{"):
            имя = кусок[1:-1]
            if имя in ("IL", "DEL", "IM"):
                куски.append(ДЫРЫ[имя])
            elif имя in видены:
                куски.append(f"(?P={имя})")
            else:
                видены.add(имя); куски.append(ДЫРЫ[имя])
        else:
            куски.append(re.escape(кусок))
    return "".join(куски)


def _образцы():
    вон = []
    for язык, формы in ЯЗЫКИ.items():
        for форма, я in формы.items():
            for k, ответ in enumerate(я[1:]):
                # one pattern over the whole page: the hole of the question and the
                # hole of the answer are the SAME hole, and a back-reference binds them
                между = "(?: " + re.escape(ВОПРОС_ПОСЛЕ[язык]) + ")?" if форма in ПОВЕЛЕНИЯ else ""
                общие = set()
                образ = re.compile("^" + _образец(я[0], общие) + между + " " + _образец(ответ, общие) + "$")
                вон.append((образ, язык, форма, k))
    return вон


ОБРАЗЦЫ = _образцы()


def судить(строка):
    """(судимо, истинно): the line is a page of a frame, and its numbers hold."""
    с = строка.strip()
    for образ, язык, форма, k in ОБРАЗЦЫ:
        м = образ.match(с)
        if not м:
            continue
        г = {к: (int(v) if v.isdigit() else v) for к, v in м.groupdict().items() if v is not None}
        return True, _верно(форма, k, г, язык)
    return False, False


def _верно(форма, k, г, язык):
    if форма == "на_сколько":
        return г["c"] > г["d"] and г["r"] == г["c"] - г["d"]
    if форма == "словом":
        return г["N"] == числом(язык, г["n"])
    if форма == "половина":
        return г["n"] % 2 == 0 and г["h"] == г["n"] // 2
    if форма == "возраст":
        a, k_, s = г["a"], г["k"], г["s"]
        return s == a + k_ and (г["Га"], г["Гk"], г["Гs"]) == (год(язык, a), год(язык, k_), год(язык, s))
    if форма == "после":
        return г["m"] == г["n"] + 1
    if форма == "перед":
        return г["m"] == г["n"] - 1
    if форма in ("больше", "меньше"):
        a, b = г["a"], г["b"]
        return a != b and г["c"] == max(a, b) and г["d"] == min(a, b) and г["r"] == г["c"] - г["d"]
    if форма in ("счёт", "обратно"):
        a, b = г["a"], г["b"]
        ряд = [int(x) for x in г["ряд"].split(", ")]
        ждём = list(range(a, b + 1)) if форма == "счёт" else list(range(b, a - 1, -1))
        return a < b and ряд == ждём
    if форма == "чёт":
        n, h = г["n"], г["h"]
        чётное = (k == 0)
        return (n % 2 == 0) == чётное and h == n // 2
    return False


def _самопроверка():
    for показ, (язык, форма) in ПОКАЗЫ.items():
        assert судить(показ) == (True, True), (язык, форма, показ)
    мутанты = 0
    for показ in list(ПОКАЗЫ)[::37]:
        битая = re.sub(r"(\d+)\.$", lambda м: f"{int(м.group(1)) + 1}.", показ)
        if битая != показ:
            # a mutant that breaks the frame itself («+ 2» for «+ 1») is a lie by
            # closure, not by count: the house reads it as no page at all
            assert судить(битая) in ((True, False), (False, False)), битая
            мутанты += судить(битая) == (True, False)
    for язык in ("ru", "en", "it"):
        print("  ", страница(язык, "после", n=8, m=9))
        print("  ", страница(язык, "больше", a=7, b=9))
        print("  ", страница(язык, "чёт", n=7))
        print("  ", страница(язык, "счёт", a=1, b=5, ряд=[1, 2, 3, 4, 5]))
    print(f"  мутантов поймано: {мутанты}")
    print(f"  дом пишет показов: {len(ПОКАЗЫ)} (языков {len(ЯЗЫКИ)}, форм {len(ФОРМЫ)})")


if __name__ == "__main__":
    _самопроверка()
