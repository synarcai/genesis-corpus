#!/usr/bin/env python3
"""THE HOUSE OF THE CLOCK — the carry that is sixty, not ten (06.09).

A census of the свод found ZERO lines carrying a time of day: no «9:15», no «11:45», nothing.
The corpus counts things, money, degrees and floors, and every one of those carries by TEN.
The clock carries by SIXTY, and an organism that has never seen the hour boundary crossed has
no reason to believe that fifty minutes plus twenty-five is one hour fifteen and not seventy-five
of anything.

WHAT THE HOUSE SHOWS. One journey and three questions over it, each the inverse of another:

    THE ARRIVAL. «the train left at 9:15. the journey takes 2 hours 30 minutes. when will it
    arrive? at 11:45: 9 hours 15 minutes + 2 hours 30 minutes = 11 hours 45 minutes.»

    THE DEPARTURE. The same journey read backwards: arrival minus duration.

    THE DURATION. Two times and the question how long — the difference, in hours and minutes.

EVERY PAGE CROSSES THE HOUR, and that is the point: a page whose minutes add to less than sixty
teaches nothing the ten-carry did not already teach, and the house does not write it. The
ledger is written in HOURS AND MINUTES, not in the clock's own colon: «9:15 + 2:30» is not an
equation of any arithmetic the corpus declares, while «9 hours 15 minutes + 2 hours 30 minutes
= 11 hours 45 minutes» is the claim itself, and its count forms bend by the pack's rule.

WHAT IS BORROWED: nine languages and the counting rule of the packs (through the house of the
pair), the openers from the house of the pair. Declared here: the words of hour and minute with
their count forms, the frames of a journey, and the way each language writes a time of day.

WHAT IS NOT MEASURED, NAMED: the twelve-hour clock with its am/pm (the corpus writes the
twenty-four-hour clock, as nine of nine languages do in writing), a journey crossing midnight,
and seconds.
"""
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import asking  # noqa: E402 — the house of the pair declares which openers a question may wear
import svampforms as S  # noqa: E402 — the count cell of a pack

ЯЗЫКИ = ("ru", "en", "de", "fr", "es", "it", "pt", "nl", "pl")
# ЧАС И МИНУТА СО СВОИМИ СЧЁТНЫМИ ФОРМАМИ — правило счёта берётся у пакета, а не пишется вновь
ЧАС = {
    "ru": ("час", "часа", "часов"), "en": ("hour", "hours"), "de": ("Stunde", "Stunden"),
    "fr": ("heure", "heures"), "es": ("hora", "horas"), "it": ("ora", "ore"),
    "pt": ("hora", "horas"), "nl": ("uur", "uur"), "pl": ("godzina", "godziny", "godzin"),
}
МИНУТА = {
    "ru": ("минута", "минуты", "минут"), "en": ("minute", "minutes"), "de": ("Minute", "Minuten"),
    "fr": ("minute", "minutes"), "es": ("minuto", "minutos"), "it": ("minuto", "minuti"),
    "pt": ("minuto", "minutos"), "nl": ("minuut", "minuten"), "pl": ("minuta", "minuty", "minut"),
}
# ПОЕЗДКИ: (час отправления, минута, часы пути, минуты пути) — минуты ВСЕГДА переваливают за час
ПОЕЗДКИ = (
    (9, 15, 2, 30), (7, 40, 1, 35), (10, 50, 2, 25), (6, 35, 3, 40), (8, 45, 1, 20),
    (11, 55, 2, 10), (5, 25, 4, 45), (13, 30, 1, 50), (14, 20, 2, 55), (16, 35, 1, 45),
    (12, 50, 3, 15), (15, 45, 2, 20), (17, 40, 1, 30), (18, 25, 2, 40), (19, 50, 1, 15),
    (20, 35, 1, 40), (6, 45, 2, 35), (7, 55, 1, 25), (8, 35, 3, 45), (9, 40, 2, 50),
    (10, 25, 1, 55), (11, 45, 2, 35), (12, 35, 1, 45), (13, 55, 2, 15), (14, 50, 1, 35),
    (15, 25, 3, 50), (16, 45, 1, 40), (17, 55, 2, 30), (5, 50, 4, 25), (6, 25, 2, 45),
    (7, 35, 3, 40), (8, 55, 1, 50), (9, 25, 2, 55), (10, 45, 3, 30), (11, 35, 1, 55),
    (13, 45, 2, 45), (14, 25, 1, 50), (16, 55, 2, 25), (18, 45, 1, 30), (19, 35, 2, 40),
)
РЕЧЬ = {
    "ru": dict(выехал="поезд выехал в {T}.", идёт="он идёт {D}.", приедет="поезд приедет в {T2}.",
               вопрос_приедет="когда он приедет?", вопрос_выехал="когда он выехал?",
               оба="поезд выехал в {T} и приехал в {T2}.", вопрос_сколько="сколько он ехал?",
               ответ_время="в {T2}", ответ_время_назад="в {T}", двоеточие=": "),
    "en": dict(выехал="the train left at {T}.", идёт="the journey takes {D}.",
               приедет="the train arrives at {T2}.",
               вопрос_приедет="when will it arrive?", вопрос_выехал="when did it leave?",
               оба="the train left at {T} and arrived at {T2}.", вопрос_сколько="how long did it travel?",
               ответ_время="at {T2}", ответ_время_назад="at {T}", двоеточие=": "),
    "de": dict(выехал="der Zug fuhr um {T} ab.", идёт="die Fahrt dauert {D}.",
               приедет="der Zug kommt um {T2} an.",
               вопрос_приедет="wann kommt er an?", вопрос_выехал="wann ist er abgefahren?",
               оба="der Zug fuhr um {T} ab und kam um {T2} an.", вопрос_сколько="wie lange fuhr er?",
               ответ_время="um {T2}", ответ_время_назад="um {T}", двоеточие=": "),
    "fr": dict(выехал="le train est parti à {T}.", идёт="le trajet dure {D}.",
               приедет="le train arrive à {T2}.",
               вопрос_приедет="quand arrive-t-il ?", вопрос_выехал="quand est-il parti ?",
               оба="le train est parti à {T} et est arrivé à {T2}.",
               вопрос_сколько="combien de temps a-t-il roulé ?",
               ответ_время="à {T2}", ответ_время_назад="à {T}", двоеточие=" : "),
    "es": dict(выехал="el tren salió a las {T}.", идёт="el viaje dura {D}.",
               приедет="el tren llega a las {T2}.",
               вопрос_приедет="¿cuándo llega?", вопрос_выехал="¿cuándo salió?",
               оба="el tren salió a las {T} y llegó a las {T2}.", вопрос_сколько="¿cuánto tiempo viajó?",
               ответ_время="a las {T2}", ответ_время_назад="a las {T}", двоеточие=": "),
    "it": dict(выехал="il treno è partito alle {T}.", идёт="il viaggio dura {D}.",
               приедет="il treno arriva alle {T2}.",
               вопрос_приедет="quando arriva?", вопрос_выехал="quando è partito?",
               оба="il treno è partito alle {T} ed è arrivato alle {T2}.",
               вопрос_сколько="quanto tempo ha viaggiato?",
               ответ_время="alle {T2}", ответ_время_назад="alle {T}", двоеточие=": "),
    "pt": dict(выехал="o comboio partiu às {T}.", идёт="a viagem dura {D}.",
               приедет="o comboio chega às {T2}.",
               вопрос_приедет="quando chega?", вопрос_выехал="quando partiu?",
               оба="o comboio partiu às {T} e chegou às {T2}.", вопрос_сколько="quanto tempo viajou?",
               ответ_время="às {T2}", ответ_время_назад="às {T}", двоеточие=": "),
    "nl": dict(выехал="de trein vertrok om {T}.", идёт="de reis duurt {D}.",
               приедет="de trein komt om {T2} aan.",
               вопрос_приедет="wanneer komt hij aan?", вопрос_выехал="wanneer is hij vertrokken?",
               оба="de trein vertrok om {T} en kwam om {T2} aan.", вопрос_сколько="hoe lang reed hij?",
               ответ_время="om {T2}", ответ_время_назад="om {T}", двоеточие=": "),
    "pl": dict(выехал="pociąg odjechał o {T}.", идёт="podróż trwa {D}.",
               приедет="pociąg przyjeżdża o {T2}.",
               вопрос_приедет="kiedy przyjedzie?", вопрос_выехал="kiedy odjechał?",
               оба="pociąg odjechał o {T} i przyjechał o {T2}.", вопрос_сколько="jak długo jechał?",
               ответ_время="o {T2}", ответ_время_назад="o {T}", двоеточие=": "),
}
ФОРМЫ = ("прибытие", "отправление", "длительность")


def _счёт(язык, таблица, n):
    return S._счёт(таблица[язык], n, язык)


def _время(ч, м):
    """«9:15» — двадцатичетырёхчасовые часы, как их пишут все девять языков."""
    return "%d:%02d" % (ч, м)


def _длительность(язык, ч, м):
    """«2 часа 30 минут» — счётные формы часа и минуты по правилу пакета."""
    куски = []
    if ч:
        куски.append("%d %s" % (ч, _счёт(язык, ЧАС, ч)))
    if м:
        куски.append("%d %s" % (м, _счёт(язык, МИНУТА, м)))
    return " ".join(куски)


def рамка(язык, форма):
    р = РЕЧЬ[язык]
    if форма == "прибытие":
        # ЛЕДЖЕР ПИШЕТСЯ ЧАСАМИ И МИНУТАМИ, А НЕ ДВОЕТОЧИЕМ ЧАСОВ: «9:15 + 2:30» не есть
        # равенство никакой объявленной корпусом арифметики, а «9 часов 15 минут + 2 часа
        # 30 минут = 11 часов 45 минут» есть само утверждение, и его формы гнёт правило пакета
        return (р["выехал"] + " " + р["идёт"] + " " + р["вопрос_приедет"] + " "
                + р["ответ_время"] + р["двоеточие"] + "{Dt} + {D} = {Dt2}.")
    if форма == "отправление":
        return (р["приедет"] + " " + р["идёт"] + " " + р["вопрос_выехал"] + " "
                + р["ответ_время_назад"] + р["двоеточие"] + "{Dt2} − {D} = {Dt}.")
    return (р["оба"] + " " + р["вопрос_сколько"] + " " + "{D}" + р["двоеточие"]
            + "{Dt2} − {Dt} = {D}.")


def страница(язык, форма, ч, м, дч, дм):
    всего = (ч * 60 + м) + (дч * 60 + дм)
    ч2, м2 = divmod(всего, 60)
    поля = dict(T=_время(ч, м), T2=_время(ч2, м2), D=_длительность(язык, дч, дм),
                Dt=_длительность(язык, ч, м), Dt2=_длительность(язык, ч2, м2))
    return рамка(язык, форма).format(**поля)


def _показы():
    вон = {}
    for язык in ЯЗЫКИ:
        for ч, м, дч, дм in ПОЕЗДКИ:
            if м + дм < 60 or ч * 60 + м + дч * 60 + дм >= 24 * 60:
                continue          # дом пишет лишь то, что ПЕРЕВАЛИВАЕТ за час и не за полночь
            for форма in ФОРМЫ:
                вон[страница(язык, форма, ч, м, дч, дм)] = (язык, форма)
    return вон


ПОКАЗЫ = _показы()


def _альт(слова):
    return "(?:" + "|".join(re.escape(с) for с in sorted({с for с in слова if с}, key=lambda с: (-len(с), с))) + ")"


def _образец(язык, шаблон):
    часы = _альт(ЧАС[язык])
    минуты = _альт(МИНУТА[язык])
    длит = r"(?:\d+ " + часы + r" )?\d+ " + минуты + r"|\d+ " + часы
    дыры = {"T": r"\d+:\d\d", "T2": r"\d+:\d\d", "D": длит, "Dt": длит, "Dt2": длит}
    счёт, куски = {}, []
    for кусок in re.split(r"(\{[^}]+\})", шаблон):
        if кусок.startswith("{"):
            дыра = кусок[1:-1]
            счёт[дыра] = счёт.get(дыра, 0) + 1
            куски.append(f"(?P<h_{дыра}__{счёт[дыра]}>{дыры[дыра]})")
        else:
            куски.append(re.escape(кусок))
    return re.compile("^" + "".join(куски) + "$")


ОБРАЗЦЫ = [(_образец(язык, рамка(язык, форма)), язык, форма)
           for язык in ЯЗЫКИ for форма in ФОРМЫ]


def _значения(м):
    вон = {}
    for ключ, знач in м.groupdict().items():
        дыра, _ = ключ[2:].rsplit("__", 1)
        if дыра in вон and вон[дыра] != знач:
            return None
        вон[дыра] = знач
    return вон


def _минуты(язык, текст):
    """Часы и минуты длительности обратно в минуты; None, если формы не по правилу пакета."""
    ч = м = 0
    for число, слово in re.findall(r"(\d+) (\S+)", текст):
        n = int(число)
        if слово == _счёт(язык, ЧАС, n):
            ч = n
        elif слово == _счёт(язык, МИНУТА, n):
            м = n
        else:
            return None
    return ч * 60 + м


def _чч(текст):
    """Минуты от полуночи; None, если на циферблате не время. МИНУТА ЦИФЕРБЛАТА МЕНЬШЕ
    ШЕСТИДЕСЯТИ, и это не придирка: «12:75» и «13:15» суть одно число минут, и судья,
    считающий одни минуты, назвал бы «12:75» истиной — ровно тот перенос по десяти, ради
    которого дом и написан."""
    ч, м = текст.split(":")
    if not (0 <= int(м) < 60 and 0 <= int(ч) < 24):
        return None
    return int(ч) * 60 + int(м)


def _вердикт(язык, форма, зн):
    t, t2 = _чч(зн["T"]), _чч(зн["T2"])
    d = _минуты(язык, зн["D"])
    dt, dt2 = _минуты(язык, зн["Dt"]), _минуты(язык, зн["Dt2"])
    if None in (t, t2, d, dt, dt2) or d < 1:
        return False
    # ЧАСЫ И МИНУТЫ ЛЕДЖЕРА ЕСТЬ ТО ЖЕ ВРЕМЯ, ЧТО НА ЦИФЕРБЛАТЕ
    if dt != t or dt2 != t2:
        return False
    # ПЕРЕНОС ЕСТЬ ШЕСТЬДЕСЯТ: минуты складываются с переходом через час, и час обязан вырасти
    if t + d != t2:
        return False
    if (t % 60) + (d % 60) < 60:
        return False
    return t2 < 24 * 60


def судить(строка):
    """(судимо, истинно): a page of a frame of the house whose clock adds up; else silence."""
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
        # ПОЕЗДКА, ПЕРЕВАЛИВАЮЩАЯ ЗА ЧАС: 50 + 25 = 75 минут, то есть час пятнадцать
        ч, м, дч, дм = 10, 50, 2, 25
        час11, час12, час13 = (_счёт(язык, ЧАС, n) for n in (11, 12, 13))
        п = страница(язык, "прибытие", ч, м, дч, дм)
        assert судить(п) == (True, True), п
        # (1) ПЕРЕНОС СЧИТАН ПО ДЕСЯТИ: «12:75» вместо «13:15»
        битая = п.replace("13:15", "12:75")
        assert судить(битая) == (True, False), битая
        # (2) ПРИБЫТИЕ НА ЧАС РАНЬШЕ — и циферблат, и леджер согласны между собой, но сумма нет
        битая = п.replace("13:15", "12:15").replace("13 " + час13, "12 " + час12)
        assert судить(битая) == (True, False), битая
        # (3) ЛЕДЖЕР РАЗОШЁЛСЯ С ЦИФЕРБЛАТОМ
        битая = п.replace("13 " + час13, "12 " + час12)
        assert судить(битая) == (True, False), битая
        # (4) ОБРАТНЫЙ ХОД: отправление посчитано сложением
        о = страница(язык, "отправление", ч, м, дч, дм)
        assert судить(о) == (True, True), о
        часы_ = _счёт(язык, ЧАС, ч)
        битая = о.replace("10:50", "15:50").replace("10 " + часы_, "15 " + _счёт(язык, ЧАС, 15))
        assert судить(битая) == (True, False), битая
        # (5) ДЛИТЕЛЬНОСТЬ: разность взята без переноса
        д = страница(язык, "длительность", ч, м, дч, дм)
        assert судить(д) == (True, True), д
        мин25, мин35 = _счёт(язык, МИНУТА, 25), _счёт(язык, МИНУТА, 35)
        битая = д.replace("25 " + мин25, "35 " + мин35)
        assert судить(битая) == (True, False), битая
        мутанты += 5
        # (6) ЗАЧИН ВОПРОСА ОБЪЯВЛЕН ДОМОМ ПАРЫ
        for стр in (п, о, д):
            вопрос = стр[:стр.index("?") + 1].split(". ")[-1]
            assert asking.зачин_объявлен(вопрос) is not False, (язык, вопрос)
    for язык in ЯЗЫКИ:
        print("  ", страница(язык, "прибытие", 10, 50, 2, 25))
    for язык in ("ru", "en", "pl"):
        print("  ", страница(язык, "отправление", 7, 40, 1, 35))
        print("  ", страница(язык, "длительность", 6, 35, 3, 40))
    по_форме = {}
    for _, (язык, форма) in ПОКАЗЫ.items():
        по_форме[форма] = по_форме.get(форма, 0) + 1
    print(f"  мутантов поймано: {мутанты}")
    print(f"  дом пишет показов: {len(ПОКАЗЫ)} (языков {len(ЯЗЫКИ)}, форм {len(ФОРМЫ)}, образцов {len(ОБРАЗЦЫ)}): "
          + ", ".join(f"{ф} {к}" for ф, к in по_форме.items()))


if __name__ == "__main__":
    _самопроверка()
