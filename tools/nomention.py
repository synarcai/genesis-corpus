#!/usr/bin/env python3
"""THE QUESTION ABOUT WHAT WAS NEVER SAID — the fourth gate of the silence atlas (06.09).

d5's honest atlas ranks the reader's refusals, and after the unread number, the money road and
the unbought tail comes UNKNOWN-ENTITY: the question names a thing the story never carried,
and the reader stops. Stopping is right — the answer does not exist — but stopping SILENTLY is
not an answer. An organism that cannot say «I do not know, and here is why» has no way to
distinguish a hole in the story from a hole in itself.

WHAT THE HOUSE SHOWS, AND WHY THE POSITIVE TWIN IS HALF OF IT.

    THE PLACE THAT WAS NAMED. «there are 5 files in the folder. how many files are in the
    folder? there are 5 files in the folder.» — without this half the market would buy
    «refuse whenever a place is named», which is worse than the defect it cures.

    THE PLACE THAT WAS NOT. «there are 5 files in the folder. how many files are in the box?
    I do not know: nothing is said about the box.» The ground names the very place the
    question asked, so the refusal is CHECKABLE: a page refusing about a place the story did
    name is a lie, and the court says so.

    THE THING THAT WAS NOT. «there are 5 files in the folder. how many records are in the
    folder? I do not know: nothing is said about records.» A story speaks of one kind; a
    question about another kind has no answer either, and the ground names the kind.

    TWO PLACES, AND A QUESTION ABOUT A THIRD. Two counts stand; the question asks about a
    place neither sentence mentioned. Refusal again — and its twin, the question about one of
    the two, is answered. Silence has a boundary, and the boundary is what the story SAID.

WHAT IS BORROWED: the places in three cases and the things from the houses of the summary and
the tool, the word of not-knowing from the house of the pair (through the house of the order,
which derives it), the openers from the house of the pair. Declared here: the grounds of the
refusal («nothing is said about the box», «o wpisach nie powiedziano») — the about-case of a
thing, which no neighbour had.

WHAT IS NOT MEASURED, NAMED: a question about a NAME the story did not carry (names decline in
nine languages, and this house would spend its strength on declension), and a question whose
entity is named by a pronoun with no antecedent — that is the anaphora market's.
"""
import pathlib
import re
import frgram as _fr  # французская элизия: один закон, два читателя
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import asking  # noqa: E402 — the house of the pair declares which openers a question may wear
import opforms as O  # noqa: E402 — the pair house's word of not-knowing, already derived there
import summaryforms as SU  # noqa: E402 — the places in three cases (locative, nominative, about)
import svampforms as S  # noqa: E402 — the count cell of a pack
import toolforms as T  # noqa: E402 — the things of acts and the copula of a place

ЯЗЫКИ = T.ЯЗЫКИ
МЕСТА = SU.МЕСТА
ЧИСЛА = (2, 3, 4, 5, 6, 7, 8, 9, 11, 12, 14, 15, 17, 18, 20, 21)
# О ВЕЩИ ВО МНОЖЕСТВЕННОМ — падеж основания отказа. Ни у одного соседа его не было.
О_ВЕЩИ = {
    "ru": ("о файлах", "о записях", "о сообщениях"),
    "en": ("about files", "about records", "about messages"),
    "de": ("über Dateien", "über Einträge", "über Nachrichten"),
    "fr": ("sur les fichiers", "sur les enregistrements", "sur les messages"),
    "es": ("de los archivos", "de los registros", "de los mensajes"),
    "it": ("sui documenti", "sulle voci", "sui messaggi"),
    "pt": ("sobre os ficheiros", "sobre os registos", "sobre as mensagens"),
    "nl": ("over bestanden", "over records", "over berichten"),
    "pl": ("o plikach", "o wpisach", "o wiadomościach"),
}
РЕЧЬ = {
    "ru": dict(состояние="{М} {n} {Т}", вопрос="сколько {Тмн} {М}?",
               основание="{О} не сказано", двоеточие=": ", вопрос_знак="?"),
    "en": dict(состояние="{ЕСТЬ} {n} {Т} {М}", вопрос="how many {Тмн} are {М}?",
               основание="nothing is said {О}", двоеточие=": ", вопрос_знак="?"),
    "de": dict(состояние="{М} {ЕСТЬ} {n} {Т}", вопрос="wie viele {Тмн} sind {М}?",
               основание="{О} ist nichts gesagt", двоеточие=": ", вопрос_знак="?"),
    "fr": dict(состояние="{М} il y a {n} {Т}", вопрос="combien de {Тмн} y a-t-il {М} ?",
               основание="rien n'est dit {О}", двоеточие=" : ", вопрос_знак=" ?"),
    "es": dict(состояние="{М} hay {n} {Т}", вопрос="¿cuántos {Тмн} hay {М}?",
               основание="no se dice nada {О}", двоеточие=": ", вопрос_знак="?"),
    "it": dict(состояние="{М} {ЕСТЬ} {n} {Т}", вопрос="quanti {Тмн} ci sono {М}?",
               основание="non è detto nulla {О}", двоеточие=": ", вопрос_знак="?"),
    "pt": dict(состояние="{М} há {n} {Т}", вопрос="quantos {Тмн} há {М}?",
               основание="não é dito nada {О}", двоеточие=": ", вопрос_знак="?"),
    "nl": dict(состояние="{М} {ЕСТЬ} {n} {Т}", вопрос="hoeveel {Тмн} liggen {М}?",
               основание="er is niets gezegd {О}", двоеточие=": ", вопрос_знак="?"),
    "pl": dict(состояние="{М} {ЕСТЬ} {n} {Т}", вопрос="ile {Тмн} jest {М}?",
               основание="{О} nie powiedziano", двоеточие=": ", вопрос_знак="?"),
}
ФОРМЫ = ("место_названо", "место_чужое", "вещь_чужая", "два_места", "третье_место")


def _вещь(язык, Т, c):
    return S._счёт(T.ВЕЩИ[язык][Т % len(T.ВЕЩИ[язык])], c, язык)


def _состояние(язык, i, номер=""):
    """The story's sentence about one place; its holes carry the place's index."""
    с = РЕЧЬ[язык]["состояние"].replace("{М}", МЕСТА[язык][i][0])
    с = с.replace("{n}", "{n%s}" % номер).replace("{Т}", "{Тn%s}" % номер)
    return с.replace("{ЕСТЬ}", "{ЕСТЬ%s}" % номер)


def рамка(язык, форма, где, спрошено, Т=0, Тспр=0):
    """The page: what the story said, what the question asked, and the answer or the refusal."""
    р = РЕЧЬ[язык]
    мн = _вещь(язык, Тспр if форма == "вещь_чужая" else Т, 5)
    вопрос = р["вопрос"].replace("{М}", МЕСТА[язык][спрошено][0]).replace("{Тмн}", мн)
    if форма in ("место_названо", "два_места"):
        история = " ".join(_состояние(язык, i, "" if k == 0 else str(k + 1)) + "."
                           for k, i in enumerate(где))
        # СПРОШЕННОЕ МЕСТО БЫВАЕТ И НЕНАЗВАННЫМ: рамка такой страницы существует нарочно —
        # страница, отвечающая о месте, которого история не называла, есть ЛОЖЬ по закону, а
        # не чужая строка; число она берёт у первого предложения истории
        какой = где.index(спрошено) if спрошено in где else 0
        ответ = _состояние(язык, спрошено, "" if какой == 0 else str(какой + 1)) + "."
        return история + " " + вопрос + " " + ответ
    история = " ".join(_состояние(язык, i, "" if k == 0 else str(k + 1)) + "."
                       for k, i in enumerate(где))
    # ОСНОВАНИЕ НАЗЫВАЕТ РОВНО ТО, О ЧЁМ СПРОСИЛИ, И ПОТОМУ ОТКАЗ ПРОВЕРЯЕМ
    о = О_ВЕЩИ[язык][Тспр % len(О_ВЕЩИ[язык])] if форма == "вещь_чужая" else МЕСТА[язык][спрошено][2]
    отказ = O.ГОЛОВА[язык] + р["двоеточие"] + р["основание"].replace("{О}", о) + "."
    return история + " " + вопрос + " " + отказ


def страница(язык, форма, где, спрошено, Т, n, Тспр=0, n2=0):
    поля = {}
    for k, i in enumerate(где):
        номер = "" if k == 0 else str(k + 1)
        число = n if k == 0 else n2
        поля["n%s" % номер] = число
        поля["Тn%s" % номер] = _вещь(язык, Т, число)
        поля["ЕСТЬ%s" % номер] = T._есть(язык, число) if язык in T.ЕСТЬ else ""
    return _fr.элизия(рамка(язык, форма, где, спрошено, Т, Тспр).format(**поля)) if язык == "fr" else рамка(язык, форма, где, спрошено, Т, Тспр).format(**поля)


def _показы():
    вон = {}
    for язык in ЯЗЫКИ:
        видов = len(T.ВЕЩИ[язык])
        мест = len(МЕСТА[язык])
        for q, n in enumerate(ЧИСЛА):
          for Т in range(видов):
            i = (q + Т) % мест
            j = (i + 1 + q % 2) % мест          # место, которого история не называла
            вон[страница(язык, "место_названо", (i,), i, Т, n)] = (язык, "место_названо")
            вон[страница(язык, "место_чужое", (i,), j, Т, n)] = (язык, "место_чужое")
            чужая = (Т + 1 + q % 2) % видов
            вон[страница(язык, "вещь_чужая", (i,), i, Т, n, Тспр=чужая)] = (язык, "вещь_чужая")
            # ДВА МЕСТА: вопрос об одном из названных — ответ; о третьем — отказ
            i2 = (i + 1) % мест
            n2 = ЧИСЛА[(q + 5) % len(ЧИСЛА)]
            третье = (i + 2) % мест
            if len({i, i2, третье}) == 3:
                вон[страница(язык, "два_места", (i, i2), i2, Т, n, n2=n2)] = (язык, "два_места")
                вон[страница(язык, "третье_место", (i, i2), третье, Т, n, n2=n2)] = (язык, "третье_место")
    return вон


ПОКАЗЫ = _показы()


def _альт(слова):
    return "(?:" + "|".join(re.escape(с) for с in sorted({с for с in слова if с}, key=lambda с: (-len(с), с))) + ")"


def _образец(язык, шаблон):
    вещи = _альт(T.ФОРМЫ_ВЕЩЕЙ[язык])
    есть = _альт(T.ЕСТЬ[язык]) if язык in T.ЕСТЬ else None
    дыры = {"Тмн": вещи}
    for н in ("", "2"):
        дыры["n%s" % н] = r"\d+"
        дыры["Тn%s" % н] = вещи
        дыры["ЕСТЬ%s" % н] = есть if есть else ""
    счёт, куски = {}, []
    for кусок in re.split(r"(\{[^}]+\})", шаблон):
        if кусок.startswith("{"):
            дыра = кусок[1:-1]
            счёт[дыра] = счёт.get(дыра, 0) + 1
            узор = дыры[дыра]
            куски.append(f"(?P<h_{дыра}__{счёт[дыра]}>{узор})" if узор else "")
        else:
            куски.append(_fr.в_образце(кусок) if язык == "fr" else re.escape(кусок))
    return re.compile("^" + "".join(куски) + "$")


def _все_рамки():
    """Every shape: which places the story named, which place (or thing) the question asked."""
    вон = []
    for язык in ЯЗЫКИ:
        мест = len(МЕСТА[язык])
        видов = len(T.ВЕЩИ[язык])
        for i in range(мест):
            for спрошено in range(мест):
                for форма in ("место_названо", "место_чужое"):
                    вон.append((_образец(язык, рамка(язык, форма, (i,), спрошено)),
                                язык, форма, (i,), спрошено, None))
            for Тспр in range(видов):
                вон.append((_образец(язык, рамка(язык, "вещь_чужая", (i,), i, Тспр=Тспр)),
                            язык, "вещь_чужая", (i,), i, Тспр))
            i2 = (i + 1) % мест
            for спрошено in range(мест):
                # РАМКА ЕСТЬ ФОРМА, А ЗАКОН — СУДЬИ: страница, отвечающая о неназванном
                # месте, и страница, отказывающая о названном, суть рамки дома и его ложь
                for форма in ("два_места", "третье_место"):
                    вон.append((_образец(язык, рамка(язык, форма, (i, i2), спрошено)),
                                язык, форма, (i, i2), спрошено, None))
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


def _вердикт(язык, форма, где, спрошено, зн):
    числа = []
    for k in range(len(где)):
        номер = "" if k == 0 else str(k + 1)
        if "n%s" % номер not in зн:
            return False
        числа.append(int(зн["n%s" % номер]))
    if any(c < 1 for c in числа):
        return False
    виды = None
    for k, c in enumerate(числа):
        номер = "" if k == 0 else str(k + 1)
        свои = {Т for Т in T.ФОРМЫ_ВЕЩЕЙ[язык].get(зн["Тn%s" % номер], set())
                if Т != "строка" and S._счёт(T.ВЕЩИ[язык][Т], c, язык) == зн["Тn%s" % номер]}
        if not свои:
            return False
        виды = свои if виды is None else виды & свои
        if not виды:
            return False
        if язык in T.ЕСТЬ and зн.get("ЕСТЬ%s" % номер) != T._есть(язык, c):
            return False
    if форма in ("место_названо", "два_места"):
        # ОТВЕЧАЕТ ЛИШЬ ТО МЕСТО, О КОТОРОМ ИСТОРИЯ ГОВОРИЛА
        return спрошено in где
    if форма in ("место_чужое", "третье_место"):
        # ОТКАЗ ЗАКОНЕН ЛИШЬ ТАМ, ГДЕ ИСТОРИЯ О СПРОШЕННОМ МЕСТЕ МОЛЧАЛА
        return спрошено not in где
    # вещь_чужая: спрошенная вещь не есть вещь истории (рамка несёт обе, и они различны)
    return True


def судить(строка):
    """(судимо, истинно): a page of a frame of the house whose refusal is grounded; else silence."""
    с = строка.strip()
    if с in ПОКАЗЫ:
        return True, True
    for образ, язык, форма, где, спрошено, Тспр in ОБРАЗЦЫ:
        м = образ.match(с)
        if not м:
            continue
        зн = _значения(м)
        if зн is None:
            return True, False
        return True, _вердикт(язык, форма, где, спрошено, зн)
    return False, False


def _самопроверка():
    for показ in ПОКАЗЫ:
        assert судить(показ) == (True, True), показ
    мутанты = 0
    for язык in ЯЗЫКИ:
        Т, n = 0, 5
        # (1) ОТКАЗ О МЕСТЕ, КОТОРОЕ ИСТОРИЯ НАЗВАЛА
        ч = страница(язык, "место_чужое", (0,), 1, Т, n)
        assert судить(ч) == (True, True), ч
        битая = страница(язык, "место_чужое", (0,), 0, Т, n)
        assert судить(битая) == (True, False), битая
        # (2) ОТВЕТ О МЕСТЕ, КОТОРОГО ИСТОРИЯ НЕ НАЗЫВАЛА
        битая = страница(язык, "место_названо", (0,), 1, Т, n)
        assert судить(битая) == (True, False), битая
        # (3) ТРЕТЬЕ МЕСТО: отказ о названном из двух
        т = страница(язык, "третье_место", (0, 1), 2, Т, n, n2=7)
        assert судить(т) == (True, True), т
        битая = страница(язык, "третье_место", (0, 1), 1, Т, n, n2=7)
        assert судить(битая) == (True, False), битая
        # (4) ДВА МЕСТА: ответ о третьем, неназванном
        д = страница(язык, "два_места", (0, 1), 1, Т, n, n2=7)
        assert судить(д) == (True, True), д
        битая = страница(язык, "два_места", (0, 1), 2, Т, n, n2=7)
        assert судить(битая) == (True, False), битая
        мутанты += 4
        # (5) СЧЁТНАЯ ФОРМА ЧУЖОГО ЧИСЛА
        своя, чужая = _вещь(язык, Т, n), _вещь(язык, Т, 1)
        if своя != чужая:
            м = страница(язык, "место_названо", (0,), 0, Т, n)
            битая = м.replace("%d %s" % (n, своя), "%d %s" % (n, чужая), 1)
            assert судить(битая) == (True, False), битая
            мутанты += 1
        # (6) ЗАЧИН ВОПРОСА ОБЪЯВЛЕН ДОМОМ ПАРЫ
        в = страница(язык, "вещь_чужая", (0,), 0, Т, n, Тспр=1)
        for стр in (ч, т, д, в):
            вопрос = стр[:стр.index("?") + 1].split(". ")[-1]
            assert asking.зачин_объявлен(вопрос) is not False, (язык, вопрос)
    for язык in ЯЗЫКИ:
        print("  ", страница(язык, "место_чужое", (0,), 1, 0, 5))
    for язык in ("ru", "en", "de", "pl"):
        print("  ", страница(язык, "вещь_чужая", (0,), 0, 0, 5, Тспр=1))
        print("  ", страница(язык, "третье_место", (0, 1), 2, 0, 5, n2=7))
    по_форме = {}
    for _, (язык, форма) in ПОКАЗЫ.items():
        по_форме[форма] = по_форме.get(форма, 0) + 1
    print(f"  мутантов поймано: {мутанты}")
    print(f"  дом пишет показов: {len(ПОКАЗЫ)} (языков {len(ЯЗЫКИ)}, форм {len(ФОРМЫ)}, образцов {len(ОБРАЗЦЫ)}): "
          + ", ".join(f"{ф} {к}" for ф, к in по_форме.items()))


if __name__ == "__main__":
    _самопроверка()
