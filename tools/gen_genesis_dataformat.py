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

import bilang  # noqa: E402 — язык показа по азбуке
import pathlib
import random
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import dataformat as дф  # noqa: E402
from layer import Сбор, emit_grouped  # noqa: E402

ЦЕЛЬ = "datasets/genesis_dataformat.txt"
# ЯДРО ДОСЛОВНЫХ ПОВТОРОВ: форма покупается повторностью, и первые
# записи каждого прохода одинаковы во всех проходах.
ЯДРО = 3


# РОД ЗДЕСЬ — СТОРОНА ПЕРЕВОДА, А НЕ ЯЗЫК РАССКАЗА. «json → yaml» и «yaml → json» суть
# ДВА РАЗНЫХ ДЕЛА: одно пишет, другое читает, и учатся они порознь. А русская и английская
# поверхности одного перевода — одно дело, сказанное дважды.
ЗАПИСЬ_В_JSON = "запись, названная в json"
JSON_В_ПИСЬМО = "json → другое письмо"
ПИСЬМО_В_JSON = "другое письмо → json"
JSON_В_СЛОВА = "json → слова"
СЛОВА_В_JSON = "слова → json"


def _показы(з):
    """Все переводы одной записи — попарно, обеими сторонами."""
    вон = Сбор()
    письма = {имя: писать(з) for имя, писать, _ч in дф.ПИСЬМЕНА}
    # ОДНОСТРОЧНЫЕ ПИСЬМЕНА ПЕРЕВОДЯТСЯ В СТРОКЕ; многострочные
    # (yaml, toml, csv) переводятся с ИМЕНЕМ письма, ибо перевод строки
    # внутри показа разорвал бы его на строки, из которых ни одна не
    # была бы показом.
    for имя, текст in письма.items():
        if "\n" in текст:
            continue
        # РОД, СКАЗАННЫЙ ОДНИМ ЯЗЫКОМ, ЕСТЬ ПОЛОВИНА РОДА (15.09). Два рода дома — «запись,
        # названная в json» и «другое письмо → json» — звучали только по-английски, тогда как
        # обратная сторона («json → другое письмо») говорила обоими языками. Ничего, кроме
        # рамки речи, тут и не разнилось: запись, письмо и вердикт у обоих языков одни.
        вон.род = ЗАПИСЬ_В_JSON
        вон.append(f"in json this record is {письма['json']}.")
        вон.append(f"в письме json эта запись есть {письма['json']}.")
        break
    for имя, текст in письма.items():
        if имя == "json":
            continue
        сказано = текст.replace("\n", " ; ")
        вон.род = JSON_В_ПИСЬМО
        вон.append(f"{письма['json']} written in {имя} is {сказано}.")
        вон.род = ПИСЬМО_В_JSON
        вон.append(f"{сказано} written in json is {письма['json']}.")
        вон.append(f"{сказано} в письме json есть {письма['json']}.")
        вон.род = JSON_В_ПИСЬМО
        вон.append(f"{письма['json']} в письме {имя} есть {сказано}.")
    for язык, связка_ru in (("en", None), ("ru", None)):
        речь = дф.в_речь(з, язык)
        если = ("in words" if язык == "en" else "в словах")
        вон.род = JSON_В_СЛОВА
        вон.append(f"{письма['json']} {если} is {речь}"
                   if язык == "en" else
                   f"{письма['json']} {если} есть {речь}")
        вон.род = СЛОВА_В_JSON
        вон.append(f"{речь[:-1]} in json is {письма['json']}."
                   if язык == "en" else
                   f"{речь[:-1]} в json есть {письма['json']}.")
    вон.род = JSON_В_СЛОВА
    вон.append(f"how is {письма['json']} said in words? "
               f"{письма['json']} in words is {дф.в_речь(з, 'en')}")
    вон.append(f"как читается {письма['json']}? {письма['json']} "
               f"в словах есть {дф.в_речь(з, 'ru')}")
    return вон


def записи(шаг, сколько=10):
    """Записи прохода: ядро дословных плюс ходящие числами."""
    вон = Сбор()
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
        for с, род in _показы(з).парами:
            вон.род = род
            вон.append(с)
        if j < ЯДРО:
            for с, род in _показы(з).парами:
                вон.род = род
                вон.append(с)
    return вон


def pass_groups(шаг):
    return [записи(шаг)]


# --------------------------------------------------------------- ОБЪЯВЛЕНИЕ ДОМА

РОДЫ = (ЗАПИСЬ_В_JSON, JSON_В_ПИСЬМО, ПИСЬМО_В_JSON, JSON_В_СЛОВА, СЛОВА_В_JSON)

ЗАЧЕМ_РОДА = {
    ЗАПИСЬ_В_JSON: "запись названа одним письмом, без второй стороны",
    JSON_В_ПИСЬМО: "json переписан в yaml, toml, csv — сказано на обоих языках",
    ПИСЬМО_В_JSON: "обратная сторона того же перевода: чужое письмо прочтено в json",
    JSON_В_СЛОВА: "запись сказана речью — утверждением и вопросом",
    СЛОВА_В_JSON: "речь возвращена в запись: перевод в обратную сторону",
}


def группы(шаг):
    return pass_groups(шаг)


def страницы(шаг):
    return [с for г in группы(шаг) for с in г]


def перебор_страниц(шаг):
    return [п for г in группы(шаг) for п in г.парами]


def _показы_дома():
    from layer import PASSES                             # noqa: PLC0415
    вон = {}
    for шаг in range(len(PASSES)):
        for с, род in перебор_страниц(шаг):
            for строка in с.split("\n"):
                if строка.rstrip():
                    вон.setdefault(строка.rstrip(), (bilang.азбукой(строка.rstrip()), род))
    return вон


ПОКАЗЫ = _показы_дома()


def _самопроверка_дома():
    assert set(ЗАЧЕМ_РОДА) == set(РОДЫ), "глосса рода разошлась с объявлением"
    вне = {р for _с, р in перебор_страниц(0)} - set(РОДЫ)
    assert not вне, f"род кован и не объявлен: {sorted(вне)}"
    пустые = set(РОДЫ) - {р for _я, р in ПОКАЗЫ.values()}
    assert not пустые, f"род объявлен и не кован: {sorted(пустые)}"


_самопроверка_дома()


def main():
    беды = дф.оракул()
    if беды:
        print(f"ФОРМАТЫ ОТКАЗ: {len(беды)} записей не обратимы")
        return 2
    emit_grouped(ЦЕЛЬ, pass_groups)
    return 0


if __name__ == "__main__":
    sys.exit(main())
