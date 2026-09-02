#!/usr/bin/env python3
"""WHERE ONE WORD ENDS AND THE NEXT BEGINS — declared, not assumed.

Every parser in the park assumed the space. On «三加二等于五。» the
language census and the arithmetic court both saw ONE token — the whole
sentence — and so could judge nothing at all. The rest of the
architecture was already blind to script (a pack declares its writing
system, its range, its probe, its agreement rule), and this was the one
place where an alphabet was still presumed.

THE SEGMENTER READS WHAT THE LANGUAGE DECLARED ABOUT ITSELF. A pack
carries its numerals, its operator words and the forms of its classes;
those ARE its vocabulary, and the segmenter cuts by LONGEST MATCH over
exactly them, falling back to a single character. A word the pack never
declared is not invented here — it is left as characters, and whatever
judges the line will simply not judge what it cannot read. That is the
honest failure: silence, not a guess.

Scripts that write without spaces are named by the pack
(`"segmentation": "longest-match"`); everything else keeps the space,
because for a space-writing language the space IS the declaration.
"""

import re

BARE_WORD = r"[^\W\d_]+"
SPACED = re.compile(r"\d+|" + BARE_WORD + r"|[+\-*/×÷=−⋅]")
GLYPHS = set("+-*/×÷=−⋅")


БУКВА = r"[^\W\d_]"


def внутрисловные(словарь):
    r"""Знаки, стоящие ВНУТРИ объявленных слов, — ВЫВЕДЕНЫ, не объявлены.

    Украинское «п'ятнадцять» — одно слово, и апостроф в нём не граница,
    а буква по должности: суд пласта, резавший по [^\W\d_]+, видел «п»
    и «ятнадцять» и звал второе необъявленным. Тот же знак живёт во
    французском «l'homme», в английском «don't», в каталонском «l·l»,
    в хорватском и в турецком «Ali'nin» — и ни один из этих случаев не
    должен стоить нового поля в пакете.

    ЗНАК, ЖИВУЩИЙ МЕЖДУ ДВУМЯ БУКВАМИ ОБЪЯВЛЕННОГО СЛОВА, ТЕМ САМЫМ
    ОБЪЯВЛЕН. Пакет уже сказал всё, что нужно, назвав свои слова;
    прибору остаётся прочесть сказанное, а не спросить ещё раз. Это тот
    же род, что и разбиение письма без пробелов: письмо есть свойство
    языка, и язык о нём УЖЕ высказался — словарём.
    """
    import unicodedata
    знаки = set()
    for слово in словарь:
        после_буквы = False
        for i, ch in enumerate(слово):
            if ch.isalnum() or ch == "_":
                после_буквы = True
                continue
            if ch.isspace():
                после_буквы = False
                continue
            # КОМБИНИРУЮЩАЯ МЕТКА ЕСТЬ БУКВА ПО ДОЛЖНОСТИ ВЕЗДЕ, ГДЕ
            # СТОИТ: она не может начать слово и не может стоять одна,
            # и потому не требует буквы С ОБЕИХ сторон — довольно
            # буквы слева. Значок гласной в конце слова («किताबें»)
            # иначе остался бы за границей.
            if unicodedata.category(ch).startswith("M"):
                # МЕТКА СТОИТ И ЗА ДРУГОЙ МЕТКОЙ: «किताबें» несёт
                # значок гласной, а следом анусвару, и требование
                # БУКВЫ прямо слева теряло вторую. Метка законна везде,
                # где слева от неё уже была буква — сквозь другие метки.
                if после_буквы:
                    знаки.add(ch)
                continue
            if 0 < i < len(слово) - 1:
                до, после = слово[i - 1], слово[i + 1]
                if до.isalpha() and после.isalpha():
                    знаки.add(ch)
    return знаки


def _по_словам(text, словарь):
    """Слова письма пакета, цифры и глифы — без многословных.

    Отдельный ход нарочно: рекурсивный зов ПОЛНОГО разбора на остатке
    входил в ветвь многословных снова и снова и упирался в глубину
    рекурсии. Ход, вызывающий сам себя на том же входе, есть не
    рекурсия, а петля.
    """
    образец = word_re(словарь)
    вон = []
    for кусок in re.findall(r"\d+|[+\-*/×÷=−⋅]|\S+", text):
        if кусок.isdigit() or кусок in GLYPHS:
            вон.append(кусок)
            continue
        вон += образец.findall(кусок)
    return вон


_МНОГО = {}


def многословные(словарь):
    """Образец объявленных многословных, длинные впереди, или None.

    Границы слова стерегутся с обеих сторон, чтобы «bốn mươi» не
    откусило хвост у соседа. Письму без пробелов этот путь не нужен —
    у него свой, и он выбирается прежде.
    """
    ключ = frozenset(словарь)
    if ключ in _МНОГО:
        return _МНОГО[ключ]
    длинные = sorted((с for с in словарь if " " in с),
                     key=len, reverse=True)
    if not длинные:
        _МНОГО[ключ] = None
        return None
    куски = []
    for с in длинные:
        слева = f"(?<!{BARE_WORD[:-1]})" if с[:1].isalpha() else ""
        справа = f"(?!{BARE_WORD[:-1]})" if с[-1:].isalpha() else ""
        куски.append(слева + re.escape(с) + справа)
    _МНОГО[ключ] = re.compile("|".join(куски))
    return _МНОГО[ключ]


def word_re(словарь=()):
    """Образец СЛОВА этого письма: буквы со знаками, живущими внутри.

    Без словаря — старое правило (одни буквы), ибо без объявления
    внутрисловных знаков нет.
    """
    знаки = внутрисловные(словарь)
    if not знаки:
        return re.compile(BARE_WORD, re.UNICODE)
    класс = "[" + "".join(re.escape(з) for з in sorted(знаки)) + "]"
    # ЗНАК БЫВАЕТ И В КОНЦЕ СЛОВА. «किताबें» кончается значком гласной,
    # и образец, требовавший буквы ПОСЛЕ знака, обрубал слово до
    # «किताब» — не разорвал, но укоротил, и поле ONCE считало два
    # разных слова одним. Хвост объявлен так же, как середина.
    return re.compile(
        f"{BARE_WORD}(?:{класс}+{BARE_WORD})*{класс}*", re.UNICODE)


def spaced_tokens(text, словарь=()):
    r"""Runs of letters, runs of digits, and operator glyphs.

    БУКВА БЫВАЕТ КОМБИНИРУЮЩЕЙ МЕТКОЙ, И ЭТО НЕ ИСКЛЮЧЕНИЕ, А ЦЕЛЫЙ
    РОД ПИСЬМА. В абугиде гласная пишется ЗНАЧКОМ ПРИ согласной
    («किताबें»), и такой значок по Unicode есть метка (категория Mn),
    а не буква: образец `[^\W\d_]+` рвёт слово на обломки — «क», «त»,
    «ब», — и прибор считает три «слова» там, где написано одно.

    Замер, взятый на пакете хинди двумя прогонами, разнящимися одной
    строкой объявления: по словарю — 425 равенств и 166 слов; по
    пробелу — 85 равенств и 77 «слов». ОБА ЗЕЛЕНЫ. Но во втором
    триста сорок равенств, сказанных словами хинди, исчезали без следа,
    а семьдесят семь «слов» были обломками. Зелёное поле, измерившее
    не то.

    Лечение — тот же закон, каким лечился украинский апостроф внутри
    слова: ЗНАК, ЖИВУЩИЙ МЕЖДУ ДВУМЯ БУКВАМИ ОБЪЯВЛЕННОГО СЛОВА, ТЕМ
    САМЫМ ОБЪЯВЛЕН БУКВОЙ ПО ДОЛЖНОСТИ. Словарь пакета даёт эти знаки
    сам; языку без них ничего не меняется.
    """
    if словарь:
        # ОБЪЯВЛЕННОЕ МНОГОСЛОВНОЕ ЕСТЬ ОДИН ТОКЕН — И ЗДЕСЬ ТОЖЕ.
        # Закон жил в арифметическом суде и не жил в сегментаторе: форж
        # языковых пакетов, читая арабское «ستة عشر» (шестнадцать) и
        # вьетнамское «bốn mươi» (сорок), видел два слова и объявлял
        # ложью тридцать шесть честных равенств. Один закон в двух
        # домах, и второй о нём не знал.
        составные = многословные(словарь)
        if составные is not None:
            вон, хвост = [], 0
            for м in составные.finditer(text):
                вон += _по_словам(text[хвост:м.start()], словарь)
                вон.append(м.group())
                хвост = м.end()
            return вон + _по_словам(text[хвост:], словарь)
        return _по_словам(text, словарь)
    return SPACED.findall(text)


def matched_tokens(text, vocabulary):
    """Longest declared word wins; anything else is one character.

    Digits keep their runs — a numeral written with figures is one
    value in every script — and declared words are tried longest
    first, so «等于» is one token and not «等» plus «于».
    """
    if not vocabulary:
        return spaced_tokens(text)
    longest = max(len(w) for w in vocabulary)
    out, i, n = [], 0, len(text)
    while i < n:
        ch = text[i]
        if ch.isdigit() and ch.isascii():
            j = i
            while j < n and text[j].isdigit() and text[j].isascii():
                j += 1
            out.append(text[i:j])
            i = j
            continue
        if ch in GLYPHS:
            out.append(ch)
            i += 1
            continue
        if ch.isspace():
            i += 1
            continue
        взято = None
        for length in range(min(longest, n - i), 0, -1):
            кусок = text[i:i + length]
            if кусок in vocabulary:
                взято = кусок
                break
        if взято:
            out.append(взято)
            i += len(взято)
        elif ch.isalpha():
            out.append(ch)
            i += 1
        else:
            i += 1
    return out


def tokens(text, vocabulary=(), spaced=True):
    """The one entry point: the caller says which discipline applies."""
    return (spaced_tokens(text, set(vocabulary)) if spaced
            else matched_tokens(text, set(vocabulary)))
