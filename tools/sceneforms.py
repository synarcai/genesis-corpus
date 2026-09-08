#!/usr/bin/env python3
"""THE HOUSE OF THE SCENE — frames without a verb of action (05.09, wave of the frame market).

MEASURED ON THE HELD-OUT KEY: story holdings are bought in ENGLISH ALONE — zero right answers
on eight languages where the corpus shows all nine. The reader's frame market (AskFrame) buys
what the corpus SHOWS as a frame, and a frame is a skeleton of a question with a relation that
reproduces the shown answer. Therefore the corpus owes the market not new verbs but the VOLUME
OF DIFFERENT FRAMES: a scene held by a copula and a preposition, asked in six ways.

SIX FRAMES, NINE LANGUAGES, NO VERB OF ACTION:
  · a place holding TWO kinds, the question naming the second («в коробке 12 книг и 5 мелков»);
  · a class of a thing («кот — животное. что такое кот?») — the members and their classes are
    the world-facts house's declaration, read here, not re-declared;
  · TWO places, the question asking WHERE there are more — the answer is a place, not a number;
  · the COLOUR of the things («у Ани 12 красных шаров. какого цвета шары у Ани? красные.»);
  · the belonging of things to a place, the thing standing FIRST («12 книг на полке. где …?»);
  · IS THERE — a yes/no question over a place, with its negative twin («на полке нет мелков»),
    the polarity words read from the pack.

WHAT THE HOUSE BORROWS AND WHAT IT DECLARES. Bearers, things and their count forms come from
the action-pages house and the packs; places with their preposition and case, the copula of a
place and the plural article — from the holdings house (one declaration, several readers);
classes — from the world-facts house; colours — from the SVAMP house, attributive («12 красных
шаров») and predicative («красные») from its two tables. Declared here: the question surfaces
of the six frames, the Polish copula of a place (it bends by the COUNT FORM: «jest 12 książek»
but «są 3 książki»), and the negative frame of each language.

THE SEAM OF THE COLOUR IS READ FROM THE TABLES, NOT LISTED. Where the two colour tables of the
SVAMP house disagree at an index (they were written for different frames — «rouges/bleues»
against «rouges/jaunes»), the house writes only the index where they agree; where the
predicative is a form of the SAME adjective (ru «красных/красные», de «rote/rot», nl, pl, en),
both indices are written, and that agreement is declared. The Russian and Polish attributive
stands in the genitive plural, which is the form of «many» — so the colour frame is written
only for numbers whose count form is «many» there, and for n ≥ 2 elsewhere.

THE JUDGE IS THE FRAME ITSELF (as in the holdings house): every hole repeated in the frame
carries one value, the count form is the form of its number, the copula agrees with the number,
the place of the answer is the place of the story, the colour of the answer is the colour of the
story, the polarity of the answer is the polarity of the question. The world is CLOSED.

WHAT IS NOT MEASURED, NAMED: nothing here computes — the world asks only whether a FRAME is
read, which is the frame market's first question.
"""
import json
import pathlib
import re
import frgram as _fr  # французская элизия: один закон, два читателя
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import actionpages as A  # noqa: E402
import holdforms as HF  # noqa: E402 — places, the copula of a place, the plural article
import langpack  # noqa: E402
import rugram  # noqa: E402 — the Russian nominative plural («шары», not «шара»)
import svampforms as S  # noqa: E402 — bearers' forms, gender of things, colours
import worldfacts as W  # noqa: E402 — the classes of things

_ПАКЕТЫ = pathlib.Path(__file__).resolve().parent / "langpacks"
ЯЗЫКИ = HF.ЯЗЫКИ
ВЕРХ = 40

# THE POLARITY WORDS ARE THE PACK'S (М-284: a pack declares its «yes» and «no»)
ДА = {}
НЕТ = {}
for _яз in ЯЗЫКИ:
    _п = json.loads((_ПАКЕТЫ / f"{_яз}.json").read_text(encoding="utf-8")).get("polarity") or {}
    ДА[_яз] = (_п.get("yes") or [None])[0]
    НЕТ[_яз] = (_п.get("no") or [None])[0]
    assert ДА[_яз] and НЕТ[_яз], (_яз, "the pack declares no polarity")

# THE POLISH COPULA OF A PLACE BENDS BY THE COUNT FORM, not by «one or many»: «na półce jest
# 12 książek» (many), «na półce są 3 książki» (few), «na półce jest 1 książka» (one).
СВЯЗКА_PL = {"one": "jest", "few": "są", "many": "jest"}
_ФОРМЫ_СЧЁТА = ("one", "few", "many")


def _ячейка(язык, n):
    """The pack's count cell of n: «one» / «few» / «many» (the rule is the pack's)."""
    пакет = json.loads((_ПАКЕТЫ / f"{язык}.json").read_text(encoding="utf-8"))
    return _ФОРМЫ_СЧЁТА[langpack.count_form_index(пакет, {"forms": list(_ФОРМЫ_СЧЁТА)}, n)]


_ЯЧЕЙКИ = {язык: {n: _ячейка(язык, n) for n in range(0, ВЕРХ + 2)} for язык in ЯЗЫКИ}

# THE PREDICATIVE COLOUR IS A FORM OF THE SAME ADJECTIVE in these languages (the attributive
# «красных» and the predicative «красные» are one word); elsewhere the two tables of the SVAMP
# house were written for different frames, and only an index where they AGREE may be used.
ОДНО_ПРИЛАГАТЕЛЬНОЕ = frozenset({"ru", "en", "de", "nl", "pl"})


def _цвета(язык):
    """[(attributive, attributive-masculine, predicative)] — only the agreeing indices."""
    вон = []
    for i in (0, 1):
        атр = S.ЦВЕТА[язык][i]
        атр_м = S.ЦВЕТА_М.get(язык, S.ЦВЕТА[язык])[i]
        пред = S.ЦВЕТ_ПРЕД[язык][i]
        if язык in ОДНО_ПРИЛАГАТЕЛЬНОЕ or атр == пред:
            вон.append((атр, атр_м, пред))
    return вон


ЦВЕТА = {язык: _цвета(язык) for язык in ЯЗЫКИ}
for _яз, _ц in ЦВЕТА.items():
    assert _ц, (_яз, "no colour agrees between the two tables")

РАМКИ = {
    "ru": dict(
        место_два="{М} {n} {Тn} и {m} {Т2m}. сколько {Т2мн} {М}? {М} {m} {Т2m}.",
        класс="{ч} — {к}. что такое {ч}? {ч} — {к}.",
        два_места="{М} {n} {Тn}, а {М2} {m} {Тm}. где {Тмн} больше? {МБ}.",
        цвет="у {Xр} {n} {Ц} {Тn}. какого цвета {Тим} у {Xр}? {ЦП}.",
        принадлежность="{n} {Тn} {М}. где {n} {Тn}? {М}.",
        есть_ли="{М} {n} {Тn}. есть ли {Тим} {М}? {ДА}, {М} {n} {Тn}.",
        нет_ли="{М} нет {Тмн}. есть ли {Тим} {М}? {НЕТ}, {М} нет {Тмн}."),
    "en": dict(
        место_два="{ЕСТЬn} {n} {Тn} and {m} {Т2m} {М}. how many {Т2мн} are {М}? {ЕСТЬm} {m} {Т2m} {М}.",
        класс="{ч} is {к}. what is {ч}? {ч} is {к}.",
        два_места="{ЕСТЬn} {n} {Тn} {М} and {ЕСТЬm} {m} {Тm} {М2}. where are there more {Тмн}? {МБ}.",
        цвет="{X} has {n} {Ц} {Тn}. what colour are the {Тмн}? {ЦП}.",
        принадлежность="{n} {Тn} are {М}. where are the {n} {Тn}? {М}.",
        есть_ли="{ЕСТЬn} {n} {Тn} {М}. are there any {Тмн} {М}? {ДА}, {ЕСТЬn} {n} {Тn} {М}.",
        нет_ли="there are no {Тмн} {М}. are there any {Тмн} {М}? {НЕТ}, there are no {Тмн} {М}."),
    "de": dict(
        место_два="{М} {ЕСТЬn} {n} {Тn} und {m} {Т2m}. wie viele {Т2мн} {ЕСТЬm} {М}? {М} {ЕСТЬm} {m} {Т2m}.",
        класс="{ч} ist {к}. was ist {ч}? {ч} ist {к}.",
        два_места="{М} {ЕСТЬn} {n} {Тn} und {М2} {ЕСТЬm} {m} {Тm}. wo {ЕСТЬ2м} mehr {Тмн}? {МБ}.",
        цвет="{X} hat {n} {Ц} {Тn}. welche Farbe haben die {Тмн}? {ЦП}.",
        принадлежность="{n} {Тn} {ЕСТЬ2n} {М}. wo {ЕСТЬ2n} die {n} {Тn}? {М}.",
        есть_ли="{М} {ЕСТЬn} {n} {Тn}. gibt es {Тмн} {М}? {ДА}, {М} {ЕСТЬn} {n} {Тn}.",
        нет_ли="{М} sind keine {Тмн}. gibt es {Тмн} {М}? {НЕТ}, {М} sind keine {Тмн}."),
    "fr": dict(
        место_два="il y a {n} {Тn} et {m} {Т2m} {М}. combien de {Т2мн} y a-t-il {М} ? il y a {m} {Т2m} {М}.",
        класс="{ч} est {к}. {ЧТО}{ч} ? {ч} est {к}.",
        два_места="il y a {n} {Тn} {М} et {m} {Тm} {М2}. où y a-t-il plus de {Тмн} ? {МБ}.",
        цвет="{X} a {n} {Тn} {Ц}. de quelle couleur sont les {Тмн} ? {ЦП}.",
        принадлежность="{n} {Тn} {ЕСТЬ2n} {М}. où {ЕСТЬ2n} les {n} {Тn} ? {М}.",
        есть_ли="il y a {n} {Тn} {М}. y a-t-il des {Тмн} {М} ? {ДА}, il y a {n} {Тn} {М}.",
        нет_ли="il n'y a pas de {Тмн} {М}. y a-t-il des {Тмн} {М} ? {НЕТ}, il n'y a pas de {Тмн} {М}."),
    "es": dict(
        место_два="hay {n} {Тn} y {m} {Т2m} {М}. ¿{кск2} {Т2мн} hay {М}? hay {m} {Т2m} {М}.",
        класс="{ч} es {к}. ¿qué es {ч}? {ч} es {к}.",
        два_места="hay {n} {Тn} {М} y {m} {Тm} {М2}. ¿dónde hay más {Тмн}? {МБ}.",
        цвет="{X} tiene {n} {Тn} {Ц}. ¿de qué color son {АМ} {Тмн}? {ЦП}.",
        принадлежность="{n} {Тn} {ЕСТЬ2n} {М}. ¿dónde {ЕСТЬ2n} {АМ} {n} {Тn}? {М}.",
        # ZAČIN «¿hay» НЕ ОБЪЯВЛЕН ПАКЕТОМ, «¿es» ОБЪЯВЛЕН: вопрос о наличии ставится
        # вердиктным («¿es verdad que …?»), как и португальский
        есть_ли="hay {n} {Тn} {М}. ¿es verdad que hay {Тмн} {М}? {ДА}, hay {n} {Тn} {М}.",
        нет_ли="no hay {Тмн} {М}. ¿es verdad que hay {Тмн} {М}? {НЕТ}, no hay {Тмн} {М}."),
    "it": dict(
        место_два="{ЕСТЬn} {n} {Тn} e {m} {Т2m} {М}. {quante2} {Т2мн} {ЕСТЬm} {М}? {ЕСТЬm} {m} {Т2m} {М}.",
        класс="{ч} è {к}. che cos'è {ч}? {ч} è {к}.",
        два_места="{ЕСТЬn} {n} {Тn} {М} e {ЕСТЬm} {m} {Тm} {М2}. dove ci sono più {Тмн}? {МБ}.",
        цвет="{X} ha {n} {Тn} {Ц}. di che colore sono {АМ} {Тмн}? {ЦП}.",
        принадлежность="{n} {Тn} {ЕСТЬ2n} {М}. dove {ЕСТЬ2n} {АМ} {n} {Тn}? {М}.",
        есть_ли="{ЕСТЬn} {n} {Тn} {М}. ci sono {Тмн} {М}? {ДА}, {ЕСТЬn} {n} {Тn} {М}.",
        нет_ли="non ci sono {Тмн} {М}. ci sono {Тмн} {М}? {НЕТ}, non ci sono {Тмн} {М}."),
    "pt": dict(
        место_два="há {n} {Тn} e {m} {Т2m} {М}. {quantas2} {Т2мн} há {М}? há {m} {Т2m} {М}.",
        класс="{ч} é {к}. o que é {ч}? {ч} é {к}.",
        два_места="há {n} {Тn} {М} e {m} {Тm} {М2}. onde há mais {Тмн}? {МБ}.",
        цвет="{X} tem {n} {Тn} {Ц}. de que cor são {АМ} {Тмн}? {ЦП}.",
        принадлежность="{n} {Тn} {ЕСТЬ2n} {М}. onde {ЕСТЬ2n} {АМ} {n} {Тn}? {М}.",
        # O ZAČIN «há» НЕ ОБЪЯВЛЕН ПАКЕТОМ, А «é» ОБЪЯВЛЕН: вопрос о наличии ставится
        # вердиктным («é verdade que …?») — и это вторая польза, вердиктная рамка
        есть_ли="há {n} {Тn} {М}. é verdade que há {Тмн} {М}? {ДА}, há {n} {Тn} {М}.",
        нет_ли="não há {Тмн} {М}. é verdade que há {Тмн} {М}? {НЕТ}, não há {Тмн} {М}."),
    "nl": dict(
        место_два="er {ЕСТЬn} {n} {Тn} en {m} {Т2m} {М}. hoeveel {Т2мн} {ЕСТЬm} er {М}? er {ЕСТЬm} {m} {Т2m} {М}.",
        класс="{ч} is {к}. wat is {ч}? {ч} is {к}.",
        два_места="er {ЕСТЬn} {n} {Тn} {М} en er {ЕСТЬm} {m} {Тm} {М2}. waar liggen meer {Тмн}? {МБ}.",
        цвет="{X} heeft {n} {Ц} {Тn}. welke kleur hebben de {Тмн}? {ЦП}.",
        принадлежность="{n} {Тn} {ЕСТЬ2n} {М}. waar {ЕСТЬ2n} de {n} {Тn}? {М}.",
        # ZAČIN «liggen» НЕ ОБЪЯВЛЕН ПАКЕТОМ, «zijn» объявлен — вопрос ставится связкой
        есть_ли="er {ЕСТЬn} {n} {Тn} {М}. zijn er {Тмн} {М}? {ДА}, er {ЕСТЬn} {n} {Тn} {М}.",
        нет_ли="er liggen geen {Тмн} {М}. zijn er {Тмн} {М}? {НЕТ}, er liggen geen {Тмн} {М}."),
    "pl": dict(
        место_два="{М} {ЕСТЬn} {n} {Тn} i {m} {Т2m}. ile {Т2мн} {ЕСТЬm} {М}? {М} {ЕСТЬm} {m} {Т2m}.",
        класс="{ч} to {к}. co to jest {ч}? {ч} to {к}.",
        два_места="{М} {ЕСТЬn} {n} {Тn}, a {М2} {ЕСТЬm} {m} {Тm}. gdzie jest więcej {Тмн}? {МБ}.",
        цвет="{X} ma {n} {Ц} {Тn}. jakiego koloru są {Тим}? {ЦП}.",
        принадлежность="{n} {Тn} {ЕСТЬn} {М}. gdzie {ЕСТЬn} {n} {Тn}? {М}.",
        есть_ли="{М} {ЕСТЬn} {n} {Тn}. czy {М} są {Тим}? {ДА}, {М} {ЕСТЬn} {n} {Тn}.",
        нет_ли="{М} nie ma {Тмн}. czy {М} są {Тим}? {НЕТ}, {М} nie ma {Тмн}."),
}
ФОРМЫ = ("место_два", "класс", "два_места", "цвет", "принадлежность", "есть_ли", "нет_ли")
for _яз in ЯЗЫКИ:
    assert set(РАМКИ[_яз]) == set(ФОРМЫ), (_яз, "frames do not match the forms")


def _связка(язык, n, вопрос=False):
    """The copula of a place for n: the holdings house's tables, plus the Polish count rule."""
    if язык == "pl":
        return СВЯЗКА_PL[_ЯЧЕЙКИ["pl"][n]]
    таблица = HF.ЕСТЬ2 if вопрос else HF.ЕСТЬ
    if язык in таблица:
        return таблица[язык][0 if n == 1 else 1]
    return None


# THE NOMINATIVE PLURAL IS ASKED FOR, AND IT IS NOT THE COUNT FORM. «есть ли монеты на полке?»
# and «jakiego koloru są monety?» want the nominative plural, while the count form of five is the
# genitive («монет», «monet»). Russian declares it in its own house (rugram.именительный_мн);
# Polish writes the nominative plural as the form of two («monety», «książki»); the other
# languages have one plural and it is the same word.
def _именительный_мн(язык, Т):
    if язык == "ru":
        return rugram.именительный_мн(A.ЯЗЫКИ["ru"]["вещи"][Т])
    if язык == "pl":
        return A._вещь("pl", Т, 2)
    return A._вещь(язык, Т, 5)


def _цвет_годен(язык, n):
    """The attributive colour of ru/pl is the genitive plural — the form of «many»; elsewhere
    any plural does («12 rote Bücher», «12 livres rouges»)."""
    if язык in ("ru", "pl"):
        return _ЯЧЕЙКИ[язык][n] == "many"
    return n != 1


def _поля(язык, Т, n, m=None, Т2=None, М=0, М2=1, i=0, ц=0, к=0):
    вещей = len(A.ЯЗЫКИ[язык]["вещи"])
    Т2 = (Т + 1) % вещей if Т2 is None else Т2 % вещей
    if Т2 == Т:
        Т2 = (Т2 + 1) % вещей
    m = n if m is None else m
    вещь = lambda c: A._вещь(язык, Т, c)
    вещь2 = lambda c: A._вещь(язык, Т2, c)
    места = HF.МЕСТА[язык]
    М_, М2_ = места[М % len(места)], места[М2 % len(места)]
    if М2_ == М_:
        М2_ = места[(М2 + 1) % len(места)]
    X = S._лицо(язык, i)
    атр, атр_м, пред = ЦВЕТА[язык][ц % len(ЦВЕТА[язык])]
    член, класс = W.КЛАССЫ[язык][к % len(W.КЛАССЫ[язык])]
    род = S.РОД_ВЕЩЕЙ.get(язык, {}).get(вещь(5), "f")
    род2 = S.РОД_ВЕЩЕЙ.get(язык, {}).get(вещь2(5), "f")
    п = dict(X=X[0], Xр=X[2], n=n, m=m, М=М_, М2=М2_, МБ=(М_ if n > m else М2_),
             Тn=вещь(n), Тm=вещь(m), Тмн=вещь(5), Тим=_именительный_мн(язык, Т),
             Т2m=вещь2(m), Т2мн=вещь2(5),
             Ц=(атр_м if род == "m" else атр), ЦП=пред, ч=член, к=класс,
             # THE FRENCH «QUE» ELIDES BEFORE A VOWEL («qu'est-ce qu'une araignée ?»): the rule
             # is read from the member's first letter, not listed
             ЧТО=("qu'est-ce qu'" if член[:1].lower() in "aeiouyéèàhu" else "qu'est-ce que "),
             ДА=ДА[язык], НЕТ=НЕТ[язык])
    for имя, число, вопрос in (("ЕСТЬn", n, False), ("ЕСТЬm", m, False),
                               ("ЕСТЬ2n", n, True), ("ЕСТЬ2м", m, True)):
        с = _связка(язык, число, вопрос)
        if с is not None:
            п[имя] = с
    if язык in HF.АРТИКЛЬ_МН:
        п["АМ"] = HF.АРТИКЛЬ_МН[язык][0 if род == "m" else 1]
    for дыра, (м_, ж_) in S.РОДОВЫЕ.get(язык, {}).items():
        п[дыра] = м_ if род == "m" else ж_
        п[дыра + "2"] = м_ if род2 == "m" else ж_
    return п


def страница(язык, форма, Т, n, **чем):
    # ЭЛИЗИЯ ПОСЛЕ ПОДСТАНОВКИ: «de œufs» → «d'œufs»
    готовая = РАМКИ[язык][форма].format(**_поля(язык, Т, n, **чем))
    return _fr.элизия(готовая) if язык == "fr" else готовая


def _пара(n):
    """The second number: never the first one, and never equal to it."""
    k = (n * 5 + 7) % ВЕРХ + 1
    return k if k != n else k % ВЕРХ + 1


def _показы():
    вон = {}
    for язык in ЯЗЫКИ:
        вещей = len(A.ЯЗЫКИ[язык]["вещи"])
        лиц = len(A.ЛИЦА[язык])
        мест = len(HF.МЕСТА[язык])
        цветов = len(ЦВЕТА[язык])
        for n in range(1, ВЕРХ + 1):
            m = _пара(n)
            Т = n % вещей
            for сдвиг in (0, 1):
                Тс = (Т + сдвиг * 3) % вещей
                вон[страница(язык, "место_два", Тс, n, m=m, Т2=(Тс + 1 + n % 3) % вещей,
                             М=(n + сдвиг) % мест)] = (язык, "место_два")
                вон[страница(язык, "два_места", Тс, n, m=m, М=(n + сдвиг) % мест,
                             М2=(n + 1 + сдвиг + n % 2) % мест)] = (язык, "два_места")
                вон[страница(язык, "принадлежность", (n * 3 + 1 + сдвиг) % вещей, n,
                             М=(n * 2 + сдвиг) % мест)] = (язык, "принадлежность")
                вон[страница(язык, "есть_ли", (n * 5 + 2 + сдвиг) % вещей, n,
                             М=(n + 2 + сдвиг) % мест)] = (язык, "есть_ли")
            if _цвет_годен(язык, n):
                for ц in range(цветов):
                    вон[страница(язык, "цвет", (n + ц) % вещей, n, i=(n + ц) % лиц,
                                 ц=ц)] = (язык, "цвет")
        for к in range(len(W.КЛАССЫ[язык])):
            вон[страница(язык, "класс", 0, 1, к=к)] = (язык, "класс")
        for Т in range(вещей):
            for М in range(мест):
                вон[страница(язык, "нет_ли", Т, 1, М=М)] = (язык, "нет_ли")
    return вон


ПОКАЗЫ = _показы()

ФОРМЫ_ВЕЩЕЙ = HF.ФОРМЫ_ВЕЩЕЙ
_ДЫРА = re.compile(r"\{([^}]+)\}")
_ALT = lambda слова: "(?:" + "|".join(re.escape(с) for с in sorted({с for с in слова if с}, key=lambda с: (-len(с), с))) + ")"


def _образец(язык, рамка):
    """One pattern over the whole page; the i-th occurrence of a hole is the group «h_hole__i»."""
    лица = [S._лицо(язык, i) for i in range(len(A.ЛИЦА[язык]))]
    связки = {с for n in range(0, ВЕРХ + 2) for в in (False, True) if (с := _связка(язык, n, в))}
    цвета_а = {ц for пара in ЦВЕТА[язык] for ц in пара[:2]}
    цвета_п = {пара[2] for пара in ЦВЕТА[язык]}
    дыры = {"X": _ALT(л[0] for л in лица), "Xр": _ALT(л[2] for л in лица),
            "n": r"\d+", "m": r"\d+",
            "Тn": _ALT(ФОРМЫ_ВЕЩЕЙ[язык]), "Тm": _ALT(ФОРМЫ_ВЕЩЕЙ[язык]),
            "Тмн": _ALT(ФОРМЫ_ВЕЩЕЙ[язык]),
            "Тим": _ALT(_именительный_мн(язык, Т) for Т in range(len(A.ЯЗЫКИ[язык]["вещи"]))),
            "Т2m": _ALT(ФОРМЫ_ВЕЩЕЙ[язык]),
            "Т2мн": _ALT(ФОРМЫ_ВЕЩЕЙ[язык]),
            "М": _ALT(HF.МЕСТА[язык]), "М2": _ALT(HF.МЕСТА[язык]), "МБ": _ALT(HF.МЕСТА[язык]),
            "Ц": _ALT(цвета_а), "ЦП": _ALT(цвета_п),
            "ч": _ALT(ч for ч, _ in W.КЛАССЫ[язык]), "к": _ALT(к for _, к in W.КЛАССЫ[язык]),
            "ДА": re.escape(ДА[язык]), "НЕТ": re.escape(НЕТ[язык]),
            "ЧТО": _ALT(("qu'est-ce qu'", "qu'est-ce que "))}
    for имя in ("ЕСТЬn", "ЕСТЬm", "ЕСТЬ2n", "ЕСТЬ2м"):
        if связки:
            дыры[имя] = _ALT(связки)
    if язык in HF.АРТИКЛЬ_МН:
        дыры["АМ"] = _ALT(HF.АРТИКЛЬ_МН[язык])
    for дыра, пара in S.РОДОВЫЕ.get(язык, {}).items():
        дыры[дыра] = _ALT(пара)
        дыры[дыра + "2"] = _ALT(пара)
    счёт, куски = {}, []
    for кусок in re.split(r"(\{[^}]+\})", рамка):
        if кусок.startswith("{"):
            дыра = кусок[1:-1]
            счёт[дыра] = счёт.get(дыра, 0) + 1
            куски.append(f"(?P<h_{дыра}__{счёт[дыра]}>{дыры[дыра]})")
        else:
            куски.append(_fr.в_образце(кусок) if язык == "fr" else re.escape(кусок))
    return re.compile("^" + "".join(куски) + "$")


ОБРАЗЦЫ = [(_образец(язык, рамка), язык, форма)
           for язык, рамки in РАМКИ.items() for форма, рамка in рамки.items()]


def _вердикт(язык, форма, м):
    значения = {}
    for ключ, v in м.groupdict().items():
        дыра, _ = ключ[2:].rsplit("__", 1)
        if дыра in значения and значения[дыра] != v:
            return False
        значения[дыра] = v
    n = int(значения["n"]) if "n" in значения else None
    m = int(значения["m"]) if "m" in значения else None
    # the count form is the form of its number, and one thing keeps its row
    for дыра, число in (("Тn", n), ("Тm", m), ("Т2m", m)):
        if дыра in значения and число is not None:
            свои = ФОРМЫ_ВЕЩЕЙ[язык].get(значения[дыра], set())
            if not any(A._вещь(язык, Т, число) == значения[дыра] for Т in свои):
                return False
    if "Тмн" in значения and "Тn" in значения:
        if not (ФОРМЫ_ВЕЩЕЙ[язык].get(значения["Тмн"], set()) & ФОРМЫ_ВЕЩЕЙ[язык].get(значения["Тn"], set())):
            return False
    if "Тим" in значения:                          # the nominative plural is of the SAME thing
        свои = {Т for Т in range(len(A.ЯЗЫКИ[язык]["вещи"])) if _именительный_мн(язык, Т) == значения["Тим"]}
        for дыра in ("Тn", "Тмн", "Тm"):
            if дыра in значения and not (свои & ФОРМЫ_ВЕЩЕЙ[язык].get(значения[дыра], set())):
                return False
    if "Тm" in значения and "Тn" in значения:      # two places hold the SAME thing
        if not (ФОРМЫ_ВЕЩЕЙ[язык].get(значения["Тm"], set()) & ФОРМЫ_ВЕЩЕЙ[язык].get(значения["Тn"], set())):
            return False
    if "Т2m" in значения:                          # the second kind is ANOTHER kind
        свои2 = ФОРМЫ_ВЕЩЕЙ[язык].get(значения["Т2m"], set())
        if "Т2мн" in значения and not (свои2 & ФОРМЫ_ВЕЩЕЙ[язык].get(значения["Т2мн"], set())):
            return False
        if "Тn" in значения and (свои2 & ФОРМЫ_ВЕЩЕЙ[язык].get(значения["Тn"], set())):
            return False
    # the copula agrees with its number
    for имя, число, вопрос in (("ЕСТЬn", n, False), ("ЕСТЬm", m, False),
                               ("ЕСТЬ2n", n, True), ("ЕСТЬ2м", m, True)):
        if имя in значения and число is not None:
            с = _связка(язык, число, вопрос)
            if с is not None and значения[имя] != с:
                return False
    # «where are there more» answers with the place of the greater number
    if форма == "два_места" and n is not None and m is not None:
        if n == m:
            return False
        надо = значения["М"] if n > m else значения["М2"]
        if значения.get("МБ") != надо:
            return False
    # the colour of the answer is the colour of the story, and the seam holds
    if форма == "цвет":
        if n is None or not _цвет_годен(язык, n):
            return False
        род = S.РОД_ВЕЩЕЙ.get(язык, {}).get(значения.get("Тмн", ""), "f")
        пара = next((п for п in ЦВЕТА[язык] if значения["ЦП"] == п[2]), None)
        if пара is None:
            return False
        if значения["Ц"] != (пара[1] if род == "m" else пара[0]):
            return False
    # the class of the answer is the class the world-facts house declares for that member
    if форма == "класс":
        свои = {к for ч, к in W.КЛАССЫ[язык] if ч == значения["ч"]}
        if значения["к"] not in свои:
            return False
        if "ЧТО" in значения:
            надо = "qu'est-ce qu'" if значения["ч"][:1].lower() in "aeiouyéèàhu" else "qu'est-ce que "
            if значения["ЧТО"] != надо:
                return False
    if "АМ" in значения and "Тмн" in значения and язык in HF.АРТИКЛЬ_МН:
        род = S.РОД_ВЕЩЕЙ.get(язык, {}).get(значения["Тмн"], "f")
        if значения["АМ"] != HF.АРТИКЛЬ_МН[язык][0 if род == "m" else 1]:
            return False
    for дыра, пара in S.РОДОВЫЕ.get(язык, {}).items():
        if дыра + "2" in значения and "Т2мн" in значения:
            род2 = S.РОД_ВЕЩЕЙ.get(язык, {}).get(значения["Т2мн"], "f")
            if значения[дыра + "2"] != (пара[0] if род2 == "m" else пара[1]):
                return False
    if n is not None and not (1 <= n <= ВЕРХ):
        return False
    return True


def судить(строка):
    """(судимо, истинно): a page of a frame of the house whose holes agree; else silence."""
    с = строка.strip()
    if с in ПОКАЗЫ:
        return True, True
    for образ, язык, форма in ОБРАЗЦЫ:
        м = образ.match(с)
        if м:
            return True, _вердикт(язык, форма, м)
    return False, False


def _хвост(с):
    м = list(re.finditer(r"[?？] ", с))
    return м[-1].end() if м else 0


def _самопроверка():
    for показ in ПОКАЗЫ:
        assert судить(показ) == (True, True), показ
    мутанты = 0
    for язык in ЯЗЫКИ:
        вещей = len(A.ЯЗЫКИ[язык]["вещи"])
        # (1) вопрос о ВТОРОМ роде, отвеченный числом первого
        мд = страница(язык, "место_два", 0, 12, m=5, Т2=1, М=0)
        assert судить(мд) == (True, True), мд
        х = _хвост(мд)
        assert судить(мд[:х] + мд[х:].replace("5", "12", 1)) == (True, False), мд
        # (2) «где больше» отвечено местом меньшего числа
        дм = страница(язык, "два_места", 0, 12, m=5, М=0, М2=1)
        assert судить(дм) == (True, True), дм
        х = _хвост(дм)
        чужое = HF.МЕСТА[язык][1]
        assert судить(дм[:х] + чужое + ".") == (True, False), дм
        # (3) цвет ответа — чужой цвет
        n_ц = next(n for n in range(2, ВЕРХ + 1) if _цвет_годен(язык, n))
        ц = страница(язык, "цвет", 0, n_ц, i=0, ц=0)
        assert судить(ц) == (True, True), ц
        if len(ЦВЕТА[язык]) > 1:
            х = _хвост(ц)
            assert судить(ц[:х] + ЦВЕТА[язык][1][2] + ".") == (True, False), ц
            мутанты += 1
        # (4) место ответа — чужое место
        пр = страница(язык, "принадлежность", 0, 12, М=0)
        assert судить(пр) == (True, True), пр
        х = _хвост(пр)
        assert судить(пр[:х] + HF.МЕСТА[язык][2] + ".") == (True, False), пр
        # (5) «да» при отрицании (полярность ответа против вопроса)
        нл = страница(язык, "нет_ли", 0, 1, М=0)
        assert судить(нл) == (True, True), нл
        х = _хвост(нл)
        assert судить(нл[:х] + нл[х:].replace(НЕТ[язык], ДА[язык], 1)) == (False, False), нл
        # (6) класс чужой вещи
        кл = страница(язык, "класс", 0, 1, к=0)
        assert судить(кл) == (True, True), кл
        свой = W.КЛАССЫ[язык][0][1]
        чужой = next(к for _, к in W.КЛАССЫ[язык] if к != свой)
        assert судить(кл[:_хвост(кл)] + кл[_хвост(кл):].replace(свой, чужой, 1)) == (True, False), кл
        # (7) счётная форма не по числу
        ел = страница(язык, "есть_ли", 0, 12, М=0)
        assert судить(ел) == (True, True), ел
        иная = A._вещь(язык, 0, 1)
        if иная != A._вещь(язык, 0, 12):
            assert судить(ел.replace(A._вещь(язык, 0, 12), иная, 1)) == (True, False), ел
            мутанты += 1
        мутанты += 6
    for язык, форма in (("ru", "место_два"), ("ru", "класс"), ("en", "два_места"), ("de", "цвет"),
                        ("fr", "принадлежность"), ("es", "есть_ли"), ("pl", "нет_ли"),
                        ("it", "место_два"), ("nl", "цвет"), ("pt", "два_места")):
        n = 12 if форма != "цвет" else next(n for n in range(2, ВЕРХ) if _цвет_годен(язык, n))
        print("  ", страница(язык, форма, 0, n, m=5, М=0, М2=1)[:150])
    по_форме = {}
    for _, (_, форма) in ПОКАЗЫ.items():
        по_форме[форма] = по_форме.get(форма, 0) + 1
    по_языку = {}
    for _, (язык, _) in ПОКАЗЫ.items():
        по_языку[язык] = по_языку.get(язык, 0) + 1
    print(f"  мутантов поймано: {мутанты}")
    print(f"  цвета по языкам: " + ", ".join(f"{я} {len(ц)}" for я, ц in ЦВЕТА.items()))
    print(f"  дом пишет показов: {len(ПОКАЗЫ)} (языков {len(ЯЗЫКИ)}, форм {len(ФОРМЫ)}): "
          + ", ".join(f"{ф} {к}" for ф, к in по_форме.items()))
    print(f"  по языкам: " + ", ".join(f"{я} {к}" for я, к in по_языку.items()))


if __name__ == "__main__":
    _самопроверка()
