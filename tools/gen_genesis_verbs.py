#!/usr/bin/env python3
"""GENESIS layer: THE VERBS OF GSM8K, AND THE PERFECT.

e9's g1.46 stalls on «Alex has caught 5 more than Stan»: the perfect
«has V-ed» is not bought, because no layer ever showed it. The census
of the benchmark gives the verbs; this layer shows them in the
four-place discipline the market reads, and shows the perfect BESIDE
its plain past so the pair is bought from shows rather than assumed by
a rule.

THE VERB CENSUS TOOK FOUR WITNESSES, and each removed a different kind
of impostor:
  · the word stands BEFORE a number at least LAW times (counting
    position);
  · it is not a declared FUNCTION WORD — «a», «to», «her» carry a
    second form in the text as readily as any verb, and no count tells
    them apart (M-103: what a census cannot see is declared);
  · it is not a declared ITEM — «page 5» puts a thing before a number;
  · it is not a PROPER NAME — «Wednesday 5» likewise, and the evidence
    is capitalisation in the untouched text;
  · and it has a second VERBAL form in the same text (-s, -ed, -ing).

FORMS ARE DECLARED, NOT DERIVED. «eat/ate/eaten» and «run/ran/run»
obey no rule a corpus could show us in one pass, and a guessed form is
a lie shown twice.
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from gsm_items import ANIMATE, ITEMS  # noqa: E402
from layer import emit  # noqa: E402
from plural import by_count  # noqa: E402

NAMES = ["ida", "omar", "pia", "rosa", "sven", "tara", "umar", "vera"]
# ИМЯ ОБЪЯВЛЕНО ПАКЕТОМ (дом имён, М-131): суд читает имя группой и сверяет
# с пакетом; имя, которого пакет не знает, не вправе войти в показ.
import json as _json
import pathlib as _pathlib
_ИМЕНА_ПАКЕТА = set(_json.loads((_pathlib.Path(__file__).resolve().parent / "langpacks"
                                  / "en.json").read_text(encoding="utf-8"))["person_names"])
# РЕГИСТР ИМЕНИ ЧИТАЕТСЯ ИЗ ПАКЕТА (05.09): список дома выбирает лица, пакет
# объявляет их письмо; «ann» дома есть «Ann» пакета, и в показ входит пакетное.
_ПО_СТРОЧНОМУ = {и.lower(): и for и in _ИМЕНА_ПАКЕТА}
NAMES = [_ПО_СТРОЧНОМУ.get(и.lower(), и) for и in NAMES]
assert set(NAMES) <= _ИМЕНА_ПАКЕТА, "имя не объявлено пакетом en"
THINGS = [w for w in ITEMS if w not in ANIMATE]
# (base, third person, past, participle, items it truly takes)
#
# THE PAIRING IS A FACT ABOUT THE WORLD, AND NO CENSUS SEES IT (M-103).
# The first run said «vera planted 4 pieces», «sven delivers 9 years»,
# «omar has received 3 inches» — flawless grammar, false about what can
# be done to what. The same cure as the rates layer: the verb declares
# its items, and a check at build time refuses anything not in the
# census lexicon.
VERBS = [
    ("collect", "collects", "collected", "collected", ['cards', 'stickers', 'shells', 'marbles']),
    ("bake", "bakes", "baked", "baked", ['cookies', 'cupcakes', 'batches']),
    ("order", "orders", "ordered", "ordered", ['books', 'packs', 'meals']),
    ("plant", "plants", "planted", "planted", ['roses', 'flowers']),
    ("deliver", "delivers", "delivered", "delivered", ['newspapers', 'packs', 'meals']),
    ("upload", "uploads", "uploaded", "uploaded", ['vlogs', 'paintings']),
    ("receive", "receives", "received", "received", ['cards', 'reports', 'signatures']),
    ("produce", "produces", "produced", "produced", ['eggs', 'reports', 'paintings']),
    ("score", "scores", "scored", "scored", ['points']),
    ("count", "counts", "counted", "counted", ['marbles', 'balloons', 'cards']),
    ("weigh", "weighs", "weighed", "weighed", ['pounds', 'kilograms', 'ounces']),
    ("walk", "walks", "walked", "walked", ['miles', 'kilometers', 'yards']),
    ("need", "needs", "needed", "needed", ['cups', 'gallons', 'tablespoons']),
    ("use", "uses", "used", "used", ['pens', 'bandages', 'tablespoons']),
    ("buy", "buys", "bought", "bought", ['books', 'apples', 'bananas']),
    ("sell", "sells", "sold", "sold", ['cookies', 'books', 'flowers']),
    ("make", "makes", "made", "made", ['cupcakes', 'paintings', 'sandwiches']),
    ("hold", "holds", "held", "held", ['marbles', 'balloons', 'cards']),
    ("take", "takes", "took", "taken", ['minutes', 'hours', 'seconds']),
    ("give", "gives", "gave", "given", ['stickers', 'candies', 'lollipops']),
    ("eat", "eats", "ate", "eaten", ['apples', 'cookies', 'sandwiches']),
    ("run", "runs", "ran", "run", ['miles', 'kilometers', 'yards']),
    ("grow", "grows", "grew", "grown", ['roses', 'flowers']),
    ("see", "sees", "saw", "seen", ['paintings', 'balloons', 'flowers']),
    # «catch» просил e9: g1.46 пишет «Alex has caught 5 more than Stan»,
    # и перфект этого глагола не был показан ни разу.
    ("catch", "catches", "caught", "caught", ['balls', 'cards', 'balloons']),
    ("put", "puts", "put", "put", ['marbles', 'cards', 'balloons']),
    ("spend", "spends", "spent", "spent", ['minutes', 'hours', 'dollars']),
    ("pay", "pays", "paid", "paid", ['dollars']),
    ("read", "reads", "read", "read", ['pages', 'books', 'newspapers']),
    # «gets» и «drinks» перепись назвала третьими лицами, стоящими перед
    # числом: «she gets 20 marbles», «ingrid drinks 8 cups».
    ("get", "gets", "got", "got", ['marbles', 'cards', 'points']),
    ("drink", "drinks", "drank", "drunk", ['cups', 'gallons', 'ounces']),
]


def pass_shows(pass_i):
    out = []
    unknown = [w for _, _, _, _, its in VERBS for w in its
               if w not in ITEMS]
    assert not unknown, unknown
    for i, (base, s3, past, done, its) in enumerate(VERBS):
        seed = pass_i * 17 + i * 5
        a = NAMES[seed % len(NAMES)]
        b = NAMES[(seed + 3) % len(NAMES)]
        it = its[seed % len(its)]
        n = seed % 7 + 3           # 3..9
        m = seed % 4 + 1           # 1..4
        # ОТВЕТ И ЕГО КУЗНИЦА — ДВЕ ПОВЕРХНОСТИ ОДНОГО ФАКТА (М-166): 310
        # вычисленных ответов без единого шага. Чередование берётся с
        # разряда, свободного от разрядов имени, вещи и обоих чисел.
        forge = f": {n} + {m} = {n + m}" if (seed // 8) % 2 == 0 else ""
        # the four-place discipline, in the past
        out.append(
            f"{a} {past} {n} {by_count(n, it)}. "
            f"{a} {past} {m} {by_count(m, it)} more. "
            f"how many {it} does {a} hold now? "
            f"{a} holds {n + m} {by_count(n + m, it)}{forge}."
        )
        # THE PERFECT BESIDE ITS PAST: the pair is shown, not assumed
        out.append(
            f"{a} has {done} {n} {by_count(n, it)}. "
            f"{a} {past} {n} {by_count(n, it)}."
        )
        # g1.46's own shape: the perfect inside a comparison
        out.append(
            f"{b} has {done} {m} {by_count(m, it)}. "
            f"{a} has {done} {n} more {it} than {b}. "
            f"how many {it} does {a} hold now? "
            f"{a} holds {n + m} {by_count(n + m, it)}{forge}."
        )
        # the present, so base and third person live too
        out.append(
            f"{a} {s3} {n} {by_count(n, it)} every day. "
            f"they {base} {n} {by_count(n, it)} every day."
        )
    return out


def main():
    emit("datasets/genesis_verbs.txt", pass_shows)


if __name__ == "__main__":
    main()
