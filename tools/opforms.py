#!/usr/bin/env python3
"""THE HOUSE OF THE OPERATOR WORD IN AN ORDER — «divide 14 by 2. what do you get? 7.» (05.09).

A NAMED DEFECT, MEASURED ON THE HELD-OUT KEY. The reader answered «divide 14 em 2 partes
iguais. o que dá?» with 28 — it multiplied. The diagnosis is holon's and it is a diagnosis of
the CORPUS, not of the reader: the school shows the operator word only BETWEEN its numbers
(«12 divide 2 = 6»), and the frame «{verb} {N} {prep} {N}» — the word standing BEFORE both
numbers, in an order, with the operands separated by a preposition — was never bought. A
question whose whole content is an echo («what do you get?») then carries no operation at
all: everything the answer needs stands in the imperative sentence before it.

WHAT THIS HOUSE SHOWS, AND WHY EACH PART IS THERE.

    THE ORDER OF OPERANDS IS THE PREPOSITION'S, NOT THE READING ORDER. «subtract 2 from 9»
    is 9 − 2 and «divide 14 by 2» is 14 ÷ 2, while «add 3 and 4» is symmetric. The house
    shows all five operations in nine languages, each with the preposition its language
    uses, and the judge recomputes by the preposition — so a page that reads the numbers
    left to right is a lie the court names.

    THE WORD AND THE SIGN ARE ONE KEY. Half the pages answer bare («7.»), half answer with
    the ledger («7: 14 ÷ 2 = 7.»), the same numbers in both — the word of the order and the
    sign of the equation meet on one page, which is the whole purchase.

    AN ORDER WITH ONE NUMBER IS ANSWERED BY NOT KNOWING. «divide 14. what do you get?» has
    no second operand, and the page says so with the pair house's OWN word of not-knowing —
    derived from that house, never declared twice — over a ground declared here. The court
    also carries a frame the world never writes: the same one-number order answered by a
    NUMBER. It is a lie by construction, and it is the trap for any reader that guesses.

WHAT IS BORROWED: nine languages and the surface «divide {n} into {k} equal parts» from the
house of the number line (asserted equal, not copied), the word of not-knowing from the
house of the pair, and every question opener stands declared there too.

WHAT IS NOT MEASURED, NAMED: an order with three operands, an order whose result is not
whole (division here always divides), and the imperative of a story («take 5 apples») —
that is the house of the tool, and it moves a state instead of naming a number.
"""
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import asking  # noqa: E402 — the house of the pair declares which openers a question may wear
import numberline as NL  # noqa: E402 — the surface «divide {n} into {k} equal parts»
import svampforms as S  # noqa: E402 — the pair house's own word of not-knowing

ЯЗЫКИ = ("ru", "en", "de", "fr", "es", "it", "pt", "nl", "pl")
ЗНАКИ = {"сложи": "+", "вычти": "−", "умножь": "×", "раздели": "÷", "поровну": "÷"}
ДЕЙСТВИЯ = ("сложи", "вычти", "умножь", "раздели", "поровну")

# ПОВЕЛЕНИЕ — ГЛАГОЛ ПЕРЕД ОБОИМИ ЧИСЛАМИ, И ПОРЯДОК ОПЕРАНДОВ ЗАДАЁТ ПРЕДЛОГ.
# «{a}» — первый операнд действия, «{b}» — второй; «subtract {b} from {a}» есть a − b.
ПОВЕЛЕНИЯ = {
    "ru": dict(сложи="сложи {a} и {b}", вычти="вычти {b} из {a}", умножь="умножь {a} на {b}",
               раздели="раздели {a} на {b}", поровну="раздели {a} на {b} равные части"),
    "en": dict(сложи="add {a} and {b}", вычти="subtract {b} from {a}", умножь="multiply {a} by {b}",
               раздели="divide {a} by {b}", поровну="divide {a} into {b} equal parts"),
    "de": dict(сложи="addiere {a} und {b}", вычти="subtrahiere {b} von {a}", умножь="multipliziere {a} mit {b}",
               раздели="teile {a} durch {b}", поровну="teile {a} in {b} gleiche Teile"),
    "fr": dict(сложи="additionne {a} et {b}", вычти="soustrais {b} de {a}", умножь="multiplie {a} par {b}",
               раздели="divise {a} par {b}", поровну="divise {a} en {b} parts égales"),
    "es": dict(сложи="suma {a} y {b}", вычти="resta {b} de {a}", умножь="multiplica {a} por {b}",
               раздели="divide {a} entre {b}", поровну="divide {a} en {b} partes iguales"),
    "it": dict(сложи="somma {a} e {b}", вычти="sottrai {b} da {a}", умножь="moltiplica {a} per {b}",
               раздели="dividi {a} per {b}", поровну="dividi {a} in {b} parti uguali"),
    "pt": dict(сложи="soma {a} e {b}", вычти="subtrai {b} de {a}", умножь="multiplica {a} por {b}",
               раздели="divide {a} por {b}", поровну="divide {a} em {b} partes iguais"),
    "nl": dict(сложи="tel {a} en {b} op", вычти="trek {b} van {a} af", умножь="vermenigvuldig {a} met {b}",
               раздели="deel {a} door {b}", поровну="verdeel {a} in {b} gelijke delen"),
    "pl": dict(сложи="dodaj {a} i {b}", вычти="odejmij {b} od {a}", умножь="pomnóż {a} przez {b}",
               раздели="podziel {a} przez {b}", поровну="podziel {a} na {b} równe części"),
}
# ПОВЕРХНОСТЬ «ПОРОВНУ» НЕ ОБЪЯВЛЯЕТСЯ ДВАЖДЫ, А ВЫВОДИТСЯ У ДОМА ЧИСЛОВОГО РЯДА: этот
# дом добавляет к ней вопрос-эхо, а слова остаются одни — «share {n} equally between {k}»,
# «раздели {n} на {k} поровну», «divide {n} em {k} partes iguais».
for _яз in ЯЗЫКИ:
    ПОВЕЛЕНИЯ[_яз]["поровну"] = (NL.ЯЗЫКИ[_яз]["поровну"][0].rstrip(".")
                                 .replace("{n}", "{a}").replace("{k}", "{b}"))
    assert "{a}" in ПОВЕЛЕНИЯ[_яз]["поровну"] and "{b}" in ПОВЕЛЕНИЯ[_яз]["поровну"], _яз

# ПОВЕЛЕНИЕ ОДНОГО ЧИСЛА — та же голова, второй операнд не назван.
ОДНО_ЧИСЛО = {
    "ru": dict(сложи="сложи {a}", вычти="вычти {a}", умножь="умножь {a}", раздели="раздели {a}",
               поровну="раздели {a} поровну"),
    "en": dict(сложи="add {a}", вычти="subtract {a}", умножь="multiply {a}", раздели="divide {a}",
               поровну="share {a} equally"),
    "de": dict(сложи="addiere {a}", вычти="subtrahiere {a}", умножь="multipliziere {a}", раздели="teile {a}",
               поровну="teile {a} gleichmäßig"),
    "fr": dict(сложи="additionne {a}", вычти="soustrais {a}", умножь="multiplie {a}", раздели="divise {a}",
               поровну="partage {a} en parts égales"),
    "es": dict(сложи="suma {a}", вычти="resta {a}", умножь="multiplica {a}", раздели="divide {a}",
               поровну="reparte {a} en partes iguales"),
    "it": dict(сложи="somma {a}", вычти="sottrai {a}", умножь="moltiplica {a}", раздели="dividi {a}",
               поровну="dividi {a} in parti uguali"),
    "pt": dict(сложи="soma {a}", вычти="subtrai {a}", умножь="multiplica {a}", раздели="divide {a}",
               поровну="divide {a} em partes iguais"),
    "nl": dict(сложи="tel {a} op", вычти="trek {a} af", умножь="vermenigvuldig {a}", раздели="deel {a}",
               поровну="verdeel {a} gelijk"),
    "pl": dict(сложи="dodaj {a}", вычти="odejmij {a}", умножь="pomnóż {a}", раздели="podziel {a}",
               поровну="podziel {a} na równe części"),
}
# ВОПРОС-ЭХО — две поверхности на язык: весь его смысл в том, что он НЕ несёт операции.
ВОПРОСЫ = {
    "ru": ("что получится?", "сколько получится?"),
    "en": ("what do you get?", "what is the result?"),
    "de": ("was kommt heraus?", "wie viel kommt heraus?"),
    "fr": ("qu'est-ce que ça donne ?", "combien cela fait-il ?"),
    "es": ("¿qué da?", "¿cuánto da?"),
    "it": ("quanto fa?", "quanto viene?"),
    "pt": ("o que dá?", "quanto dá?"),
    "nl": ("wat krijg je?", "hoeveel krijg je?"),
    "pl": ("ile wychodzi?", "ile to jest?"),
}
# ОСНОВАНИЕ ОТКАЗА — голова его берётся у дома пары (см. _голова_отказа), здесь только основание.
ОСНОВАНИЕ = {
    "ru": "второе число не сказано", "en": "the second number is not said",
    "de": "die zweite Zahl ist nicht gesagt", "fr": "le second nombre n'est pas dit",
    "es": "no se dice el segundo número", "it": "il secondo numero non è detto",
    "pt": "o segundo número não é dito", "nl": "het tweede getal is niet gezegd",
    "pl": "nie powiedziano drugiej liczby",
}
ДВОЕТОЧИЕ = {язык: (" : " if язык == "fr" else ": ") for язык in ЯЗЫКИ}
# СЛОВО ОПЕРАТОРА ИНФИКСОМ — вторая позиция того же слова, и глиф рядом связывает слово с
# таблицей: «divide 14 by 2. what do you get? 7: 14 divided by 2 = 7, 14 ÷ 2 = 7.» Одна
# страница покупает слово ПЕРЕД числами и МЕЖДУ ними одним ключом (просьба holon, 05.09).
ИНФИКС = {
    "ru": ("плюс", "минус", "умножить на", "разделить на"),
    "en": ("plus", "minus", "times", "divided by"),
    "de": ("plus", "minus", "mal", "geteilt durch"),
    "fr": ("plus", "moins", "fois", "divisé par"),
    "es": ("más", "menos", "por", "dividido por"),
    "it": ("più", "meno", "per", "diviso"),
    "pt": ("mais", "menos", "vezes", "dividido por"),
    "nl": ("plus", "min", "keer", "gedeeld door"),
    "pl": ("plus", "minus", "razy", "podzielone przez"),
}
ПОРЯДОК_ИНФИКСА = {"сложи": 0, "вычти": 1, "умножь": 2, "раздели": 3, "поровну": 3}
# СВЯЗКА ШКОЛЬНОГО СЧЁТА — «14 divided by 2 IS 7». Инфиксная строка пишется СВЯЗКОЙ, а не
# знаком равенства, и это не украшение: суд поспешности берёт плечо равенства ПРОБЕГОМ от
# «=» и останавливается на первой букве, так что «7 plus 8 = 15» дало бы ему плечо «8»
# против 15 и честную строку он звал бы ложью (замер 05.09: 47 строк польского мира). Знак
# равенства на странице всё равно стоит — во второй, глифовой половине ответа, где плечо
# чисто, — и слово оператора связывается со знаком через ОДНО ЗНАЧЕНИЕ, а не через «=».
СВЯЗКА_СЧЁТА = {"ru": "будет", "en": "is", "de": "ist", "fr": "fait", "es": "es",
                "it": "fa", "pt": "é", "nl": "is", "pl": "to"}
ФОРМЫ = ("повеление", "повеление_леджер", "повеление_инфикс", "отказ")


def _голова_отказа(язык):
    """The pair house's OWN word of not-knowing, read out of its refusal — never declared twice."""
    хвост = S.РАМКИ[язык]["без_данных"].split("?", 1)[1]
    return хвост.split(":", 1)[0].strip()


ГОЛОВА = {язык: _голова_отказа(язык) for язык in ЯЗЫКИ}
for _яз in ЯЗЫКИ:
    assert ГОЛОВА[_яз] and len(ГОЛОВА[_яз]) > 2, (_яз, "the pair house lost its word of not-knowing")

# ПАРЫ ЧИСЕЛ — своя дорожка на действие: вычитание не уходит ниже нуля, деление делит нацело.
ПАРЫ = {
    "сложи": ((3, 4), (5, 6), (7, 8), (9, 12), (11, 15), (13, 6), (17, 4), (21, 9), (25, 14), (30, 7)),
    "вычти": ((9, 2), (14, 5), (20, 7), (18, 9), (25, 11), (30, 13), (16, 4), (22, 8), (27, 19), (12, 3)),
    "умножь": ((6, 7), (3, 8), (4, 9), (5, 6), (7, 3), (8, 4), (9, 5), (12, 3), (11, 4), (6, 6)),
    "раздели": ((14, 2), (18, 3), (24, 4), (35, 5), (36, 6), (28, 7), (40, 8), (45, 9), (30, 5), (48, 6)),
    "поровну": ((12, 3), (20, 4), (30, 6), (16, 2), (27, 3), (42, 7), (25, 5), (32, 4), (54, 9), (21, 7)),
}


for _д, _пары in ПАРЫ.items():
    if _д in ("вычти", "раздели", "поровну"):
        for _a, _b in _пары:
            assert _a != _b, (_д, _a, _b, "a symmetric pair witnesses no order")

def _счёт(действие, a, b):
    if действие == "сложи":
        return a + b
    if действие == "вычти":
        return a - b
    if действие == "умножь":
        return a * b
    return a // b if b and a % b == 0 else None


def рамка(язык, форма, действие, в):
    """The page's template: the order, the echo question and the answer of the house."""
    вопрос = ВОПРОСЫ[язык][в]
    if форма == "отказ":
        приказ = ОДНО_ЧИСЛО[язык][действие] + "."
        ответ = ГОЛОВА[язык] + ДВОЕТОЧИЕ[язык] + ОСНОВАНИЕ[язык] + "."
        return приказ + " " + вопрос + " " + ответ
    приказ = ПОВЕЛЕНИЯ[язык][действие] + "."
    if форма == "повеление":
        ответ = "{r}."
    elif форма == "повеление_инфикс":
        # ТО ЖЕ СЛОВО МЕЖДУ ЧИСЛАМИ, А ГЛИФ РЯДОМ: слово покупается в обеих позициях одним
        # ключом, и таблица знаков привязывается к слову значением, а не соседством
        слово = ИНФИКС[язык][ПОРЯДОК_ИНФИКСА[действие]]
        ответ = ("{r}" + ДВОЕТОЧИЕ[язык] + "{a} " + слово + " {b} " + СВЯЗКА_СЧЁТА[язык]
                 + " {r}, " + "{a} " + ЗНАКИ[действие] + " {b} = {r}.")
    else:
        # СЛОВО ПОРЯДКА И ЗНАК РАВЕНСТВА НА ОДНОЙ СТРАНИЦЕ — это и есть покупка
        ответ = "{r}" + ДВОЕТОЧИЕ[язык] + "{a} " + ЗНАКИ[действие] + " {b} = {r}."
    return приказ + " " + вопрос + " " + ответ


# РАМКА СУДА, КОТОРУЮ МИР НЕ ПИШЕТ: приказ одного числа, отвеченный ЧИСЛОМ. Ложь по
# построению — второго операнда нет, и никакое число не верно.
def рамка_ложного_отказа(язык, действие, в):
    return ОДНО_ЧИСЛО[язык][действие] + ". " + ВОПРОСЫ[язык][в] + " {r}."


def страница(язык, форма, действие, в, a, b=None):
    r = _счёт(действие, a, b) if b is not None else None
    т = рамка(язык, форма, действие, в)
    return т.format(a=a, b=b, r=r)


def _показы():
    вон = {}
    for язык in ЯЗЫКИ:
        for действие in ДЕЙСТВИЯ:
            for i, (a, b) in enumerate(ПАРЫ[действие]):
                assert _счёт(действие, a, b) is not None, (действие, a, b)
                for в in (0, 1):
                    вон[страница(язык, "повеление", действие, в, a, b)] = (язык, "повеление")
                    вон[страница(язык, "повеление_леджер", действие, в, a, b)] = (язык, "повеление_леджер")
                    вон[страница(язык, "повеление_инфикс", действие, в, a, b)] = (язык, "повеление_инфикс")
                # ОТКАЗ ПОКАЗЫВАЕТСЯ РЕЖЕ ПРИКАЗА: он есть край рынка, а не его середина
                if i % 3 == 0:
                    вон[страница(язык, "отказ", действие, i % 2, a)] = (язык, "отказ")
    return вон


ПОКАЗЫ = _показы()


def _образец(шаблон):
    """One pattern over the whole page; the i-th occurrence of a hole is «h_<hole>__i»."""
    дыры = {"a": r"\d+", "b": r"\d+", "r": r"\d+"}
    счёт, куски = {}, []
    for кусок in re.split(r"(\{[^}]+\})", шаблон):
        if кусок.startswith("{"):
            дыра = кусок[1:-1]
            счёт[дыра] = счёт.get(дыра, 0) + 1
            куски.append(f"(?P<h_{дыра}__{счёт[дыра]}>{дыры[дыра]})")
        else:
            куски.append(re.escape(кусок))
    return re.compile("^" + "".join(куски) + "$")


def _все_рамки():
    вон = []
    for язык in ЯЗЫКИ:
        for действие in ДЕЙСТВИЯ:
            for в in (0, 1):
                for форма in ФОРМЫ:
                    вон.append((_образец(рамка(язык, форма, действие, в)), язык, форма, действие))
                вон.append((_образец(рамка_ложного_отказа(язык, действие, в)), язык, "отказ_числом", действие))
    return вон


ОБРАЗЦЫ = _все_рамки()


def _значения(м):
    вон = {}
    for ключ, знач in м.groupdict().items():
        дыра, _ = ключ[2:].rsplit("__", 1)
        if дыра in вон and вон[дыра] != знач:
            return None
        вон[дыра] = знач
    return вон


def _вердикт(форма, действие, зн):
    if форма == "отказ":
        return True                     # ни одного числа: отказ и есть весь ответ
    if форма == "отказ_числом":
        return False                    # приказ одного числа, отвеченный числом, — ложь всегда
    a, b, r = int(зн["a"]), int(зн["b"]), int(зн["r"])
    if b < 1 or a < 1:
        return False
    # ПОРЯДОК ОПЕРАНДОВ — ПРЕДЛОГА, А НЕ ЧТЕНИЯ: «subtract 2 from 9» есть 9 − 2
    свой = _счёт(действие, a, b)
    return свой is not None and свой == r


def судить(строка):
    """(судимо, истинно): a page of a frame of the house whose order recomputes; else silence."""
    с = строка.strip()
    if с in ПОКАЗЫ:
        return True, True
    for образ, язык, форма, действие in ОБРАЗЦЫ:
        м = образ.match(с)
        if not м:
            continue
        зн = _значения(м)
        if зн is None:
            return True, False
        return True, _вердикт(форма, действие, зн)
    return False, False


def _самопроверка():
    for показ in ПОКАЗЫ:
        assert судить(показ) == (True, True), показ
    мутанты = 0
    for язык in ЯЗЫКИ:
        for действие in ДЕЙСТВИЯ:
            a, b = ПАРЫ[действие][0]
            верно = _счёт(действие, a, b)
            п = страница(язык, "повеление", действие, 0, a, b)
            assert судить(п) == (True, True), п
            # (1) ЧУЖОЙ ОТВЕТ
            битая = п.replace("? %d." % верно, "? %d." % (верно + 1))
            assert судить(битая) == (True, False), битая
            мутанты += 1
            # (2) СЛОВО ПОРЯДКА ПРОЧИТАНО КАК ДРУГОЕ ДЕЙСТВИЕ — ровно замеренный дефект:
            # «divide 14 em 2 partes iguais. o que dá?» читатель отвечал 28, то есть умножил
            чужое = a * b if действие in ("сложи", "раздели", "поровну") else a + b
            if чужое != верно:
                битая = п.replace("? %d." % верно, "? %d." % чужое)
                assert судить(битая) == (True, False), битая
                мутанты += 1
            # (3) ЛЕДЖЕР НЕ СХОДИТСЯ С ОТВЕТОМ
            л = страница(язык, "повеление_леджер", действие, 1, a, b)
            assert судить(л) == (True, True), л
            битая = л[:л.rindex("= ")] + "= %d." % (верно + 2)
            assert судить(битая) == (True, False), битая
            мутанты += 1
            # (3b) ИНФИКС: СЛОВО МЕЖДУ ЧИСЛАМИ И ГЛИФ РЯДОМ — оба обязаны дать один ответ
            и = страница(язык, "повеление_инфикс", действие, 0, a, b)
            assert судить(и) == (True, True), и
            битая = и[:и.rindex("= ")] + "= %d." % (верно + 3)
            assert судить(битая) == (True, False), битая
            мутанты += 1
            # (4) ПРИКАЗ ОДНОГО ЧИСЛА, ОТВЕЧЕННЫЙ ЧИСЛОМ
            о = страница(язык, "отказ", действие, 0, a)
            assert судить(о) == (True, True), о
            битая = рамка_ложного_отказа(язык, действие, 0).format(a=a, r=a)
            assert судить(битая) == (True, False), битая
            мутанты += 1
            # (5) ЗАЧИН ВОПРОСА ОБЪЯВЛЕН ДОМОМ ПАРЫ
            for стр in (п, л, и, о):
                вопрос = стр[:стр.index("?") + 1].split(". ")[-1]
                assert asking.зачин_объявлен(вопрос) is not False, (язык, вопрос)
    for язык in ЯЗЫКИ:
        print("  ", страница(язык, "повеление", "поровну", 0, 12, 3))
    for язык, действие in (("en", "вычти"), ("ru", "умножь"), ("de", "раздели"), ("pl", "сложи")):
        print("  ", страница(язык, "повеление_леджер", действие, 1, *ПАРЫ[действие][1]))
    for язык, действие in (("es", "поровну"), ("it", "раздели"), ("pt", "вычти"), ("nl", "умножь"), ("fr", "сложи")):
        print("  ", страница(язык, "повеление_инфикс", действие, 0, *ПАРЫ[действие][0]))
    for язык in ("pt", "fr", "nl"):
        print("  ", страница(язык, "отказ", "раздели", 0, 14))
    по_форме = {}
    for _, (язык, форма) in ПОКАЗЫ.items():
        по_форме[форма] = по_форме.get(форма, 0) + 1
    print(f"  мутантов поймано: {мутанты}")
    print(f"  дом пишет показов: {len(ПОКАЗЫ)} (языков {len(ЯЗЫКИ)}, форм {len(ФОРМЫ)}, образцов {len(ОБРАЗЦЫ)}): "
          + ", ".join(f"{ф} {к}" for ф, к in по_форме.items()))


if __name__ == "__main__":
    _самопроверка()
