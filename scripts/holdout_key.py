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
ДОМА_СЛЕДУЮЩЕГО = ДОМА_КАНДИДАТА + ("держания без глагола", "рамки сравнения", "сцена")
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
    if беда:
        print(f"УДЕРЖАННЫЙ КЛЮЧ FAIL: удержанные числа стоят в таблицах дома: {sorted(map(str, беда))}")
        return 1
    ряд = страницы() + _линия() + _перекрёсток() + _буквы()          # состав ключа 0.8.0
    ряд_след = ряд + _держания() + _сравнения() + _сцена()           # состав следующей точки
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
        было = (корень / КЛЮЧ).read_text(encoding="utf-8") if (корень / КЛЮЧ).is_file() else ""
        if было != свежий:
            разных = sum(1 for a, b in zip(было.splitlines(), свежий.splitlines()) if a != b)
            print(f"  ЗАМОРОЗКА: ключ на диске разошёлся с порождаемым ({len(было.splitlines())} "
                  f"против {len(ряд)} строк, различны {разных}) — изменился дом ключа релиза "
                  f"({', '.join(ДОМА_КАНДИДАТА)})")
            print(f"УДЕРЖАННЫЙ КЛЮЧ FAIL: ключ заморожен ({ЗАМОРОЗКА}), но разошёлся с домами")
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
