#!/usr/bin/env python3
"""THE HOUSE OF THE DATE — the carry whose base is NOT the same twice (06.09).

The census that found no clock and no mixed measure found no date either: ZERO lines carrying
«5 March» or «5 марта» with a day number. The corpus knows the names of the months and their
order (the calendar house) and it knows how to count days as a unit (the time-unit house), but
it never crosses from one month into the next — and that crossing is the only carry in the
whole corpus WHOSE BASE CHANGES: thirty-one days in March, thirty in April, twenty-eight in
February. A carry with a fixed base can be learnt as a habit; this one can only be learnt as a
law that ASKS THE MONTH how long it is.

THREE MOVEMENTS, AND THE MONTH'S LENGTH NAMED IN EVERY LEDGER.

    FORWARD. «28 March. six days later. what date will it be? 3 April: March has 31 days,
    28 + 6 = 34, 34 − 31 = 3.»

    BACKWARD. «3 April. six days earlier. what date was it? 28 March: March has 31 days,
    3 − 6 = −3, 31 − 3 = 28.»

    THE SPAN. «from 28 March to 3 April. how many days passed? 6 days: 31 − 28 = 3, 3 + 3 = 6.»

EVERY PAGE CROSSES THE MONTH, and February crosses with its own twenty-eight — the page that
teaches the base is not a constant.

A DECLARED GAP, NAMED AND NOT HIDDEN: GERMAN. German writes the day of a date with a full stop
(«5. März»), and a full stop followed by a space is the end of a sentence for every reader and
every court of this corpus. A house that wrote it would split its own pages in half; a house
that wrote «5 März» would write German wrongly. The gap is therefore declared here and waits
for a corpus-wide declaration of the date separator — the same way the pair house declares the
Russian gap of its unit form.

WHAT IS BORROWED: the counting rule of the packs (through the house of the pair) for «6 days»,
and the openers from the house of the pair. Declared here: six months with their lengths and
the form each language uses beside a day number.

WHAT IS NOT MEASURED, NAMED: a crossing of the year (December into January), a leap February,
and a span longer than one month.
"""
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import asking  # noqa: E402 — the house of the pair declares which openers a question may wear
import svampforms as S  # noqa: E402 — the count cell of a pack

# ЯЗЫКИ ДОМА — ВОСЕМЬ: немецкий объявлен пропуском (см. docstring и ПРОПУСК ниже)
ЯЗЫКИ = ("ru", "en", "fr", "es", "it", "pt", "nl", "pl")
ПРОПУСК = {"de": "число дня пишется точкой («5. März»), а точка есть конец предложения корпуса"}
# ШЕСТЬ МЕСЯЦЕВ И ИХ ДЛИНЫ — база переноса, которую надо СПРОСИТЬ У МЕСЯЦА
МЕСЯЦЫ = ("январь", "февраль", "март", "апрель", "май", "июнь")
ДЛИНЫ = {"январь": 31, "февраль": 28, "март": 31, "апрель": 30, "май": 31, "июнь": 30}
# ФОРМА МЕСЯЦА ПРИ ЧИСЛЕ ДНЯ — падеж пишется, а не выводится
ПРИ_ЧИСЛЕ = {
    "ru": dict(январь="января", февраль="февраля", март="марта", апрель="апреля", май="мая", июнь="июня"),
    "en": dict(январь="January", февраль="February", март="March", апрель="April", май="May", июнь="June"),
    "fr": dict(январь="janvier", февраль="février", март="mars", апрель="avril", май="mai", июнь="juin"),
    "es": dict(январь="de enero", февраль="de febrero", март="de marzo", апрель="de abril", май="de mayo", июнь="de junio"),
    "it": dict(январь="gennaio", февраль="febbraio", март="marzo", апрель="aprile", май="maggio", июнь="giugno"),
    "pt": dict(январь="de janeiro", февраль="de fevereiro", март="de março", апрель="de abril", май="de maio", июнь="de junho"),
    "nl": dict(январь="januari", февраль="februari", март="maart", апрель="april", май="mei", июнь="juni"),
    "pl": dict(январь="stycznia", февраль="lutego", март="marca", апрель="kwietnia", май="maja", июнь="czerwca"),
}
# ИМЯ МЕСЯЦА В ЛЕДЖЕРЕ («в марте 31 день») — своя форма, ибо падеж иной
В_МЕСЯЦЕ = {
    "ru": dict(январь="в январе", февраль="в феврале", март="в марте", апрель="в апреле", май="в мае", июнь="в июне"),
    "en": dict(январь="January has", февраль="February has", март="March has", апрель="April has", май="May has", июнь="June has"),
    "fr": dict(январь="janvier a", февраль="février a", март="mars a", апрель="avril a", май="mai a", июнь="juin a"),
    "es": dict(январь="enero tiene", февраль="febrero tiene", март="marzo tiene", апрель="abril tiene", май="mayo tiene", июнь="junio tiene"),
    "it": dict(январь="gennaio ha", февраль="febbraio ha", март="marzo ha", апрель="aprile ha", май="maggio ha", июнь="giugno ha"),
    "pt": dict(январь="janeiro tem", февраль="fevereiro tem", март="março tem", апрель="abril tem", май="maio tem", июнь="junho tem"),
    "nl": dict(январь="januari heeft", февраль="februari heeft", март="maart heeft", апрель="april heeft", май="mei heeft", июнь="juni heeft"),
    "pl": dict(январь="styczeń ma", февраль="luty ma", март="marzec ma", апрель="kwiecień ma", май="maj ma", июнь="czerwiec ma"),
}
ДЕНЬ = {
    "ru": ("день", "дня", "дней"), "en": ("day", "days"), "fr": ("jour", "jours"),
    "es": ("día", "días"), "it": ("giorno", "giorni"), "pt": ("dia", "dias"),
    "nl": ("dag", "dagen"), "pl": ("dzień", "dni", "dni"),
}
РЕЧЬ = {
    "ru": dict(дата="{D}.", вперёд="через {K}.", назад="{K} назад.",
               вопрос_вперёд="какое будет число?", вопрос_назад="какое было число?",
               промежуток="с {D} по {D2}.", вопрос_сколько="сколько дней прошло?",
               месяц="{М} {L} {LD}", двоеточие=": "),
    "en": dict(дата="{D}.", вперёд="{K} later.", назад="{K} earlier.",
               вопрос_вперёд="what date will it be?", вопрос_назад="what date was it?",
               промежуток="from {D} to {D2}.", вопрос_сколько="how many days passed?",
               месяц="{М} {L} {LD}", двоеточие=": "),
    "fr": dict(дата="{D}.", вперёд="{K} plus tard.", назад="{K} plus tôt.",
               вопрос_вперёд="quelle date sera-t-il ?", вопрос_назад="quelle date était-ce ?",
               промежуток="du {D} au {D2}.", вопрос_сколько="combien de jours se sont écoulés ?",
               месяц="{М} {L} {LD}", двоеточие=" : "),
    "es": dict(дата="{D}.", вперёд="{K} después.", назад="{K} antes.",
               вопрос_вперёд="¿qué fecha será?", вопрос_назад="¿qué fecha era?",
               промежуток="del {D} al {D2}.", вопрос_сколько="¿cuántos días pasaron?",
               месяц="{М} {L} {LD}", двоеточие=": "),
    "it": dict(дата="{D}.", вперёд="{K} dopo.", назад="{K} prima.",
               вопрос_вперёд="che data sarà?", вопрос_назад="che data era?",
               промежуток="dal {D} al {D2}.", вопрос_сколько="quanti giorni sono passati?",
               месяц="{М} {L} {LD}", двоеточие=": "),
    "pt": dict(дата="{D}.", вперёд="{K} depois.", назад="{K} antes.",
               вопрос_вперёд="que data será?", вопрос_назад="que data era?",
               промежуток="de {D} a {D2}.", вопрос_сколько="quantos dias passaram?",
               месяц="{М} {L} {LD}", двоеточие=": "),
    "nl": dict(дата="{D}.", вперёд="{K} later.", назад="{K} eerder.",
               вопрос_вперёд="welke datum wordt het?", вопрос_назад="welke datum was het?",
               промежуток="van {D} tot {D2}.", вопрос_сколько="hoeveel dagen zijn er verstreken?",
               месяц="{М} {L} {LD}", двоеточие=": "),
    "pl": dict(дата="{D}.", вперёд="{K} później.", назад="{K} wcześniej.",
               вопрос_вперёд="jaka będzie data?", вопрос_назад="jaka była data?",
               промежуток="od {D} do {D2}.", вопрос_сколько="ile dni minęło?",
               месяц="{М} {L} {LD}", двоеточие=": "),
}
ФОРМЫ = ("вперёд", "назад", "промежуток")
# ПЕРЕХОДЫ: (месяц, день, шаг) — день + шаг ВСЕГДА переваливает за конец месяца
ПЕРЕХОДЫ = (
    ("март", 28, 6), ("апрель", 27, 8), ("февраль", 26, 5), ("май", 29, 4), ("январь", 30, 3),
    ("июнь", 28, 7), ("март", 30, 9), ("февраль", 25, 11), ("апрель", 25, 12), ("май", 28, 6),
    ("январь", 27, 9), ("июнь", 26, 10), ("март", 27, 13), ("февраль", 24, 8), ("апрель", 29, 5),
    ("май", 30, 7), ("январь", 29, 6), ("июнь", 29, 4), ("март", 26, 14), ("февраль", 27, 6),
)


def _след(месяц):
    return МЕСЯЦЫ[(МЕСЯЦЫ.index(месяц) + 1) % len(МЕСЯЦЫ)]


def _день(язык, n):
    return "%d %s" % (n, S._счёт(ДЕНЬ[язык], n, язык))


def _дата(язык, месяц, д):
    return "%d %s" % (д, ПРИ_ЧИСЛЕ[язык][месяц])


def рамка(язык, форма, месяц):
    """The page: a date, a step across the month, and a ledger that ASKS THE MONTH its length."""
    р = РЕЧЬ[язык]
    длина = (р["месяц"].replace("{М}", В_МЕСЯЦЕ[язык][месяц])
             .replace("{L}", "{L}").replace("{LD}", "{LD}"))
    if форма == "вперёд":
        # ЛЕДЖЕР НАЗЫВАЕТ ДЛИНУ МЕСЯЦА: без неё перенос неотличим от переноса по десяти
        return (р["дата"].replace("{D}", "{D}") + " " + р["вперёд"] + " " + р["вопрос_вперёд"]
                + " {D2}" + р["двоеточие"] + длина + ", {d} + {k} = {s}, {s} − {L} = {d2}.")
    if форма == "назад":
        return (р["дата"].replace("{D}", "{D2}") + " " + р["назад"] + " " + р["вопрос_назад"]
                + " {D}" + р["двоеточие"] + длина + ", {L} − {d2} = {r}, {k} − {d2} = {r2}.")
    return (р["промежуток"] + " " + р["вопрос_сколько"] + " {K}" + р["двоеточие"]
            + длина + ", {L} − {d} = {r}, {r} + {d2} = {k}.")


def страница(язык, форма, месяц, д, шаг):
    длина = ДЛИНЫ[месяц]
    д2 = д + шаг - длина
    поля = dict(D=_дата(язык, месяц, д), D2=_дата(язык, _след(месяц), д2), K=_день(язык, шаг),
                L=длина, LD=S._счёт(ДЕНЬ[язык], длина, язык), d=д, d2=д2, k=шаг, s=д + шаг,
                r=длина - д, r2=шаг - д2)
    return рамка(язык, форма, месяц).format(**поля)


def _показы():
    вон = {}
    for язык in ЯЗЫКИ:
        for месяц, д, шаг in ПЕРЕХОДЫ:
            if д + шаг <= ДЛИНЫ[месяц] or д > ДЛИНЫ[месяц]:
                continue          # дом пишет лишь то, что ПЕРЕВАЛИВАЕТ за конец месяца
            for форма in ФОРМЫ:
                вон[страница(язык, форма, месяц, д, шаг)] = (язык, форма)
    return вон


ПОКАЗЫ = _показы()


def _альт(слова):
    return "(?:" + "|".join(re.escape(с) for с in sorted({с for с in слова if с}, key=lambda с: (-len(с), с))) + ")"


def _образец(язык, шаблон, месяц):
    дни = _альт(ДЕНЬ[язык])
    дыры = {"D": r"\d+ " + re.escape(ПРИ_ЧИСЛЕ[язык][месяц]),
            "D2": r"\d+ " + re.escape(ПРИ_ЧИСЛЕ[язык][_след(месяц)]),
            "K": r"\d+ " + дни,
            "L": r"\d+", "LD": дни, "d": r"\d+", "d2": r"\d+", "k": r"\d+", "s": r"\d+",
            "r": r"\d+", "r2": r"\d+"}
    счёт, куски = {}, []
    for кусок in re.split(r"(\{[^}]+\})", шаблон):
        if кусок.startswith("{"):
            дыра = кусок[1:-1]
            счёт[дыра] = счёт.get(дыра, 0) + 1
            куски.append(f"(?P<h_{дыра}__{счёт[дыра]}>{дыры[дыра]})")
        else:
            куски.append(re.escape(кусок))
    return re.compile("^" + "".join(куски) + "$")


ОБРАЗЦЫ = [(_образец(язык, рамка(язык, форма, месяц), месяц), язык, форма, месяц)
           for язык in ЯЗЫКИ for форма in ФОРМЫ for месяц in МЕСЯЦЫ]


def _значения(м):
    вон = {}
    for ключ, знач in м.groupdict().items():
        дыра, _ = ключ[2:].rsplit("__", 1)
        if дыра in вон and вон[дыра] != знач:
            return None
        вон[дыра] = знач
    return вон


def _число(текст):
    м = re.match(r"(\d+) ", текст)
    return int(м.group(1)) if м else None


def _вердикт(язык, форма, месяц, зн):
    # ЧИСЛО ДНЯ ЧИТАЕТСЯ ТАМ, ГДЕ ОНО СТОИТ: рамка обратного хода не несёт дыры «d» — день
    # исходной даты стоит в самой дате, и судья берёт его оттуда, а не падает (шрам 06.09:
    # суд рушился с KeyError на ПОРЧЕННОЙ странице, ибо истинные проходили списком показов и
    # до закона не доходили — падение суда есть немота, а немота хуже лжи)
    L, d2, k = int(зн["L"]), int(зн["d2"]), int(зн["k"])
    d = int(зн["d"]) if "d" in зн else _число(зн["D"])
    if d is None:
        return False
    # ДЛИНА МЕСЯЦА ОБЪЯВЛЕНА МЕСЯЦЕМ, А НЕ ПРИДУМАНА СТРАНИЦЕЙ
    if L != ДЛИНЫ[месяц] or зн.get("LD") != S._счёт(ДЕНЬ[язык], L, язык):
        return False
    if not (1 <= d <= L and 1 <= d2 and k >= 1):
        return False
    # ЧИСЛА ДАТ И ШАГА В ТЕКСТЕ СУТЬ ТЕ ЖЕ, ЧТО В ЛЕДЖЕРЕ
    if _число(зн["D"]) != d or _число(зн["D2"]) != d2 or _число(зн["K"]) != k:
        return False
    if зн["K"] != _день(язык, k):
        return False
    # ПЕРЕХОД ЕСТЬ ПЕРЕХОД: шаг обязан вынести за конец месяца, и число нового месяца сходится
    if d + k <= L or d + k - L != d2:
        return False
    if форма == "вперёд":
        return int(зн["s"]) == d + k
    if форма == "назад":
        return int(зн["r"]) == L - d2 and int(зн["r2"]) == k - d2
    return int(зн["r"]) == L - d and int(зн["r"]) + d2 == k


def судить(строка):
    """(судимо, истинно): a page of a frame of the house whose month crossing recomputes."""
    с = строка.strip()
    if с in ПОКАЗЫ:
        return True, True
    for образ, язык, форма, месяц in ОБРАЗЦЫ:
        м = образ.match(с)
        if not м:
            continue
        зн = _значения(м)
        if зн is None:
            return True, False
        return True, _вердикт(язык, форма, месяц, зн)
    return False, False


def _самопроверка():
    for показ in ПОКАЗЫ:
        assert судить(показ) == (True, True), показ
    мутанты = 0
    for язык in ЯЗЫКИ:
        месяц, д, шаг = "март", 28, 6
        п = страница(язык, "вперёд", месяц, д, шаг)
        assert судить(п) == (True, True), п
        # (1) ДЛИНА МЕСЯЦА ВЗЯТА ЧУЖАЯ (30 вместо 31) — перенос сдвигается на день
        битая = п.replace("31", "30")
        assert судить(битая) == (True, False), битая
        # (2) ЧИСЛО НОВОГО МЕСЯЦА НЕ СХОДИТСЯ
        битая = п.replace(_дата(язык, "апрель", 3), _дата(язык, "апрель", 4))
        assert судить(битая) == (True, False), битая
        мутанты += 2
        # (3) ФЕВРАЛЬ СЧИТАН КАК ТРИДЦАТИОДНОДНЕВНЫЙ
        ф = страница(язык, "вперёд", "февраль", 26, 5)
        assert судить(ф) == (True, True), ф
        битая = ф.replace("28", "31")
        assert судить(битая) == (True, False), битая
        мутанты += 1
        # (4) ОБРАТНЫЙ ХОД И ПРОМЕЖУТОК
        н = страница(язык, "назад", месяц, д, шаг)
        assert судить(н) == (True, True), н
        пр = страница(язык, "промежуток", месяц, д, шаг)
        assert судить(пр) == (True, True), пр
        битая = пр.replace(_день(язык, шаг), _день(язык, шаг + 1))
        assert судить(битая) == (True, False), битая
        мутанты += 1
        # (5) ЗАЧИН ВОПРОСА ОБЪЯВЛЕН ДОМОМ ПАРЫ
        for стр in (п, н, пр, ф):
            вопрос = стр[:стр.index("?") + 1].split(". ")[-1]
            assert asking.зачин_объявлен(вопрос) is not False, (язык, вопрос)
    for язык in ЯЗЫКИ:
        print("  ", страница(язык, "вперёд", "март", 28, 6))
    for язык in ("ru", "en", "pl"):
        print("  ", страница(язык, "назад", "февраль", 26, 5))
        print("  ", страница(язык, "промежуток", "апрель", 27, 8))
    по_форме = {}
    for _, (язык, форма) in ПОКАЗЫ.items():
        по_форме[форма] = по_форме.get(форма, 0) + 1
    print(f"  мутантов поймано: {мутанты}")
    print(f"  дом пишет показов: {len(ПОКАЗЫ)} (языков {len(ЯЗЫКИ)}, форм {len(ФОРМЫ)}, образцов {len(ОБРАЗЦЫ)}, "
          f"объявленный пропуск: {sorted(ПРОПУСК)}): " + ", ".join(f"{ф} {к}" for ф, к in по_форме.items()))


if __name__ == "__main__":
    _самопроверка()
