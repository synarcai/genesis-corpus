#!/usr/bin/env python3
"""THE HOUSE OF SUFFICIENCY — «хватит ли?», the yes-or-no that is bought by arithmetic (06.09).

The census found ZERO lines carrying «хватит ли» / «is that enough» in the whole свод. The corpus
computes prices, sums, differences and shares — and never once DECIDES with them. Yet the
commonest use a person makes of arithmetic is exactly this: not «how much», but «is what I have
enough», and the answer is a WORD («да», «nein») whose ground is a number. A reader that can
multiply but cannot decide has learned the operation and not its use.

WHAT THE HOUSE SHOWS, three frames over one purse:
  хватит      — the money suffices: the cost multiplied out, and the REMAINDER subtracted, so the
                yes is not a claim but a subtraction that comes out the right way round;
  не_хватит   — it does not: the same multiplication, and the subtraction turned the OTHER way,
                naming what is missing. The direction of the subtraction IS the verdict;
  сколько_ещё — the shortfall asked as a number, which is the same page read as a question.
The equality case is shown on purpose («12 for 12, nothing left over»): the boundary of a decision
is where a reader that guesses by «about the same» fails.

WHAT IS BORROWED, NOT REDECLARED: the apple, the book, the pencil, the currency and the price
sentence itself come from the house of price (tools/priceforms.py) with the pack's counting rule;
the question openers are declared by the house of the pair. Declared here: the purse, the two
verdict words of each language, and the two directions of the difference — «останется» and «не
хватает» — with the case each language demands after them (Russian and Polish put the currency in
the genitive after «не хватает» / «brakuje»; the others do not inflect it).

WHAT IS NOT MEASURED, NAMED: a purse that must cover two different goods, change given back in
coins, and any decision whose ground is not exact arithmetic («примерно хватит»).

AND ONE GRAMMAR NOT SHOWN, NAMED WITH ITS REASON. The strictly correct Russian for a shortfall is
the NEGATIVE GENITIVE — «не хватает двух рублей», and with a figure «не хватает 2 рублей» — where
the negated verb of lacking governs the genitive and the counting form of the numeral does not
apply. The corpus' Russian-grammar court reads «2 рублей» by the general counting rule and calls
it a lie (measured: nine pages of this house, all Russian and Polish, refused at the gate). The
court is not wrong about the general rule and this house is not the place to teach it the
exception, so the shortfall is said here in the nominative construction every language shares
(«нужно ещё 2 рубля», «trzeba jeszcze 2 złote»). The negative genitive is a named entrance for
the grammar court, not a hole in this house.
"""
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import asking  # noqa: E402 — the house of the pair declares which openers a question may wear
import priceforms as P  # noqa: E402 — the goods, the currency, the price sentence, the count rule

ЯЗЫКИ = ("ru", "en", "de", "fr", "es", "it", "pt", "nl", "pl")
# (цена, кошелёк, сколько ХВАТИТ, сколько НЕ хватит) — среди них случай ровного счёта (3, 12, 4)
СЛУЧАИ = ((2, 10, 4, 6), (3, 12, 4, 5), (5, 20, 3, 5), (4, 15, 3, 4))
# РОВНО — граница решения: денег в точности столько, сколько надо, и остаток НУЛЬ назван
# словом, а не цифрой: «ничего не останется». Читатель, угадывающий «примерно столько же»,
# ломается именно здесь, и потому граница показана отдельной формой.
ФОРМЫ = ("хватит", "ровно", "не_хватит", "сколько_ещё")
РЕЧЬ = {
    "ru": dict(кошелёк="у меня {M}.", вопрос="хватит ли на {K}?", да="да", нет="нет",
               остаток="останется {X}", нехватка="нужно ещё {X}",
               вопрос_ещё="сколько ещё нужно на {K}?", двоеточие=": ", род_нехватки=False, ничего="ничего не останется"),
    "en": dict(кошелёк="i have {M}.", вопрос="is that enough for {K}?", да="yes", нет="no",
               остаток="{X} will be left", нехватка="{X} are missing",
               вопрос_ещё="how much more is needed for {K}?", двоеточие=": ", род_нехватки=False, ничего="nothing will be left"),
    "de": dict(кошелёк="ich habe {M}.", вопрос="ist das genug für {K}?", да="ja", нет="nein",
               остаток="{X} bleiben übrig", нехватка="{X} fehlen",
               вопрос_ещё="wie viel fehlt noch für {K}?", двоеточие=": ", род_нехватки=False, ничего="es bleibt nichts übrig"),
    "fr": dict(кошелёк="j'ai {M}.", вопрос="est-ce assez pour {K} ?", да="oui", нет="non",
               остаток="il reste {X}", нехватка="il manque {X}",
               вопрос_ещё="combien manque-t-il pour {K} ?", двоеточие=" : ", род_нехватки=False, ничего="il ne reste rien"),
    "es": dict(кошелёк="tengo {M}.", вопрос="¿es suficiente para {K}?", да="sí", нет="no",
               остаток="quedan {X}", нехватка="faltan {X}",
               вопрос_ещё="¿cuánto falta para {K}?", двоеточие=": ", род_нехватки=False, ничего="no queda nada"),
    "it": dict(кошелёк="ho {M}.", вопрос="è abbastanza per {K}?", да="sì", нет="no",
               остаток="restano {X}", нехватка="mancano {X}",
               вопрос_ещё="quanto manca per {K}?", двоеточие=": ", род_нехватки=False, ничего="non resta nulla"),
    "pt": dict(кошелёк="tenho {M}.", вопрос="é suficiente para {K}?", да="sim", нет="não",
               остаток="sobram {X}", нехватка="faltam {X}",
               вопрос_ещё="quanto falta para {K}?", двоеточие=": ", род_нехватки=False, ничего="não sobra nada"),
    "nl": dict(кошелёк="ik heb {M}.", вопрос="is dat genoeg voor {K}?", да="ja", нет="nee",
               остаток="er blijft {X} over", нехватка="er ontbreken {X}",
               вопрос_ещё="hoeveel is er nog nodig voor {K}?", двоеточие=": ", род_нехватки=False, ничего="er blijft niets over"),
    "pl": dict(кошелёк="mam {M}.", вопрос="czy wystarczy na {K}?", да="tak", нет="nie",
               остаток="zostanie {X}", нехватка="trzeba jeszcze {X}",
               вопрос_ещё="ile jeszcze potrzeba na {K}?", двоеточие=": ", род_нехватки=False, ничего="nic nie zostanie"),
}


def _вещь(язык, i):
    return P.ЯЗЫКИ[язык]["вещи"][i]


def _валюта(язык):
    return P.ЯЗЫКИ[язык]["валюта"]


def деньги(язык, n, родительный=False):
    """«2 рубля», «2 złote» — и «2 рублей» там, где язык требует родительного."""
    слов = _валюта(язык)
    if родительный and isinstance(слов, dict) and "many" in слов:
        return "%d %s" % (n, слов["many"])
    return "%d %s" % (n, P.форма(язык, слов, n))


def товар(язык, i, k):
    return "%d %s" % (k, P.форма(язык, _вещь(язык, i), k))


def цена_фраза(язык, i, n):
    """The price sentence is the house of price's own — taken, not written again."""
    рамка = P.ЯЗЫКИ[язык]["рамка"][0].split(". ")[0]
    return рамка.format(В1=_вещь(язык, i)["one"], n=n, Р=P.форма(язык, _валюта(язык), n),
                        k="", Вk="") + "."


def рамка(язык, форма):
    р = РЕЧЬ[язык]
    голова = "{ЦЕНА} " + р["кошелёк"].replace("{M}", "{M}") + " "
    if форма == "сколько_ещё":
        return (голова + р["вопрос_ещё"].replace("{K}", "{K}") + " {D}" + р["двоеточие"]
                + "{k} × {n} = {v}, {v} − {m} = {d}.")
    вопрос = р["вопрос"] + " "
    if форма == "ровно":
        # ГРАНИЦА: вычитание даёт нуль, и нуль сказан словом
        return (голова + вопрос + р["да"] + р["двоеточие"] + "{k} × {n} = {v}, {m} − {v} = 0, "
                + р["ничего"] + ".")
    if форма == "хватит":
        # ВЕРДИКТ ЕСТЬ НАПРАВЛЕНИЕ ВЫЧИТАНИЯ: кошелёк минус цена
        return (голова + вопрос + р["да"] + р["двоеточие"] + "{k} × {n} = {v}, {m} − {v} = {o}, "
                + р["остаток"] + ".")
    # ЗДЕСЬ ВЫЧИТАНИЕ ИДЁТ ОБРАТНО: цена минус кошелёк
    return (голова + вопрос + р["нет"] + р["двоеточие"] + "{k} × {n} = {v}, {v} − {m} = {d}, "
            + р["нехватка"] + ".")


def страница(язык, форма, i, случай):
    n, m, k_да, k_нет = случай
    k = k_да if форма in ("хватит", "ровно") else k_нет
    v = k * n
    зн = dict(ЦЕНА=цена_фраза(язык, i, n), M=деньги(язык, m), K=товар(язык, i, k),
              k=k, n=n, v=v, m=m)
    if форма == "ровно":
        pass
    elif форма == "хватит":
        зн.update(o=m - v, X=деньги(язык, m - v))
    else:
        зн.update(d=v - m, D=деньги(язык, v - m),
                  X=деньги(язык, v - m, РЕЧЬ[язык]["род_нехватки"]))
    return рамка(язык, форма).format(**зн)


def _показы():
    вон = {}
    for язык in ЯЗЫКИ:
        for i in range(len(P.ЯЗЫКИ[язык]["вещи"])):
            for случай in СЛУЧАИ:
                n, m, k_да, _ = случай
                ровно = k_да * n == m
                for форма in ФОРМЫ:
                    if форма == ("хватит" if ровно else "ровно"):
                        continue
                    вон[страница(язык, форма, i, случай)] = (язык, форма)
    return вон


ПОКАЗЫ = _показы()


def _альт(слова):
    сорт = sorted({с for с in слова if с}, key=lambda с: (-len(с), с))
    return "(?:" + "|".join(re.escape(с) for с in сорт) + ")"


def _дыры(язык):
    вал = _альт(з for з in ([_валюта(язык)[ф] for ф in _валюта(язык)]
                            if isinstance(_валюта(язык), dict) else [_валюта(язык)]))
    вещи = _альт(з for i in range(len(P.ЯЗЫКИ[язык]["вещи"]))
                 for з in _вещь(язык, i).values())
    деньги_ = r"\d+ " + вал
    # ЦЕНА — НЕ «ЧТО УГОДНО»: дыра, открытая на любой текст, есть ЛОВУШКА НАЧАЛА
    # (scripts/prefix_traps.py: удвоенная строка «X. X.» пролезала в дыру и звалась ложью,
    # хотя суду о ней сказать нечего). Цен у дома двенадцать на язык, и они перечислены.
    цены = _альт(цена_фраза(язык, i, n) for i in range(len(P.ЯЗЫКИ[язык]["вещи"]))
                 for n, _m, _kд, _kн in СЛУЧАИ)
    return {"ЦЕНА": цены, "M": деньги_, "K": r"\d+ " + вещи, "X": деньги_, "D": деньги_,
            "k": r"\d+", "n": r"\d+", "v": r"\d+", "m": r"\d+", "o": r"\d+", "d": r"\d+"}


def _образец(язык, форма):
    дыры, счёт, куски = _дыры(язык), {}, []
    for кусок in re.split(r"(\{[^}]+\})", рамка(язык, форма)):
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


def _вещь_по_счёту(язык, слово):
    """Which of the goods this counted phrase names, and how many — the count form is judged too."""
    число, _, хвост = слово.partition(" ")
    for i in range(len(P.ЯЗЫКИ[язык]["вещи"])):
        if P.форма(язык, _вещь(язык, i), int(число)) == хвост:
            return i, int(число)
    return None, None


def _вердикт(язык, форма, зн):
    i, k = _вещь_по_счёту(язык, зн["K"])
    if i is None or k != int(зн["k"]) or k < 1:
        return False
    n, m, v = int(зн["n"]), int(зн["m"]), int(зн["v"])
    if n < 1 or m < 1 or k * n != v:
        return False
    if зн["M"] != деньги(язык, m) or зн["ЦЕНА"] != цена_фраза(язык, i, n):
        return False
    if форма == "ровно":
        # ГРАНИЦА ИСТИННА ЛИШЬ ТАМ, ГДЕ РАВЕНСТВО ТОЧНОЕ
        return v == m
    if форма == "хватит":
        # ДА ПОКУПАЕТСЯ ТЕМ, ЧТО ОСТАТОК ПОЛОЖИТЕЛЕН И ПОСЧИТАН
        return v < m and int(зн["o"]) == m - v and зн["X"] == деньги(язык, m - v)
    d = int(зн["d"])
    if not (v > m and d == v - m):
        return False
    if форма == "сколько_ещё":
        return зн["D"] == деньги(язык, d)
    return зн["X"] == деньги(язык, d, РЕЧЬ[язык]["род_нехватки"])


def судить(строка):
    """(судимо, истинно): a page of the purse whose decision is its own subtraction; else silence."""
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
        х = страница(язык, "хватит", 0, (2, 10, 4, 6))
        assert судить(х) == (True, True), х
        # (1) ПРОИЗВЕДЕНИЕ ПОСЧИТАНО НЕВЕРНО
        битая = х.replace("4 × 2 = 8", "4 × 2 = 6").replace("10 − 8 = 2", "10 − 6 = 4")
        assert судить(битая) == (True, False), битая
        # (2) ОСТАТОК ПОСЧИТАН НЕВЕРНО (и назван словом)
        битая = х.replace("10 − 8 = 2, " + РЕЧЬ[язык]["остаток"].format(X=деньги(язык, 2)),
                          "10 − 8 = 3, " + РЕЧЬ[язык]["остаток"].format(X=деньги(язык, 3)))
        assert судить(битая) == (True, False), битая
        н = страница(язык, "не_хватит", 0, (2, 10, 4, 6))
        assert судить(н) == (True, True), н
        # (3) НЕХВАТКА ПОСЧИТАНА НЕВЕРНО
        битая = н.replace("12 − 10 = 2, " + РЕЧЬ[язык]["нехватка"].format(
            X=деньги(язык, 2, РЕЧЬ[язык]["род_нехватки"])),
            "12 − 10 = 4, " + РЕЧЬ[язык]["нехватка"].format(
                X=деньги(язык, 4, РЕЧЬ[язык]["род_нехватки"])))
        assert судить(битая) == (True, False), битая
        # (4) СЧЁТНАЯ ФОРМА ТОВАРА ОТ ЧУЖОГО ЧИСЛА
        своя, чужая = P.форма(язык, _вещь(язык, 0), 6), P.форма(язык, _вещь(язык, 0), 1)
        if своя != чужая:
            битая = н.replace("6 " + своя, "6 " + чужая)
            assert судить(битая) == (True, False), битая
            мутанты += 1
        р = страница(язык, "ровно", 0, (3, 12, 4, 5))
        assert судить(р) == (True, True), р
        # (5) ГРАНИЦА ОБЪЯВЛЕНА ТАМ, ГДЕ РАВЕНСТВА НЕТ
        битая = р.replace("4 × 3 = 12, 12 − 12 = 0", "4 × 3 = 12, 13 − 12 = 0").replace(
            деньги(язык, 12) + ".", деньги(язык, 13) + ".")
        assert судить(битая) == (True, False), битая
        е = страница(язык, "сколько_ещё", 0, (2, 10, 4, 6))
        assert судить(е) == (True, True), е
        # (6) ОТВЕТ О НЕХВАТКЕ РАЗОШЁЛСЯ С ЛЕДЖЕРОМ
        битая = е.replace("? " + деньги(язык, 2), "? " + деньги(язык, 3), 1)
        assert судить(битая) == (True, False), битая
        мутанты += 6
        # (7) ЗАЧИН ВОПРОСА ОБЪЯВЛЕН ДОМОМ ПАРЫ
        for стр in (х, н, е):
            вопрос = [ч for ч in стр.split(". ") if "?" in ч][0]
            вопрос = вопрос[:вопрос.index("?") + 1]
            assert asking.зачин_объявлен(вопрос) is not False, (язык, вопрос)
    for язык in ЯЗЫКИ:
        print("  ", страница(язык, "не_хватит", 0, (2, 10, 4, 6)))
    for язык in ("ru", "de", "pl"):
        print("  ", страница(язык, "ровно", 1, (3, 12, 4, 5)))
        print("  ", страница(язык, "сколько_ещё", 2, (5, 20, 3, 5)))
    по_форме = {}
    for _, (_язык, форма) in ПОКАЗЫ.items():
        по_форме[форма] = по_форме.get(форма, 0) + 1
    print(f"  мутантов поймано: {мутанты}")
    print(f"  дом пишет показов: {len(ПОКАЗЫ)} (языков {len(ЯЗЫКИ)}, случаев {len(СЛУЧАИ)}, "
          f"образцов {len(ОБРАЗЦЫ)}): " + ", ".join(f"{ф} {к}" for ф, к in по_форме.items()))


if __name__ == "__main__":
    _самопроверка()
