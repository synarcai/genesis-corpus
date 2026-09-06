#!/usr/bin/env python3
"""THE PRO-FORM OF THE GOODS — the thing named once, then stood in for (06.09).

ASKED FOR BY omega-ad. SVAMP tact 510 — «lost 11 marbles and found 5 new ones» — is answered 8
instead of 13: «ones» is not bought as a GOODS, the fact it carries is left unplaced, and the
number rides on nothing. The свод cannot teach it, because it barely has it:

    «N new ones» ................. 24 lines, ALL in one world, ALL English, ONE frame, ONE goods
    «N ones» of any kind ......... the same 24
    ru «столько же» / «таких же» .. 4 / 0
    the pro-form in the other seven languages ... nothing of this shape

Twenty-four lines of one frame in one language do not buy a pro-form. A market that has met
«ones» only after «red apples» has met a collocation, not a stand-in.

WHAT A PAGE MUST BUY:
  · the pro-form is not a NEW goods — the ledger adds it to the goods named BEFORE it, and a
    reader that takes «5 new ones» for a fifth thing answers with the wrong total;
  · the pro-form survives a SUBTRACTION in between: «I had 20, I lost 11 and found 5 new ones» is
    two steps, and the second stands on the first. This is tact 510 exactly, and it is the frame
    that tells resolution from luck: a reader that adds where it should subtract, or that binds
    «new ones» to the number 11 instead of the goods, lands on 8 rather than 14;
  · the goods can be named ONCE and then elided EVERYWHERE — in the pro-form and in the question
    alike — and only the ANSWER names it again. A question that repeats the goods lets the reader
    skip the resolution entirely.

THE SHAPE OF THE PRO-FORM IS ITSELF A SHOWN FACT, and the languages part company twice:

  · ENGLISH CANNOT ELIDE THE NOUN after an adjective — it must prop it with «ones» («5 new
    ones»). The other eight leave the bare adjective («5 новых», «5 neue», «5 nouvelles»,
    «5 nuevas», «5 nuove», «5 novas», «5 nieuwe», «5 nowych»), and the adjective AGREES with the
    gender of the elided noun where the language marks it (fr/es/it/pt: «5 nouvelles» pommes
    against «5 nouveaux» livres);
  · the QUESTION with the goods elided takes a partitive clitic in French and Italian («combien
    EN ai-je», «quante NE ho») and nothing at all in the other seven. A reader taught that the
    elided question must carry a clitic would be taught a fact seven of the nine do not have.

WHY THE COUNT OF THE PRO-FORM IS NEVER TWO, THREE OR FOUR: with the noun elided, Russian and
Polish put the adjective in the genitive plural after five and up («5 новых») but in the
nominative plural after two to four («три новые»), and which of the two a headless phrase takes
is not settled by the corpus's own witness. The house shows the settled case and NAMES the
unsettled one rather than guessing at it.

WHAT IS BORROWED: the goods and the counting rule of the house of price.

WHAT IS NOT MEASURED, NAMED: the pro-form over TWO candidate goods («I have 7 books and 10 apples
and 5 new ones») — genuinely ambiguous in English and not a thing to teach; the pro-form of a
person («the tall one»); and the pro-form standing for a goods named in a NEIGHBOURING line — a
show must carry what it needs.
"""
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import asking  # noqa: E402 — the house of the pair declares which openers a question may wear
import priceforms as P  # noqa: E402 — the goods and the pack's counting rule

ЯЗЫКИ = ("ru", "en", "de", "fr", "es", "it", "pt", "nl", "pl")
ТОВАРЫ = (0, 1)  # яблоко (женского рода в романских) и книга — род различает согласование
ФОРМЫ = ("прибавка", "два_шага", "без_товара")
# ЧИСЛО ПРО-ФОРМЫ ВСЕГДА ≥ 5 (см. объявление дома); ни одно число страницы — ни данное, ни
# выведенное — не берёт счётной ячейки «one», несущей само числительное
ПАРЫ = ((10, 5), (11, 6), (13, 7), (14, 8), (20, 9), (25, 12))
ТРОЙКИ = ((20, 11, 5), (25, 13, 6), (30, 14, 8), (24, 10, 9))

# РОД ТОВАРА И СОГЛАСОВАНИЕ ПО НЕМУ — ОБЪЯВЛЕНЫ, а не угаданы: прилагательное при опущенном
# имени гнётся по роду ИМЕННО ТОГО имени, которого нет на странице, и вывести его неоткуда.
РОД_ТОВАРА = {"fr": {0: "ж", 1: "м"}, "es": {0: "ж", 1: "м"},
              "it": {0: "ж", 1: "м"}, "pt": {0: "ж", 1: "м"}}
НОВЫЕ = {
    "ru": {"м": "новых", "ж": "новых"},
    "en": {"м": "new ones", "ж": "new ones"},
    "de": {"м": "neue", "ж": "neue"},
    "fr": {"м": "nouveaux", "ж": "nouvelles"},
    "es": {"м": "nuevos", "ж": "nuevas"},
    "it": {"м": "nuovi", "ж": "nuove"},
    "pt": {"м": "novos", "ж": "novas"},
    "nl": {"м": "nieuwe", "ж": "nieuwe"},
    "pl": {"м": "nowych", "ж": "nowych"},
}
# ВОПРОСИТЕЛЬНОЕ ПРИ ОПУЩЕННОМ ИМЕНИ тоже гнётся по роду там, где язык его метит
СКОЛЬКО = {
    "fr": {"м": "combien", "ж": "combien"},
    "es": {"м": "cuántos", "ж": "cuántas"},
    "it": {"м": "quanti", "ж": "quante"},
    "pt": {"м": "quantos", "ж": "quantas"},
}

РЕЧЬ = {
    "ru": dict(
        есть="у меня {N} и {M}.", вопрос="сколько у меня {Тмн}?",
        было="у меня было {N}.", потерял="я потерял {K} и нашёл {M}.",
        вопрос_теперь="сколько у меня {Тмн} теперь?",
        есть_кратко="у меня {N}.", купил="я покупаю {M}.",
        вопрос_без="сколько у меня теперь?", двоеточие=": "),
    "en": dict(
        есть="i have {N} and {M}.", вопрос="how many {Тмн} do i have?",
        было="i had {N}.", потерял="i lost {K} and found {M}.",
        вопрос_теперь="how many {Тмн} do i have now?",
        есть_кратко="i have {N}.", купил="i buy {M}.",
        вопрос_без="how many do i have now?", двоеточие=": "),
    "de": dict(
        есть="ich habe {N} und {M}.", вопрос="wie viele {Тмн} habe ich?",
        было="ich hatte {N}.", потерял="ich verlor {K} und fand {M}.",
        вопрос_теперь="wie viele {Тмн} habe ich jetzt?",
        есть_кратко="ich habe {N}.", купил="ich kaufe {M}.",
        вопрос_без="wie viele habe ich jetzt?", двоеточие=": "),
    "fr": dict(
        есть="j'ai {N} et {M}.", вопрос="combien de {Тмн} ai-je ?",
        было="j'avais {N}.", потерял="j'ai perdu {K} et trouvé {M}.",
        вопрос_теперь="combien de {Тмн} ai-je maintenant ?",
        есть_кратко="j'ai {N}.", купил="j'achète {M}.",
        вопрос_без="combien en ai-je maintenant ?", двоеточие=" : "),
    "es": dict(
        есть="tengo {N} y {M}.", вопрос="¿{сколько} {Тмн} tengo?",
        было="tenía {N}.", потерял="perdí {K} y encontré {M}.",
        вопрос_теперь="¿{сколько} {Тмн} tengo ahora?",
        есть_кратко="tengo {N}.", купил="compro {M}.",
        вопрос_без="¿{сколько} tengo ahora?", двоеточие=": "),
    "it": dict(
        есть="ho {N} e {M}.", вопрос="{сколько} {Тмн} ho?",
        было="avevo {N}.", потерял="ho perso {K} e trovato {M}.",
        вопрос_теперь="{сколько} {Тмн} ho adesso?",
        есть_кратко="ho {N}.", купил="compro {M}.",
        вопрос_без="{сколько} ne ho adesso?", двоеточие=": "),
    "pt": dict(
        есть="tenho {N} e {M}.", вопрос="{сколько} {Тмн} tenho?",
        было="tinha {N}.", потерял="perdi {K} e encontrei {M}.",
        вопрос_теперь="{сколько} {Тмн} tenho agora?",
        есть_кратко="tenho {N}.", купил="compro {M}.",
        вопрос_без="{сколько} tenho agora?", двоеточие=": "),
    "nl": dict(
        есть="ik heb {N} en {M}.", вопрос="hoeveel {Тмн} heb ik?",
        было="ik had {N}.", потерял="ik verloor {K} en vond {M}.",
        вопрос_теперь="hoeveel {Тмн} heb ik nu?",
        есть_кратко="ik heb {N}.", купил="ik koop {M}.",
        вопрос_без="hoeveel heb ik nu?", двоеточие=": "),
    "pl": dict(
        есть="mam {N} i {M}.", вопрос="ile {Тмн} mam?",
        было="miałem {N}.", потерял="zgubiłem {K} i znalazłem {M}.",
        вопрос_теперь="ile {Тмн} mam teraz?",
        есть_кратко="mam {N}.", купил="kupuję {M}.",
        вопрос_без="ile mam teraz?", двоеточие=": "),
}


def вещей(язык, i, n):
    return "%d %s" % (n, P.форма(язык, P.ЯЗЫКИ[язык]["вещи"][i], n))


def множ(язык, i):
    """Счётная форма множества — ею спрашивают «сколько»."""
    ф = P.ЯЗЫКИ[язык]["вещи"][i]
    return ф["many"] if isinstance(ф, dict) else ф[-1]


def _род(язык, i):
    return РОД_ТОВАРА.get(язык, {}).get(i, "м")


def проформа(язык, i, m):
    """«5 new ones», «5 новых», «5 nouvelles» — ЧИСЛО и прилагательное, имя опущено."""
    return "%d %s" % (m, НОВЫЕ[язык][_род(язык, i)])


def _поля(язык, i):
    п = dict(Тмн=множ(язык, i))
    if язык in СКОЛЬКО:
        п["сколько"] = СКОЛЬКО[язык][_род(язык, i)]
    return п


def страница(язык, форма, i, числа):
    р = РЕЧЬ[язык]
    п = _поля(язык, i)
    дв = р["двоеточие"]
    if форма == "два_шага":
        n, k, m = числа
        итог = n - k + m
        голова = (р["было"].format(N=вещей(язык, i, n), **п) + " "
                  + р["потерял"].format(K=вещей(язык, i, k), M=проформа(язык, i, m), **п))
        return (голова + " " + р["вопрос_теперь"].format(**п) + " " + вещей(язык, i, итог) + дв
                + f"{n} − {k} = {n - k}, {n - k} + {m} = {итог}.")
    n, m = числа
    итог = n + m
    if форма == "прибавка":
        # ПРО-ФОРМА НЕ ЕСТЬ НОВЫЙ ТОВАР: леджер прибавляет её к названному ПЕРЕД ней
        голова = р["есть"].format(N=вещей(язык, i, n), M=проформа(язык, i, m), **п)
        вопрос = р["вопрос"].format(**п)
    else:
        # ТОВАР НАЗВАН ОДИН РАЗ И ОПУЩЕН ВЕЗДЕ — в про-форме и в вопросе; имя возвращает ОТВЕТ
        голова = (р["есть_кратко"].format(N=вещей(язык, i, n), **п) + " "
                  + р["купил"].format(M=проформа(язык, i, m), **п))
        вопрос = р["вопрос_без"].format(**п)
    return голова + " " + вопрос + " " + вещей(язык, i, итог) + дв + f"{n} + {m} = {итог}."


def _показы():
    вон = {}
    for язык in ЯЗЫКИ:
        for i in ТОВАРЫ:
            for числа in ПАРЫ:
                for форма in ("прибавка", "без_товара"):
                    вон[страница(язык, форма, i, числа)] = (язык, форма)
            for числа in ТРОЙКИ:
                вон[страница(язык, "два_шага", i, числа)] = (язык, "два_шага")
    return вон


ПОКАЗЫ = _показы()


def _альт(слова):
    сорт = sorted({с for с in слова if с}, key=lambda с: (-len(с), с))
    return "(?:" + "|".join(re.escape(с) for с in сорт) + ")"


def _дыры(язык, i):
    ф = P.ЯЗЫКИ[язык]["вещи"][i]
    формы = _альт(ф.values() if isinstance(ф, dict) else ф)
    число = r"\d+ " + формы
    # ЯЧЕЙКА ПРО-ФОРМЫ ПРИНИМАЕТ ЛЮБОЕ ОБЪЯВЛЕННОЕ ПРИЛАГАТЕЛЬНОЕ ЯЗЫКА, а не только верное по
    # роду: иначе порча рода стала бы НЕМОТОЙ, и суд, поставленный её ловить, слеп бы на ней
    проф = r"\d+ " + _альт(НОВЫЕ[язык].values())
    дыры = {"N": число, "K": число, "S": число, "M": проф}
    if язык in СКОЛЬКО:
        дыры["сколько"] = _альт(СКОЛЬКО[язык].values())
    return дыры


# ЗНАК ДЕЙСТВИЯ СТОИТ ДЫРОЙ, А НЕ БУКВОЙ (тот же закон, что у констант дома шкалы): подменённый
# знак обязан быть ЛОЖЬЮ, а не немотой. Рамка с «+» буквой сделала бы «9 − 5 = 4» — ложь такта
# 510 в чистом виде — НЕСУДИМОЙ, и суд, поставленный её ловить, слеп бы ровно на ней.
_ЧИСЛА = {"n": r"(?P<n>\d+)", "k": r"(?P<k>\d+)", "m": r"(?P<m>\d+)",
          "r": r"(?P<r>\d+)", "r2": r"(?P<r2>\d+)", "s": r"(?P<s>\d+)",
          "зн1": r"(?P<зн1>[+−])", "зн2": r"(?P<зн2>[+−])", "зн": r"(?P<зн>[+−])"}


def рамка(язык, форма, i):
    р = РЕЧЬ[язык]
    п = dict(Тмн=множ(язык, i))
    if язык in СКОЛЬКО:
        п["сколько"] = "{сколько}"
    дв = р["двоеточие"]
    if форма == "два_шага":
        голова = (р["было"].format(N="{N}", **п) + " " + р["потерял"].format(K="{K}", M="{M}", **п))
        return (голова + " " + р["вопрос_теперь"].format(**п) + " {S}" + дв
                + "{n} {зн1} {k} = {r}, {r2} {зн2} {m} = {s}.")
    if форма == "прибавка":
        голова = р["есть"].format(N="{N}", M="{M}", **п)
        вопрос = р["вопрос"].format(**п)
    else:
        голова = р["есть_кратко"].format(N="{N}", **п) + " " + р["купил"].format(M="{M}", **п)
        вопрос = р["вопрос_без"].format(**п)
    return голова + " " + вопрос + " {S}" + дв + "{n} {зн} {m} = {s}."


def _образец(язык, форма, i):
    дыры, счёт, куски = _дыры(язык, i), {}, []
    for кусок in re.split(r"(\{[^}]+\})", рамка(язык, форма, i)):
        if not кусок.startswith("{"):
            куски.append(re.escape(кусок)); continue
        дыра = кусок[1:-1]
        if дыра in _ЧИСЛА:
            куски.append(_ЧИСЛА[дыра]); continue
        счёт[дыра] = счёт.get(дыра, 0) + 1
        куски.append(f"(?P<h_{дыра}__{счёт[дыра]}>{дыры[дыра]})")
    return re.compile("^" + "".join(куски) + "$")


ОБРАЗЦЫ = [(_образец(язык, форма, i), язык, форма, i)
           for язык in ЯЗЫКИ for форма in ФОРМЫ for i in ТОВАРЫ]


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


def _вердикт(язык, форма, i, зн):
    вещь = lambda c: вещей(язык, i, c)
    n, m = _число(зн["N"]), _число(зн["M"])
    # ПРО-ФОРМА СОГЛАСОВАНА С РОДОМ ОПУЩЕННОГО ИМЕНИ
    if зн["M"] != проформа(язык, i, m):
        return False
    if язык in СКОЛЬКО and зн.get("сколько") != СКОЛЬКО[язык][_род(язык, i)]:
        return False
    if форма == "два_шага":
        k = _число(зн["K"])
        if k >= n:
            return False
        остаток, итог = n - k, n - k + m
        # ЗНАКИ ЛЕДЖЕРА СУДЯТСЯ: первый шаг ОТНИМАЕТ, второй ПРИБАВЛЯЕТ
        if зн["зн1"] != "−" or зн["зн2"] != "+":
            return False
        шаги = (int(зн["n"]), int(зн["k"]), int(зн["r"]), int(зн["r2"]), int(зн["m"]), int(зн["s"]))
        if шаги != (n, k, остаток, остаток, m, итог):
            return False
        return зн["N"] == вещь(n) and зн["K"] == вещь(k) and зн["S"] == вещь(итог)
    итог = n + m
    if зн["зн"] != "+":
        return False
    if (int(зн["n"]), int(зн["m"]), int(зн["s"])) != (n, m, итог):
        return False
    return зн["N"] == вещь(n) and зн["S"] == вещь(итог)


def судить(строка):
    """(судимо, истинно): a page whose pro-form stands for the goods named before it."""
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


_ЧИСЛИТЕЛЬНОЕ_ПРИ_ЦИФРЕ = re.compile(
    r"\d+ (?:один|одна|одно|jeden|jedna|jedno|one |un |una |uno |ein |eine |uma )")


def _самопроверка():
    for показ in ПОКАЗЫ:
        assert судить(показ) == (True, True), показ
    при_цифре = [с for с in ПОКАЗЫ if _ЧИСЛИТЕЛЬНОЕ_ПРИ_ЦИФРЕ.search(с)]
    assert not при_цифре, при_цифре[:3]
    # РУБЕЖ ЧИСЛА ПРО-ФОРМЫ: с опущенным именем русский и польский решены только от пяти
    assert all(m >= 5 for _n, m in ПАРЫ) and all(m >= 5 for _n, _k, m in ТРОЙКИ)
    # РУБЕЖ РОДА: объявление покрывает каждый товар языка, который род метит
    for язык, роды in РОД_ТОВАРА.items():
        assert set(роды) == set(ТОВАРЫ), (язык, sorted(роды))
        for i in ТОВАРЫ:
            assert роды[i] in НОВЫЕ[язык] and роды[i] in СКОЛЬКО[язык], (язык, i)
    мутанты = 0
    for язык in ЯЗЫКИ:
        п = страница(язык, "прибавка", 0, (10, 5))
        # (1) ПРО-ФОРМА ПРИНЯТА ЗА НОВЫЙ ТОВАР: её число не вошло в итог
        битая = п.replace("? " + вещей(язык, 0, 15), "? " + вещей(язык, 0, 10))
        assert судить(битая) == (True, False), битая
        # (2) ЛЕДЖЕР НЕ СХОДИТСЯ
        битая = п.replace("10 + 5 = 15", "10 + 5 = 16")
        assert судить(битая) == (True, False), битая
        мутанты += 2
        д = страница(язык, "два_шага", 1, (20, 11, 5))
        # (3) ЛОЖЬ ТАКТА 510: второй шаг не опирается на первый, ответ 8 вместо 14
        битая = д.replace("20 − 11 = 9, 9 + 5 = 14", "20 − 11 = 9, 9 − 5 = 4")
        assert судить(битая) == (True, False), битая
        # (4) ВЫЧИТАНИЕ ОБРАЩЕНО
        битая = д.replace("20 − 11 = 9", "11 − 20 = 9")
        assert судить(битая) == (True, False), битая
        мутанты += 2
        б = страница(язык, "без_товара", 0, (13, 7))
        # (5) ОТВЕТ НЕ НАЗВАЛ ТОВАРА, КОТОРОГО НЕТ В ВОПРОСЕ — счётная форма чужого числа
        битая = б.replace("? " + вещей(язык, 0, 20), "? " + вещей(язык, 0, 13))
        assert судить(битая) == (True, False), битая
        мутанты += 1
        # (6) ПРО-ФОРМА НЕ ПО РОДУ ОПУЩЕННОГО ИМЕНИ (только там, где язык род метит)
        if НОВЫЕ[язык]["м"] != НОВЫЕ[язык]["ж"]:
            битая = п.replace(проформа(язык, 0, 5), "5 " + НОВЫЕ[язык]["м"])
            assert судить(битая) == (True, False), битая
            мутанты += 1
        # (7) ЗАЧИН ВОПРОСА ОБЪЯВЛЕН ДОМОМ ПАРЫ
        for стр in (п, д, б):
            голова = стр[:стр.index("?") + 1]
            вопрос = голова[голова.rindex(". ") + 2:] if ". " in голова else голова
            assert asking.зачин_объявлен(вопрос) is not False, (язык, вопрос)
    for язык in ЯЗЫКИ:
        print("  ", страница(язык, "прибавка", 0, (10, 5)))
    for язык in ("ru", "fr", "it", "pl"):
        print("  ", страница(язык, "два_шага", 1, (20, 11, 5)))
        print("  ", страница(язык, "без_товара", 0, (13, 7)))
    по_форме = {}
    for _, (_я, форма) in ПОКАЗЫ.items():
        по_форме[форма] = по_форме.get(форма, 0) + 1
    print(f"  мутантов поймано: {мутанты}")
    print(f"  дом пишет показов: {len(ПОКАЗЫ)} (языков {len(ЯЗЫКИ)}, образцов {len(ОБРАЗЦЫ)}): "
          + ", ".join(f"{ф} {к}" for ф, к in по_форме.items()))


if __name__ == "__main__":
    _самопроверка()
