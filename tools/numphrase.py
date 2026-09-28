#!/usr/bin/env python3
"""THE HOUSE OF THE NUMBER'S PHRASE — the number that hangs on a form, not on a digit (06.09).

The measure of the executor (d5, band p156) named the debt exactly: of 423 tacts where the reader
does not read a number, 409 carry PLAIN DIGITS — the trouble is not the shape of the number but
the shape of the PHRASE it hangs on. The lines it stumbles on are «the first chapter is 48 pages
long», «41 children were riding», «36 more push-ups but 33 fewer crunches». The census of the свод
says why: eight lines carry «N pages long», six carry a progressive with a counted subject, and
ZERO carry «N more … but N fewer».

FOUR FRAMES, EACH A DIFFERENT WAY FOR A NUMBER TO SIT IN A SENTENCE:
  обладание      — the measure as what the text HAS: «the story has 52 pages», «в рассказе
                   52 страницы» (Russian has no verb here at all — the number stands in a
                   locative phrase with no predicate to lean on);
  длина          — the SAME FACT as a PREDICATE OF LENGTH: the story IS fifty-two pages long.
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
question wearing four bodies: «how many pages does the story have?» is not «how long is it?».
Each page ends with a question about ONE of its numbers and the number as the answer — the debt
the measure named is exactly this: a number that no question reaches.

WHAT IS BORROWED: the goods of the house of price and the counting rule of the packs. Declared
here: the story and the page, the child and the verb of riding, and the two comparison frames.

SCENES REWRITTEN 23.09 BY THE OWNER'S WORD (a band is an instrument, not a textbook): the house was
ordered by the lines of the SVAMP band itself — «a book has 2 chapters. the first chapter is 48 pages
long», «41 children were riding». The four frames stay; the chapter became a story, and the
lengths and the counts of children are no longer the band's numbers.

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
# ЧИСЛА ПОЛОСЫ УШЛИ (23.09): «the first chapter is 48 pages long», «37 pages long» и «41 children
# were riding» — строки самой полосы SVAMP, по которым дом был заказан; длины и дети — наши.
ДЛИНЫ = (52, 83, 132, 29, 70, 243)
ДЕТИ_ОДИН = (21, 61, 31, 101)
ДЕТИ_МНОГО = (29, 35, 42, 11, 111)
# ДВОЙНОЕ СРАВНЕНИЕ: (больше, меньше) — числа разные, чтобы второе не тянулось за первым
ПАРЫ_ДВОЙНОГО = ((8, 5), (12, 7), (15, 9), (6, 4))
# ДВЕ ФОРМЫ ДЛИНЫ, А НЕ ОДНА (просьба holon 06.09): один и тот же факт о рассказе сказан
# ОБЛАДАНИЕМ («в рассказе 52 страницы», «the story has 52 pages») и ПРЕДИКАТОМ
# ДЛИНЫ («рассказ — 52 страницы длиной», «the story is 52 pages long»), и обе на
# всех девяти языках. Дом, дающий языку одну форму, продаёт рынку ту одну: читатель выучит,
# что число живёт при «has», и не узнает его при «is … long». Языки расходятся в том, ОТДЕЛЬНЫЙ
# ли у предиката глагол (ru, en, de, fr, it, nl) или хвост при глаголе обладания (es, pt, pl), —
# и это расхождение само есть показанный факт.
ФОРМЫ = ("обладание", "длина", "прогрессив", "двойное")
ФОРМЫ_ДЛИНЫ = ("обладание", "длина")
РЕЧЬ = {
    "ru": dict(глава="рассказ", обладание="в рассказе {N}", вопрос_обладания="сколько страниц в рассказе?",
               длина="{Г} — {N} длиной", вопрос_длины="какой длины рассказ?",
               катались_один="{N} катался на карусели", катались_много="{N} каталось на карусели",
               вопрос_детей="сколько детей каталось на карусели?",
               двойное="у Ани на {A} больше, но на {B} меньше",
               вопрос_двойного="на сколько книг больше?"),
    "en": dict(глава="the story", обладание="{Г} has {N}", вопрос_обладания="how many pages does the story have?",
               длина="{Г} is {N} long", вопрос_длины="how long is the story?",
               катались_один="{N} were riding the carousel", катались_много="{N} were riding the carousel",
               вопрос_детей="how many children were riding the carousel?",
               двойное="ann has {A} more but {B} fewer",
               вопрос_двойного="how many more books?"),
    "de": dict(глава="die Geschichte", обладание="{Г} hat {N}", вопрос_обладания="wie viele Seiten hat die Geschichte?",
               длина="{Г} ist {N} lang", вопрос_длины="wie lang ist die Geschichte?",
               катались_один="{N} fuhren Karussell", катались_много="{N} fuhren Karussell",
               вопрос_детей="wie viele Kinder fuhren Karussell?",
               двойное="Anna hat {A} mehr, aber {B} weniger",
               вопрос_двойного="wie viele Bücher mehr?"),
    "fr": dict(глава="le récit", обладание="{Г} fait {N}", вопрос_обладания="combien de pages fait le récit ?",
               длина="{Г} est long de {N}", вопрос_длины="quelle est la longueur du récit ?",
               катались_один="{N} faisaient du manège", катались_много="{N} faisaient du manège",
               вопрос_детей="combien d'enfants faisaient du manège ?",
               двойное="anne a {A} de plus, mais {B} de moins",
               вопрос_двойного="combien de livres en plus ?"),
    "es": dict(глава="el cuento", обладание="{Г} tiene {N}", вопрос_обладания="¿cuántas páginas tiene el cuento?",
               длина="{Г} tiene {N} de largo", вопрос_длины="¿qué longitud tiene el cuento?",
               катались_один="{N} montaban en el tiovivo", катались_много="{N} montaban en el tiovivo",
               вопрос_детей="¿cuántos niños montaban en el tiovivo?",
               двойное="ana tiene {A} más, pero {B} menos",
               вопрос_двойного="¿cuántos libros más?"),
    "it": dict(глава="il racconto", обладание="{Г} ha {N}", вопрос_обладания="quante pagine ha il racconto?",
               длина="{Г} è lungo {N}", вопрос_длины="quanto è lungo il racconto?",
               катались_один="{N} andavano sulla giostra", катались_много="{N} andavano sulla giostra",
               вопрос_детей="quanti bambini andavano sulla giostra?",
               двойное="anna ha {A} in più, ma {B} in meno",
               вопрос_двойного="quanti libri in più?"),
    "pt": dict(глава="o conto", обладание="{Г} tem {N}", вопрос_обладания="quantas páginas tem o conto?",
               длина="{Г} tem {N} de comprimento", вопрос_длины="qual é o comprimento do conto?",
               катались_один="{N} andavam no carrossel", катались_много="{N} andavam no carrossel",
               вопрос_детей="quantas crianças andavam no carrossel?",
               двойное="ana tem {A} a mais, mas {B} a menos",
               вопрос_двойного="quantos livros a mais?"),
    "nl": dict(глава="het verhaal", обладание="{Г} heeft {N}", вопрос_обладания="hoeveel bladzijden heeft het verhaal?",
               длина="{Г} is {N} lang", вопрос_длины="hoe lang is het verhaal?",
               катались_один="{N} reden op de draaimolen", катались_много="{N} reden op de draaimolen",
               вопрос_детей="hoeveel kinderen reden op de draaimolen?",
               двойное="anna heeft {A} meer, maar {B} minder",
               вопрос_двойного="hoeveel boeken meer?"),
    "pl": dict(глава="opowiadanie", обладание="{Г} ma {N}", вопрос_обладания="ile stron ma opowiadanie?",
               длина="{Г} ma {N} długości", вопрос_длины="jakiej długości jest opowiadanie?",
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
    # ВЫХОД ПО НАБОРУ СНЯТ (21.09): здесь стояло «если строка в ПОКАЗЫ — истина», и
    # содержательный закон ниже не спрашивался о СВОИХ страницах ни разу.
    #
    #     НАБОР ГОВОРИТ, ЧТО ДОМ СТРАНИЦУ НАПИСАЛ, А НЕ ЧТО ОНА ВЕРНА.
    #
    # Замерено: закон судит все 225 показов дома верно и без набора — выход был
    # чистым балластом, слепившим дом к порче, вписанной в его же набор. Полный закон
    # и замер по всем сорока шести домам — в `scripts/house_mutant.py`.
    for образ, язык, форма, один in ОБРАЗЦЫ:
        м = образ.match(с)
        if not м:
            continue
        зн = _значения(м)
        if зн is None:
            return True, False
        return True, _вердикт(язык, форма, один, зн)
    return False, False


def подсадки():
    """ПРЕДСТАВЛЕННОЕ «НЕТ» (М-483), ВЫВЕДЕННОЕ ИЗ ТАБЛИЦ ДОМА (23.09), — [(род порчи, битая строка)].

    Суд мира держал подсадки литералами прежних сцен («the first chapter is 124 pages long…»), и
    перепись сцен оставила бы их чужими строками. Порча берётся у страницы, которую дом пишет
    сейчас, и каждая ловится СВОЕЙ порчей: ответ длины назвал другое число (в обеих формах);
    счётная форма страниц от чужого числа; русский глагол в единственном при числе многих;
    ЛОВУШКА ПОСЛЕДНЕЙ ЦИФРЫ — одиннадцать в единственном; ответ о детях разошёлся с фразой; второе
    число потянулось за первым; ответ взят у второго числа; счётная форма товара от чужого числа."""
    д0, д1 = ДЛИНЫ[0], ДЛИНЫ[1]
    один = ДЕТИ_ОДИН[1]
    много = next(n for n in ДЕТИ_МНОГО if n % 100 not in range(11, 15))
    одиннадцать = next(n for n in ДЕТИ_МНОГО if n % 100 in range(11, 15))
    a, b = ПАРЫ_ДВОЙНОГО[1]
    вон = []
    for язык in ЯЗЫКИ:
        for форма in ФОРМЫ_ДЛИНЫ:
            д = страница(язык, форма, д0)
            вон.append(("ответ длины — другое число", д, д.replace("? " + страниц(язык, д0), "? " + страниц(язык, д1))))
            чужая = д.replace(страниц(язык, д0), f"{д0} " + S._счёт(СТРАНИЦА[язык], 2, язык), 1)
            if чужая != д:
                вон.append(("счётная форма страниц от чужого числа", д, чужая))
        п = страница(язык, "прогрессив", один)
        вон.append(("ответ о детях разошёлся с фразой", п, п.replace("? " + детей(язык, один), "? " + детей(язык, много))))
        в = страница(язык, "двойное", a, b)
        вон.append(("второе число потянулось за первым", в, в.replace(вещей(язык, 2, b), вещей(язык, 2, a))))
        вон.append(("ответ у второго числа", в, в.replace("? " + вещей(язык, 1, a), "? " + вещей(язык, 1, b))))
        чужая = в.replace(вещей(язык, 1, a), f"{a} " + P.форма(язык, P.ЯЗЫКИ[язык]["вещи"][1], 2), 1)
        if чужая != в:
            вон.append(("счётная форма товара от чужого числа", в, чужая))
        if язык in ДВИЖУЩИЕ:
            for n, род in ((много, "глагол в единственном при числе многих"),
                           (одиннадцать, "ловушка последней цифры: одиннадцать в единственном")):
                м = страница(язык, "прогрессив", n)
                вон.append((род, м, м.replace(РЕЧЬ[язык]["катались_много"].format(N=детей(язык, n)),
                                              РЕЧЬ[язык]["катались_один"].format(N=детей(язык, n)))))
    for род, с, битая in вон:
        assert битая != с, (род, с)
    return [(род, битая) for род, _, битая in вон]


def _самопроверка():
    for показ in ПОКАЗЫ:
        assert судить(показ) == (True, True), показ
    мутанты = 0
    for род, битая in подсадки():
        assert судить(битая) == (True, False), (род, битая)
        мутанты += 1
    д0, один, (a, b) = ДЛИНЫ[0], ДЕТИ_ОДИН[1], ПАРЫ_ДВОЙНОГО[1]
    for язык in ЯЗЫКИ:
        if язык not in ДВИЖУЩИЕ:
            # ЧЕСТНАЯ СТРАНИЦА НЕДВИЖУЩЕГО ЯЗЫКА С ЧИСЛОМ ВНЕ ОБЪЯВЛЕННОГО НАБОРА НЕ ЕСТЬ ЛОЖЬ:
            # признака глагола у неё нет, и суду нечем её отвергнуть
            for n in (52, 7, 11):
                честная = страница(язык, "прогрессив", n)
                сохр = ПОКАЗЫ.pop(честная, None)
                вердикт = судить(честная)
                if сохр is not None:
                    ПОКАЗЫ[честная] = сохр
                assert вердикт == (True, True), (язык, n, вердикт, честная)
        # ЗАЧИН ВОПРОСА ОБЪЯВЛЕН ДОМОМ ПАРЫ
        for стр in (страница(язык, "длина", д0), страница(язык, "прогрессив", один), страница(язык, "двойное", a, b)):
            вопрос = стр[стр.index(". ") + 2:стр.index("?") + 1]
            assert asking.зачин_объявлен(вопрос) is not False, (язык, вопрос)
    for язык in ЯЗЫКИ:
        print("  ", страница(язык, "прогрессив", один))
    for язык in ("ru", "de", "pl"):
        print("  ", страница(язык, "длина", д0))
        print("  ", страница(язык, "двойное", a, b))
        print("  ", страница(язык, "прогрессив", ДЕТИ_МНОГО[1]))
    по_форме = {}
    for _, (_я, форма) in ПОКАЗЫ.items():
        по_форме[форма] = по_форме.get(форма, 0) + 1
    print(f"  мутантов поймано: {мутанты}")
    print(f"  дом пишет показов: {len(ПОКАЗЫ)} (языков {len(ЯЗЫКИ)}, образцов {len(ОБРАЗЦЫ)}): "
          + ", ".join(f"{ф} {к}" for ф, к in по_форме.items()))


if __name__ == "__main__":
    _самопроверка()
