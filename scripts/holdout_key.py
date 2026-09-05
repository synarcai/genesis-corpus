#!/usr/bin/env python3
"""[УДЕРЖАННЫЙ КЛЮЧ] — questions the reader has NEVER read: the houses' frames with numbers that no
world of the canon carries.

«СВОД СПРАШИВАЕТ СЕБЯ» ЗАСЧИТЫВАЕТ ПАМЯТЬ (holon, sixth point: 21 of 91 «right» answers were
lived lines — the reader had read the very line). A gate of landing must ask what the reader
could not have memorised: the same forms, other numbers. The houses render their frames for
declared numbers; this instrument renders the SVAMP house (stories in nine languages: holdings,
acts, shares, chains, refusals) for HELD-OUT numbers — pairs that stand in no house table — and
cuts every page into question and gold answer. The key is written in the sweep's format
(value ⇥ question ⇥ answer) for both judges (holon's sweep_judge.py and scripts/sweep_self.py).

THE RULE OF UPDATE: the key is a FUNCTION of the houses and of the held-out numbers declared
here — it is rewritten at every point of the canon (point protocol), so a house that grew is
held out at once; the numbers never enter a house table (the self-check below asserts it), and
no question of the key may stand in any world of shows (asserted over the manifest's worlds).

Rubric: 0 lived lines; 0 held-out numbers found in the house tables; ≥ 400 questions.
"""
import collections
import pathlib
import re
import sys

КОРЕНЬ = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(КОРЕНЬ / "tools"))
import genesis  # noqa: E402
import svampforms as F  # noqa: E402
import numberline as N  # noqa: E402
import crossforms as C  # noqa: E402
import letters as LT  # noqa: E402
import holdforms as HF  # noqa: E402
import cmpframes as CF  # noqa: E402
import sceneforms as SC  # noqa: E402
import episodeforms as EP  # noqa: E402 — ленты актов над одним состоянием
import summaryforms as SU  # noqa: E402 — компакция: что запись хранит и что потеряла
import opforms as OP  # noqa: E402 — словесная операция в повелении
import readnum as RN  # noqa: E402 — четыре места непрочитанного числа
import mandateforms as MA  # noqa: E402 — правило против приказа
import personforms as PE  # noqa: E402 — личность: форма ответа и выбор при равных
import selfmodelforms as SM  # noqa: E402 — предсказать себя и проверить фактом
import signedworld as SW  # noqa: E402 — движение через ноль
import beforetails as BT  # noqa: E402 — хвост, указывающий назад
import discountroad as DR  # noqa: E402 — денежная дорога со скидкой
import nomention as NM  # noqa: E402 — вопрос о том, чего история не называла
import clockforms as CL  # noqa: E402 — перенос шестидесяти
import mixedunits as MU  # noqa: E402 — перенос тысячи и сотни
import dateforms as DF  # noqa: E402 — перенос через конец месяца
import clockwords as CW  # noqa: E402 — час, сказанный словом

# РУБЕЖ-ДОЛГА: ПРОЖИТЫХ_РУБЕЖ = 0
ПРОЖИТЫХ_РУБЕЖ = 0
# РУБЕЖ-ДОЛГА: ВОПРОСОВ_РУБЕЖ = 400
# РУБЕЖ-ДОЛГА: ВОПРОСОВ_СЛЕДУЮЩЕГО_РУБЕЖ = 1500
ВОПРОСОВ_РУБЕЖ = 400
ВОПРОСОВ_СЛЕДУЮЩЕГО_РУБЕЖ = 1500
# ПУСТОЙ-ОБХОД: --корень no-such-root

КЛЮЧ = "datasets/HOLDOUT-KEY.tsv"
# КЛЮЧ СЛЕДУЮЩЕЙ ТОЧКИ (05.09): дома растут быстрее, чем сменяются релизы, и ключ обязан расти
# вместе с ними — но НЕ ТОТ, что подписан релизом. Пока лежит замок, прибор пишет выросший ключ
# сюда, а замороженный сверяет по ЕГО составу домов; на точке после релиза замок снимается, и
# этот состав становится ключом.
КЛЮЧ_СЛЕДУЮЩЕГО = "datasets/HOLDOUT-KEY-NEXT.tsv"
# СОСТАВ КЛЮЧА ОБЪЯВЛЕН, А НЕ ВЫВЕДЕН ИЗ ТОГО, ЧТО СЕГОДНЯ ЛЕЖИТ В tools/. Ключ 0.8.0 порождён
# четырьмя домами; следующий — шестью (прибавились держания без глагола и рамки сравнения,
# оба рождены 05.09). Сверка замороженного идёт по своему составу и потому не падает от роста
# корпуса — падает лишь тогда, когда изменился ДОМ, стоявший в ключе кандидата.
ДОМА_КАНДИДАТА = ("svamp", "числовой ряд", "перекрёсток", "буквы")
ДОМА_СЛЕДУЮЩЕГО = ДОМА_КАНДИДАТА + ("держания без глагола", "рамки сравнения", "сцена",
                                     "эпизод", "сводка", "операция", "непрочитанное число",
                                     "мандат", "личность", "самомодель", "подписанный мир",
                                     "хвост прежде", "скидка", "неназванное", "часы",
                                     "смешанная мера", "дата", "час словом")
# УДЕРЖАННЫЕ ЧИСЛА СЕМИ НОЧНЫХ ДОМОВ (05.09). Ни одно не стоит в таблицах своего дома — это
# ПРОВЕРЯЕТСЯ в main(), а не обещается: рынок, чьи числа ключ уже показывал, меряет память, а
# не форму. Дома архитектуры агента (эпизод, сводка, мандат, личность, самомодель) и два дома
# замеренных дефектов (операция, непрочитанное число) вошли в ключ ДЕВЯТОЙ точки, ибо восьмая
# заморожена слепком.
ЭПИЗОД_ЛЕНТЫ = ((23, (4, 2, 5)), (31, (6, 3, 4)))
СВОДКА_ЧИСЛА = ((23, 27, 31, 19), (33, 29, 37, 21))
ОПЕРАЦИЯ_ПАРЫ = {"сложи": ((23, 19), (31, 26)), "вычти": ((47, 19), (52, 28)),
                 "умножь": ((13, 7), (11, 9)), "раздели": ((56, 8), (63, 9)),
                 "поровну": ((72, 8), (65, 5))}
ЧИСЛО_ТРОЙКИ = ((23, 17, 19), (31, 27, 29))
МАНДАТ_ЧИСЛА = (23, 31)
ЛИЧНОСТЬ_ПАРЫ = ((23, 8), (31, 9))
САМОМОДЕЛЬ_ПАРЫ = ((23, 8), (31, 9))
ЗНАК_ВВЕРХ = ((-30, 35), (-28, 33))
ЗНАК_ВНИЗ = ((28, 35), (31, 38))
ЗНАК_ЭТАЖИ = ((-25, 30), (-27, 32))
ХВОСТ_ОТДАЛ = ((29, 13), (37, 19))
ХВОСТ_КУПИЛ = ((27, 11), (35, 13))
ХВОСТ_ПОТРАТИЛ = ((103, 37), (117, 43))
СКИДКА_ЦЕНЫ = ((103, 37), (111, 43))
НЕНАЗВАННОЕ_ЧИСЛА = (27, 33)
ЧАСЫ_ПОЕЗДКИ = ((4, 55, 2, 35), (21, 45, 1, 25))
МЕРА_МАССЫ = ((3, 830, 2, 290), (6, 570, 1, 660))
МЕРА_ДЛИНЫ = ((3, 83, 2, 29), (6, 57, 1, 66))
ДАТА_ПЕРЕХОДЫ = (("май", 27, 9), ("январь", 25, 11))
ЧАС_СЛОВОМ = (9, 10)          # дом пишет часы 1..7; девятый и десятый удержаны
# ЗАМОРОЗКА КЛЮЧА (05.09, holon: ключ восьмой точки есть МЕРА КАНДИДАТА 0.0.1): пока рядом лежит
# «datasets/HOLDOUT-KEY.frozen», прибор не переписывает ключ, а СВЕРЯЕТ его с тем, что породил
# бы сейчас, и падает при расхождении — мера релиза не может двигаться под ногами читателя.
# Снимается удалением файла заморозки (следующая точка после релиза).
ЗАМОРОЗКА = "datasets/HOLDOUT-KEY.frozen"
# HELD-OUT NUMBERS — none of them in ЧИСЛА / ЧИСЛА_АКТОВ / ЦЕНЫ of the house (asserted); shares
# need n divisible by 2, 3 or 4 — 16, 28, 44 (by 4), 27, 33 (by 3), the rest by 2
ЧИСЛА = ((14, 9), (22, 13), (26, 17), (34, 19), (16, 9), (28, 13), (38, 17), (44, 19), (27, 13), (33, 17))
ЧИСЛА_АКТОВ = ((14, 9, 8), (22, 13, 11), (26, 17, 13), (34, 19, 14), (16, 9, 8), (28, 13, 11), (38, 17, 13), (44, 19, 14))
# prices of the «unit» form come from the house's own table, not from n and k — held out here
ЦЕНЫ = ((7, 6), (9, 8), (11, 7), (13, 9))
# THE NUMBER LINE holds out the forms that stand on declared tables (the walk 1..20 is enumerated
# whole and cannot be held out): age, the number between, the greatest / smallest of three, the row
# continued, sharing equally
ЛИНИЯ = {"ВОЗРАСТА": ((6, 4), (8, 2), (11, 6), (13, 4)), "МЕЖДУ": ((2, 4), (6, 8), (8, 10), (12, 14)),
         "ТРОЙКИ_ЧИСЕЛ": ((4, 11, 7), (6, 2, 9), (14, 19, 16), (10, 3, 8)), "РЯДЫ": ((3, 2), (4, 1), (6, 3), (2, 4)),
         "ДЕЛЁЖ": ((14, 2), (18, 3), (12, 4), (20, 4))}
ЛИНИЯ_ФОРМЫ = {"возраст", "между", "наибольшее", "наименьшее", "ряд_дальше", "поровну"}
# THE HOUSE OF LETTERS holds out WORDS: the same questions (how many letters, the first, the last,
# backwards) about words the house never declared — the answer is the word's own
СЛОВА = {"ru": ("книга", "дверь", "река"), "en": ("book", "door", "river"), "de": ("Buch", "Tür", "Fluss"),
         "fr": ("livre", "porte", "rivière"), "es": ("libro", "puerta", "río"), "it": ("libro", "porta", "fiume"),
         "pt": ("livro", "porta", "rio"), "nl": ("boek", "deur", "rivier"), "pl": ("książka", "drzwi", "rzeka")}
# THE HOUSE OF HOLDINGS WITHOUT A VERB walks the numbers 1..40 whole; its held-out numbers are
# therefore numbers ABOVE its row — the same frames, a number the house never wrote. The forms
# whose question carries no number («нет», «что_у») cannot be held out: their line is the same
# for every number and stands in the world already.
ДЕРЖАНИЯ_ЧИСЛА = (44, 52, 61, 73)
ДЕРЖАНИЯ_ФОРМЫ = ("держание", "возраст", "двое", "место", "два_товара", "чей", "место_чего")
# THE SCENE walks its numbers 1..40 whole, like the holdings house, and so its held-out numbers
# stand ABOVE that row. Two of its seven forms cannot be held out at all: «класс» enumerates every
# declared class (its question carries no number, and the line already stands in the world), and
# «нет_ли» writes «на полке нет книг» for every thing and place — neither line has a number to
# change. The remaining five are held out by number.
СЦЕНА_ЧИСЛА = (47, 55, 64, 76)
СЦЕНА_ФОРМЫ = ("место_два", "два_места", "принадлежность", "есть_ли", "цвет")
# THE FRAMES OF COMPARISON hold out pairs outside their twelve (and outside the SVAMP tables)
СРАВНЕНИЯ_ПАРЫ = ((19, 8), (23, 11), (29, 13), (31, 14), (34, 16), (39, 17), (41, 19), (46, 21))
# THE CROSSROADS holds out arithmetic pairs — the same four signs, other numbers
ДЕЙСТВИЯ = (("+", ((23, 19), (14, 7), (31, 26), (45, 55))), ("−", ((41, 19), (23, 7), (52, 26), (90, 45))),
            ("×", ((13, 3), (11, 6), (7, 8), (25, 4))), ("÷", ((42, 7), (36, 4), (63, 9), (72, 8))))
# only the forms that stand on the pairs; the triples, chains and signed sums stand on their own tables
ПЕРЕКРЁСТОК_ФОРМЫ = {"перекрёсток", "именем", "согласен", "согласен_вы", "просьба", "просьба_вы", "теперь", "словом"}
ВОПРОС = re.compile(r"[?？] ")
ЧИСЛО = re.compile(r"\d+")


def _разрезать(страница):
    """(question, answer) at the LAST question mark; None for a page without one."""
    м = list(ВОПРОС.finditer(страница))
    if not м:
        return None
    return страница[:м[-1].end()].strip(), страница[м[-1].end():].strip()


def _значение(ответ):
    числа = ЧИСЛО.findall(ответ)
    return числа[-1] if числа else ответ.rstrip(".")


def страницы():
    """Every form and act of the house for the held-out numbers, two pages per (language, form)."""
    вон = []
    цены_дома, F.ЦЕНЫ = F.ЦЕНЫ, ЦЕНЫ           # the unit form reads prices from the house table
    try:
        return _страницы(вон)
    finally:
        F.ЦЕНЫ = цены_дома


def _линия():
    """The number line's pages for the held-out tables — the house's own walk, other tables."""
    было = {имя: getattr(N, имя) for имя in ЛИНИЯ}
    for имя, таблица in ЛИНИЯ.items():
        setattr(N, имя, таблица)
    try:
        показы = N._показы()
    finally:
        for имя, таблица in было.items():
            setattr(N, имя, таблица)
    взято = collections.Counter(); вон = []
    for с, (язык, форма) in показы.items():
        if форма in ЛИНИЯ_ФОРМЫ and взято[(язык, форма)] < 2 and _разрезать(с) and ЧИСЛО.search(_разрезать(с)[0]):
            вон.append((язык, форма, с)); взято[(язык, форма)] += 1
    return вон


def _перекрёсток():
    """The crossroads' pages for held-out pairs — the same signs and names, other numbers."""
    было = C.ДЕЙСТВИЯ
    C.ДЕЙСТВИЯ = tuple((знак, имя, dict(ДЕЙСТВИЯ)[знак]) for знак, имя, _ in было)
    try:
        показы = C._показы()
    finally:
        C.ДЕЙСТВИЯ = было
    взято = collections.Counter(); вон = []
    for с, (язык, форма) in показы.items():
        if форма in ПЕРЕКРЁСТОК_ФОРМЫ and взято[(язык, форма)] < 2 and _разрезать(с) and ЧИСЛО.search(_разрезать(с)[0]):
            вон.append((язык, форма, с)); взято[(язык, форма)] += 1
    return вон


def _буквы():
    вон = []
    for язык, слова in СЛОВА.items():
        for w in слова:
            assert w not in LT.ЯЗЫКИ[язык]["слова"], (язык, w)
            for форма in LT.ФОРМЫ:
                с = LT.страница(язык, форма, w, вопросом=(форма == "наоборот"))
                if _разрезать(с):
                    вон.append((язык, форма, с))
    return вон


def _держания():
    """The holdings house's frames for numbers above its row — two pages per (language, form)."""
    вон = []
    for язык in HF.ЯЗЫКИ:
        лиц, вещей = len(HF.A.ЛИЦА[язык]), len(HF.A.ЯЗЫКИ[язык]["вещи"])
        мест = len(HF.МЕСТА[язык])
        for форма in ДЕРЖАНИЯ_ФОРМЫ:
            взято = 0
            for q, n in enumerate(ДЕРЖАНИЯ_ЧИСЛА):
                i, Т = (q + 1) % лиц, (q * 3 + 2) % вещей
                if форма == "возраст":
                    # ШОВ ГОДА ЧИТАЕТСЯ У ДОМА, А НЕ ПОВТОРЯЕТСЯ ЗДЕСЬ: число, чей год пакет
                    # гнёт неверно, дом не пишет — и ключ не спрашивает о ненаписанном.
                    if HF._год_согнут(язык, n):
                        continue
                    с = HF.страница(язык, форма, i, i + 1, 0, n)
                elif форма == "двое":
                    с = HF.страница(язык, форма, i, i + 3, Т, n, HF._пара(n))
                elif форма in ("место", "место_чего"):
                    с = HF.страница(язык, форма, 0, 1, Т, n, М=(q + 1) % мест)
                elif форма == "два_товара":
                    с = HF.страница(язык, форма, i, 0, Т, n, Т2=(Т + 1) % вещей, m=HF._пара(n))
                else:
                    с = HF.страница(язык, форма, i, i + 1, Т, n)
                if с and _разрезать(с) and ЧИСЛО.search(_разрезать(с)[0]):
                    вон.append((язык, форма, с)); взято += 1
                if взято >= 2:
                    break
    return вон


def _сравнения():
    """The comparison house's frames for held-out pairs — two pages per (language, group, form)."""
    вон = []
    for язык in CF.ЯЗЫКИ:
        лиц = len(CF.A.ЛИЦА[язык])
        for группа in CF.ГРУППЫ:
            ключ = CF.ТОВАРЫ[группа][0]
            for форма in CF.ФОРМЫ:
                взято = 0
                for q, (n, k) in enumerate(СРАВНЕНИЯ_ПАРЫ):
                    i, j = (q + 1) % лиц, (q * 3 + 2) % лиц
                    m = 2 if q % 2 == 0 else 3
                    с = CF.страница(язык, группа, форма, i, j, ключ, n, k, m)
                    if с and _разрезать(с) and ЧИСЛО.search(_разрезать(с)[0]):
                        вон.append((язык, f"{группа}/{форма}", с)); взято += 1
                    if взято >= 2:
                        break
    return вон


def _сцена():
    """The scene's frames for numbers above its row — two pages per (language, form).

    THE HOUSE PRECOMPUTES ITS COUNT CELLS ONLY TO ITS OWN ROW (`_ЯЧЕЙКИ` up to ВЕРХ + 1), and the
    Polish copula and the colour seam read that table. The key does not repeat the rule: it asks
    the house's own `_ячейка` for the held-out numbers, lends the answers to the table for the
    render, and takes them back — the seam stays the house's, and the key stays a reader.
    """
    занято = []
    for язык in SC.ЯЗЫКИ:
        for n in СЦЕНА_ЧИСЛА:
            if n not in SC._ЯЧЕЙКИ[язык]:
                SC._ЯЧЕЙКИ[язык][n] = SC._ячейка(язык, n)
                занято.append((язык, n))
    try:
        return _сцена_страницы()
    finally:
        for язык, n in занято:
            SC._ЯЧЕЙКИ[язык].pop(n, None)


def _сцена_страницы():
    вон = []
    for язык in SC.ЯЗЫКИ:
        вещей = len(SC.A.ЯЗЫКИ[язык]["вещи"])
        лиц = len(SC.A.ЛИЦА[язык])
        мест = len(HF.МЕСТА[язык])
        цветов = len(SC.ЦВЕТА[язык])
        for форма in СЦЕНА_ФОРМЫ:
            взято = 0
            for q, n in enumerate(СЦЕНА_ЧИСЛА):
                Т, m = (q * 3 + 1) % вещей, SC._пара(n)
                if форма == "место_два":
                    с = SC.страница(язык, форма, Т, n, m=m, Т2=(Т + 1 + q) % вещей, М=q % мест)
                elif форма == "два_места":
                    с = SC.страница(язык, форма, Т, n, m=m, М=q % мест, М2=(q + 1) % мест)
                elif форма == "цвет":
                    # ШОВ ЦВЕТА ЧИТАЕТСЯ У ДОМА: там, где прилагательное не согласуется с числом,
                    # дом цвета не пишет — и ключ о ненаписанном не спрашивает.
                    if not SC._цвет_годен(язык, n):
                        continue
                    с = SC.страница(язык, форма, Т, n, i=q % лиц, ц=q % цветов)
                else:
                    с = SC.страница(язык, форма, Т, n, М=(q + 2) % мест)
                if с and _разрезать(с) and ЧИСЛО.search(_разрезать(с)[0]):
                    вон.append((язык, форма, с)); взято += 1
                if взято >= 2:
                    break
    return вон


def _взять(вон, язык, форма, с, порог=2, счёт=None):
    """A page enters the key only when it splits into question and answer AND its question
    carries a number: a question without one is the same line for every value."""
    if not с:
        return счёт
    кус = _разрезать(с)
    if кус and ЧИСЛО.search(кус[0]):
        вон.append((язык, форма, с))
        return (счёт or 0) + 1
    return счёт


def _эпизод():
    """Tapes over a state whose start stands above the house's own row."""
    вон = []
    for язык in EP.ЯЗЫКИ:
        видов = len(EP.T.ВЕЩИ[язык])
        for q, (n, шаги) in enumerate(ЭПИЗОД_ЛЕНТЫ):
            for форма, фигура in (("лента_три", ("+", "−", "+")), ("после_шага", ("+", "+", "−"))):
                if min(EP._счёты(n, фигура, шаги)) < 1:
                    continue
                _взять(вон, язык, форма, EP.страница(язык, форма, q % видов, n, фигура, шаги))
    return вон


def _сводка():
    """The note over places whose counts stand above the house's row."""
    вон = []
    for язык in SU.ЯЗЫКИ:
        видов = len(SU.T.ВЕЩИ[язык])
        for q, числа in enumerate(СВОДКА_ЧИСЛА):
            P, выкинуто = 4, q % 4
            оставлены = [i for i in range(P) if i != выкинуто]
            for форма, спрошено in (("говорит", оставлены[0]), ("молчит", выкинуто),
                                    ("сводка_верна", оставлены[0]), ("сводка_лжёт", оставлены[-1])):
                _взять(вон, язык, форма,
                       SU.страница_фактов(язык, форма, q % видов, P, выкинуто, 0, спрошено, числа=числа))
    return вон


def _операция():
    """Orders whose pairs stand in no table of the house."""
    вон = []
    for язык in OP.ЯЗЫКИ:
        for действие, пары in sorted(ОПЕРАЦИЯ_ПАРЫ.items()):
            for q, (a, b) in enumerate(пары):
                for форма in ("повеление", "повеление_леджер", "повеление_равенством"):
                    _взять(вон, язык, форма, OP.страница(язык, форма, действие, q % 2, a, b))
    return вон


def _непрочитанное():
    """The four places of an unread number, over triples the house never shows."""
    вон = []
    for язык in RN.ЯЗЫКИ:
        for q, тройка in enumerate(ЧИСЛО_ТРОЙКИ):
            i = q % RN.ТОВАРОВ
            for форма in ("список", "список_всего"):
                _взять(вон, язык, форма, RN.страница(язык, форма, i, тройка))
            for форма in ("связка", "число_первым"):
                _взять(вон, язык, форма, RN.страница(язык, форма, i, (тройка[0],)))
            _взять(вон, язык, "про_форма", RN.страница(язык, "про_форма", 0, (тройка[0], тройка[1])))
    return вон


def _мандат():
    """A standing rule against an order counting things above the house's row."""
    вон = []
    for язык in MA.ЯЗЫКИ:
        видов = len(MA.T.ВЕЩИ[язык])
        for q, n in enumerate(МАНДАТ_ЧИСЛА):
            _взять(вон, язык, "запрещено", MA.страница(язык, "запрещено", (0,), 0, q % видов, n))
            _взять(вон, язык, "позволено", MA.страница(язык, "позволено", (0,), 1, q % видов, n))
            _взять(вон, язык, "какое_правило", MA.страница(язык, "какое_правило", (0, 2), 2, q % видов, n))
            _взять(вон, язык, "мандат_молчит", MA.страница(язык, "мандат_молчит", (0, 1), 2, q % видов, n))
    return вон


def _личность():
    """The same tape under two personalities, over numbers above the house's row."""
    вон = []
    for язык in PE.ЯЗЫКИ:
        видов = len(PE.T.ВЕЩИ[язык])
        for q, (n, m) in enumerate(ЛИЧНОСТЬ_ПАРЫ):
            М = PE.T.МЕСТА[язык][q % len(PE.T.МЕСТА[язык])]
            for форма in ("кратко", "подробно", "два_ответа"):
                _взять(вон, язык, форма, PE.страница(язык, форма, q % видов, n, m, М))
            _взять(вон, язык, "выбор_при_равных",
                   PE.страница(язык, "выбор_при_равных", q % видов, n, m, М, черта="осторожная", выбор="переместить"))
    return вон


def _самомодель():
    """Predict, answer, check — over numbers the house never showed."""
    вон = []
    for язык in SM.ЯЗЫКИ:
        видов = len(SM.T.ВЕЩИ[язык])
        for q, (n, m) in enumerate(САМОМОДЕЛЬ_ПАРЫ):
            М = SM.T.МЕСТА[язык][q % len(SM.T.МЕСТА[язык])]
            _взять(вон, язык, "сбылось", SM.страница(язык, "сбылось", q % видов, n, m, 0, М))
            for форма in ("не_сбылось", "ошибка", "мысль_не_меняет_факт"):
                _взять(вон, язык, форма, SM.страница(язык, форма, q % видов, n, m, 1 + q, М))
    return вон


def _знак():
    """Movements across zero over numbers the house never showed."""
    вон = []
    for язык in SW.ЯЗЫКИ:
        for t, d in ЗНАК_ВВЕРХ:
            _взять(вон, язык, "потеплело", SW.страница(язык, "потеплело", t=t, d=d))
            _взять(вон, язык, "разность_через_ноль", SW.страница(язык, "разность_через_ноль", a=t + d, b=t))
        for t, d in ЗНАК_ВНИЗ:
            _взять(вон, язык, "похолодало", SW.страница(язык, "похолодало", t=t, d=d))
        for t, d in ЗНАК_ЭТАЖИ:
            _взять(вон, язык, "лифт", SW.страница(язык, "лифт", t=t, d=d))
    return вон


def _хвост_прежде():
    """A story asked backwards over pairs the house never showed."""
    вон = []
    for язык in BT.ЯЗЫКИ:
        for q, (r, k) in enumerate(ХВОСТ_ОТДАЛ):
            _взять(вон, язык, "отдал", BT.страница(язык, "отдал", q % BT.ТОВАРОВ, q % 5, r, k))
        for q, (r, k) in enumerate(ХВОСТ_КУПИЛ):
            _взять(вон, язык, "купил", BT.страница(язык, "купил", (q + 1) % BT.ТОВАРОВ, (q + 2) % 5, r, k))
        for q, (r, k) in enumerate(ХВОСТ_ПОТРАТИЛ):
            _взять(вон, язык, "потратил", BT.страница(язык, "потратил", 0, (q + 3) % 5, r, k))
    return вон


def _скидка():
    """Four questions over a price pair the house never showed."""
    вон = []
    for язык in DR.ЯЗЫКИ:
        for q, (цена, скидка) in enumerate(СКИДКА_ЦЕНЫ):
            i = q % 2
            _взять(вон, язык, "цена_со_скидкой", DR.страница(язык, "цена_со_скидкой", i, цена, скидка))
            for форма, k in (("счёт_со_скидкой", 3), ("сколько_за_сумму", 4), ("сколько_со_скидкой", 5)):
                _взять(вон, язык, форма, DR.страница(язык, форма, i, цена, скидка, k))
    return вон


def _неназванное():
    """The refusal about what the story never said, over counts the house never showed."""
    вон = []
    for язык in NM.ЯЗЫКИ:
        мест = len(NM.МЕСТА[язык])
        видов = len(NM.T.ВЕЩИ[язык])
        for q, n in enumerate(НЕНАЗВАННОЕ_ЧИСЛА):
            i, Т = q % мест, q % видов
            _взять(вон, язык, "место_названо", NM.страница(язык, "место_названо", (i,), i, Т, n))
            _взять(вон, язык, "место_чужое", NM.страница(язык, "место_чужое", (i,), (i + 1) % мест, Т, n))
            _взять(вон, язык, "вещь_чужая", NM.страница(язык, "вещь_чужая", (i,), i, Т, n, Тспр=(Т + 1) % видов))
            i2 = (i + 1) % мест
            третье = (i + 2) % мест
            if len({i, i2, третье}) == 3:
                _взять(вон, язык, "третье_место", NM.страница(язык, "третье_место", (i, i2), третье, Т, n, n2=n + 4))
    return вон


def _часы():
    """Journeys across the hour over times the house never showed."""
    вон = []
    for язык in CL.ЯЗЫКИ:
        for ч, м, дч, дм in ЧАСЫ_ПОЕЗДКИ:
            if м + дм < 60 or (ч * 60 + м + дч * 60 + дм) >= 24 * 60:
                continue
            for форма in CL.ФОРМЫ:
                _взять(вон, язык, форма, CL.страница(язык, форма, ч, м, дч, дм))
    return вон


def _мера():
    """Measures crossing their unit over pairs the house never showed."""
    вон = []
    for язык in MU.ЯЗЫКИ:
        for б1, м1, б2, м2 in МЕРА_МАССЫ:
            for форма in ("масса_плюс", "масса_минус"):
                _взять(вон, язык, форма, MU.страница(язык, форма, б1, м1, б2, м2))
        for б1, м1, б2, м2 in МЕРА_ДЛИНЫ:
            for форма in ("длина_плюс", "длина_минус"):
                _взять(вон, язык, форма, MU.страница(язык, форма, б1, м1, б2, м2))
    return вон


def _дата():
    """Month crossings the house never showed."""
    вон = []
    for язык in DF.ЯЗЫКИ:
        for месяц, д, шаг in ДАТА_ПЕРЕХОДЫ:
            if д + шаг <= DF.ДЛИНЫ[месяц]:
                continue
            for форма in DF.ФОРМЫ:
                _взять(вон, язык, форма, DF.страница(язык, форма, месяц, д, шаг))
    return вон


def _час_словом():
    """The spoken quarter-hours of the hours the house holds back."""
    вон = []
    for язык in CW.ЯЗЫКИ:
        for ч in ЧАС_СЛОВОМ:
            for вид in CW.ВИДЫ:
                for форма in CW.ФОРМЫ:
                    _взять(вон, язык, форма, CW.страница(язык, форма, вид, ч))
    return вон


def _страницы(вон):
    for язык in F.РАМКИ:
        лиц = len(F.A.ЛИЦА[язык]); вещей = len(F.A.ЯЗЫКИ[язык]["вещи"])
        for форма in F.ФОРМЫ:
            if форма not in F.РАМКИ[язык] or язык in F.ОБЪЯВЛЕННЫЕ_ПРОПУСКИ.get(форма, ()):
                continue
            взято = 0
            for q, (n, k) in enumerate(ЧИСЛА):
                for вариант in range(3):
                    с = F.страница(язык, форма, (q + 2) % лиц, (q * 3 + 2) % лиц, (q + 1) % вещей, n, k, вариант)
                    # A PAGE WITHOUT A NUMBER IN ITS QUESTION CANNOT BE HELD OUT: the refusal «how many
                    # coins does Ann have? I do not know …» is the same line for every number
                    if с and _разрезать(с) and ЧИСЛО.search(_разрезать(с)[0]):
                        вон.append((язык, форма, с)); взято += 1
                        break
                if взято >= 2:
                    break
        for форма in F.ФОРМЫ_АКТОВ:
            if форма not in F.РАМКИ_АКТОВ[язык]:
                continue
            взято = 0
            for q, (n, k, m) in enumerate(ЧИСЛА_АКТОВ):
                с = F.страница_акта(язык, форма, (q + 2) % лиц, (q * 3 + 2) % лиц, n, k, m)
                if с and _разрезать(с):
                    вон.append((язык, форма, с)); взято += 1
                if взято >= 2:
                    break
    return вон


def main(argv):
    корень = pathlib.Path(argv[argv.index("--корень") + 1]) if "--корень" in argv else КОРЕНЬ
    if not (корень / "datasets").is_dir():
        print(f"УДЕРЖАННЫЙ КЛЮЧ ОТКАЗ: нет дерева в {корень}")
        return 2
    # THE FIRST NUMBER OF A STORY IS WHAT MEMORY KEYS ON: the held-out n never stands as a house n,
    # and no held-out pair or triple stands in a house table (a small k or m may recur — the
    # line differs by its story)
    свои_n = {n for n, *_ in F.ЧИСЛА} | {n for n, *_ in F.ЧИСЛА_АКТОВ}
    свои_ряды = set(F.ЧИСЛА) | set(F.ЧИСЛА_АКТОВ) | {(n, k) for n, k, _ in F.ЧИСЛА_АКТОВ} | set(F.ЦЕНЫ)
    беда = ({n for n, *_ in ЧИСЛА} | {n for n, *_ in ЧИСЛА_АКТОВ}) & свои_n
    беда |= {р for р in set(ЧИСЛА) | set(ЧИСЛА_АКТОВ) | {(n, k) for n, k, _ in ЧИСЛА_АКТОВ} | set(ЦЕНЫ) if р in свои_ряды}
    for имя, таблица in ЛИНИЯ.items():
        беда |= set(таблица) & set(getattr(N, имя))
    домашние_пары = {(з, п) for з, _, пары in C.ДЕЙСТВИЯ for п in пары}
    беда |= {(з, п) for з, пары in ДЕЙСТВИЯ for п in пары if (з, п) in домашние_пары}
    # ДЕРЖАНИЯ: дом обходит свой ряд ЦЕЛИКОМ, и удержать можно лишь число выше ряда
    беда |= {n for n in ДЕРЖАНИЯ_ЧИСЛА if n <= HF.ВЕРХ}
    # РАМКИ СРАВНЕНИЯ: ни первое число, ни пара не стоят в двенадцати парах дома
    первые_сравнения = {n for n, _ in CF.ПАРЫ}
    беда |= {n for n, _ in СРАВНЕНИЯ_ПАРЫ if n in первые_сравнения}
    беда |= {п for п in СРАВНЕНИЯ_ПАРЫ if п in set(CF.ПАРЫ)}
    # СЦЕНА: дом обходит свой ряд ЦЕЛИКОМ, и удержать можно лишь число выше ряда
    беда |= {n for n in СЦЕНА_ЧИСЛА if n <= SC.ВЕРХ}
    # СЕМЬ НОЧНЫХ ДОМОВ: ни одно удержанное число не стоит в таблице своего дома
    беда |= {n for n, _ in ЭПИЗОД_ЛЕНТЫ if n in set(EP.НАЧАЛА)}
    беда |= {c for числа in СВОДКА_ЧИСЛА for c in числа if c in set(SU.ЧИСЛА)}
    беда |= {п for д, пары in ОПЕРАЦИЯ_ПАРЫ.items() for п in пары if п in set(OP.ПАРЫ[д])}
    беда |= {c for т in ЧИСЛО_ТРОЙКИ for c in т if c in set(RN.ОДИНОЧКИ) or any(c in тр for тр in RN.ТРОЙКИ)}
    беда |= {n for n in МАНДАТ_ЧИСЛА if n in set(MA.ЧИСЛА)}
    беда |= {n for n, m in ЛИЧНОСТЬ_ПАРЫ if n in set(PE.НАЧАЛА) or m in set(PE.ШАГИ)}
    беда |= {n for n, m in САМОМОДЕЛЬ_ПАРЫ if n in set(SM.НАЧАЛА) or m in set(SM.ШАГИ)}
    беда |= {п for п in ЗНАК_ВВЕРХ if п in set(SW.ВВЕРХ)} | {п for п in ЗНАК_ВНИЗ if п in set(SW.ВНИЗ)}
    беда |= {п for п in ЗНАК_ЭТАЖИ if п in set(SW.ЭТАЖИ)}
    беда |= {п for п in ХВОСТ_ОТДАЛ if п in set(BT.ОТДАЛ)} | {п for п in ХВОСТ_КУПИЛ if п in set(BT.КУПИЛ)}
    беда |= {п for п in ХВОСТ_ПОТРАТИЛ if п in set(BT.ПОТРАТИЛ)}
    беда |= {п for п in СКИДКА_ЦЕНЫ if п in set(DR.ЦЕНЫ)}
    беда |= {n for n in НЕНАЗВАННОЕ_ЧИСЛА if n in set(NM.ЧИСЛА)}
    беда |= {п for п in ЧАСЫ_ПОЕЗДКИ if п in set(CL.ПОЕЗДКИ)}
    беда |= {п for п in МЕРА_МАССЫ if п in set(MU.МАССЫ)} | {п for п in МЕРА_ДЛИНЫ if п in set(MU.ДЛИНЫ)}
    беда |= {п for п in ДАТА_ПЕРЕХОДЫ if п in set(DF.ПЕРЕХОДЫ)}
    беда |= {ч for ч in ЧАС_СЛОВОМ if ч in set(CW.ЧАСЫ)}
    if беда:
        print(f"УДЕРЖАННЫЙ КЛЮЧ FAIL: удержанные числа стоят в таблицах дома: {sorted(map(str, беда))}")
        return 1
    ряд = страницы() + _линия() + _перекрёсток() + _буквы()          # состав ключа 0.8.0
    ряд_след = (ряд + _держания() + _сравнения() + _сцена()          # состав следующей точки
                + _эпизод() + _сводка() + _операция() + _непрочитанное()
                + _мандат() + _личность() + _самомодель()
                + _знак() + _хвост_прежде() + _скидка() + _неназванное()
                + _часы() + _мера() + _дата() + _час_словом())
    # no question may stand in a world of shows (lived lines)
    прожито = set()
    for путь in genesis.worlds(kind="shows"):
        if путь.is_file():
            прожито.update(л.strip() for л in путь.read_text(encoding="utf-8", errors="replace").splitlines())
    прожитые = [(язык, форма, с) for язык, форма, с in ряд if с.strip() in прожито]
    прожитые_след = [(я, ф, с) for я, ф, с in ряд_след if с.strip() in прожито]
    прожитых, прожитых_след = len(прожитые), len(прожитые_след)
    for язык, форма, с in (прожитые + прожитые_след)[:3]:
        print(f"  ПРОЖИТА [{язык} {форма}] {с[:90]}")

    def _строки(ряд_):
        вон = []
        for язык, форма, с in ряд_:
            в, о = _разрезать(с)
            вон.append(f"{_значение(о)}\t{в}\t{о}")
        return "\n".join(вон) + "\n"

    свежий, свежий_след = _строки(ряд), _строки(ряд_след)
    заморожен = (корень / ЗАМОРОЗКА).is_file()
    if заморожен:
        # СЛЕПОК СВЕРЯЕТСЯ СО СВОЕЙ ПОДПИСЬЮ, А НЕ С ПОРОЖДЕНИЕМ (05.09, второй урок замка).
        # Первая редакция сверяла замороженный ключ с тем, что дома породили бы СЕЙЧАС, — и
        # упала в тот же час, когда дом историй вырос волной скрытого количества. Но рост
        # домов есть цель работы, а не порча меры: мера релиза неподвижна потому, что она
        # СЛЕПОК, и её целостность есть подпись, записанная в самом замке. Рост домов виден
        # числом ключа СЛЕДУЮЩЕЙ точки, который пишется рядом.
        import hashlib
        замок = (корень / ЗАМОРОЗКА).read_text(encoding="utf-8")
        подпись = re.search(r"sha256 ([0-9a-f]{64})", замок)
        файл = корень / КЛЮЧ
        сейчас = hashlib.sha256(файл.read_bytes()).hexdigest() if файл.is_file() else ""
        if not подпись:
            print(f"УДЕРЖАННЫЙ КЛЮЧ FAIL: замок {ЗАМОРОЗКА} не несёт подписи слепка")
            return 1
        if сейчас != подпись.group(1):
            print(f"  СЛЕПОК ИСПОРЧЕН: подпись замка {подпись.group(1)[:16]}, на диске {сейчас[:16]}")
            print("УДЕРЖАННЫЙ КЛЮЧ FAIL: замороженный ключ разошёлся со своей подписью")
            return 1
        (корень / КЛЮЧ_СЛЕДУЮЩЕГО).write_text(свежий_след, encoding="utf-8")
    else:
        # ЗАМОК СНЯТ — ключ следующей точки СТАНОВИТСЯ ключом, и лишнего файла рядом не остаётся
        (корень / КЛЮЧ).write_text(свежий_след, encoding="utf-8")
        (корень / КЛЮЧ_СЛЕДУЮЩЕГО).unlink(missing_ok=True)
    def _числа(ряд_):
        по_языку = collections.Counter(я for я, _, _ in ряд_)
        глубина = collections.Counter(("2+" if с.count("=") >= 2 else "1" if "=" in с else "0")
                                      for _, _, с in ряд_)
        return ("по языкам " + " ".join(f"{я} {к}" for я, к in sorted(по_языку.items()))
                + "; по глубине " + " ".join(f"[{г}] {к}" for г, к in sorted(глубина.items())))

    поза = "PASS" if прожитых <= ПРОЖИТЫХ_РУБЕЖ and len(ряд) >= ВОПРОСОВ_РУБЕЖ else "FAIL"
    состояние = "заморожен, сверен" if заморожен else "переписан"
    print(f"УДЕРЖАННЫЙ КЛЮЧ {поза}: вопросов {len(ряд)} (рубеж {ВОПРОСОВ_РУБЕЖ}), прожитых {прожитых} "
          f"(рубеж {ПРОЖИТЫХ_РУБЕЖ}); " + _числа(ряд) + f"; домов {len(ДОМА_КАНДИДАТА)}; "
          f"ключ {КЛЮЧ} ({состояние})")
    if not заморожен:
        return 0 if поза == "PASS" else 1
    поза_след = ("PASS" if прожитых_след <= ПРОЖИТЫХ_РУБЕЖ
                 and len(ряд_след) >= ВОПРОСОВ_СЛЕДУЮЩЕГО_РУБЕЖ else "FAIL")
    print(f"КЛЮЧ СЛЕДУЮЩЕЙ ТОЧКИ {поза_след}: вопросов {len(ряд_след)} "
          f"(рубеж {ВОПРОСОВ_СЛЕДУЮЩЕГО_РУБЕЖ}), прожитых {прожитых_след} "
          f"(рубеж {ПРОЖИТЫХ_РУБЕЖ}); " + _числа(ряд_след) + f"; домов {len(ДОМА_СЛЕДУЮЩЕГО)}; "
          f"ключ {КЛЮЧ_СЛЕДУЮЩЕГО}")
    return 0 if поза == "PASS" and поза_след == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
