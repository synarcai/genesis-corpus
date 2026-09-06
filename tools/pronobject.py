#!/usr/bin/env python3
"""TRANSFER WITH A PRONOUN OBJECT — the receiver named once, then only pointed at (06.09).

ASKED FOR BY holon (measure of omega-ad on p156/FULL). SVAMP tact 458 — «Jack gave HIM 20 marbles.
Josh had 22 before…» — is answered 22 instead of 42, and it falls on one thing: «him/her/them» are
not bought as pronouns. The market of pronouns votes with the word BEFORE the verb (the actor's
place); the OBJECT'S place never votes at all. The свод cannot fix that by asking, because it does
not carry the shape: «him» 12 lines, «gave her» 10 on the whole FULL.

WHAT IS SHOWN. Two bearers are named with their counts in the FIRST clause; the second clause
transfers a number, and its receiver is a PRONOUN — the antecedent is the SECOND-named person, so
a reader that binds the pronoun to the first name (or to the subject) answers with the wrong
ledger. The page then asks about ONE of the two, and both askings exist:

  отдающий   — «how many does the GIVER have now?» — the ledger SUBTRACTS (n − m);
  получатель — the same head, «how many does the RECEIVER have now?» — the ledger ADDS (k + m).

The mirror is the point. One ledger alone lets a reader answer by a rule of position («the number
of the first person, minus»); with both, the question decides which ledger is meant, and the
pronoun decides who the question is about.

THREE PRONOUNS, EACH WITH ITS OWN PAGE: she, he, they. The genders are not decoration — the giver
is of the other gender in every page, so the pronoun cannot be resolved by «the only person there
is», and in Russian and Polish the giver's own verb MOVES with the giver's gender («Ваня дал» /
«Аня дала», «Marek dał» / «Maria dała») while the object pronoun moves with the receiver.

THE PLACE OF THE OBJECT IS ADJACENCY TO THE VERB, NOT DISTANCE TO THE NUMBER — and the languages
put it on different sides, which is declared rather than smoothed:

  after the verb .......... ru «дал ЕЙ 8», en «gave HER 8», de «gab IHR 8», nl «gaf HAAR 8»,
                            pl «dał JEJ 8»
  before the verb ......... fr «LUI a donné 8», es «LE dio 8», it «LE ha dato 8»
  fused to the verb ....... pt «deu-LHE 8»
  after the whole verb .... it plural «ha dato LORO 8» — Italian has no unambiguous plural clitic
                            in this slot, and the honest form is the postposed one

AND A SECOND DECLARED DIVERGENCE: French and Spanish DO NOT MARK GENDER in this pronoun at all —
«lui» and «le» serve both «to him» and «to her», and only the plural moves («leur», «les»). A
reader taught that the object pronoun carries gender would be taught a fact that two of the nine
languages do not have. Both singulars are shown in every language, so the collapse is visible.

WHAT IS BORROWED: the goods and the counting rule of the house of price; every transfer
construction is one the corpus already carries and judges.

WHAT IS NOT MEASURED, NAMED: the pronoun as SUBJECT of the transfer (the corpus has it), the
reflexive receiver («he gave himself»), and a third clause that transfers again — the frame shows
that the object's place is bought by adjacency, and a chain buys length, not a fact.
"""
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import asking  # noqa: E402 — the house of the pair declares which openers a question may wear
import priceforms as P  # noqa: E402 — the goods and the pack's counting rule

ЯЗЫКИ = ("ru", "en", "de", "fr", "es", "it", "pt", "nl", "pl")
ТОВАРЫ = (1, 2)  # книга и карандаш из дома цены
ЛИЦА = ("она", "он", "они")
ФОРМЫ = ("отдающий", "получатель")
# ТРОЙКИ (было у отдающего, было у получателя, передано); передано < было у отдающего, и все три
# числа разные, чтобы ответ нельзя было взять «тем же числом»
# Ни одно число страницы — ни данное, ни выведенное — не берёт счётной ячейки «one»: дом цены
# объявляет её ЦЕЛОЙ ФРАЗОЙ («один карандаш»), а русский даёт её и 21, и 31, и 101, отчего
# «21 один карандаш» вышла бы ложью письма. Рубеж стоит в самопроверке.
ТРОЙКИ = ((20, 5, 8), (14, 3, 6), (25, 9, 13), (18, 7, 4),
          (32, 12, 15), (11, 6, 3), (27, 8, 19), (16, 4, 7))

# РЕЧЬ. «м»/«ж» — два мужских и два женских имени (М-148: разнообразие, не масса); «род» — форма
# имени там, где её требует рамка (русский родительный при «у», португальский артикль).
РЕЧЬ = {
    "ru": dict(
        м=("Ваня", "Дима"), ж=("Аня", "Лена"), пара=("Аня и Оля",),
        род={"Ваня": "Вани", "Дима": "Димы", "Аня": "Ани", "Лена": "Лены", "Аня и Оля": "Ани и Оли"},
        дал={"м": "дал", "ж": "дала"},
        имел={"м": "было", "ж": "было", "мн": "было"}, имеет={"ед": "", "мн": ""},
        мест={"она": "ей", "он": "ему", "они": "им"},
        было="у {Ар} {имелА} {N}, а у {Бр} {имелБ} {K}.",
        дача="{А} {дал} {мест} {M}.",
        вопрос="сколько {Тмн} у {Кр} теперь?", двоеточие=": "),
    "en": dict(
        м=("Ben", "Tom"), ж=("Ann", "Kate"), пара=("Ann and Kate",),
        род={}, дал={"м": "gave", "ж": "gave"},
        имел={"м": "had", "ж": "had", "мн": "had"}, имеет={"ед": "does", "мн": "do"},
        мест={"она": "her", "он": "him", "они": "them"},
        было="{Ар} {имелА} {N} and {Бр} {имелБ} {K}.",
        дача="{А} {дал} {мест} {M}.",
        вопрос="how many {Тмн} {имеет} {Кр} have now?", двоеточие=": "),
    "de": dict(
        м=("Ben", "Jonas"), ж=("Anna", "Mia"), пара=("Anna und Mia",),
        род={}, дал={"м": "gab", "ж": "gab"},
        имел={"м": "hatte", "ж": "hatte", "мн": "hatten"}, имеет={"ед": "hat", "мн": "haben"},
        мест={"она": "ihr", "он": "ihm", "они": "ihnen"},
        было="{Ар} {имелА} {N} und {Бр} {имелБ} {K}.",
        дача="{А} {дал} {мест} {M}.",
        вопрос="wie viele {Тмн} {имеет} {Кр} jetzt?", двоеточие=": "),
    "fr": dict(
        м=("Hugo", "Louis"), ж=("Léa", "Zoé"), пара=("Léa et Zoé",),
        род={}, дал={"м": "a donné", "ж": "a donné"},
        имел={"м": "avait", "ж": "avait", "мн": "avaient"}, имеет={"ед": "a", "мн": "ont"},
        мест={"она": "lui", "он": "lui", "они": "leur"},
        было="{Ар} {имелА} {N} et {Бр} {имелБ} {K}.",
        дача="{А} {мест} {дал} {M}.",
        вопрос="combien de {Тмн} {имеет} {Кр} maintenant ?", двоеточие=" : "),
    "es": dict(
        м=("Carlos", "Pablo"), ж=("Ana", "Elena"), пара=("Ana y Elena",),
        род={}, дал={"м": "dio", "ж": "dio"},
        имел={"м": "tenía", "ж": "tenía", "мн": "tenían"}, имеет={"ед": "tiene", "мн": "tienen"},
        мест={"она": "le", "он": "le", "они": "les"},
        было="{Ар} {имелА} {N} y {Бр} {имелБ} {K}.",
        дача="{А} {мест} {дал} {M}.",
        вопрос="¿{сколько} {Тмн} {имеет} {Кр} ahora?", двоеточие=": "),
    "it": dict(
        м=("Matteo", "Luca"), ж=("Giulia", "Sara"), пара=("Giulia e Sara",),
        род={}, дал={"м": "ha dato", "ж": "ha dato"},
        имел={"м": "aveva", "ж": "aveva", "мн": "avevano"}, имеет={"ед": "ha", "мн": "hanno"},
        мест={"она": "le", "он": "gli", "они": "loro"},
        было="{Ар} {имелА} {N} e {Бр} {имелБ} {K}.",
        # ИТАЛЬЯНСКОЕ МНОЖЕСТВЕННОЕ СТОИТ ПОСЛЕ ГЛАГОЛА («ha dato loro»), единственное — перед
        дача="{А} {мест} {дал} {M}.", дача_они="{А} {дал} {мест} {M}.",
        вопрос="{сколько} {Тмн} {имеет} {Кр} adesso?", двоеточие=": "),
    "pt": dict(
        м=("o Tiago", "o Rui"), ж=("a Inês", "a Ana"), пара=("a Inês e a Ana",),
        род={}, дал={"м": "deu", "ж": "deu"},
        имел={"м": "tinha", "ж": "tinha", "мн": "tinham"}, имеет={"ед": "tem", "мн": "têm"},
        мест={"она": "-lhe", "он": "-lhe", "они": "-lhes"},
        было="{Ар} {имелА} {N} e {Бр} {имелБ} {K}.",
        дача="{А} {дал}{мест} {M}.",
        вопрос="{сколько} {Тмн} {имеет} {Кр} agora?", двоеточие=": "),
    "nl": dict(
        м=("Bram", "Daan"), ж=("Lotte", "Eva"), пара=("Lotte en Eva",),
        род={}, дал={"м": "gaf", "ж": "gaf"},
        имел={"м": "had", "ж": "had", "мн": "hadden"}, имеет={"ед": "heeft", "мн": "hebben"},
        мест={"она": "haar", "он": "hem", "они": "hun"},
        было="{Ар} {имелА} {N} en {Бр} {имелБ} {K}.",
        дача="{А} {дал} {мест} {M}.",
        вопрос="hoeveel {Тмн} {имеет} {Кр} nu?", двоеточие=": "),
    "pl": dict(
        м=("Marek", "Piotr"), ж=("Maria", "Zofia"), пара=("Maria i Zofia",),
        род={}, дал={"м": "dał", "ж": "dała"},
        имел={"м": "miał", "ж": "miała", "мн": "miały"}, имеет={"ед": "ma", "мн": "mają"},
        мест={"она": "jej", "он": "mu", "они": "im"},
        было="{Ар} {имелА} {N}, a {Бр} {имелБ} {K}.",
        дача="{А} {дал} {мест} {M}.",
        вопрос="ile {Тмн} {имеет} {Кр} teraz?", двоеточие=": "),
}

# РОД ТОВАРА И СОГЛАСОВАНИЕ ПО НЕМУ — ОБЪЯВЛЕНЫ (тот же закон, что в доме родственника):
# итальянское вопросительное гнётся по роду вещи («quanti libri» — «quante matite»), испанское и
# португальское тоже. Шесть прочих языков рода здесь не метят, и это сказано, а не умолчано.
РОД_ТОВАРА = {"it": {1: "м", 2: "ж"}, "es": {1: "м", 2: "м"}, "pt": {1: "м", 2: "м"}}
ПО_РОДУ = {
    "it": {"сколько": {"м": "quanti", "ж": "quante"}},
    "es": {"сколько": {"м": "cuántos", "ж": "cuántas"}},
    "pt": {"сколько": {"м": "quantos", "ж": "quantas"}},
}


def вещей(язык, i, n):
    return "%d %s" % (n, P.форма(язык, P.ЯЗЫКИ[язык]["вещи"][i], n))


def множ(язык, i):
    """Счётная форма множества — ею спрашивают «сколько»."""
    ф = P.ЯЗЫКИ[язык]["вещи"][i]
    return ф["many"] if isinstance(ф, dict) else ф[-1]


def _род(язык, имя):
    return РЕЧЬ[язык]["род"].get(имя, имя)


def _лица(язык, лицо, шаг):
    """(отдающий, его род, получатель, его род). Отдающий ВСЕГДА другого рода, чем получатель:
    местоимение нельзя разрешить «единственным, кто там есть»."""
    р = РЕЧЬ[язык]
    if лицо == "она":
        А, Б, ра = р["м"][шаг % len(р["м"])], р["ж"][0], "м"
    elif лицо == "он":
        А, Б, ра = р["ж"][шаг % len(р["ж"])], р["м"][0], "ж"
    else:
        А, Б, ра = р["м"][шаг % len(р["м"])], р["пара"][0], "м"
    return А, Б, ра


_ПОЛ_ЛИЦА = {"она": "ж", "он": "м", "они": "мн"}


def _сколько(язык, i):
    """Вопросительное слово, согласованное с РОДОМ ТОВАРА там, где язык его гнёт."""
    род = РОД_ТОВАРА.get(язык, {}).get(i)
    return ПО_РОДУ[язык]["сколько"][род] if род else ""


def _глаголы(язык, форма, лицо, ра):
    """Глагол «иметь» у каждого из двух и глагол вопроса: МНОЖЕСТВЕННОЕ ПРИ ДВУХ ПОЛУЧАТЕЛЯХ.

    Семь языков из девяти двигают здесь глагол («hatten», «avaient», «tenían», «avevano»,
    «tinham», «hadden», «miały», и английское «do» против «does»); русский не двигает вовсе.
    Дом, взявший единственное на оба места, написал бы «Léa et Zoé avait» — ложь письма.
    """
    р = РЕЧЬ[язык]
    полб = _ПОЛ_ЛИЦА[лицо]
    множ_вопрос = (форма == "получатель" and лицо == "они")
    return (р["имел"][ра], р["имел"][полб],
            р["имеет"]["мн" if множ_вопрос else "ед"])


def страница(язык, форма, i, лицо, шаг):
    р = РЕЧЬ[язык]
    n, k, m = ТРОЙКИ[шаг]
    А, Б, ра = _лица(язык, лицо, шаг)
    имелА, имелБ, имеет = _глаголы(язык, форма, лицо, ра)
    голова = (р["было"].format(Ар=_род(язык, А), Бр=_род(язык, Б), имелА=имелА, имелБ=имелБ,
                               N=вещей(язык, i, n), K=вещей(язык, i, k))
              + " " + (р.get("дача_они") if лицо == "они" and "дача_они" in р else р["дача"])
              .format(А=А, дал=р["дал"][ра], мест=р["мест"][лицо], M=вещей(язык, i, m)))
    кто = А if форма == "отдающий" else Б
    итог = n - m if форма == "отдающий" else k + m
    знак = "−" if форма == "отдающий" else "+"
    лево = n if форма == "отдающий" else k
    return (голова + " " + р["вопрос"].format(Тмн=множ(язык, i), Кр=_род(язык, кто),
                                              имеет=имеет, **{"сколько": _сколько(язык, i)}) + " "
            + вещей(язык, i, итог) + р["двоеточие"] + f"{лево} {знак} {m} = {итог}.")


def _показы():
    вон = {}
    for язык in ЯЗЫКИ:
        for i in ТОВАРЫ:
            for лицо in ЛИЦА:
                for шаг in range(len(ТРОЙКИ)):
                    for форма in ФОРМЫ:
                        вон[страница(язык, форма, i, лицо, шаг)] = (язык, форма, лицо)
    return вон


ПОКАЗЫ = _показы()


def _альт(слова):
    сорт = sorted({с for с in слова if с}, key=lambda с: (-len(с), с))
    return "(?:" + "|".join(re.escape(с) for с in сорт) + ")"


def _имена(язык):
    р = РЕЧЬ[язык]
    прямые = list(р["м"]) + list(р["ж"]) + list(р["пара"])
    return прямые + [_род(язык, и) for и in прямые]


def _дыры(язык, i):
    ф = P.ЯЗЫКИ[язык]["вещи"][i]
    формы = _альт(ф.values() if isinstance(ф, dict) else ф)
    число = r"\d+ " + формы
    р = РЕЧЬ[язык]
    имена = _альт(_имена(язык))
    return {"N": число, "K": число, "M": число, "S": число,
            "А": имена, "Ар": имена, "Бр": имена, "Кр": имена,
            # МЕСТОИМЕНИЕ — ОБЪЯВЛЕННОЕ СЛОВО, А НЕ ЛЮБОЕ
            "мест": _альт(р["мест"].values()), "дал": _альт(р["дал"].values()),
            # ГЛАГОЛЫ — ОБЪЯВЛЕННЫЕ ФОРМЫ, А НЕ ЛЮБЫЕ СЛОВА
            "имелА": _альт(р["имел"].values()), "имелБ": _альт(р["имел"].values()),
            "имеет": _альт(р["имеет"].values()) if any(р["имеет"].values()) else "(?:)",
            # ВОПРОСИТЕЛЬНОЕ — ЯЧЕЙКА, А НЕ БУКВА РАМКИ: иначе «quanti matite» стала бы
            # НЕСУДИМОЙ, а суд обязан назвать её ЛОЖЬЮ и сказать, чем именно она ложна
            "сколько": _альт(ПО_РОДУ[язык]["сколько"].values()) if язык in ПО_РОДУ else "(?:)"}


_ЧИСЛА = {"n": r"(?P<n>\d+)", "m": r"(?P<m>\d+)", "s": r"(?P<s>\d+)"}


def рамка(язык, форма, i, лицо):
    р = РЕЧЬ[язык]
    голова = (р["было"].format(Ар="{Ар}", Бр="{Бр}", N="{N}", K="{K}",
                               имелА="{имелА}", имелБ="{имелБ}")
              + " " + (р.get("дача_они") if лицо == "они" and "дача_они" in р else р["дача"])
              .format(А="{А}", дал="{дал}", мест="{мест}", M="{M}"))
    знак = "−" if форма == "отдающий" else "+"
    return (голова + " " + р["вопрос"].format(Тмн=множ(язык, i), Кр="{Кр}", имеет="{имеет}",
                                              **{"сколько": "{сколько}"}) + " {S}"
            + р["двоеточие"] + "{n} " + знак + " {m} = {s}.")


def _образец(язык, форма, i, лицо):
    дыры, счёт, куски = _дыры(язык, i), {}, []
    for кусок in re.split(r"(\{[^}]+\})", рамка(язык, форма, i, лицо)):
        if not кусок.startswith("{"):
            куски.append(re.escape(кусок)); continue
        дыра = кусок[1:-1]
        if дыра in _ЧИСЛА:
            куски.append(_ЧИСЛА[дыра]); continue
        счёт[дыра] = счёт.get(дыра, 0) + 1
        куски.append(f"(?P<h_{дыра}__{счёт[дыра]}>{дыры[дыра]})")
    return re.compile("^" + "".join(куски) + "$")


# ОБРАЗЕЦ НА КАЖДОЕ ЛИЦО ОТДЕЛЬНО: у итальянского множественное стоит по другую сторону глагола,
# и одна рамка на три лица скрыла бы это различие вместо того, чтобы его судить
ОБРАЗЦЫ = [(_образец(язык, форма, i, лицо), язык, форма, i, лицо)
           for язык in ЯЗЫКИ for форма in ФОРМЫ for i in ТОВАРЫ for лицо in ЛИЦА]


def _значения(м):
    вон = {}
    for ключ, знач in м.groupdict().items():
        if not ключ.startswith("h_"):
            вон[ключ] = знач; continue
        дыра, _ = ключ[2:].rsplit("__", 1)
        if дыра in вон and вон[дыра] != знач:
            return None
        вон[дыра] = знач
    return вон


def _число(кусок):
    return int(кусок.split(" ", 1)[0])


def _пол(язык, имя):
    р = РЕЧЬ[язык]
    прямое = next((и for и in _имена(язык) if _род(язык, и) == имя or и == имя), None)
    if прямое is None:
        return None
    if прямое in р["пара"] or _род(язык, прямое) == имя and прямое in р["пара"]:
        return "пара"
    return "м" if прямое in р["м"] else "ж" if прямое in р["ж"] else "пара"


def _вердикт(язык, форма, i, лицо, зн):
    р = РЕЧЬ[язык]
    вещь = lambda c: вещей(язык, i, c)
    n, k, m = _число(зн["N"]), _число(зн["K"]), _число(зн["M"])
    # ОТДАЮЩИЙ ЕСТЬ ПЕРВЫЙ НАЗВАННЫЙ, ПОЛУЧАТЕЛЬ — ВТОРОЙ, И ОНИ РАЗНЫЕ
    if зн["Ар"] == зн["Бр"] or _род(язык, зн["А"]) != зн["Ар"]:
        return False
    # МЕСТОИМЕНИЕ ЕСТЬ МЕСТОИМЕНИЕ ПОЛУЧАТЕЛЯ, А НЕ ЛЮБОЕ ОБЪЯВЛЕННОЕ
    if зн["мест"] != р["мест"][лицо]:
        return False
    полб = _пол(язык, зн["Бр"])
    if полб is None or (лицо == "они") != (полб == "пара"):
        return False
    if лицо in ("она", "он") and полб != ("ж" if лицо == "она" else "м"):
        return False
    # ГЛАГОЛ ОТДАЮЩЕГО СОГЛАСОВАН С ЕГО РОДОМ (там, где язык его двигает)
    пола = _пол(язык, зн["Ар"])
    if пола not in ("м", "ж") or зн["дал"] != р["дал"][пола]:
        return False
    # ГЛАГОЛЫ «ИМЕТЬ» И ВОПРОСА — ТЕ, ЧТО НАЗНАЧАЮТ РОД ОТДАЮЩЕГО И ЧИСЛО ПОЛУЧАТЕЛЯ
    имелА, имелБ, имеет = _глаголы(язык, форма, лицо, пола)
    if зн["имелА"] != имелА or зн["имелБ"] != имелБ:
        return False
    if зн.get("имеет", "") != имеет:
        return False
    # ВОПРОСИТЕЛЬНОЕ СОГЛАСОВАНО С РОДОМ ТОВАРА (там, где язык его гнёт)
    if язык in ПО_РОДУ and зн.get("сколько") != _сколько(язык, i):
        return False
    if m >= n:
        return False
    # ВОПРОС РЕШАЕТ, ЧЕЙ ЛЕДЖЕР: у отдающего вычитание, у получателя сложение
    if форма == "отдающий":
        кто, лево, итог = зн["Ар"], n, n - m
    else:
        кто, лево, итог = зн["Бр"], k, k + m
    if зн["Кр"] != кто:
        return False
    if (int(зн["n"]), int(зн["m"]), int(зн["s"])) != (лево, m, итог):
        return False
    return зн["N"] == вещь(n) and зн["K"] == вещь(k) and зн["M"] == вещь(m) and зн["S"] == вещь(итог)


def судить(строка):
    """(судимо, истинно): a transfer whose receiver is a pronoun, and whose ledger is the asked one."""
    с = строка.strip()
    if с in ПОКАЗЫ:
        return True, True
    for образ, язык, форма, i, лицо in ОБРАЗЦЫ:
        м = образ.match(с)
        if not м:
            continue
        зн = _значения(м)
        if зн is None:
            return True, False
        return True, _вердикт(язык, форма, i, лицо, зн)
    return False, False


# ЧИСЛИТЕЛЬНОЕ ПРИ ЦИФРЕ — тот же рубеж, что в доме родственника: ячейка «one» дома цены несёт
# само слово, и русский даёт её 21, 31, 41, 101, отчего «21 один карандаш» была бы ложью письма.
_ЧИСЛИТЕЛЬНОЕ_ПРИ_ЦИФРЕ = re.compile(
    r"\d+ (?:один|одна|одно|jeden|jedna|jedno|one |un |una |uno |ein |eine |uma )")


def _самопроверка():
    for показ in ПОКАЗЫ:
        assert судить(показ) == (True, True), показ
    при_цифре = [с for с in ПОКАЗЫ if _ЧИСЛИТЕЛЬНОЕ_ПРИ_ЦИФРЕ.search(с)]
    assert not при_цифре, при_цифре[:3]
    # РУБЕЖ РОДА ТОВАРА: объявленный род покрывает каждый товар языка, который его метит
    for язык, роды in РОД_ТОВАРА.items():
        assert set(роды) == set(ТОВАРЫ), (язык, sorted(роды), sorted(ТОВАРЫ))
        for ключ, формы in ПО_РОДУ[язык].items():
            for i in ТОВАРЫ:
                assert роды[i] in формы, (язык, ключ, i, роды[i])
    мутанты = 0
    for язык in ЯЗЫКИ:
        р = РЕЧЬ[язык]
        о = страница(язык, "отдающий", 1, "она", 0)          # 20, 5, 8
        п = страница(язык, "получатель", 1, "она", 0)
        # (1) ЛЕДЖЕР ОТДАЮЩЕГО ПОДСТАВЛЕН ПОЛУЧАТЕЛЮ — та самая ложь такта 458
        битая = п.replace("5 + 8 = 13", "20 − 8 = 12").replace("? " + вещей(язык, 1, 13),
                                                               "? " + вещей(язык, 1, 12))
        assert судить(битая) == (True, False), битая
        # (2) ЛЕДЖЕР НЕ СХОДИТСЯ
        битая = о.replace("20 − 8 = 12", "20 − 8 = 13")
        assert судить(битая) == (True, False), битая
        # (3) ВЫЧИТАНИЕ ОБРАЩЕНО
        битая = о.replace("20 − 8 = 12", "8 − 20 = 12")
        assert судить(битая) == (True, False), битая
        мутанты += 3
        # (4) МЕСТОИМЕНИЕ ЧУЖОГО ЛИЦА (только там, где язык их различает)
        если = р["мест"]
        if если["она"] != если["он"]:
            битая = о.replace(р["дача"].format(А="", дал=р["дал"]["м"], мест=если["она"], M="").strip(),
                              р["дача"].format(А="", дал=р["дал"]["м"], мест=если["он"], M="").strip())
            if битая != о:
                assert судить(битая) == (True, False), битая
                мутанты += 1
        # (5) ГЛАГОЛ ОТДАЮЩЕГО НЕ ПО ЕГО РОДУ (только там, где язык его двигает)
        if р["дал"]["м"] != р["дал"]["ж"]:
            битая = о.replace(f' {р["дал"]["м"]} ', f' {р["дал"]["ж"]} ')
            assert судить(битая) == (True, False), битая
            мутанты += 1
        # (6) ЗАЧИН ВОПРОСА ОБЪЯВЛЕН ДОМОМ ПАРЫ
        for стр in (о, п):
            голова = стр[:стр.index("?") + 1]
            вопрос = голова[голова.rindex(". ") + 2:] if ". " in голова else голова
            assert asking.зачин_объявлен(вопрос) is not False, (язык, вопрос)
    for язык in ЯЗЫКИ:
        print("  ", страница(язык, "отдающий", 1, "она", 0))
    for язык in ("ru", "fr", "it", "pt", "pl"):
        print("  ", страница(язык, "получатель", 1, "он", 1))
        print("  ", страница(язык, "получатель", 2, "они", 2))
    по_лицу = {}
    for _, (_я, _ф, лицо) in ПОКАЗЫ.items():
        по_лицу[лицо] = по_лицу.get(лицо, 0) + 1
    на_язык = len(ПОКАЗЫ) // len(ЯЗЫКИ)
    print(f"  мутантов поймано: {мутанты}")
    print(f"  дом пишет показов: {len(ПОКАЗЫ)} (языков {len(ЯЗЫКИ)}, образцов {len(ОБРАЗЦЫ)}): "
          + ", ".join(f"{л} {к}" for л, к in по_лицу.items()))
    print(f"  на язык {на_язык}, на язык и лицо {на_язык // len(ЛИЦА)}")


if __name__ == "__main__":
    _самопроверка()
