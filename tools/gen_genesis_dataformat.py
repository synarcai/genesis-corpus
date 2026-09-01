#!/usr/bin/env python3
"""GENESIS layer: DATA FORMATS — one record, four writings and a speech.

The owner's requirement was not «markdown»; it was «every format, in
full, at the most expressive level». Markdown proved the mechanism: a
construct declares how to WRITE it and how to READ it, and their
agreement is the oracle. This layer proves the mechanism GENERALISES —
because a law that works on one predicate is a coincidence, and a law
that works on two is a law.

WHAT IS DIFFERENT HERE, AND WHY IT MATTERS. Markdown marks up TEXT:
the construct says how to read what is written. A data format carries
STRUCTURE: the SAME tree of values is written in four different scripts,
and the translation between them is exactly the ability we taught for
formulas. An organism that knows JSON and does not know that YAML says
the same thing knows a syntax and does not know DATA.

    JSON  {"count": 3, "name": "form"}
    YAML  count: 3
          name: form
    TOML  count = 3
          name = "form"
    CSV   count,name
          3,form
    речь  в записи поле count имеет значение 3, поле name имеет
          значение form.

CONVERSION IS THE SHOW ITSELF, in every direction that matters, and the
court parses BOTH sides with ITS OWN readers and requires the SAME
RECORD — not the same string. Two writings differ in every character
and mean one thing; that is the whole point of a format.

THE BOUNDARY IS DECLARED HONESTLY: flat records only. Nesting is held
differently by every format and not at all by CSV, and showing it as one
tree would be a lie about CSV. Nesting will come as its own genus when
there is something true to say about it in all four scripts.
"""

import pathlib
import random
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import dataformat as дф  # noqa: E402
from layer import emit_grouped  # noqa: E402

ЦЕЛЬ = "datasets/genesis_dataformat.txt"
# ЯДРО ДОСЛОВНЫХ ПОВТОРОВ: форма покупается повторностью, и первые
# записи каждого прохода одинаковы во всех проходах.
ЯДРО = 3


def _показы(з):
    """Все переводы одной записи — попарно, обеими сторонами."""
    вон = []
    письма = {имя: писать(з) for имя, писать, _ч in дф.ПИСЬМЕНА}
    # ОДНОСТРОЧНЫЕ ПИСЬМЕНА ПЕРЕВОДЯТСЯ В СТРОКЕ; многострочные
    # (yaml, toml, csv) переводятся с ИМЕНЕМ письма, ибо перевод строки
    # внутри показа разорвал бы его на строки, из которых ни одна не
    # была бы показом.
    for имя, текст in письма.items():
        if "\n" in текст:
            continue
        вон.append(f"in json this record is {письма['json']}.")
        break
    for имя, текст in письма.items():
        if имя == "json":
            continue
        сказано = текст.replace("\n", " ; ")
        вон.append(f"{письма['json']} written in {имя} is {сказано}.")
        вон.append(f"{сказано} written in json is {письма['json']}.")
        вон.append(f"{письма['json']} в письме {имя} есть {сказано}.")
    for язык, связка_ru in (("en", None), ("ru", None)):
        речь = дф.в_речь(з, язык)
        если = ("in words" if язык == "en" else "в словах")
        вон.append(f"{письма['json']} {если} is {речь}"
                   if язык == "en" else
                   f"{письма['json']} {если} есть {речь}")
        вон.append(f"{речь[:-1]} in json is {письма['json']}."
                   if язык == "en" else
                   f"{речь[:-1]} в json есть {письма['json']}.")
    вон.append(f"how is {письма['json']} said in words? "
               f"{письма['json']} in words is {дф.в_речь(з, 'en')}")
    вон.append(f"как читается {письма['json']}? {письма['json']} "
               f"в словах есть {дф.в_речь(з, 'ru')}")
    return вон


def записи(шаг, сколько=10):
    """Записи прохода: ядро дословных плюс ходящие числами."""
    вон = []
    for j in range(сколько):
        r = random.Random(j * 7 if j < ЯДРО else шаг * 37 + j * 7)
        з = дф.запись(r, 1 + r.randrange(4))
        # ХОДЫ СВЕРЯЮТСЯ ПЕРЕД ПОКАЗОМ: запись, не вернувшаяся всеми
        # письменами и обеими речами, не выходит в корпус.
        плохо = any(читать(писать(з)) != з
                    for _и, писать, читать in дф.ПИСЬМЕНА)
        плохо = плохо or any(дф.из_речи(дф.в_речь(з, я), я) != з
                             for я in ("en", "ru"))
        if плохо:
            continue
        вон += _показы(з)
        if j < ЯДРО:
            вон += _показы(з)
    return вон


def pass_groups(шаг):
    return [записи(шаг)]


def main():
    беды = дф.оракул()
    if беды:
        print(f"ФОРМАТЫ ОТКАЗ: {len(беды)} записей не обратимы")
        return 2
    emit_grouped(ЦЕЛЬ, pass_groups)
    return 0


if __name__ == "__main__":
    sys.exit(main())
