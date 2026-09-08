#!/usr/bin/env python3
"""THE HOUSE OF THE MIXED MEASURE — the carry that is a thousand, and the one that is a hundred (06.09).

The census that found no clock in the свод found no mixed measure either: ZERO lines carrying
«2 kg 300 g» or «2 m 30 cm». The corpus converts units (the units house) and counts things, but
it never shows the everyday shape where a measure is written in TWO units at once and the
smaller one overflows into the greater. The clock house showed the carry of sixty; this one
shows the carry of a thousand (gram into kilogram) and of a hundred (centimetre into metre),
so that the carry is bought as a LAW WITH A BASE and not as a habit of ten.

FOUR MOVEMENTS, TWO OF THEM BORROWING. Adding into the greater unit («2 kg 300 g + 1 kg 800 g
= 4 kg 100 g» — the grams overflow and the kilogram grows) and taking away out of it («4 kg
100 g − 1 kg 800 g = 2 kg 300 g» — the grams do not suffice and the kilogram is broken), and
the same pair over metres and centimetres.

EVERY PAGE CROSSES THE UNIT, and the house writes no other: a sum whose grams stay under a
thousand teaches nothing the plain addition of the corpus did not already teach.

WHAT IS BORROWED: nine languages and the counting rule of the packs (through the house of the
pair), the openers from the house of the pair. Declared here: the four units with their count
forms and the frames of a bag and a rope.

WHAT IS NOT MEASURED, NAMED: three units at once (kg, g and mg), a measure written as a
decimal («2.3 kg» — that is the notation house's), and any base but a thousand and a hundred.
"""
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import asking  # noqa: E402 — the house of the pair declares which openers a question may wear
import svampforms as S  # noqa: E402 — the count cell of a pack

ЯЗЫКИ = ("ru", "en", "de", "fr", "es", "it", "pt", "nl", "pl")
ОСНОВЫ = {"масса": 1000, "длина": 100}
БОЛЬШАЯ = {
    "масса": {"ru": ("килограмм", "килограмма", "килограммов"), "en": ("kilogram", "kilograms"),
              "de": ("Kilogramm", "Kilogramm"), "fr": ("kilogramme", "kilogrammes"),
              "es": ("kilogramo", "kilogramos"), "it": ("chilogrammo", "chilogrammi"),
              "pt": ("quilograma", "quilogramas"), "nl": ("kilogram", "kilogram"),
              "pl": ("kilogram", "kilogramy", "kilogramów")},
    "длина": {"ru": ("метр", "метра", "метров"), "en": ("metre", "metres"),
              "de": ("Meter", "Meter"), "fr": ("mètre", "mètres"),
              "es": ("metro", "metros"), "it": ("metro", "metri"),
              "pt": ("metro", "metros"), "nl": ("meter", "meter"),
              "pl": ("metr", "metry", "metrów")},
}
МАЛАЯ = {
    "масса": {"ru": ("грамм", "грамма", "граммов"), "en": ("gram", "grams"),
              "de": ("Gramm", "Gramm"), "fr": ("gramme", "grammes"),
              "es": ("gramo", "gramos"), "it": ("grammo", "grammi"),
              "pt": ("grama", "gramas"), "nl": ("gram", "gram"),
              "pl": ("gram", "gramy", "gramów")},
    "длина": {"ru": ("сантиметр", "сантиметра", "сантиметров"), "en": ("centimetre", "centimetres"),
              "de": ("Zentimeter", "Zentimeter"), "fr": ("centimètre", "centimètres"),
              "es": ("centímetro", "centímetros"), "it": ("centimetro", "centimetri"),
              "pt": ("centímetro", "centímetros"), "nl": ("centimeter", "centimeter"),
              "pl": ("centymetr", "centymetry", "centymetrów")},
}
# ПАРЫ (большая, малая) для каждого слагаемого: малые ВСЕГДА переваливают через основание
МАССЫ = ((2, 300, 1, 800), (3, 450, 2, 700), (1, 250, 3, 900), (4, 600, 1, 550),
         (2, 850, 2, 350), (5, 720, 1, 480), (3, 150, 4, 950), (6, 480, 2, 640),
         (1, 900, 5, 250), (7, 350, 1, 800), (2, 640, 3, 470), (4, 780, 2, 390),
         (3, 520, 2, 660), (5, 940, 1, 130), (2, 470, 4, 750), (6, 810, 1, 290),
         (1, 360, 7, 880), (4, 250, 3, 790), (8, 630, 2, 520), (3, 940, 5, 170),
         (2, 580, 6, 460), (7, 720, 1, 350), (5, 190, 4, 930), (9, 460, 1, 640),
         # ЕДИНИЦА МЕЛКОЙ МЕРЫ — ПОКАЗ, А НЕ КРАЙНИЙ СЛУЧАЙ (08.09). Мера «единственное при
         # единице» держала «gram» в долгу: 322 «grams» и ни одного «1 gram». Обе пары
         # соблюдают закон дома — страница ОБЯЗАНА переходить через меру:
         #
         #     (2, 999, 1, 2)  сложение: 999 + 2 = 1001 — граммы переполняются, и в ответе
         #                     стои́т «4 килограмма 1 грамм»;
         #     (4, 1, 1, 800)  вычитание: 1 < 800 — граммов не хватает, килограмм ломается,
         #                     и «1 грамм» стои́т в первом слагаемом.
         (2, 999, 1, 2), (4, 1, 1, 800))
ДЛИНЫ = ((2, 30, 1, 85), (3, 45, 2, 70), (1, 25, 3, 90), (4, 60, 1, 55),
         (2, 85, 2, 35), (5, 72, 1, 48), (3, 15, 4, 95), (6, 48, 2, 64),
         (1, 90, 5, 25), (7, 35, 1, 80), (2, 64, 3, 47), (4, 78, 2, 39),
        (3, 52, 2, 66), (5, 94, 1, 13), (2, 47, 4, 75), (6, 81, 1, 29),
        (1, 36, 7, 88), (4, 25, 3, 79), (8, 63, 2, 52), (3, 94, 5, 17),
        (2, 58, 6, 46), (7, 72, 1, 35), (5, 19, 4, 93), (9, 46, 1, 64))
РЕЧЬ = {
    "ru": dict(масса_есть="мешок весит {A}.", масса_добавили="в него добавили {B}.",
               масса_вопрос="сколько весит мешок?", масса_было="мешок весил {V}.",
               масса_взяли="из него взяли {B}.", масса_вопрос2="сколько весит мешок теперь?",
               длина_есть="верёвка длиной {A}.", длина_добавили="к ней привязали {B}.",
               длина_вопрос="сколько стало?", длина_было="верёвка была длиной {V}.",
               длина_отрезали="от неё отрезали {B}.", длина_вопрос2="сколько осталось?",
               двоеточие=": "),
    "en": dict(масса_есть="the bag weighs {A}.", масса_добавили="{B} was added to it.",
               масса_вопрос="how much does the bag weigh?", масса_было="the bag weighed {V}.",
               масса_взяли="{B} was taken out of it.", масса_вопрос2="how much does the bag weigh now?",
               длина_есть="the rope is {A} long.", длина_добавили="{B} was tied to it.",
               длина_вопрос="how long is it now?", длина_было="the rope was {V} long.",
               длина_отрезали="{B} was cut off it.", длина_вопрос2="how much is left?",
               двоеточие=": "),
    "de": dict(масса_есть="der Sack wiegt {A}.", масса_добавили="{B} wurden hineingegeben.",
               масса_вопрос="wie viel wiegt der Sack?", масса_было="der Sack wog {V}.",
               масса_взяли="{B} wurden herausgenommen.", масса_вопрос2="wie viel wiegt der Sack jetzt?",
               длина_есть="das Seil ist {A} lang.", длина_добавили="{B} wurden angeknüpft.",
               длина_вопрос="wie lang ist es jetzt?", длина_было="das Seil war {V} lang.",
               длина_отрезали="{B} wurden abgeschnitten.", длина_вопрос2="wie viel bleibt übrig?",
               двоеточие=": "),
    "fr": dict(масса_есть="le sac pèse {A}.", масса_добавили="on y a ajouté {B}.",
               масса_вопрос="combien pèse le sac ?", масса_было="le sac pesait {V}.",
               масса_взяли="on en a retiré {B}.", масса_вопрос2="combien pèse le sac maintenant ?",
               длина_есть="la corde mesure {A}.", длина_добавили="on y a attaché {B}.",
               длина_вопрос="quelle est la longueur maintenant ?", длина_было="la corde mesurait {V}.",
               длина_отрезали="on en a coupé {B}.", длина_вопрос2="combien reste-t-il ?",
               двоеточие=" : "),
    "es": dict(масса_есть="el saco pesa {A}.", масса_добавили="se le añadieron {B}.",
               масса_вопрос="¿cuánto pesa el saco?", масса_было="el saco pesaba {V}.",
               масса_взяли="se le sacaron {B}.", масса_вопрос2="¿cuánto pesa el saco ahora?",
               длина_есть="la cuerda mide {A}.", длина_добавили="se le ataron {B}.",
               длина_вопрос="¿cuánto mide ahora?", длина_было="la cuerda medía {V}.",
               длина_отрезали="se le cortaron {B}.", длина_вопрос2="¿cuánto queda?",
               двоеточие=": "),
    "it": dict(масса_есть="il sacco pesa {A}.", масса_добавили="ci sono stati aggiunti {B}.",
               масса_вопрос="quanto pesa il sacco?", масса_было="il sacco pesava {V}.",
               масса_взяли="ne sono stati tolti {B}.", масса_вопрос2="quanto pesa il sacco adesso?",
               длина_есть="la corda è lunga {A}.", длина_добавили="ci sono stati legati {B}.",
               длина_вопрос="quanto è lungo adesso?", длина_было="la corda era lunga {V}.",
               длина_отрезали="ne sono stati tagliati {B}.", длина_вопрос2="quanto resta?",
               двоеточие=": "),
    "pt": dict(масса_есть="o saco pesa {A}.", масса_добавили="foram acrescentados {B}.",
               масса_вопрос="quanto pesa o saco?", масса_было="o saco pesava {V}.",
               масса_взяли="foram retirados {B}.", масса_вопрос2="quanto pesa o saco agora?",
               длина_есть="a corda mede {A}.", длина_добавили="foram atados {B}.",
               длина_вопрос="que comprimento tem agora?", длина_было="a corda media {V}.",
               длина_отрезали="foram cortados {B}.", длина_вопрос2="quanto resta?",
               двоеточие=": "),
    "nl": dict(масса_есть="de zak weegt {A}.", масса_добавили="er werd {B} bij gedaan.",
               масса_вопрос="hoeveel weegt de zak?", масса_было="de zak woog {V}.",
               масса_взяли="er werd {B} uit gehaald.", масса_вопрос2="hoeveel weegt de zak nu?",
               длина_есть="het touw is {A} lang.", длина_добавили="er werd {B} aan geknoopt.",
               длина_вопрос="hoe lang is het nu?", длина_было="het touw was {V} lang.",
               длина_отрезали="er werd {B} afgeknipt.", длина_вопрос2="hoeveel blijft er over?",
               двоеточие=": "),
    "pl": dict(масса_есть="worek waży {A}.", масса_добавили="dodano do niego {B}.",
               масса_вопрос="ile waży worek?", масса_было="worek ważył {V}.",
               масса_взяли="wyjęto z niego {B}.", масса_вопрос2="ile waży worek teraz?",
               длина_есть="lina ma długość {A}.", длина_добавили="doczepiono do niej {B}.",
               длина_вопрос="ile jest teraz?", длина_было="lina miała długość {V}.",
               длина_отрезали="odcięto od niej {B}.", длина_вопрос2="ile zostało?",
               двоеточие=": "),
}
ФОРМЫ = ("масса_плюс", "масса_минус", "длина_плюс", "длина_минус")
РОД = {"масса_плюс": "масса", "масса_минус": "масса", "длина_плюс": "длина", "длина_минус": "длина"}


def _счёт(язык, таблица, n):
    return S._счёт(таблица[язык], n, язык)


def _мера(язык, род, б, м):
    """«2 кг 300 г» пишется словами: счётная форма каждой единицы по правилу пакета."""
    куски = []
    if б:
        куски.append("%d %s" % (б, _счёт(язык, БОЛЬШАЯ[род], б)))
    if м:
        куски.append("%d %s" % (м, _счёт(язык, МАЛАЯ[род], м)))
    return " ".join(куски)


def рамка(язык, форма):
    р = РЕЧЬ[язык]
    род = РОД[форма]
    if форма.endswith("_плюс"):
        return (р[род + "_есть"] + " " + р[род + "_добавили"] + " " + р[род + "_вопрос"] + " "
                + "{V}" + р["двоеточие"] + "{A} + {B} = {V}.")
    ключ_вопроса = род + ("_вопрос2" if род == "масса" else "_вопрос2")
    return (р[род + "_было"] + " " + р[род + ("_взяли" if род == "масса" else "_отрезали")] + " "
            + р[ключ_вопроса] + " " + "{A}" + р["двоеточие"] + "{V} − {B} = {A}.")


def страница(язык, форма, б1, м1, б2, м2):
    род = РОД[форма]
    осн = ОСНОВЫ[род]
    всего = (б1 * осн + м1) + (б2 * осн + м2)
    бv, мv = divmod(всего, осн)
    поля = dict(A=_мера(язык, род, б1, м1), B=_мера(язык, род, б2, м2),
                V=_мера(язык, род, бv, мv))
    return рамка(язык, форма).format(**поля)


def _показы():
    вон = {}
    for язык in ЯЗЫКИ:
        for б1, м1, б2, м2 in МАССЫ:
            if м1 + м2 < ОСНОВЫ["масса"]:
                continue          # дом пишет лишь то, что ПЕРЕВАЛИВАЕТ через единицу
            вон[страница(язык, "масса_плюс", б1, м1, б2, м2)] = (язык, "масса_плюс")
            вон[страница(язык, "масса_минус", б1, м1, б2, м2)] = (язык, "масса_минус")
        for б1, м1, б2, м2 in ДЛИНЫ:
            if м1 + м2 < ОСНОВЫ["длина"]:
                continue
            вон[страница(язык, "длина_плюс", б1, м1, б2, м2)] = (язык, "длина_плюс")
            вон[страница(язык, "длина_минус", б1, м1, б2, м2)] = (язык, "длина_минус")
    return вон


ПОКАЗЫ = _показы()


def _альт(слова):
    return "(?:" + "|".join(re.escape(с) for с in sorted({с for с in слова if с}, key=lambda с: (-len(с), с))) + ")"


def _образец(язык, шаблон, род):
    б = _альт(БОЛЬШАЯ[род][язык])
    м = _альт(МАЛАЯ[род][язык])
    мера = r"(?:\d+ " + б + r" )?\d+ " + м + r"|\d+ " + б
    дыры = {"A": мера, "B": мера, "V": мера}
    счёт, куски = {}, []
    for кусок in re.split(r"(\{[^}]+\})", шаблон):
        if кусок.startswith("{"):
            дыра = кусок[1:-1]
            счёт[дыра] = счёт.get(дыра, 0) + 1
            куски.append(f"(?P<h_{дыра}__{счёт[дыра]}>{дыры[дыра]})")
        else:
            куски.append(re.escape(кусок))
    return re.compile("^" + "".join(куски) + "$")


ОБРАЗЦЫ = [(_образец(язык, рамка(язык, форма), РОД[форма]), язык, форма)
           for язык in ЯЗЫКИ for форма in ФОРМЫ]


def _значения(м):
    вон = {}
    for ключ, знач in м.groupdict().items():
        дыра, _ = ключ[2:].rsplit("__", 1)
        if дыра in вон and вон[дыра] != знач:
            return None
        вон[дыра] = знач
    return вон


def _в_малых(язык, род, текст):
    """Мера словами обратно в малые единицы; None, если формы не по правилу пакета."""
    б = м = 0
    for число, слово in re.findall(r"(\d+) (\S+)", текст):
        n = int(число)
        if слово == _счёт(язык, БОЛЬШАЯ[род], n):
            б = n
        elif слово == _счёт(язык, МАЛАЯ[род], n):
            м = n
        else:
            return None
    # МАЛАЯ ЕДИНИЦА МЕНЬШЕ СВОЕГО ОСНОВАНИЯ: «4 кг 1100 г» не есть мера, а есть перенос,
    # не сделанный до конца — ровно та ложь, ради которой дом написан
    if м >= ОСНОВЫ[род]:
        return None
    return б * ОСНОВЫ[род] + м


def _вердикт(язык, форма, зн):
    род = РОД[форма]
    a, b, v = (_в_малых(язык, род, зн[к]) for к in ("A", "B", "V"))
    if None in (a, b, v) or min(a, b) < 1:
        return False
    if a + b != v:
        return False
    # ПЕРЕНОС ЧЕРЕЗ ЕДИНИЦУ ЕСТЬ ПРЕДМЕТ ДОМА: сумма малых обязана перевалить основание
    return (a % ОСНОВЫ[род]) + (b % ОСНОВЫ[род]) >= ОСНОВЫ[род]


def судить(строка):
    """(судимо, истинно): a page of a frame of the house whose measure carries; else silence."""
    с = строка.strip()
    if с in ПОКАЗЫ:
        return True, True
    for образ, язык, форма in ОБРАЗЦЫ:
        м = образ.match(с)
        if not м:
            continue
        зн = _значения(м)
        if зн is None:
            return True, False
        return True, _вердикт(язык, форма, зн)
    return False, False


def _самопроверка():
    for показ in ПОКАЗЫ:
        assert судить(показ) == (True, True), показ
    мутанты = 0
    for язык in ЯЗЫКИ:
        б1, м1, б2, м2 = 2, 300, 1, 800
        п = страница(язык, "масса_плюс", б1, м1, б2, м2)
        assert судить(п) == (True, True), п
        # (1) ПЕРЕНОС НЕ СДЕЛАН: «3 кг 1100 г» вместо «4 кг 100 г»
        битая = п.replace(_мера(язык, "масса", 4, 100), _мера(язык, "масса", 3, 1100))
        assert судить(битая) == (True, False), битая
        # (2) СУММА НЕ СХОДИТСЯ
        битая = п.replace(_мера(язык, "масса", 4, 100), _мера(язык, "масса", 4, 200))
        assert судить(битая) == (True, False), битая
        мутанты += 2
        # (3) ЗАЁМ НЕ СДЕЛАН: вычитание считано по большой единице отдельно от малой
        м_ = страница(язык, "масса_минус", б1, м1, б2, м2)
        assert судить(м_) == (True, True), м_
        битая = м_.replace(_мера(язык, "масса", 2, 300), _мера(язык, "масса", 3, 300))
        assert судить(битая) == (True, False), битая
        мутанты += 1
        # (4) ДЛИНА: перенос через сто
        д = страница(язык, "длина_плюс", 2, 30, 1, 85)
        assert судить(д) == (True, True), д
        битая = д.replace(_мера(язык, "длина", 4, 15), _мера(язык, "длина", 3, 115))
        assert судить(битая) == (True, False), битая
        мутанты += 1
        # (5) ЗАЧИН ВОПРОСА ОБЪЯВЛЕН ДОМОМ ПАРЫ
        for стр in (п, м_, д):
            вопрос = стр[:стр.index("?") + 1].split(". ")[-1]
            assert asking.зачин_объявлен(вопрос) is not False, (язык, вопрос)
    for язык in ЯЗЫКИ:
        print("  ", страница(язык, "масса_плюс", 2, 300, 1, 800))
    for язык in ("ru", "en", "pl"):
        print("  ", страница(язык, "масса_минус", 2, 300, 1, 800))
        print("  ", страница(язык, "длина_плюс", 2, 30, 1, 85))
    по_форме = {}
    for _, (язык, форма) in ПОКАЗЫ.items():
        по_форме[форма] = по_форме.get(форма, 0) + 1
    print(f"  мутантов поймано: {мутанты}")
    print(f"  дом пишет показов: {len(ПОКАЗЫ)} (языков {len(ЯЗЫКИ)}, форм {len(ФОРМЫ)}, образцов {len(ОБРАЗЦЫ)}): "
          + ", ".join(f"{ф} {к}" for ф, к in по_форме.items()))


if __name__ == "__main__":
    _самопроверка()
