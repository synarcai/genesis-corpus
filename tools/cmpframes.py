#!/usr/bin/env python3
"""THE HOUSE OF COMPARISON FRAMES — the marker is bought as a frame, not as a word (05.09).

THE DEFECT, MEASURED. On the held-out key of 05.09 twelve of the reader's fifteen lies were one
class: a comparison marker on a non-English page («9 … más que», «in più di», «meer dan»,
«więcej niż») answered by a NEIGHBOURING number — 14 + 1 = 15, 22 − 13 = 9 — the marker itself
was never bought, so the number was taken from the row. The house of story shapes showed the
marker on one deed alone, with bare-number answers, from a table of eight triples; that is a
show of the marker, not a market of it.

WHAT THIS HOUSE SHOWS. Nine languages; two kinds of bearer sentence — a DEED («{X} planted n
oaks», «посадил», «pflanzte», «a planté», «plantó», «ha piantato», «plantou», «plantte»,
«posadził») over the planted trees, and a HOLDING («{X} has n jars», «у {X} n банок», «hat»,
«a», «tiene», «ha», «tem», «heeft», «ma») over goods; four frames on each: MORE-BY («{Y} planted
k more than {X}» → n + k), LESS-BY (→ n − k), TIMES («twice / three times as many as» → n × m)
and HOW-MANY-MORE (the inverse question: two stories, the difference asked → s − n). Every
answer is a FULL SENTENCE with the bearer, the number and the thing, then the ledger — that is
how a verb becomes a holding verb (holon: the answer's number folds to the story by one choice).

THE SCENES ARE OUR OWN (23.09, the owner's word: a public band is an instrument, never a
source). Until 23.09 the deed was the band's own exercise and the holdings its own goods; the
construction stays, the scene is the story house's rewritten one — trees planted, jars,
mushrooms, pears, stamps, nuts and photos held.

WHAT THE HOUSE DECLARES AND WHAT IT BORROWS. Bearers are the packs' persons through the story
house's face (the Portuguese article, the Russian genitive of the holding); goods are the story
house's act goods with their count forms by the pack's agreement rule (the singular for 1 alone
where the language keeps it so) and their gender in es/it/pt from its one table
(`svampforms.РОД_ТОВАРА_АКТОВ`: the question word and the partitive bend by it); the multiplier
words and the past-tense gender of the Slavic deed verb are declared here. Numbers are twelve
pairs OUTSIDE the story house's tables, so the market is bought on numbers the tables never
showed.

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
import frgram as _fr  # noqa: E402 — французская элизия: один закон, два читателя
import rugram as _RUG  # noqa: E402 — закон русского прошедшего: род формы при лице
import svampforms as S  # noqa: E402 — the bearer's face, the act goods, their count forms and gender

ЯЗЫКИ = ("ru", "en", "de", "fr", "es", "it", "pt", "nl", "pl")
ФОРМЫ = ("больше_на", "меньше_на", "во_столько", "на_сколько",
         # WAVE 2 (05.09): the answer is a NAME, an equality or a multiplicity — comparison
         # without arithmetic in three of the four, and the inverse of TIMES in the fourth
         "кто_больше", "кто_меньше", "поровну", "во_сколько_раз")
ГРУППЫ = ("дело", "держание")
ТОВАРЫ = {"дело": ("дубы", "берёзы"),
          "держание": ("банки", "грибы", "груши", "марки", "орехи", "фото")}
# TWELVE PAIRS OUTSIDE THE STORY HOUSE'S TABLES: (n, k), n > k; the TIMES frame multiplies n by 2 or 3
ПАРЫ = ((16, 7), (22, 9), (26, 11), (28, 13), (32, 14), (36, 15),
        (42, 17), (27, 8), (33, 12), (38, 19), (21, 6), (45, 18))
_ПЕРВЫЕ_ИСТОРИЙ = {п[0] for п in S.ЧИСЛА} | {п[0] for п in S.ЧИСЛА_АКТОВ}
for _n, _k in ПАРЫ:
    assert _n > _k >= 1 and _n not in _ПЕРВЫЕ_ИСТОРИЙ, (_n, _k, "the story house's tables show this number first")
    assert (_n, _k) not in S.ЧИСЛА and all(т[:2] != (_n, _k) for т in S.ЧИСЛА_АКТОВ), (_n, _k)
ЗНАК = {"больше_на": "+", "меньше_на": "−", "во_столько": "×", "на_сколько": "−", "во_сколько_раз": "÷"}
# THE WORD OF EQUALITY is the answer of the EQUAL frame; it is declared, not derived
РАВЕНСТВО = {"ru": "поровну", "en": "the same", "de": "gleich viele", "fr": "autant",
             "es": "lo mismo", "it": "lo stesso numero", "pt": "o mesmo", "nl": "evenveel",
             "pl": "po tyle samo"}
КРАТ = {"ru": {2: "вдвое", 3: "втрое"}, "en": {2: "twice", 3: "three times"}, "de": {2: "zweimal", 3: "dreimal"},
        "fr": {2: "deux fois", 3: "trois fois"}, "es": {2: "el doble", 3: "el triple"}, "it": {2: "il doppio", 3: "il triplo"},
        "pt": {2: "o dobro", 3: "o triplo"}, "nl": {2: "twee keer", 3: "drie keer"}, "pl": {2: "dwa razy", 3: "trzy razy"}}
# THE SLAVIC DEED VERB BENDS BY THE BEARER'S GENDER in the past («посадил»/«посадила», «posadził»/«posadziła»).
# It bends in the QUESTION too: the Russian TIMES question held a bare «сделал» before its bearer
# until 23.09, and ten pages said «во сколько раз больше … сделал Аня» — the court called them true.
ГЛАГОЛ_ДЕЛА = {"ru": "посадил", "pl": "posadził"}
РОДОВЫЕ = {"es": {"кск": ("cuántos", "cuántas")},
           "it": {"quante": ("quanti", "quante"), "delle": ("dei", "delle")},
           "pt": {"quantas": ("quantos", "quantas"), "das": ("dos", "das")}}

# THE FRAMES: {X} {Y} bearers, {Xр} {Yр} their genitives (the Russian holding), {Xчьё} the name's possessive
# from the story house's one door (pt «do João», «da Ana»: until 23.09 the frame wrote «de {X}», and 96
# pages said «o dobro das rosas de a Maria»), {В} {ВY} the deed verb bent
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
            больше_на="{X} planted {n} {Тn}. {Y} planted {k} more {Тмн} than {X}. how many {Тмн} did {Y} plant? {Y} planted {s} {Тs}: {n} {знак} {k} = {s}.",
            меньше_на="{X} planted {n} {Тn}. {Y} planted {k} fewer {Тмн} than {X}. how many {Тмн} did {Y} plant? {Y} planted {r} {Тr}: {n} {знак} {k} = {r}.",
            во_столько="{X} planted {n} {Тn}. {Y} planted {КРАТ} as many {Тмн} as {X}. how many {Тмн} did {Y} plant? {Y} planted {p} {Тp}: {n} {знак} {m} = {p}.",
            на_сколько="{X} planted {n} {Тn}. {Y} planted {s} {Тs}. how many more {Тмн} did {Y} plant than {X}? {k} more {Тмн}: {s} {знак} {n} = {k}."),
        "держание": dict(
            больше_на="{X} has {n} {Тn}. {Y} has {k} more {Тмн} than {X}. how many {Тмн} does {Y} have? {Y} has {s} {Тs}: {n} {знак} {k} = {s}.",
            меньше_на="{X} has {n} {Тn}. {Y} has {k} fewer {Тмн} than {X}. how many {Тмн} does {Y} have? {Y} has {r} {Тr}: {n} {знак} {k} = {r}.",
            во_столько="{X} has {n} {Тn}. {Y} has {КРАТ} as many {Тмн} as {X}. how many {Тмн} does {Y} have? {Y} has {p} {Тp}: {n} {знак} {m} = {p}.",
            на_сколько="{X} has {n} {Тn}. {Y} has {s} {Тs}. how many more {Тмн} does {Y} have than {X}? {k} more {Тмн}: {s} {знак} {n} = {k}."),
    },
    "de": {
        "дело": dict(
            больше_на="{X} pflanzte {n} {Тn}. {Y} pflanzte {k} {Тмн} mehr als {X}. wie viele {Тмн} pflanzte {Y}? {Y} pflanzte {s} {Тs}: {n} {знак} {k} = {s}.",
            меньше_на="{X} pflanzte {n} {Тn}. {Y} pflanzte {k} {Тмн} weniger als {X}. wie viele {Тмн} pflanzte {Y}? {Y} pflanzte {r} {Тr}: {n} {знак} {k} = {r}.",
            во_столько="{X} pflanzte {n} {Тn}. {Y} pflanzte {КРАТ} so viele {Тмн} wie {X}. wie viele {Тмн} pflanzte {Y}? {Y} pflanzte {p} {Тp}: {n} {знак} {m} = {p}.",
            на_сколько="{X} pflanzte {n} {Тn}. {Y} pflanzte {s} {Тs}. wie viele {Тмн} mehr pflanzte {Y} als {X}? {k} {Тмн} mehr: {s} {знак} {n} = {k}."),
        "держание": dict(
            больше_на="{X} hat {n} {Тn}. {Y} hat {k} {Тмн} mehr als {X}. wie viele {Тмн} hat {Y}? {Y} hat {s} {Тs}: {n} {знак} {k} = {s}.",
            меньше_на="{X} hat {n} {Тn}. {Y} hat {k} {Тмн} weniger als {X}. wie viele {Тмн} hat {Y}? {Y} hat {r} {Тr}: {n} {знак} {k} = {r}.",
            во_столько="{X} hat {n} {Тn}. {Y} hat {КРАТ} so viele {Тмн} wie {X}. wie viele {Тмн} hat {Y}? {Y} hat {p} {Тp}: {n} {знак} {m} = {p}.",
            на_сколько="{X} hat {n} {Тn}. {Y} hat {s} {Тs}. wie viele {Тмн} mehr hat {Y} als {X}? {k} {Тмн} mehr: {s} {знак} {n} = {k}."),
    },
    "fr": {
        "дело": dict(
            больше_на="{X} a planté {n} {Тn}. {Y} a planté {k} {Тмн} de plus que {X}. combien de {Тмн} a plantés {Y} ? {Y} a planté {s} {Тs} : {n} {знак} {k} = {s}.",
            меньше_на="{X} a planté {n} {Тn}. {Y} a planté {k} {Тмн} de moins que {X}. combien de {Тмн} a plantés {Y} ? {Y} a planté {r} {Тr} : {n} {знак} {k} = {r}.",
            во_столько="{X} a planté {n} {Тn}. {Y} a planté {КРАТ} plus de {Тмн} que {X}. combien de {Тмн} a plantés {Y} ? {Y} a planté {p} {Тp} : {n} {знак} {m} = {p}.",
            на_сколько="{X} a planté {n} {Тn}. {Y} a planté {s} {Тs}. combien de {Тмн} de plus a plantés {Y} que {X} ? {k} {Тмн} de plus : {s} {знак} {n} = {k}."),
        "держание": dict(
            больше_на="{X} a {n} {Тn}. {Y} a {k} {Тмн} de plus que {X}. combien de {Тмн} a {Y} ? {Y} a {s} {Тs} : {n} {знак} {k} = {s}.",
            меньше_на="{X} a {n} {Тn}. {Y} a {k} {Тмн} de moins que {X}. combien de {Тмн} a {Y} ? {Y} a {r} {Тr} : {n} {знак} {k} = {r}.",
            во_столько="{X} a {n} {Тn}. {Y} a {КРАТ} plus de {Тмн} que {X}. combien de {Тмн} a {Y} ? {Y} a {p} {Тp} : {n} {знак} {m} = {p}.",
            на_сколько="{X} a {n} {Тn}. {Y} a {s} {Тs}. combien de {Тмн} de plus a {Y} que {X} ? {k} {Тмн} de plus : {s} {знак} {n} = {k}."),
    },
    "es": {
        "дело": dict(
            больше_на="{X} plantó {n} {Тn}. {Y} plantó {k} {Тмн} más que {X}. ¿{кск} {Тмн} plantó {Y}? {Y} plantó {s} {Тs}: {n} {знак} {k} = {s}.",
            меньше_на="{X} plantó {n} {Тn}. {Y} plantó {k} {Тмн} menos que {X}. ¿{кск} {Тмн} plantó {Y}? {Y} plantó {r} {Тr}: {n} {знак} {k} = {r}.",
            во_столько="{X} plantó {n} {Тn}. {Y} plantó {КРАТ} de {Тмн} que {X}. ¿{кск} {Тмн} plantó {Y}? {Y} plantó {p} {Тp}: {n} {знак} {m} = {p}.",
            на_сколько="{X} plantó {n} {Тn}. {Y} plantó {s} {Тs}. ¿{кск} {Тмн} más plantó {Y} que {X}? {k} {Тмн} más: {s} {знак} {n} = {k}."),
        "держание": dict(
            больше_на="{X} tiene {n} {Тn}. {Y} tiene {k} {Тмн} más que {X}. ¿{кск} {Тмн} tiene {Y}? {Y} tiene {s} {Тs}: {n} {знак} {k} = {s}.",
            меньше_на="{X} tiene {n} {Тn}. {Y} tiene {k} {Тмн} menos que {X}. ¿{кск} {Тмн} tiene {Y}? {Y} tiene {r} {Тr}: {n} {знак} {k} = {r}.",
            во_столько="{X} tiene {n} {Тn}. {Y} tiene {КРАТ} de {Тмн} que {X}. ¿{кск} {Тмн} tiene {Y}? {Y} tiene {p} {Тp}: {n} {знак} {m} = {p}.",
            на_сколько="{X} tiene {n} {Тn}. {Y} tiene {s} {Тs}. ¿{кск} {Тмн} más tiene {Y} que {X}? {k} {Тмн} más: {s} {знак} {n} = {k}."),
    },
    "it": {
        "дело": dict(
            больше_на="{X} ha piantato {n} {Тn}. {Y} ha piantato {k} {Тмн} in più di {X}. {quante} {Тмн} ha piantato {Y}? {Y} ha piantato {s} {Тs}: {n} {знак} {k} = {s}.",
            меньше_на="{X} ha piantato {n} {Тn}. {Y} ha piantato {k} {Тмн} in meno di {X}. {quante} {Тмн} ha piantato {Y}? {Y} ha piantato {r} {Тr}: {n} {знак} {k} = {r}.",
            во_столько="{X} ha piantato {n} {Тn}. {Y} ha piantato {КРАТ} {delle} {Тмн} di {X}. {quante} {Тмн} ha piantato {Y}? {Y} ha piantato {p} {Тp}: {n} {знак} {m} = {p}.",
            на_сколько="{X} ha piantato {n} {Тn}. {Y} ha piantato {s} {Тs}. {quante} {Тмн} in più ha piantato {Y} di {X}? {k} {Тмн} in più: {s} {знак} {n} = {k}."),
        "держание": dict(
            больше_на="{X} ha {n} {Тn}. {Y} ha {k} {Тмн} in più di {X}. {quante} {Тмн} ha {Y}? {Y} ha {s} {Тs}: {n} {знак} {k} = {s}.",
            меньше_на="{X} ha {n} {Тn}. {Y} ha {k} {Тмн} in meno di {X}. {quante} {Тмн} ha {Y}? {Y} ha {r} {Тr}: {n} {знак} {k} = {r}.",
            во_столько="{X} ha {n} {Тn}. {Y} ha {КРАТ} {delle} {Тмн} di {X}. {quante} {Тмн} ha {Y}? {Y} ha {p} {Тp}: {n} {знак} {m} = {p}.",
            на_сколько="{X} ha {n} {Тn}. {Y} ha {s} {Тs}. {quante} {Тмн} in più ha {Y} di {X}? {k} {Тмн} in più: {s} {знак} {n} = {k}."),
    },
    "pt": {
        "дело": dict(
            больше_на="{X} plantou {n} {Тn}. {Y} plantou mais {k} {Тмн} do que {X}. {quantas} {Тмн} plantou {Y}? {Y} plantou {s} {Тs}: {n} {знак} {k} = {s}.",
            меньше_на="{X} plantou {n} {Тn}. {Y} plantou menos {k} {Тмн} do que {X}. {quantas} {Тмн} plantou {Y}? {Y} plantou {r} {Тr}: {n} {знак} {k} = {r}.",
            во_столько="{X} plantou {n} {Тn}. {Y} plantou {КРАТ} {das} {Тмн} {Xчьё}. {quantas} {Тмн} plantou {Y}? {Y} plantou {p} {Тp}: {n} {знак} {m} = {p}.",
            на_сколько="{X} plantou {n} {Тn}. {Y} plantou {s} {Тs}. {quantas} {Тмн} a mais plantou {Y} do que {X}? mais {k} {Тмн}: {s} {знак} {n} = {k}."),
        "держание": dict(
            больше_на="{X} tem {n} {Тn}. {Y} tem mais {k} {Тмн} do que {X}. {quantas} {Тмн} tem {Y}? {Y} tem {s} {Тs}: {n} {знак} {k} = {s}.",
            меньше_на="{X} tem {n} {Тn}. {Y} tem menos {k} {Тмн} do que {X}. {quantas} {Тмн} tem {Y}? {Y} tem {r} {Тr}: {n} {знак} {k} = {r}.",
            во_столько="{X} tem {n} {Тn}. {Y} tem {КРАТ} {das} {Тмн} {Xчьё}. {quantas} {Тмн} tem {Y}? {Y} tem {p} {Тp}: {n} {знак} {m} = {p}.",
            на_сколько="{X} tem {n} {Тn}. {Y} tem {s} {Тs}. {quantas} {Тмн} a mais tem {Y} do que {X}? mais {k} {Тмн}: {s} {знак} {n} = {k}."),
    },
    "nl": {
        "дело": dict(
            больше_на="{X} plantte {n} {Тn}. {Y} plantte {k} {Тмн} meer dan {X}. hoeveel {Тмн} plantte {Y}? {Y} plantte {s} {Тs}: {n} {знак} {k} = {s}.",
            меньше_на="{X} plantte {n} {Тn}. {Y} plantte {k} {Тмн} minder dan {X}. hoeveel {Тмн} plantte {Y}? {Y} plantte {r} {Тr}: {n} {знак} {k} = {r}.",
            во_столько="{X} plantte {n} {Тn}. {Y} plantte {КРАТ} zoveel {Тмн} als {X}. hoeveel {Тмн} plantte {Y}? {Y} plantte {p} {Тp}: {n} {знак} {m} = {p}.",
            на_сколько="{X} plantte {n} {Тn}. {Y} plantte {s} {Тs}. hoeveel {Тмн} meer plantte {Y} dan {X}? {k} {Тмн} meer: {s} {знак} {n} = {k}."),
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

# WAVE 2 — THE ANSWER WITHOUT ARITHMETIC (05.09). Three frames ask the reader to NAME, not to
# count: who has more, who has fewer, and who has more when neither does (the equality is its own
# answer, and its number is the story's). The fourth is the inverse of TIMES: two stories and the
# question «how many times more», answered by the declared multiplier word and a ledger of
# DIVISION. The winner is a hole ({W} the name, {Wр} the Russian genitive, {ВW} the Slavic verb
# bent by the winner's gender) — so the page cannot be read by position: half the pages carry the
# larger number FIRST and half SECOND, and the judge names the bearer by the numbers, not by place.
ВОЛНА2 = {
    "ru": {
        "дело": dict(
            кто_больше="{X} {В} {n} {Тn}. {Y} {ВY} {k} {Тk}. кто посадил больше {Тмн}? {W} {ВW} больше {Тмн}.",
            кто_меньше="{X} {В} {n} {Тn}. {Y} {ВY} {k} {Тk}. кто посадил меньше {Тмн}? {W} {ВW} меньше {Тмн}.",
            поровну="{X} {В} {n} {Тn}. {Y} {ВY} {n} {Тn}. кто посадил больше {Тмн}? никто: оба посадили поровну — {n} {Тn}.",
            во_сколько_раз="{X} {В} {p} {Тp}. {Y} {ВY} {n} {Тn}. во сколько раз больше {Тмн} {В} {X}, чем {Y}? {КРАТ}: {p} {знак} {n} = {m}."),
        "держание": dict(
            кто_больше="у {Xр} {n} {Тn}. у {Yр} {k} {Тk}. у кого {Тмн} больше? у {Wр} {Тмн} больше.",
            кто_меньше="у {Xр} {n} {Тn}. у {Yр} {k} {Тk}. у кого {Тмн} меньше? у {Wр} {Тмн} меньше.",
            поровну="у {Xр} {n} {Тn}. у {Yр} {n} {Тn}. у кого {Тмн} больше? ни у кого: у обоих поровну — {n} {Тn}.",
            во_сколько_раз="у {Xр} {p} {Тp}. у {Yр} {n} {Тn}. во сколько раз больше {Тмн} у {Xр}, чем у {Yр}? {КРАТ}: {p} {знак} {n} = {m}."),
    },
    "en": {
        "дело": dict(
            кто_больше="{X} planted {n} {Тn}. {Y} planted {k} {Тk}. who planted more {Тмн}? {W} planted more {Тмн}.",
            кто_меньше="{X} planted {n} {Тn}. {Y} planted {k} {Тk}. who planted fewer {Тмн}? {W} planted fewer {Тмн}.",
            поровну="{X} planted {n} {Тn}. {Y} planted {n} {Тn}. who planted more {Тмн}? neither: they planted the same number — {n} {Тn}.",
            во_сколько_раз="{X} planted {p} {Тp}. {Y} planted {n} {Тn}. how many times more {Тмн} did {X} plant than {Y}? {КРАТ} as many: {p} {знак} {n} = {m}."),
        "держание": dict(
            кто_больше="{X} has {n} {Тn}. {Y} has {k} {Тk}. who has more {Тмн}? {W} has more {Тмн}.",
            кто_меньше="{X} has {n} {Тn}. {Y} has {k} {Тk}. who has fewer {Тмн}? {W} has fewer {Тмн}.",
            поровну="{X} has {n} {Тn}. {Y} has {n} {Тn}. who has more {Тмн}? neither: they have the same — {n} {Тn}.",
            во_сколько_раз="{X} has {p} {Тp}. {Y} has {n} {Тn}. how many times more {Тмн} does {X} have than {Y}? {КРАТ} as many: {p} {знак} {n} = {m}."),
    },
    "de": {
        "дело": dict(
            кто_больше="{X} pflanzte {n} {Тn}. {Y} pflanzte {k} {Тk}. wer pflanzte mehr {Тмн}? {W} pflanzte mehr {Тмн}.",
            кто_меньше="{X} pflanzte {n} {Тn}. {Y} pflanzte {k} {Тk}. wer pflanzte weniger {Тмн}? {W} pflanzte weniger {Тмн}.",
            поровну="{X} pflanzte {n} {Тn}. {Y} pflanzte {n} {Тn}. wer pflanzte mehr {Тмн}? keiner: beide pflanzten gleich viele — {n} {Тn}.",
            во_сколько_раз="{X} pflanzte {p} {Тp}. {Y} pflanzte {n} {Тn}. wie viele Mal mehr {Тмн} pflanzte {X} als {Y}? {КРАТ} so viele: {p} {знак} {n} = {m}."),
        "держание": dict(
            кто_больше="{X} hat {n} {Тn}. {Y} hat {k} {Тk}. wer hat mehr {Тмн}? {W} hat mehr {Тмн}.",
            кто_меньше="{X} hat {n} {Тn}. {Y} hat {k} {Тk}. wer hat weniger {Тмн}? {W} hat weniger {Тмн}.",
            поровну="{X} hat {n} {Тn}. {Y} hat {n} {Тn}. wer hat mehr {Тмн}? keiner: beide haben gleich viele — {n} {Тn}.",
            во_сколько_раз="{X} hat {p} {Тp}. {Y} hat {n} {Тn}. wie viele Mal mehr {Тмн} hat {X} als {Y}? {КРАТ} so viele: {p} {знак} {n} = {m}."),
    },
    "fr": {
        "дело": dict(
            кто_больше="{X} a planté {n} {Тn}. {Y} a planté {k} {Тk}. qui a planté plus de {Тмн} ? {W} a planté plus de {Тмн}.",
            кто_меньше="{X} a planté {n} {Тn}. {Y} a planté {k} {Тk}. qui a planté moins de {Тмн} ? {W} a planté moins de {Тмн}.",
            поровну="{X} a planté {n} {Тn}. {Y} a planté {n} {Тn}. qui a planté plus de {Тмн} ? personne : les deux en ont planté autant — {n} {Тn}.",
            во_сколько_раз="{X} a planté {p} {Тp}. {Y} a planté {n} {Тn}. combien de fois plus de {Тмн} a plantés {X} que {Y} ? {КРАТ} plus : {p} {знак} {n} = {m}."),
        "держание": dict(
            кто_больше="{X} a {n} {Тn}. {Y} a {k} {Тk}. qui a plus de {Тмн} ? {W} a plus de {Тмн}.",
            кто_меньше="{X} a {n} {Тn}. {Y} a {k} {Тk}. qui a moins de {Тмн} ? {W} a moins de {Тмн}.",
            поровну="{X} a {n} {Тn}. {Y} a {n} {Тn}. qui a plus de {Тмн} ? personne : les deux en ont autant — {n} {Тn}.",
            во_сколько_раз="{X} a {p} {Тp}. {Y} a {n} {Тn}. combien de fois plus de {Тмн} a {X} que {Y} ? {КРАТ} plus : {p} {знак} {n} = {m}."),
    },
    "es": {
        "дело": dict(
            кто_больше="{X} plantó {n} {Тn}. {Y} plantó {k} {Тk}. ¿quién plantó más {Тмн}? {W} plantó más {Тмн}.",
            кто_меньше="{X} plantó {n} {Тn}. {Y} plantó {k} {Тk}. ¿quién plantó menos {Тмн}? {W} plantó menos {Тмн}.",
            поровну="{X} plantó {n} {Тn}. {Y} plantó {n} {Тn}. ¿quién plantó más {Тмн}? ninguno: los dos plantaron lo mismo — {n} {Тn}.",
            во_сколько_раз="{X} plantó {p} {Тp}. {Y} plantó {n} {Тn}. ¿cuántas veces más {Тмн} plantó {X} que {Y}? {КРАТ}: {p} {знак} {n} = {m}."),
        "держание": dict(
            кто_больше="{X} tiene {n} {Тn}. {Y} tiene {k} {Тk}. ¿quién tiene más {Тмн}? {W} tiene más {Тмн}.",
            кто_меньше="{X} tiene {n} {Тn}. {Y} tiene {k} {Тk}. ¿quién tiene menos {Тмн}? {W} tiene menos {Тмн}.",
            поровну="{X} tiene {n} {Тn}. {Y} tiene {n} {Тn}. ¿quién tiene más {Тмн}? ninguno: los dos tienen lo mismo — {n} {Тn}.",
            во_сколько_раз="{X} tiene {p} {Тp}. {Y} tiene {n} {Тn}. ¿cuántas veces más {Тмн} tiene {X} que {Y}? {КРАТ}: {p} {знак} {n} = {m}."),
    },
    "it": {
        "дело": dict(
            кто_больше="{X} ha piantato {n} {Тn}. {Y} ha piantato {k} {Тk}. chi ha piantato più {Тмн}? {W} ha piantato più {Тмн}.",
            кто_меньше="{X} ha piantato {n} {Тn}. {Y} ha piantato {k} {Тk}. chi ha piantato meno {Тмн}? {W} ha piantato meno {Тмн}.",
            поровну="{X} ha piantato {n} {Тn}. {Y} ha piantato {n} {Тn}. chi ha piantato più {Тмн}? nessuno: entrambi ne hanno piantato lo stesso numero — {n} {Тn}.",
            во_сколько_раз="{X} ha piantato {p} {Тp}. {Y} ha piantato {n} {Тn}. quante volte più {Тмн} ha piantato {X} di {Y}? {КРАТ}: {p} {знак} {n} = {m}."),
        "держание": dict(
            кто_больше="{X} ha {n} {Тn}. {Y} ha {k} {Тk}. chi ha più {Тмн}? {W} ha più {Тмн}.",
            кто_меньше="{X} ha {n} {Тn}. {Y} ha {k} {Тk}. chi ha meno {Тмн}? {W} ha meno {Тмн}.",
            поровну="{X} ha {n} {Тn}. {Y} ha {n} {Тn}. chi ha più {Тмн}? nessuno: entrambi ne hanno lo stesso numero — {n} {Тn}.",
            во_сколько_раз="{X} ha {p} {Тp}. {Y} ha {n} {Тn}. quante volte più {Тмн} ha {X} di {Y}? {КРАТ}: {p} {знак} {n} = {m}."),
    },
    "pt": {
        "дело": dict(
            кто_больше="{X} plantou {n} {Тn}. {Y} plantou {k} {Тk}. quem plantou mais {Тмн}? {W} plantou mais {Тмн}.",
            кто_меньше="{X} plantou {n} {Тn}. {Y} plantou {k} {Тk}. quem plantou menos {Тмн}? {W} plantou menos {Тмн}.",
            поровну="{X} plantou {n} {Тn}. {Y} plantou {n} {Тn}. quem plantou mais {Тмн}? ninguém: os dois plantaram o mesmo — {n} {Тn}.",
            во_сколько_раз="{X} plantou {p} {Тp}. {Y} plantou {n} {Тn}. quantas vezes mais {Тмн} plantou {X} do que {Y}? {КРАТ}: {p} {знак} {n} = {m}."),
        "держание": dict(
            кто_больше="{X} tem {n} {Тn}. {Y} tem {k} {Тk}. quem tem mais {Тмн}? {W} tem mais {Тмн}.",
            кто_меньше="{X} tem {n} {Тn}. {Y} tem {k} {Тk}. quem tem menos {Тмн}? {W} tem menos {Тмн}.",
            поровну="{X} tem {n} {Тn}. {Y} tem {n} {Тn}. quem tem mais {Тмн}? ninguém: os dois têm o mesmo — {n} {Тn}.",
            во_сколько_раз="{X} tem {p} {Тp}. {Y} tem {n} {Тn}. quantas vezes mais {Тмн} tem {X} do que {Y}? {КРАТ}: {p} {знак} {n} = {m}."),
    },
    "nl": {
        "дело": dict(
            кто_больше="{X} plantte {n} {Тn}. {Y} plantte {k} {Тk}. wie plantte meer {Тмн}? {W} plantte meer {Тмн}.",
            кто_меньше="{X} plantte {n} {Тn}. {Y} plantte {k} {Тk}. wie plantte minder {Тмн}? {W} plantte minder {Тмн}.",
            поровну="{X} plantte {n} {Тn}. {Y} plantte {n} {Тn}. wie plantte meer {Тмн}? niemand: beiden plantten evenveel — {n} {Тn}.",
            во_сколько_раз="{X} plantte {p} {Тp}. {Y} plantte {n} {Тn}. hoeveel keer meer {Тмн} plantte {X} dan {Y}? {КРАТ} zoveel: {p} {знак} {n} = {m}."),
        "держание": dict(
            кто_больше="{X} heeft {n} {Тn}. {Y} heeft {k} {Тk}. wie heeft meer {Тмн}? {W} heeft meer {Тмн}.",
            кто_меньше="{X} heeft {n} {Тn}. {Y} heeft {k} {Тk}. wie heeft minder {Тмн}? {W} heeft minder {Тмн}.",
            поровну="{X} heeft {n} {Тn}. {Y} heeft {n} {Тn}. wie heeft meer {Тмн}? niemand: beiden hebben evenveel — {n} {Тn}.",
            во_сколько_раз="{X} heeft {p} {Тp}. {Y} heeft {n} {Тn}. hoeveel keer meer {Тмн} heeft {X} dan {Y}? {КРАТ} zoveel: {p} {знак} {n} = {m}."),
    },
    "pl": {
        "дело": dict(
            кто_больше="{X} {В} {n} {Тn}. {Y} {ВY} {k} {Тk}. kto posadził więcej {Тмн}? {W} {ВW} więcej {Тмн}.",
            кто_меньше="{X} {В} {n} {Тn}. {Y} {ВY} {k} {Тk}. kto posadził mniej {Тмн}? {W} {ВW} mniej {Тмн}.",
            поровну="{X} {В} {n} {Тn}. {Y} {ВY} {n} {Тn}. kto posadził więcej {Тмн}? nikt: obydwoje posadzili po tyle samo — {n} {Тn}.",
            во_сколько_раз="{X} {В} {p} {Тp}. {Y} {ВY} {n} {Тn}. ile razy więcej {Тмн} {В} {X} niż {Y}? {КРАТ} więcej: {p} {знак} {n} = {m}."),
        "держание": dict(
            кто_больше="{X} ma {n} {Тn}. {Y} ma {k} {Тk}. kto ma więcej {Тмн}? {W} ma więcej {Тмн}.",
            кто_меньше="{X} ma {n} {Тn}. {Y} ma {k} {Тk}. kto ma mniej {Тмн}? {W} ma mniej {Тмн}.",
            поровну="{X} ma {n} {Тn}. {Y} ma {n} {Тn}. kto ma więcej {Тмн}? nikt: obydwoje mają po tyle samo — {n} {Тn}.",
            во_сколько_раз="{X} ma {p} {Тp}. {Y} ma {n} {Тn}. ile razy więcej {Тмн} ma {X} niż {Y}? {КРАТ} więcej: {p} {знак} {n} = {m}."),
    },
}
for _язык, _группы in ВОЛНА2.items():
    for _группа, _рамки in _группы.items():
        РАМКИ[_язык][_группа].update(_рамки)
# THE WORD OF EQUALITY STANDS IN ITS FRAME, and the frame is the house's own text: a page that
# says «more» where the numbers are equal is no page of this house at all.
for _язык, _слово in РАВЕНСТВО.items():
    assert any(_слово in РАМКИ[_язык][_гр]["поровну"] for _гр in ГРУППЫ), (_язык, "the equality word is not in its frame")

def _товар(язык, ключ, c):
    """The goods in the count form of c — the story house's forms, the pack's rule."""
    return S._товар_форма(язык, ключ, c)


def _поля(язык, группа, i, j, ключ, n, k, m):
    X, Y = S._лицо(язык, i), S._лицо(язык, j)
    if Y[0] == X[0]:
        Y = S._лицо(язык, j + 1)
    s, r, p = n + k, n - k, n * m
    п = dict(X=X[0], Xр=X[2], Xчьё=S._имя_чьё(язык, X), Y=Y[0], Yр=Y[2], n=n, k=k, s=s, r=r, p=p, m=m,
             Тn=_товар(язык, ключ, n), Тk=_товар(язык, ключ, k), Тs=_товар(язык, ключ, s),
             Тr=_товар(язык, ключ, r), Тp=_товар(язык, ключ, p), Тмн=S.ТОВАРЫ_АКТОВ[язык][ключ][-1],
             КРАТ=КРАТ[язык][m])
    if язык in ГЛАГОЛ_ДЕЛА:
        п["В"] = ГЛАГОЛ_ДЕЛА[язык] + A._а(язык, X[1])
        п["ВY"] = ГЛАГОЛ_ДЕЛА[язык] + A._а(язык, Y[1])
    род = S.РОД_ТОВАРА_АКТОВ.get(язык, {}).get(п["Тмн"])
    assert язык not in РОДОВЫЕ or род in ("m", "f"), (язык, п["Тмн"], "the goods' gender is not declared")
    for дыра, (м_, ж_) in РОДОВЫЕ.get(язык, {}).items():
        п[дыра] = м_ if род == "m" else ж_
    п["_X"], п["_Y"] = X, Y      # the faces themselves: the winner is chosen by the frame
    return п


БЕЗ_АРИФМЕТИКИ = ("кто_больше", "кто_меньше", "поровну")


def страница(язык, группа, форма, i, j, ключ, n, k, m=2, обратно=False):
    """A page of the frame. THE LARGER NUMBER STANDS FIRST OR SECOND BY THE CALLER'S WORD
    («обратно»): a comparison whose answer is always the first bearer teaches place, not
    number. The EQUAL frame gives both bearers one number; the INVERSE-TIMES frame gives the
    first bearer n × m and the second n."""
    if форма in ("кто_больше", "кто_меньше") and обратно:
        n, k = k, n
    if форма == "поровну":
        k = n
    п = _поля(язык, группа, i, j, ключ, n, k, m)
    п["знак"] = ЗНАК.get(форма, "")
    if форма in ("кто_больше", "кто_меньше"):
        первым = (n > k) if форма == "кто_больше" else (n < k)
        W = п["_X"] if первым else п["_Y"]
        п["W"], п["Wр"] = W[0], W[2]
        if язык in ГЛАГОЛ_ДЕЛА:
            п["ВW"] = ГЛАГОЛ_ДЕЛА[язык] + A._а(язык, W[1])
    готовая = РАМКИ[язык][группа][форма].format(**п)
    # ФРАНЦУЗСКАЯ ЭЛИЗИЯ ДЕЛАЕТСЯ ПОСЛЕ ПОДСТАНОВКИ: рамка держит «de» целым, ибо не знает,
    # что за ним встанет («combien de abdos» → «combien d'abdos»). Закон — у дома языка.
    return _fr.элизия(готовая) if язык == "fr" else готовая


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
                        if форма in ВОЛНА2["ru"]["дело"]:
                            continue          # wave 2 walks its own rows below
                        вон[страница(язык, группа, форма, i, j, ключ, n, k, m)] = (язык, группа, форма)
                # WAVE 2: six pairs of the twelve, each written BOTH ways round (the larger first
                # and second), so the answering name cannot be read off the place
                for q, (n, k) in enumerate(ПАРЫ[::2]):
                    i, j = (q + g) % лиц, (q * 3 + 1 + g) % лиц
                    m = 2 if (q + g) % 2 == 0 else 3
                    for обратно in (False, True):
                        for форма in ("кто_больше", "кто_меньше"):
                            вон[страница(язык, группа, форма, i, j, ключ, n, k, m, обратно)] = (язык, группа, форма)
                    вон[страница(язык, группа, "поровну", i, j, ключ, n, k, m)] = (язык, группа, "поровну")
                    for кратность in (2, 3):
                        вон[страница(язык, группа, "во_сколько_раз", i, j, ключ, n, k, кратность)] = (язык, группа, "во_сколько_раз")
    return вон


ПОКАЗЫ = _показы()

# РОД ЗДЕСЬ ТРЕТИЙ, А НЕ ВТОРОЙ (13.09). Значение показа — тройка (язык, группа, форма).
# Группа («дело» или «держание») есть ДОВОД страницы, как местоимение у соседа `pronobject`:
# она выбирает товары и вторую волну, но не меняет утверждения о сравнении. Род есть ФОРМА:
# «больше_на» о банках и «больше_на» о посаженных дубах суть один род и один закон суда.
#
#     ДОМ, У КОТОРОГО РОД СТОИТ НЕ НА ОБЫЧНОМ МЕСТЕ, ГОВОРИТ ЭТО САМ. Указатель родов,
#     угадывающий место, назвал бы родами две группы и потерял бы восемь форм.
РОД_В_ПОКАЗЕ = 2

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


def _лица(язык):
    """name → face and genitive → face: the winner is named in the frame's own case."""
    по_имени, по_роду = {}, {}
    for i in range(len(A.ЛИЦА[язык])):
        л = S._лицо(язык, i)
        по_имени[л[0]] = л
        по_роду[л[2]] = л
    return по_имени, по_роду


ЛИЦА_ПО_ИМЕНИ, ЛИЦА_ПО_РОДУ = {}, {}
for _я in ЯЗЫКИ:
    ЛИЦА_ПО_ИМЕНИ[_я], ЛИЦА_ПО_РОДУ[_я] = _лица(_я)


def _alt(слова):
    return "(?:" + "|".join(re.escape(с) for с in sorted({с for с in слова if с}, key=lambda с: (-len(с), с))) + ")"


def _образец(язык, рамка):
    """One anchored pattern over the page; the i-th occurrence of a hole is the group «h_hole__i»."""
    лица = [S._лицо(язык, i) for i in range(len(A.ЛИЦА[язык]))]
    имена, род = _alt(л[0] for л in лица), _alt(л[2] for л in лица)
    товары = _alt(ФОРМЫ_ТОВАРОВ[язык])
    глагол = _alt([ГЛАГОЛ_ДЕЛА[язык], ГЛАГОЛ_ДЕЛА[язык] + A._а(язык, "f")]) if язык in ГЛАГОЛ_ДЕЛА else None
    дыры = {"X": имена, "Y": имена, "Xр": род, "Xчьё": _alt(S._имя_чьё(язык, л) for л in лица), "Yр": род, "n": r"\d+", "k": r"\d+", "s": r"\d+", "r": r"\d+",
            "p": r"\d+", "m": r"\d+", "Тn": товары, "Тk": товары, "Тs": товары, "Тr": товары, "Тp": товары,
            "Тмн": товары, "КРАТ": _alt(КРАТ[язык].values()), "знак": r"[+−×÷]", "В": глагол, "ВY": глагол,
            "W": имена, "Wр": род, "ВW": глагол}
    for дыра, пара in РОДОВЫЕ.get(язык, {}).items():
        дыры[дыра] = _alt(пара)
    счёт, куски = {}, []
    for кусок in re.split(r"(\{[^}]+\})", рамка):
        if кусок.startswith("{"):
            дыра = кусок[1:-1]
            счёт[дыра] = счёт.get(дыра, 0) + 1
            куски.append(f"(?P<h_{дыра}__{счёт[дыра]}>{дыры[дыра]})")
        else:
            куски.append(_fr.в_образце(кусок) if язык == "fr" else re.escape(кусок))
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
    if "знак" in з and з["знак"] != ЗНАК.get(форма):
        return False
    # the possessive is the possessive of the page's own first bearer, not of a neighbour
    if "Xчьё" in з and (з.get("X") not in ЛИЦА_ПО_ИМЕНИ[язык]
                        or S._имя_чьё(язык, ЛИЦА_ПО_ИМЕНИ[язык][з["X"]]) != з["Xчьё"]):
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
    if форма in ("кто_больше", "кто_меньше"):
        # THE NAME IS READ FROM THE NUMBERS, NEVER FROM THE PLACE: the winner of MORE is the
        # bearer of the greater number, of FEWER the lesser; equal numbers are no comparison.
        if ч["n"] == ч["k"]:
            return False
        первый, второй = з.get("X") or з.get("Xр"), з.get("Y") or з.get("Yр")
        больший = первый if ч["n"] > ч["k"] else второй
        нужен = больший if форма == "кто_больше" else (второй if больший == первый else первый)
        if (з.get("W") or з.get("Wр")) != нужен:
            return False
        if "ВW" in з:
            лицо = ЛИЦА_ПО_ИМЕНИ[язык].get(нужен) or ЛИЦА_ПО_РОДУ[язык].get(нужен)
            if лицо is None or з["ВW"] != ГЛАГОЛ_ДЕЛА[язык] + A._а(язык, лицо[1]):
                return False
    if форма == "поровну" and "k" in ч and ч["k"] != ч["n"]:
        return False
    if форма == "во_сколько_раз" and (ч["p"] != ч["n"] * ч["m"] or _КРАТНОСТЬ[язык].get(з["КРАТ"]) != ч["m"]):
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
    род = S.РОД_ТОВАРА_АКТОВ.get(язык, {}).get(з["Тмн"])
    if язык in РОДОВЫЕ and род not in ("m", "f"):
        return False
    for дыра, пара in РОДОВЫЕ.get(язык, {}).items():
        if дыра in з and з[дыра] != (пара[0] if род == "m" else пара[1]):
            return False
    return True



# РОД ПРОШЕДШЕГО СВЕРЯЕТСЯ С ЛИЦОМ ПОСЛЕ ВЕРДИКТА (08.09). Окончание глагола стои́т в
# образце ДЫРОЙ, принимающей любую букву, — иначе образец не покрыл бы обоих родов, —
# и вердикт о нём не спрашивал. Подмена «Анна сделала» → «Анна сделал» проходила
# образцом и звалась ИСТИНОЙ.
#
#     СУД, МОЛЧАЩИЙ О ПОРЧЕ, БЕРЁТ ИСТИНУ У СОСЕДА. СУД, ЗОВУЩИЙ ПОРЧУ ИСТИНОЙ,
#     ОТНИМАЕТ ЕЁ У ВСЕХ: палата видит зелёный вердикт и дальше не смотрит.
#
# Закон берётся у дома языка (`rugram.не_по_роду`), лица — у себя: ни один из двух
# не может проверить страницу один.
_РОДЫ_ЛИЦ = {л[0]: л[1] for л in A.ЛИЦА.get("ru", ()) if len(л) > 1 and л[1] in ("m", "f")}

def судить(строка):
    """(судимо, истинно): a page of a frame of the house whose holes agree and whose ledger
    recomputes; silence on anything else (the closed world's gate makes it a lie)."""
    с = строка.strip()
    # ВЫХОД ПО НАБОРУ СНЯТ (21.09): здесь стояло «если строка в ПОКАЗЫ — истина», и
    # содержательный закон ниже не спрашивался о СВОИХ страницах ни разу.
    #
    #     НАБОР ГОВОРИТ, ЧТО ДОМ СТРАНИЦУ НАПИСАЛ, А НЕ ЧТО ОНА ВЕРНА.
    #
    # Замерено: закон судит все 6480 показов дома верно и без набора — выход был
    # чистым балластом, слепившим дом к порче, вписанной в его же набор. Полный закон
    # и замер по всем сорока шести домам — в `scripts/house_mutant.py`.
    for образ, язык, группа, форма in ОБРАЗЦЫ:
        м = образ.match(с)
        if м:
            если = _вердикт(язык, группа, форма, м)
            if если and язык == "ru" and _RUG.не_по_роду(с, _РОДЫ_ЛИЦ):
                return True, False
            return True, если
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
            б = страница(язык, "дело", "во_столько", 0, 3, ТОВАРЫ["дело"][0], 16, 7, 2)
            стоит = next((с for с in пара if f" {с} " in б), None)
            if стоит is None:
                continue
            другое = пара[1] if стоит == пара[0] else пара[0]
            assert судить(б.replace(f" {стоит} ", f" {другое} ")) == (True, False), б
            мутанты += 1
        # WAVE 2 (05.09): the answer without arithmetic and the inverse of TIMES
        for группа in ГРУППЫ:
            ключ = ТОВАРЫ[группа][0]
            X, Y = S._лицо(язык, 0), S._лицо(язык, 3)
            for форма, победитель, проигравший in (("кто_больше", X, Y), ("кто_меньше", Y, X)):
                стр = страница(язык, группа, форма, 0, 3, ключ, 26, 11)
                assert судить(стр) == (True, True), стр
                # (9) the name of the OTHER bearer: the answer read off the place, not the numbers
                хвост = стр[стр.rfind("?"):]
                для, на = ((победитель[0], проигравший[0]) if победитель[0] in хвост
                           else (победитель[2], проигравший[2]))
                битая = стр[:стр.rfind("?")] + хвост.replace(для, на, 1)
                assert судить(битая) == (True, False), битая
                мутанты += 1
            # (10) EQUAL told of unequal numbers
            рв = страница(язык, группа, "поровну", 1, 4, ключ, 26, 11)
            assert судить(рв) == (True, True), рв
            assert судить(рв.replace("26", "27", 1)) == (True, False), рв
            # (11) the inverse of TIMES with a multiplier word that is not the quotient
            вр = страница(язык, группа, "во_сколько_раз", 2, 5, ключ, 16, 7, 2)
            assert судить(вр) == (True, True), вр
            assert судить(вр.replace(КРАТ[язык][2], КРАТ[язык][3], 1)) == (True, False), вр
            # (12) the inverse of TIMES whose division does not divide
            assert судить(вр.replace(" ÷ 16 = 2", " ÷ 16 = 3")) == (True, False), вр
            мутанты += 3
        # (14) the possessive of a NEIGHBOUR («o dobro das fotos do Pedro» on a page of João), and
        # the uncontracted article that stood in 96 pages until 23.09 («de o João»)
        if язык == "pt":
            for группа in ГРУППЫ:
                в = страница(язык, группа, "во_столько", 1, 4, ТОВАРЫ[группа][0], 22, 9, 2)
                X, чужой = S._лицо(язык, 1), S._лицо(язык, 2)
                assert S._имя_чьё(язык, X) in в, в
                assert судить(в.replace(S._имя_чьё(язык, X), S._имя_чьё(язык, чужой))) == (True, False), в
                assert судить(в.replace(S._имя_чьё(язык, X), "de " + X[0])) == (False, False), в
                мутанты += 2
        # (13) the Slavic TIMES question whose verb does not bend by its bearer: until 23.09 the
        # Russian frame held a bare «сделал» there, and «… сделал Аня, чем Дима?» was called true
        if язык in ГЛАГОЛ_ДЕЛА:
            i = next(i for i in range(len(A.ЛИЦА[язык])) if S._лицо(язык, i)[1] == "f")
            X = S._лицо(язык, i)
            вр = страница(язык, "дело", "во_сколько_раз", i, i + 1, ТОВАРЫ["дело"][0], 16, 7, 2)
            согласный = ГЛАГОЛ_ДЕЛА[язык] + A._а(язык, "f")
            assert судить(вр) == (True, True) and f"{согласный} {X[0]}" in вр, вр
            битая = вр.replace(f"{согласный} {X[0]}", f"{ГЛАГОЛ_ДЕЛА[язык]} {X[0]}")
            assert судить(битая) == (True, False), битая
            мутанты += 1
    print("  ", страница("ru", "дело", "больше_на", 0, 3, "дубы", 16, 7))
    print("  ", страница("es", "дело", "меньше_на", 1, 4, "дубы", 22, 9))
    print("  ", страница("it", "держание", "во_столько", 2, 5, "банки", 26, 11, 2))
    print("  ", страница("pl", "дело", "на_сколько", 3, 6, "берёзы", 28, 13))
    print("  ", страница("pt", "держание", "больше_на", 0, 3, "грибы", 32, 14))
    print("  ", страница("nl", "держание", "меньше_на", 1, 4, "груши", 36, 15))
    print("  ", страница("ru", "держание", "кто_больше", 0, 3, "марки", 26, 11))
    print("  ", страница("en", "дело", "кто_меньше", 1, 4, "дубы", 22, 9, обратно=True))
    print("  ", страница("de", "держание", "поровну", 2, 5, "орехи", 32, 14))
    print("  ", страница("pl", "дело", "во_сколько_раз", 3, 6, "берёзы", 16, 7, 3))
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
