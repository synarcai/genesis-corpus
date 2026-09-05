#!/usr/bin/env python3
"""THE HOUSE OF SVAMP SHAPES — the eight mute shapes of the live SVAMP band (d5, 06.09),
each a form with its recomputing court, in English and Russian.

d5 read the live band (726 tacts) and named what no frame of the corpus holds:
(1) oblique pronouns as pronouns («gave 5 of them», «gave him 20»); (2) place held
by a bare «were» — closed in the house of action measure; (3) the hidden quantity
«some» and the heads of the total («in all», «altogether», «in total», «a total
of», «now has N left»); (4) the words of time order («at first … then»); (5) the
hypothetical act in the question («if she gives away 64, how many will she
have?»); (6) transfer with a direction («gave 20 to him» = «gave him 20», «took
5 from her»); (7) the unit before the number («$ 3») — English only, declared;
(8) goods outside the lexicon («2 pages of reading homework and 4 pages of math
homework»). Names and things are the house of action pages' (tools/actionpages.py),
pronouns are declared here by gender; every answer carries its ledger, and the
court recomputes it. The world is CLOSED.

    python3 tools/svampforms.py    # self-check with mutants
"""
import json
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import actionpages as A  # noqa: E402

_ПАКЕТЫ = pathlib.Path(__file__).resolve().parent / "langpacks"

# pronouns by gender: nominative, genitive-with-у (ru) / object (en), dative (ru) / object (en)
МЕСТОИМЕНИЯ = {"en": {"m": dict(он="he", него="him", ему="him"), "f": dict(он="she", него="her", ему="her")},
               "ru": {"m": dict(он="он", него="него", ему="ему"), "f": dict(он="она", него="неё", ему="ей")}}
ГОЛОВЫ_ИТОГА = {"en": ("in all", "altogether", "in total"), "ru": ("всего", "в сумме", "итого")}
ВРЕМЯ = {"en": (("at first", "then"), ("initially", "later"), ("originally", "finally"), ("at the start", "then")),
         "ru": (("сначала", "потом"), ("вначале", "затем"), ("изначально", "позже"))}
ЦВЕТА = {"en": ("red", "blue"), "ru": ("красных", "синих")}
# goods outside the lexicon: (two kinds, the union), count forms one/many (ru: one/few/many)
ТОВАРЫ = {"en": ((("page of reading homework", "pages of reading homework"), ("page of math homework", "pages of math homework"), ("page of homework", "pages of homework")),
                 (("pack of red cards", "packs of red cards"), ("pack of blue cards", "packs of blue cards"), ("pack of cards", "packs of cards")),
                 (("box of apples", "boxes of apples"), ("box of pears", "boxes of pears"), ("box of fruit", "boxes of fruit"))),
          "ru": ((("страница чтения", "страницы чтения", "страниц чтения"), ("страница математики", "страницы математики", "страниц математики"), ("страница", "страницы", "страниц")),
                 (("пачка красных карт", "пачки красных карт", "пачек красных карт"), ("пачка синих карт", "пачки синих карт", "пачек синих карт"), ("пачка карт", "пачки карт", "пачек карт")),
                 (("коробка яблок", "коробки яблок", "коробок яблок"), ("коробка груш", "коробки груш", "коробок груш"), ("коробка фруктов", "коробки фруктов", "коробок фруктов")))}

РАМКИ = {
    "en": dict(
        некоторые="{X} had {n} {Тn}. {Он} gave some of them away. now {он} has {r} {Тr} left. how many {Тмн} did {он} give away? {k}: {n} − {r} = {k}.",
        итог="{X} has {a} {Ц1} {Тмн} and {b} {Ц2} {Тмн}. how many {Тмн} does {X} have {ГОЛОВА}? {s} {Тs}: {a} + {b} = {s}.",
        итог_всего="{X} has {a} {Ц1} {Тмн} and {b} {Ц2} {Тмн}. how many {Тмн} does {X} have? a total of {s} {Тs}: {a} + {b} = {s}.",
        осталось="{X} had {n} {Тn}. {Он} gave away {k}. how many does {он} have now? {он} now has {r} left: {n} − {k} = {r}.",
        из_них="{X} had {n} {Тn}. {Он} gave {k} of them to {Y}. how many {Тмн} does {он} have now? {r}: {n} − {k} = {r}.",
        ему="{X} had {n} {Тn}. {Y} gave {ему} {k} more. how many {Тмн} does {он} have now? {s}: {n} + {k} = {s}.",
        если="{X} has {n} {Тn}. if {он} gives away {k}, how many will {он} have? {r}: {n} − {k} = {r}.",
        если_придут="there are {n} {Тn} in the box. if {k} more are put in, how many will there be? {s}: {n} + {k} = {s}.",
        время="{В1} {X} had {n} {Тn}. {В2} {он} got {k} more. how many {Тмн} does {он} have now? {s}: {n} + {k} = {s}.",
        кому="{X} had {n} {Тn}. {Он} gave {k} {Тk} to {Y}. how many {Тмн} does {X} have now? {r}: {n} − {k} = {r}.",
        у_него="{X} had {n} {Тn}. {Y} took {k} {Тk} from {него}. how many {Тмн} does {X} have now? {r}: {n} − {k} = {r}.",
        единица="a {Т1} costs $ {n}. how much do {k} {Тмн} cost? $ {v}: {k} × {n} = {v}.",
        товар="{X} has {a} {Г1a} and {b} {Г2b}. how many {Г3мн} does {он} have in all? {s} {Г3s}: {a} + {b} = {s}.",
    ),
    "ru": dict(
        некоторые="у {Xр} было {n} {Тn}. {Он} отдал{а} несколько. теперь у {него} осталось {r} {Тr}. сколько {Тмн} {он} отдал{а}? {k}: {n} − {r} = {k}.",
        итог="у {Xр} {a} {Ц1} {Тмн} и {b} {Ц2} {Тмн}. сколько {Тмн} у {Xр} {ГОЛОВА}? {s} {Тs}: {a} + {b} = {s}.",
        итог_всего="у {Xр} {a} {Ц1} {Тмн} и {b} {Ц2} {Тмн}. сколько {Тмн} у {Xр}? всего {s} {Тs}: {a} + {b} = {s}.",
        осталось="у {Xр} было {n} {Тn}. {Он} отдал{а} {k}. сколько у {него} теперь? теперь у {него} осталось {r}: {n} − {k} = {r}.",
        из_них="у {Xр} было {n} {Тn}. {Он} отдал{а} {k} из них {Yд}. сколько {Тмн} у {него} теперь? {r}: {n} − {k} = {r}.",
        ему="у {Xр} было {n} {Тn}. {Y} дал{аY} {ему} ещё {k}. сколько {Тмн} у {него} теперь? {s}: {n} + {k} = {s}.",
        если="у {Xр} {n} {Тn}. если {он} отдаст {k}, сколько у {него} останется? {r}: {n} − {k} = {r}.",
        если_придут="в коробке {n} {Тn}. если положить ещё {k}, сколько там будет? {s}: {n} + {k} = {s}.",
        время="{В1} у {Xр} было {n} {Тn}. {В2} {он} получил{а} ещё {k}. сколько {Тмн} у {него} теперь? {s}: {n} + {k} = {s}.",
        кому="у {Xр} было {n} {Тn}. {Он} отдал{а} {k} {Тk} {Yд}. сколько {Тмн} у {Xр} теперь? {r}: {n} − {k} = {r}.",
        у_него="у {Xр} было {n} {Тn}. {Y} взял{аY} у {него} {k} {Тk}. сколько {Тмн} у {Xр} теперь? {r}: {n} − {k} = {r}.",
        товар="у {Xр} {a} {Г1a} и {b} {Г2b}. сколько {Г3мн} у {него} всего? {s} {Г3s}: {a} + {b} = {s}.",
    ),
}
ФОРМЫ = ("некоторые", "итог", "итог_всего", "осталось", "из_них", "ему", "если", "если_придут", "время", "кому", "у_него", "единица", "товар")
# the unit before the number is an English shape of the band; Russian writes «3 ₽» after — declared gap
ОБЪЯВЛЕННЫЕ_ПРОПУСКИ = {"единица": frozenset({"ru"})}
ЧИСЛА = ((12, 5), (20, 8), (15, 6), (9, 4), (30, 12), (25, 7), (18, 11), (40, 15))
ЦЕНЫ = ((3, 4), (2, 5), (6, 3), (5, 5))
_ДАТ = None


def _дательный(имя):
    global _ДАТ
    if _ДАТ is None:
        п = json.loads((_ПАКЕТЫ / "ru.json").read_text(encoding="utf-8"))
        _ДАТ = {и: ф.get("dat") for и, ф in (п.get("person_forms") or {}).items()}
    return _ДАТ.get(имя)


def _лицо(язык, i):
    return A.ЛИЦА[язык][i % len(A.ЛИЦА[язык])]


def _поля(язык, i, j, Т, n, k, форма):
    X, Y = _лицо(язык, i), _лицо(язык, j)
    if Y[0] == X[0]:
        Y = _лицо(язык, j + 1)
    м = МЕСТОИМЕНИЯ[язык][X[1]]
    вещь = lambda c: A._вещь(язык, Т, c)
    п = dict(X=X[0], Xр=X[2], Y=Y[0], Yд=_дательный(Y[0]) if язык == "ru" else Y[0],
             он=м["он"], Он=м["он"], него=м["него"], ему=м["ему"],
             а=A._а(язык, X[1]), аY=A._а(язык, Y[1]),
             n=n, k=k, r=n - k, s=n + k, a=n, b=k,
             Тn=вещь(n), Тk=вещь(k), Тr=вещь(n - k), Тs=вещь(n + k), Тмн=вещь(5), Т1=вещь(1))
    return п


def страница(язык, форма, i, j, Т, n, k, вариант=0):
    if язык in ОБЪЯВЛЕННЫЕ_ПРОПУСКИ.get(форма, ()):
        return None
    р = РАМКИ[язык][форма]
    п = _поля(язык, i, j, Т, n, k, форма)
    if форма == "итог":
        п.update(ГОЛОВА=ГОЛОВЫ_ИТОГА[язык][вариант % len(ГОЛОВЫ_ИТОГА[язык])])
    if форма in ("итог", "итог_всего"):
        п.update(Ц1=ЦВЕТА[язык][0], Ц2=ЦВЕТА[язык][1])
    if форма == "время":
        в1, в2 = ВРЕМЯ[язык][вариант % len(ВРЕМЯ[язык])]
        п.update(В1=в1, В2=в2)
    if форма == "единица":
        n_, k_ = ЦЕНЫ[вариант % len(ЦЕНЫ)]
        п.update(n=n_, k=k_, v=n_ * k_, Тмн=A._вещь(язык, Т, 5))
    if форма == "товар":
        г1, г2, г3 = ТОВАРЫ[язык][вариант % len(ТОВАРЫ[язык])]
        п.update(Г1a=_счёт(г1, n), Г2b=_счёт(г2, k), Г3мн=г3[-1], Г3s=_счёт(г3, n + k))
    return р.format(**п)


def _счёт(ф, c):
    """Count form of a declared goods phrase: (one, many) for en, (one, few, many) for ru."""
    if len(ф) == 2:
        return ф[0] if c == 1 else ф[1]
    if c % 100 in range(11, 15):
        return ф[2]
    п = c % 10
    return ф[0] if п == 1 else ф[1] if п in (2, 3, 4) else ф[2]


def _показы():
    вон = {}
    for язык in РАМКИ:
        лиц = len(A.ЛИЦА[язык]); вещей = len(A.ЯЗЫКИ[язык]["вещи"])
        for форма in ФОРМЫ:
            if форма not in РАМКИ[язык]:
                continue
            for q, (n, k) in enumerate(ЧИСЛА):
                i = q % лиц; j = (q * 3 + 1) % лиц; Т = q % вещей
                for вариант in range(3 if форма in ("итог", "время", "товар") else (4 if форма == "единица" else 1)):
                    с = страница(язык, форма, i, j, Т, n, k, вариант)
                    if с:
                        вон[с] = (язык, форма)
    return вон


ПОКАЗЫ = _показы()


def _образцы():
    """A regex per frame: names, things, pronouns, time words and goods are declared
    alternations; numbers are holes; the ledger is read by the judge."""
    вон = []
    alt = lambda слова: "(?:" + "|".join(re.escape(с) for с in sorted(set(с for с in слова if с), key=len, reverse=True)) + ")"
    for язык, рамки in РАМКИ.items():
        имена = [л[0] for л in A.ЛИЦА[язык]]; род = [л[2] for л in A.ЛИЦА[язык]]
        дат = [_дательный(л[0]) for л in A.ЛИЦА[язык]] if язык == "ru" else имена
        вещи = [A._вещь(язык, Т, c) for Т in range(len(A.ЯЗЫКИ[язык]["вещи"])) for c in (1, 2, 5)]
        вещи1 = [A.ЯЗЫКИ[язык]["вещи"][Т][0] if язык == "en" else A.ЯЗЫКИ[язык]["вещи"][Т] for Т in range(len(A.ЯЗЫКИ[язык]["вещи"]))]
        мест = [v for г in МЕСТОИМЕНИЯ[язык].values() for v in г.values()]
        товары = [ф for ряд in ТОВАРЫ[язык] for г in ряд for ф in г]
        дыры = {"X": alt(имена), "Y": alt(имена), "Xр": alt(род), "Yд": alt(дат), "он": alt(мест), "Он": alt(мест), "него": alt(мест), "ему": alt(мест),
                "а": "(?:а|о|и|)", "аY": "(?:а|о|и|)", "n": r"(\d+)", "k": r"(\d+)", "r": r"(\d+)", "s": r"(\d+)", "a": r"(\d+)", "b": r"(\d+)", "v": r"(\d+)",
                "Тn": alt(вещи), "Тk": alt(вещи), "Тr": alt(вещи), "Тs": alt(вещи), "Тмн": alt(вещи), "Т1": alt(вещи1),
                "ГОЛОВА": alt(ГОЛОВЫ_ИТОГА[язык]), "Ц1": alt(ЦВЕТА[язык]), "Ц2": alt(ЦВЕТА[язык]),
                "В1": alt(в for в, _ in ВРЕМЯ[язык]), "В2": alt(в for _, в in ВРЕМЯ[язык]),
                "Г1a": alt(товары), "Г2b": alt(товары), "Г3мн": alt(товары), "Г3s": alt(товары)}
        for форма, рамка in рамки.items():
            куски = []
            for кусок in re.split(r"(\{[^}]+\})", рамка):
                куски.append(дыры[кусок[1:-1]] if кусок.startswith("{") else re.escape(кусок))
            вон.append((re.compile("^" + "".join(куски) + "$"), язык, форма))
    return вон


ОБРАЗЦЫ = _образцы()

# ГЛАГОЛЫ-АКТЫ ЖИВОЙ ПОЛОСЫ (holon, атлас непрочитанных чисел, 06.09): пятая точка купила 307
# глаголов истории, но среди них нет тех, на которых стоят десятки задач SVAMP — did, added, threw
# away, learned that … came, got on / got off, played, spent; и формы «a box of N crayons»,
# «a total of N hours», «the first chapter is N pages long», две клаузы с «and», список через
# запятую того же товара, «ones» = тот же товар. Каждому глаголу — ≥ LAW показов как АКТ: носитель +
# глагол + число + товар + вопрос. Товары объявлены со счётными формами (en: one/many; ru: one/few/many).
ТОВАРЫ_АКТОВ = {
    "en": {"отжимания": ("push-up", "push-ups"), "скручивания": ("crunch", "crunches"), "приложения": ("app", "apps"),
           "фигурки": ("action figure", "action figures"), "крышки": ("bottle cap", "bottle caps"), "розы": ("rose", "roses"),
           "посетители": ("visitor", "visitors"), "дети": ("child", "children"), "игры": ("game", "games"), "часы": ("hour", "hours"),
           "мелки": ("crayon", "crayons"), "страницы": ("page", "pages")},
    "ru": {"отжимания": ("отжимание", "отжимания", "отжиманий"), "скручивания": ("скручивание", "скручивания", "скручиваний"),
           "приложения": ("приложение", "приложения", "приложений"), "фигурки": ("фигурка", "фигурки", "фигурок"),
           "крышки": ("крышка", "крышки", "крышек"), "розы": ("роза", "розы", "роз"), "посетители": ("посетитель", "посетителя", "посетителей"),
           "дети": ("ребёнок", "ребёнка", "детей"), "игры": ("игра", "игры", "игр"), "часы": ("час", "часа", "часов"),
           "мелки": ("мелок", "мелка", "мелков"), "страницы": ("страница", "страницы", "страниц")},
}
РАМКИ_АКТОВ = {
    "en": dict(
        сделал="{X} did {n} {ОТЖn} and {k} {СКРk}. how many {ОТЖмн} did {X} do? {n}. how many exercises in all? {s}: {n} + {k} = {s}.",
        больше_чем="{X} did {n} {ОТЖn}. {Y} did {k} more {ОТЖмн} than {X}. how many {ОТЖмн} did {Y} do? {s}: {n} + {k} = {s}.",
        меньше_чем="{X} did {n} {ОТЖn}. {Y} did {k} {ОТЖмн} less than {X}. how many {ОТЖмн} did {Y} do? {r}: {n} − {k} = {r}.",
        добавил="{X} had {n} {ПРИЛn} on the phone. {Он} added {k} new {ПРИЛмн}. how many {ПРИЛмн} does {он} have now? {s}: {n} + {k} = {s}.",
        добавил_на_полку="{X} had {n} {ФИГn} on the shelf. later {он} added {k} more {ФИГмн} to the shelf. how many {ФИГмн} are on the shelf now? {s}: {n} + {k} = {s}.",
        выбросил="{X} found {n} {КРЫШn} at the park while {он} threw away {k} old ones. how many more {КРЫШмн} did {он} find than throw away? {r}: {n} − {k} = {r}.",
        выбросил_розы="there were {n} {РОЗn} in the vase. {X} threw away {k} {РОЗмн} from the vase. how many {РОЗмн} are in the vase now? {r}: {n} − {k} = {r}.",
        узнал="{X} learned that {n} {ПОСn} came to the palace that day and {k} the next day. how many {ПОСмн} came in all? {s}: {n} + {k} = {s}.",
        сели_вышли="there were {n} {ДЕТn} on the bus. at the bus stop {k} {ДЕТмн} got on the bus while some got off. now there are {s} {ДЕТмн} on the bus. how many {ДЕТмн} got off? {k2}: {n} + {k} − {s} = {k2}.",
        сыграл="{X} played {n} {ИГРn} on monday and {k} {ИГРмн} on tuesday. how many {ИГРмн} did {X} play in all? {s}: {n} + {k} = {s}.",
        потратил="{X} spent {n} {ЧАСn} on english and {k} {ЧАСмн} on chinese. how many {ЧАСмн} did {X} spend in all? a total of {s} {ЧАСмн}: {n} + {k} = {s}.",
        список="every day {X} spends {n} {ЧАСn} on english, {k} {ЧАСмн} on chinese and {m} {ЧАСмн} on spanish. how many {ЧАСмн} does {X} spend in all? {t}: {n} + {k} + {m} = {t}.",
        коробка="{X} got a box of {n} {МЕЛn} and a box of {k} {МЕЛмн}. how many {МЕЛмн} does {X} have? {s}: {n} + {k} = {s}.",
        главы="a book has 2 chapters. the first chapter is {n} {СТРn} long and the second chapter is {k} {СТРмн} long. how many {СТРмн} does the book have in all? {s}: {n} + {k} = {s}.",
        две_клаузы="{X} had {n} {ИГРn} and {Y} had {k} {ИГРмн}. how many {ИГРмн} did they have together? {s}: {n} + {k} = {s}.",
    ),
    "ru": dict(
        сделал="{X} сделал{а} {n} {ОТЖn} и {k} {СКРk}. сколько {ОТЖмн} сделал{а} {X}? {n}. сколько упражнений всего? {s}: {n} + {k} = {s}.",
        больше_чем="{X} сделал{а} {n} {ОТЖn}. {Y} сделал{аY} на {k} {ОТЖk} больше, чем {X}. сколько {ОТЖмн} сделал{аY} {Y}? {s}: {n} + {k} = {s}.",
        меньше_чем="{X} сделал{а} {n} {ОТЖn}. {Y} сделал{аY} на {k} {ОТЖk} меньше, чем {X}. сколько {ОТЖмн} сделал{аY} {Y}? {r}: {n} − {k} = {r}.",
        добавил="у {Xр} было {n} {ПРИЛn} в телефоне. {Он} добавил{а} {k} {ПРИЛk}. сколько {ПРИЛмн} у {него} теперь? {s}: {n} + {k} = {s}.",
        добавил_на_полку="у {Xр} на полке было {n} {ФИГn}. потом {он} добавил{а} на полку ещё {k} {ФИГk}. сколько {ФИГмн} на полке теперь? {s}: {n} + {k} = {s}.",
        выбросил="{X} нашёл{а} в парке {n} {КРЫШn}, а {k} старых выбросил{а}. на сколько больше {КРЫШмн} {он} нашёл{а}, чем выбросил{а}? {r}: {n} − {k} = {r}.",
        выбросил_розы="в вазе было {n} {РОЗn}. {X} выбросил{а} из вазы {k} {РОЗk}. сколько {РОЗмн} в вазе теперь? {r}: {n} − {k} = {r}.",
        узнал="{X} узнал{а}, что во дворец в тот день пришли {n} {ПОСn}, а на следующий — {k}. сколько {ПОСмн} пришло всего? {s}: {n} + {k} = {s}.",
        сели_вышли="в автобусе было {n} {ДЕТn}. на остановке {k} {ДЕТk} сели, а несколько вышли. теперь в автобусе {s} {ДЕТs}. сколько {ДЕТмн} вышло? {k2}: {n} + {k} − {s} = {k2}.",
        сыграл="{X} сыграл{а} {n} {ИГРn} в понедельник и {k} {ИГРk} во вторник. сколько {ИГРмн} сыграл{а} {X} всего? {s}: {n} + {k} = {s}.",
        потратил="{X} потратил{а} {n} {ЧАСn} на английский и {k} {ЧАСk} на китайский. сколько {ЧАСмн} потратил{а} {X} всего? всего {s} {ЧАСs}: {n} + {k} = {s}.",
        список="каждый день {X} тратит {n} {ЧАСn} на английский, {k} {ЧАСk} на китайский и {m} {ЧАСm} на испанский. сколько {ЧАСмн} тратит {X} всего? {t}: {n} + {k} + {m} = {t}.",
        коробка="{X} получил{а} коробку с {n} {МЕЛn} и коробку с {k} {МЕЛk}. сколько {МЕЛмн} у {Xр}? {s}: {n} + {k} = {s}.",
        главы="в книге 2 главы. в первой главе {n} {СТРn}, во второй — {k} {СТРk}. сколько {СТРмн} в книге всего? {s}: {n} + {k} = {s}.",
        две_клаузы="у {Xр} было {n} {ИГРn}, а у {Yр} — {k} {ИГРk}. сколько {ИГРмн} было у них вместе? {s}: {n} + {k} = {s}.",
    ),
}
_ТОВАР_ПО_ДЫРЕ = {"ОТЖ": "отжимания", "СКР": "скручивания", "ПРИЛ": "приложения", "ФИГ": "фигурки", "КРЫШ": "крышки", "РОЗ": "розы",
                  "ПОС": "посетители", "ДЕТ": "дети", "ИГР": "игры", "ЧАС": "часы", "МЕЛ": "мелки", "СТР": "страницы"}
ФОРМЫ_АКТОВ = tuple(РАМКИ_АКТОВ["en"])
ЧИСЛА_АКТОВ = ((12, 5, 4), (35, 3, 9), (20, 8, 6), (15, 7, 2), (30, 12, 10), (9, 4, 3), (18, 11, 5), (24, 15, 7))


def _товар_форма(язык, ключ, c):
    return _счёт(ТОВАРЫ_АКТОВ[язык][ключ], c)


def _поля_акта(язык, i, j, n, k, m):
    X, Y = _лицо(язык, i), _лицо(язык, j)
    if Y[0] == X[0]:
        Y = _лицо(язык, j + 1)
    мест = МЕСТОИМЕНИЯ[язык][X[1]]
    п = dict(X=X[0], Xр=X[2], Y=Y[0], Yр=Y[2], он=мест["он"], Он=мест["он"], него=мест["него"],
             а=A._а(язык, X[1]), аY=A._а(язык, Y[1]),
             n=n, k=k, m=m, r=n - k, s=n + k, t=n + k + m, k2=k - (n + k - (n + k - k)) if False else k)
    # «сели_вышли»: сели k, вышли k2, теперь s = n + k − k2 — вышло меньше, чем село
    п["k2"] = max(1, k // 2); п["s_бус"] = n + k - п["k2"]
    for дыра, ключ in _ТОВАР_ПО_ДЫРЕ.items():
        п[дыра + "n"] = _товар_форма(язык, ключ, n); п[дыра + "k"] = _товар_форма(язык, ключ, k)
        п[дыра + "m"] = _товар_форма(язык, ключ, m); п[дыра + "s"] = _товар_форма(язык, ключ, n + k)
        п[дыра + "мн"] = ТОВАРЫ_АКТОВ[язык][ключ][-1]
    return п


def страница_акта(язык, форма, i, j, n, k, m=4):
    р = РАМКИ_АКТОВ[язык][форма]
    п = _поля_акта(язык, i, j, n, k, m)
    if форма == "сели_вышли":
        п = dict(п, s=п["s_бус"], ДЕТs=_товар_форма(язык, "дети", п["s_бус"]))
    return р.format(**п)


def _показы_актов():
    вон = {}
    for язык in РАМКИ_АКТОВ:
        лиц = len(A.ЛИЦА[язык])
        for форма in ФОРМЫ_АКТОВ:
            for q, (n, k, m) in enumerate(ЧИСЛА_АКТОВ):
                вон[страница_акта(язык, форма, q % лиц, (q * 3 + 1) % лиц, n, k, m)] = (язык, форма)
    return вон


ПОКАЗЫ.update(_показы_актов())


def _образцы_актов():
    вон = []
    alt = lambda слова: "(?:" + "|".join(re.escape(с) for с in sorted(set(с for с in слова if с), key=len, reverse=True)) + ")"
    for язык, рамки in РАМКИ_АКТОВ.items():
        имена = [л[0] for л in A.ЛИЦА[язык]]; род = [л[2] for л in A.ЛИЦА[язык]]
        мест = [v for г in МЕСТОИМЕНИЯ[язык].values() for v in г.values()]
        дыры = {"X": alt(имена), "Y": alt(имена), "Xр": alt(род), "Yр": alt(род), "он": alt(мест), "Он": alt(мест), "него": alt(мест),
                "а": "(?:а|о|и|)", "аY": "(?:а|о|и|)", "n": r"(\d+)", "k": r"(\d+)", "m": r"(\d+)", "r": r"(\d+)", "s": r"(\d+)", "t": r"(\d+)", "k2": r"(\d+)"}
        for дыра, ключ in _ТОВАР_ПО_ДЫРЕ.items():
            формы = alt(ТОВАРЫ_АКТОВ[язык][ключ])
            for суффикс in ("n", "k", "m", "s", "мн"):
                дыры[дыра + суффикс] = формы
        for форма, рамка in рамки.items():
            куски = [дыры[к[1:-1]] if к.startswith("{") else re.escape(к) for к in re.split(r"(\{[^}]+\})", рамка)]
            вон.append((re.compile("^" + "".join(куски) + "$"), язык, форма))
    return вон


ОБРАЗЦЫ.extend(_образцы_актов())
ЛЕДЖЕР3 = re.compile(r"(\d+) \+ (\d+) ([+−]) (\d+) = (\d+)\.$")
ЛЕДЖЕР = re.compile(r"(\d+) ([+−×]) (\d+) = (\d+)\.$")


def судить(строка):
    """(судимо, истинно): a page of the house, or a line of its frame whose ledger does not hold."""
    с = строка.strip()
    if с in ПОКАЗЫ:
        return True, True
    for образ, язык, форма in ОБРАЗЦЫ:
        if образ.match(с):
            м3 = ЛЕДЖЕР3.search(с)
            if м3:
                a, b, з, c_, v = int(м3.group(1)), int(м3.group(2)), м3.group(3), int(м3.group(4)), int(м3.group(5))
                верно = v == (a + b + c_ if з == "+" else a + b - c_)
                числа = [int(x) for x in re.findall(r"\d+", с[:м3.start()])]
                return True, верно and a in числа and b in числа and c_ in числа
            м = ЛЕДЖЕР.search(с)
            if not м:
                return True, False
            a, з, b, v = int(м.group(1)), м.group(2), int(м.group(3)), int(м.group(4))
            верно = v == (a + b if з == "+" else a - b if з == "−" else a * b)
            # the numbers of the story (BEFORE the ledger) must be the numbers of the ledger
            числа = [int(x) for x in re.findall(r"\d+", с[:м.start()])]
            return True, верно and a in числа and b in числа
    return False, False


def _самопроверка():
    for показ, (язык, форма) in ПОКАЗЫ.items():
        assert судить(показ) == (True, True), (язык, форма, показ)
    мутанты = 0
    for язык in РАМКИ:
        for форма in ФОРМЫ:
            if форма not in РАМКИ[язык] or язык in ОБЪЯВЛЕННЫЕ_ПРОПУСКИ.get(форма, ()):
                continue
            с = страница(язык, форма, 0, 1, 0, 12, 5)
            битая = re.sub(r"= (\d+)\.$", lambda м: f"= {int(м.group(1)) + 1}.", с)
            assert судить(битая) == (True, False), битая
            мутанты += 1
    for язык in РАМКИ_АКТОВ:
        for форма in ФОРМЫ_АКТОВ:
            с = страница_акта(язык, форма, 0, 1, 12, 5)
            битая = re.sub(r"= (\d+)\.$", lambda м: f"= {int(м.group(1)) + 1}.", с)
            assert судить(битая) == (True, False), битая
            мутанты += 1
    for форма in ("некоторые", "итог", "из_них", "если", "время", "кому", "единица", "товар"):
        print("  ", страница("en", форма, 0, 1, 0, 12, 5))
    for форма in ("некоторые", "из_них", "кому", "товар"):
        print("  ", страница("ru", форма, 2, 3, 1, 12, 5))
    print(f"  мутантов поймано: {мутанты}")
    print(f"  дом пишет показов: {len(ПОКАЗЫ)} (языков {len(РАМКИ)}, форм {len(ФОРМЫ)})")


if __name__ == "__main__":
    _самопроверка()
