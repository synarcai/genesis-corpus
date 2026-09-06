#!/usr/bin/env python3
"""THE HOUSE OF THE UNREAD NUMBER — the four places a number hides (05.09).

A MEASURE, NOT A GUESS. The atlas of silence ranks the reader's named exits, and the largest
gate of the grove is «numbers-unread»: 179 rows of 415 refusals. The atlas names WHERE the
number stood when it went unread, and this house shows exactly those four places, in nine
languages, each with a question that cannot be answered without reading it:

    A LIST WITHOUT COMMAS. «i have 3 apples 4 books 5 pencils» — the numbers and their things
    stand shoulder to shoulder with no punctuation between the pairs. A reader that segments
    by commas takes «4» for the apples; the question asks about the apples, and the court's
    presented «no» is that very answer.

    A NUMBER AFTER THE COPULA. «i have apples. there are 5.» — the thing stands in one
    sentence and its count in the next, with no noun beside the number at all.

    A NUMBER FIRST. «7 apples are on the table.» — the sentence opens with a digit, where
    most of the corpus opens with a name or a place.

    A NUMBER UNDER A CURRENCY SIGN. «one apple costs $5» — the sign is glued to the number
    («$5») or trails it («5 €», «5 zł», «5 ₽»), and the number under it is still a number:
    the page multiplies it by a count and shows the ledger.

AND THE PRO-FORM OF THE GOODS, asked for by the neighbouring measure: «i have 3 red apples
and 5 new ones» — the second number counts a thing named by a pro-form, not by its noun, and
the answer adds the two. Nine languages, each with its own agreement («5 nowych», «5 nuevas»,
«5 новых»).

WHAT IS BORROWED: the goods (apple, book, pencil), the currency word and the counting rule of
the pack come from the house of the price — one declaration, several readers. Declared here:
the bare plural (a counted genitive is not a plural: «яблок» is not «яблоки»), the currency
SIGN and the side it stands on, the class word of a total, the gendered question word of each
goods for the three languages that bend it, and the colour and pro-form words of the apple.

WHAT IS NOT MEASURED, NAMED: a number written in letters (the house of the number line owns
it), a number with a decimal point, and a list of four or more goods.
"""
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import asking  # noqa: E402 — the house of the pair declares which openers a question may wear
import priceforms as P  # noqa: E402 — the goods, the currency word and the pack's counting rule

ЯЗЫКИ = ("ru", "en", "de", "fr", "es", "it", "pt", "nl", "pl")
ТОВАРОВ = 3
# ГОЛЫЙ МНОЖЕСТВЕННЫЙ — не счётная форма: «яблок» есть родительный при числе, а «яблоки» есть
# множественное. Дом пары этого различия не держит, и здесь оно объявлено.
ПЛЮРАЛЬ = {
    "ru": ("яблоки", "книги", "карандаши"), "en": ("apples", "books", "pencils"),
    "de": ("Äpfel", "Bücher", "Bleistifte"), "fr": ("des pommes", "des livres", "des crayons"),
    "es": ("manzanas", "libros", "lápices"), "it": ("delle mele", "dei libri", "delle matite"),
    "pt": ("maçãs", "livros", "lápis"), "nl": ("appels", "boeken", "potloden"),
    "pl": ("jabłka", "książki", "ołówki"),
}
# ЗНАК ВАЛЮТЫ И ЕГО СТОРОНА — «$5» слева, «5 €» справа: сторона есть свойство языка.
ЗНАК = {"ru": ("₽", "после"), "en": ("$", "до"), "de": ("€", "после"), "fr": ("€", "после"),
        "es": ("€", "после"), "it": ("€", "после"), "pt": ("€", "после"), "nl": ("€", "после"),
        "pl": ("zł", "после")}
# РОД ТОВАРА ТАМ, ГДЕ ВОПРОСНОЕ СЛОВО ЕГО ДЕРЖИТ
РОД = {"es": ("f", "m", "m"), "it": ("f", "m", "f"), "pt": ("f", "m", "m")}
КСК = {"es": {"m": "¿cuántos", "f": "¿cuántas"}, "it": {"m": "quanti", "f": "quante"},
       "pt": {"m": "quantos", "f": "quantas"}}
# ЦВЕТ И ПРО-ФОРМА — только у яблока: прилагательное согласуется с родом вещи, и дом не
# угадывает согласования, он его пишет.
ЦВЕТ = {"ru": "красных", "en": "red", "de": "rote", "fr": "rouges", "es": "rojas",
        "it": "rosse", "pt": "vermelhas", "nl": "rode",
        "pl": dict(one="czerwone", few="czerwone", many="czerwonych")}
НОВЫЕ = {"ru": "новых", "en": "new ones", "de": "neue", "fr": "nouvelles", "es": "nuevas",
         "it": "nuove", "pt": "novas", "nl": "nieuwe",
         "pl": dict(one="nowe", few="nowe", many="nowych")}

РЕЧЬ = {
    "ru": dict(имею="у меня {a} {Тa} {b} {Тb} {c} {Тc}.", вопрос_моё="сколько у меня {МН}?",
               вопрос_всего="сколько вещей у меня?", есть="у меня есть {ПЛ}.", их="их {n}.",
               стол="{n} {Тn} на столе.", вопрос_стол="сколько {МН} на столе?",
               стоит="{В1} стоит {Ц}.", вопрос_цена="сколько стоит {В1}?",
               вопрос_цены="сколько стоят {k} {Тk}?",
               про="у меня {a} {ЦВ} {Тa} и {b} {НВ}.", двоеточие=": ", вопрос="?"),
    "en": dict(имею="i have {a} {Тa} {b} {Тb} {c} {Тc}.", вопрос_моё="how many {МН} do i have?",
               вопрос_всего="how many things do i have?", есть="i have {ПЛ}.", их="there are {n}.",
               стол="{n} {Тn} are on the table.", вопрос_стол="how many {МН} are on the table?",
               стоит="{В1} costs {Ц}.", вопрос_цена="how much does {В1} cost?",
               вопрос_цены="how much do {k} {Тk} cost?",
               про="i have {a} {ЦВ} {Тa} and {b} {НВ}.", двоеточие=": ", вопрос="?"),
    "de": dict(имею="ich habe {a} {Тa} {b} {Тb} {c} {Тc}.", вопрос_моё="wie viele {МН} habe ich?",
               вопрос_всего="wie viele Dinge habe ich?", есть="ich habe {ПЛ}.", их="es sind {n}.",
               стол="{n} {Тn} liegen auf dem Tisch.", вопрос_стол="wie viele {МН} liegen auf dem Tisch?",
               стоит="{В1} kostet {Ц}.", вопрос_цена="wie viel kostet {В1}?",
               вопрос_цены="wie viel kosten {k} {Тk}?",
               про="ich habe {a} {ЦВ} {Тa} und {b} {НВ}.", двоеточие=": ", вопрос="?"),
    "fr": dict(имею="j'ai {a} {Тa} {b} {Тb} {c} {Тc}.", вопрос_моё="combien de {МН} ai-je ?",
               вопрос_всего="combien de choses ai-je ?", есть="j'ai {ПЛ}.", их="il y en a {n}.",
               стол="{n} {Тn} sont sur la table.", вопрос_стол="combien de {МН} sont sur la table ?",
               стоит="{В1} coûte {Ц}.", вопрос_цена="combien coûte {В1} ?",
               вопрос_цены="combien coûtent {k} {Тk} ?",
               про="j'ai {a} {Тa} {ЦВ} et {b} {НВ}.", двоеточие=" : ", вопрос=" ?"),
    "es": dict(имею="tengo {a} {Тa} {b} {Тb} {c} {Тc}.", вопрос_моё="{КСК} {МН} tengo?",
               вопрос_всего="¿cuántas cosas tengo?", есть="tengo {ПЛ}.", их="hay {n}.",
               стол="{n} {Тn} están en la mesa.", вопрос_стол="{КСК} {МН} están en la mesa?",
               стоит="{В1} cuesta {Ц}.", вопрос_цена="¿cuánto cuesta {В1}?",
               вопрос_цены="¿cuánto cuestan {k} {Тk}?",
               про="tengo {a} {Тa} {ЦВ} y {b} {НВ}.", двоеточие=": ", вопрос="?"),
    "it": dict(имею="ho {a} {Тa} {b} {Тb} {c} {Тc}.", вопрос_моё="{КСК} {МН} ho?",
               вопрос_всего="quante cose ho?", есть="ho {ПЛ}.", их="ce ne sono {n}.",
               стол="{n} {Тn} sono sul tavolo.", вопрос_стол="{КСК} {МН} sono sul tavolo?",
               стоит="{В1} costa {Ц}.", вопрос_цена="quanto costa {В1}?",
               вопрос_цены="quanto costano {k} {Тk}?",
               про="ho {a} {Тa} {ЦВ} e {b} {НВ}.", двоеточие=": ", вопрос="?"),
    "pt": dict(имею="tenho {a} {Тa} {b} {Тb} {c} {Тc}.", вопрос_моё="{КСК} {МН} tenho?",
               вопрос_всего="quantas coisas tenho?", есть="tenho {ПЛ}.", их="há {n}.",
               стол="{n} {Тn} estão na mesa.", вопрос_стол="{КСК} {МН} estão na mesa?",
               стоит="{В1} custa {Ц}.", вопрос_цена="quanto custa {В1}?",
               вопрос_цены="quanto custam {k} {Тk}?",
               про="tenho {a} {Тa} {ЦВ} e {b} {НВ}.", двоеточие=": ", вопрос="?"),
    "nl": dict(имею="ik heb {a} {Тa} {b} {Тb} {c} {Тc}.", вопрос_моё="hoeveel {МН} heb ik?",
               вопрос_всего="hoeveel dingen heb ik?", есть="ik heb {ПЛ}.", их="het zijn er {n}.",
               стол="{n} {Тn} liggen op de tafel.", вопрос_стол="hoeveel {МН} liggen op de tafel?",
               стоит="{В1} kost {Ц}.", вопрос_цена="hoeveel kost {В1}?",
               вопрос_цены="hoeveel kosten {k} {Тk}?",
               про="ik heb {a} {ЦВ} {Тa} en {b} {НВ}.", двоеточие=": ", вопрос="?"),
    "pl": dict(имею="mam {a} {Тa} {b} {Тb} {c} {Тc}.", вопрос_моё="ile mam {МН}?",
               вопрос_всего="ile mam rzeczy?", есть="mam {ПЛ}.", их="jest ich {n}.",
               стол="{n} {Тn} leży na stole.", вопрос_стол="ile {МН} leży na stole?",
               стоит="{В1} kosztuje {Ц}.", вопрос_цена="ile kosztuje {В1}?",
               вопрос_цены="ile kosztują {k} {Тk}?",
               про="mam {a} {ЦВ} {Тa} i {b} {НВ}.", двоеточие=": ", вопрос="?"),
}
ФОРМЫ = ("список", "список_всего", "связка", "число_первым", "цена_знаком", "цена_счётом", "про_форма")
ТРОЙКИ = ((3, 4, 5), (5, 2, 7), (6, 9, 3), (8, 4, 6), (2, 7, 9), (4, 8, 2), (9, 3, 5), (7, 6, 4),
          (12, 5, 8), (10, 3, 6), (11, 7, 2), (13, 4, 9), (14, 6, 3), (15, 2, 8), (16, 9, 4),
          (34, 5, 6), (18, 3, 7), (36, 8, 2), (20, 4, 5), (21, 6, 9), (22, 7, 3), (38, 5, 4),
          (24, 2, 6), (25, 9, 8))
ОДИНОЧКИ = (5, 6, 7, 8, 9, 10, 11, 12, 14, 15, 18, 20, 13, 16, 33, 35, 21, 22, 37, 24,
            26, 28, 30, 32)
ЦЕНЫ = (2, 3, 5, 7)
СЧЁТ = (2, 3, 4)
ПАРЫ = ((3, 5), (4, 2), (6, 3), (5, 7), (2, 8), (7, 4), (9, 2), (8, 6), (10, 5), (12, 3), (11, 4), (6, 9),
        (13, 6), (14, 3), (15, 8), (16, 5), (33, 2), (18, 7), (35, 4), (20, 9), (21, 6), (22, 3), (37, 8), (24, 5))


def _вещь(язык, i, k):
    """The count form of goods i for k — the price house's table and the pack's own rule."""
    return P.форма(язык, P.ЯЗЫКИ[язык]["вещи"][i], k)


def _слово(язык, таблица, k):
    """A word that may bend by count (Polish adjectives) or may not (everything else)."""
    з = таблица[язык]
    return P.форма(язык, з, k) if isinstance(з, dict) else з


def _ксk(язык, i):
    """The question word of the goods, where the language bends it by gender."""
    return КСК[язык][РОД[язык][i]] if язык in КСК else ""


def _цена(язык, n):
    знак, сторона = ЗНАК[язык]
    return f"{знак}{n}" if сторона == "до" else f"{n} {знак}"


def рамка(язык, форма, i, дыра_цены="Ц"):
    """The page's template: the number stands where the atlas says it goes unread."""
    р = РЕЧЬ[язык]
    # ВОПРОС ВСЕГДА БЕРЁТ СЧЁТНУЮ ФОРМУ, А ГОЛЫЙ МНОЖЕСТВЕННЫЙ СТОИТ ЛИШЬ В ИСТОРИИ:
    # «у меня есть яблоки. их 7. сколько у меня яблок?» — две разные формы одной вещи.
    мн = P.ЯЗЫКИ[язык]["вещи"][i].get("many")
    вопрос_моё = р["вопрос_моё"].replace("{КСК}", _ксk(язык, i)).replace("{МН}", мн)
    if форма == "список":
        return р["имею"] + " " + вопрос_моё + " {a}."
    if форма == "список_всего":
        return (р["имею"] + " " + р["вопрос_всего"] + " {s}" + р["двоеточие"]
                + "{a} + {b} + {c} = {s}.")
    if форма == "связка":
        return р["есть"].replace("{ПЛ}", ПЛЮРАЛЬ[язык][i]) + " " + р["их"] + " " + вопрос_моё + " {n}."
    if форма == "число_первым":
        вопрос = р["вопрос_стол"].replace("{КСК}", _ксk(язык, i)).replace("{МН}", мн)
        return р["стол"] + " " + вопрос + " {n}."
    if форма in ("цена_знаком", "цена_счётом"):
        В1 = P.ЯЗЫКИ[язык]["вещи"][i]["one"]
        начало = р["стоит"].replace("{В1}", В1).replace("{Ц}", "{Ц}")
        if форма == "цена_знаком":
            return начало + " " + р["вопрос_цена"].replace("{В1}", В1) + " {Ц}."
        вопрос = р["вопрос_цены"]
        return начало + " " + вопрос + " {ЦV}" + р["двоеточие"] + "{k} × {n} = {v}."
    # про_форма — второе число считает вещь, названную про-формой, а не именем
    return р["про"] + " " + вопрос_моё + " {s}" + р["двоеточие"] + "{a} + {b} = {s}."


def страница(язык, форма, i, числа):
    р = РЕЧЬ[язык]
    п = {}
    if форма in ("список", "список_всего"):
        a, b, c = числа
        п = dict(a=a, b=b, c=c, s=a + b + c, Тa=_вещь(язык, i, a),
                 Тb=_вещь(язык, (i + 1) % ТОВАРОВ, b), Тc=_вещь(язык, (i + 2) % ТОВАРОВ, c))
    elif форма in ("связка", "число_первым"):
        n = числа[0]
        п = dict(n=n, Тn=_вещь(язык, i, n))
    elif форма == "цена_знаком":
        n = числа[0]
        п = dict(Ц=_цена(язык, n))
    elif форма == "цена_счётом":
        n, k = числа
        п = dict(n=n, k=k, v=n * k, Ц=_цена(язык, n), ЦV=_цена(язык, n * k), Тk=_вещь(язык, i, k))
    else:
        a, b = числа
        п = dict(a=a, b=b, s=a + b, Тa=_вещь(язык, i, a),
                 ЦВ=_слово(язык, ЦВЕТ, a), НВ=_слово(язык, НОВЫЕ, b))
    т = рамка(язык, форма, i)
    # ВТОРАЯ И ТРЕТЬЯ ВЕЩИ СПИСКА СТОЯТ ЗА ПЕРВОЙ ПО КРУГУ — список несёт три РАЗНЫЕ вещи
    return т.format(**п)


def _показы():
    вон = {}
    for язык in ЯЗЫКИ:
        for i in range(ТОВАРОВ):
            for тройка in ТРОЙКИ:
                вон[страница(язык, "список", i, тройка)] = (язык, "список")
                вон[страница(язык, "список_всего", i, тройка)] = (язык, "список_всего")
            for n in ОДИНОЧКИ:
                вон[страница(язык, "связка", i, (n,))] = (язык, "связка")
                вон[страница(язык, "число_первым", i, (n,))] = (язык, "число_первым")
            for n in ЦЕНЫ:
                вон[страница(язык, "цена_знаком", i, (n,))] = (язык, "цена_знаком")
                for k in СЧЁТ:
                    вон[страница(язык, "цена_счётом", i, (n, k))] = (язык, "цена_счётом")
        for a, b in ПАРЫ:                       # про-форма — только у яблока (род прилагательного)
            вон[страница(язык, "про_форма", 0, (a, b))] = (язык, "про_форма")
    return вон


ПОКАЗЫ = _показы()


def _альт(слова):
    return "(?:" + "|".join(re.escape(с) for с in sorted({с for с in слова if с}, key=lambda с: (-len(с), с))) + ")"


def _образец(язык, шаблон, i):
    вещи = lambda j: _альт(P.ЯЗЫКИ[язык]["вещи"][j % ТОВАРОВ].values())
    знак, сторона = ЗНАК[язык]
    цена = (re.escape(знак) + r"\d+") if сторона == "до" else (r"\d+ " + re.escape(знак))
    дыры = {"a": r"\d+", "b": r"\d+", "c": r"\d+", "n": r"\d+", "s": r"\d+", "k": r"\d+",
            "v": r"\d+", "Тa": вещи(i), "Тb": вещи(i + 1), "Тc": вещи(i + 2), "Тn": вещи(i),
            "Тk": вещи(i), "Ц": цена, "ЦV": цена,
            "ЦВ": _альт(ЦВЕТ[язык].values() if isinstance(ЦВЕТ[язык], dict) else [ЦВЕТ[язык]]),
            "НВ": _альт(НОВЫЕ[язык].values() if isinstance(НОВЫЕ[язык], dict) else [НОВЫЕ[язык]])}
    счёт, куски = {}, []
    for кусок in re.split(r"(\{[^}]+\})", шаблон):
        if кусок.startswith("{"):
            дыра = кусок[1:-1]
            счёт[дыра] = счёт.get(дыра, 0) + 1
            куски.append(f"(?P<h_{дыра}__{счёт[дыра]}>{дыры[дыра]})")
        else:
            куски.append(re.escape(кусок))
    return re.compile("^" + "".join(куски) + "$")


ОБРАЗЦЫ = [(_образец(язык, рамка(язык, форма, i), i), язык, форма, i)
           for язык in ЯЗЫКИ for форма in ФОРМЫ
           for i in (range(ТОВАРОВ) if форма != "про_форма" else (0,))]


def _значения(м):
    вон = {}
    for ключ, знач in м.groupdict().items():
        дыра, _ = ключ[2:].rsplit("__", 1)
        if дыра in вон and вон[дыра] != знач:
            return None
        вон[дыра] = знач
    return вон


def _число(текст):
    м = re.search(r"\d+", текст)
    return int(м.group()) if м else None


def _вердикт(язык, форма, i, зн):
    if форма in ("список", "список_всего"):
        a, b, c = int(зн["a"]), int(зн["b"]), int(зн["c"])
        if min(a, b, c) < 1:
            return False
        # СЧЁТНАЯ ФОРМА КАЖДОЙ ВЕЩИ — ФОРМА ЕЁ ЧИСЛА (иначе список читается вразнобой)
        for дыра, ч, j in (("Тa", a, i), ("Тb", b, i + 1), ("Тc", c, i + 2)):
            if зн[дыра] != _вещь(язык, j % ТОВАРОВ, ч):
                return False
        if форма == "список_всего":
            return int(зн["s"]) == a + b + c
        return True                     # ответ есть {a} по построению рамки: дыра одна
    if форма in ("связка", "число_первым"):
        n = int(зн["n"])
        if n < 1:
            return False
        if форма == "число_первым" and зн["Тn"] != _вещь(язык, i, n):
            return False
        return True
    if форма == "цена_знаком":
        return _число(зн["Ц"]) is not None and _число(зн["Ц"]) >= 1
    if форма == "цена_счётом":
        n, k, v = int(зн["n"]), int(зн["k"]), int(зн["v"])
        if n < 1 or k < 1 or n * k != v:
            return False
        if _число(зн["Ц"]) != n or _число(зн["ЦV"]) != v:
            return False
        return зн["Тk"] == _вещь(язык, i, k)
    a, b, s = int(зн["a"]), int(зн["b"]), int(зн["s"])
    if a < 1 or b < 1 or a + b != s:
        return False
    if зн["Тa"] != _вещь(язык, 0, a):
        return False
    return зн["ЦВ"] == _слово(язык, ЦВЕТ, a) and зн["НВ"] == _слово(язык, НОВЫЕ, b)


def _судить_образцом(строка):
    """(судимо, истинно): a page of a frame of the house whose number reads back; else silence."""
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


def _хвост(с):
    м = list(re.finditer(r"[?？] ", с))
    return м[-1].end() if м else 0


def _самопроверка():
    for показ in ПОКАЗЫ:
        assert судить(показ) == (True, True), показ
    мутанты = 0
    for язык in ЯЗЫКИ:
        for i in range(ТОВАРОВ):
            a, b, c = 3, 4, 5
            # (1) В СПИСКЕ БЕЗ ЗАПЯТЫХ ВЗЯТО ЧИСЛО СОСЕДА — сам замеренный дефект
            сп = страница(язык, "список", i, (a, b, c))
            assert судить(сп) == (True, True), сп
            хв = _хвост(сп)
            битая = сп[:хв] + сп[хв:].replace(str(a), str(b), 1)
            assert судить(битая) == (True, False), битая
            # (2) ИТОГ СПИСКА НЕ СХОДИТСЯ
            в = страница(язык, "список_всего", i, (a, b, c))
            assert судить(в) == (True, True), в
            битая = в[:_хвост(в)] + в[_хвост(в):].replace("12", "13")
            assert судить(битая) == (True, False), битая
            # (3) СЧЁТНАЯ ФОРМА ВТОРОЙ ВЕЩИ — ФОРМА ЧУЖОГО ЧИСЛА
            своя, чужая = _вещь(язык, (i + 1) % ТОВАРОВ, b), _вещь(язык, (i + 1) % ТОВАРОВ, 1)
            if своя != чужая:
                битая = сп.replace(" " + своя, " " + чужая, 1)
                assert судить(битая) == (True, False), битая
                мутанты += 1
            мутанты += 2
            # (4) ЧИСЛО ПЕРВЫМ: ОТВЕТ НЕ РАВЕН ВЕДУЩЕМУ ЧИСЛУ
            п = страница(язык, "число_первым", i, (7,))
            assert судить(п) == (True, True), п
            битая = п[:_хвост(п)] + п[_хвост(п):].replace("7", "8")
            assert судить(битая) == (True, False), битая
            # (5) ЧИСЛО ПОСЛЕ СВЯЗКИ: ОТВЕТ НЕ РАВЕН ЕМУ
            с = страница(язык, "связка", i, (7,))
            assert судить(с) == (True, True), с
            битая = с[:_хвост(с)] + с[_хвост(с):].replace("7", "9")
            assert судить(битая) == (True, False), битая
            # (6) ЦЕНА СЧЁТОМ: ЛЕДЖЕР НЕ СХОДИТСЯ
            ц = страница(язык, "цена_счётом", i, (5, 3))
            assert судить(ц) == (True, True), ц
            битая = ц[:ц.rindex("= ")] + "= 16."
            assert судить(битая) == (True, False), битая
            мутанты += 3
        # (7) ПРО-ФОРМА: СУММА НЕ СХОДИТСЯ
        пр = страница(язык, "про_форма", 0, (3, 5))
        assert судить(пр) == (True, True), пр
        битая = пр[:_хвост(пр)] + пр[_хвост(пр):].replace("8", "9")
        assert судить(битая) == (True, False), битая
        мутанты += 1
        # (8) ЗАЧИН ВОПРОСА ОБЪЯВЛЕН ДОМОМ ПАРЫ
        for стр in (сп, в, п, с, ц, пр):
            вопрос = стр[:стр.index("?") + 1].split(". ")[-1]
            assert asking.зачин_объявлен(вопрос) is not False, (язык, вопрос)
    for язык in ЯЗЫКИ:
        print("  ", страница(язык, "список", 0, (3, 4, 5)))
    for язык in ("ru", "en", "pl", "fr"):
        print("  ", страница(язык, "связка", 0, (7,)))
        print("  ", страница(язык, "число_первым", 1, (9,)))
        print("  ", страница(язык, "цена_счётом", 0, (5, 3)))
        print("  ", страница(язык, "про_форма", 0, (3, 5)))
    по_форме = {}
    for _, (язык, форма) in ПОКАЗЫ.items():
        по_форме[форма] = по_форме.get(форма, 0) + 1
    print(f"  мутантов поймано: {мутанты}")
    print(f"  дом пишет показов: {len(ПОКАЗЫ)} (языков {len(ЯЗЫКИ)}, форм {len(ФОРМЫ)}, образцов {len(ОБРАЗЦЫ)}): "
          + ", ".join(f"{ф} {к}" for ф, к in по_форме.items()))




import closedworld as _зк  # noqa: E402 — закон замкнутого мира читается после сборки показов
_СКЕЛЕТЫ_ЗНАКА = _зк.скелеты_знака(ПОКАЗЫ)


def судить(строка):
    """(судимо, истинно) — с ЗАКОНОМ ЗНАКА поверх образца.

    ЗНАК ДЕЙСТВИЯ СУДИТСЯ ЗАКОНОМ ЗАМКНУТОГО МИРА, А НЕ ДЫРОЙ В КАЖДОЙ РАМКЕ: строка,
    становящаяся ИСТИННОЙ при замене одного знака, есть строка ЭТОГО дома с испорченным
    знаком (М-489). Прежде такая строка получала НЕМОТУ, и палата брала истину у суда
    арифметики — у соседа (М-131).
    """
    вердикт = _судить_образцом(строка)
    if вердикт[0] is False and _зк.ложь_по_знаку(
            строка, _СКЕЛЕТЫ_ЗНАКА, ПОКАЗЫ, _судить_образцом):
        return True, False
    return вердикт
if __name__ == "__main__":
    _самопроверка()
