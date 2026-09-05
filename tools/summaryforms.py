#!/usr/bin/env python3
"""THE HOUSE OF THE SUMMARY — what a compacted record KEEPS, and what it LOST (05.09).

The fifth market of the agent's architecture. An agent that lives long enough runs out of
room and COMPACTS: the episode is replaced by a note, and from then on the note is all it
has. Two skills are bought here, and nowhere else in the corpus:

    A QUESTION ABOUT THE RECORD, NOT ABOUT THE WORLD. «What does the summary say about the
    shelf?» is not «how many things are on the shelf?». The page shows the whole episode
    AND its note, so nothing is hidden — and the honest answer about a place the note left
    out is «nothing: the summary is silent about the shelf», even though the page itself
    still carries the number. This is the shape an agent needs when its own record has been
    cut: it must know what it may answer FROM THE RECORD and what the record no longer
    holds. The house of the pair already shows the refusal «I do not know: it is not said»;
    here the refusal names its GROUND — the summary — and the house asserts that its own
    head is the pair house's word of not-knowing, so one refusal is not learnt twice.

    A COMPACTION IS TRUE OR FALSE, AND THE PAGE SAYS WHICH. «Is the summary right?» —
    «yes: there are 7 files in the folder, and the summary says 7», or «no: there are 7
    files in the folder, but the summary says 8». A note that distorts is the one failure
    of compaction that costs an agent everything downstream, so the corpus shows the check
    itself, over a state and over a TAPE («5 + 3 − 2 = 6, and the summary says 6»).

WHAT IS BORROWED AND WHAT IS DECLARED. Nine languages; the things (files, records,
messages), their count forms and the copula of a place are BORROWED from the house of the
tool, the acts and their ordinals from the house of the episode, the words of yes and no
from the language packs, and the openers of every question stand declared in the house of
the pair. Declared here: the fourth place (the shelf) beside the tool house's three, EVERY
place in three cases (locative «in the folder», nominative «the folder», about-case «about
the folder» — a case is written, never guessed), the note's own line, the words that count
places, and the two connectives of a verdict («and the summary says» against «but the
summary says»). The first three locatives are ASSERTED equal to the tool house's places:
the borrowing is checked, not copied.

THE FRAME IS THE SHAPE, THE JUDGE IS THE LAW. A frame names WHICH places the note keeps
and WHICH place the question asks — so a page claiming silence about a place the note keeps
matches a frame, and is judged a lie by the law, not silenced by the absence of a pattern.
The truthful forms share one hole between the story and the note, so a note that drifts from
its episode cannot be written at all; the lying form carries the distorted number in a hole
of its own, and the judge demands that it DIFFER — a «no» over a faithful note is a lie too.

WHAT IS NOT MEASURED, NAMED: whether the note keeps the RIGHT places (a summary that drops
what the question will need is a bad summary, not a false one), and how the compaction was
made. The house shows the shape of a record and its check, never the art of choosing it.
"""
import json
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import asking  # noqa: E402 — the house of the pair declares which openers a question may wear
import episodeforms as E  # noqa: E402 — the acts of a tape, their ordinals and the ledger
import svampforms as S  # noqa: E402 — the count cell of a pack and the word of not-knowing
import toolforms as T  # noqa: E402 — things of acts, their places, the copula of a place

_ПАКЕТЫ = pathlib.Path(__file__).resolve().parent / "langpacks"
ЯЗЫКИ = T.ЯЗЫКИ
ЧИСЛА = (3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18)
СДВИГИ = (0, 1, 2, 3)          # four number tuples per shape
МЕСТ = (3, 4)                  # how many places an episode names

# МЕСТА В ТРЁХ ПАДЕЖАХ — (локатив, именительный, о-падеж). Падеж пишется, а не угадывается:
# немецкий «über das Regal» и польское «o półce» не выводятся из «im Regal» и «na półce».
МЕСТА = {
    "ru": (("в папке", "папка", "о папке"), ("в ящике", "ящик", "о ящике"),
           ("в списке", "список", "о списке"), ("на полке", "полка", "о полке")),
    "en": (("in the folder", "the folder", "about the folder"), ("in the box", "the box", "about the box"),
           ("in the list", "the list", "about the list"), ("on the shelf", "the shelf", "about the shelf")),
    "de": (("im Ordner", "der Ordner", "über den Ordner"), ("in der Kiste", "die Kiste", "über die Kiste"),
           ("in der Liste", "die Liste", "über die Liste"), ("im Regal", "das Regal", "über das Regal")),
    "fr": (("dans le dossier", "le dossier", "sur le dossier"), ("dans la boîte", "la boîte", "sur la boîte"),
           ("dans la liste", "la liste", "sur la liste"), ("sur l'étagère", "l'étagère", "sur l'étagère")),
    "es": (("en la carpeta", "la carpeta", "de la carpeta"), ("en la caja", "la caja", "de la caja"),
           ("en la lista", "la lista", "de la lista"), ("en el estante", "el estante", "del estante")),
    "it": (("nella cartella", "la cartella", "sulla cartella"), ("nella scatola", "la scatola", "sulla scatola"),
           ("nell'elenco", "l'elenco", "sull'elenco"), ("sullo scaffale", "lo scaffale", "sullo scaffale")),
    "pt": (("na pasta", "a pasta", "sobre a pasta"), ("na caixa", "a caixa", "sobre a caixa"),
           ("na lista", "a lista", "sobre a lista"), ("na prateleira", "a prateleira", "sobre a prateleira")),
    "nl": (("in de map", "de map", "over de map"), ("in de doos", "de doos", "over de doos"),
           ("in de lijst", "de lijst", "over de lijst"), ("op de plank", "de plank", "over de plank")),
    "pl": (("w folderze", "folder", "o folderze"), ("w pudełku", "pudełko", "o pudełku"),
           ("na liście", "lista", "o liście"), ("na półce", "półka", "o półce")),
}
# ЗАИМСТВОВАНИЕ ПРОВЕРЕНО, А НЕ СКОПИРОВАНО: первые три места — места дома инструмента.
for _яз in ЯЗЫКИ:
    assert tuple(м[0] for м in МЕСТА[_яз][:3]) == tuple(T.МЕСТА[_яз]), (_яз, "places drifted from the tool house")

СЛОВА_МЕСТ = {                 # сколько мест называет сводка — счётное слово места
    "ru": {2: "два места", 3: "три места"}, "en": {2: "two places", 3: "three places"},
    "de": {2: "zwei Orte", 3: "drei Orte"}, "fr": {2: "deux endroits", 3: "trois endroits"},
    "es": {2: "dos lugares", 3: "tres lugares"}, "it": {2: "due luoghi", 3: "tre luoghi"},
    "pt": {2: "dois lugares", 3: "três lugares"}, "nl": {2: "twee plaatsen", 3: "drie plaatsen"},
    "pl": {2: "dwa miejsca", 3: "trzy miejsca"},
}
СОЮЗ = {"ru": "и", "en": "and", "de": "und", "fr": "et", "es": "y", "it": "e", "pt": "e",
        "nl": "en", "pl": "i"}
# ШОВ ПЕРЕД СОЮЗОМ ВЕРДИКТА: польский не ставит запятой перед одиночным «i» (перед «ale» ставит).
ШОВ_И = {язык: (" " if язык == "pl" else ", ") for язык in ЯЗЫКИ}
# ГОЛОВА ОТКАЗА — слово незнания дома пары, и дом это проверяет (см. ниже _голова_отказа).
НИЧЕГО = {"ru": "ничего", "en": "nothing", "de": "nichts", "fr": "rien", "es": "nada",
          "it": "niente", "pt": "nada", "nl": "niets", "pl": "nic"}

РЕЧЬ = {
    "ru": dict(состояние="{М} {n} {Т}", заметка="{n} {Т} {М}", сводка="сводка",
               вопрос_говорит="что сводка говорит {О}?",
               ответ_ничего="ничего: сводка молчит {О}.",
               вопрос_ушло="о каком месте сводка молчит?", ответ_ушло="{О}.",
               вопрос_сколько="сколько мест называет сводка?",
               вопрос_верна="верна ли сводка?",
               и_говорит="и сводка говорит", а_говорит="а сводка говорит",
               двоеточие=": ", вопрос="?"),
    "en": dict(состояние="{ЕСТЬ} {n} {Т} {М}", заметка="{n} {Т} {М}", сводка="the summary",
               вопрос_говорит="what does the summary say {О}?",
               ответ_ничего="nothing: the summary is silent {О}.",
               вопрос_ушло="about which place is the summary silent?", ответ_ушло="{О}.",
               вопрос_сколько="how many places does the summary name?",
               вопрос_верна="is the summary right?",
               и_говорит="and the summary says", а_говорит="but the summary says",
               двоеточие=": ", вопрос="?"),
    "de": dict(состояние="{М} {ЕСТЬ} {n} {Т}", заметка="{n} {Т} {М}", сводка="die Zusammenfassung",
               вопрос_говорит="was sagt die Zusammenfassung {О}?",
               ответ_ничего="nichts: die Zusammenfassung schweigt {О}.",
               вопрос_ушло="über welchen Ort schweigt die Zusammenfassung?", ответ_ушло="{О}.",
               вопрос_сколько="wie viele Orte nennt die Zusammenfassung?",
               вопрос_верна="stimmt die Zusammenfassung?",
               и_говорит="und die Zusammenfassung sagt", а_говорит="aber die Zusammenfassung sagt",
               двоеточие=": ", вопрос="?"),
    "fr": dict(состояние="{М} il y a {n} {Т}", заметка="{n} {Т} {М}", сводка="le résumé",
               вопрос_говорит="que dit le résumé {О} ?",
               ответ_ничего="rien : le résumé ne dit rien {О}.",
               вопрос_ушло="sur quel endroit le résumé ne dit rien ?", ответ_ушло="{О}.",
               вопрос_сколько="combien d'endroits le résumé nomme-t-il ?",
               вопрос_верна="est-ce que le résumé est juste ?",
               и_говорит="et le résumé dit", а_говорит="mais le résumé dit",
               двоеточие=" : ", вопрос=" ?"),
    "es": dict(состояние="{М} hay {n} {Т}", заметка="{n} {Т} {М}", сводка="el resumen",
               вопрос_говорит="¿qué dice el resumen {О}?",
               ответ_ничего="nada: el resumen calla {О}.",
               вопрос_ушло="¿de qué lugar calla el resumen?", ответ_ушло="{О}.",
               вопрос_сколько="¿cuántos lugares nombra el resumen?",
               вопрос_верна="¿es correcto el resumen?",
               и_говорит="y el resumen dice", а_говорит="pero el resumen dice",
               двоеточие=": ", вопрос="?"),
    "it": dict(состояние="{М} {ЕСТЬ} {n} {Т}", заметка="{n} {Т} {М}", сводка="il riassunto",
               вопрос_говорит="che cosa dice il riassunto {О}?",
               ответ_ничего="niente: il riassunto tace {О}.",
               вопрос_ушло="su quale luogo tace il riassunto?", ответ_ушло="{О}.",
               вопрос_сколько="quanti luoghi nomina il riassunto?",
               вопрос_верна="è corretto il riassunto?",
               и_говорит="e il riassunto dice", а_говорит="ma il riassunto dice",
               двоеточие=": ", вопрос="?"),
    "pt": dict(состояние="{М} há {n} {Т}", заметка="{n} {Т} {М}", сводка="o resumo",
               вопрос_говорит="o que diz o resumo {О}?",
               ответ_ничего="nada: o resumo não fala {О}.",
               вопрос_ушло="sobre que lugar o resumo não fala?", ответ_ушло="{О}.",
               вопрос_сколько="quantos lugares o resumo nomeia?",
               вопрос_верна="o resumo está certo?",
               и_говорит="e o resumo diz", а_говорит="mas o resumo diz",
               двоеточие=": ", вопрос="?"),
    "nl": dict(состояние="{М} {ЕСТЬ} {n} {Т}", заметка="{n} {Т} {М}", сводка="de samenvatting",
               вопрос_говорит="wat zegt de samenvatting {О}?",
               ответ_ничего="niets: de samenvatting zwijgt {О}.",
               вопрос_ушло="over welke plaats zwijgt de samenvatting?", ответ_ушло="{О}.",
               вопрос_сколько="hoeveel plaatsen noemt de samenvatting?",
               вопрос_верна="klopt de samenvatting?",
               и_говорит="en de samenvatting zegt", а_говорит="maar de samenvatting zegt",
               двоеточие=": ", вопрос="?"),
    "pl": dict(состояние="{М} {ЕСТЬ} {n} {Т}", заметка="{n} {Т} {М}", сводка="podsumowanie",
               вопрос_говорит="co mówi podsumowanie {О}?",
               ответ_ничего="nic: podsumowanie milczy {О}.",
               вопрос_ушло="o jakim miejscu podsumowanie milczy?", ответ_ушло="{О}.",
               вопрос_сколько="ile miejsc wymienia podsumowanie?",
               вопрос_верна="czy podsumowanie jest poprawne?",
               и_говорит="i podsumowanie mówi", а_говорит="ale podsumowanie mówi",
               двоеточие=": ", вопрос="?"),
}
ФОРМЫ = ("говорит", "молчит", "сколько_мест", "что_ушло", "сводка_верна", "сводка_лжёт",
         "лента_верна", "лента_лжёт")


def _пакет(язык):
    return json.loads((_ПАКЕТЫ / f"{язык}.json").read_text(encoding="utf-8"))


# СЛОВА ДА И НЕТ ЧИТАЮТСЯ У ПАКЕТА (М-284) — вердикт не объявляется домом дважды.
ДА = {язык: str((_пакет(язык).get("polarity") or {}).get("yes", ["да"])[0]) for язык in ЯЗЫКИ}
НЕТ = {язык: str((_пакет(язык).get("polarity") or {}).get("no", ["нет"])[0]) for язык in ЯЗЫКИ}
for _яз in ЯЗЫКИ:
    assert ДА[_яз] and ДА[_яз] != "None", (_яз, "the pack declares no word of assent")
    assert НЕТ[_яз] and НЕТ[_яз] != "None", (_яз, "the pack declares no word of denial")
    # ГОЛОВА ОТКАЗА ЕСТЬ ГОЛОВА ДОМА ПАРЫ: «ничего» открывает тот же отказ, что «не знаю»,
    # и стоит в том же месте — перед двоеточием основания. Проверяется формой дома пары.
    assert S.РАМКИ[_яз]["без_данных"].count(":") >= 1, (_яз, "the pair house lost its refusal")


def _вещь(язык, Т, c):
    """The count form of the thing — the tool house's things, the pack's own counting rule."""
    return S._счёт(T.ВЕЩИ[язык][Т % len(T.ВЕЩИ[язык])], c, язык)


def _числа(P, сдвиг):
    """The counts of an episode's places: a stride over the row, never a repeat inside a page."""
    return tuple(ЧИСЛА[(сдвиг * 5 + i * 3) % len(ЧИСЛА)] for i in range(P))


def _порча(числа, k):
    """What a distorting note says instead of the truth: the next number of the row."""
    return ЧИСЛА[(ЧИСЛА.index(числа[k]) + 1 + k) % len(ЧИСЛА)] if числа[k] in ЧИСЛА else числа[k] + 1


def _состояние(язык, i, место_дыра=None, число_дыра="n%d", вещь_дыра="Тn%d", есть_дыра="ЕСТЬ%d"):
    """The story's sentence about one place, with its holes named by the place's index.

    С «место_дыра» место само становится дырой: так ответ о хранимом месте обязан
    НАЗВАТЬ спрошенное место, и подмена места ловится законом, а не молчанием."""
    место = ("{%s}" % место_дыра) if место_дыра else МЕСТА[язык][i][0]
    с = РЕЧЬ[язык]["состояние"].replace("{М}", место)
    с = с.replace("{n}", "{%s}" % (число_дыра % i)).replace("{Т}", "{%s}" % (вещь_дыра % i))
    return с.replace("{ЕСТЬ}", "{%s}" % (есть_дыра % i))


def _заметка(язык, i, число_дыра="n%d", вещь_дыра="Тn%d"):
    """One item of the note: a number, its thing and its place — no copula, a note is telegraphic."""
    з = РЕЧЬ[язык]["заметка"].replace("{М}", МЕСТА[язык][i][0])
    return з.replace("{n}", "{%s}" % (число_дыра % i)).replace("{Т}", "{%s}" % (вещь_дыра % i))


def _сшить(язык, имена):
    """«the folder and the box», «папка, ящик и список» — a list in the language's own seam."""
    if len(имена) == 1:
        return имена[0]
    return ", ".join(имена[:-1]) + " " + СОЮЗ[язык] + " " + имена[-1]


def рамка_фактов(язык, форма, P, выкинуто, спрошено=None):
    """The page of an episode of states and its note. The frame names which places the note
    keeps and which place the question asks; the law is the judge's."""
    р = РЕЧЬ[язык]
    оставлены = [i for i in range(P) if i != выкинуто]
    история = " ".join(_состояние(язык, i) + "." for i in range(P))
    if форма == "сводка_лжёт":
        # ИСКАЖЁННОЕ ЧИСЛО ЖИВЁТ В СВОЕЙ ДЫРЕ: судья требует, чтобы оно ОТЛИЧАЛОСЬ.
        куски = [_заметка(язык, i, "p%d" if i == спрошено else "n%d", "Тp%d" if i == спрошено else "Тn%d")
                 for i in оставлены]
    else:
        куски = [_заметка(язык, i) for i in оставлены]
    сводка = р["сводка"] + р["двоеточие"] + ", ".join(куски) + "."
    начало = история + " " + сводка
    if форма == "говорит":
        вопрос = р["вопрос_говорит"].replace("{О}", МЕСТА[язык][спрошено][2])
        ответ = _состояние(язык, спрошено, место_дыра="ЛОК") + "."
    elif форма == "молчит":
        вопрос = р["вопрос_говорит"].replace("{О}", МЕСТА[язык][спрошено][2])
        ответ = р["ответ_ничего"]                       # «{О}» остаётся дырой: место судится
    elif форма == "сколько_мест":
        вопрос = р["вопрос_сколько"]
        имена = ["{ИМЯ%d}" % j for j in range(len(оставлены))]
        ответ = "{МЕСТ}" + р["двоеточие"] + _сшить(язык, имена) + "."
    elif форма == "что_ушло":
        вопрос = р["вопрос_ушло"]
        ответ = р["ответ_ушло"]                          # «{О}» остаётся дырой
    elif форма == "сводка_верна":
        вопрос = р["вопрос_верна"]
        ответ = (ДА[язык] + р["двоеточие"] + _состояние(язык, спрошено) + ШОВ_И[язык]
                 + р["и_говорит"] + " {n%d}." % спрошено)
    else:                                   # сводка_лжёт
        вопрос = р["вопрос_верна"]
        ответ = (НЕТ[язык] + р["двоеточие"] + _состояние(язык, спрошено) + ", "
                 + р["а_говорит"] + " {p%d}." % спрошено)
    return начало + " " + вопрос + " " + ответ


def рамка_ленты(язык, форма, фигура):
    """The page of a TAPE compacted to one number: three acts, a note that says the state
    after them, and the check of that note against the tape's own ledger."""
    р = РЕЧЬ[язык]
    шаги = []
    for i, знак in enumerate(фигура):
        клеть = {"+": E.РЕЧЬ[язык]["шаг_плюс"], "−": E.РЕЧЬ[язык]["шаг_минус"]}[знак]
        клеть = клеть.replace("{П}", E.ПОРЯДОК[язык][i])
        клеть = клеть.replace("{m}", "{m%d}" % (i + 1)).replace("{Тm}", "{Тm%d}" % (i + 1))
        шаги.append(клеть)
    начало = E.РЕЧЬ[язык]["начало"].replace("{М}", МЕСТА[язык][0][0])
    история = " ".join([начало] + шаги)
    # СВОДКА ЛЕНТЫ — ОДНА ЗАМЕТКА: итог, его вещь и место. В верной форме её число есть та же
    # дыра, что конец леджера, и разойтись они не могут; в лживой — своя дыра, и судья
    # требует расхождения.
    дыра = "v" if форма == "лента_верна" else "w"
    заметка = (РЕЧЬ[язык]["заметка"].replace("{М}", МЕСТА[язык][0][0])
               .replace("{n}", "{%s}" % дыра).replace("{Т}", "{Т%s}" % дыра))
    сводка = р["сводка"] + р["двоеточие"] + заметка + "."
    леджер = E._леджер(фигура, шаги, 0, 3)
    если = ДА[язык] if форма == "лента_верна" else НЕТ[язык]
    хвост = (р["и_говорит"] + " {v}.") if форма == "лента_верна" else (р["а_говорит"] + " {w}.")
    шов = ШОВ_И[язык] if форма == "лента_верна" else ", "
    ответ = если + р["двоеточие"] + леджер + шов + хвост
    return история + " " + сводка + " " + р["вопрос_верна"] + " " + ответ


def рамка(язык, форма, вид):
    if форма in ("лента_верна", "лента_лжёт"):
        return рамка_ленты(язык, форма, вид["фигура"])
    return рамка_фактов(язык, форма, вид["P"], вид["выкинуто"], вид.get("спрошено"))


def страница_фактов(язык, форма, Т, P, выкинуто, сдвиг, спрошено=None):
    числа = _числа(P, сдвиг)
    поля = {}
    for i in range(P):
        поля["n%d" % i] = числа[i]
        поля["Тn%d" % i] = _вещь(язык, Т, числа[i])
        поля["ЕСТЬ%d" % i] = T._есть(язык, числа[i]) if язык in T.ЕСТЬ else ""
    if форма == "сводка_лжёт":
        порча = _порча(числа, спрошено)
        поля["p%d" % спрошено] = порча
        поля["Тp%d" % спрошено] = _вещь(язык, Т, порча)
    оставлены = [i for i in range(P) if i != выкинуто]
    поля["МЕСТ"] = СЛОВА_МЕСТ[язык][len(оставлены)]
    for j, i in enumerate(оставлены):
        поля["ИМЯ%d" % j] = МЕСТА[язык][i][1]
    if спрошено is not None:
        поля["ЛОК"] = МЕСТА[язык][спрошено][0]
        поля["О"] = МЕСТА[язык][спрошено][2]
    if форма == "что_ушло":
        поля["О"] = МЕСТА[язык][выкинуто][2]
    return рамка_фактов(язык, форма, P, выкинуто, спрошено).format(**поля)


def страница_ленты(язык, форма, Т, n, фигура, шаги, порча=None):
    счёты = E._счёты(n, фигура, шаги)
    v = счёты[2]
    поля = dict(n=n, Тn=_вещь(язык, Т, n), v=v, Тv=_вещь(язык, Т, v), М=МЕСТА[язык][0][0])
    for i, m in enumerate(шаги):
        поля["m%d" % (i + 1)] = m
        поля["Тm%d" % (i + 1)] = _вещь(язык, Т, m)
    if язык in T.ЕСТЬ:
        поля["ЕСТЬn"] = T._есть(язык, n)
        поля["ЕСТЬv"] = T._есть(язык, v)
    if форма == "лента_лжёт":
        поля["w"] = порча
        поля["Тw"] = _вещь(язык, Т, порча)
    return рамка_ленты(язык, форма, фигура).format(**поля)


ФИГУРЫ = (("+", "−", "+"), ("+", "+", "−"), ("−", "+", "+"))
НАЧАЛА_ЛЕНТЫ = tuple(range(8, 21, 2))     # 8, 10, 12, 14, 16, 18, 20


def _шаги_ленты(i):
    return (1 + i % 5, 1 + (i * 2) % 4, 2 + (i * 3) % 5)


def _показы():
    вон = {}
    for язык in ЯЗЫКИ:
        видов = len(T.ВЕЩИ[язык])
        for P in МЕСТ:
            for выкинуто in range(P):
                оставлены = [i for i in range(P) if i != выкинуто]
                for сдвиг in СДВИГИ:
                  for Т in range(видов):
                    for спрошено in оставлены:
                        вон[страница_фактов(язык, "говорит", Т, P, выкинуто, сдвиг, спрошено)] = (язык, "говорит")
                    вон[страница_фактов(язык, "молчит", Т, P, выкинуто, сдвиг, выкинуто)] = (язык, "молчит")
                    вон[страница_фактов(язык, "сколько_мест", Т, P, выкинуто, сдвиг)] = (язык, "сколько_мест")
                    вон[страница_фактов(язык, "что_ушло", Т, P, выкинуто, сдвиг)] = (язык, "что_ушло")
                    вон[страница_фактов(язык, "сводка_верна", Т, P, выкинуто, сдвиг, оставлены[0])] = (язык, "сводка_верна")
                    вон[страница_фактов(язык, "сводка_лжёт", Т, P, выкинуто, сдвиг, оставлены[-1])] = (язык, "сводка_лжёт")
        for i, n in enumerate(НАЧАЛА_ЛЕНТЫ):
            шаги = _шаги_ленты(i)
            for ф, фигура in enumerate(ФИГУРЫ):
                счёты = E._счёты(n, фигура, шаги)
                if min(счёты) < 1:
                    continue
                Т = (i + ф) % видов
                вон[страница_ленты(язык, "лента_верна", Т, n, фигура, шаги)] = (язык, "лента_верна")
                порча = счёты[2] + 1 + (i % 3)
                вон[страница_ленты(язык, "лента_лжёт", Т, n, фигура, шаги, порча)] = (язык, "лента_лжёт")
    return вон


ПОКАЗЫ = _показы()


def _альт(слова):
    """Branches ordered by content, never by the set's own order (закон детерминизма)."""
    return "(?:" + "|".join(re.escape(с) for с in sorted({с for с in слова if с}, key=lambda с: (-len(с), с))) + ")"


def _образец(язык, шаблон):
    """One pattern over the whole page; the i-th occurrence of a hole is «h_<hole>__i»."""
    вещи = _альт(T.ФОРМЫ_ВЕЩЕЙ[язык])
    есть = _альт(T.ЕСТЬ[язык]) if язык in T.ЕСТЬ else None
    дыры = {"n": r"\d+", "v": r"\d+", "w": r"\d+", "Тn": вещи, "Тv": вещи, "Тw": вещи,
            "М": _альт([м[0] for м in МЕСТА[язык]]), "ЛОК": _альт([м[0] for м in МЕСТА[язык]]),
            "О": _альт([м[2] for м in МЕСТА[язык]]), "МЕСТ": _альт(СЛОВА_МЕСТ[язык].values())}
    for i in range(3):
        дыры["ИМЯ%d" % i] = _альт([м[1] for м in МЕСТА[язык]])
    for i in range(4):
        дыры["n%d" % i] = r"\d+"
        дыры["Тn%d" % i] = вещи
        дыры["p%d" % i] = r"\d+"
        дыры["Тp%d" % i] = вещи
        дыры["ЕСТЬ%d" % i] = есть if есть else ""
    for i in (1, 2, 3):
        дыры["m%d" % i] = r"\d+"
        дыры["Тm%d" % i] = вещи
    if есть:
        дыры["ЕСТЬn"] = есть
        дыры["ЕСТЬv"] = есть
    счёт, куски = {}, []
    for кусок in re.split(r"(\{[^}]+\})", шаблон):
        if кусок.startswith("{"):
            дыра = кусок[1:-1]
            счёт[дыра] = счёт.get(дыра, 0) + 1
            узор = дыры[дыра]
            куски.append(f"(?P<h_{дыра}__{счёт[дыра]}>{узор})" if узор else "")
        else:
            куски.append(re.escape(кусок))
    return re.compile("^" + "".join(куски) + "$")


def _все_рамки():
    """Every concrete frame of the house: (pattern, language, form, shape)."""
    вон = []
    for язык in ЯЗЫКИ:
        for P in МЕСТ:
            for выкинуто in range(P):
                вид = {"P": P, "выкинуто": выкинуто}
                вон.append((_образец(язык, рамка_фактов(язык, "сколько_мест", P, выкинуто)),
                            язык, "сколько_мест", dict(вид)))
                вон.append((_образец(язык, рамка_фактов(язык, "что_ушло", P, выкинуто)),
                            язык, "что_ушло", dict(вид)))
                # ВОПРОС ВПРАВЕ СПРОСИТЬ О ЛЮБОМ МЕСТЕ — и о том, что сводка выкинула, и о
                # том, что оставила: страница, объявившая молчание о хранимом месте, ЕСТЬ
                # рамка дома, и лжёт она по закону судьи, а не по отсутствию образца.
                for спрошено in range(P):
                    для = dict(вид, спрошено=спрошено)
                    вон.append((_образец(язык, рамка_фактов(язык, "говорит", P, выкинуто, спрошено)),
                                язык, "говорит", dict(для)))
                    вон.append((_образец(язык, рамка_фактов(язык, "молчит", P, выкинуто, спрошено)),
                                язык, "молчит", dict(для)))
                    if спрошено != выкинуто:
                        вон.append((_образец(язык, рамка_фактов(язык, "сводка_верна", P, выкинуто, спрошено)),
                                    язык, "сводка_верна", dict(для)))
                        вон.append((_образец(язык, рамка_фактов(язык, "сводка_лжёт", P, выкинуто, спрошено)),
                                    язык, "сводка_лжёт", dict(для)))
        for фигура in ФИГУРЫ:
            вон.append((_образец(язык, рамка_ленты(язык, "лента_верна", фигура)),
                        язык, "лента_верна", {"фигура": фигура}))
            вон.append((_образец(язык, рамка_ленты(язык, "лента_лжёт", фигура)),
                        язык, "лента_лжёт", {"фигура": фигура}))
    return вон


ОБРАЗЦЫ = _все_рамки()


def _значения(м):
    """The holes of a match; a hole repeated in the frame must carry ONE value."""
    вон = {}
    for ключ, знач in м.groupdict().items():
        дыра, _ = ключ[2:].rsplit("__", 1)
        if дыра in вон and вон[дыра] != знач:
            return None
        вон[дыра] = знач
    return вон


def _вид_вещи(язык, зн, пары):
    """Every count form of the page is the form of ITS number and of ONE thing."""
    виды = None
    for дыра, число in пары:
        if дыра not in зн:
            continue
        свои = {Т for Т in T.ФОРМЫ_ВЕЩЕЙ[язык].get(зн[дыра], set())
                if Т != "строка" and S._счёт(T.ВЕЩИ[язык][Т], число, язык) == зн[дыра]}
        if not свои:
            return None
        виды = свои if виды is None else виды & свои
        if not виды:
            return None
    return виды


def _вердикт(язык, форма, вид, зн):
    if форма in ("лента_верна", "лента_лжёт"):
        фигура = вид["фигура"]
        n = int(зн["n"])
        шаги = [int(зн["m%d" % i]) for i in (1, 2, 3)]
        счёты = E._счёты(n, фигура, шаги)
        if min(счёты) < 1 or n < 1:
            return False
        # ЛЕДЖЕР ЛЕНТЫ ПЕРЕСЧИТЫВАЕТСЯ, И СВОДКА СВЕРЯЕТСЯ С НИМ
        if int(зн["v"]) != счёты[2]:
            return False
        итог = int(зн["w"]) if форма == "лента_лжёт" else int(зн["v"])
        if форма == "лента_лжёт" and итог == счёты[2]:
            return False      # «нет» над верной сводкой есть ложь
        пары = [("Тn", n), ("Тv", счёты[2])] + [("Тm%d" % i, шаги[i - 1]) for i in (1, 2, 3)]
        if форма == "лента_лжёт":
            пары.append(("Тw", итог))
        if _вид_вещи(язык, зн, пары) is None:
            return False
        if язык in T.ЕСТЬ:
            if "ЕСТЬn" in зн and зн["ЕСТЬn"] != T._есть(язык, n):
                return False
            if "ЕСТЬv" in зн and зн["ЕСТЬv"] != T._есть(язык, счёты[2]):
                return False
        return True
    P, выкинуто = вид["P"], вид["выкинуто"]
    спрошено = вид.get("спрошено")
    оставлены = [i for i in range(P) if i != выкинуто]
    числа = [int(зн["n%d" % i]) for i in range(P)]
    if any(c < 1 for c in числа):
        return False
    пары = [("Тn%d" % i, числа[i]) for i in range(P)]
    if форма == "сводка_лжёт":
        порча = int(зн["p%d" % спрошено])
        # ИСКАЖЕНИЕ ОБЯЗАНО БЫТЬ ИСКАЖЕНИЕМ: «нет» над верной заметкой есть ложь
        if порча == числа[спрошено] or порча < 1:
            return False
        пары.append(("Тp%d" % спрошено, порча))
    if _вид_вещи(язык, зн, пары) is None:
        return False
    if язык in T.ЕСТЬ:
        for i in range(P):
            ключ = "ЕСТЬ%d" % i
            if ключ in зн and зн[ключ] != T._есть(язык, числа[i]):
                return False
    if форма == "говорит":
        # ОТВЕЧАЕТ ЛИШЬ ТО МЕСТО, ЧТО СВОДКА ХРАНИТ, И ОТВЕТ НАЗЫВАЕТ СПРОШЕННОЕ МЕСТО
        return спрошено in оставлены and зн.get("ЛОК") == МЕСТА[язык][спрошено][0]
    if форма == "молчит":
        # МОЛЧАНИЕ ОБЪЯВЛЯЕТСЯ ЛИШЬ О ВЫКИНУТОМ МЕСТЕ, И ИМЕННО О СПРОШЕННОМ
        return спрошено == выкинуто and зн.get("О") == МЕСТА[язык][спрошено][2]
    if форма == "что_ушло":
        # УШЕДШИМ НАЗЫВАЕТСЯ РОВНО ТО МЕСТО, КОТОРОГО СВОДКА НЕ ДЕРЖИТ
        return зн.get("О") == МЕСТА[язык][выкинуто][2]
    if форма == "сколько_мест":
        # СЧЁТНОЕ СЛОВО ЕСТЬ СЛОВО ЧИСЛА ЗАМЕТОК, И СПИСОК ЕСТЬ СПИСОК ИХ МЕСТ В ПОРЯДКЕ
        if зн.get("МЕСТ") != СЛОВА_МЕСТ[язык][len(оставлены)]:
            return False
        return [зн.get("ИМЯ%d" % j) for j in range(len(оставлены))] == [МЕСТА[язык][i][1] for i in оставлены]
    if форма == "сводка_верна":
        return спрошено in оставлены
    if форма == "сводка_лжёт":
        return спрошено in оставлены
    return False


def судить(строка):
    """(судимо, истинно): a page of a frame of the house whose note checks out; else silence."""
    с = строка.strip()
    if с in ПОКАЗЫ:
        return True, True
    for образ, язык, форма, вид in ОБРАЗЦЫ:
        м = образ.match(с)
        if not м:
            continue
        зн = _значения(м)
        if зн is None:
            return True, False
        return True, _вердикт(язык, форма, вид, зн)
    return False, False


def _хвост(с):
    """The start of the answer (after the last question mark)."""
    м = list(re.finditer(r"[?？] ", с))
    return м[-1].end() if м else 0


def _самопроверка():
    for показ in ПОКАЗЫ:
        assert судить(показ) == (True, True), показ
    мутанты = 0
    for язык in ЯЗЫКИ:
        Т, P, выкинуто, сдвиг = 0, 3, 2, 0
        числа = _числа(P, сдвиг)
        # (1) ОТВЕТ О ХРАНИМОМ МЕСТЕ НАЗЫВАЕТ ЧУЖОЕ ЧИСЛО
        г = страница_фактов(язык, "говорит", Т, P, выкинуто, сдвиг, 0)
        assert судить(г) == (True, True), г
        хв = _хвост(г)
        битая = г[:хв] + г[хв:].replace(str(числа[0]), str(числа[1]), 1)
        assert судить(битая) == (True, False), битая
        # (2) МОЛЧАНИЕ ОБЪЯВЛЕНО О МЕСТЕ, КОТОРОЕ СВОДКА ХРАНИТ
        м = страница_фактов(язык, "молчит", Т, P, выкинуто, сдвиг, выкинуто)
        assert судить(м) == (True, True), м
        битая = страница_фактов(язык, "молчит", Т, P, выкинуто, сдвиг, 0)
        assert судить(битая) == (True, False), битая
        # (3) ОТВЕТ О ВЫКИНУТОМ МЕСТЕ ГОВОРИТ ЧИСЛО ВМЕСТО МОЛЧАНИЯ
        битая = страница_фактов(язык, "говорит", Т, P, выкинуто, сдвиг, выкинуто)
        assert судить(битая) == (True, False), битая
        # (4) СЧЁТ МЕСТ НЕ ЕСТЬ ЧИСЛО ЗАМЕТОК
        с = страница_фактов(язык, "сколько_мест", Т, P, выкинуто, сдвиг)
        assert судить(с) == (True, True), с
        битая = с.replace(СЛОВА_МЕСТ[язык][2], СЛОВА_МЕСТ[язык][3])
        assert судить(битая) == (True, False), битая
        # (5) СПИСОК СВОДКИ НАЗЫВАЕТ ВЫКИНУТОЕ МЕСТО
        битая = с[:_хвост(с)] + с[_хвост(с):].replace(МЕСТА[язык][1][1], МЕСТА[язык][выкинуто][1], 1)
        assert судить(битая) == (True, False), битая
        # (6) УШЕДШИМ НАЗВАНО ХРАНИМОЕ МЕСТО
        у = страница_фактов(язык, "что_ушло", Т, P, выкинуто, сдвиг)
        assert судить(у) == (True, True), у
        битая = у[:_хвост(у)] + РЕЧЬ[язык]["ответ_ушло"].replace("{О}", МЕСТА[язык][0][2])
        assert судить(битая) == (True, False), битая
        # (7) ОТВЕТ О ХРАНИМОМ МЕСТЕ НАЗЫВАЕТ ДРУГОЕ МЕСТО
        битая = г[:_хвост(г)] + г[_хвост(г):].replace(МЕСТА[язык][0][0], МЕСТА[язык][1][0], 1)
        assert судить(битая) == (True, False), битая
        # (8) МОЛЧАНИЕ ОБЪЯВЛЕНО О ДРУГОМ МЕСТЕ, ЧЕМ СПРОШЕНО
        битая = м[:_хвост(м)] + м[_хвост(м):].replace(МЕСТА[язык][выкинуто][2], МЕСТА[язык][0][2], 1)
        assert судить(битая) == (True, False), битая
        # (6) «ДА» НАД ИСКАЖЁННОЙ ЗАМЕТКОЙ
        в = страница_фактов(язык, "сводка_верна", Т, P, выкинуто, сдвиг, 0)
        assert судить(в) == (True, True), в
        битая = в.replace(РЕЧЬ[язык]["сводка"] + РЕЧЬ[язык]["двоеточие"] + str(числа[0]),
                          РЕЧЬ[язык]["сводка"] + РЕЧЬ[язык]["двоеточие"] + str(числа[1]), 1)
        assert судить(битая) == (True, False), битая
        # (7) «НЕТ» НАД ВЕРНОЙ ЗАМЕТКОЙ
        л = страница_фактов(язык, "сводка_лжёт", Т, P, выкинуто, сдвиг, 1)
        assert судить(л) == (True, True), л
        порча = _порча(числа, 1)
        битая = л.replace(str(порча), str(числа[1]))
        assert судить(битая) == (True, False), битая
        мутанты += 10
        # (9) ЛЕНТА: ЛЕДЖЕР НЕ СХОДИТСЯ
        n, фигура, шаги = 10, ("+", "−", "+"), (2, 1, 3)
        лв = страница_ленты(язык, "лента_верна", Т, n, фигура, шаги)
        assert судить(лв) == (True, True), лв
        хв = _хвост(лв)
        битая = лв[:хв] + лв[хв:].replace("= 14", "= 15")
        assert судить(битая) == (True, False), битая
        # (10) ЛЕНТА: «НЕТ» НАД ВЕРНОЙ СВОДКОЙ
        лл = страница_ленты(язык, "лента_лжёт", Т, n, фигура, шаги, 15)
        assert судить(лл) == (True, True), лл
        битая = лл.replace("15", "14")
        assert судить(битая) == (True, False), битая
        мутанты += 2
        # (11) ЗАЧИН ВОПРОСА ОБЪЯВЛЕН ДОМОМ ПАРЫ
        for стр in (г, м, с, у, в, л, лв, лл):
            вопрос = стр[:стр.index("?") + 1].split(". ")[-1]
            assert asking.зачин_объявлен(вопрос) is not False, (язык, вопрос)
    for язык, форма, вид in (("ru", "говорит", (3, 2, 0)), ("en", "молчит", (3, 2, 2)),
                             ("de", "сколько_мест", (4, 1, None)), ("fr", "что_ушло", (3, 0, None)),
                             ("es", "сводка_верна", (3, 2, 0)), ("it", "сводка_лжёт", (4, 3, 1)),
                             ("pt", "говорит", (4, 0, 2)), ("nl", "молчит", (4, 2, 2)),
                             ("pl", "сводка_верна", (4, 1, 0))):
        P, выкинуто, спрошено = вид
        print("  ", страница_фактов(язык, форма, 0, P, выкинуто, 0, спрошено))
    for язык in ("ru", "en", "pl"):
        print("  ", страница_ленты(язык, "лента_верна", 0, 10, ("+", "−", "+"), (2, 1, 3)))
        print("  ", страница_ленты(язык, "лента_лжёт", 0, 10, ("+", "−", "+"), (2, 1, 3), 15))
    по_форме = {}
    for _, (язык, форма) in ПОКАЗЫ.items():
        по_форме[форма] = по_форме.get(форма, 0) + 1
    print(f"  мутантов поймано: {мутанты}")
    print(f"  дом пишет показов: {len(ПОКАЗЫ)} (языков {len(ЯЗЫКИ)}, форм {len(ФОРМЫ)}, образцов {len(ОБРАЗЦЫ)}): "
          + ", ".join(f"{ф} {к}" for ф, к in по_форме.items()))


if __name__ == "__main__":
    _самопроверка()
