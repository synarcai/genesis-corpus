#!/usr/bin/env python3
"""THE HOUR SAID IN WORDS — one time, and nine ways to divide it (06.09).

The census that found no clock in the свод found no spoken clock either: ZERO lines with «half
past two» or «половина третьего». The house of the clock buys the arithmetic of the hour; this
one buys its NAME — and the name is where the nine languages disagree about the same minute.

    THE SAME 2:30 IS «HALF PAST TWO» AND «HALF OF THE THIRD». English, French, Spanish,
    Italian and Portuguese count from the hour that has passed; Russian, German, Dutch and
    Polish count toward the hour that is coming: «half past two» against «половина третьего»,
    «halb drei», «half drie», «wpół do trzeciej». A corpus that showed only one of the two
    would teach an organism that the clock is named one way and the other way is an error.

    THE QUARTER SPLITS THE SAME WAY, AND NOT ALWAYS THE SAME AS THE HALF. German says «Viertel
    nach eins» (from the hour past) but «halb zwei» (toward the hour coming) — the two halves
    of one language disagree, and only a declared table can hold that.

TWO DIRECTIONS, so the naming is a road and not a label: from the figures to the words («the
clock shows 2:15. how do you say it in words? a quarter past two») and from the words back to
the figures («they said: a quarter past two. how do you write it in figures? 2:15»).

WHAT IS BORROWED: the openers from the house of the pair. Declared here: the hour words of
each language in the cases its clock phrases need (Russian keeps two, Polish three), and the
three phrases themselves with the SHIFT each takes — nought for the hour that passed, one for
the hour that comes.

WHAT IS NOT MEASURED, NAMED: minutes other than a quarter and a half (every language names
them by plain counting, which the corpus already has), the twenty-four-hour clock said aloud,
and the words «midday» and «midnight».
"""
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import asking  # noqa: E402 — the house of the pair declares which openers a question may wear

ЯЗЫКИ = ("ru", "en", "de", "fr", "es", "it", "pt", "nl", "pl")
ЧАСЫ = (1, 2, 3, 4, 5, 6, 7)          # час, от которого считают; следующий берётся сдвигом
# ЧАСЫ 8..11 ДОМ НЕ ПИШЕТ НАРОЧНО: таблицы доведены до двенадцати, и удержанный ключ спрашивает
# ими то, чего дом не показывал, — так меряется ФОРМА, а не память
# ТАБЛИЦЫ ЧАСОВЫХ СЛОВ — по одной на КАЖДЫЙ падеж, которого требует фраза часов этого языка.
# Индекс 1..8 (нулевой не используется).
СЛОВА = {
    "ru": {"род": (None, "первого", "второго", "третьего", "четвёртого", "пятого", "шестого", "седьмого",
                   "восьмого", "девятого", "десятого", "одиннадцатого", "двенадцатого"),
           "им": (None, "час", "два", "три", "четыре", "пять", "шесть", "семь", "восемь",
                  "девять", "десять", "одиннадцать", "двенадцать")},
    "en": {"им": (None, "one", "two", "three", "four", "five", "six", "seven", "eight",
                  "nine", "ten", "eleven", "twelve")},
    "de": {"им": (None, "eins", "zwei", "drei", "vier", "fünf", "sechs", "sieben", "acht",
                  "neun", "zehn", "elf", "zwölf")},
    "nl": {"им": (None, "een", "twee", "drie", "vier", "vijf", "zes", "zeven", "acht",
                  "negen", "tien", "elf", "twaalf")},
    "fr": {"им": (None, "une heure", "deux heures", "trois heures", "quatre heures", "cinq heures",
                  "six heures", "sept heures", "huit heures", "neuf heures", "dix heures",
                  "onze heures", "douze heures")},
    "es": {"им": (None, "la una", "las dos", "las tres", "las cuatro", "las cinco", "las seis",
                  "las siete", "las ocho", "las nueve", "las diez", "las once", "las doce")},
    "it": {"им": (None, "l'una", "le due", "le tre", "le quattro", "le cinque", "le sei",
                  "le sette", "le otto", "le nove", "le dieci", "le undici", "le dodici")},
    "pt": {"им": (None, "uma", "duas", "três", "quatro", "cinco", "seis", "sete", "oito",
                  "nove", "dez", "onze", "doze")},
    "pl": {"по": (None, "pierwszej", "drugiej", "trzeciej", "czwartej", "piątej", "szóstej", "siódmej",
                  "ósmej", "dziewiątej", "dziesiątej", "jedenastej", "dwunastej"),
           "до": (None, "pierwszej", "drugiej", "trzeciej", "czwartej", "piątej", "szóstej", "siódmej",
                  "ósmej", "dziewiątej", "dziesiątej", "jedenastej", "dwunastej"),
           "им": (None, "pierwsza", "druga", "trzecia", "czwarta", "piąta", "szósta", "siódma",
                  "ósma", "dziewiąta", "dziesiąta", "jedenasta", "dwunasta")},
}
# ФРАЗА ЧАСОВ И ЕЁ СДВИГ: 0 — считают от прошедшего часа, 1 — к наступающему. Сдвиг объявлен
# ПОФРАЗНО, ибо две половины одного языка расходятся (немецкое «Viertel nach eins» при «halb zwei»).
ФРАЗЫ = {
    "ru": dict(четверть=("четверть {A}", 1, "род"), половина=("половина {A}", 1, "род"),
               без=("без четверти {A}", 1, "им")),
    "en": dict(четверть=("a quarter past {A}", 0, "им"), половина=("half past {A}", 0, "им"),
               без=("a quarter to {A}", 1, "им")),
    "de": dict(четверть=("Viertel nach {A}", 0, "им"), половина=("halb {A}", 1, "им"),
               без=("Viertel vor {A}", 1, "им")),
    "nl": dict(четверть=("kwart over {A}", 0, "им"), половина=("half {A}", 1, "им"),
               без=("kwart voor {A}", 1, "им")),
    "fr": dict(четверть=("{A} et quart", 0, "им"), половина=("{A} et demie", 0, "им"),
               без=("{A} moins le quart", 1, "им")),
    "es": dict(четверть=("{A} y cuarto", 0, "им"), половина=("{A} y media", 0, "им"),
               без=("{A} menos cuarto", 1, "им")),
    "it": dict(четверть=("{A} e un quarto", 0, "им"), половина=("{A} e mezza", 0, "им"),
               без=("{A} meno un quarto", 1, "им")),
    "pt": dict(четверть=("{A} e um quarto", 0, "им"), половина=("{A} e meia", 0, "им"),
               без=("{A} menos um quarto", 1, "им")),
    "pl": dict(четверть=("kwadrans po {A}", 0, "по"), половина=("wpół do {A}", 1, "до"),
               без=("za kwadrans {A}", 1, "им")),
}
МИНУТЫ = {"четверть": 15, "половина": 30, "без": 45}
РЕЧЬ = {
    "ru": dict(показывают="часы показывают {T}.", вопрос_словами="как сказать это словами?",
               сказали="говорят: {W}.", вопрос_цифрами="как записать это цифрами?"),
    "en": dict(показывают="the clock shows {T}.", вопрос_словами="how do you say it in words?",
               сказали="they said: {W}.", вопрос_цифрами="how do you write it in figures?"),
    "de": dict(показывают="die Uhr zeigt {T}.", вопрос_словами="wie sagt man das in Worten?",
               сказали="man sagt: {W}.", вопрос_цифрами="wie schreibt man das in Ziffern?"),
    "fr": dict(показывают="l'horloge indique {T}.", вопрос_словами="comment le dit-on en mots ?",
               сказали="on dit : {W}.", вопрос_цифрами="comment l'écrit-on en chiffres ?"),
    "es": dict(показывают="el reloj marca {T}.", вопрос_словами="¿cómo se dice en palabras?",
               сказали="se dice: {W}.", вопрос_цифрами="¿cómo se escribe en cifras?"),
    "it": dict(показывают="l'orologio segna {T}.", вопрос_словами="come si dice a parole?",
               сказали="si dice: {W}.", вопрос_цифрами="come si scrive in cifre?"),
    "pt": dict(показывают="o relógio marca {T}.", вопрос_словами="como se diz por palavras?",
               сказали="diz-se: {W}.", вопрос_цифрами="como se escreve em algarismos?"),
    "nl": dict(показывают="de klok wijst {T} aan.", вопрос_словами="hoe zegt men dat in woorden?",
               сказали="men zegt: {W}.", вопрос_цифрами="hoe schrijft men dat in cijfers?"),
    "pl": dict(показывают="zegar wskazuje {T}.", вопрос_словами="jak to powiedzieć słowami?",
               сказали="mówi się: {W}.", вопрос_цифрами="jak to zapisać cyframi?"),
}
ФОРМЫ = ("словами", "цифрами")
ВИДЫ = ("четверть", "половина", "без")


def _слово(язык, вид, ч):
    """Фраза часов: шаблон языка, сдвиг часа и падеж — всё объявлено, ничто не выведено."""
    шаблон, сдвиг, падеж = ФРАЗЫ[язык][вид]
    таблица = СЛОВА[язык][падеж]
    слово = таблица[ч + сдвиг]
    return шаблон.replace("{A}", слово)


def _цифры(ч, вид):
    return "%d:%02d" % (ч, МИНУТЫ[вид])


def рамка(язык, форма, вид, ч):
    р = РЕЧЬ[язык]
    слова, цифры = _слово(язык, вид, ч), _цифры(ч, вид)
    if форма == "словами":
        return (р["показывают"].replace("{T}", цифры) + " " + р["вопрос_словами"] + " " + слова + ".")
    return (р["сказали"].replace("{W}", слова) + " " + р["вопрос_цифрами"] + " " + цифры + ".")


def страница(язык, форма, вид, ч):
    return рамка(язык, форма, вид, ч)


def _показы():
    вон = {}
    for язык in ЯЗЫКИ:
        for вид in ВИДЫ:
            for ч in ЧАСЫ:
                for форма in ФОРМЫ:
                    вон[страница(язык, форма, вид, ч)] = (язык, форма)
    return вон


ПОКАЗЫ = _показы()
# ВСЕ ФРАЗЫ ДОМА — множество, по которому судится ЧУЖОЕ СЛОВО при своей рамке
# РАМКА ЗНАЕТ ВЕСЬ ЦИФЕРБЛАТ, А ПОКАЗЫ — ЛИШЬ ЕГО ЧАСТЬ: иначе удержанная страница (час 9,
# которого дом не писал) была бы для суда ЧУЖОЙ строкой, и ключ мерил бы молчание вместо формы
ВСЕ_ЧАСЫ = tuple(range(1, 12))
_ФРАЗЫ_ЯЗЫКА = {язык: {_слово(язык, вид, ч): (вид, ч) for вид in ВИДЫ for ч in ВСЕ_ЧАСЫ}
                for язык in ЯЗЫКИ}


def _альт(слова):
    return "(?:" + "|".join(re.escape(с) for с in sorted({с for с in слова if с}, key=lambda с: (-len(с), с))) + ")"


def _образец(язык, форма):
    """Рамка держит ЧАСЫ и СЛОВА дырами: подмена любой из них есть ложь, а не чужая строка."""
    р = РЕЧЬ[язык]
    фразы = _альт(_ФРАЗЫ_ЯЗЫКА[язык])
    if форма == "словами":
        шаблон = р["показывают"].replace("{T}", "{T}") + " " + р["вопрос_словами"] + " {W}."
    else:
        шаблон = р["сказали"].replace("{W}", "{W}") + " " + р["вопрос_цифрами"] + " {T}."
    дыры = {"T": r"\d+:\d\d", "W": фразы}
    счёт, куски = {}, []
    for кусок in re.split(r"(\{[^}]+\})", шаблон):
        if кусок.startswith("{"):
            дыра = кусок[1:-1]
            счёт[дыра] = счёт.get(дыра, 0) + 1
            куски.append(f"(?P<h_{дыра}__{счёт[дыра]}>{дыры[дыра]})")
        else:
            куски.append(re.escape(кусок))
    return re.compile("^" + "".join(куски) + "$")


ОБРАЗЦЫ = [(_образец(язык, форма), язык, форма) for язык in ЯЗЫКИ for форма in ФОРМЫ]


def _значения(м):
    вон = {}
    for ключ, знач in м.groupdict().items():
        дыра, _ = ключ[2:].rsplit("__", 1)
        if дыра in вон and вон[дыра] != знач:
            return None
        вон[дыра] = знач
    return вон


def _вердикт(язык, форма, зн):
    пара = _ФРАЗЫ_ЯЗЫКА[язык].get(зн["W"])
    if пара is None:
        return False
    вид, ч = пара
    # СЛОВО И ЦИФРЫ СУТЬ ОДНА МИНУТА: фраза называет свой час и свою четверть, и цифры обязаны
    # быть ровно теми же — здесь и ловится язык, посчитанный «от прошедшего часа» там, где он
    # считает «к наступающему»
    return зн["T"] == _цифры(ч, вид)


def судить(строка):
    """(судимо, истинно): a page of a frame of the house whose words name that very minute."""
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
        # (1) ЧАС СДВИНУТ: «половина третьего» при 3:30 (а не 2:30) — ровно та ошибка, которую
        # делает читатель, выучивший одну из двух половин мира
        п = страница(язык, "словами", "половина", 2)
        assert судить(п) == (True, True), п
        битая = п.replace("2:30", "3:30")
        assert судить(битая) == (True, False), битая
        # (2) ЧЕТВЕРТЬ ВМЕСТО ПОЛОВИНЫ
        битая = п.replace(_слово(язык, "половина", 2), _слово(язык, "четверть", 2))
        assert судить(битая) == (True, False), битая
        # (3) ОБРАТНЫЙ ХОД: слова названы, цифры чужие
        ц = страница(язык, "цифрами", "без", 4)
        assert судить(ц) == (True, True), ц
        битая = ц.replace("4:45", "5:45")
        assert судить(битая) == (True, False), битая
        # (4) ЧУЖОЙ ЧАС В СЛОВАХ
        битая = ц.replace(_слово(язык, "без", 4), _слово(язык, "без", 5))
        assert судить(битая) == (True, False), битая
        мутанты += 4
        # (5) ЗАЧИН ВОПРОСА ОБЪЯВЛЕН ДОМОМ ПАРЫ
        for стр in (п, ц):
            вопрос = стр[:стр.index("?") + 1].split(". ")[-1]
            assert asking.зачин_объявлен(вопрос) is not False, (язык, вопрос)
    for язык in ЯЗЫКИ:
        print("  ", страница(язык, "словами", "половина", 2))
    for язык in ("ru", "en", "de", "pl"):
        print("  ", страница(язык, "словами", "четверть", 1))
        print("  ", страница(язык, "цифрами", "без", 4))
    по_форме = {}
    for _, (язык, форма) in ПОКАЗЫ.items():
        по_форме[форма] = по_форме.get(форма, 0) + 1
    print(f"  мутантов поймано: {мутанты}")
    print(f"  дом пишет показов: {len(ПОКАЗЫ)} (языков {len(ЯЗЫКИ)}, форм {len(ФОРМЫ)}, видов {len(ВИДЫ)}, "
          f"образцов {len(ОБРАЗЦЫ)}): " + ", ".join(f"{ф} {к}" for ф, к in по_форме.items()))


if __name__ == "__main__":
    _самопроверка()
