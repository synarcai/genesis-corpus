#!/usr/bin/env python3
"""THE HOUSE OF CHAINS — a ledger of two steps in twenty-nine languages.

The owner's word: every language in surplus. Ten languages carry houses of
phrases; the other nineteen (am, ar, el, fa, fi, he, hi, hu, id, ja, ka,
ko, sv, sw, ta, th, uk, vi, zh) had lexicon and single equalities only —
and NOT ONE CHAIN: «6 + 5 = 11. 11 − 3 = 8.» — the form the market of
reasoning buys (holon, ONE-CARRIER: the ledger is the program is the
proof).

NOT ONE NEW WORD IS INVENTED. Every pack already declares, in its
`show_kinds.arithmetic`, the TEMPLATES of its equalities with holes —
«{num:n} plus {num:m} equals {num:sum}.», «{num:sum} 减 {num:m} 等于
{num:n}。», «{num:n} 足す {num:m} は {num:sum}.» — and the numerals that
fill them. This house reads those templates, tells addition from
subtraction and multiplication from division BY THE PLACE OF THE HOLES,
and writes two steps in a row where the result of the first is an operand
of the second. The court reads the same templates back, reads the numerals
to their numbers by the pack, recounts every step and checks the seam:
the number that leaves the first step is the number that enters the
second — a chain whose seam is broken is a lie.
"""
import json
import pathlib
import re

КОРЕНЬ = pathlib.Path(__file__).resolve().parents[1]
ПАКЕТЫ = КОРЕНЬ / "tools" / "langpacks"
_ДЫРА = re.compile(r"\{(num:)?([nms]\w*|sum|prod)\}")


def _пакеты():
    вон = {}
    for путь in sorted(ПАКЕТЫ.glob("*.json")):
        try:
            вон[путь.stem] = json.loads(путь.read_text(encoding="utf-8"))
        except ValueError:
            continue
    return вон


ПАКЕТЫ_ВСЕ = _пакеты()


def числительные(язык):
    """{value: word} of the pack — the only numbers this language may say."""
    вон = {}
    for ключ, слово in (ПАКЕТЫ_ВСЕ[язык].get("numerals") or {}).items():
        к = str(ключ)
        if k_целое(к):
            вон[int(к)] = str(слово)
    return вон


def k_целое(к):
    return k_цифры(к) and int(к) >= 0


def k_цифры(к):
    return к.lstrip("-").isdigit()


def _вид(шаблон):
    """(operation, hole order) of a declared template, read by the PLACE of its
    holes: «{num:n} + {num:m} = {num:sum}» is addition, «{num:sum} − {num:m} =
    {num:n}» subtraction, «{num:n} × {num:m} = {num:prod}» multiplication,
    «{num:prod} ÷ {num:m} = {num:n}» division; the same four with bare holes
    are the same operations written in figures."""
    имена = [м.group(2) for м in _ДЫРА.finditer(шаблон)]
    словами = all(м.group(1) for м in _ДЫРА.finditer(шаблон))
    if len(имена) != 3:
        return None
    порядок = tuple(имена)
    if порядок == ("n", "m", "sum"):
        return "+", словами
    if порядок == ("sum", "m", "n"):
        return "−", словами
    if порядок == ("n", "m", "prod"):
        return "×", словами
    if порядок == ("prod", "m", "n"):
        return "÷", словами
    return None


def шаблоны(язык):
    """{(operation, in words): template} — the pack's own table."""
    вон = {}
    род = (ПАКЕТЫ_ВСЕ[язык].get("show_kinds") or {}).get("arithmetic") or {}
    for ш in род.get("templates") or ():
        в = _вид(ш)
        if в is not None and в not in вон:
            вон[в] = ш
    return вон


ЯЗЫКИ = {л: ш for л, ш in ((л, шаблоны(л)) for л in ПАКЕТЫ_ВСЕ) if len(ш) >= 4}
ЧИСЛА = {л: числительные(л) for л in ЯЗЫКИ}


def умеет(язык, оп, словами=True):
    """Does the pack declare THIS operation in THIS writing? A chain never
    mixes the two writings — «6 + 5 = 11。 十一减三等于八。» is no chain of one
    house, and a language whose figures say only addition says none."""
    return (оп, словами) in ЯЗЫКИ[язык]


def шаг(язык, оп, a, b, r, словами=True):
    """One declared equality with its numbers in place: a op b = r, where the
    template decides which hole holds which number."""
    ш = ЯЗЫКИ[язык][(оп, словами)]
    т = ЧИСЛА[язык]
    пиши = (lambda x: т[x]) if all(м.group(1) for м in _ДЫРА.finditer(ш)) else str
    з = {"+": {"n": a, "m": b, "sum": r}, "−": {"sum": a, "m": b, "n": r},
         "×": {"n": a, "m": b, "prod": r}, "÷": {"prod": a, "m": b, "n": r}}[оп]
    return _ДЫРА.sub(lambda м: пиши(з[м.group(2)]), ш)


def цепь(язык, шаги, словами=True):
    """«6 + 5 = 11. 11 − 3 = 8.» — the steps in a row, the seam between them
    the number itself: шаги = ((op, a, b, r), …)."""
    return " ".join(шаг(язык, оп, a, b, r, словами) for оп, a, b, r in шаги)


def годно(язык, значения, словами=True):
    """Are all the numbers sayable in this language (the pack's numerals)?"""
    if not словами:
        return True
    т = ЧИСЛА[язык]
    return all(з in т for з in значения)


def _счёт(оп, a, b):
    if оп == "+":
        return a + b
    if оп == "−":
        return a - b
    if оп == "×":
        return a * b
    return a // b if b and a % b == 0 else None


def цепи(язык, словами=True):
    """The chains this language can say: two steps, the seam a number of the
    pack; built from the declared numerals only."""
    if not (умеет(язык, "+", словами) and умеет(язык, "−", словами)):
        return []
    т = sorted(ЧИСЛА[язык]) if словами else list(range(2, 40))
    вон = []
    for a in т:
        for b in т:
            if b < 1 or a < 1:
                continue
            s = a + b
            if s not in т and словами:
                continue
            for c in т:
                if c < 1 or c >= s:
                    continue
                r = s - c
                if словами and r not in т:
                    continue
                вон.append((("+", a, b, s), ("−", s, c, r)))
    return вон


# --- the court's side ---
def _образец(язык, ш):
    """The template as a pattern: every hole a group of the language's numbers."""
    т = ЧИСЛА[язык]
    словами = all(м.group(1) for м in _ДЫРА.finditer(ш))
    дыра = ("(" + "|".join(re.escape(с) for с in sorted(set(т.values()), key=lambda с: (-len(с), с))) + ")") if словами else r"(\d+)"
    куски, конец = [], 0
    for м in _ДЫРА.finditer(ш):
        куски.append(re.escape(ш[конец:м.start()])); куски.append(дыра); конец = м.end()
    куски.append(re.escape(ш[конец:]))
    return "".join(куски)


def образцы(язык):
    """[(pattern of one step, operation, hole order, in words)] — the pack's table."""
    вон = []
    for (оп, словами), ш in ЯЗЫКИ[язык].items():
        имена = [м.group(2) for м in _ДЫРА.finditer(ш)]
        вон.append((re.compile(_образец(язык, ш)), оп, имена, словами))
    return вон


ОБРАЗЦЫ = {л: образцы(л) for л in ЯЗЫКИ}
_ПО_СЛОВУ = {л: {с: з for з, с in ЧИСЛА[л].items()} for л in ЯЗЫКИ}


def разобрать_шаг(язык, кусок):
    """(operation, a, b, r) of one declared equality, or None."""
    for образец, оп, имена, словами in ОБРАЗЦЫ[язык]:
        м = образец.fullmatch(кусок.strip())
        if not м:
            continue
        читать = (lambda с: _ПО_СЛОВУ[язык].get(с)) if словами else (lambda с: int(с))
        з = {}
        for имя, г in zip(имена, м.groups()):
            v = читать(г)
            if v is None:
                return None
            з[имя] = v
        if оп == "+":
            return оп, з["n"], з["m"], з["sum"]
        if оп == "−":
            return оп, з["sum"], з["m"], з["n"]
        if оп == "×":
            return оп, з["n"], з["m"], з["prod"]
        return оп, з["prod"], з["m"], з["n"]
    return None


def _куски(строка):
    """The steps of a chain: a step ends where its template's own end stands
    («.», «。», «۔»), so the split is by the end mark plus a space."""
    return [к for к in re.split(r"(?<=[.。۔?؟!]) ", строка.strip()) if к.strip()]


def простое(n):
    return n > 1 and all(n % d for d in range(2, int(n ** 0.5) + 1))


def _перебор_держится(шаги):
    """THE SEARCH IS A CHAIN WITHOUT A SEAM (holon's choice 03.09, way «б»): a
    walk over consecutive candidates, each rejected by its own witness — «3 × 3
    = 9. 2 × 5 = 10. 1 × 11 = 11.» The results run one after another; every
    candidate but the last is composite and stands beside ITS LEAST divisor;
    the last stands beside one, and only a prime may — that is the predicate
    said without a word for it. A pack that never declared «prime» still shows
    the search, and the market sees the walk it must repeat."""
    if len(шаги) < 2 or any(оп != "×" for оп, _, _, _ in шаги):
        return False
    результаты = [r for _, _, _, r in шаги]
    if any(b - a != 1 for a, b in zip(результаты, результаты[1:])):
        return False
    for i, (_, a, b, r) in enumerate(шаги):
        последний = i == len(шаги) - 1
        меньший = min(a, b)
        if последний:
            if меньший != 1 or not простое(r):
                return False
        else:
            наименьший = next((d for d in range(2, r) if r % d == 0), None)
            if наименьший is None or меньший != наименьший:
                return False
    return True


def _две_страницы(куски):
    """Распадается ли ряд кусков на ДВЕ законченные страницы дома?"""
    for k in range(2, len(куски) - 1):
        левая, правая = " ".join(куски[:k]), " ".join(куски[k:])
        if судить(левая) == (True, True) and судить(правая) == (True, True):
            return True
    return False


def судить(строка):
    """(судимо, истинно): a chain of two or more declared equalities — either a
    LEDGER, whose seam holds (the result of a step is an operand of the next),
    or a SEARCH, whose results run consecutively and whose witnesses reject
    every candidate but the last."""
    с = строка.strip()
    куски = _куски(с)
    if len(куски) < 2:
        return False, False
    for язык in ЯЗЫКИ:
        шаги = [разобрать_шаг(язык, к) for к in куски]
        if any(ш is None for ш in шаги):
            continue
        for оп, a, b, r in шаги:
            if _счёт(оп, a, b) != r:
                return True, False
        # THE SEAM: the result of a step is an operand of the next
        шов = all(r1 in (a2, b2) for (_, _, _, r1), (_, a2, b2, _) in zip(шаги, шаги[1:]))
        if шов:
            return True, True
        if _перебор_держится(шаги):
            return True, True
        # СТРОКА, РАСПАДАЮЩАЯСЯ НА ДВЕ МОИ СТРАНИЦЫ, ЕСТЬ ДВЕ СТРАНИЦЫ, А НЕ ОДНА ЛОЖНАЯ
        # (16.09, прибор `scripts/prefix_traps.py`). Дом кует цепи от двух шагов до шести, и
        # по длине двух страниц подряд от одной не отличить; отличает их ДЕЛО: у ложной
        # цепи шов рвётся и половины её сами по себе ничем не связаны, а у двух страниц
        # каждая половина есть ЗАКОНЧЕННАЯ цепь — леджер или перебор.
        #
        #     СУД, ЧИТАЮЩИЙ НАЧАЛО СТРОКИ, ЕСТЬ ЛОВУШКА, ВЗВЕДЁННАЯ НА БУДУЩЕЕ. Вопрос «моя
        #     ли это строка» СТАРШЕ вопроса о её правоте, и здесь он задаётся последним лишь
        #     потому, что ответ на него дороже: его платят разрезом.
        #
        # Порча при этом не уходит: испорченное число рвёт свою половину, и обе половины
        # честными уже не будут — разрез не спасает ни одной подсадки дома.
        if _две_страницы(куски):
            return False, False
        return True, False
    return False, False


def перебор(язык, n):
    """The walk from n to the next prime, as the declared equalities say it, or
    None — the language cannot say one of the numbers."""
    т = ЧИСЛА[язык]
    if not умеет(язык, "×"):
        return None
    p = n + 1
    while not простое(p):
        p += 1
    шаги = []
    for m in range(n + 1, p + 1):
        d = next((d for d in range(2, m) if m % d == 0), 1)
        if m not in т or d not in т or (m // d) not in т:
            return None
        шаги.append(("×", d, m // d, m))
    return шаги if len(шаги) >= 2 else None


# ИМЕНА РОДОВ ДЛЯ ПЕРЕПИСИ ДОМОВ (`scripts/houses_census.py`): она печатает их тому, кто ищет
# в своде дыру, — чтобы дом не был построен второй раз.
#
# ИМЯ РОДА СТОИ́Т ЗДЕСЬ, А НЕ У ТАБЛИЦЫ, ИБО ТАБЛИЦЫ РОДОВ У ЭТОГО ДОМА НЕТ: род задан не
# ключом, а ГЛУБИНОЙ леджера — сколько шагов, и берёт ли следующий ответ предыдущего. Два
# строителя и суть два рода: `цепи` даёт двухшаговую, `перебор` — глубокую.
#
# ЧТО РОДОМ НЕ ОБЪЯВЛЕНО И ПОЧЕМУ: письмо цифрами (`словами=False`) есть умение СУДА читать
# такую запись, а не род страницы. В `datasets/genesis_chains_langs.txt` цифр нет ни одной —
# все числа писаны числительными языка, — и объявить письмо родом значило бы назвать родом то,
# чего в мире нет.
assert callable(цепи) and callable(перебор), "строителя рода не стало, а имя рода осталось"
РОДЫ = ("цепь из двух шагов: ответ первого есть вход второго",
        "цепь вглубь: от трёх до шести шагов, покуда числительные языка позволяют")


# ------------------------------------------------------------------ СТРАНИЦЫ МИРА
#
# СТРОИТЕЛИ ПЕРЕЕХАЛИ ИЗ КУЗНИЦЫ В ДОМ (13.09). Роды этот дом объявлял с первого дня, а
# страниц не отдавал: они строились в кузнице, и указатель родов не мог назвать ни одной из
# 3 092 строк мира.
#
#     ДОМ, ОБЪЯВИВШИЙ РОДЫ И НЕ ОТДАВШИЙ СТРАНИЦ, ОБЕЩАЕТ ИМЕНА, КОТОРЫХ НЕКОМУ ПРИЛОЖИТЬ.
#
# Кузница по-прежнему кует — она лишь берёт готовые группы отсюда.

def _пара(язык, шаг, i):
    """(a, b) whose sum and difference the language can say."""
    т = sorted(v for v in ЧИСЛА[язык] if v >= 1)
    for сдвиг in range(len(т)):
        a = т[(шаг * 7 + i * 5 + сдвиг) % len(т)]
        b = т[(шаг * 3 + i * 11 + сдвиг * 3) % len(т)]
        if a < 1 or b < 1 or (a + b) not in ЧИСЛА[язык]:
            continue
        return a, b
    return None


def _тройка(язык, шаг, i, оп):
    """(a, b) whose product (or quotient) and the next step the language can say."""
    т = sorted(v for v in ЧИСЛА[язык] if v >= 1)
    for сдвиг in range(len(т)):
        a = т[(шаг * 5 + i * 3 + сдвиг) % len(т)]
        b = т[(шаг * 11 + i * 7 + сдвиг * 2) % len(т)]
        if a < 2 or b < 2:
            continue
        p = a * b if оп == "×" else None
        if p is None or p not in ЧИСЛА[язык]:
            continue
        return a, b
    return None


def язык_группа_меченая(шаг, язык):
    """[(страница, род)] — и РОД БЕРЁТСЯ У СТРОИТЕЛЯ, а не считается по точкам (15.09).

    ПРЕЖНЯЯ РЕДАКЦИЯ ЧИТАЛА РОД ИЗ ГОТОВОЙ СТРОКИ: «вглубь, если точек больше двух». Справка
    её при этом гласила «род берётся у строителя: разбирать готовую строку не нужно» — и
    справка была права, а тело делало обратное.

        ФУНКЦИЯ, ЧЬЯ СПРАВКА ГОВОРИТ «РОД ОТ СТРОИТЕЛЯ», А ТЕЛО СЧИТАЕТ ТОЧКИ, БЕРЁТ РОД У
        ПИСЬМА. И письмо у языков РАЗНОЕ: китайская точка есть «。», и `count(".")` даёт на
        китайской странице ноль при любой глубине. Двадцать восемь языков клали цепи вглубь
        под своим именем, а китайский — все свои под именем двухшаговой цепи, и род «цепь
        вглубь» стоял на zh пустым.

    Нашла это МЕРА ЩЕРБАТОСТИ, впервые прочтя дом: язык был донесён до словаря показов в тот
    же день, и первая же клетка решётки оказалась пустой не по природе языка, а по знаку
    препинания.
    """
    вон = []
    двух, вглубь = РОДЫ
    если = умеет
    if not (если(язык, "+") and если(язык, "−")):
        return вон
    # six chains (+, −): the sum is spent by a subtraction
    for i in range(6):
        п = _пара(язык, шаг, i)
        if п is None:
            continue
        a, b = п
        s = a + b
        for c in sorted(v for v in ЧИСЛА[язык] if 1 <= v < s):
            if (s - c) in ЧИСЛА[язык] and c != b:
                вон.append((цепь(язык, (("+", a, b, s), ("−", s, c, s - c))), двух))
                break
    # three chains (×, +): the product is grown by an addition
    if если(язык, "×"):
        for i in range(3):
            п = _тройка(язык, шаг, i, "×")
            if п is None:
                continue
            a, b = п
            p = a * b
            for c in sorted(v for v in ЧИСЛА[язык] if v >= 1):
                if (p + c) in ЧИСЛА[язык] and c != a:
                    вон.append((цепь(язык, (("×", a, b, p), ("+", p, c, p + c))), двух))
                    break
    # chains of THREE and FOUR steps: the ledger of the market of reasoning, and
    # the food of the library of chains (holon 03.09: a bought chain becomes a
    # step of another, so depth is what the library eats)
    for i in range(6):
        цепочка = _вглубь(язык, шаг, i + 3, шагов=3)
        if цепочка:
            вон.append((цепь(язык, цепочка), вглубь))
    for i in range(4):
        цепочка = _вглубь(язык, шаг, i + 9, шагов=4)
        if цепочка:
            вон.append((цепь(язык, цепочка), вглубь))
    # ГЛУБЖЕ ЧЕТЫРЁХ (мандат владельца о цепочках вглубь): пять и шесть шагов
    # там, где объявленные числа языка позволяют пройти их — строитель
    # возвращает ничто, если пути нет, и язык с бедной таблицей просто не
    # пишет глубокой цепи вместо того, чтобы выдумать число.
    for i in range(3):
        цепочка = _вглубь(язык, шаг, i + 13, шагов=5)
        if цепочка:
            вон.append((цепь(язык, цепочка), вглубь))
    for i in range(2):
        цепочка = _вглубь(язык, шаг, i + 16, шагов=6)
        if цепочка:
            вон.append((цепь(язык, цепочка), вглубь))
    # THE SEARCH AS A CHAIN WITHOUT A SEAM (the collegium's task 2, way «б»
    # chosen by holon 03.09): the walk to the next prime, every candidate
    # rejected by its own witness, the last standing beside one — the predicate
    # said without a word for it, so a pack that never declared «prime» still
    # shows the search
    for i in range(4):
        n = 2 + (шаг * 7 + i * 5) % 60
        for сдвиг in range(60):
            ш = перебор(язык, n + сдвиг)
            if ш and 2 <= len(ш) <= 6:
                # ХОД К БЛИЖАЙШЕМУ ПРОСТОМУ ЕСТЬ ЦЕПЬ СВОЕЙ ДЛИНЫ: два шага — двухшаговая,
                # глубже — вглубь. Прежде это решала та же считалка точек.
                вон.append((цепь(язык, ш), двух if len(ш) <= 2 else вглубь))
                break
    return вон


def язык_группа(шаг, язык):
    """[страница] — то же, без меток: этим кормится кузница."""
    return [с for с, _р in язык_группа_меченая(шаг, язык)]


def _вглубь(язык, шаг, i, шагов):
    """A chain of `шагов` steps: every intermediate number is one the language
    declares, and every step spends the previous result."""
    т = sorted(v for v in ЧИСЛА[язык] if v >= 1)
    п = _пара(язык, шаг, i)
    if п is None:
        return None
    a, b = п
    s = a + b
    цепочка = [("+", a, b, s)]
    текущее = s
    # the operations walk in turn: −, ×, −, ÷ … — each taking the running number
    порядок = ("−", "×", "−", "+")
    for k in range(шагов - 1):
        оп = порядок[(k + шаг) % len(порядок)]
        нашли = False
        if оп == "−":
            for c in sorted(v for v in т if 1 <= v < текущее):
                if (текущее - c) in ЧИСЛА[язык] and (текущее - c) >= 2:
                    цепочка.append(("−", текущее, c, текущее - c)); текущее -= c; нашли = True
                    break
        elif оп == "×" and умеет(язык, "×"):
            for d in sorted(v for v in т if v >= 2):
                if (текущее * d) in ЧИСЛА[язык]:
                    цепочка.append(("×", текущее, d, текущее * d)); текущее *= d; нашли = True
                    break
        else:
            for c in sorted(v for v in т if v >= 1):
                if (текущее + c) in ЧИСЛА[язык]:
                    цепочка.append(("+", текущее, c, текущее + c)); текущее += c; нашли = True
                    break
        if not нашли:
            # the language cannot say the next number — the chain stops honestly
            return цепочка if len(цепочка) >= шагов - 1 and len(цепочка) >= 2 else None
    return цепочка


def группы(шаг):
    """[[страница]] — ровно те группы и в том порядке, какими кузница кормит `emit_grouped`."""
    return [язык_группа(шаг, язык) for язык in ЯЗЫКИ]


def перебор_с_языком(шаг):
    """[(страница, род, ЯЗЫК)] — тройка, и третье поле есть объявление языка страницы.

    ЯЗЫК СТОИТ В ЗАГОЛОВКЕ ЦИКЛА И ТЕРЯЛСЯ НА ПОРОГЕ СЛОВАРЯ (15.09): обход идёт по языкам и
    каждому отдаёт свою группу, а `ПОКАЗЫ` клали одно имя рода — и дом становился для меры
    щербатости НЕЧИТАЕМЫМ: не «ровным», а именно нечитаемым.

        ТО, ЧТО СТОИТ В ЗАГОЛОВКЕ ЦИКЛА, ЗНАЕТ СТРОИТЕЛЬ; ТО, ЧТО НЕ ЛЕГЛО В ОБЪЯВЛЕНИЕ, НЕ
        ЗНАЕТ НИКТО.

    Пара «(страница, род)» осталась при `перебор_страниц` нетронутой: её форму знают чужие
    читатели, и менять её ради третьего поля значило бы платить чужими договорами за своё
    объявление.
    """
    вон = []
    for язык in ЯЗЫКИ:
        вон.extend((с, р, язык) for с, р in язык_группа_меченая(шаг, язык))
    return вон


def перебор_страниц(шаг):
    """[(страница, род)] — те же группы, но каждая страница под своим именем."""
    return [(с, р) for с, р, _я in перебор_с_языком(шаг)]


ЗАЧЕМ_РОДА = {р: р for р in РОДЫ}


def _показы():
    """{строка свода: род} — ПОСТРОЧНО, ибо свод построчен."""
    from layer import PASSES                              # noqa: PLC0415
    вон = {}
    for шаг in range(len(PASSES)):
        for с, род, язык in перебор_с_языком(шаг):
            for строка in с.split("\n"):
                if строка.rstrip():
                    вон.setdefault(строка.rstrip(), (язык, род))
    return вон


ПОКАЗЫ = _показы()


def _самопроверка_страниц():
    assert all("\n" not in к for к in ПОКАЗЫ), "словарь показов обязан быть построчным"
    # ПОКАЗ НЕСЁТ ПАРУ «(ЯЗЫК, РОД)», И САМОПРОВЕРКА ЧИТАЕТ ОБЕ ПОЛОВИНЫ.
    сказанные = {я for я, _р in ПОКАЗЫ.values()}
    assert сказанные == set(ЯЗЫКИ), (
        f"язык объявлен и не кован либо кован и не объявлен: {sorted(сказанные ^ set(ЯЗЫКИ))}")
    пустые = set(РОДЫ) - {р for _я, р in ПОКАЗЫ.values()}
    assert not пустые, f"род объявлен и не кован: {sorted(пустые)}"
    из_перебора = sorted(с for с, _р in перебор_страниц(0))
    из_групп = sorted(с for г in группы(0) for с in г)
    assert из_перебора == из_групп, "пересборка потеряла или выдумала страницы"


_самопроверка_страниц()
