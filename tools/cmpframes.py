#!/usr/bin/env python3
"""THE HOUSE OF COMPARISON FRAMES — the marker is bought as a frame, not as a word (05.09).

THE DEFECT, MEASURED. On the held-out key of 05.09 twelve of the reader's fifteen lies were one
class: a comparison marker on a non-English page («9 flexiones más que», «in più di», «meer
dan», «więcej niż») answered by a NEIGHBOURING number — 14 + 1 = 15, 22 − 13 = 9 — the marker
itself was never bought, so the number was taken from the row. The SVAMP house shows the
marker on push-ups alone, with bare-number answers, from a table of eight triples; that is a
show of the marker, not a market of it.

WHAT THIS HOUSE SHOWS. Nine languages; two kinds of bearer sentence — a DEED («{X} did n
push-ups», «сделал», «machte», «a fait», «hizo», «ha fatto», «fez», «deed», «zrobił») over deeds
and a HOLDING («{X} has n bottle caps», «у {X} n крышек», «hat», «a», «tiene», «ha», «tem»,
«heeft», «ma») over goods; four frames on each: MORE-BY («{Y} did k more than {X}» → n + k),
LESS-BY (→ n − k), TIMES («twice / three times as many as» → n × m) and HOW-MANY-MORE (the
inverse question: two stories, the difference asked → s − n). Every answer is a FULL SENTENCE
with the bearer, the number and the thing, then the ledger — that is how a verb becomes a
holding verb (holon: the answer's number folds to the story by one choice).

WHAT THE HOUSE DECLARES AND WHAT IT BORROWS. Bearers are the packs' persons through the SVAMP
house's face (the Portuguese article, the Russian genitive of the holding); goods are the
SVAMP house's deed goods with their count forms by the pack's agreement rule (the singular for
1 alone where the language keeps it so); the multiplier words, the past-tense gender of the
Slavic deed verb and the gender of the goods in es/it/pt (the question word and the partitive
bend by it) are declared here. Numbers are twelve pairs OUTSIDE the SVAMP tables, so the
market is bought on numbers the tables never showed.

THE JUDGE RECOMPUTES. A page is a frame whose holes are declared alternations; a repeated hole
carries one value; the ledger's sign is the frame's sign (a MORE frame with a minus in its
ledger is a lie BY SIGN — the very lie the reader tells); the ledger is recomputed from the
story's numbers; the answer's number is the ledger's result; each count form is the form of
its number and every goods form is a form of ONE goods; the question word is the gender of
the goods. The world is CLOSED: a line of no frame is a lie of the world.
"""
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import actionpages as A  # noqa: E402
import svampforms as S  # noqa: E402 — the bearer's face, the deed goods and their count forms

ЯЗЫКИ = ("ru", "en", "de", "fr", "es", "it", "pt", "nl", "pl")
ФОРМЫ = ("больше_на", "меньше_на", "во_столько", "на_сколько")
ГРУППЫ = ("дело", "держание")
ТОВАРЫ = {"дело": ("отжимания", "скручивания"),
          "держание": ("крышки", "фигурки", "мелки", "розы", "игры", "приложения")}
# TWELVE PAIRS OUTSIDE THE SVAMP TABLES: (n, k), n > k; the TIMES frame multiplies n by 2 or 3
ПАРЫ = ((16, 7), (22, 9), (26, 11), (28, 13), (32, 14), (36, 15),
        (42, 17), (27, 8), (33, 12), (38, 19), (21, 6), (45, 18))
_ПЕРВЫЕ_SVAMP = {п[0] for п in S.ЧИСЛА} | {п[0] for п in S.ЧИСЛА_АКТОВ}
for _n, _k in ПАРЫ:
    assert _n > _k >= 1 and _n not in _ПЕРВЫЕ_SVAMP, (_n, _k, "the SVAMP tables show this number first")
    assert (_n, _k) not in S.ЧИСЛА and all(т[:2] != (_n, _k) for т in S.ЧИСЛА_АКТОВ), (_n, _k)
ЗНАК = {"больше_на": "+", "меньше_на": "−", "во_столько": "×", "на_сколько": "−"}
КРАТ = {"ru": {2: "вдвое", 3: "втрое"}, "en": {2: "twice", 3: "three times"}, "de": {2: "zweimal", 3: "dreimal"},
        "fr": {2: "deux fois", 3: "trois fois"}, "es": {2: "el doble", 3: "el triple"}, "it": {2: "il doppio", 3: "il triplo"},
        "pt": {2: "o dobro", 3: "o triplo"}, "nl": {2: "twee keer", 3: "drie keer"}, "pl": {2: "dwa razy", 3: "trzy razy"}}
# THE SLAVIC DEED VERB BENDS BY THE BEARER'S GENDER in the past («сделал»/«сделала», «zrobił»/«zrobiła»)
ГЛАГОЛ_ДЕЛА = {"ru": "сделал", "pl": "zrobił"}
# THE GENDER OF THE GOODS where the question word bends by it (the plural form → gender)
РОД = {"es": {"flexiones": "f", "abdominales": "m", "chapas": "f", "figuras": "f", "lápices de colores": "m",
              "rosas": "f", "partidas": "f", "aplicaciones": "f"},
       "it": {"flessioni": "f", "addominali": "m", "tappi": "m", "statuine": "f", "pastelli": "m",
              "rose": "f", "partite": "f", "app": "f"},
       "pt": {"flexões": "f", "abdominais": "m", "tampas": "f", "bonecos": "m", "lápis de cor": "m",
              "rosas": "f", "jogos": "m", "aplicações": "f"}}
РОДОВЫЕ = {"es": {"кск": ("cuántos", "cuántas")},
           "it": {"quante": ("quanti", "quante"), "delle": ("dei", "delle")},
           "pt": {"quantas": ("quantos", "quantas"), "das": ("dos", "das")}}

# THE FRAMES: {X} {Y} bearers, {Xр} {Yр} their genitives (the Russian holding), {В} {ВY} the deed verb bent
# by gender, {n} {k} {s} {r} {p} {m} numbers, {Тc} the goods in the count form of c, {Тмн} the plural,
# {КРАТ} the multiplier word, {знак} the ledger's sign, gender holes by the goods
РАМКИ = {
    "ru": {
        "дело": dict(
            больше_на="{X} {В} {n} {Тn}. {Y} {ВY} на {k} {Тk} больше, чем {X}. сколько {Тмн} {ВY} {Y}? {Y} {ВY} {s} {Тs}: {n} {знак} {k} = {s}.",
            меньше_на="{X} {В} {n} {Тn}. {Y} {ВY} на {k} {Тk} меньше, чем {X}. сколько {Тмн} {ВY} {Y}? {Y} {ВY} {r} {Тr}: {n} {знак} {k} = {r}.",
            во_столько="{X} {В} {n} {Тn}. {Y} {ВY} {КРАТ} больше {Тмн}, чем {X}. сколько {Тмн} {ВY} {Y}? {Y} {ВY} {p} {Тp}: {n} {знак} {m} = {p}.",
            на_сколько="{X} {В} {n} {Тn}. {Y} {ВY} {s} {Тs}. на сколько больше {Тмн} {ВY} {Y}, чем {X}? на {k} {Тk} больше: {s} {знак} {n} = {k}."),
        "держание": dict(
            больше_на="у {Xр} {n} {Тn}. у {Yр} на {k} {Тk} больше, чем у {Xр}. сколько {Тмн} у {Yр}? у {Yр} {s} {Тs}: {n} {знак} {k} = {s}.",
            меньше_на="у {Xр} {n} {Тn}. у {Yр} на {k} {Тk} меньше, чем у {Xр}. сколько {Тмн} у {Yр}? у {Yр} {r} {Тr}: {n} {знак} {k} = {r}.",
            во_столько="у {Xр} {n} {Тn}. у {Yр} {КРАТ} больше {Тмн}, чем у {Xр}. сколько {Тмн} у {Yр}? у {Yр} {p} {Тp}: {n} {знак} {m} = {p}.",
            на_сколько="у {Xр} {n} {Тn}. у {Yр} {s} {Тs}. на сколько больше {Тмн} у {Yр}, чем у {Xр}? на {k} {Тk} больше: {s} {знак} {n} = {k}."),
    },
    "en": {
        "дело": dict(
            больше_на="{X} did {n} {Тn}. {Y} did {k} more {Тмн} than {X}. how many {Тмн} did {Y} do? {Y} did {s} {Тs}: {n} {знак} {k} = {s}.",
            меньше_на="{X} did {n} {Тn}. {Y} did {k} fewer {Тмн} than {X}. how many {Тмн} did {Y} do? {Y} did {r} {Тr}: {n} {знак} {k} = {r}.",
            во_столько="{X} did {n} {Тn}. {Y} did {КРАТ} as many {Тмн} as {X}. how many {Тмн} did {Y} do? {Y} did {p} {Тp}: {n} {знак} {m} = {p}.",
            на_сколько="{X} did {n} {Тn}. {Y} did {s} {Тs}. how many more {Тмн} did {Y} do than {X}? {k} more {Тмн}: {s} {знак} {n} = {k}."),
        "держание": dict(
            больше_на="{X} has {n} {Тn}. {Y} has {k} more {Тмн} than {X}. how many {Тмн} does {Y} have? {Y} has {s} {Тs}: {n} {знак} {k} = {s}.",
            меньше_на="{X} has {n} {Тn}. {Y} has {k} fewer {Тмн} than {X}. how many {Тмн} does {Y} have? {Y} has {r} {Тr}: {n} {знак} {k} = {r}.",
            во_столько="{X} has {n} {Тn}. {Y} has {КРАТ} as many {Тмн} as {X}. how many {Тмн} does {Y} have? {Y} has {p} {Тp}: {n} {знак} {m} = {p}.",
            на_сколько="{X} has {n} {Тn}. {Y} has {s} {Тs}. how many more {Тмн} does {Y} have than {X}? {k} more {Тмн}: {s} {знак} {n} = {k}."),
    },
    "de": {
        "дело": dict(
            больше_на="{X} machte {n} {Тn}. {Y} machte {k} {Тмн} mehr als {X}. wie viele {Тмн} machte {Y}? {Y} machte {s} {Тs}: {n} {знак} {k} = {s}.",
            меньше_на="{X} machte {n} {Тn}. {Y} machte {k} {Тмн} weniger als {X}. wie viele {Тмн} machte {Y}? {Y} machte {r} {Тr}: {n} {знак} {k} = {r}.",
            во_столько="{X} machte {n} {Тn}. {Y} machte {КРАТ} so viele {Тмн} wie {X}. wie viele {Тмн} machte {Y}? {Y} machte {p} {Тp}: {n} {знак} {m} = {p}.",
            на_сколько="{X} machte {n} {Тn}. {Y} machte {s} {Тs}. wie viele {Тмн} mehr machte {Y} als {X}? {k} {Тмн} mehr: {s} {знак} {n} = {k}."),
        "держание": dict(
            больше_на="{X} hat {n} {Тn}. {Y} hat {k} {Тмн} mehr als {X}. wie viele {Тмн} hat {Y}? {Y} hat {s} {Тs}: {n} {знак} {k} = {s}.",
            меньше_на="{X} hat {n} {Тn}. {Y} hat {k} {Тмн} weniger als {X}. wie viele {Тмн} hat {Y}? {Y} hat {r} {Тr}: {n} {знак} {k} = {r}.",
            во_столько="{X} hat {n} {Тn}. {Y} hat {КРАТ} so viele {Тмн} wie {X}. wie viele {Тмн} hat {Y}? {Y} hat {p} {Тp}: {n} {знак} {m} = {p}.",
            на_сколько="{X} hat {n} {Тn}. {Y} hat {s} {Тs}. wie viele {Тмн} mehr hat {Y} als {X}? {k} {Тмн} mehr: {s} {знак} {n} = {k}."),
    },
    "fr": {
        "дело": dict(
            больше_на="{X} a fait {n} {Тn}. {Y} a fait {k} {Тмн} de plus que {X}. combien de {Тмн} a fait {Y} ? {Y} a fait {s} {Тs} : {n} {знак} {k} = {s}.",
            меньше_на="{X} a fait {n} {Тn}. {Y} a fait {k} {Тмн} de moins que {X}. combien de {Тмн} a fait {Y} ? {Y} a fait {r} {Тr} : {n} {знак} {k} = {r}.",
            во_столько="{X} a fait {n} {Тn}. {Y} a fait {КРАТ} plus de {Тмн} que {X}. combien de {Тмн} a fait {Y} ? {Y} a fait {p} {Тp} : {n} {знак} {m} = {p}.",
            на_сколько="{X} a fait {n} {Тn}. {Y} a fait {s} {Тs}. combien de {Тмн} de plus a fait {Y} que {X} ? {k} {Тмн} de plus : {s} {знак} {n} = {k}."),
        "держание": dict(
            больше_на="{X} a {n} {Тn}. {Y} a {k} {Тмн} de plus que {X}. combien de {Тмн} a {Y} ? {Y} a {s} {Тs} : {n} {знак} {k} = {s}.",
            меньше_на="{X} a {n} {Тn}. {Y} a {k} {Тмн} de moins que {X}. combien de {Тмн} a {Y} ? {Y} a {r} {Тr} : {n} {знак} {k} = {r}.",
            во_столько="{X} a {n} {Тn}. {Y} a {КРАТ} plus de {Тмн} que {X}. combien de {Тмн} a {Y} ? {Y} a {p} {Тp} : {n} {знак} {m} = {p}.",
            на_сколько="{X} a {n} {Тn}. {Y} a {s} {Тs}. combien de {Тмн} de plus a {Y} que {X} ? {k} {Тмн} de plus : {s} {знак} {n} = {k}."),
    },
    "es": {
        "дело": dict(
            больше_на="{X} hizo {n} {Тn}. {Y} hizo {k} {Тмн} más que {X}. ¿{кск} {Тмн} hizo {Y}? {Y} hizo {s} {Тs}: {n} {знак} {k} = {s}.",
            меньше_на="{X} hizo {n} {Тn}. {Y} hizo {k} {Тмн} menos que {X}. ¿{кск} {Тмн} hizo {Y}? {Y} hizo {r} {Тr}: {n} {знак} {k} = {r}.",
            во_столько="{X} hizo {n} {Тn}. {Y} hizo {КРАТ} de {Тмн} que {X}. ¿{кск} {Тмн} hizo {Y}? {Y} hizo {p} {Тp}: {n} {знак} {m} = {p}.",
            на_сколько="{X} hizo {n} {Тn}. {Y} hizo {s} {Тs}. ¿{кск} {Тмн} más hizo {Y} que {X}? {k} {Тмн} más: {s} {знак} {n} = {k}."),
        "держание": dict(
            больше_на="{X} tiene {n} {Тn}. {Y} tiene {k} {Тмн} más que {X}. ¿{кск} {Тмн} tiene {Y}? {Y} tiene {s} {Тs}: {n} {знак} {k} = {s}.",
            меньше_на="{X} tiene {n} {Тn}. {Y} tiene {k} {Тмн} menos que {X}. ¿{кск} {Тмн} tiene {Y}? {Y} tiene {r} {Тr}: {n} {знак} {k} = {r}.",
            во_столько="{X} tiene {n} {Тn}. {Y} tiene {КРАТ} de {Тмн} que {X}. ¿{кск} {Тмн} tiene {Y}? {Y} tiene {p} {Тp}: {n} {знак} {m} = {p}.",
            на_сколько="{X} tiene {n} {Тn}. {Y} tiene {s} {Тs}. ¿{кск} {Тмн} más tiene {Y} que {X}? {k} {Тмн} más: {s} {знак} {n} = {k}."),
    },
    "it": {
        "дело": dict(
            больше_на="{X} ha fatto {n} {Тn}. {Y} ha fatto {k} {Тмн} in più di {X}. {quante} {Тмн} ha fatto {Y}? {Y} ha fatto {s} {Тs}: {n} {знак} {k} = {s}.",
            меньше_на="{X} ha fatto {n} {Тn}. {Y} ha fatto {k} {Тмн} in meno di {X}. {quante} {Тмн} ha fatto {Y}? {Y} ha fatto {r} {Тr}: {n} {знак} {k} = {r}.",
            во_столько="{X} ha fatto {n} {Тn}. {Y} ha fatto {КРАТ} {delle} {Тмн} di {X}. {quante} {Тмн} ha fatto {Y}? {Y} ha fatto {p} {Тp}: {n} {знак} {m} = {p}.",
            на_сколько="{X} ha fatto {n} {Тn}. {Y} ha fatto {s} {Тs}. {quante} {Тмн} in più ha fatto {Y} di {X}? {k} {Тмн} in più: {s} {знак} {n} = {k}."),
        "держание": dict(
            больше_на="{X} ha {n} {Тn}. {Y} ha {k} {Тмн} in più di {X}. {quante} {Тмн} ha {Y}? {Y} ha {s} {Тs}: {n} {знак} {k} = {s}.",
            меньше_на="{X} ha {n} {Тn}. {Y} ha {k} {Тмн} in meno di {X}. {quante} {Тмн} ha {Y}? {Y} ha {r} {Тr}: {n} {знак} {k} = {r}.",
            во_столько="{X} ha {n} {Тn}. {Y} ha {КРАТ} {delle} {Тмн} di {X}. {quante} {Тмн} ha {Y}? {Y} ha {p} {Тp}: {n} {знак} {m} = {p}.",
            на_сколько="{X} ha {n} {Тn}. {Y} ha {s} {Тs}. {quante} {Тмн} in più ha {Y} di {X}? {k} {Тмн} in più: {s} {знак} {n} = {k}."),
    },
    "pt": {
        "дело": dict(
            больше_на="{X} fez {n} {Тn}. {Y} fez mais {k} {Тмн} do que {X}. {quantas} {Тмн} fez {Y}? {Y} fez {s} {Тs}: {n} {знак} {k} = {s}.",
            меньше_на="{X} fez {n} {Тn}. {Y} fez menos {k} {Тмн} do que {X}. {quantas} {Тмн} fez {Y}? {Y} fez {r} {Тr}: {n} {знак} {k} = {r}.",
            во_столько="{X} fez {n} {Тn}. {Y} fez {КРАТ} {das} {Тмн} de {X}. {quantas} {Тмн} fez {Y}? {Y} fez {p} {Тp}: {n} {знак} {m} = {p}.",
            на_сколько="{X} fez {n} {Тn}. {Y} fez {s} {Тs}. {quantas} {Тмн} a mais fez {Y} do que {X}? mais {k} {Тмн}: {s} {знак} {n} = {k}."),
        "держание": dict(
            больше_на="{X} tem {n} {Тn}. {Y} tem mais {k} {Тмн} do que {X}. {quantas} {Тмн} tem {Y}? {Y} tem {s} {Тs}: {n} {знак} {k} = {s}.",
            меньше_на="{X} tem {n} {Тn}. {Y} tem menos {k} {Тмн} do que {X}. {quantas} {Тмн} tem {Y}? {Y} tem {r} {Тr}: {n} {знак} {k} = {r}.",
            во_столько="{X} tem {n} {Тn}. {Y} tem {КРАТ} {das} {Тмн} de {X}. {quantas} {Тмн} tem {Y}? {Y} tem {p} {Тp}: {n} {знак} {m} = {p}.",
            на_сколько="{X} tem {n} {Тn}. {Y} tem {s} {Тs}. {quantas} {Тмн} a mais tem {Y} do que {X}? mais {k} {Тмн}: {s} {знак} {n} = {k}."),
    },
    "nl": {
        "дело": dict(
            больше_на="{X} deed {n} {Тn}. {Y} deed {k} {Тмн} meer dan {X}. hoeveel {Тмн} deed {Y}? {Y} deed {s} {Тs}: {n} {знак} {k} = {s}.",
            меньше_на="{X} deed {n} {Тn}. {Y} deed {k} {Тмн} minder dan {X}. hoeveel {Тмн} deed {Y}? {Y} deed {r} {Тr}: {n} {знак} {k} = {r}.",
            во_столько="{X} deed {n} {Тn}. {Y} deed {КРАТ} zoveel {Тмн} als {X}. hoeveel {Тмн} deed {Y}? {Y} deed {p} {Тp}: {n} {знак} {m} = {p}.",
            на_сколько="{X} deed {n} {Тn}. {Y} deed {s} {Тs}. hoeveel {Тмн} meer deed {Y} dan {X}? {k} {Тмн} meer: {s} {знак} {n} = {k}."),
        "держание": dict(
            больше_на="{X} heeft {n} {Тn}. {Y} heeft {k} {Тмн} meer dan {X}. hoeveel {Тмн} heeft {Y}? {Y} heeft {s} {Тs}: {n} {знак} {k} = {s}.",
            меньше_на="{X} heeft {n} {Тn}. {Y} heeft {k} {Тмн} minder dan {X}. hoeveel {Тмн} heeft {Y}? {Y} heeft {r} {Тr}: {n} {знак} {k} = {r}.",
            во_столько="{X} heeft {n} {Тn}. {Y} heeft {КРАТ} zoveel {Тмн} als {X}. hoeveel {Тмн} heeft {Y}? {Y} heeft {p} {Тp}: {n} {знак} {m} = {p}.",
            на_сколько="{X} heeft {n} {Тn}. {Y} heeft {s} {Тs}. hoeveel {Тмн} meer heeft {Y} dan {X}? {k} {Тмн} meer: {s} {знак} {n} = {k}."),
    },
    "pl": {
        "дело": dict(
            больше_на="{X} {В} {n} {Тn}. {Y} {ВY} o {k} {Тk} więcej niż {X}. ile {Тмн} {ВY} {Y}? {Y} {ВY} {s} {Тs}: {n} {знак} {k} = {s}.",
            меньше_на="{X} {В} {n} {Тn}. {Y} {ВY} o {k} {Тk} mniej niż {X}. ile {Тмн} {ВY} {Y}? {Y} {ВY} {r} {Тr}: {n} {знак} {k} = {r}.",
            во_столько="{X} {В} {n} {Тn}. {Y} {ВY} {КРАТ} więcej {Тмн} niż {X}. ile {Тмн} {ВY} {Y}? {Y} {ВY} {p} {Тp}: {n} {знак} {m} = {p}.",
            на_сколько="{X} {В} {n} {Тn}. {Y} {ВY} {s} {Тs}. o ile więcej {Тмн} {ВY} {Y} niż {X}? o {k} {Тk} więcej: {s} {знак} {n} = {k}."),
        "держание": dict(
            больше_на="{X} ma {n} {Тn}. {Y} ma o {k} {Тk} więcej niż {X}. ile {Тмн} ma {Y}? {Y} ma {s} {Тs}: {n} {знак} {k} = {s}.",
            меньше_на="{X} ma {n} {Тn}. {Y} ma o {k} {Тk} mniej niż {X}. ile {Тмн} ma {Y}? {Y} ma {r} {Тr}: {n} {знак} {k} = {r}.",
            во_столько="{X} ma {n} {Тn}. {Y} ma {КРАТ} więcej {Тмн} niż {X}. ile {Тмн} ma {Y}? {Y} ma {p} {Тp}: {n} {знак} {m} = {p}.",
            на_сколько="{X} ma {n} {Тn}. {Y} ma {s} {Тs}. o ile więcej {Тмн} ma {Y} niż {X}? o {k} {Тk} więcej: {s} {знак} {n} = {k}."),
    },
}


def _товар(язык, ключ, c):
    """The goods in the count form of c — the SVAMP house's forms, the pack's rule."""
    return S._товар_форма(язык, ключ, c)


def _поля(язык, группа, i, j, ключ, n, k, m):
    X, Y = S._лицо(язык, i), S._лицо(язык, j)
    if Y[0] == X[0]:
        Y = S._лицо(язык, j + 1)
    s, r, p = n + k, n - k, n * m
    п = dict(X=X[0], Xр=X[2], Y=Y[0], Yр=Y[2], n=n, k=k, s=s, r=r, p=p, m=m,
             Тn=_товар(язык, ключ, n), Тk=_товар(язык, ключ, k), Тs=_товар(язык, ключ, s),
             Тr=_товар(язык, ключ, r), Тp=_товар(язык, ключ, p), Тмн=S.ТОВАРЫ_АКТОВ[язык][ключ][-1],
             КРАТ=КРАТ[язык][m])
    if язык in ГЛАГОЛ_ДЕЛА:
        п["В"] = ГЛАГОЛ_ДЕЛА[язык] + A._а(язык, X[1])
        п["ВY"] = ГЛАГОЛ_ДЕЛА[язык] + A._а(язык, Y[1])
    род = РОД.get(язык, {}).get(п["Тмн"], "f")
    for дыра, (м_, ж_) in РОДОВЫЕ.get(язык, {}).items():
        п[дыра] = м_ if род == "m" else ж_
    return п


def страница(язык, группа, форма, i, j, ключ, n, k, m=2):
    п = _поля(язык, группа, i, j, ключ, n, k, m)
    п["знак"] = ЗНАК[форма]
    return РАМКИ[язык][группа][форма].format(**п)


def _показы():
    вон = {}
    for язык in ЯЗЫКИ:
        лиц = len(A.ЛИЦА[язык])
        for группа in ГРУППЫ:
            for g, ключ in enumerate(ТОВАРЫ[группа]):
                for q, (n, k) in enumerate(ПАРЫ):
                    i, j = (q + g) % лиц, (q * 3 + 1 + g) % лиц
                    m = 2 if (q + g) % 2 == 0 else 3
                    for форма in ФОРМЫ:
                        вон[страница(язык, группа, форма, i, j, ключ, n, k, m)] = (язык, группа, форма)
    return вон


ПОКАЗЫ = _показы()

# THE JUDGE
ВЕРХ_ФОРМ = 200


def _формы_товаров(язык):
    """form → the goods keys wearing it, over every count the house can write."""
    вон = {}
    for группа in ГРУППЫ:
        for ключ in ТОВАРЫ[группа]:
            for c in range(1, ВЕРХ_ФОРМ):
                вон.setdefault(_товар(язык, ключ, c), set()).add(ключ)
            вон.setdefault(S.ТОВАРЫ_АКТОВ[язык][ключ][-1], set()).add(ключ)
    return вон


ФОРМЫ_ТОВАРОВ = {язык: _формы_товаров(язык) for язык in ЯЗЫКИ}
_КРАТНОСТЬ = {язык: {слово: m for m, слово in кр.items()} for язык, кр in КРАТ.items()}


def _alt(слова):
    return "(?:" + "|".join(re.escape(с) for с in sorted({с for с in слова if с}, key=lambda с: (-len(с), с))) + ")"


def _образец(язык, рамка):
    """One anchored pattern over the page; the i-th occurrence of a hole is the group «h_hole__i»."""
    лица = [S._лицо(язык, i) for i in range(len(A.ЛИЦА[язык]))]
    имена, род = _alt(л[0] for л in лица), _alt(л[2] for л in лица)
    товары = _alt(ФОРМЫ_ТОВАРОВ[язык])
    глагол = _alt([ГЛАГОЛ_ДЕЛА[язык], ГЛАГОЛ_ДЕЛА[язык] + A._а(язык, "f")]) if язык in ГЛАГОЛ_ДЕЛА else None
    дыры = {"X": имена, "Y": имена, "Xр": род, "Yр": род, "n": r"\d+", "k": r"\d+", "s": r"\d+", "r": r"\d+",
            "p": r"\d+", "m": r"\d+", "Тn": товары, "Тk": товары, "Тs": товары, "Тr": товары, "Тp": товары,
            "Тмн": товары, "КРАТ": _alt(КРАТ[язык].values()), "знак": r"[+−×]", "В": глагол, "ВY": глагол}
    for дыра, пара in РОДОВЫЕ.get(язык, {}).items():
        дыры[дыра] = _alt(пара)
    счёт, куски = {}, []
    for кусок in re.split(r"(\{[^}]+\})", рамка):
        if кусок.startswith("{"):
            дыра = кусок[1:-1]
            счёт[дыра] = счёт.get(дыра, 0) + 1
            куски.append(f"(?P<h_{дыра}__{счёт[дыра]}>{дыры[дыра]})")
        else:
            куски.append(re.escape(кусок))
    return re.compile("^" + "".join(куски) + "$")


ОБРАЗЦЫ = [(_образец(язык, рамка), язык, группа, форма)
           for язык, группы in РАМКИ.items() for группа, рамки in группы.items() for форма, рамка in рамки.items()]


def _вердикт(язык, группа, форма, м):
    """Repeated holes agree; the sign is the frame's; the ledger recomputes; the answer is the
    ledger's result; every goods form is the form of its number and of one goods; the question
    word bends by the goods' gender."""
    з = {}
    for ключ, v in м.groupdict().items():
        дыра = ключ[2:].rsplit("__", 1)[0]
        if дыра in з and з[дыра] != v:
            return False
        з[дыра] = v
    if з["знак"] != ЗНАК[форма]:
        return False
    ч = {д: int(з[д]) for д in ("n", "k", "s", "r", "p", "m") if д in з}
    if any(v < 1 for v in ч.values()):
        return False
    if форма == "больше_на" and ч["s"] != ч["n"] + ч["k"]:
        return False
    if форма == "меньше_на" and ч["r"] != ч["n"] - ч["k"]:
        return False
    if форма == "во_столько" and (ч["p"] != ч["n"] * ч["m"] or _КРАТНОСТЬ[язык].get(з["КРАТ"]) != ч["m"]):
        return False
    if форма == "на_сколько" and ч["k"] != ч["s"] - ч["n"]:
        return False
    # one goods wears every goods form of the page, each in the form of its number
    ключи = set(ФОРМЫ_ТОВАРОВ[язык].get(з["Тмн"], ()))
    for д in ("Тn", "Тk", "Тs", "Тr", "Тp"):
        if д in з:
            c = ч[д[1]]
            ключи &= {кл for кл in ФОРМЫ_ТОВАРОВ[язык].get(з[д], ()) if _товар(язык, кл, c) == з[д]}
    if not ключи or not any(S.ТОВАРЫ_АКТОВ[язык][кл][-1] == з["Тмн"] for кл in ключи):
        return False
    if not any(кл in ТОВАРЫ[группа] for кл in ключи):
        return False
    род = РОД.get(язык, {}).get(з["Тмн"], "f")
    for дыра, пара in РОДОВЫЕ.get(язык, {}).items():
        if дыра in з and з[дыра] != (пара[0] if род == "m" else пара[1]):
            return False
    return True


def судить(строка):
    """(судимо, истинно): a page of a frame of the house whose holes agree and whose ledger
    recomputes; silence on anything else (the closed world's gate makes it a lie)."""
    с = строка.strip()
    if с in ПОКАЗЫ:
        return True, True
    for образ, язык, группа, форма in ОБРАЗЦЫ:
        м = образ.match(с)
        if м:
            return True, _вердикт(язык, группа, форма, м)
    return False, False


_ПОСЛ_ЧИСЛО = re.compile(r"(\d+)(?=[^\d]*$)")


def _самопроверка():
    for показ in ПОКАЗЫ:
        assert судить(показ) == (True, True), показ
    мутанты = 0
    for язык in ЯЗЫКИ:
        for группа in ГРУППЫ:
            ключ = ТОВАРЫ[группа][0]
            б = страница(язык, группа, "больше_на", 0, 3, ключ, 16, 7)
            # (1) the ledger does not add up: its result is off, the answer's number with it
            assert судить(б.replace("23", "24")) == (True, False), б
            # (2) the answer's number is not the ledger's result
            assert судить(_ПОСЛ_ЧИСЛО.sub("24", б)) == (True, False), б
            # (3) the LIE BY SIGN: a MORE frame whose ledger subtracts (the reader's own lie)
            знаковая = б.replace("23", "9").replace(" + ", " − ")
            assert судить(знаковая) == (True, False), знаковая
            # (4) a count form not of its number: the answer's goods in the form of 1
            один = _товар(язык, ключ, 1)
            if один != _товар(язык, ключ, 23):
                битая = б[:б.rfind("?")] + б[б.rfind("?"):].replace(_товар(язык, ключ, 23), один, 1)
                assert судить(битая) == (True, False), битая
                мутанты += 1
            # (5) a foreign bearer: silence of the house, a lie at the closed world's gate
            X = S._лицо(язык, 0)
            assert судить(б.replace(X[0], "Zorbo").replace(X[2], "Zorbo")) == (False, False), б
            # (6) TIMES with the wrong multiplier in the ledger
            в = страница(язык, группа, "во_столько", 1, 4, ключ, 22, 9, 2)
            assert судить(в) == (True, True), в
            assert судить(в.replace(" × 2 = 44", " × 3 = 44")) == (True, False), в
            assert судить(в.replace(" × 2 = 44", " × 3 = 66").replace("66 ", "66 ", 1)) in ((True, False), (False, False)), в
            # (7) HOW-MANY-MORE answered with the sum
            н = страница(язык, группа, "на_сколько", 2, 5, ключ, 26, 11)
            assert судить(н) == (True, True), н
            assert судить(н.replace(" − ", " + ")) == (True, False), н
            мутанты += 6
        # (8) the question word of the wrong gender (es/it/pt)
        for дыра, пара in РОДОВЫЕ.get(язык, {}).items():
            б = страница(язык, "дело", "во_столько", 0, 3, "отжимания", 16, 7, 2)
            стоит = next((с for с in пара if f" {с} " in б), None)
            if стоит is None:
                continue
            другое = пара[1] if стоит == пара[0] else пара[0]
            assert судить(б.replace(f" {стоит} ", f" {другое} ")) == (True, False), б
            мутанты += 1
    print("  ", страница("ru", "дело", "больше_на", 0, 3, "отжимания", 16, 7))
    print("  ", страница("es", "дело", "меньше_на", 1, 4, "отжимания", 22, 9))
    print("  ", страница("it", "держание", "во_столько", 2, 5, "крышки", 26, 11, 2))
    print("  ", страница("pl", "дело", "на_сколько", 3, 6, "скручивания", 28, 13))
    print("  ", страница("pt", "держание", "больше_на", 0, 3, "фигурки", 32, 14))
    print("  ", страница("nl", "держание", "меньше_на", 1, 4, "мелки", 36, 15))
    print(f"  мутантов поймано: {мутанты}")
    по_форме, по_языку = {}, {}
    for _, (язык, группа, форма) in ПОКАЗЫ.items():
        по_форме[форма] = по_форме.get(форма, 0) + 1
        по_языку[язык] = по_языку.get(язык, 0) + 1
    print(f"  дом пишет показов: {len(ПОКАЗЫ)} (языков {len(ЯЗЫКИ)}, групп {len(ГРУППЫ)}, форм {len(ФОРМЫ)}): "
          + ", ".join(f"{ф} {к}" for ф, к in по_форме.items()) + "; по языкам "
          + ", ".join(f"{я} {к}" for я, к in по_языку.items()))


if __name__ == "__main__":
    _самопроверка()
