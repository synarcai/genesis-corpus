#!/usr/bin/env python3
"""THE TAIL THAT POINTS BACKWARD — «how many did I have TO BEGIN WITH?» (05.09).

The third gate of the silence atlas, named by measure: 24 rows of the grove and 23 of the
reader stop at an unbought tail — «to begin with», «in the beginning», «initially», «at the
start», «before he spent his money». The market of before-tails exists and did not reach its
quorum: the corpus showed the words too few times for them to be bought.

WHAT THE TAIL DOES, AND WHY IT IS NOT DECORATION. It reverses the question. «i gave away 3
apples. i have 7 apples left» — asked forward, the answer is 7; asked with the tail, «how many
apples did i have TO BEGIN WITH?», the answer is 10, and the ledger runs the act BACKWARDS:
7 + 3 = 10. A reader that reads the tail as noise answers 7 and is wrong every time. So this
house shows one and the same story asked only backwards, with FIVE different tails per
language, because the market must buy the WORDS, not one phrase.

THREE ACTS, EACH INVERTED BY ITS OWN SIGN: what was given away is added back, what was bought
is taken away, what was spent is added back to what is left. The money act is here on purpose:
the second gate of the same atlas is the money road, and a sum that must be restored is where
the two gates meet.

FIRST PERSON, AND THAT IS A DECISION. «i gave away» needs no name and no case; a house that
declined names in nine languages would spend its whole strength on declension and buy the tail
in none. The goods, their count forms and the currency word come from the house of the price —
one declaration, several readers.

WHAT IS NOT MEASURED, NAMED: two acts before the question (that is the episode house), a tail
that points forward («in the end»), and any story where the initial state is stated outright —
here it is always the unknown.
"""
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import asking  # noqa: E402 — the house of the pair declares which openers a question may wear
import priceforms as P  # noqa: E402 — the goods, the currency word and the pack's counting rule

ЯЗЫКИ = ("ru", "en", "de", "fr", "es", "it", "pt", "nl", "pl")
ТОВАРОВ = 3
# ПАРЫ (что стало, сколько ушло/пришло) — начальное состояние всегда больше единицы
ОТДАЛ = ((7, 3), (11, 4), (9, 6), (13, 5), (8, 7), (15, 9), (6, 2), (12, 8))
КУПИЛ = ((11, 4), (14, 6), (9, 3), (17, 8), (12, 5), (20, 9), (10, 2), (16, 7))
ПОТРАТИЛ = ((76, 25), (48, 17), (95, 38), (63, 29), (52, 14), (87, 46), (39, 21), (71, 33))
# ЗНАК ВАЛЮТЫ И ЕГО СТОРОНА — как у дома непрочитанного числа: сторона есть свойство языка
ЗНАК = {"ru": ("₽", "после"), "en": ("$", "до"), "de": ("€", "после"), "fr": ("€", "после"),
        "es": ("€", "после"), "it": ("€", "после"), "pt": ("€", "после"), "nl": ("€", "после"),
        "pl": ("zł", "после")}
РОД = {"es": ("f", "m", "m"), "it": ("f", "m", "f"), "pt": ("f", "m", "m")}
КСК = {"es": {"m": "¿cuántos", "f": "¿cuántas"}, "it": {"m": "quanti", "f": "quante"},
       "pt": {"m": "quantos", "f": "quantas"}}
# ХВОСТЫ «ПРЕЖДЕ» — пять на язык. Рынок покупает СЛОВА, а не одну фразу, и потому их пять.
ХВОСТЫ = {
    "ru": ("сначала", "вначале", "изначально", "поначалу", "до того"),
    "en": ("to begin with", "in the beginning", "initially", "at the start", "before that"),
    "de": ("zu Beginn", "am Anfang", "anfangs", "ursprünglich", "davor"),
    "fr": ("au début", "au commencement", "initialement", "au départ", "avant cela"),
    "es": ("al principio", "al comienzo", "inicialmente", "de entrada", "antes de eso"),
    "it": ("all'inizio", "in principio", "inizialmente", "all'origine", "prima di questo"),
    "pt": ("no início", "no começo", "inicialmente", "de início", "antes disso"),
    "nl": ("in het begin", "aanvankelijk", "oorspronkelijk", "om te beginnen", "daarvoor"),
    "pl": ("na początku", "początkowo", "pierwotnie", "na wstępie", "przedtem"),
}
РЕЧЬ = {
    "ru": dict(отдал="я отдал {k} {Тk}.", осталось="у меня осталось {r} {Тr}.",
               купил="я купил {k} {Тk}.", теперь="теперь у меня {r} {Тr}.",
               потратил="я потратил {Цk}.", осталось_денег="у меня осталось {Цr}.",
               вопрос_вещь="сколько {МН} у меня было {ХВОСТ}?",
               вопрос_деньги="сколько денег у меня было {ХВОСТ}?",
               ответ_вещь="{v} {Тv}", ответ_деньги="{Цv}",
               двоеточие=": ", вопрос="?"),
    "en": dict(отдал="i gave away {k} {Тk}.", осталось="i have {r} {Тr} left.",
               купил="i bought {k} {Тk}.", теперь="now i have {r} {Тr}.",
               потратил="i spent {Цk}.", осталось_денег="i have {Цr} left.",
               вопрос_вещь="how many {МН} did i have {ХВОСТ}?",
               вопрос_деньги="how much money did i have {ХВОСТ}?",
               ответ_вещь="{v} {Тv}", ответ_деньги="{Цv}",
               двоеточие=": ", вопрос="?"),
    "de": dict(отдал="ich habe {k} {Тk} weggegeben.", осталось="mir sind {r} {Тr} geblieben.",
               купил="ich habe {k} {Тk} gekauft.", теперь="jetzt habe ich {r} {Тr}.",
               потратил="ich habe {Цk} ausgegeben.", осталось_денег="mir sind {Цr} geblieben.",
               вопрос_вещь="wie viele {МН} hatte ich {ХВОСТ}?",
               вопрос_деньги="wie viel Geld hatte ich {ХВОСТ}?",
               ответ_вещь="{v} {Тv}", ответ_деньги="{Цv}",
               двоеточие=": ", вопрос="?"),
    "fr": dict(отдал="j'ai donné {k} {Тk}.", осталось="il me reste {r} {Тr}.",
               купил="j'ai acheté {k} {Тk}.", теперь="maintenant j'ai {r} {Тr}.",
               потратил="j'ai dépensé {Цk}.", осталось_денег="il me reste {Цr}.",
               вопрос_вещь="combien de {МН} avais-je {ХВОСТ} ?",
               вопрос_деньги="combien d'argent avais-je {ХВОСТ} ?",
               ответ_вещь="{v} {Тv}", ответ_деньги="{Цv}",
               двоеточие=" : ", вопрос=" ?"),
    "es": dict(отдал="di {k} {Тk}.", осталось="me quedan {r} {Тr}.",
               купил="compré {k} {Тk}.", теперь="ahora tengo {r} {Тr}.",
               потратил="gasté {Цk}.", осталось_денег="me quedan {Цr}.",
               вопрос_вещь="{КСК} {МН} tenía {ХВОСТ}?",
               вопрос_деньги="¿cuánto dinero tenía {ХВОСТ}?",
               ответ_вещь="{v} {Тv}", ответ_деньги="{Цv}",
               двоеточие=": ", вопрос="?"),
    "it": dict(отдал="ho dato {k} {Тk}.", осталось="mi restano {r} {Тr}.",
               купил="ho comprato {k} {Тk}.", теперь="adesso ho {r} {Тr}.",
               потратил="ho speso {Цk}.", осталось_денег="mi restano {Цr}.",
               вопрос_вещь="{КСК} {МН} avevo {ХВОСТ}?",
               вопрос_деньги="quanti soldi avevo {ХВОСТ}?",
               ответ_вещь="{v} {Тv}", ответ_деньги="{Цv}",
               двоеточие=": ", вопрос="?"),
    "pt": dict(отдал="dei {k} {Тk}.", осталось="restam-me {r} {Тr}.",
               купил="comprei {k} {Тk}.", теперь="agora tenho {r} {Тr}.",
               потратил="gastei {Цk}.", осталось_денег="restam-me {Цr}.",
               вопрос_вещь="{КСК} {МН} tinha {ХВОСТ}?",
               вопрос_деньги="quanto dinheiro tinha {ХВОСТ}?",
               ответ_вещь="{v} {Тv}", ответ_деньги="{Цv}",
               двоеточие=": ", вопрос="?"),
    "nl": dict(отдал="ik heb {k} {Тk} weggegeven.", осталось="ik heb nog {r} {Тr} over.",
               купил="ik heb {k} {Тk} gekocht.", теперь="nu heb ik {r} {Тr}.",
               потратил="ik heb {Цk} uitgegeven.", осталось_денег="ik heb nog {Цr} over.",
               вопрос_вещь="hoeveel {МН} had ik {ХВОСТ}?",
               вопрос_деньги="hoeveel geld had ik {ХВОСТ}?",
               ответ_вещь="{v} {Тv}", ответ_деньги="{Цv}",
               двоеточие=": ", вопрос="?"),
    "pl": dict(отдал="oddałem {k} {Тk}.", осталось="zostało mi {r} {Тr}.",
               купил="kupiłem {k} {Тk}.", теперь="teraz mam {r} {Тr}.",
               потратил="wydałem {Цk}.", осталось_денег="zostało mi {Цr}.",
               вопрос_вещь="ile {МН} miałem {ХВОСТ}?",
               вопрос_деньги="ile pieniędzy miałem {ХВОСТ}?",
               ответ_вещь="{v} {Тv}", ответ_деньги="{Цv}",
               двоеточие=": ", вопрос="?"),
}
ФОРМЫ = ("отдал", "купил", "потратил")


def _вещь(язык, i, k):
    return P.форма(язык, P.ЯЗЫКИ[язык]["вещи"][i], k)


def _ксk(язык, i):
    return КСК[язык][РОД[язык][i]] if язык in КСК else ""


def _цена(язык, n):
    знак, сторона = ЗНАК[язык]
    return f"{знак}{n}" if сторона == "до" else f"{n} {знак}"


def рамка(язык, форма, i, хвост):
    """The page: an act, the state after it, and the question that runs the act backwards."""
    р = РЕЧЬ[язык]
    х = ХВОСТЫ[язык][хвост]
    if форма == "потратил":
        вопрос = р["вопрос_деньги"].replace("{ХВОСТ}", х)
        return (р["потратил"] + " " + р["осталось_денег"] + " " + вопрос + " "
                + р["ответ_деньги"] + р["двоеточие"] + "{r} + {k} = {v}.")
    мн = P.ЯЗЫКИ[язык]["вещи"][i].get("many")
    вопрос = р["вопрос_вещь"].replace("{КСК}", _ксk(язык, i)).replace("{МН}", мн).replace("{ХВОСТ}", х)
    if форма == "отдал":
        # ОТДАННОЕ ВОЗВРАЩАЕТСЯ СЛОЖЕНИЕМ — акт обращён, а не повторён
        return (р["отдал"] + " " + р["осталось"] + " " + вопрос + " "
                + р["ответ_вещь"] + р["двоеточие"] + "{r} + {k} = {v}.")
    return (р["купил"] + " " + р["теперь"] + " " + вопрос + " "
            + р["ответ_вещь"] + р["двоеточие"] + "{r} − {k} = {v}.")


def страница(язык, форма, i, хвост, r, k):
    v = r + k if форма in ("отдал", "потратил") else r - k
    if форма == "потратил":
        поля = dict(r=r, k=k, v=v, Цk=_цена(язык, k), Цr=_цена(язык, r), Цv=_цена(язык, v))
    else:
        поля = dict(r=r, k=k, v=v, Тk=_вещь(язык, i, k), Тr=_вещь(язык, i, r), Тv=_вещь(язык, i, v))
    return рамка(язык, форма, i, хвост).format(**поля)


def _показы():
    вон = {}
    for язык in ЯЗЫКИ:
        for хвост in range(len(ХВОСТЫ[язык])):
            # ВЕЩЬ ИДЁТ ПО КРУГУ ВМЕСТЕ С ПАРОЙ: рынок должен видеть хвост при РАЗНЫХ вещах и
            # разных числах, а не одну фразу, повторённую тридцать раз
            for q, (r, k) in enumerate(ОТДАЛ):
                i = (q + хвост) % ТОВАРОВ
                вон[страница(язык, "отдал", i, хвост, r, k)] = (язык, "отдал")
                вон[страница(язык, "отдал", (i + 1) % ТОВАРОВ, хвост, r, k)] = (язык, "отдал")
            for q, (r, k) in enumerate(КУПИЛ):
                if r - k < 1:
                    continue
                i = (q + хвост + 1) % ТОВАРОВ
                вон[страница(язык, "купил", i, хвост, r, k)] = (язык, "купил")
                вон[страница(язык, "купил", (i + 2) % ТОВАРОВ, хвост, r, k)] = (язык, "купил")
            for q, (r, k) in enumerate(ПОТРАТИЛ):
                вон[страница(язык, "потратил", 0, хвост, r, k)] = (язык, "потратил")
    return вон


ПОКАЗЫ = _показы()


def _альт(слова):
    return "(?:" + "|".join(re.escape(с) for с in sorted({с for с in слова if с}, key=lambda с: (-len(с), с))) + ")"


def _образец(язык, шаблон, i):
    вещи = _альт(P.ЯЗЫКИ[язык]["вещи"][i].values())
    знак, сторона = ЗНАК[язык]
    цена = (re.escape(знак) + r"\d+") if сторона == "до" else (r"\d+ " + re.escape(знак))
    дыры = {"r": r"\d+", "k": r"\d+", "v": r"\d+", "Тr": вещи, "Тk": вещи, "Тv": вещи,
            "Цr": цена, "Цk": цена, "Цv": цена}
    счёт, куски = {}, []
    for кусок in re.split(r"(\{[^}]+\})", шаблон):
        if кусок.startswith("{"):
            дыра = кусок[1:-1]
            счёт[дыра] = счёт.get(дыра, 0) + 1
            куски.append(f"(?P<h_{дыра}__{счёт[дыра]}>{дыры[дыра]})")
        else:
            куски.append(re.escape(кусок))
    return re.compile("^" + "".join(куски) + "$")


ОБРАЗЦЫ = [(_образец(язык, рамка(язык, форма, i, хвост), i), язык, форма, i)
           for язык in ЯЗЫКИ for форма in ФОРМЫ
           for i in (range(ТОВАРОВ) if форма != "потратил" else (0,))
           for хвост in range(len(ХВОСТЫ[язык]))]


def _значения(м):
    вон = {}
    for ключ, знач in м.groupdict().items():
        дыра, _ = ключ[2:].rsplit("__", 1)
        if дыра in вон and вон[дыра] != знач:
            return None
        вон[дыра] = знач
    return вон


def _число(с):
    м = re.search(r"\d+", с)
    return int(м.group()) if м else None


def _вердикт(язык, форма, i, зн):
    if форма == "потратил":
        r, k, v = int(зн["r"]), int(зн["k"]), int(зн["v"])
        if min(r, k) < 1 or v != r + k:
            return False
        return (_число(зн["Цr"]) == r and _число(зн["Цk"]) == k and _число(зн["Цv"]) == v)
    r, k, v = int(зн["r"]), int(зн["k"]), int(зн["v"])
    if min(r, k, v) < 1:
        return False
    # АКТ ОБРАЩАЕТСЯ ЗНАКОМ СВОЕГО РОДА: отданное складывается, купленное вычитается
    if v != (r + k if форма == "отдал" else r - k):
        return False
    for дыра, число in (("Тr", r), ("Тk", k), ("Тv", v)):
        if зн[дыра] != _вещь(язык, i, число):
            return False
    return True


def судить(строка):
    """(судимо, истинно): a page of a frame of the house whose act runs backwards correctly."""
    с = строка.strip()
    if с in ПОКАЗЫ:
        return True, True
    for образ, язык, форма, i in ОБРАЗЦЫ:
        м = образ.match(с)
        if not м:
            continue
        зн = _значения(м)
        if зн is None:
            return True, False
        return True, _вердикт(язык, форма, i, зн)
    return False, False


def _хвост_ответа(с):
    м = list(re.finditer(r"[?？] ", с))
    return м[-1].end() if м else 0


def _самопроверка():
    for показ in ПОКАЗЫ:
        assert судить(показ) == (True, True), показ
    мутанты = 0
    for язык in ЯЗЫКИ:
        # (1) ХВОСТ ПРОЧИТАН КАК ШУМ: ответ равен тому, что ОСТАЛОСЬ, а не начальному
        о = страница(язык, "отдал", 0, 0, 7, 3)
        assert судить(о) == (True, True), о
        хв = _хвост_ответа(о)
        битая = о[:хв] + о[хв:].replace("10", "7")
        assert судить(битая) == (True, False), битая
        # (2) АКТ ПОВТОРЁН, А НЕ ОБРАЩЁН: купленное сложено вместо вычитания
        к = страница(язык, "купил", 0, 1, 11, 4)
        assert судить(к) == (True, True), к
        хв = _хвост_ответа(к)
        битая = к[:хв] + к[хв:].replace("7", "15")
        assert судить(битая) == (True, False), битая
        # (3) ДЕНЬГИ: сумма не восстановлена
        д = страница(язык, "потратил", 0, 2, 76, 25)
        assert судить(д) == (True, True), д
        битая = д.replace("= 101.", "= 100.")
        assert судить(битая) == (True, False), битая
        мутанты += 3
        # (4) СЧЁТНАЯ ФОРМА НАЧАЛЬНОГО ЧИСЛА — ФОРМА ЧУЖОГО ЧИСЛА
        своя, чужая = _вещь(язык, 0, 10), _вещь(язык, 0, 1)
        if своя != чужая:
            хв = _хвост_ответа(о)
            битая = о[:хв] + о[хв:].replace("10 " + своя, "10 " + чужая, 1)
            assert судить(битая) == (True, False), битая
            мутанты += 1
        # (5) ЗАЧИН ВОПРОСА ОБЪЯВЛЕН ДОМОМ ПАРЫ, А ХВОСТ СТОИТ В ЕГО КОНЦЕ
        for стр in (о, к, д):
            вопрос = стр[:стр.index("?") + 1].split(". ")[-1]
            assert asking.зачин_объявлен(вопрос) is not False, (язык, вопрос)
    for язык in ЯЗЫКИ:
        print("  ", страница(язык, "отдал", 0, 0, 7, 3))
    for язык in ("ru", "en", "de", "pl"):
        print("  ", страница(язык, "купил", 1, 2, 11, 4))
        print("  ", страница(язык, "потратил", 0, 3, 76, 25))
    по_форме, по_хвосту = {}, {}
    for с, (язык, форма) in ПОКАЗЫ.items():
        по_форме[форма] = по_форме.get(форма, 0) + 1
    print(f"  мутантов поймано: {мутанты}")
    print(f"  дом пишет показов: {len(ПОКАЗЫ)} (языков {len(ЯЗЫКИ)}, форм {len(ФОРМЫ)}, хвостов 5, "
          f"образцов {len(ОБРАЗЦЫ)}): " + ", ".join(f"{ф} {к}" for ф, к in по_форме.items()))


if __name__ == "__main__":
    _самопроверка()
