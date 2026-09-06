#!/usr/bin/env python3
"""THE HOUSE OF THE NUMBER'S PHRASE — the number that hangs on a form, not on a digit (06.09).

The measure of the executor (d5, band p156) named the debt exactly: of 423 tacts where the reader
does not read a number, 409 carry PLAIN DIGITS — the trouble is not the shape of the number but
the shape of the PHRASE it hangs on. The lines it stumbles on are «the first chapter is 48 pages
long», «41 children were riding», «36 more push-ups but 33 fewer crunches». The census of the свод
says why: eight lines carry «N pages long», six carry a progressive with a counted subject, and
ZERO carry «N more … but N fewer».

FOUR FRAMES, EACH A DIFFERENT WAY FOR A NUMBER TO SIT IN A SENTENCE:
  обладание      — the measure as what the text HAS: «the first chapter has 48 pages», «в первой
                   главе 48 страниц» (Russian has no verb here at all — the number stands in a
                   locative phrase with no predicate to lean on);
  длина          — the SAME FACT as a PREDICATE OF LENGTH: the chapter IS forty-eight pages long.
                   BOTH forms are shown in ALL NINE languages, because a house that gives a language
                   one of them sells the market that one: a reader that has met the number only
                   beside «has» will not know it beside «is … long». The languages part company on
                   HOW the predicate is built — a verb of its own (ru, en, de, fr, it, nl: «ist 48
                   Seiten lang», «est long de 48 pages») or a tail on the verb of possession (es,
                   pt, pl: «tiene 48 páginas de largo», «ma 48 stron długości») — and that parting
                   is itself a shown fact, not a smoothing;
  прогрессив     — the counted subject with a verb, where the NUMBER DECIDES THE VERB'S FORM:
                   Russian says «41 ребёнок катался» in the singular and «35 детей каталось» in
                   the neuter, Polish keeps the neuter for both, the rest keep the plural. A reader
                   that has met the number only beside a noun has never seen it govern a verb.
                   THE BOUNDARY IS NOT THE LAST DIGIT: eleven ends in one and takes the plural
                   («11 детей каталось»), twenty-one does not («21 ребёнок катался»). Both sides
                   are shown, because a rule shown on one side only is indistinguishable from the
                   rule of the last digit, and the reader would buy the counterfeit. The form is
                   asked of the LANGUAGE PACK — the same cell that decides the noun's count form —
                   so the verb and the noun cannot disagree;
  двойное        — two comparisons of OPPOSITE direction in one sentence («8 книг больше, но
                   5 карандашей меньше»): the second number must not be dragged in the direction
                   of the first, and the ledger names both moves.

Each of the four frames carries its OWN question, so the pair «question? answer.» is never one
question wearing four bodies: «how many pages does the chapter have?» is not «how long is it?».
Each page ends with a question about ONE of its numbers and the number as the answer — the debt
the measure named is exactly this: a number that no question reaches.

WHAT IS BORROWED: the goods of the house of price and the counting rule of the packs. Declared
here: the chapter and the page, the child and the verb of riding, and the two comparison frames.

WHAT IS NOT MEASURED, NAMED: the number inside a name («Chapter 5» as a title) and the number as
a year.

THE VERB IS JUDGED ONLY WHERE IT MOVES. Of the nine languages exactly one moves its verb with the
number — Russian; Polish keeps the neuter for both and the other seven the plural. The pattern
therefore carries the singular/plural mark ONLY for a moving language (`ДВИЖУЩИЕ`, declared by the
difference of the speech itself, not by a list in the engine). A court that marked all nine would
call an honest English page a lie («52 children were riding») and would catch its own mutants FOR
FREE — by the number rather than by the damage — which is exactly the catch scripts/court_mutants.py
hunts for.
"""
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import asking  # noqa: E402 — the house of the pair declares which openers a question may wear
import priceforms as P  # noqa: E402 — the goods and the pack's counting rule
import svampforms as S  # noqa: E402 — the count cell of a pack

ЯЗЫКИ = ("ru", "en", "de", "fr", "es", "it", "pt", "nl", "pl")
СТРАНИЦА = {"ru": ("страница", "страницы", "страниц"), "en": ("page", "pages"),
            "de": ("Seite", "Seiten"), "fr": ("page", "pages"), "es": ("página", "páginas"),
            "it": ("pagina", "pagine"), "pt": ("página", "páginas"), "nl": ("bladzijde", "bladzijden"),
            "pl": ("strona", "strony", "stron")}
РЕБЁНОК = {"ru": ("ребёнок", "ребёнка", "детей"), "en": ("child", "children"),
           "de": ("Kind", "Kinder"), "fr": ("enfant", "enfants"), "es": ("niño", "niños"),
           "it": ("bambino", "bambini"), "pt": ("criança", "crianças"), "nl": ("kind", "kinderen"),
           "pl": ("dziecko", "dzieci", "dzieci")}
# ЧИСЛА ДЛИНЫ и ЧИСЛА ДЕТЕЙ. У последних два рода, и граница между ними НЕ ЕСТЬ ПОСЛЕДНЯЯ ЦИФРА:
# русский глагол встаёт в единственное ровно там, где языковой пакет даёт счётную ячейку «one»
# (1, 21, 31, 41, 101), и НЕ ВСТАЁТ при 11 и 111 — они кончаются на один и берут множественное
# («11 детей каталось»). Обе стороны показаны, иначе правило неотличимо от правила последней
# цифры, и читатель купит подделку вместо закона.
ДЛИНЫ = (48, 96, 124, 37, 60, 215)
ДЕТИ_ОДИН = (21, 41, 31, 101)
ДЕТИ_МНОГО = (29, 35, 42, 11, 111)
# ДВОЙНОЕ СРАВНЕНИЕ: (больше, меньше) — числа разные, чтобы второе не тянулось за первым
ПАРЫ_ДВОЙНОГО = ((8, 5), (12, 7), (15, 9), (6, 4))
# ДВЕ ФОРМЫ ДЛИНЫ, А НЕ ОДНА (просьба holon 06.09): один и тот же факт о главе сказан
# ОБЛАДАНИЕМ («в первой главе 48 страниц», «the first chapter has 48 pages») и ПРЕДИКАТОМ
# ДЛИНЫ («первая глава — 48 страниц длиной», «the first chapter is 48 pages long»), и обе на
# всех девяти языках. Дом, дающий языку одну форму, продаёт рынку ту одну: читатель выучит,
# что число живёт при «has», и не узнает его при «is … long». Языки расходятся в том, ОТДЕЛЬНЫЙ
# ли у предиката глагол (ru, en, de, fr, it, nl) или хвост при глаголе обладания (es, pt, pl), —
# и это расхождение само есть показанный факт.
ФОРМЫ = ("обладание", "длина", "прогрессив", "двойное")
ФОРМЫ_ДЛИНЫ = ("обладание", "длина")
РЕЧЬ = {
    "ru": dict(глава="первая глава", обладание="в первой главе {N}", вопрос_обладания="сколько страниц в первой главе?",
               длина="{Г} — {N} длиной", вопрос_длины="какой длины первая глава?",
               катались_один="{N} катался на карусели", катались_много="{N} каталось на карусели",
               вопрос_детей="сколько детей каталось на карусели?",
               двойное="у Ани на {A} больше, но на {B} меньше",
               вопрос_двойного="на сколько книг больше?"),
    "en": dict(глава="the first chapter", обладание="{Г} has {N}", вопрос_обладания="how many pages does the first chapter have?",
               длина="{Г} is {N} long", вопрос_длины="how long is the first chapter?",
               катались_один="{N} were riding the carousel", катались_много="{N} were riding the carousel",
               вопрос_детей="how many children were riding the carousel?",
               двойное="ann has {A} more but {B} fewer",
               вопрос_двойного="how many more books?"),
    "de": dict(глава="das erste Kapitel", обладание="{Г} hat {N}", вопрос_обладания="wie viele Seiten hat das erste Kapitel?",
               длина="{Г} ist {N} lang", вопрос_длины="wie lang ist das erste Kapitel?",
               катались_один="{N} fuhren Karussell", катались_много="{N} fuhren Karussell",
               вопрос_детей="wie viele Kinder fuhren Karussell?",
               двойное="Anna hat {A} mehr, aber {B} weniger",
               вопрос_двойного="wie viele Bücher mehr?"),
    "fr": dict(глава="le premier chapitre", обладание="{Г} fait {N}", вопрос_обладания="combien de pages fait le premier chapitre ?",
               длина="{Г} est long de {N}", вопрос_длины="quelle est la longueur du premier chapitre ?",
               катались_один="{N} faisaient du manège", катались_много="{N} faisaient du manège",
               вопрос_детей="combien d'enfants faisaient du manège ?",
               двойное="anne a {A} de plus, mais {B} de moins",
               вопрос_двойного="combien de livres en plus ?"),
    "es": dict(глава="el primer capítulo", обладание="{Г} tiene {N}", вопрос_обладания="¿cuántas páginas tiene el primer capítulo?",
               длина="{Г} tiene {N} de largo", вопрос_длины="¿qué longitud tiene el primer capítulo?",
               катались_один="{N} montaban en el tiovivo", катались_много="{N} montaban en el tiovivo",
               вопрос_детей="¿cuántos niños montaban en el tiovivo?",
               двойное="ana tiene {A} más, pero {B} menos",
               вопрос_двойного="¿cuántos libros más?"),
    "it": dict(глава="il primo capitolo", обладание="{Г} ha {N}", вопрос_обладания="quante pagine ha il primo capitolo?",
               длина="{Г} è lungo {N}", вопрос_длины="quanto è lungo il primo capitolo?",
               катались_один="{N} andavano sulla giostra", катались_много="{N} andavano sulla giostra",
               вопрос_детей="quanti bambini andavano sulla giostra?",
               двойное="anna ha {A} in più, ma {B} in meno",
               вопрос_двойного="quanti libri in più?"),
    "pt": dict(глава="o primeiro capítulo", обладание="{Г} tem {N}", вопрос_обладания="quantas páginas tem o primeiro capítulo?",
               длина="{Г} tem {N} de comprimento", вопрос_длины="qual é o comprimento do primeiro capítulo?",
               катались_один="{N} andavam no carrossel", катались_много="{N} andavam no carrossel",
               вопрос_детей="quantas crianças andavam no carrossel?",
               двойное="ana tem {A} a mais, mas {B} a menos",
               вопрос_двойного="quantos livros a mais?"),
    "nl": dict(глава="het eerste hoofdstuk", обладание="{Г} heeft {N}", вопрос_обладания="hoeveel bladzijden heeft het eerste hoofdstuk?",
               длина="{Г} is {N} lang", вопрос_длины="hoe lang is het eerste hoofdstuk?",
               катались_один="{N} reden op de draaimolen", катались_много="{N} reden op de draaimolen",
               вопрос_детей="hoeveel kinderen reden op de draaimolen?",
               двойное="anna heeft {A} meer, maar {B} minder",
               вопрос_двойного="hoeveel boeken meer?"),
    "pl": dict(глава="pierwszy rozdział", обладание="{Г} ma {N}", вопрос_обладания="ile stron ma pierwszy rozdział?",
               длина="{Г} ma {N} długości", вопрос_длины="jakiej długości jest pierwszy rozdział?",
               катались_один="{N} jeździło na karuzeli", катались_много="{N} jeździło na karuzeli",
               вопрос_детей="ile dzieci jeździło na karuzeli?",
               двойное="anna ma {A} więcej, ale {B} mniej",
               вопрос_двойного="ile książek więcej?"),
}


# ЯЗЫКИ, ГДЕ ЧИСЛО ДВИГАЕТ ГЛАГОЛ: объявлены РАЗЛИЧИЕМ двух рамок самой речи, а не списком в
# движке — язык, чей глагол не движется, несёт одну рамку, и признак «единственное» ему не
# приписывается вовсе. Иначе суд отверг бы честную английскую страницу с числом не на один
# («52 children were riding»), а подсадку ловил бы ЗАДАРОМ — не по её порче, а по свободному
# числу, и это ровно тот улов, который ищет scripts/court_mutants.py.
ДВИЖУЩИЕ = frozenset(я for я in ЯЗЫКИ if РЕЧЬ[я]["катались_один"] != РЕЧЬ[я]["катались_много"])


def единственное(язык, n):
    """Форма глагола есть форма ЧИСЛА, и её называет языковой пакет, а не последняя цифра."""
    return S._ячейка(язык, n) == 0


def страниц(язык, n):
    return "%d %s" % (n, S._счёт(СТРАНИЦА[язык], n, язык))


def детей(язык, n):
    return "%d %s" % (n, S._счёт(РЕБЁНОК[язык], n, язык))


def вещей(язык, i, n):
    """«8 книг», «5 ołówków» — товар берётся у дома цены вместе с правилом счёта."""
    return "%d %s" % (n, P.форма(язык, P.ЯЗЫКИ[язык]["вещи"][i], n))


def страница(язык, форма, n, m=0):
    р = РЕЧЬ[язык]
    if форма in ФОРМЫ_ДЛИНЫ:
        # ЧИСЛО СТОИТ СКАЗУЕМЫМ, А НЕ СЧЁТОМ ПРЕДМЕТОВ, и сказуемое это ДВУХ ВИДОВ
        тело = р[форма].format(Г=р["глава"], N=страниц(язык, n))
        вопрос = р["вопрос_обладания" if форма == "обладание" else "вопрос_длины"]
        return тело + ". " + вопрос + " " + страниц(язык, n) + "."
    if форма == "прогрессив":
        # ЧИСЛО УПРАВЛЯЕТ ГЛАГОЛОМ: русский ставит единственное при числе на один
        ключ = "катались_один" if единственное(язык, n) else "катались_много"
        тело = р[ключ].format(N=детей(язык, n))
        return тело + ". " + р["вопрос_детей"] + " " + детей(язык, n) + "."
    # ДВА СРАВНЕНИЯ ПРОТИВОПОЛОЖНЫХ НАПРАВЛЕНИЙ В ОДНОЙ ФРАЗЕ
    тело = р["двойное"].format(A=вещей(язык, 1, n), B=вещей(язык, 2, m))
    return тело + ". " + р["вопрос_двойного"] + " " + вещей(язык, 1, n) + "."


def _показы():
    вон = {}
    for язык in ЯЗЫКИ:
        for форма in ФОРМЫ_ДЛИНЫ:
            for n in ДЛИНЫ:
                вон[страница(язык, форма, n)] = (язык, форма)
        for n in ДЕТИ_ОДИН + ДЕТИ_МНОГО:
            вон[страница(язык, "прогрессив", n)] = (язык, "прогрессив")
        for n, m in ПАРЫ_ДВОЙНОГО:
            вон[страница(язык, "двойное", n, m)] = (язык, "двойное")
    return вон


ПОКАЗЫ = _показы()


def _альт(слова):
    сорт = sorted({с for с in слова if с}, key=lambda с: (-len(с), с))
    return "(?:" + "|".join(re.escape(с) for с in сорт) + ")"


def _дыры(язык):
    книги = _альт(P.ЯЗЫКИ[язык]["вещи"][1].values())
    карандаши = _альт(P.ЯЗЫКИ[язык]["вещи"][2].values())
    return {"N1": r"\d+ " + _альт(СТРАНИЦА[язык]), "N2": r"\d+ " + _альт(СТРАНИЦА[язык]),
            "D1": r"\d+ " + _альт(РЕБЁНОК[язык]), "D2": r"\d+ " + _альт(РЕБЁНОК[язык]),
            "A1": r"\d+ " + книги, "A2": r"\d+ " + книги, "B1": r"\d+ " + карандаши}


def рамка(язык, форма, один=True):
    р = РЕЧЬ[язык]
    if форма in ФОРМЫ_ДЛИНЫ:
        вопрос = р["вопрос_обладания" if форма == "обладание" else "вопрос_длины"]
        return р[форма].format(Г=р["глава"], N="{N1}") + ". " + вопрос + " {N2}."
    if форма == "прогрессив":
        ключ = "катались_один" if один else "катались_много"
        return р[ключ].format(N="{D1}") + ". " + р["вопрос_детей"] + " {D2}."
    return (р["двойное"].format(A="{A1}", B="{B1}") + ". " + р["вопрос_двойного"] + " {A2}.")


def _образец(язык, форма, один=True):
    дыры, счёт, куски = _дыры(язык), {}, []
    for кусок in re.split(r"(\{[^}]+\})", рамка(язык, форма, один)):
        if кусок.startswith("{"):
            дыра = кусок[1:-1]
            счёт[дыра] = счёт.get(дыра, 0) + 1
            куски.append(f"(?P<h_{дыра}__{счёт[дыра]}>{дыры[дыра]})")
        else:
            куски.append(re.escape(кусок))
    return re.compile("^" + "".join(куски) + "$")


ОБРАЗЦЫ = ([(_образец(язык, форма), язык, форма, None)
            for язык in ЯЗЫКИ for форма in ФОРМЫ_ДЛИНЫ + ("двойное",)]
           + [(_образец(язык, "прогрессив", один), язык, "прогрессив",
               один if язык in ДВИЖУЩИЕ else None)
              for язык in ЯЗЫКИ
              for один in ((True, False) if язык in ДВИЖУЩИЕ else (True,))])


def _значения(м):
    вон = {}
    for ключ, знач in м.groupdict().items():
        дыра, _ = ключ[2:].rsplit("__", 1)
        if дыра in вон and вон[дыра] != знач:
            return None
        вон[дыра] = знач
    return вон


def _число(кусок):
    return int(кусок.split(" ", 1)[0])


def _вердикт(язык, форма, один, зн):
    if форма in ФОРМЫ_ДЛИНЫ:
        n = _число(зн["N1"])
        # ОТВЕТ ЕСТЬ ТО ЖЕ ЧИСЛО В ТОЙ ЖЕ СЧЁТНОЙ ФОРМЕ — в обеих формах длины
        return зн["N1"] == зн["N2"] == страниц(язык, n)
    if форма == "прогрессив":
        n = _число(зн["D1"])
        # ФОРМА ГЛАГОЛА ЕСТЬ ФОРМА ЧИСЛА — и судится лишь там, где язык её двигает
        if один is not None and один != единственное(язык, n):
            return False
        return зн["D1"] == зн["D2"] == детей(язык, n)
    a, b = _число(зн["A1"]), _число(зн["B1"])
    # ВТОРОЕ ЧИСЛО НЕ ТЯНЕТСЯ ЗА ПЕРВЫМ, И ОТВЕТ ВЗЯТ У СПРОШЕННОГО
    return a != b and зн["A1"] == зн["A2"] == вещей(язык, 1, a) and зн["B1"] == вещей(язык, 2, b)


def судить(строка):
    """(судимо, истинно): a page whose number sits in its phrase and answers its question."""
    с = строка.strip()
    if с in ПОКАЗЫ:
        return True, True
    for образ, язык, форма, один in ОБРАЗЦЫ:
        м = образ.match(с)
        if not м:
            continue
        зн = _значения(м)
        if зн is None:
            return True, False
        return True, _вердикт(язык, форма, один, зн)
    return False, False


def _самопроверка():
    for показ in ПОКАЗЫ:
        assert судить(показ) == (True, True), показ
    мутанты = 0
    for язык in ЯЗЫКИ:
        for форма in ФОРМЫ_ДЛИНЫ:
            д = страница(язык, форма, 48)
            # (1) ОТВЕТ НАЗЫВАЕТ ДРУГОЕ ЧИСЛО — в каждой из двух форм длины
            битая = д.replace("? " + страниц(язык, 48), "? " + страниц(язык, 96))
            assert судить(битая) == (True, False), битая
            # (1а) СЧЁТНАЯ ФОРМА СТРАНИЦ ОТ ЧУЖОГО ЧИСЛА
            битая = д.replace(страниц(язык, 48), "48 " + S._счёт(СТРАНИЦА[язык], 2, язык), 1)
            if битая != д:
                assert судить(битая) == (True, False), битая
                мутанты += 1
            мутанты += 1
        д = страница(язык, "длина", 48)
        п = страница(язык, "прогрессив", 41)
        assert судить(п) == (True, True), п
        # (2) ОТВЕТ О ДЕТЯХ РАЗОШЁЛСЯ С ФРАЗОЙ
        битая = п.replace("? " + детей(язык, 41), "? " + детей(язык, 29))
        assert судить(битая) == (True, False), битая
        в = страница(язык, "двойное", 8, 5)
        assert судить(в) == (True, True), в
        # (3) ВТОРОЕ ЧИСЛО ПОТЯНУЛОСЬ ЗА ПЕРВЫМ
        битая = в.replace(вещей(язык, 2, 5), вещей(язык, 2, 8))
        assert судить(битая) == (True, False), битая
        # (4) ОТВЕТ ВЗЯТ У ВТОРОГО ЧИСЛА, А СПРОШЕНО О ПЕРВОМ
        битая = в.replace("? " + вещей(язык, 1, 8), "? " + вещей(язык, 1, 5))
        assert судить(битая) == (True, False), битая
        мутанты += 3
        # (5) ФОРМА ГЛАГОЛА НЕ ОТ ЧИСЛА (только там, где язык её двигает)
        м = страница(язык, "прогрессив", 35)
        if язык in ДВИЖУЩИЕ:
            битая = м.replace(РЕЧЬ[язык]["катались_много"].format(N=детей(язык, 35)),
                              РЕЧЬ[язык]["катались_один"].format(N=детей(язык, 35)))
            assert судить(битая) == (True, False), битая
            мутанты += 1
            # (6) ЛОВУШКА ПОСЛЕДНЕЙ ЦИФРЫ: одиннадцать кончается на один и берёт множественное
            одиннадцать = страница(язык, "прогрессив", 11)
            битая = одиннадцать.replace(РЕЧЬ[язык]["катались_много"].format(N=детей(язык, 11)),
                                        РЕЧЬ[язык]["катались_один"].format(N=детей(язык, 11)))
            assert судить(битая) == (True, False), битая
            мутанты += 1
        else:
            # ЧЕСТНАЯ СТРАНИЦА НЕДВИЖУЩЕГО ЯЗЫКА С ЧИСЛОМ ВНЕ ОБЪЯВЛЕННОГО НАБОРА НЕ ЕСТЬ ЛОЖЬ:
            # признака глагола у неё нет, и суду нечем её отвергнуть
            for n in (52, 7, 11):
                честная = страница(язык, "прогрессив", n)
                сохр = ПОКАЗЫ.pop(честная, None)
                вердикт = судить(честная)
                if сохр is not None:
                    ПОКАЗЫ[честная] = сохр
                assert вердикт == (True, True), (язык, n, вердикт, честная)
        # (6) ЗАЧИН ВОПРОСА ОБЪЯВЛЕН ДОМОМ ПАРЫ
        for стр in (д, п, в):
            вопрос = стр[стр.index(". ") + 2:стр.index("?") + 1]
            assert asking.зачин_объявлен(вопрос) is not False, (язык, вопрос)
    for язык in ЯЗЫКИ:
        print("  ", страница(язык, "прогрессив", 41))
    for язык in ("ru", "de", "pl"):
        print("  ", страница(язык, "длина", 48))
        print("  ", страница(язык, "двойное", 12, 7))
        print("  ", страница(язык, "прогрессив", 35))
    по_форме = {}
    for _, (_я, форма) in ПОКАЗЫ.items():
        по_форме[форма] = по_форме.get(форма, 0) + 1
    print(f"  мутантов поймано: {мутанты}")
    print(f"  дом пишет показов: {len(ПОКАЗЫ)} (языков {len(ЯЗЫКИ)}, образцов {len(ОБРАЗЦЫ)}): "
          + ", ".join(f"{ф} {к}" for ф, к in по_форме.items()))


if __name__ == "__main__":
    _самопроверка()
