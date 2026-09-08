#!/usr/bin/env python3
"""THE HOUSE OF THE QUANTIFIER — «all», «some», «none» over a set that is counted (06.09).

The census found FOUR lines of «every one of» in the whole свод. The corpus counts a set and
compares its parts, but it almost never says what holds of ALL of it, of SOME of it, or of NONE
of it — and those three are the whole of elementary logic, the place where a number turns into
a claim.

FIVE QUESTIONS OVER ONE BASKET, and each answer carries its WITNESS:

    ALL, AND ITS REFUTATION. «are all the apples red? no: 2 are green» — a universal claim is
    refuted by a counted witness, not by a bare «no». And its true twin, over a basket where
    every apple is red, answers «yes: all 4 are red».

    SOME. «are there any green ones? yes: 2 are green» — an existential claim answered by the
    count that makes it true.

    NONE. «are there any blue ones? no: not one is blue» — the colour that the basket never
    carried, refused with its ground, so that «no» is not a guess about the unseen.

    THE COMPLEMENT, COUNTED. «how many apples are not red? 2: 5 − 3 = 2» — negation as
    subtraction, which is where a quantifier meets arithmetic.

WHAT IS BORROWED: nine languages, the goods and the counting rule of the packs (through the
house of the price), and the openers of the house of the pair. Declared here: the three colours
in the form each language uses after a number, and the sentences of the four claims.

WHAT IS NOT MEASURED, NAMED: nested quantifiers («every basket has some red apple»), a set of
more than two kinds at once, and the vague quantifiers «many» and «few» — a corpus that counts
cannot afford a word whose truth it cannot check.
"""
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import asking  # noqa: E402 — the house of the pair declares which openers a question may wear
import plgram as _PL  # noqa: E402 — закон польской связки: один закон, один читатель
import priceforms as P  # noqa: E402 — the apple and the pack's counting rule

ЯЗЫКИ = ("ru", "en", "de", "fr", "es", "it", "pt", "nl", "pl")
# ЦВЕТ СТОИТ В ТРЁХ РАЗНЫХ ПАДЕЖАХ, И ЭТО НЕ ПРИДИРКА, А ЯЗЫК. При числе он один
# («3 красных яблока», «3 czerwone jabłka» при двух-четырёх и «5 czerwonych» при пяти),
# сказуемым другой (немецкое сказуемое НЕ СКЛОНЯЕТСЯ: «2 sind grün», а не «grüne»),
# после отрицания третий («сколько яблок не красных?»). Три таблицы, а не одна с догадкой.
# ЦВЕТ ПРИ ЧИСЛЕ ГНЁТСЯ ПО СЧЁТУ, И ЕДИНИЦА БЕРЁТ ЕДИНСТВЕННОЕ. Суд согласования поймал
# 24 обвинения (06.09): «1 красных», «1 rouges», «1 rojas», «1 rote», «1 rosse», «1 rode» —
# ложь письма в шести языках разом, рождённая тем, что цвет объявлялся ОДНОЙ формой. Цвет при
# числе есть ПРИЛАГАТЕЛЬНОЕ и гнётся как счётное имя; формы взяты по роду вещи корзины
# (яблоко — среднего рода, Apfel — мужского, pomme/manzana/mela/maçã — женского).
ЦВ_ПРИ_ЧИСЛЕ = {
    "ru": (dict(one="красное", few="красных", many="красных"),
           dict(one="зелёное", few="зелёных", many="зелёных"),
           dict(one="синее", few="синих", many="синих")),
    "en": ("red", "green", "blue"),
    "de": (dict(one="roter", many="rote"), dict(one="grüner", many="grüne"),
           dict(one="blauer", many="blaue")),
    "fr": (dict(one="rouge", many="rouges"), dict(one="verte", many="vertes"),
           dict(one="bleue", many="bleues")),
    "es": (dict(one="roja", many="rojas"), dict(one="verde", many="verdes"),
           dict(one="azul", many="azules")),
    "it": (dict(one="rossa", many="rosse"), dict(one="verde", many="verdi"),
           dict(one="blu", many="blu")),
    "pt": (dict(one="vermelha", many="vermelhas"), dict(one="verde", many="verdes"),
           dict(one="azul", many="azuis")),
    "nl": ("rode", "groene", "blauwe"),
    "pl": (dict(one="czerwone", few="czerwone", many="czerwonych"),
           dict(one="zielone", few="zielone", many="zielonych"),
           dict(one="niebieskie", few="niebieskie", many="niebieskich")),
}
ЦВ_СКАЗУЕМОЕ = {
    "ru": ("красные", "зелёные", "синие"), "en": ("red", "green", "blue"),
    "de": ("rot", "grün", "blau"), "fr": ("rouges", "vertes", "bleues"),
    "es": ("rojas", "verdes", "azules"), "it": ("rosse", "verdi", "blu"),
    "pt": ("vermelhas", "verdes", "azuis"), "nl": ("rood", "groen", "blauw"),
    "pl": ("czerwone", "zielone", "niebieskie"),
}
ЦВ_ОТРИЦАНИЕ = {
    "ru": ("красных", "зелёных", "синих"), "en": ("red", "green", "blue"),
    "de": ("rot", "grün", "blau"), "fr": ("rouges", "vertes", "bleues"),
    "es": ("rojas", "verdes", "azules"), "it": ("rosse", "verdi", "blu"),
    "pt": ("vermelhas", "verdes", "azuis"), "nl": ("rood", "groen", "blauw"),
    "pl": ("czerwonych", "zielonych", "niebieskich"),
}
# ГОЛЫЙ МНОЖЕСТВЕННЫЙ ВЕЩИ — для «все ли ЯБЛОКИ красные?»: счётная форма («яблок», «jabłek»)
# именительного не заменяет
ПЛЮРАЛЬ = {"ru": "яблоки", "en": "apples", "de": "Äpfel", "fr": "pommes", "es": "manzanas",
           "it": "mele", "pt": "maçãs", "nl": "appels", "pl": "jabłka"}
НАБОРЫ = ((5, 3), (7, 4), (6, 2), (9, 5), (8, 6), (4, 1), (11, 7), (10, 3),
          (12, 8), (13, 9), (6, 4), (15, 11), (14, 6), (7, 2), (9, 7), (8, 5))
ВСЕ_КРАСНЫЕ = (4, 6, 5, 8, 7, 9, 3, 10)
РЕЧЬ = {
    "ru": dict(корзина="в корзине {n} {Т}: {k} {ЦА} и {m} {ЦБ}.",
               корзина_все="в корзине {n} {Т}: все {n} {ЦА}.",
               вопрос_все="все ли {Тмн} {ЦАИ}?", вопрос_есть="есть ли {ЦБ}?",
               вопрос_нет="есть ли {ЦВ}?", вопрос_не="сколько {Тмн} не {ЦАИ}?",
               да="да", нет="нет", ни_одного="ни одного {ЦВЕД}", все_они="все {n} {ЦА}",
               свидетель="{m} {ЦБ}", двоеточие=": "),
    "en": dict(корзина="there are {n} {Т} in the basket: {k} {ЦА} and {m} {ЦБ}.",
               корзина_все="there are {n} {Т} in the basket: all {n} {ЦА}.",
               вопрос_все="are all the {Тмн} {ЦАИ}?", вопрос_есть="are there any {ЦБ} ones?",
               вопрос_нет="are there any {ЦВ} ones?", вопрос_не="how many {Тмн} are not {ЦАИ}?",
               да="yes", нет="no", ни_одного="not one is {ЦВЕД}", все_они="all {n} are {ЦА}",
               свидетель="{m} are {ЦБ}", двоеточие=": "),
    "de": dict(корзина="im Korb sind {n} {Т}: {k} {ЦА} und {m} {ЦБ}.",
               корзина_все="im Korb sind {n} {Т}: alle {n} {ЦА}.",
               вопрос_все="sind alle {Тмн} {ЦАИ}?", вопрос_есть="gibt es {ЦБ}?",
               вопрос_нет="gibt es {ЦВ}?", вопрос_не="wie viele {Тмн} sind nicht {ЦАИ}?",
               да="ja", нет="nein", ни_одного="kein einziger ist {ЦВЕД}", все_они="alle {n} sind {ЦА}",
               свидетель="{m} sind {ЦБс}", двоеточие=": "),
    "fr": dict(корзина="il y a {n} {Т} dans le panier : {k} {ЦА} et {m} {ЦБ}.",
               корзина_все="il y a {n} {Т} dans le panier : toutes les {n} {ЦА}.",
               вопрос_все="toutes les {Тмн} sont-elles {ЦАИ} ?", вопрос_есть="y a-t-il des {ЦБ} ?",
               вопрос_нет="y a-t-il des {ЦВ} ?", вопрос_не="combien de {Тмн} ne sont pas {ЦАИ} ?",
               да="oui", нет="non", ни_одного="aucune n'est {ЦВЕД}", все_они="toutes les {n} sont {ЦА}",
               свидетель="{m} sont {ЦБ}", двоеточие=" : "),
    "es": dict(корзина="hay {n} {Т} en la cesta: {k} {ЦА} y {m} {ЦБ}.",
               корзина_все="hay {n} {Т} en la cesta: las {n} {ЦА}.",
               вопрос_все="¿son {ЦАИ} todas las {Тмн}?", вопрос_есть="¿hay {ЦБ}?",
               вопрос_нет="¿hay {ЦВ}?", вопрос_не="¿cuántas {Тмн} no son {ЦАИ}?",
               да="sí", нет="no", ни_одного="ninguna es {ЦВЕД}", все_они="las {n} son {ЦА}",
               свидетель="{m} son {ЦБ}", двоеточие=": "),
    "it": dict(корзина="nel cesto ci sono {n} {Т}: {k} {ЦА} e {m} {ЦБ}.",
               корзина_все="nel cesto ci sono {n} {Т}: tutte e {n} {ЦА}.",
               вопрос_все="è vero che tutte le {Тмн} sono {ЦАИ}?", вопрос_есть="ci sono {Тмн} {ЦБ}?",
               вопрос_нет="ci sono {Тмн} {ЦВ}?", вопрос_не="quante {Тмн} non sono {ЦАИ}?",
               да="sì", нет="no", ни_одного="nessuna è {ЦВЕД}", все_они="tutte e {n} sono {ЦА}",
               свидетель="{m} sono {ЦБ}", двоеточие=": "),
    "pt": dict(корзина="há {n} {Т} no cesto: {k} {ЦА} e {m} {ЦБ}.",
               корзина_все="há {n} {Т} no cesto: as {n} {ЦА}.",
               вопрос_все="são todas as {Тмн} {ЦАИ}?", вопрос_есть="tem {Тмн} {ЦБ}?",
               вопрос_нет="tem {Тмн} {ЦВ}?", вопрос_не="quantas {Тмн} não são {ЦАИ}?",
               да="sim", нет="não", ни_одного="nenhuma é {ЦВЕД}", все_они="as {n} são {ЦА}",
               свидетель="{m} são {ЦБ}", двоеточие=": "),
    "nl": dict(корзина="in de mand liggen {n} {Т}: {k} {ЦА} en {m} {ЦБ}.",
               корзина_все="in de mand liggen {n} {Т}: alle {n} {ЦА}.",
               вопрос_все="zijn alle {Тмн} {ЦАИ}?", вопрос_есть="zijn er {ЦБ}?",
               вопрос_нет="zijn er {ЦВ}?", вопрос_не="hoeveel {Тмн} zijn niet {ЦАИ}?",
               да="ja", нет="nee", ни_одного="geen enkele is {ЦВЕД}", все_они="alle {n} zijn {ЦА}",
               свидетель="{m} zijn {ЦБс}", двоеточие=": "),
    "pl": dict(корзина="w koszyku {ЕСТЬ} {n} {Т}: {k} {ЦА} i {m} {ЦБ}.",
               корзина_все="w koszyku {ЕСТЬ} {n} {Т}: wszystkie {n} {ЦА}.",
               вопрос_все="czy wszystkie {Тмн} są {ЦАИ}?", вопрос_есть="czy są {ЦБ}?",
               вопрос_нет="czy są {ЦВ}?", вопрос_не="ile {Тмн} nie jest {ЦАИ}?",
               да="tak", нет="nie", ни_одного="ani jedno nie jest {ЦВЕД}", все_они="wszystkie {n} {ЕСТЬ} {ЦА}",
               свидетель="{m} {ЦБ}", двоеточие=": "),
}
ФОРМЫ = ("все_нет", "все_да", "есть_да", "ни_одного", "сколько_не")


def _вещь(язык, k):
    return P.форма(язык, P.ЯЗЫКИ[язык]["вещи"][0], k)


def _цвет_при_числе(язык, i, n):
    """Цвет при числе ГНЁТСЯ ПО СЧЁТУ: единица берёт единственное («1 красное», «1 roter»),
    прочие — множественное. Английский и голландский не гнут его вовсе, и их форма одна."""
    з = ЦВ_ПРИ_ЧИСЛЕ[язык][i]
    return P.форма(язык, з, n) if isinstance(з, dict) else з


def рамка(язык, форма, nk=None):
    """nk = (n, k, m): числа нужны там, где цвет при числе гнётся по счёту (польский)."""
    р = РЕЧЬ[язык]
    n, k, m = nk if nk else (5, 3, 2)
    ЦА, ЦБ = _цвет_при_числе(язык, 0, k), _цвет_при_числе(язык, 1, m)
    ЦАвсе = _цвет_при_числе(язык, 0, n)
    ЦВ = ЦВ_СКАЗУЕМОЕ[язык][2]
    ЦБс = ЦВ_СКАЗУЕМОЕ[язык][1]
    ЦАИ = ЦВ_СКАЗУЕМОЕ[язык][0]
    ЦАотр = ЦВ_ОТРИЦАНИЕ[язык][0]
    ЦВЕД = ЦВ_СКАЗУЕМОЕ[язык][2]
    def дать(ключ):
        с = р[ключ]
        # «{ЦА}» при числе всего набора — в форме «все N красных»
        если_все = ключ in ("корзина_все", "все_они")
        с = с.replace("{ЦА}", ЦАвсе if если_все else ЦА)
        # СКАЗУЕМОЕ ОБЪЯВЛЯЕТ СЕБЯ САМО: шаблон, которому нужна несклоняемая форма, пишет
        # «{ЦБс}» (немецкое «2 sind grün»), а форму при числе — «{ЦБ}» («2 зелёных»)
        с = с.replace("{ЦБс}", ЦБс)
        с = с.replace("{ЦБ}", ЦБс if ключ in ("вопрос_есть",) else ЦБ)
        с = с.replace("{ЦВ}", ЦВ).replace("{ЦВЕД}", ЦВЕД)
        с = с.replace("{ЦАИ}", ЦАотр if ключ == "вопрос_не" else ЦАИ)
        # ВОПРОС «СКОЛЬКО …» БЕРЁТ СЧЁТНУЮ ФОРМУ, А «ВСЕ ЛИ …» — ИМЕНИТЕЛЬНЫЙ МНОЖЕСТВЕННЫЙ:
        # «ile jabłEK nie jest czerwonych?» против «czy wszystkie jabłKA są czerwone?»
        мн = _вещь(язык, 5) if ключ == "вопрос_не" else ПЛЮРАЛЬ[язык]
        # СВЯЗКА ГНЁТСЯ ТЕМ ЖЕ ЧИСЛОМ, ЧТО И ЦВЕТ РЯДОМ С НЕЙ (08.09). «w koszyku jest 4
        # jabłka» было ложью по-польски — при двух-четырёх стои́т «są»; и та же ложь стояла
        # в ответе «wszystkie 6 są czerwonych», где дом УЖЕ гнул прилагательное по полосе
        # («czerwone» / «czerwonych») и оставлял глагол буквой.
        #
        #     ОДНА ОГОВОРКА, ГНУЩАЯ ПРИЛАГАТЕЛЬНОЕ И НЕ ГНУЩАЯ ГЛАГОЛА, ПРОТИВОРЕЧИТ СЕБЕ
        #     В ПРЕДЕЛАХ ТРЁХ СЛОВ.
        #
        # Закон берётся у дома языка (`plgram.связка`), а не пишется здесь; подмена связки
        # ловится законом замкнутого мира (`closedworld.ложь_по_связке`), а не рамкой.
        if "{ЕСТЬ}" in с:
            с = с.replace("{ЕСТЬ}", _PL.связка("наст", n))
        return с.replace("{Тмн}", мн)
    if форма == "все_да":
        # УНИВЕРСАЛЬНОЕ УТВЕРЖДЕНИЕ, КОТОРОЕ ВЕРНО, ТОЖЕ НЕСЁТ СВИДЕТЕЛЯ — счёт всего набора
        return (дать("корзина_все") + " " + дать("вопрос_все") + " " + р["да"] + р["двоеточие"]
                + дать("все_они") + ".")
    начало = дать("корзина")
    if форма == "все_нет":
        # УНИВЕРСАЛЬНОЕ ОПРОВЕРГАЕТСЯ СЧЁТНЫМ СВИДЕТЕЛЕМ, А НЕ ГОЛЫМ «НЕТ»
        return (начало + " " + дать("вопрос_все") + " " + р["нет"] + р["двоеточие"]
                + дать("свидетель") + ".")
    if форма == "есть_да":
        return (начало + " " + дать("вопрос_есть") + " " + р["да"] + р["двоеточие"]
                + дать("свидетель") + ".")
    if форма == "ни_одного":
        # ЦВЕТ, КОТОРОГО КОРЗИНА НЕ НЕСЛА: отказ с основанием, а не догадка о невидимом
        return (начало + " " + дать("вопрос_нет") + " " + р["нет"] + р["двоеточие"]
                + дать("ни_одного") + ".")
    # ОТРИЦАНИЕ КАК ВЫЧИТАНИЕ — там квантор встречается с арифметикой
    return начало + " " + дать("вопрос_не") + " {m}" + р["двоеточие"] + "{n} − {k} = {m}."


def страница(язык, форма, n, k):
    m = n - k
    поля = dict(n=n, k=k, m=m, Т=_вещь(язык, n))
    return рамка(язык, форма, (n, k, m)).format(**поля)


def _показы():
    вон = {}
    for язык in ЯЗЫКИ:
        for n, k in НАБОРЫ:
            for форма in ("все_нет", "есть_да", "ни_одного", "сколько_не"):
                вон[страница(язык, форма, n, k)] = (язык, форма)
        for n in ВСЕ_КРАСНЫЕ:
            вон[страница(язык, "все_да", n, n)] = (язык, "все_да")
    return вон


ПОКАЗЫ = _показы()


def _альт(слова):
    return "(?:" + "|".join(re.escape(с) for с in sorted({с for с in слова if с}, key=lambda с: (-len(с), с))) + ")"


def _образец(язык, форма, nk):
    вещи = _альт(P.ЯЗЫКИ[язык]["вещи"][0].values())
    дыры = {"n": r"\d+", "k": r"\d+", "m": r"\d+", "Т": вещи, "Тмн": вещи}
    счёт, куски = {}, []
    for кусок in re.split(r"(\{[^}]+\})", рамка(язык, форма, nk)):
        if кусок.startswith("{"):
            дыра = кусок[1:-1]
            счёт[дыра] = счёт.get(дыра, 0) + 1
            куски.append(f"(?P<h_{дыра}__{счёт[дыра]}>{дыры[дыра]})")
        else:
            куски.append(re.escape(кусок))
    return re.compile("^" + "".join(куски) + "$")


# ФОРМЫ ЦВЕТА ПРИ ЧИСЛЕ РАЗНЫЕ У РАЗНЫХ СЧЁТОВ (польский), и потому образец строится на
# КАЖДЫЙ набор чисел дома: рамка есть форма, а форма зависит от того, сколько их
_НАБОРЫ_РАМОК = sorted({(n, k, n - k) for n, k in НАБОРЫ} | {(n, n, 0) for n in ВСЕ_КРАСНЫЕ})
ОБРАЗЦЫ = [(_образец(язык, форма, nk), язык, форма, nk)
           for язык in ЯЗЫКИ for форма in ФОРМЫ for nk in _НАБОРЫ_РАМОК]


def _значения(м):
    вон = {}
    for ключ, знач in м.groupdict().items():
        дыра, _ = ключ[2:].rsplit("__", 1)
        if дыра in вон and вон[дыра] != знач:
            return None
        вон[дыра] = знач
    return вон


def _вердикт(язык, форма, зн, nk):
    """ЧИСЛА СТРАНИЦЫ ОБЯЗАНЫ БЫТЬ ЧИСЛАМИ ЕЁ РАМКИ, ибо форма цвета живёт в рамке.

    Образец строится на КАЖДЫЙ набор чисел (цвет при числе гнётся по счёту), а дыры {n}, {k},
    {m} берут любые цифры — и строка «1 красных» проходила образцом, собранным для пятёрки с
    тройкой: числа свои, цвет чужой. Суд согласования поймал это раньше меня (24 обвинения в
    шести языках, 06.09); ныне вердикт требует, чтобы числа строки были числами ЕЁ рамки.
    """
    n = int(зн["n"])
    k_рамки = nk[1] if форма != "все_да" else nk[0]
    if n != nk[0]:
        return False
    if форма != "все_да" and int(зн["k"]) != k_рамки:
        return False
    if n < 1 or зн.get("Т") != _вещь(язык, n):
        return False
    if форма == "все_да":
        return True           # рамка несёт одно число, и оно есть весь набор
    k = int(зн["k"])
    m = int(зн["m"]) if "m" in зн else None
    if not (1 <= k < n):
        return False          # если бы k равнялось n, зелёных не было бы вовсе
    if m is None or m != n - k:
        return False
    return True


def _судить_образцом(строка):
    """(судимо, истинно): a page of a frame of the house whose witness counts; else silence."""
    с = строка.strip()
    if с in ПОКАЗЫ:
        return True, True
    for образ, язык, форма, nk in ОБРАЗЦЫ:
        м = образ.match(с)
        if not м:
            continue
        зн = _значения(м)
        if зн is None:
            return True, False
        return True, _вердикт(язык, форма, зн, nk)
    return False, False


def _хвост(с):
    м = list(re.finditer(r"[?？]\s", с))
    return м[-1].end() if м else 0


def _самопроверка():
    for показ in ПОКАЗЫ:
        assert судить(показ) == (True, True), показ
    мутанты = 0
    for язык in ЯЗЫКИ:
        n, k = 5, 3
        # (1) СВИДЕТЕЛЬ ОПРОВЕРЖЕНИЯ ПОСЧИТАН НЕВЕРНО
        вн = страница(язык, "все_нет", n, k)
        assert судить(вн) == (True, True), вн
        хв = _хвост(вн)
        битая = вн[:хв] + вн[хв:].replace("2", "3", 1)
        assert судить(битая) == (True, False), битая
        # (2) ДОПОЛНЕНИЕ ПОСЧИТАНО СЛОЖЕНИЕМ
        сн = страница(язык, "сколько_не", n, k)
        assert судить(сн) == (True, True), сн
        битая = сн.replace("= 2.", "= 8.")
        assert судить(битая) == (True, False), битая
        мутанты += 2
        # (3) ЕСТЬ ЛИ: свидетель чужого числа
        е = страница(язык, "есть_да", n, k)
        assert судить(е) == (True, True), е
        хв = _хвост(е)
        битая = е[:хв] + е[хв:].replace("2", "4", 1)
        assert судить(битая) == (True, False), битая
        мутанты += 1
        # (4) НИ ОДНОГО и ВСЕ ДА — рамки дома, и их зачины объявлены
        ни = страница(язык, "ни_одного", n, k)
        assert судить(ни) == (True, True), ни
        вд = страница(язык, "все_да", 4, 4)
        assert судить(вд) == (True, True), вд
        for стр in (вн, сн, е, ни, вд):
            вопрос = стр[:стр.index("?") + 1].split(". ")[-1]
            assert asking.зачин_объявлен(вопрос) is not False, (язык, вопрос)
    for язык in ЯЗЫКИ:
        print("  ", страница(язык, "все_нет", 5, 3))
    for язык in ("ru", "en", "pl"):
        print("  ", страница(язык, "ни_одного", 7, 4))
        print("  ", страница(язык, "сколько_не", 9, 5))
        print("  ", страница(язык, "все_да", 4, 4))
    по_форме = {}
    for _, (язык, форма) in ПОКАЗЫ.items():
        по_форме[форма] = по_форме.get(форма, 0) + 1
    print(f"  мутантов поймано: {мутанты}")
    print(f"  дом пишет показов: {len(ПОКАЗЫ)} (языков {len(ЯЗЫКИ)}, форм {len(ФОРМЫ)}, образцов {len(ОБРАЗЦЫ)}): "
          + ", ".join(f"{ф} {к}" for ф, к in по_форме.items()))




import closedworld as _зк  # noqa: E402 — закон замкнутого мира читается после сборки показов
_СКЕЛЕТЫ_ЗНАКА = _зк.скелеты_знака(ПОКАЗЫ)


def судить(строка):
    """(судимо, истинно) — с ЗАКОНОМ ЗНАКА поверх образца.

    ЗНАК ДЕЙСТВИЯ СУДИТСЯ ЗАКОНОМ ЗАМКНУТОГО МИРА, А НЕ ДЫРОЙ В КАЖДОЙ РАМКЕ: строка,
    становящаяся ИСТИННОЙ при замене одного знака, есть строка ЭТОГО дома с испорченным
    знаком (М-489). Прежде такая строка получала НЕМОТУ, и палата брала истину у суда
    арифметики — у соседа (М-131).
    """
    вердикт = _судить_образцом(строка)
    if вердикт[0] is False and _зк.ложь_по_знаку(
            строка, _СКЕЛЕТЫ_ЗНАКА, ПОКАЗЫ, _судить_образцом):
        return True, False
    # СВЯЗКА ЕСТЬ ЗНАК СТРОКИ: подмена «jest»↔«są» делает страницу ЛОЖНОЙ, а не чужой
    if вердикт[0] is False and _зк.ложь_по_связке(строка, ПОКАЗЫ, _PL.ГРУППЫ_СВЯЗКИ):
        return True, False
    return вердикт
if __name__ == "__main__":
    _самопроверка()
