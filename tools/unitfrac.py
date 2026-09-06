#!/usr/bin/env python3
"""THE HOUSE OF THE NAMED FRACTION OF A UNIT — «полчаса» is a WORD and a COMPUTATION (06.09).

The census found ZERO lines carrying «полчаса», «half an hour», «четверть часа» or «quarter of
an hour» in the whole свод — and the house of speed had to declare the hole out loud when it
refused to show a fraction of an hour. Yet no everyday text lives without these words: they are
how the languages say a quantity that is not a whole number of units, and every one of them is
IRREGULAR — Russian welds the half into one word («полчаса», «полгода»), German inflects the
adjective by the unit's gender («eine halbe Stunde», «ein halber Meter», «ein halbes Jahr»),
Polish has a single word for the quarter-hour («kwadrans») and a special half-and-one form
(«półtorej godziny»), Dutch counts three quarter-hours as «drie kwartier».

WHAT THE HOUSE SHOWS — one law over FOUR BASES:
  вниз   — the named fraction asked in the smaller unit («полчаса — это сколько минут? 30 минут:
           60 ÷ 2 = 30»);
  вверх  — the same equality read from the number back to the word («45 минут — это три четверти
           часа»), so the naming is shown to be REVERSIBLE and not a one-way lookup;
  сумма  — the fraction entering arithmetic with a whole number of the smaller unit («полчаса и
           ещё 10 минут — это 40 минут: 30 + 10 = 40»), which is where a reader that only knows
           the word and not its number breaks.
The bases are the hour (60), the kilogram (1000), the metre (100) and the year (12) — four
DIFFERENT numbers under one law, so the law is seen as a law and not as a fact about sixty. The
hour carries all four fractions (a half, a quarter, three quarters, one and a half); the other
three carry the half, which is the fraction every language names with a word of its own.

WHAT IS BORROWED, NOT REDECLARED: the minute from the house of the clock, the gram and the
centimetre from the house of mixed measure, and the counting rule of the packs through the house
of the pair. Declared here: the month, and the fraction WORDS themselves — the one thing no
neighbour holds.

WHAT IS NOT MEASURED, NAMED: a fraction of a fraction, thirds (whose minutes are twenty but whose
grams are not whole), and the fraction written as a figure («0,5 часа») — that is the market of
the decimal notation.
"""
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import asking  # noqa: E402 — the house of the pair declares which openers a question may wear
import clockforms as CF  # noqa: E402 — the minute with its count forms
import mixedunits as MU  # noqa: E402 — the gram and the centimetre with their count forms
import svampforms as S  # noqa: E402 — the count cell of a pack

ЯЗЫКИ = ("ru", "en", "de", "fr", "es", "it", "pt", "nl", "pl")
# МЕСЯЦ — единственная малая единица, которой нет у соседей; прочие взяты, а не объявлены вновь
МЕСЯЦ = {"ru": ("месяц", "месяца", "месяцев"), "en": ("month", "months"),
         "de": ("Monat", "Monate"), "fr": ("mois", "mois"), "es": ("mes", "meses"),
         "it": ("mese", "mesi"), "pt": ("mês", "meses"), "nl": ("maand", "maanden"),
         "pl": ("miesiąc", "miesiące", "miesięcy")}
ОСНОВА = {"час": 60, "килограмм": 1000, "метр": 100, "год": 12}
МАЛАЯ = {"час": CF.МИНУТА, "килограмм": MU.МАЛАЯ["масса"], "метр": MU.МАЛАЯ["длина"], "год": МЕСЯЦ}
ЕДИНИЦЫ = ("час", "килограмм", "метр", "год")
# ДРОБЬ = (числитель, знаменатель); леджер у каждой свой, потому что счёт у каждой свой
ДРОБИ = {"половина": (1, 2), "четверть": (1, 4), "три_четверти": (3, 4), "полтора": (3, 2)}
# СЛОВА ДРОБИ — то единственное, чего нет ни у одного соседа: час несёт все четыре, прочие — половину
СЛОВА = {
    "ru": {"час": ("полчаса", "четверть часа", "три четверти часа", "полтора часа"),
           "килограмм": ("полкилограмма",), "метр": ("полметра",), "год": ("полгода",)},
    "en": {"час": ("half an hour", "a quarter of an hour", "three quarters of an hour",
                   "an hour and a half"),
           "килограмм": ("half a kilogram",), "метр": ("half a metre",), "год": ("half a year",)},
    "de": {"час": ("eine halbe Stunde", "eine Viertelstunde", "eine Dreiviertelstunde",
                   "anderthalb Stunden"),
           "килограмм": ("ein halbes Kilogramm",), "метр": ("ein halber Meter",),
           "год": ("ein halbes Jahr",)},
    "fr": {"час": ("une demi-heure", "un quart d'heure", "trois quarts d'heure",
                   "une heure et demie"),
           "килограмм": ("un demi-kilogramme",), "метр": ("un demi-mètre",),
           "год": ("une demi-année",)},
    "es": {"час": ("media hora", "un cuarto de hora", "tres cuartos de hora", "una hora y media"),
           "килограмм": ("medio kilogramo",), "метр": ("medio metro",), "год": ("medio año",)},
    "it": {"час": ("mezz'ora", "un quarto d'ora", "tre quarti d'ora", "un'ora e mezza"),
           "килограмм": ("mezzo chilogrammo",), "метр": ("mezzo metro",), "год": ("mezzo anno",)},
    "pt": {"час": ("meia hora", "um quarto de hora", "três quartos de hora", "uma hora e meia"),
           "килограмм": ("meio quilograma",), "метр": ("meio metro",), "год": ("meio ano",)},
    "nl": {"час": ("een half uur", "een kwartier", "drie kwartier", "anderhalf uur"),
           "килограмм": ("een half kilogram",), "метр": ("een halve meter",),
           "год": ("een half jaar",)},
    "pl": {"час": ("pół godziny", "kwadrans", "trzy kwadranse", "półtorej godziny"),
           "килограмм": ("pół kilograma",), "метр": ("pół metra",), "год": ("pół roku",)},
}
РЕЧЬ = {
    "ru": dict(вопрос="{Ф} — это сколько {МН}?", связка="{N} — это {Ф}",
               сумма="{Ф} и ещё {K} — это {S}", иначе="как иначе сказать {N}?", двоеточие=": "),
    "en": dict(вопрос="how many {МН} is {Ф}?", связка="{N} is {Ф}",
               сумма="{Ф} and another {K} is {S}", иначе="how else can you say {N}?", двоеточие=": "),
    "de": dict(вопрос="wie viele {МН} sind {Ф}?", связка="{N} sind {Ф}",
               сумма="{Ф} und noch {K} sind {S}", иначе="wie sagt man {N} anders?", двоеточие=": "),
    "fr": dict(вопрос="combien de {МН} fait {Ф} ?", связка="{N} font {Ф}",
               сумма="{Ф} et encore {K} font {S}", иначе="comment dire autrement {N} ?", двоеточие=" : "),
    "es": dict(вопрос="¿cuántos {МН} son {Ф}?", связка="{N} son {Ф}",
               сумма="{Ф} y {K} más son {S}", иначе="¿cómo se dice {N} de otra manera?", двоеточие=": "),
    "it": dict(вопрос="quanti {МН} sono {Ф}?", связка="{N} sono {Ф}",
               сумма="{Ф} e altri {K} sono {S}", иначе="come si dice altrimenti {N}?", двоеточие=": "),
    "pt": dict(вопрос="quantos {МН} são {Ф}?", связка="{N} são {Ф}",
               сумма="{Ф} e mais {K} são {S}", иначе="como se diz {N} de outra maneira?", двоеточие=": "),
    "nl": dict(вопрос="hoeveel {МН} is {Ф}?", связка="{N} is {Ф}",
               сумма="{Ф} en nog {K} is {S}", иначе="hoe zeg je {N} anders?", двоеточие=": "),
    "pl": dict(вопрос="ile {МН} to {Ф}?", связка="{N} to {Ф}",
               сумма="{Ф} i jeszcze {K} to {S}", иначе="jak inaczej powiedzieć {N}?", двоеточие=": "),
}
ФОРМЫ = ("вниз", "вверх", "сумма")
ПРИБАВКИ = (10, 20)


def дроби(единица):
    return list(ДРОБИ)[:4] if единица == "час" else ["половина"]


def _слово(язык, единица, дробь):
    return СЛОВА[язык][единица][list(ДРОБИ).index(дробь)]


def величина(единица, дробь):
    ч, з = ДРОБИ[дробь]
    return ОСНОВА[единица] * ч // з


def _счётно(язык, единица, n):
    """«30 минут», «30 minut» — счётное слово малой единицы берётся у соседа, а не объявляется."""
    return "%d %s" % (n, S._счёт(МАЛАЯ[единица][язык], n, язык))


def _множ(язык, единица):
    """The plural the question wears — «минут», «Minuten»: the count word of a big number."""
    return S._счёт(МАЛАЯ[единица][язык], 5, язык)


def леджер(единица, дробь):
    """The ledger of the fraction: the base divided, the quarter tripled, the half added back.

    ЗНАМЕНАТЕЛЬ СТОИТ ДЫРОЙ, А НЕ БУКВОЙ. Держать «÷ 2» буквой образца значит ослепнуть ровно
    на той лжи, ради которой дом поставлен: страница «ile miesięcy to pół roku? 6 miesięcy:
    12 ÷ 4 = 6» — половина, посчитанная как четверть, — не совпадала ни с одним образцом и
    получала МОЛЧАНИЕ, а немота хуже лжи. Ныне знаменатель и числитель судятся числом.
    """
    if дробь in ("половина", "четверть"):
        return "{C} ÷ {z} = {n}"
    if дробь == "три_четверти":
        return "{C} ÷ {z} × {ч} = {n}"
    return "{C} + {H} = {n}"


def рамка(язык, единица, дробь, форма):
    р = РЕЧЬ[язык]
    мн = _множ(язык, единица)
    if форма == "вниз":
        # ИМЯ ДРОБИ СПРОШЕНО ЧИСЛОМ МАЛОЙ ЕДИНИЦЫ
        return (р["вопрос"].replace("{МН}", мн) + " {N}" + р["двоеточие"]
                + леджер(единица, дробь) + ".")
    if форма == "вверх":
        # ЧИСЛО ПРОЧТЕНО ОБРАТНО ИМЕНЕМ — РАВЕНСТВО ОБРАТИМО, И СТРАНИЦА СПРАШИВАЕТ ОБ ЭТОМ
        return р["иначе"] + " {Ф}" + р["двоеточие"] + леджер(единица, дробь) + "."
    # ДРОБЬ ВХОДИТ В СЧЁТ НАРАВНЕ С ЦЕЛЫМ
    return р["сумма"] + р["двоеточие"] + "{n} + {k} = {s}."


def страница(язык, единица, дробь, форма, прибавка=0):
    n, C = величина(единица, дробь), ОСНОВА[единица]
    ч, з = ДРОБИ[дробь]
    зн = dict(Ф=_слово(язык, единица, дробь), N=_счётно(язык, единица, n), C=C, H=C // 2, n=n,
              z=з, ч=ч)
    if форма == "сумма":
        зн.update(K=_счётно(язык, единица, прибавка), S=_счётно(язык, единица, n + прибавка),
                  k=прибавка, s=n + прибавка)
    return рамка(язык, единица, дробь, форма).format(**зн)


def _показы():
    вон = {}
    for язык in ЯЗЫКИ:
        for единица in ЕДИНИЦЫ:
            for дробь in дроби(единица):
                for форма in ("вниз", "вверх"):
                    вон[страница(язык, единица, дробь, форма)] = (язык, форма)
                if единица == "час":
                    for прибавка in ПРИБАВКИ:
                        вон[страница(язык, единица, дробь, "сумма", прибавка)] = (язык, "сумма")
    return вон


ПОКАЗЫ = _показы()


def _альт(слова):
    сорт = sorted({с for с in слова if с}, key=lambda с: (-len(с), с))
    return "(?:" + "|".join(re.escape(с) for с in сорт) + ")"


def _дыры(язык, единица):
    счётные = r"\d+ " + _альт(f for е in ЕДИНИЦЫ for f in МАЛАЯ[е][язык])
    фразы = _альт(ф for е in ЕДИНИЦЫ for ф in СЛОВА[язык][е])
    return {"Ф": фразы, "N": счётные, "K": счётные, "S": счётные,
            "C": r"\d+", "H": r"\d+", "n": r"\d+", "k": r"\d+", "s": r"\d+",
            "z": r"\d+", "ч": r"\d+"}


def _образец(язык, единица, дробь, форма):
    дыры, счёт, куски = _дыры(язык, единица), {}, []
    for кусок in re.split(r"(\{[^}]+\})", рамка(язык, единица, дробь, форма)):
        if кусок.startswith("{"):
            дыра = кусок[1:-1]
            счёт[дыра] = счёт.get(дыра, 0) + 1
            куски.append(f"(?P<h_{дыра}__{счёт[дыра]}>{дыры[дыра]})")
        else:
            куски.append(re.escape(кусок))
    return re.compile("^" + "".join(куски) + "$")


ОБРАЗЦЫ = [(_образец(язык, единица, дробь, форма), язык, единица, дробь, форма)
           for язык in ЯЗЫКИ for единица in ЕДИНИЦЫ for дробь in дроби(единица)
           for форма in ФОРМЫ if not (форма == "сумма" and единица != "час")]


def _значения(м):
    вон = {}
    for ключ, знач in м.groupdict().items():
        дыра, _ = ключ[2:].rsplit("__", 1)
        if дыра in вон and вон[дыра] != знач:
            return None
        вон[дыра] = знач
    return вон


def _по_слову(язык, слово):
    """Which unit and which fraction this word names — the word is the key of the whole page."""
    for единица in ЕДИНИЦЫ:
        for дробь in дроби(единица):
            if _слово(язык, единица, дробь) == слово:
                return единица, дробь
    return None, None


def судить(строка):
    """(судимо, истинно): a page whose fraction word rebuilds it exactly; else silence."""
    с = строка.strip()
    if с in ПОКАЗЫ:
        return True, True
    for образ, язык, _единица, _дробь, форма in ОБРАЗЦЫ:
        м = образ.match(с)
        if not м:
            continue
        зн = _значения(м)
        if зн is None:
            return True, False
        единица, дробь = _по_слову(язык, зн["Ф"])
        if единица is None:
            return True, False
        # СЛОВО ДРОБИ ПЕРЕСТРАИВАЕТ СТРАНИЦУ — ЧИСЛО, СЧЁТНАЯ ФОРМА И ЛЕДЖЕР СРАЗУ
        прибавка = int(зн["k"]) if форма == "сумма" else 0
        if форма == "сумма" and прибавка < 1:
            return True, False
        return True, страница(язык, единица, дробь, форма, прибавка) == с
    return False, False


def _самопроверка():
    for показ in ПОКАЗЫ:
        assert судить(показ) == (True, True), показ
    мутанты = 0
    for язык in ЯЗЫКИ:
        н = страница(язык, "час", "половина", "вниз")
        assert судить(н) == (True, True), н
        # (1) ЧИСЛО ДРОБИ ПОДМЕНЕНО (счётная форма при нём — от чужого числа)
        битая = н.replace("= 30.", "= 20.").replace(_счётно(язык, "час", 30), _счётно(язык, "час", 20))
        assert судить(битая) == (True, False), битая
        # (2) ОСНОВА ПОДМЕНЕНА: делят не шестьдесят
        битая = н.replace("60 ÷ 2", "50 ÷ 2")
        assert судить(битая) == (True, False), битая
        # (3) СЛОВО ДРОБИ ЧУЖОЕ: четверть названа половиной часа
        ч = страница(язык, "час", "четверть", "вниз")
        битая = ч.replace(_слово(язык, "час", "четверть"), _слово(язык, "час", "половина"))
        assert судить(битая) == (True, False), битая
        # (4) ОБРАТНОЕ ЧТЕНИЕ ЛЖЁТ: число не той дроби
        в = страница(язык, "час", "три_четверти", "вверх")
        assert судить(в) == (True, True), в
        битая = в.replace(_счётно(язык, "час", 45), _счётно(язык, "час", 40)).replace("= 45.", "= 40.")
        assert судить(битая) == (True, False), битая
        # (5) СУММА СЛОЖЕНА НЕВЕРНО
        с = страница(язык, "час", "половина", "сумма", 10)
        assert судить(с) == (True, True), с
        битая = с.replace("30 + 10 = 40", "30 + 10 = 50").replace(_счётно(язык, "час", 40),
                                                                  _счётно(язык, "час", 50))
        assert судить(битая) == (True, False), битая
        # (6) ЧУЖАЯ ОСНОВА В ЧУЖОЙ ЕДИНИЦЕ: полкилограмма делят как час
        к = страница(язык, "килограмм", "половина", "вниз")
        assert судить(к) == (True, True), к
        битая = к.replace("1000 ÷ 2", "60 ÷ 2")
        assert судить(битая) == (True, False), битая
        мутанты += 6
        # (7) ЗАЧИН ВОПРОСА ОБЪЯВЛЕН ДОМОМ ПАРЫ
        вопрос = н[:н.index("?") + 1]
        assert asking.зачин_объявлен(вопрос) is not False, (язык, вопрос)
    for язык in ЯЗЫКИ:
        print("  ", страница(язык, "час", "четверть", "вниз"))
    for язык in ("ru", "de", "pl"):
        print("  ", страница(язык, "год", "половина", "вверх"))
        print("  ", страница(язык, "час", "полтора", "сумма", 20))
        print("  ", страница(язык, "метр", "половина", "вниз"))
    по_форме = {}
    for _, (_язык, форма) in ПОКАЗЫ.items():
        по_форме[форма] = по_форме.get(форма, 0) + 1
    print(f"  мутантов поймано: {мутанты}")
    print(f"  дом пишет показов: {len(ПОКАЗЫ)} (языков {len(ЯЗЫКИ)}, единиц {len(ЕДИНИЦЫ)}, "
          f"образцов {len(ОБРАЗЦЫ)}): " + ", ".join(f"{ф} {к}" for ф, к in по_форме.items()))


if __name__ == "__main__":
    _самопроверка()
