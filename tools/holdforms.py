#!/usr/bin/env python3
"""THE HOUSE OF HOLDINGS WITHOUT A VERB — the first show «only by frames» (05.09).

The owner's word (through holon): stop the small laws, prototype ONE BEARER — a story read
only by frames, one relation of the executor, a certificate. The first worlds such a reader
must buy are the plainest: a bearer holds a number of things and is asked how many; a
person has an age and is asked how old; two bearers hold two numbers and the question names
the second; a bearer holds none. No act, no ledger, no arithmetic: the answer is the story's
own number said back in a full sentence — the voice of the page (holon: a holding verb
becomes a HOLDING verb only when the answer is a sentence whose number folds to the story
by one choice, here by no choice at all).

WHAT THE HOUSE DECLARES AND WHAT IT BORROWS. Nine languages; bearers are the packs' persons
(the action-pages house declares them with gender and genitive; the Russian dative comes
from the pack's person_forms, the Polish dative and the Portuguese article from the SVAMP
house — one declaration, several readers); things are the action-pages things with their
count forms by the pack's agreement rule; the year bends by the number-line house's table;
the zero is the pack's numeral. Numbers run 1..40 — a wide row, not a table of eight pairs:
the goal is the VOLUME of frames, and the world is cut across the passes by the layer.

THE JUDGE IS THE FRAME ITSELF. A page is a frame whose holes are filled by declared
alternations; every hole that stands twice in the frame (the bearer of the question is the
bearer of the story, the answer's number is the story's, the answer's thing is the story's)
must carry the same value in both places; the count form must be the form of its number,
the year the form of its age, the question word the gender of the thing. The world is
CLOSED: a line the house does not recognise is a lie of the world, not a silence.

WHAT IS NOT MEASURED, NAMED: whether the reader can add or subtract — nothing here computes;
this world asks only whether a frame is READ, which is the prototype's first question.
"""
import json
import pathlib
import re
import frgram as _fr  # французская элизия: один закон, два читателя
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import actionpages as A  # noqa: E402
import numberline as N  # noqa: E402
import plgram  # noqa: E402 — три формы счёта: их считает и связка
import svampforms as S  # noqa: E402 — dative and article of the bearer, gender of the thing

_ПАКЕТЫ = pathlib.Path(__file__).resolve().parent / "langpacks"
ЯЗЫКИ = ("ru", "en", "de", "fr", "es", "it", "pt", "nl", "pl")
ВЕРХ = 40                      # the row of numbers the house walks: 1..40

РАМКИ = {
    "ru": dict(держание="у {Xр} {n} {Тn}. сколько {Тмн} у {Xр}? у {Xр} {n} {Тn}.",
               возраст="{Xд} {n} {Гn}. сколько лет {Xд}? {Xд} {n} {Гn}.",
               двое="у {Xр} {n} {Тn}, а у {Yр} {k} {Тk}. сколько {Тмн} у {Yр}? у {Yр} {k} {Тk}.",
               нет="у {Xр} нет {Тмн}. сколько {Тмн} у {Xр}? {ноль}: у {Xр} нет {Тмн}.",
               место="{М} {n} {Тn}. сколько {Тмн} {М}? {М} {n} {Тn}.",
               два_товара="у {Xр} {n} {Тn} и {m} {Т2m}. сколько {Т2мн} у {Xр}? у {Xр} {m} {Т2m}.",
               чей="у {Xр} {n} {Тn}. у кого {n} {Тn}? у {Xр}.",
               что_у="у {Xр} {n} {Тn}. что у {Xр}? у {Xр} {Тмн}.",
               место_чего="{М} {n} {Тn}. где {n} {Тn}? {М}."),
    "en": dict(держание="{X} has {n} {Тn}. how many {Тмн} does {X} have? {X} has {n} {Тn}.",
               возраст="{X} is {n} {Гn} old. how old is {X}? {X} is {n} {Гn} old.",
               двое="{X} has {n} {Тn} and {Y} has {k} {Тk}. how many {Тмн} does {Y} have? {Y} has {k} {Тk}.",
               нет="{X} has no {Тмн}. how many {Тмн} does {X} have? {ноль}: {X} has no {Тмн}.",
               место="{ЕСТЬ} {n} {Тn} {М}. how many {Тмн} are {М}? {ЕСТЬ} {n} {Тn} {М}.",
               два_товара="{X} has {n} {Тn} and {m} {Т2m}. how many {Т2мн} does {X} have? {X} has {m} {Т2m}.",
               чей="{X} has {n} {Тn}. who has {n} {Тn}? {X}.",
               что_у="{X} has {n} {Тn}. what does {X} have? {X} has {Тмн}.",
               место_чего="{ЕСТЬ} {n} {Тn} {М}. where {ЕСТЬ2} the {n} {Тn}? {М}."),
    "de": dict(держание="{X} hat {n} {Тn}. wie viele {Тмн} hat {X}? {X} hat {n} {Тn}.",
               возраст="{X} ist {n} {Гn} alt. wie alt ist {X}? {X} ist {n} {Гn} alt.",
               двое="{X} hat {n} {Тn} und {Y} hat {k} {Тk}. wie viele {Тмн} hat {Y}? {Y} hat {k} {Тk}.",
               нет="{X} hat keine {Тмн}. wie viele {Тмн} hat {X}? {ноль}: {X} hat keine {Тмн}.",
               место="{М} {ЕСТЬ} {n} {Тn}. wie viele {Тмн} sind {М}? {М} {ЕСТЬ} {n} {Тn}.",
               два_товара="{X} hat {n} {Тn} und {m} {Т2m}. wie viele {Т2мн} hat {X}? {X} hat {m} {Т2m}.",
               чей="{X} hat {n} {Тn}. wer hat {n} {Тn}? {X}.",
               что_у="{X} hat {n} {Тn}. was hat {X}? {X} hat {Тмн}.",
               место_чего="{М} {ЕСТЬ} {n} {Тn}. wo {ЕСТЬ2} die {n} {Тn}? {М}."),
    "fr": dict(держание="{X} a {n} {Тn}. combien de {Тмн} a {X} ? {X} a {n} {Тn}.",
               возраст="{X} a {n} {Гn}. quel âge a {X} ? {X} a {n} {Гn}.",
               двое="{X} a {n} {Тn} et {Y} a {k} {Тk}. combien de {Тмн} a {Y} ? {Y} a {k} {Тk}.",
               нет="{X} n'a pas de {Тмн}. combien de {Тмн} a {X} ? {ноль} : {X} n'a pas de {Тмн}.",
               место="il y a {n} {Тn} {М}. combien de {Тмн} y a-t-il {М} ? il y a {n} {Тn} {М}.",
               два_товара="{X} a {n} {Тn} et {m} {Т2m}. combien de {Т2мн} a {X} ? {X} a {m} {Т2m}.",
               чей="{X} a {n} {Тn}. qui a {n} {Тn} ? {X}.",
               что_у="{X} a {n} {Тn}. qu'est-ce que {X} a ? {X} a des {Тмн}.",
               место_чего="il y a {n} {Тn} {М}. où {ЕСТЬ2} les {n} {Тn} ? {М}."),
    "es": dict(держание="{X} tiene {n} {Тn}. ¿{кск} {Тмн} tiene {X}? {X} tiene {n} {Тn}.",
               возраст="{X} tiene {n} {Гn}. ¿cuántos años tiene {X}? {X} tiene {n} {Гn}.",
               двое="{X} tiene {n} {Тn} y {Y} tiene {k} {Тk}. ¿{кск} {Тмн} tiene {Y}? {Y} tiene {k} {Тk}.",
               нет="{X} no tiene {Тмн}. ¿{кск} {Тмн} tiene {X}? {ноль}: {X} no tiene {Тмн}.",
               место="hay {n} {Тn} {М}. ¿{кск} {Тмн} hay {М}? hay {n} {Тn} {М}.",
               два_товара="{X} tiene {n} {Тn} y {m} {Т2m}. ¿{кск2} {Т2мн} tiene {X}? {X} tiene {m} {Т2m}.",
               чей="{X} tiene {n} {Тn}. ¿quién tiene {n} {Тn}? {X}.",
               что_у="{X} tiene {n} {Тn}. ¿qué tiene {X}? {X} tiene {Тмн}.",
               место_чего="hay {n} {Тn} {М}. ¿dónde {ЕСТЬ2} {АМ} {n} {Тn}? {М}."),
    "it": dict(держание="{X} ha {n} {Тn}. {quante} {Тмн} ha {X}? {X} ha {n} {Тn}.",
               возраст="{X} ha {n} {Гn}. quanti anni ha {X}? {X} ha {n} {Гn}.",
               двое="{X} ha {n} {Тn} e {Y} ha {k} {Тk}. {quante} {Тмн} ha {Y}? {Y} ha {k} {Тk}.",
               нет="{X} non ha {Тмн}. {quante} {Тмн} ha {X}? {ноль}: {X} non ha {Тмн}.",
               место="{ЕСТЬ} {n} {Тn} {М}. {quante} {Тмн} ci sono {М}? {ЕСТЬ} {n} {Тn} {М}.",
               два_товара="{X} ha {n} {Тn} e {m} {Т2m}. {quante2} {Т2мн} ha {X}? {X} ha {m} {Т2m}.",
               чей="{X} ha {n} {Тn}. chi ha {n} {Тn}? {X}.",
               что_у="{X} ha {n} {Тn}. che cosa ha {X}? {X} ha {Тмн}.",
               место_чего="{ЕСТЬ} {n} {Тn} {М}. dove {ЕСТЬ2} {АМ} {n} {Тn}? {М}."),
    "pt": dict(держание="{X} tem {n} {Тn}. {quantas} {Тмн} tem {X}? {X} tem {n} {Тn}.",
               возраст="{X} tem {n} {Гn}. quantos anos tem {X}? {X} tem {n} {Гn}.",
               двое="{X} tem {n} {Тn} e {Y} tem {k} {Тk}. {quantas} {Тмн} tem {Y}? {Y} tem {k} {Тk}.",
               нет="{X} não tem {Тмн}. {quantas} {Тмн} tem {X}? {ноль}: {X} não tem {Тмн}.",
               место="há {n} {Тn} {М}. {quantas} {Тмн} há {М}? há {n} {Тn} {М}.",
               два_товара="{X} tem {n} {Тn} e {m} {Т2m}. {quantas2} {Т2мн} tem {X}? {X} tem {m} {Т2m}.",
               чей="{X} tem {n} {Тn}. quem tem {n} {Тn}? {X}.",
               что_у="{X} tem {n} {Тn}. o que tem {X}? {X} tem {Тмн}.",
               место_чего="há {n} {Тn} {М}. onde {ЕСТЬ2} {АМ} {n} {Тn}? {М}."),
    "nl": dict(держание="{X} heeft {n} {Тn}. hoeveel {Тмн} heeft {X}? {X} heeft {n} {Тn}.",
               возраст="{X} is {n} {Гn} oud. hoe oud is {X}? {X} is {n} {Гn} oud.",
               двое="{X} heeft {n} {Тn} en {Y} heeft {k} {Тk}. hoeveel {Тмн} heeft {Y}? {Y} heeft {k} {Тk}.",
               нет="{X} heeft geen {Тмн}. hoeveel {Тмн} heeft {X}? {ноль}: {X} heeft geen {Тмн}.",
               место="er {ЕСТЬ} {n} {Тn} {М}. hoeveel {Тмн} liggen {М}? er {ЕСТЬ} {n} {Тn} {М}.",
               два_товара="{X} heeft {n} {Тn} en {m} {Т2m}. hoeveel {Т2мн} heeft {X}? {X} heeft {m} {Т2m}.",
               чей="{X} heeft {n} {Тn}. wie heeft {n} {Тn}? {X}.",
               что_у="{X} heeft {n} {Тn}. wat heeft {X}? {X} heeft {Тмн}.",
               место_чего="er {ЕСТЬ} {n} {Тn} {М}. waar {ЕСТЬ2} de {n} {Тn}? {М}."),
    "pl": dict(держание="{X} ma {n} {Тn}. ile {Тмн} ma {X}? {X} ma {n} {Тn}.",
               возраст="{X} ma {n} {Гn}. ile lat ma {X}? {X} ma {n} {Гn}.",
               двое="{X} ma {n} {Тn}, a {Y} ma {k} {Тk}. ile {Тмн} ma {Y}? {Y} ma {k} {Тk}.",
               нет="{X} nie ma {Тмн}. ile {Тмн} ma {X}? {ноль}: {X} nie ma {Тмн}.",
               место="{М} {ЕСТЬП} {n} {Тn}. ile {Тмн} jest {М}? {М} {ЕСТЬП} {n} {Тn}.",
               два_товара="{X} ma {n} {Тn} i {m} {Т2m}. ile {Т2мн} ma {X}? {X} ma {m} {Т2m}.",
               чей="{X} ma {n} {Тn}. kto ma {n} {Тn}? {X}.",
               что_у="{X} ma {n} {Тn}. co ma {X}? {X} ma {Тмн}.",
               место_чего="{М} {ЕСТЬП} {n} {Тn}. gdzie {ЕСТЬП} {n} {Тn}? {М}."),
}
ФОРМЫ = ("держание", "возраст", "двое", "нет", "место", "два_товара", "чей", "что_у", "место_чего")
# THE SINGULAR IS FOR ONE ALONE in these languages («21 ans», «21 años», «21 anni», «21 anos»,
# «21 years»); a pack whose agreement rule bends 11/21/31 to the singular is wrong there, and
# the house does not write what the pack bends wrong: those ages are a DECLARED SEAM until the
# pack is corrected (the Polish rule was cured the same way, fa0db99). Nothing is skipped once
# the pack says «one» for 1 alone — the seam is read from the table, not from a list of numbers.
ЕДИНИЦА_ТОЛЬКО_ОДИН = frozenset({"en", "de", "fr", "es", "it", "pt", "nl"})


# THE PLACE IS DECLARED WITH ITS PREPOSITION AND CASE (05.09, wave 2 of the house): a place
# bends in Russian and Polish («на полке», «w pudełku») and takes an article elsewhere («on the
# shelf», «im Regal», «sur l'étagère»), and the house writes the whole prepositional phrase —
# one declaration, no guessing at cases. The question and the answer wear the SAME phrase.
МЕСТА = {
    "ru": ("на полке", "на столе", "в коробке", "в сумке"),
    "en": ("on the shelf", "on the table", "in the box", "in the bag"),
    "de": ("im Regal", "auf dem Tisch", "in der Kiste", "in der Tasche"),
    "fr": ("sur l'étagère", "sur la table", "dans la boîte", "dans le sac"),
    "es": ("en el estante", "en la mesa", "en la caja", "en la bolsa"),
    "it": ("sullo scaffale", "sul tavolo", "nella scatola", "nella borsa"),
    "pt": ("na prateleira", "na mesa", "na caixa", "no saco"),
    "nl": ("op de plank", "op de tafel", "in de doos", "in de tas"),
    "pl": ("na półce", "na stole", "w pudełku", "w torbie"),
}
# THE COPULA OF A PLACE BENDS WITH THE NUMBER: «there is 1 card» / «there are 12 cards»,
# «im Regal ist 1 Buch» / «sind 12 Bücher», «c'è 1 libro» / «ci sono 12 libri», «er ligt 1 boek» /
# «er liggen 12 boeken». Where the language keeps one form («hay», «há», «na półce jest»), the
# frame writes it and needs no hole. The judge checks the copula against the number.
ЕСТЬ = {"en": ("there is", "there are"), "de": ("ist", "sind"), "it": ("c'è", "ci sono"),
        "nl": ("ligt", "liggen")}
# the same law for the question «where is / where are»
ЕСТЬ2 = {"en": ("is", "are"), "de": ("ist", "sind"), "it": ("è", "sono"), "nl": ("ligt", "liggen"),
         "fr": ("est", "sont"), "es": ("está", "están"), "pt": ("está", "estão")}

# СВЯЗКА, ГНУЩАЯСЯ НЕ ПАРОЙ, А ПОЛОСОЙ СЧЁТА (08.09). Строкой выше стояло объявление: «где язык
# держит одну форму („hay“, „há“, „na półce jest“), рамка пишет её и дыры не просит». О польском
# это было ЛОЖЬЮ, и ложь была не в слове, а в СЧЁТЕ ФОРМ: пара «один / много» не годится языку,
# у которого их три. Польское «jest» стоит при ровно единице и при родительном множественном
# (5+, подростки, 21, 31), а при именительном множественном (2–4, кроме 12–14) стоит «są».
# Рамка писала «jest» всегда — и восемнадцать её страниц («na półce jest 3 jabłka») были ложны,
# а суд о них МОЛЧАЛ БЫ при подмене: связка стояла в образце буквой, и обратная строка просто не
# совпала бы с ним.
#
#     ЯЗЫК, У КОТОРОГО ТРИ ФОРМЫ СЧЁТА, ГНЁТ ПО НИМ ВСЁ, ЧТО СОГЛАСУЕТСЯ С ЧИСЛОМ, — И ГЛАГОЛ
#     ТОЖЕ. Дом уже брал ТРИ формы у существительного (`plgram.форма`); связка бралась парой,
#     и оттого дом знал закон и применял его наполовину.
#
# Индекс берётся ТОТ ЖЕ, что у существительного (`plgram.индекс`), а не свой: связка и вещь
# согласуются с одним числом, и два разных счёта формы разошлись бы в тот день, когда починят
# один из них.
# Таблица берётся У ДОМА ЯЗЫКА, а не переписывается сюда: один закон — один читатель, и
# день, когда польская связка уточнится, не должен стоить правки в девяти домах.
ЕСТЬ_ПОЛОСОЙ = {"pl": plgram.СВЯЗКА["наст"]}
# «ile {Тмн} jest {М}?» связки НЕ гнёт и дыры не просит: подлежащее там — «ile X» с родительным
# множественным, и оно стоит с «jest» при всяком числе. Это не буква вместо закона, а закон,
# у которого одна форма.

# THE PLURAL ARTICLE BENDS WITH THE THING where the language has one and it is not invariant
# («los libros» / «las flores», «i libri» / «le carte», «os livros» / «as flores»); the languages
# whose plural article is one word write it inside the frame and need no hole.
АРТИКЛЬ_МН = {"es": ("los", "las"), "it": ("i", "le"), "pt": ("os", "as")}


def _пакет(язык):
    return json.loads((_ПАКЕТЫ / f"{язык}.json").read_text(encoding="utf-8"))


# THE ZERO IS THE PACK'S NUMERAL («ноль», «zero», «null», «zéro», «cero», «nul») — read, not declared here
НОЛЬ = {язык: str((_пакет(язык).get("numerals") or {}).get("0")) for язык in ЯЗЫКИ}
for _яз, _н in НОЛЬ.items():
    assert _н and _н != "None", (_яз, "the pack declares no zero")


def _дательный(язык, лицо):
    """The dative of the bearer where the language bends it («Ане», «Annie», «à Ana»)."""
    if язык == "ru":
        return S._дательный(лицо[0]) or лицо[0]
    if язык == "pl":
        return S.ДАТЕЛЬНЫЙ_PL.get(лицо[0], лицо[0])
    if язык == "pt":
        return S._дательный_pt(лицо)
    return лицо[0]


def _поля(язык, i, j, Т, n, k, М=0, Т2=None, m=None):
    X, Y = S._лицо(язык, i), S._лицо(язык, j)
    if Y[0] == X[0]:
        Y = S._лицо(язык, j + 1)
    вещь = lambda c: A._вещь(язык, Т, c)
    вещей = len(A.ЯЗЫКИ[язык]["вещи"])
    Т2 = (Т + 1) % вещей if Т2 is None else Т2 % вещей
    if Т2 == Т:
        Т2 = (Т2 + 1) % вещей
    m = k if m is None else m
    вещь2 = lambda c: A._вещь(язык, Т2, c)
    п = dict(X=X[0], Xр=X[2], Xд=_дательный(язык, X), Y=Y[0], Yр=Y[2],
             n=n, k=k, m=m, Тn=вещь(n), Тk=вещь(k), Тмн=вещь(5), Гn=N.год(язык, n), ноль=НОЛЬ[язык],
             М=МЕСТА[язык][М % len(МЕСТА[язык])], Т2m=вещь2(m), Т2мн=вещь2(5))
    род = S.РОД_ВЕЩЕЙ.get(язык, {}).get(вещь(5), "f")
    род2 = S.РОД_ВЕЩЕЙ.get(язык, {}).get(вещь2(5), "f")
    for дыра, (м_, ж_) in S.РОДОВЫЕ.get(язык, {}).items():
        п[дыра] = м_ if род == "m" else ж_
        п[дыра + "2"] = м_ if род2 == "m" else ж_
    if язык in АРТИКЛЬ_МН:
        п["АМ"] = АРТИКЛЬ_МН[язык][0 if род == "m" else 1]
    if язык in ЕСТЬ:
        п["ЕСТЬ"] = ЕСТЬ[язык][0 if n == 1 else 1]
    if язык in ЕСТЬ2:
        п["ЕСТЬ2"] = ЕСТЬ2[язык][0 if n == 1 else 1]
    if язык in ЕСТЬ_ПОЛОСОЙ:
        п["ЕСТЬП"] = plgram.связка("наст", n)
    return п


def страница(язык, форма, i, j, Т, n, k=None, М=0, Т2=None, m=None):
    # ФРАНЦУЗСКАЯ ЭЛИЗИЯ ДЕЛАЕТСЯ ПОСЛЕ ПОДСТАНОВКИ: рамка держит «de» целым, ибо не знает,
    # что за ним встанет («de œufs» → «d'œufs»). Закон — у дома языка.
    готовая = РАМКИ[язык][форма].format(**_поля(язык, i, j, Т, n, k if k is not None else n, М, Т2, m))
    return _fr.элизия(готовая) if язык == "fr" else готовая


def _пара(n):
    """The second bearer's number: never the first one's."""
    k = (n * 7 + 3) % ВЕРХ + 1
    return k if k != n else k % ВЕРХ + 1


def _год_согнут(язык, n):
    """True where the pack bends the year of n to the singular in a language that keeps it for 1
    alone; a year that never bends («jaar») is never bent."""
    один, два = N.год(язык, 1), N.год(язык, 2)
    return язык in ЕДИНИЦА_ТОЛЬКО_ОДИН and n != 1 and один != два and N.год(язык, n) == один


ШОВ_ГОДА = {язык: [n for n in range(1, ВЕРХ + 1) if _год_согнут(язык, n)] for язык in ЯЗЫКИ}


def _показы():
    вон = {}
    for язык in ЯЗЫКИ:
        лиц, вещей = len(A.ЛИЦА[язык]), len(A.ЯЗЫКИ[язык]["вещи"])
        for n in range(1, ВЕРХ + 1):
            for i, Т in ((n % лиц, n % вещей), ((n * 3 + 1) % лиц, (n * 5 + 2) % вещей), ((n * 7 + 2) % лиц, (n * 3 + 1) % вещей)):
                вон[страница(язык, "держание", i, i + 1, Т, n)] = (язык, "держание")
            if not _год_согнут(язык, n):
                for i in (n % лиц, (n * 3 + 1) % лиц):
                    вон[страница(язык, "возраст", i, i + 1, 0, n)] = (язык, "возраст")
            for i, Т in ((n % лиц, (n * 5 + 1) % вещей), ((n * 5 + 3) % лиц, n % вещей)):
                вон[страница(язык, "двое", i, i + 3, Т, n, _пара(n))] = (язык, "двое")
        for i in range(лиц):
            for Т in range(вещей):
                вон[страница(язык, "нет", i, i + 1, Т, 1)] = (язык, "нет")
        # WAVE 2 — the frames the reader must buy in nine languages (05.09, measured on the
        # held-out key: story holdings are bought in English alone). A place holding things, a
        # bearer holding two DIFFERENT things and asked about the second, and three questions
        # whose answer is not a number at all: who holds, what is held, where it lies.
        мест = len(МЕСТА[язык])
        for n in range(1, ВЕРХ + 1):
            for сдвиг in (0, 1):
                Т = (n * (3 + сдвиг) + сдвиг) % вещей
                вон[страница(язык, "место", 0, 1, Т, n, М=(n + сдвиг) % мест)] = (язык, "место")
                вон[страница(язык, "два_товара", (n * 2 + сдвиг) % лиц, 0, Т, n,
                             Т2=(Т + 1 + сдвиг) % вещей, m=_пара(n))] = (язык, "два_товара")
            i, Т = n % лиц, (n * 5 + 1) % вещей
            вон[страница(язык, "чей", i, i + 1, Т, n)] = (язык, "чей")
            вон[страница(язык, "что_у", i, i + 1, Т, n)] = (язык, "что_у")
            # ШОВ ЕДИНСТВЕННОГО ЧИСЛА: вопрос «где» называет вещь ОПРЕДЕЛЁННОЙ («die 12 Bücher»,
            # «les 12 livres», «los 12 libros»), а её единственное требует артикля по роду в
            # каждом языке — таблицы рода единственного дом не объявлял, и он не пишет того,
            # чего не знает: форма стоит на числах от двух (шов читается правилом, не списком).
            if n >= 2:
                вон[страница(язык, "место_чего", 0, 1, Т, n, М=n % мест)] = (язык, "место_чего")
                # ВТОРАЯ ДИАГОНАЛЬ РЯДА (08.09). Рамка «где N X?» брала ОДНУ связку вещи с
                # местом на каждое число — и оттого давала три-четыре страницы на вещь при
                # законе опоры LAW³ = 8; прибор «ключ без опоры» назвал два её русских рода
                # поимённо. Вторая связка на то же число ровняет ряд вдвое и не заводит нового
                # рода: это та же рамка, тот же вопрос, иные вещь и место.
                #
                #     РЯД, ХОДЯЩИЙ ОДНОЙ ДИАГОНАЛЬЮ, ПОКАЗЫВАЕТ КАЖДУЮ ВЕЩЬ ВПОЛОВИНУ.
                вон[страница(язык, "место_чего", 0, 1, (n * 3 + 2) % вещей, n,
                             М=(n + 1) % мест)] = (язык, "место_чего")
    return вон


ПОКАЗЫ = _показы()


def _формы_вещей(язык):
    """form of a thing → the things wearing it (a form may belong to several things' rows)."""
    вон = {}
    for Т in range(len(A.ЯЗЫКИ[язык]["вещи"])):
        for c in range(0, ВЕРХ + 2):
            вон.setdefault(A._вещь(язык, Т, c), set()).add(Т)
    return вон


ФОРМЫ_ВЕЩЕЙ = {язык: _формы_вещей(язык) for язык in ЯЗЫКИ}
ГОДЫ = {язык: {N.год(язык, c) for c in range(0, ВЕРХ + 2)} for язык in ЯЗЫКИ}
_ДЫРА = re.compile(r"\{([^}]+)\}")


def _образец(язык, рамка):
    """One pattern over the whole page; the i-th occurrence of a hole is the group «hole__i»."""
    alt = lambda слова: "(?:" + "|".join(re.escape(с) for с in sorted({с for с in слова if с}, key=lambda с: (-len(с), с))) + ")"
    лица = [S._лицо(язык, i) for i in range(len(A.ЛИЦА[язык]))]
    имена = alt(л[0] for л in лица); род = alt(л[2] for л in лица); дат = alt(_дательный(язык, л) for л in лица)
    вещи = alt(ФОРМЫ_ВЕЩЕЙ[язык]); годы = alt(ГОДЫ[язык])
    дыры = {"X": имена, "Y": имена, "Xр": род, "Yр": род, "Xд": дат, "n": r"\d+", "k": r"\d+",
            "m": r"\d+", "Тn": вещи, "Тk": вещи, "Тмн": вещи, "Т2m": вещи, "Т2мн": вещи,
            "Гn": годы, "ноль": re.escape(НОЛЬ[язык]), "М": alt(МЕСТА[язык])}
    if язык in АРТИКЛЬ_МН:
        дыры["АМ"] = alt(АРТИКЛЬ_МН[язык])
    if язык in ЕСТЬ:
        дыры["ЕСТЬ"] = alt(ЕСТЬ[язык])
    if язык in ЕСТЬ2:
        дыры["ЕСТЬ2"] = alt(ЕСТЬ2[язык])
    if язык in ЕСТЬ_ПОЛОСОЙ:
        дыры["ЕСТЬП"] = alt(ЕСТЬ_ПОЛОСОЙ[язык])
    for дыра, пара in S.РОДОВЫЕ.get(язык, {}).items():
        дыры[дыра] = alt(пара)
        дыры[дыра + "2"] = alt(пара)
    счёт = {}
    куски = []
    for кусок in re.split(r"(\{[^}]+\})", рамка):
        if кусок.startswith("{"):
            дыра = кусок[1:-1]
            счёт[дыра] = счёт.get(дыра, 0) + 1
            куски.append(f"(?P<{_имя(дыра)}__{счёт[дыра]}>{дыры[дыра]})")
        else:
            куски.append(_fr.в_образце(кусок) if язык == "fr" else re.escape(кусок))
    return re.compile("^" + "".join(куски) + "$")


def _имя(дыра):
    """Group names must be identifiers: Cyrillic is fine, «р»/«д» suffixes too."""
    return "h_" + дыра


ОБРАЗЦЫ = [(_образец(язык, рамка), язык, форма) for язык, рамки in РАМКИ.items() for форма, рамка in рамки.items()]


def _вердикт(язык, форма, м):
    """Every hole repeated in the frame carries one value; forms are the forms of their numbers."""
    значения = {}
    for ключ, v in м.groupdict().items():
        дыра, _ = ключ[2:].rsplit("__", 1)
        if дыра in значения and значения[дыра] != v:
            return False
        значения[дыра] = v
    n = int(значения["n"]) if "n" in значения else None
    if "Тn" in значения and not any(A._вещь(язык, Т, n) == значения["Тn"] for Т in ФОРМЫ_ВЕЩЕЙ[язык].get(значения["Тn"], ())):
        return False
    if "Тk" in значения:
        k = int(значения["k"])
        if not any(A._вещь(язык, Т, k) == значения["Тk"] for Т in ФОРМЫ_ВЕЩЕЙ[язык].get(значения["Тk"], ())):
            return False
        # the two bearers' things are the same thing (Тмн is the plural of Тn and Тk)
        общие = ФОРМЫ_ВЕЩЕЙ[язык].get(значения["Тn"], set()) & ФОРМЫ_ВЕЩЕЙ[язык].get(значения["Тk"], set())
        if not общие:
            return False
    if "Тмн" in значения and "Тn" in значения:
        if not (ФОРМЫ_ВЕЩЕЙ[язык].get(значения["Тмн"], set()) & ФОРМЫ_ВЕЩЕЙ[язык].get(значения["Тn"], set())):
            return False
    if "Т2m" in значения:
        m = int(значения["m"])
        свои2 = ФОРМЫ_ВЕЩЕЙ[язык].get(значения["Т2m"], set())
        if not any(A._вещь(язык, Т, m) == значения["Т2m"] for Т in свои2):
            return False
        # the second thing's plural is the plural of the SAME second thing
        if "Т2мн" in значения and not (свои2 & ФОРМЫ_ВЕЩЕЙ[язык].get(значения["Т2мн"], set())):
            return False
        # and the second thing is NOT the first one: the question names another thing
        if "Тn" in значения and (свои2 & ФОРМЫ_ВЕЩЕЙ[язык].get(значения["Тn"], set())):
            return False
    if "Гn" in значения and N.год(язык, n) != значения["Гn"]:
        return False
    if форма in ("держание", "двое", "нет", "возраст") and n is not None and not (1 <= n <= ВЕРХ):
        return False
    if форма == "место_чего" and n is not None and n < 2:
        return False        # the seam of the singular: the house does not write it
    for дыра, пара in S.РОДОВЫЕ.get(язык, {}).items():
        if дыра in значения and "Тмн" in значения:
            род = S.РОД_ВЕЩЕЙ.get(язык, {}).get(значения["Тмн"], "f")
            if значения[дыра] != (пара[0] if род == "m" else пара[1]):
                return False
        # the question word of the SECOND thing bends with the second thing
        if дыра + "2" in значения and "Т2мн" in значения:
            род2 = S.РОД_ВЕЩЕЙ.get(язык, {}).get(значения["Т2мн"], "f")
            if значения[дыра + "2"] != (пара[0] if род2 == "m" else пара[1]):
                return False
    for дыра, таблица in (("ЕСТЬ", ЕСТЬ), ("ЕСТЬ2", ЕСТЬ2)):
        if дыра in значения and n is not None and язык in таблица:
            if значения[дыра] != таблица[язык][0 if n == 1 else 1]:
                return False
    if "ЕСТЬП" in значения and n is not None and язык in ЕСТЬ_ПОЛОСОЙ:
        if значения["ЕСТЬП"] != plgram.связка("наст", n):
            return False
    if "АМ" in значения and "Тn" in значения and язык in АРТИКЛЬ_МН:
        вещи_ = ФОРМЫ_ВЕЩЕЙ[язык].get(значения["Тn"], set())
        род = S.РОД_ВЕЩЕЙ.get(язык, {}).get(A._вещь(язык, next(iter(вещи_)), 5), "f") if вещи_ else "f"
        if значения["АМ"] != (АРТИКЛЬ_МН[язык][0] if род == "m" else АРТИКЛЬ_МН[язык][1]):
            return False
    return True


def судить(строка):
    """(судимо, истинно): a page of a frame of the house, and its holes agree; else silence."""
    с = строка.strip()
    if с in ПОКАЗЫ:
        return True, True
    for образ, язык, форма in ОБРАЗЦЫ:
        м = образ.match(с)
        if м:
            return True, _вердикт(язык, форма, м)
    return False, False


def _самопроверка():
    for показ in ПОКАЗЫ:
        assert судить(показ) == (True, True), показ
    мутанты = 0
    for язык in ЯЗЫКИ:
        д = страница(язык, "держание", 0, 1, 0, 12)
        # the answer's number is not the story's
        битая = re.sub(r"(\d+)(?=[^\d]*$)", lambda м: str(int(м.group(1)) + 1), д)
        assert судить(битая) == (True, False), битая
        # a foreign bearer is not a page of the house — silence here, a lie at the closed world's gate
        X = S._лицо(язык, 0)
        чужая = next(д.replace(ф, "Zorbo") for ф in (X[0], X[2], _дательный(язык, X)) if ф in д)
        assert судить(чужая) == (False, False), чужая
        # the second bearer's question answered with the first bearer's number
        дв = страница(язык, "двое", 0, 3, 0, 12, 5)
        assert судить(дв) == (True, True), дв
        assert судить(re.sub(r"(\d+)(?=[^\d]*$)", "12", дв)) == (True, False), дв
        # the age with the wrong form of the year (where the language bends the year)
        в = страница(язык, "возраст", 0, 1, 0, 12)
        for c in (1, 2):
            иная = N.год(язык, c)
            if иная != N.год(язык, 12):
                assert судить(в[:v_last(в)] + в[v_last(в):].replace(N.год(язык, 12), иная, 1)) == (True, False), в
                мутанты += 1
                break
        # «none» answered with a number is not a page of the house
        н = страница(язык, "нет", 0, 1, 0, 1)
        assert судить(н) == (True, True), н
        assert судить(н[:v_last(н)] + н[v_last(н):].replace(НОЛЬ[язык], "3", 1)) == (False, False), н
        мутанты += 4
        # ── ВОЛНА 2: пять родов лжи новых рамок ──────────────────────────────
        # (1) вопрос о ВТОРОМ товаре, отвеченный числом первого
        дт = страница(язык, "два_товара", 0, 1, 0, 12, Т2=1, m=5)
        assert судить(дт) == (True, True), дт
        хв = v_last(дт)
        assert судить(дт[:хв] + дт[хв:].replace("5", "12", 1)) == (True, False), дт
        # (2) владелец назван чужим именем
        ч = страница(язык, "чей", 0, 1, 0, 12)
        assert судить(ч) == (True, True), ч
        X0, X1 = S._лицо(язык, 0), S._лицо(язык, 1)
        for своё, чужое in ((X0[0], X1[0]), (X0[2], X1[2])):
            if своё in ч[v_last(ч):]:
                assert судить(ч[:v_last(ч)] + ч[v_last(ч):].replace(своё, чужое, 1)) == (True, False), ч
                break
        # (3) вещь названа чужой вещью
        щ = страница(язык, "что_у", 0, 1, 0, 12)
        assert судить(щ) == (True, True), щ
        своя, чужая = A._вещь(язык, 0, 5), A._вещь(язык, 1, 5)
        assert судить(щ[:v_last(щ)] + щ[v_last(щ):].replace(своя, чужая, 1)) == (True, False), щ
        # (4) место названо чужим местом
        мч = страница(язык, "место_чего", 0, 1, 0, 12, М=0)
        assert судить(мч) == (True, True), мч
        assert судить(мч[:v_last(мч)] + мч[v_last(мч):].replace(МЕСТА[язык][0], МЕСТА[язык][2], 1)) == (True, False), мч
        # (5) связка места не по числу («there are 1 card»)
        м1 = страница(язык, "место", 0, 1, 0, 1, М=0)
        assert судить(м1) == (True, True), м1
        if язык in ЕСТЬ:
            assert судить(м1.replace(ЕСТЬ[язык][0], ЕСТЬ[язык][1], 1)) == (True, False), м1
            мутанты += 1
        # (6) связка, гнущаяся ПОЛОСОЙ: «na półce jest 3 jabłka» вместо «są» — и это ЛОЖЬ,
        # а не молчание: подмена обязана быть СУДИМА, иначе закон стоит буквой (см. sign_traps)
        if язык in ЕСТЬ_ПОЛОСОЙ:
            м3 = страница(язык, "место", 0, 1, 0, 3, М=0)
            assert судить(м3) == (True, True), м3
            порча = м3.replace(ЕСТЬ_ПОЛОСОЙ[язык][1], ЕСТЬ_ПОЛОСОЙ[язык][0], 1)
            assert порча != м3 and судить(порча) == (True, False), м3
            мутанты += 1
        мутанты += 4
    print("  ", страница("ru", "держание", 1, 2, 1, 3))
    print("  ", страница("ru", "возраст", 1, 2, 0, 22))
    print("  ", страница("en", "двое", 0, 3, 2, 12, 5))
    print("  ", страница("pl", "нет", 1, 2, 0, 1))
    print("  ", страница("pt", "возраст", 1, 2, 0, 28))
    print("  ", страница("en", "место", 0, 1, 2, 12, М=0))
    print("  ", страница("de", "два_товара", 0, 1, 0, 12, Т2=2, m=5))
    print("  ", страница("es", "место_чего", 0, 1, 2, 12, М=0))
    print("  ", страница("nl", "что_у", 0, 1, 3, 7))
    print("  ", страница("fr", "чей", 0, 1, 1, 9))
    print(f"  мутантов поймано: {мутанты}")
    по_форме = {}
    for _, (язык, форма) in ПОКАЗЫ.items():
        по_форме[форма] = по_форме.get(форма, 0) + 1
    шов = {я: ч for я, ч in ШОВ_ГОДА.items() if ч}
    if шов:
        print(f"  ШОВ ГОДА (пакет гнёт к единице, дом не пишет): {шов}")
    print(f"  дом пишет показов: {len(ПОКАЗЫ)} (языков {len(ЯЗЫКИ)}, форм {len(ФОРМЫ)}): " + ", ".join(f"{ф} {к}" for ф, к in по_форме.items()))


def v_last(с):
    """The start of the answer (after the last question mark)."""
    м = list(re.finditer(r"[?？] ", с))
    return м[-1].end() if м else 0


if __name__ == "__main__":
    _самопроверка()
