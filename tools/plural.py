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


# АРТИКЛЬ ГНЁТСЯ ЗВУКОМ, А НЕ БУКВОЙ (08.09).
#
# Сто шесть строк свода в семи мирах писали «a apple», «a egg», «a hour», «a insect», «a eye»,
# «a axe», «a onion», «a orange». Дома ставили артикль ЛИТЕРАЛОМ перед дырой имени — тот же
# род, что причастие в доме ролей и связка в доме держания: рамка одна на все имена, а звук
# у каждого свой.
#
#     АРТИКЛЬ, ВЫНЕСЕННЫЙ В РАМКУ, ПЕРЕСТАЁТ СЛЫШАТЬ СЛОВО, ПЕРЕД КОТОРЫМ СТОИТ.
#
# ЗВУК НЕ ВЫВОДИТСЯ ИЗ ПИСЬМА, И ОБЕ СТОРОНЫ ЭТОГО ОБЪЯВЛЕНЫ ПОИМЁННО:
#
#   · буква гласная, звук согласный — «a unit», «a user», «a one-shot», «a European»:
#     английское «u» чаще звучит как /juː/, и правило по букве дало бы «an unit»;
#   · буква согласная, звук гласный — «an hour», «an honest answer»: «h» бывает немой.
#
# Слово, не названное ни в одном списке, судится ПЕРВОЙ БУКВОЙ, и это честная граница:
# a/e/i/o в начале английского слова звучат гласной почти всегда, а «u» из признака выведено
# вовсе — оттого ошибка возможна лишь на слове, которого дом ещё не писал.
СОГЛАСНЫЙ_ЗВУК = frozenset((
    "one", "once", "euro", "euros", "european", "unit", "units", "user", "users",
    "unique", "universal", "university", "uniform", "union", "useful", "usual", "utility",
))
ГЛАСНЫЙ_ЗВУК = frozenset(("hour", "hours", "honest", "honestly", "honour", "heir"))


# НАБОР БУКВ, А НЕ СТРОКА: имя из одних знаков препинания даёт пустую голову, а
# «'' in "aeio"» есть ИСТИНА — такое имя получало бы «an» ни за что.
ГЛАСНЫЕ_БУКВЫ = frozenset("aeio")


def article(word):
    """«a» или «an» перед словом — по ЗВУКУ, как его объявил английский."""
    низ = str(word).strip().lower()
    if not низ:
        return "a"
    голова = низ.split()[0].strip("«»\"'(),.;:")
    if голова in ГЛАСНЫЙ_ЗВУК:
        return "an"
    if голова in СОГЛАСНЫЙ_ЗВУК:
        return "a"
    return "an" if голова[:1] in ГЛАСНЫЕ_БУКВЫ else "a"


def with_article(word):
    """Слово со своим артиклем: «an eye», «a wheel»."""
    return f"{article(word)} {word}"


_ПАРА_АРТИКЛЯ = __import__("re").compile(r"\b(an?) ([a-z]+)\b")


def article_ok(line):
    """False — в английской строке стои́т «a» там, где звук требует «an» (или наоборот).

    ЧИТАЕТСЯ ПОСЛЕ ВЕРДИКТА, А НЕ В ОБРАЗЦЕ: артикль в образце суда есть ДЫРА (иначе образец
    не покрыл бы обеих форм), и проверить его может лишь тот, кто знает слово за ним.
    """
    for артикль, слово in _ПАРА_АРТИКЛЯ.findall(str(line).lower()):
        if артикль != article(слово):
            return False
    return True
