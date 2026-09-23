#!/usr/bin/env python3
"""[ШКОЛЬНЫЕ ФОРМЫ g1] — счёт основания пересчитывается, полярность судится итогом.

Мир gsmforms (tools/gen_genesis_gsmforms.py) показывает семейства конструкций,
немых по прибору FORM-MUTE (e9): сумма по носителям, температура ниже нуля,
процент от доли, унции в фунты, глубина из объёма, вероятность дробью, доля от
целого назад, дополнение. Суд не сверяет с записанным: он считает из данных строки
и сравнивает с итогом, с основанием после двоеточия и с полярностью («is not N: it
is M, because …»); вопрос судится своим ответом в той же строке.

СЦЕНЫ ДОМА ПЕРЕПИСАНЫ 23.09 (полоса — прибор, а не источник), и слова образцов
переписаны вслед: законы рамок — те же лямбды над теми же числами.
"""
import json
import pathlib
import re
import sys

КОРЕНЬ = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(КОРЕНЬ / "tools"))
import asking  # noqa: E402
import families  # noqa: E402
import rugram  # noqa: E402
import closedworld  # noqa: E402
from closedworld import Слой  # noqa: E402 — палата подаёт имя мира

Ч = r"(−?\d+)"
# ИМЯ ЛИЦА ПИШЕТСЯ С ЗАГЛАВНОЙ (пакет, 05.09) — класс букв обязан знать обе
# кассы; класс «[a-z]+» назвал 96 честных строк несудимыми в тот час, как
# пакет стал объявлять письмо имени сам
С = r"([A-Za-zА-Яа-яЁё]+)"
ИМЯ = r"([A-Za-zА-Яа-яЁё]+)"


def _n(т):
    return int(т.replace("−", "-"))


def _ч(n):
    return str(n).replace("-", "−")


def _форма_ru(вещь, n):
    ключ = rugram.ПО_ФОРМЕ.get(вещь)
    return ключ is not None and rugram.форма(ключ, n) == вещь


# 1. сумма
def _сумма(м):
    a, x, в_x, b, y, в_y, вещь, s, ox, oy, os = м.groups()
    x, y, s = _n(x), _n(y), _n(s)
    return a != b and x + y == s and (ox, oy, os) == (str(x), str(y), str(s))


def _сумма_не(м):
    a, x, в_x, b, y, в_y, вещь, чуж, ист = м.groups()
    x, y = _n(x), _n(y)
    return a != b and _n(ист) == x + y and _n(чуж) != x + y


def _сумма_ru(м):
    a, x, в_x, b, y, в_y, s, вs, ox, oy, os = м.groups()
    x, y, s = _n(x), _n(y), _n(s)
    return (a != b and x + y == s and (ox, oy, os) == (str(x), str(y), str(s))
            and _форма_ru(в_x, x) and _форма_ru(в_y, y) and _форма_ru(вs, s))


# 2. температура
def _температура(м):
    t0, глагол, d, t1, o0, знак, od, o1 = м.groups()
    t0, d, t1 = _n(t0), _n(d), _n(t1)
    падение = глагол in ("fell", "упала")
    ист = t0 - d if падение else t0 + d
    return (t1 == ист and _n(o0) == t0 and _n(od) == d and _n(o1) == t1
            and знак == ("−" if падение else "+"))


def _температура_не(м):
    t0, глагол, d, чуж, ист = м.groups()
    t0, d = _n(t0), _n(d)
    верно = t0 - d if глагол == "fell" else t0 + d
    return _n(ист) == верно and _n(чуж) != верно


# 3. процент
def _процент(м):
    всего, часть, p, o_ч, o_в, op = (_n(x) for x in м.groups())
    return 0 < часть < всего and часть * 100 == p * всего and (o_ч, o_в, op) == (часть, всего, p)


def _процент_не(м):
    всего, часть, чуж, ист = (_n(x) for x in м.groups())
    return часть * 100 == ист * всего and чуж != ист


# 4. фунты
def _фунты(м):
    унц, ф, o_у, o_ф = (_n(x) for x in м.groups()[:4])
    return унц == 16 * ф and (o_у, o_ф) == (унц, ф)


def _фунты_не(м):
    унц, чуж, ист = (_n(x) for x in м.groups())
    return унц == 16 * ист and чуж != ист


# 5. глубина
def _глубина(м):
    w, l, v, h, ov, ow, ol, oh = (_n(x) for x in м.groups())
    return v == w * l * h and (ov, ow, ol, oh) == (v, w, l, h)


def _глубина_не(м):
    w, l, v, чуж, ист = (_n(x) for x in м.groups())
    return v == w * l * ист and чуж != ист


# 6. вероятность
def _вероятность(м):
    """Дробь ответа и выкладка суммы: «is 3/8: 3 + 5 = 8 buttons, 3 of them black»."""
    r, b, num, den, or_, ob, on, or2 = (_n(x) for x in м.groups())
    return num == r and den == r + b and (or_, ob, on, or2) == (r, b, r + b, r)


def _вероятность_не(м):
    r, b, чn, чd, иn, иd = (_n(x) for x in м.groups())
    return (иn, иd) == (r, r + b) and (чn, чd) != (r, r + b)


# 7. четверти
СЛОВА_ЧЕТВЕРТЕЙ = {"one quarter": 1, "two quarters": 2, "three quarters": 3,
                   "четверть": 1, "две четверти": 2, "три четверти": 3}


def _четверти(м):
    """ИТОГ ВЫКЛАДКИ СВЕРЯЕТСЯ (23.09): образец держал «= \\d+» без группы, и итог
    «3 ÷ 1 × 4 = 13» при целом 12 судом не читался вовсе."""
    часть, слово, целое, o_ч, ok, o4, итог = м.groups()
    часть, целое, k = _n(часть), _n(целое), СЛОВА_ЧЕТВЕРТЕЙ[слово]
    return (часть * 4 == целое * k and (_n(o_ч), _n(ok)) == (часть, k) and o4 == "4"
            and _n(итог) == целое)


def _четверти_не(м):
    часть, слово, чуж, ист = м.groups()
    часть, k = _n(часть), СЛОВА_ЧЕТВЕРТЕЙ[слово]
    return часть * 4 == _n(ист) * k and _n(чуж) != _n(ист)


# 8. дополнение
def _разность(м):
    """a − b = c с основанием «a − b = c» — общий закон трёх родов дополнения."""
    a, b, c, oa, ob, oc = (_n(x) for x in м.groups()[:6])
    return a - b == c and (oa, ob, oc) == (a, b, c)


def _разность_не(м):
    a, b, чуж, ист = (_n(x) for x in м.groups()[:4])
    return a - b == _n(str(ист)) and _n(str(чуж)) != a - b


# ВОПРОСЫ: ответ = величины вопроса в их порядке + счёт; суд пересчитывает.
def _сумма_qa(м):
    a, x, _в_x, b, y, _в_y, _вещь, ox, oy, s = м.groups()
    return a != b and (_n(ox), _n(oy)) == (_n(x), _n(y)) and _n(x) + _n(y) == _n(s)


def _температура_qa(м):
    t0, глагол, d, o0, знак, od, t1 = м.groups()
    t0, d, t1 = _n(t0), _n(d), _n(t1)
    падение = глагол == "fell"
    return (_n(o0), _n(od)) == (t0, d) and знак == ("−" if падение else "+") and t1 == (t0 - d if падение else t0 + d)


def _процент_qa(м):
    всего, часть, o_в, o_ч, o_ч2, o_в2, p = (_n(x) for x in м.groups())
    return (o_в, o_ч, o_ч2, o_в2) == (всего, часть, часть, всего) and 0 < часть < всего and часть * 100 == p * всего


def _фунты_qa(м):
    унц, o_у, ф = (_n(x) for x in м.groups())
    return o_у == унц and унц == 16 * ф


def _глубина_qa(м):
    w, l, v, ow, ol, ov, ov2, ow2, ol2, h = (_n(x) for x in м.groups())
    return (ow, ol, ov, ov2, ow2, ol2) == (w, l, v, v, w, l) and v == w * l * h


def _вероятность_qa(м):
    r, b, or_, ob, n, num, den = (_n(x) for x in м.groups())
    return (or_, ob) == (r, b) and n == r + b and (num, den) == (r, n)


def _четверти_qa(м):
    часть, слово, o_ч, ok, o4, целое = м.groups()
    часть, целое, k = _n(часть), _n(целое), СЛОВА_ЧЕТВЕРТЕЙ[слово]
    return (_n(o_ч), _n(ok)) == (часть, k) and o4 == "4" and часть * 4 == целое * k


def _разность_qa(м):
    a, b, oa, ob, c = (_n(x) for x in м.groups()[:5])
    return (oa, ob) == (a, b) and a - b == c


# ВТОРОЙ СЛОЙ — семейства 9–17 и роды SVAMP: закон каждой рамки — лямбда над
# числами рамки в порядке групп; полярность — своим образцом.
СЛОВА_ДОЛЕЙ = {"half": 2, "a quarter": 4, "a fifth": 5, "a tenth": 10, "половина": 2, "четверть": 4, "пятая часть": 5, "десятая часть": 10}
# ДОМ ИМЁН ПО-РУССКИ: родительный падеж имени объявлен пакетом (person_forms),
# и суд читает «у Веры было … Вера отдала» той же таблицей, что генератор.
_RU = json.loads((pathlib.Path(__file__).resolve().parents[1] / "tools" / "langpacks" / "ru.json").read_text(encoding="utf-8"))
РОД_П = {n.capitalize(): ф["gen"].capitalize() for n, ф in _RU["person_forms"].items()}


def _тот_же(род_п, имя):
    """«Маши» и «Маша» — одно лицо: родительный из пакета."""
    return род_п == РОД_П.get(имя)


# КРАТНЫЕ СЛОВА ЧИТАЮТСЯ СЛОВАРЁМ ПАКЕТОВ (asking.ВЕЛИЧИНЫ_СЛОВОМ) — тем
# же, каким дом пары читает вопрос; доли — своим чтением, ибо доля есть
# часть, и её число здесь — делитель.
СЛОВА_КРАТНОСТИ = asking.ВЕЛИЧИНЫ_СЛОВОМ


def _остаток_общий(T, n, g, r, on, og, ng, oT, ong, orr):
    """Закон остатка: леджер сходится, остаток есть и меньше группы."""
    return ((on, og, oT, ong, orr) == (n, g, T, ng, r) and ng == n * g
            and T == ng + r and 0 < r < n)


def _остаток_en(*г):
    if len(г) == 11:                      # рассказ: со словом при остатке
        T, n, g, r, сл, on, og, ng, oT, ong, orr = г
        if сл != ("egg" if r == 1 else "eggs"):
            return False
    elif len(г) == 8:                     # вопрос: остаток стои́т лишь в леджере
        T, n, on, og, ng, oT, ong, orr = г
        g, r = og, orr
    else:
        return False
    return _остаток_общий(T, n, g, r, on, og, ng, oT, ong, orr)


def _остаток_ru(*г):
    """«яиц 14, … и осталось 2 яйца» — число всего стоит после имени (согласования нет),
    форма остатка сверяется со счётом."""
    if len(г) == 11:
        T, n, g, r, с_r, on, og, ng, oT, ong, orr = г
        if not _форма_ru(с_r, r):
            return False
    elif len(г) == 8:
        T, n, on, og, ng, oT, ong, orr = г
        g, r = og, orr
    else:
        return False
    return _остаток_общий(T, n, g, r, on, og, ng, oT, ong, orr)


def _рамка(закон):
    """Суд рамки: числа рамки (все группы, кроме словесных) → закон."""
    def проверить(м):
        г = []
        for x in м.groups():
            if x is None:
                continue
            if re.fullmatch(r"−?\d+", x):
                г.append(_n(x))
            elif x in СЛОВА_ДОЛЕЙ:
                г.append(СЛОВА_ДОЛЕЙ[x])
            elif x in СЛОВА_КРАТНОСТИ:
                г.append(СЛОВА_КРАТНОСТИ[x])
            else:
                г.append(x)
        try:
            исход = закон(*г)
        except (TypeError, ZeroDivisionError, ValueError):
            return False
        # ТРЕТИЙ ИСХОД ЗАКОНА: None — «рамка поймала, но строка не моя» (16.09).
        # Прежде исходов было два, и всякая чужая страница, попавшая в рамку,
        # звалась ЛОЖЬЮ. Закон, умеющий сказать лишь «да» и «нет», говорит «нет»
        # и о том, чего не знает.
        return None if исход is None else bool(исход)
    return проверить


ДОЛЯ = r"(half|a quarter|a fifth|a tenth|половина|четверть|пятая часть|десятая часть)"
КРАТ = r"(twice|three times|four times|вдвое|втрое|вчетверо)"
УДВ = r"(doubled|tripled|удвоили|утроили)"
ОСН = rf"{Ч} ([+−]) {Ч} = {Ч}"
ОБРАЗЦЫ = (
    (rf"^{С} has {Ч} {С} and {С} has {Ч} {С}; the total number of {С} is {Ч}: {Ч} \+ {Ч} = {Ч}\.$", _сумма),
    (rf"^{С} has {Ч} {С} and {С} has {Ч} {С}\. what's the total number of {С}\? {Ч} \+ {Ч} = {Ч}\.$", _сумма_qa),
    (rf"^{С} has {Ч} {С} and {С} has {Ч} {С}; the total number of {С} is not {Ч}: it is {Ч}\.$", _сумма_не),
    (rf"^{ИМЯ} имеет {Ч} {С}, {ИМЯ} имеет {Ч} {С}; всего у них {Ч} {С}: {Ч} \+ {Ч} = {Ч}\.$", _сумма_ru),
    (rf"^the temperature was {Ч} degrees? and (fell|rose) by {Ч} degrees?; the temperature in degrees is now {Ч}: {Ч} ([+−]) {Ч} = {Ч}\.$", _температура),
    (rf"^the temperature was {Ч} degrees? and (fell|rose) by {Ч} degrees?\. what is the temperature in degrees now\? {Ч} ([+−]) {Ч} = {Ч}\.$", _температура_qa),
    (rf"^температура была {Ч} градус(?:а|ов)? и (упала|поднялась) на {Ч} градус(?:а|ов)?; теперь температура — {Ч} градус(?:а|ов)?: {Ч} ([+−]) {Ч} = {Ч}\.$", _температура),
    (rf"^the temperature was {Ч} degrees? and (fell|rose) by {Ч} degrees?; the temperature in degrees is not {Ч}: it is {Ч}\.$", _температура_не),
    (rf"^the orchard has {Ч} trees and {Ч} of them (?:is a pear tree|are pear trees); the percentage of pear trees is {Ч} %: {Ч} ÷ {Ч} × 100 = {Ч}\.$", _процент),
    (rf"^the orchard has {Ч} trees and {Ч} of them (?:is a pear tree|are pear trees)\. what percentage of the trees are pear trees\? {Ч} trees and {Ч} pear trees?: {Ч} ÷ {Ч} × 100 = {Ч} %\.$", _процент_qa),
    (rf"^в саду {Ч} дерев(?:о|а|ьев), из них {Ч} груш(?:а|и)?; доля груш — {Ч} %: {Ч} ÷ {Ч} × 100 = {Ч}\.$", _процент),
    (rf"^the orchard has {Ч} trees and {Ч} of them (?:is a pear tree|are pear trees); the percentage of pear trees is not {Ч} %: it is {Ч} %\.$", _процент_не),
    (rf"^a bag of apples weighs {Ч} ounces and a pound is 16 ounces; the weight in pounds is {Ч}: {Ч} ÷ 16 = {Ч}\.$", _фунты),
    (rf"^a bag of apples weighs {Ч} ounces and a pound is 16 ounces\. what is the weight in pounds\? {Ч} ounces: {Ч} ÷ 16 = {Ч}\.$", _рамка(lambda у, o_у0, o_у, ф: (o_у0, o_у) == (у, у) and у == 16 * ф)),
    (rf"^мешок яблок весит {Ч} унци[йия], а в фунте 16 унций; вес в фунтах — {Ч} фунт(?:а|ов)?: {Ч} ÷ 16 = {Ч}\.$", _фунты),
    (rf"^a bag of apples weighs {Ч} ounces and a pound is 16 ounces; the weight in pounds is not {Ч}: it is {Ч}\.$", _фунты_не),
    (rf"^the pit is {Ч} meters wide and {Ч} meters long and holds {Ч} cubic meters of sand; the sand in the pit is {Ч} meters? deep: {Ч} ÷ \({Ч} × {Ч}\) = {Ч}\.$", _глубина),
    (rf"^the pit is {Ч} meters wide and {Ч} meters long and holds {Ч} cubic meters of sand\. how deep is the sand in the pit\? {Ч} by {Ч} holding {Ч}: {Ч} ÷ \({Ч} × {Ч}\) = {Ч} meters?\.$", _глубина_qa),
    (rf"^яма шириной {Ч} метр(?:а|ов)? и длиной {Ч} метр(?:а|ов)? вмещает {Ч} кубическ(?:ий|их) метр(?:а|ов)? песка; слой песка в яме — {Ч} метр(?:а|ов)?: {Ч} ÷ \({Ч} × {Ч}\) = {Ч}\.$", _глубина),
    (rf"^the pit is {Ч} meters wide and {Ч} meters long and holds {Ч} cubic meters of sand; the sand in the pit is not {Ч} meters? deep: it is {Ч} meters? deep\.$", _глубина_не),
    (rf"^a jar holds {Ч} black buttons? and {Ч} white buttons?; the probability of taking a black button, written as a fraction, is {Ч}/{Ч}: {Ч} \+ {Ч} = {Ч} buttons, {Ч} of them black\.$", _вероятность),
    (rf"^a jar holds {Ч} black buttons? and {Ч} white buttons?\. what is the probability of taking a black button, written as a fraction\? {Ч} \+ {Ч} = {Ч}: {Ч}/{Ч}\.$", _вероятность_qa),
    (rf"^в банке чёрных пуговиц {Ч}, а белых {Ч}; вероятность взять чёрную пуговицу, записанная дробью, — {Ч}/{Ч}: {Ч} \+ {Ч} = {Ч}, из них чёрных {Ч}\.$", _вероятность),
    (rf"^a jar holds {Ч} black buttons? and {Ч} white buttons?; the probability of taking a black button, written as a fraction, is not {Ч}/{Ч}: it is {Ч}/{Ч}\.$", _вероятность_не),
    (rf"^if {Ч} pages are (one quarter|two quarters|three quarters) of the book, the book has {Ч} pages: {Ч} ÷ {Ч} × (4) = {Ч}\.$", _четверти),
    (rf"^if {Ч} pages are (one quarter|two quarters|three quarters) of the book, how many pages does the book have\? {Ч} ÷ {Ч} × (4) = {Ч}\.$", _четверти_qa),
    (rf"^если {Ч} страниц(?:а|ы)? — это (четверть|две четверти|три четверти) книги, в книге {Ч} страниц(?:а|ы)?: {Ч} ÷ {Ч} × (4) = {Ч}\.$", _четверти),
    (rf"^if {Ч} pages are (one quarter|two quarters|three quarters) of the book, the book does not have {Ч} pages: it has {Ч}\.$", _четверти_не),
    (rf"^there were originally {Ч} ducks on the pond and {Ч} flew away; {Ч} ducks? remains?: {Ч} − {Ч} = {Ч}\.$", _разность),
    (rf"^if there were originally {Ч} ducks on the pond and {Ч} flew away, how many ducks remain\? {Ч} − {Ч} = {Ч}\.$", _разность_qa),
    (rf"^на пруду изначально было {Ч} ут(?:ка|ки|ок), {Ч} улетел[аи]; осталось {Ч} ут(?:ка|ки|ок): {Ч} − {Ч} = {Ч}\.$", _разность),
    (rf"^there were originally {Ч} ducks on the pond and {Ч} flew away; {Ч} ducks do not remain: {Ч} remains?\.$", _разность_не),
    (rf"^the album has room for {Ч} stamps and {Ч} (?:is|are) glued in; {Ч} stamps? (?:are|is) missing: {Ч} − {Ч} = {Ч}\.$", _разность),
    (rf"^the album has room for {Ч} stamps and {Ч} (?:is|are) glued in\. how many stamps are missing\? {Ч} − {Ч} = {Ч}\.$", _разность_qa),
    (rf"^мест для марок в альбоме {Ч}, вклеен[ао] {Ч} мар(?:ка|ки|ок); не хватает {Ч}: {Ч} − {Ч} = {Ч}\.$", _разность),
    (rf"^the album has room for {Ч} stamps and {Ч} (?:is|are) glued in; {Ч} stamps are not missing: {Ч} (?:are|is) missing\.$", _разность_не),
    (rf"^there were {Ч} guests at the party and {Ч} went home; {Ч} guests? (?:are|is) at the party now: {Ч} − {Ч} = {Ч}\.$", _разность),
    (rf"^if there were {Ч} guests at the party and {Ч} went home, how many guests are at the party now\? {Ч} − {Ч} = {Ч}\.$", _разность_qa),
    (rf"^на празднике было {Ч} гост(?:ь|я|ей), {Ч} (?:ушёл|ушли) домой; теперь на празднике {Ч} гост(?:ь|я|ей): {Ч} − {Ч} = {Ч}\.$", _разность),
    (rf"^there were {Ч} guests at the party and {Ч} went home; the number of guests at the party now is not {Ч}: it is {Ч}\.$", _разность_не),
)
ОБРАЗЦЫ_2 = (
    # 9 население: всего, доля, часть, всего, доля, часть
    (rf"^the library has {Ч} books and {ДОЛЯ} of all the books stand in the reading room; {Ч} books stand in the reading room: {Ч} ÷ {Ч} = {Ч}\.$",
     _рамка(lambda N, d, c, oN, od, oc: N == d * c and (oN, od, oc) == (N, d, c))),
    (rf"^в библиотеке {Ч} книг[аи]?, и {ДОЛЯ} всех книг стоит в читальном зале; в читальном зале стоит {Ч} книг[аи]?: {Ч} ÷ {Ч} = {Ч}\.$",
     _рамка(lambda N, d, c, oN, od, oc: N == d * c and (oN, od, oc) == (N, d, c))),
    (rf"^the library has {Ч} books and {ДОЛЯ} of all the books stand in the reading room; the number of books in the reading room is not {Ч}: it is {Ч}\.$",
     _рамка(lambda N, d, ч, и: N == d * и and ч != и)),
    (rf"^if the library has {Ч} books and {ДОЛЯ} of all the books stand in the reading room, how many books stand in the reading room\? {Ч} books: {Ч} ÷ {Ч} = {Ч}\.$",
     _рамка(lambda N, d, oN0, oN, od, c: (oN0, oN, od) == (N, N, d) and N == d * c)),
    # 10 команда
    (rf"^the number of books on the shelf is {Ч} and the number of magazines is {Ч}; the shelf holds {Ч} items: {Ч} \+ {Ч} = {Ч}\.$",
     _рамка(lambda m, d, s, om, od, os: m + d == s and (om, od, os) == (m, d, s))),
    (rf"^на полке {Ч} книг[аи]? и {Ч} журнал(?:а|ов)?; всего на полке {Ч} предмет(?:а|ов)?: {Ч} \+ {Ч} = {Ч}\.$",
     _рамка(lambda m, d, s, om, od, os: m + d == s and (om, od, os) == (m, d, s))),
    (rf"^the number of books on the shelf is {Ч} and the number of magazines is {Ч}; the shelf does not hold {Ч} items: it holds {Ч}\.$",
     _рамка(lambda m, d, ч, и: m + d == и and ч != и)),
    (rf"^if the number of books on the shelf is {Ч} and the number of magazines is {Ч}, how many items does the shelf hold\? {Ч} \+ {Ч} = {Ч}\.$",
     _рамка(lambda m, d, om, od, s: (om, od) == (m, d) and m + d == s)),
    # 11 кратно
    (rf"^the tractor cost {Ч} dollars and the barn cost {КРАТ} as much as the tractor; the barn cost {Ч} dollars: {Ч} × {Ч} = {Ч}\.$",
     _рамка(lambda c, k, h, oc, ok, oh: h == k * c and (oc, ok, oh) == (c, k, h))),
    (rf"^трактор стоил {Ч} доллар(?:а|ов)?, а амбар стоил {КРАТ} дороже трактора; амбар стоил {Ч} доллар(?:а|ов)?: {Ч} × {Ч} = {Ч}\.$",
     _рамка(lambda c, k, h, oc, ok, oh: h == k * c and (oc, ok, oh) == (c, k, h))),
    (rf"^the tractor cost {Ч} dollars and the barn cost {КРАТ} as much as the tractor; the barn did not cost {Ч} dollars: it cost {Ч}\.$",
     _рамка(lambda c, k, ч, и: и == k * c and ч != и)),
    (rf"^if the tractor cost {Ч} dollars and the barn cost {КРАТ} as much as the tractor, how much did the barn cost\? {Ч} × {Ч} = {Ч} dollars\.$",
     _рамка(lambda c, k, oc, ok, h: (oc, ok) == (c, k) and h == k * c)),
    # 12 проект
    (rf"^the order started with {Ч} boxes, was {УДВ} and then reduced by {Ч}; the final order has {Ч} boxes: {Ч} × {Ч} − {Ч} = {Ч}\.$",
     _рамка(lambda s0, k, m, f, os0, ok, om, of: f == s0 * k - m and (os0, ok, om, of) == (s0, k, m, f))),
    (rf"^заказ начинался с {Ч} короб(?:ки|ок), его {УДВ} и потом убавили на {Ч}; в итоговом заказе {Ч} короб(?:ка|ки|ок): {Ч} × {Ч} − {Ч} = {Ч}\.$",
     _рамка(lambda s0, k, m, f, os0, ok, om, of: f == s0 * k - m and (os0, ok, om, of) == (s0, k, m, f))),
    (rf"^the order started with {Ч} boxes, was {УДВ} and then reduced by {Ч}; the final order does not have {Ч} boxes: it has {Ч}\.$",
     _рамка(lambda s0, k, m, ч, и: и == s0 * k - m and ч != и)),
    (rf"^if the order started with {Ч} boxes, was {УДВ} and then reduced by {Ч}, how many boxes does the final order have\? {Ч} × {Ч} − {Ч} = {Ч}\.$",
     _рамка(lambda s0, k, m, os0, ok, om, f: (os0, ok, om) == (s0, k, m) and f == s0 * k - m)),
    # 13 окружность
    (rf"^the road around the lake is {Ч} kilometers long and the cyclist rides {Ч} kilometers per hour; the ride around the lake takes {Ч} hours: {Ч} ÷ {Ч} = {Ч}\.$",
     _рамка(lambda L, v, t, oL, ov, ot: L == v * t and (oL, ov, ot) == (L, v, t))),
    (rf"^дорога вокруг озера длиной {Ч} километр(?:а|ов)?, велосипедист едет {Ч} километр(?:а|ов)? в час; поездка вокруг озера занимает {Ч} час(?:а|ов)?: {Ч} ÷ {Ч} = {Ч}\.$",
     _рамка(lambda L, v, t, oL, ov, ot: L == v * t and (oL, ov, ot) == (L, v, t))),
    (rf"^the road around the lake is {Ч} kilometers long and the cyclist rides {Ч} kilometers per hour; the ride around the lake does not take {Ч} hours: it takes {Ч}\.$",
     _рамка(lambda L, v, ч, и: L == v * и and ч != и)),
    (rf"^if the road around the lake is {Ч} kilometers long and the cyclist rides {Ч} kilometers per hour, how many hours does the ride around the lake take\? {Ч} ÷ {Ч} = {Ч}\.$",
     _рамка(lambda L, v, oL, ov, t: (oL, ov) == (L, v) and L == v * t)),
    # 14 верёвки
    (rf"^the {Ч} poles had a total height of {Ч} meters; the average pole is {Ч} meters tall: {Ч} ÷ {Ч} = {Ч}\.$",
     _рамка(lambda n, T, a, oT, on, oa: T == n * a and (oT, on, oa) == (T, n, a))),
    (rf"^{Ч} столб(?:а|ов)? имели общую высоту {Ч} метр(?:а|ов)?; средний столб высотой {Ч} метр(?:а|ов)?: {Ч} ÷ {Ч} = {Ч}\.$",
     _рамка(lambda n, T, a, oT, on, oa: T == n * a and (oT, on, oa) == (T, n, a))),
    (rf"^the {Ч} poles had a total height of {Ч} meters; the average pole is not {Ч} meters tall: it is {Ч} meters\.$",
     _рамка(lambda n, T, ч, и: T == n * и and ч != и)),
    (rf"^if the total height of the poles is {Ч} meters and there are {Ч} poles, how tall is the average pole\? {Ч} ÷ {Ч} = {Ч} meters\.$",
     _рамка(lambda T, n, oT, on, a: (oT, on) == (T, n) and T == n * a)),
    # 15 трое
    (rf"^{С} has {Ч} shells, {С} has {Ч} more shells than {С}, and {С} has {КРАТ} as many shells as {С}; together {С}, {С} and {С} have {Ч} shells: {Ч} \+ \({Ч} \+ {Ч}\) \+ {Ч} × {Ч} = {Ч}\.$",
     _рамка(lambda x, a, y, b, x2, z, k, x3, x4, y2, z2, s, oa, oa2, ob, ok, oa3, os: x == x2 == x3 == x4 and y == y2 and z == z2 and (oa, oa2, ob, ok, oa3) == (a, a, b, k, a) and s == os == a + (a + b) + k * a)),
    (rf"^{ИМЯ} имеет {Ч} ракуш(?:ка|ки|ек), {ИМЯ} имеет на {Ч} ракуш(?:ка|ки|ек) больше, чем {ИМЯ}, а {ИМЯ} имеет {КРАТ} больше ракушек, чем {ИМЯ}; вместе у них {Ч} ракуш(?:ка|ки|ек): {Ч} \+ \({Ч} \+ {Ч}\) \+ {Ч} × {Ч} = {Ч}\.$",
     _рамка(lambda x, a, y, b, x2, z, k, x3, s, oa, oa2, ob, ok, oa3, os: x == x2 == x3 and (oa, oa2, ob, ok, oa3) == (a, a, b, k, a) and s == os == a + (a + b) + k * a)),
    (rf"^{С} has {Ч} shells, {С} has {Ч} more shells than {С}, and {С} has {КРАТ} as many shells as {С}; together they do not have {Ч} shells: they have {Ч}\.$",
     _рамка(lambda x, a, y, b, x2, z, k, x3, ч, и: x == x2 == x3 and и == a + (a + b) + k * a and ч != и)),
    (rf"^if {С} has {Ч} shells, {С} has {Ч} more shells than {С}, and {С} has {КРАТ} as many shells as {С}, how many shells do they have together\? {Ч} \+ \({Ч} \+ {Ч}\) \+ {Ч} × {Ч} = {Ч}\.$",
     _рамка(lambda x, a, y, b, x2, z, k, x3, oa, oa2, ob, ok, oa3, s: x == x2 == x3 and (oa, oa2, ob, ok, oa3) == (a, a, b, k, a) and s == a + (a + b) + k * a)),
    # 16 ставка
    (rf"^{С} signs {Ч} postcards an hour and works {Ч} hours; {С} signs {Ч} postcards: {Ч} × {Ч} = {Ч}\.$",
     _рамка(lambda n1, r, t, n2, s, or_, ot, os: n1 == n2 and s == r * t and (or_, ot, os) == (r, t, s))),
    (rf"^{ИМЯ} подписывает {Ч} открыт(?:ка|ки|ок) в час и работает {Ч} час(?:а|ов)?; {ИМЯ} подписывает {Ч} открыт(?:ка|ки|ок): {Ч} × {Ч} = {Ч}\.$",
     _рамка(lambda n1, r, t, n2, s, or_, ot, os: n1 == n2 and s == r * t and (or_, ot, os) == (r, t, s))),
    (rf"^{С} signs {Ч} postcards an hour and works {Ч} hours; {С} does not sign {Ч} postcards: {С} signs {Ч}\.$",
     _рамка(lambda n1, r, t, n2, ч, n3, и: n1 == n2 == n3 and и == r * t and ч != и)),
    (rf"^if {С} signs {Ч} postcards an hour and works {Ч} hours, how many postcards does {С} sign\? {Ч} × {Ч} = {Ч}\.$",
     _рамка(lambda n1, r, t, n2, or_, ot, s: n1 == n2 and (or_, ot) == (r, t) and s == r * t)),
    # 17 листки
    (rf"^{С} had {Ч} candies, put {Ч} in the red bowl and {Ч} in the blue bowl; {С} has {Ч} candies left: {Ч} − {Ч} − {Ч} = {Ч}\.$",
     _рамка(lambda n1, b, r, d, n2, s, ob, or_, od, os: n1 == n2 and s == b - r - d and (ob, or_, od, os) == (b, r, d, s))),
    (rf"^у {ИМЯ} было {Ч} конфет(?:а|ы)?, {Ч} ушли в красную вазу и {Ч} в синюю; осталось {Ч} конфет(?:а|ы)?: {Ч} − {Ч} − {Ч} = {Ч}\.$",
     _рамка(lambda n1, b, r, d, s, ob, or_, od, os: s == b - r - d and (ob, or_, od, os) == (b, r, d, s))),
    (rf"^{С} had {Ч} candies, put {Ч} in the red bowl and {Ч} in the blue bowl; {С} does not have {Ч} candies left: {С} has {Ч}\.$",
     _рамка(lambda n1, b, r, d, n2, ч, n3, и: n1 == n2 == n3 and и == b - r - d and ч != и)),
    (rf"^if {С} had {Ч} candies, put {Ч} in the red bowl and {Ч} in the blue bowl, how many candies does {С} have left\? {Ч} − {Ч} − {Ч} = {Ч}\.$",
     _рамка(lambda n1, b, r, d, n2, ob, or_, od, s: n1 == n2 and (ob, or_, od) == (b, r, d) and s == b - r - d)),
    # разница: столбы, покрашенные вчера и сегодня
    (rf"^{С} painted {Ч} posts yesterday and {Ч} posts today; {С} painted {Ч} more posts yesterday than today: {Ч} − {Ч} = {Ч}\.$",
     _рамка(lambda n1, x, y, n2, d, ox, oy, od: n1 == n2 and d == x - y > 0 and (ox, oy, od) == (x, y, d))),
    (rf"^{ИМЯ} вчера покрасила? {Ч} столб(?:а|ов)?, а сегодня {Ч} столб(?:а|ов)?; вчера на {Ч} столб(?:а|ов)? больше, чем сегодня: {Ч} − {Ч} = {Ч}\.$",
     _рамка(lambda n1, x, y, d, ox, oy, od: d == x - y > 0 and (ox, oy, od) == (x, y, d))),
    (rf"^{С} painted {Ч} posts yesterday and {Ч} posts today; {С} did not paint {Ч} more posts yesterday than today: {Ч} more\.$",
     _рамка(lambda n1, x, y, n2, ч, и: n1 == n2 and и == x - y > 0 and ч != и)),
    (rf"^if {С} painted {Ч} posts yesterday and {Ч} posts today, how many more posts did {С} paint yesterday than today\? {Ч} − {Ч} = {Ч}\.$",
     _рамка(lambda n1, x, y, n2, ox, oy, d: n1 == n2 and (ox, oy) == (x, y) and d == x - y > 0)),
    # скидка: билет ученика
    (rf"^a ticket costs {Ч} dollars and pupils get a discount of {Ч} dollars on each ticket; a pupil pays {Ч} dollars for a ticket: {Ч} − {Ч} = {Ч}\.$",
     _рамка(lambda c, s, p, oc, os, op: p == c - s and (oc, os, op) == (c, s, p))),
    (rf"^билет стоит {Ч} доллар(?:а|ов)?, и ученикам на каждый билет скидка {Ч} доллар(?:а|ов)?; ученик платит за билет {Ч} доллар(?:а|ов)?: {Ч} − {Ч} = {Ч}\.$",
     _рамка(lambda c, s, p, oc, os, op: p == c - s and (oc, os, op) == (c, s, p))),
    (rf"^a ticket costs {Ч} dollars and pupils get a discount of {Ч} dollars on each ticket; a pupil does not pay {Ч} dollars for a ticket: a pupil pays {Ч}\.$",
     _рамка(lambda c, s, ч, и: и == c - s and ч != и)),
    (rf"^if a ticket costs {Ч} dollars and pupils get a discount of {Ч} dollars on each ticket, how much does a pupil pay for a ticket\? {Ч} dollars: {Ч} − {Ч} = {Ч} dollars\.$",
     _рамка(lambda c, s, oc0, oc, os, p: (oc0, oc, os) == (c, c, s) and p == c - s)),
    # всего / left
    (rf"^{С} had {Ч} {С} and gave away {Ч}; {С} has {Ч} {С} left: {Ч} − {Ч} = {Ч}\.$",
     _рамка(lambda n1, x, в1, y, n2, s, в2, ox, oy, os: n1 == n2 and s == x - y and (ox, oy, os) == (x, y, s))),
    (rf"^у {ИМЯ} было {Ч} {С}, {ИМЯ} отдала? {Ч}; осталось {Ч} {С}: {Ч} − {Ч} = {Ч}\.$",
     _рамка(lambda n1, x, в1, n2, y, s, в2, ox, oy, os: _тот_же(n1, n2) and s == x - y and (ox, oy, os) == (x, y, s))),
    (rf"^{С} had {Ч} {С} and gave away {Ч}; {С} does not have {Ч} {С} left: {С} has {Ч}\.$",
     _рамка(lambda n1, x, в1, y, n2, ч, в2, n3, и: n1 == n2 == n3 and и == x - y and ч != и)),
    (rf"^if {С} had {Ч} {С} and gave away {Ч}, how many {С} are left\? {Ч} − {Ч} = {Ч}\.$",
     _рамка(lambda n1, x, в1, y, в2, ox, oy, s: (ox, oy) == (x, y) and s == x - y)),
    (rf"^{С} has {Ч} {С} in one box and {Ч} {С} in another; {С} has {Ч} {С} (in all|altogether): {Ч} \+ {Ч} = {Ч}\.$",
     _рамка(lambda n1, x, в1, y, в2, n2, s, в3, слово, ox, oy, os: n1 == n2 and s == x + y and (ox, oy, os) == (x, y, s))),
    (rf"^у {ИМЯ} {Ч} {С} в одной коробке и {Ч} {С} в другой; всего у {ИМЯ} {Ч} {С}: {Ч} \+ {Ч} = {Ч}\.$",
     _рамка(lambda n1, x, в1, y, в2, n2, s, в3, ox, oy, os: n1 == n2 and s == x + y and (ox, oy, os) == (x, y, s))),
    (rf"^{С} has {Ч} {С} in one box and {Ч} {С} in another; {С} does not have {Ч} {С} (in all|altogether): {С} has {Ч}\.$",
     _рамка(lambda n1, x, в1, y, в2, n2, ч, в3, слово, n3, и: n1 == n2 == n3 and и == x + y and ч != и)),
    (rf"^if {С} has {Ч} {С} in one box and {Ч} {С} in another, how many {С} does {С} have (in all|altogether)\? {Ч} \+ {Ч} = {Ч}\.$",
     _рамка(lambda n1, x, в1, y, в2, в3, n2, слово, ox, oy, s: n1 == n2 and (ox, oy) == (x, y) and s == x + y)),
    # группы: тарелки стопками
    (rf"^there are {Ч} plates and they are stacked in piles of {Ч}; there are {Ч} piles: {Ч} ÷ {Ч} = {Ч}\.$",
     _рамка(lambda T, n, g, oT, on, og: T == n * g and (oT, on, og) == (T, n, g))),
    (rf"^тарелок {Ч}, их сложили стопками по {Ч}; стопок {Ч}: {Ч} ÷ {Ч} = {Ч}\.$",
     _рамка(lambda T, n, g, oT, on, og: T == n * g and (oT, on, og) == (T, n, g))),
    (rf"^there are {Ч} plates and they are stacked in piles of {Ч}; there are not {Ч} piles: there are {Ч}\.$",
     _рамка(lambda T, n, ч, и: T == n * и and ч != и)),
    (rf"^if there are {Ч} plates and they are stacked in piles of {Ч}, how many piles are there\? {Ч} ÷ {Ч} = {Ч}\.$",
     _рамка(lambda T, n, oT, on, g: (oT, on) == (T, n) and T == n * g)),
    # ОСТАТОК ДЕЛЕНИЯ (08.09): группы не полны — и ФОРМУ ИМЕНИ ПРИ ОСТАТКЕ СУД ЧИТАЕТ САМ.
    # Половинчатый закон завёлся бы здесь в один шаг: довольно было написать «pupils» буквой
    # в образце, и «1 pupils» прошло бы мимо своего суда, оставшись на соседе (engram). Слово
    # взято дырой и сверено со счётом — по-английски прямо, по-русски через `_форма_ru`.
    #
    # РАССКАЗ И ВОПРОС — ОДИН ОБРАЗЕЦ, А НЕ ДВА (08.09). Прибор ширины считает род ОБРАЗЦОМ:
    # рассказ отдельным образцом есть род без вопросной поверхности, сколько бы вопросов ни
    # стояло рядом. Здесь обе половины сведены в одно чередование с общим хвостом-леджером —
    # тот же приём, каким живёт суд календаря, — и род выходит один, с вопросом.
    (rf"^(?:there are {Ч} eggs and they are packed in boxes of {Ч}; there are {Ч} full boxes and {Ч} "
     rf"(egg|eggs) left over"
     rf"|if there are {Ч} eggs and they are packed in boxes of {Ч}, how many eggs are left over)"
     rf"[:?] {Ч} × {Ч} = {Ч}, {Ч} − {Ч} = {Ч}\.$", _рамка(lambda *г: _остаток_en(*г))),
    (rf"^(?:яиц {Ч}, их разложили по коробкам по {Ч}; полных коробок {Ч}, и осталось {Ч} "
     rf"(яйц(?:о|а)|яиц)"
     rf"|если яиц {Ч} и их разложили по коробкам по {Ч}, сколько яиц останется)"
     rf"[:?] {Ч} × {Ч} = {Ч}, {Ч} − {Ч} = {Ч}\.$", _рамка(lambda *г: _остаток_ru(*г))),

)
# ТРЕТИЙ СЛОЙ (03.09): роды SVAMP по массе e9 и остаток g1. Слова родов —
# замкнутые множества суда (своё чтение таблиц генератора); закон — над числами.
СЛ = r"([а-яё]+)"
СЛОВА = r"([а-яё ]+?)"
ГЛ_A = r"(picked|washed|wrote|painted|sold|baked|counted|fed|collected|folded|carried|scored|found|drew)"
ГЛ_A0 = r"(pick|wash|write|paint|sell|bake|count|feed|collect|fold|carry|score|find|draw)"
ВЕЩЬ_A = r"(plums|plates|letters|posts|tickets|pies|ducks|rabbits|shells|napkins|boxes|points|mushrooms|pictures)"
КОГДА_EN = r"(in the morning|in the evening|on Saturday|on Sunday)"
КОГДА_RU = r"(утром|вечером|в субботу|в воскресенье)"
ОСНОВА = {"picked": "pick", "washed": "wash", "wrote": "write", "painted": "paint", "sold": "sell", "baked": "bake",
          "counted": "count", "fed": "feed", "collected": "collect", "folded": "fold", "carried": "carry",
          "scored": "score", "found": "find", "drew": "draw", "bought": "buy", "filled": "fill", "caught": "catch",
          "climbed": "climb", "won": "win", "sent": "send", "lost": "lose", "watched": "watch"}
ГЛ_B, ГЛ_B0 = r"(bought|wrote|painted|collected|washed|baked|sold|picked)", r"(buy|write|paint|collect|wash|bake|sell|pick)"
ВЕЩЬ_B = r"(kilograms of apples|kilograms of plums|letters|cards|tables|posts|shells|stones|cups|plates|pies|cakes|roses|tulips|pears|plums)"
# 22E два деятеля, одно дело: деятель — имя или «the» с одним-двумя словами («the red team»)
ДЕЯТЕЛЬ_E = r"((?:the )?[A-Za-z]+(?: [a-z]+)?)"
# ДВА СПИСКА ОДНОГО ЗАКОНА РАСХОДЯТСЯ МОЛЧА (07.09, вечер). Дом объявляет вещи в
# `tools/gen_genesis_gsmforms.py:БОЛЬШЕ_E`, суд — здесь, второй раз. Я поменял в доме
# «metres» на «meters» (одно письмо единицы в одном мире) — и суд ПЕРЕСТАЛ ЧИТАТЬ свой
# дом: ворота записи назвали две честные строки ложью, ибо их не прочёл никто, кто знает
# их закон. Вылечено добавлением слова СЮДА ЖЕ, и это лечение, а не закон.
#
#     СПИСОК, ПЕРЕПИСАННЫЙ В СУД ИЗ ДОМА, ЕСТЬ ДОЛГ, А НЕ УДОБСТВО: он верен ровно до
#     первой правки дома, и день этой правки ничем не отмечен.
#
# Долг назван и оставлен назван: свести списки в одно место — работа отдельная, ибо
# суд держит их полтора десятка, и всякий свод их через дом рискует кругом ввоза
# (дом зовёт ворота записи, ворота зовут палату, палата ввозит этот суд).
ГЛ_E, ГЛ_E0, ВЕЩЬ_E = r"(scored|filled|caught|carried|baked|sold)", r"(score|fill|catch|carry|bake|sell)", r"(points|buckets|mice|passengers|pies|tickets)"
ВЕЩЬ_C, ГДЕ = r"(apples|pears|ducks|swans)", r"(in the basket|on the lake)"
# 22П глаголы полос точками: деятель — имя, зверь или группа
ДЕЯТЕЛЬ_П = r"((?:the )?[A-Za-z]+)"
ГЛ_П = r"(climbed|baked|painted|picked|won|sent|lost|watched|sold|washed)"
ГЛ_П0 = r"(climb|bake|paint|pick|win|send|lose|watch|sell|wash)"
ВЕЩЬ_П = r"(steps|meters|pies|loaves|posts|boards|plums|pears|matches|races|parcels|postcards|buttons|keys|films|plays|cakes|cups|plates)"
НА, НА_RU = r"(on train tickets|on lunch|on paint|on brushes)", r"(на билеты|на обед|на краску|на кисти)"
ГЛ_O, ГЛ_O0, ВЕЩЬ_O = r"(picked|washed|sold|counted|fed)", r"(pick|wash|sell|count|feed)", r"(plums|cups|tickets|boats|rabbits)"
СРОК, СРОК_RU = r"(on Monday|on Tuesday|on Wednesday)", r"(в понедельник|во вторник|в среду)"
С_ВЕЩЬ = r"(pens|books|apples|coins|cards)"
КР, КР_RU = r"(half as many|twice as many|three times as many)", r"(вдвое меньше|вдвое больше|втрое больше)"
КР_К = {"half as many": (2, True), "twice as many": (2, False), "three times as many": (3, False),
        "вдвое меньше": (2, True), "вдвое больше": (2, False), "втрое больше": (3, False)}


def _срок(w, a, b, c):
    return {"on Monday": a, "on Tuesday": b, "on Wednesday": c, "в понедельник": a, "во вторник": b, "в среду": c}[w]


def _остаток(n, m, k, что, r, *осн):
    if что.startswith(("apples", "ябло")):
        return tuple(осн) == (n, k, r) and r == n - k >= 0
    return not осн and r == n


def _всего_насекомых(n, кр, t, on, on2, знак, k, ot):
    k_, делить = КР_К[кр]
    if k != k_ or знак != ("÷" if делить else "×") or (делить and n % k):
        return False
    return on == on2 == n and ot == t == n + (n // k if делить else n * k)


# 31 части: множитель словом или числом («three times» / «3 times»)
КРАТ_Ч = r"(twice|three times|four times|2 times|3 times|4 times|вдвое|втрое|вчетверо)"


def _k_кратности(кр):
    if isinstance(кр, int):
        return кр
    м = re.fullmatch(r"(\d+) times", str(кр))
    return int(м.group(1)) if м else None


def _части_лот(всего, кр, лот, ов, k1, ол, k, k1b):
    k0 = _k_кратности(кр)
    return (k0 is not None and k == k0 and k1 == k1b == k0 + 1 and ов == всего
            and ол == лот and лот * (k0 + 1) == всего)


def _части_дом(всего, кр, дом, ов, k1, ол, ол2, k, од):
    k0 = _k_кратности(кр)
    return (k0 is not None and k == k0 and k1 == k0 + 1 and ов == всего and ол2 == ол
            and ол * (k0 + 1) == всего and од == дом == ол * k0)


ОБРАЗЦЫ_3 = (
    # 22A одна вещь на двух случаях
    (rf"^{С} {ГЛ_A} {Ч} {ВЕЩЬ_A} {КОГДА_EN} and {Ч} {ВЕЩЬ_A} {КОГДА_EN}; {С} {ГЛ_A} {Ч} more {ВЕЩЬ_A} {КОГДА_EN} than {КОГДА_EN}: {Ч} − {Ч} = {Ч}\.$",
     _рамка(lambda n1, g1, x, t1, w1, y, t2, w2, n2, g2, d, t3, w3, w4, ox, oy, od: n1 == n2 and g1 == g2 and t1 == t2 == t3 and (w1, w2) == (w3, w4) and d == x - y > 0 and (ox, oy, od) == (x, y, d))),
    (rf"^{ИМЯ} {СЛ} {КОГДА_RU} {Ч} {СЛ}, а {КОГДА_RU} {Ч} {СЛ}; {КОГДА_RU} на {Ч} {СЛ} больше, чем {КОГДА_RU}: {Ч} − {Ч} = {Ч}\.$",
     _рамка(lambda n, g, w1, x, s1, w2, y, s2, w3, d, s3, w4, ox, oy, od: (w1, w2) == (w3, w4) and d == x - y > 0 and (ox, oy, od) == (x, y, d))),
    (rf"^{С} {ГЛ_A} {Ч} {ВЕЩЬ_A} {КОГДА_EN} and {Ч} {ВЕЩЬ_A} {КОГДА_EN}; {С} did not {ГЛ_A0} {Ч} more {ВЕЩЬ_A} {КОГДА_EN} than {КОГДА_EN}: {Ч} more\.$",
     _рамка(lambda n1, g1, x, t1, w1, y, t2, w2, n2, g0, ч, t3, w3, w4, и: n1 == n2 and ОСНОВА[g1] == g0 and t1 == t2 == t3 and (w1, w2) == (w3, w4) and и == x - y > 0 and ч != и)),
    (rf"^if {С} {ГЛ_A} {Ч} {ВЕЩЬ_A} {КОГДА_EN} and {Ч} {ВЕЩЬ_A} {КОГДА_EN}, how many more {ВЕЩЬ_A} did {С} {ГЛ_A0} {КОГДА_EN} than {КОГДА_EN}\? {Ч} − {Ч} = {Ч}\.$",
     _рамка(lambda n1, g1, x, t1, w1, y, t2, w2, t3, n2, g0, w3, w4, ox, oy, d: n1 == n2 and ОСНОВА[g1] == g0 and t1 == t2 == t3 and (w1, w2) == (w3, w4) and (ox, oy) == (x, y) and d == x - y > 0)),
    (rf"^if {С} {ГЛ_A} {Ч} {ВЕЩЬ_A} {КОГДА_EN} and {Ч} {ВЕЩЬ_A} {КОГДА_EN}, how many fewer {ВЕЩЬ_A} did {С} {ГЛ_A0} {КОГДА_EN} than {КОГДА_EN}\? {Ч} − {Ч} = {Ч}\.$",
     _рамка(lambda n1, g1, x, t1, w1, y, t2, w2, t3, n2, g0, w3, w4, ox, oy, d: n1 == n2 and ОСНОВА[g1] == g0 and t1 == t2 == t3 and (w1, w2) == (w4, w3) and (ox, oy) == (x, y) and d == x - y > 0)),
    # 22B две вещи одним делом
    (rf"^{С} {ГЛ_B} {Ч} {ВЕЩЬ_B} and {Ч} {ВЕЩЬ_B}; {С} {ГЛ_B} {Ч} more {ВЕЩЬ_B} than {ВЕЩЬ_B}: {Ч} − {Ч} = {Ч}\.$",
     _рамка(lambda n1, g1, x, t1, y, t2, n2, g2, d, t3, t4, ox, oy, od: n1 == n2 and g1 == g2 and (t1, t2) == (t3, t4) and d == x - y > 0 and (ox, oy, od) == (x, y, d))),
    (rf"^{ИМЯ} {СЛ} {Ч} {СЛОВА} и {Ч} {СЛОВА}; {СЛОВА} на {Ч} больше, чем {СЛОВА}: {Ч} − {Ч} = {Ч}\.$",
     _рамка(lambda n, g, x, s1, y, s2, s3, d, s4, ox, oy, od: d == x - y > 0 and (ox, oy, od) == (x, y, d))),
    (rf"^{С} {ГЛ_B} {Ч} {ВЕЩЬ_B} and {Ч} {ВЕЩЬ_B}; {С} did not {ГЛ_B0} {Ч} more {ВЕЩЬ_B} than {ВЕЩЬ_B}: {Ч} more\.$",
     _рамка(lambda n1, g1, x, t1, y, t2, n2, g0, ч, t3, t4, и: n1 == n2 and ОСНОВА[g1] == g0 and (t1, t2) == (t3, t4) and и == x - y > 0 and ч != и)),
    (rf"^if {С} {ГЛ_B} {Ч} {ВЕЩЬ_B} and {Ч} {ВЕЩЬ_B}, how many more {ВЕЩЬ_B} than {ВЕЩЬ_B} did {С} {ГЛ_B0}\? {Ч} − {Ч} = {Ч}\.$",
     _рамка(lambda n1, g1, x, t1, y, t2, t3, t4, n2, g0, ox, oy, d: n1 == n2 and ОСНОВА[g1] == g0 and (t1, t2) == (t3, t4) and (ox, oy) == (x, y) and d == x - y > 0)),
    (rf"^if {С} {ГЛ_B} {Ч} {ВЕЩЬ_B} and {Ч} {ВЕЩЬ_B}, how many fewer {ВЕЩЬ_B} than {ВЕЩЬ_B} did {С} {ГЛ_B0}\? {Ч} − {Ч} = {Ч}\.$",
     _рамка(lambda n1, g1, x, t1, y, t2, t3, t4, n2, g0, ox, oy, d: n1 == n2 and ОСНОВА[g1] == g0 and (t1, t2) == (t4, t3) and (ox, oy) == (x, y) and d == x - y > 0)),
    # 22C there were A and B где
    (rf"^there were {Ч} {ВЕЩЬ_C} and {Ч} {ВЕЩЬ_C} {ГДЕ}; there were {Ч} more {ВЕЩЬ_C} than {ВЕЩЬ_C}: {Ч} − {Ч} = {Ч}\.$",
     _рамка(lambda x, a, y, b, где, d, a2, b2, ox, oy, od: (a, b) == (a2, b2) and d == x - y > 0 and (ox, oy, od) == (x, y, d))),
    (rf"^в корзине было {Ч} {СЛ} и {Ч} {СЛ}; {СЛ} на {Ч} больше, чем {СЛ}: {Ч} − {Ч} = {Ч}\.$",
     _рамка(lambda x, a, y, b, a2, d, b2, ox, oy, od: d == x - y > 0 and (ox, oy, od) == (x, y, d))),
    (rf"^there were {Ч} {ВЕЩЬ_C} and {Ч} {ВЕЩЬ_C} {ГДЕ}; there were not {Ч} more {ВЕЩЬ_C} than {ВЕЩЬ_C}: {Ч} more\.$",
     _рамка(lambda x, a, y, b, где, ч, a2, b2, и: (a, b) == (a2, b2) and и == x - y > 0 and ч != и)),
    (rf"^if there were {Ч} {ВЕЩЬ_C} and {Ч} {ВЕЩЬ_C} {ГДЕ}, how many more {ВЕЩЬ_C} than {ВЕЩЬ_C} were there\? {Ч} − {Ч} = {Ч}\.$",
     _рамка(lambda x, a, y, b, где, a2, b2, ox, oy, d: (a, b) == (a2, b2) and (ox, oy) == (x, y) and d == x - y > 0)),
    (rf"^if there were {Ч} {ВЕЩЬ_C} and {Ч} {ВЕЩЬ_C} {ГДЕ}, how many fewer {ВЕЩЬ_C} than {ВЕЩЬ_C} were there\? {Ч} − {Ч} = {Ч}\.$",
     _рамка(lambda x, a, y, b, где, b2, a2, ox, oy, d: (a, b) == (a2, b2) and (ox, oy) == (x, y) and d == x - y > 0)),
    # 22D деньги
    (rf"^{С} spent {Ч} dollars {НА} and {Ч} dollars {НА}; {С} spent {Ч} dollars? more {НА} than {НА}: {Ч} − {Ч} = {Ч}\.$",
     _рамка(lambda n1, x, на1, y, на2, n2, d, на3, на4, ox, oy, od: n1 == n2 and (на1, на2) == (на3, на4) and d == x - y > 0 and (ox, oy, od) == (x, y, d))),
    (rf"^{ИМЯ} {СЛ} {Ч} {СЛ} {НА_RU} и {Ч} {СЛ} {НА_RU}; {НА_RU} на {Ч} {СЛ} больше, чем {НА_RU}: {Ч} − {Ч} = {Ч}\.$",
     _рамка(lambda n, g, x, s1, на1, y, s2, на2, на3, d, s3, на4, ox, oy, od: (на1, на2) == (на3, на4) and d == x - y > 0 and (ox, oy, od) == (x, y, d))),
    (rf"^{С} spent {Ч} dollars {НА} and {Ч} dollars {НА}; {С} did not spend {Ч} dollars more {НА} than {НА}: {Ч} more\.$",
     _рамка(lambda n1, x, на1, y, на2, n2, ч, на3, на4, и: n1 == n2 and (на1, на2) == (на3, на4) and и == x - y > 0 and ч != и)),
    (rf"^if {С} spent {Ч} dollars {НА} and {Ч} dollars {НА}, how much more money did {С} spend {НА} than {НА}\? {Ч} − {Ч} = {Ч} dollars?\.$",
     _рамка(lambda n1, x, на1, y, на2, n2, на3, на4, ox, oy, d: n1 == n2 and (на1, на2) == (на3, на4) and (ox, oy) == (x, y) and d == x - y > 0)),
    # 23 отбор среди отвлекающих
    (rf"^{С} {ГЛ_O} {Ч} {ВЕЩЬ_O} on Monday, {Ч} on Tuesday and {Ч} on Wednesday; {СРОК} {С} {ГЛ_O} {Ч} {ВЕЩЬ_O}\.$",
     _рамка(lambda n1, g1, a, t1, b, c, w, n2, g2, v, t2: n1 == n2 and g1 == g2 and t1 == t2 and len({a, b, c}) == 3 and v == _срок(w, a, b, c))),
    (rf"^{ИМЯ} {СЛ} в понедельник {Ч} {СЛ}, во вторник {Ч} и в среду {Ч}; {СРОК_RU} {ИМЯ} {СЛ} {Ч} {СЛ}\.$",
     _рамка(lambda n1, g1, a, s1, b, c, w, n2, g2, v, s2: n1 == n2 and g1 == g2 and len({a, b, c}) == 3 and v == _срок(w, a, b, c))),
    (rf"^if {С} {ГЛ_O} {Ч} {ВЕЩЬ_O} on Monday, {Ч} on Tuesday and {Ч} on Wednesday, how many {ВЕЩЬ_O} did {С} {ГЛ_O0} in all\? {Ч} \+ {Ч} \+ {Ч} = {Ч}\.$",
     _рамка(lambda n1, g1, a, t1, b, c, t2, n2, g0, oa, ob, oc, s: n1 == n2 and ОСНОВА[g1] == g0 and t1 == t2 and (oa, ob, oc) == (a, b, c) and s == a + b + c)),
    (rf"^{С} {ГЛ_O} {Ч} {ВЕЩЬ_O} on Monday, {Ч} on Tuesday and {Ч} on Wednesday; {С} did not {ГЛ_O0} {Ч} {ВЕЩЬ_O} {СРОК}: {С} {ГЛ_O} {Ч}\.$",
     _рамка(lambda n1, g1, a, t1, b, c, n2, g0, ч, t2, w, n3, g2, и: n1 == n2 == n3 and ОСНОВА[g1] == g0 and g1 == g2 and t1 == t2 and len({a, b, c}) == 3 and и == _срок(w, a, b, c) and ч != и)),
    (rf"^if {С} {ГЛ_O} {Ч} {ВЕЩЬ_O} on Monday, {Ч} on Tuesday and {Ч} on Wednesday, how many {ВЕЩЬ_O} did {С} {ГЛ_O0} {СРОК}\? {Ч} {СРОК}\.$",
     _рамка(lambda n1, g1, a, t1, b, c, t2, n2, g0, w, v, w2: n1 == n2 and ОСНОВА[g1] == g0 and t1 == t2 and w == w2 and len({a, b, c}) == 3 and v == _срок(w, a, b, c))),
    # 24 остаток при отвлекающем
    (rf"^the gardener picked {Ч} apples and {Ч} pears and sold {Ч} (apples|pears); the gardener still has {Ч} apples?: (?:{Ч} − {Ч} = {Ч}|the pears sold are not apples)\.$",
     _рамка(_остаток)),
    (rf"^{ИМЯ} {СЛ} {Ч} {СЛ} и {Ч} {СЛ} и {СЛ} {Ч} (ябло[а-я]*|груш[а-я]*); яблок осталось {Ч}: (?:{Ч} − {Ч} = {Ч}|проданы груши, не яблоки)\.$",
     _рамка(lambda имя, g, n, s1, m, s2, g2, k, что, r, *осн: _остаток(n, m, k, что, r, *осн))),
    (rf"^the gardener picked {Ч} apples and {Ч} pears and sold {Ч} (apples|pears); the gardener does not still have {Ч} apples: the gardener has {Ч}\.$",
     _рамка(lambda n, m, k, что, ч, и: и == (n - k if что == "apples" else n) and ч != и)),
    (rf"^if the gardener picked {Ч} apples and {Ч} pears and sold {Ч} apples, how many apples would the gardener still have\? {Ч} apples; the {Ч} pears do not count; {Ч} − {Ч} = {Ч}\.$",
     _рамка(lambda n, m, k, on, om, on2, ok, r: (on, om, on2, ok) == (n, m, n, k) and r == n - k >= 0)),
    (rf"^if the gardener picked {Ч} apples and {Ч} pears and sold {Ч} pears, how many apples would the gardener still have\? {Ч} apples; the pears sold are not apples\.$",
     _рамка(lambda n, m, k, on: on == n)),
    # 25 класс
    (rf"^there are {Ч} residents on the first floor and {Ч} on the second floor; the house has {Ч} residents: {Ч} \+ {Ч} = {Ч}\.$",
     _рамка(lambda g, b, s, og, ob, os: s == g + b and (og, ob, os) == (g, b, s))),
    (rf"^на первом этаже {Ч} {СЛ}, а на втором {Ч}; в доме {Ч} {СЛ}: {Ч} \+ {Ч} = {Ч}\.$",
     _рамка(lambda g, s1, b, s, s3, og, ob, os: s == g + b and (og, ob, os) == (g, b, s))),
    (rf"^there are {Ч} residents on the first floor and {Ч} on the second floor; the house does not have {Ч} residents: it has {Ч}\.$",
     _рамка(lambda g, b, ч, и: и == g + b and ч != и)),
    (rf"^if there are {Ч} residents on the first floor and {Ч} on the second floor, how many residents does the house have\? {Ч} \+ {Ч} = {Ч}\.$",
     _рамка(lambda g, b, og, ob, s: (og, ob) == (g, b) and s == g + b)),
    (rf"^the house has {Ч} residents and {Ч} of them live on the first floor; {Ч} residents live on the second floor: {Ч} − {Ч} = {Ч}\.$",
     _рамка(lambda s, g, b, os, og, ob: b == s - g > 0 and (os, og, ob) == (s, g, b))),
    (rf"^в доме {Ч} {СЛ}, из них {Ч} живут на первом этаже; на втором этаже {Ч} {СЛ}: {Ч} − {Ч} = {Ч}\.$",
     _рамка(lambda s, s1, g, b, s3, os, og, ob: b == s - g > 0 and (os, og, ob) == (s, g, b))),
    (rf"^the house has {Ч} residents and {Ч} of them live on the first floor; the number of residents on the second floor is not {Ч}: it is {Ч}\.$",
     _рамка(lambda s, g, ч, и: и == s - g > 0 and ч != и)),
    (rf"^if the house has {Ч} residents and {Ч} of them live on the first floor, how many residents live on the second floor\? {Ч} − {Ч} = {Ч}\.$",
     _рамка(lambda s, g, os, og, b: (os, og) == (s, g) and b == s - g > 0)),
    # 26 деньги
    (rf"^{С} bought {Ч} {С_ВЕЩЬ} at {Ч} dollars each; {С} spent {Ч} dollars: {Ч} × {Ч} = {Ч}\.$",
     _рамка(lambda n1, n, в, p, n2, t, on, op, ot: n1 == n2 and t == n * p and (on, op, ot) == (n, p, t))),
    (rf"^{ИМЯ} {СЛ} {Ч} {СЛ} по {Ч} {СЛ}; {ИМЯ} {СЛ} {Ч} {СЛ}: {Ч} × {Ч} = {Ч}\.$",
     _рамка(lambda n1, g1, n, в, p, s1, n2, g2, t, s2, on, op, ot: n1 == n2 and t == n * p and (on, op, ot) == (n, p, t))),
    (rf"^{С} bought {Ч} {С_ВЕЩЬ} at {Ч} dollars each; {С} did not spend {Ч} dollars: {С} spent {Ч}\.$",
     _рамка(lambda n1, n, в, p, n2, ч, n3, и: n1 == n2 == n3 and и == n * p and ч != и)),
    (rf"^if {С} bought {Ч} {С_ВЕЩЬ} at {Ч} dollars each, how much money did {С} spend\? {Ч} × {Ч} = {Ч} dollars\.$",
     _рамка(lambda n1, n, в, p, n2, on, op, t: n1 == n2 and (on, op) == (n, p) and t == n * p)),
    (rf"^{С} had {Ч} dollars and spent {Ч} dollars; {С} has {Ч} dollars left: {Ч} − {Ч} = {Ч}\.$",
     _рамка(lambda n1, a, b, n2, c, oa, ob, oc: n1 == n2 and c == a - b > 0 and (oa, ob, oc) == (a, b, c))),
    (rf"^у {ИМЯ} было {Ч} {СЛ}, {ИМЯ} {СЛ} {Ч} {СЛ}; осталось {Ч} {СЛ}: {Ч} − {Ч} = {Ч}\.$",
     _рамка(lambda n1, a, s1, n2, g, b, s2, c, s3, oa, ob, oc: _тот_же(n1, n2) and c == a - b > 0 and (oa, ob, oc) == (a, b, c))),
    (rf"^{С} had {Ч} dollars and spent {Ч} dollars; {С} does not have {Ч} dollars left: {С} has {Ч}\.$",
     _рамка(lambda n1, a, b, n2, ч, n3, и: n1 == n2 == n3 and и == a - b > 0 and ч != и)),
    (rf"^if {С} had {Ч} dollars and spent {Ч} dollars, how much money is left\? {Ч} − {Ч} = {Ч} dollars\.$",
     _рамка(lambda n1, a, b, oa, ob, c: (oa, ob) == (a, b) and c == a - b > 0)),
    # 27 сдача
    (rf"^a lamp costs {Ч} dollars? and {С} hands over {Ч} {Ч}-dollar bills; the change is {Ч} dollars: {Ч} × {Ч} − {Ч} = {Ч}\.$",
     _рамка(lambda p, n1, n, b, c, on, ob, op, oc: c == n * b - p > 0 and (on, ob, op, oc) == (n, b, p, c))),
    (rf"^лампа стоит {Ч} {СЛ}, {ИМЯ} даёт {Ч} {СЛ} по {Ч} {СЛ}; сдача {Ч} {СЛ}: {Ч} × {Ч} − {Ч} = {Ч}\.$",
     _рамка(lambda p, s0, n1, n, s1, b, s2, c, s4, on, ob, op, oc: c == n * b - p > 0 and (on, ob, op, oc) == (n, b, p, c))),
    (rf"^a lamp costs {Ч} dollars? and {С} hands over {Ч} {Ч}-dollar bills; the change is not {Ч} dollars: it is {Ч}\.$",
     _рамка(lambda p, n1, n, b, ч, и: и == n * b - p > 0 and ч != и)),
    (rf"^if a lamp costs {Ч} dollars? and {С} hands over {Ч} {Ч}-dollar bills, how much change does {С} get\? {Ч} × {Ч} − {Ч} = {Ч} dollars\.$",
     _рамка(lambda p, n1, n, b, n2, on, ob, op, c: n1 == n2 and (on, ob, op) == (n, b, p) and c == n * b - p > 0)),
    # 28 прибыль
    (rf"^{С} bought a bicycle for {Ч} dollars and sells it at {Ч}/{Ч} of that price; the profit is {Ч} dollars: {Ч} × {Ч} ÷ {Ч} − {Ч} = {Ч}\.$",
     _рамка(lambda n1, p, a, b, r, op, oa, ob, op2, or_: p % b == 0 and r == p * a // b - p > 0 and (op, oa, ob, op2, or_) == (p, a, b, p, r))),
    (rf"^{ИМЯ} {СЛ} велосипед за {Ч} {СЛ} и продаёт его за {Ч}/{Ч} этой цены; прибыль {Ч} {СЛ}: {Ч} × {Ч} ÷ {Ч} − {Ч} = {Ч}\.$",
     _рамка(lambda n1, g, p, s1, a, b, r, s2, op, oa, ob, op2, or_: p % b == 0 and r == p * a // b - p > 0 and (op, oa, ob, op2, or_) == (p, a, b, p, r))),
    (rf"^{С} bought a bicycle for {Ч} dollars and sells it at {Ч}/{Ч} of that price; the profit is not {Ч} dollars: it is {Ч}\.$",
     _рамка(lambda n1, p, a, b, ч, и: p % b == 0 and и == p * a // b - p > 0 and ч != и)),
    (rf"^if {С} bought a bicycle for {Ч} dollars and sells it at {Ч}/{Ч} of that price, what is the profit\? {Ч} × {Ч} ÷ {Ч} − {Ч} = {Ч} dollars\.$",
     _рамка(lambda n1, p, a, b, op, oa, ob, op2, r: p % b == 0 and (op, oa, ob, op2) == (p, a, b, p) and r == p * a // b - p > 0)),
    # 29 завышение
    (rf"^{С} said {Ч} guests came to the party, overstating the number by {Ч} percent; {Ч} guests really came: {Ч} × 100 ÷ \(100 \+ {Ч}\) = {Ч}\.$",
     _рамка(lambda n1, n, q, r, on, oq, or_: r * (100 + q) == n * 100 and (on, oq, or_) == (n, q, r))),
    (rf"^{ИМЯ} {СЛ}, что гостей на празднике было {Ч}, но {СЛ} число на {Ч} {СЛ}; на самом деле гостей было {Ч}: {Ч} × 100 ÷ \(100 \+ {Ч}\) = {Ч}\.$",
     _рамка(lambda n1, g, n, g2, q, s2, r, on, oq, or_: r * (100 + q) == n * 100 and (on, oq, or_) == (n, q, r))),
    (rf"^{С} said {Ч} guests came to the party, overstating the number by {Ч} percent; the real number is not {Ч}: it is {Ч}\.$",
     _рамка(lambda n1, n, q, ч, и: и * (100 + q) == n * 100 and ч != и)),
    (rf"^if {С} said {Ч} guests came to the party, overstating the number by {Ч} percent, how many guests really came\? {Ч} × 100 ÷ \(100 \+ {Ч}\) = {Ч}\.$",
     _рамка(lambda n1, n, q, on, oq, r: (on, oq) == (n, q) and r * (100 + q) == n * 100)),
    # 30 половина / кратно и всего
    (rf"^there were {Ч} apples and {КР} pears as apples in the basket; there were {Ч} apples and pears in all: {Ч} \+ {Ч} (÷|×) {Ч} = {Ч}\.$",
     _рамка(_всего_насекомых)),
    (rf"^в корзине было {Ч} {СЛ} и {КР_RU} груш; всего яблок и груш {Ч}: {Ч} \+ {Ч} (÷|×) {Ч} = {Ч}\.$",
     _рамка(lambda n, s, кр, t, on, on2, знак, k, ot: _всего_насекомых(n, кр, t, on, on2, знак, k, ot))),
    (rf"^there were {Ч} apples and {КР} pears as apples in the basket; there were not {Ч} apples and pears in all: there were {Ч}\.$",
     _рамка(lambda n, кр, ч, и: и == n + (n // КР_К[кр][0] if КР_К[кр][1] else n * КР_К[кр][0]) and (not КР_К[кр][1] or n % КР_К[кр][0] == 0) and ч != и)),
    (rf"^if there were {Ч} apples and {КР} pears as apples in the basket, how many apples and pears were there in all\? {Ч} \+ {Ч} (÷|×) {Ч} = {Ч}\.$",
     _рамка(lambda n, кр, on, on2, знак, k, t: _всего_насекомых(n, кр, t, on, on2, знак, k, t))),
    # 31 части: часть и её кратное дают целое
    (rf"^a boat and a trailer cost {Ч} dollars and the boat cost {КРАТ_Ч} as much as the trailer; the trailer cost {Ч} dollars: {Ч} ÷ {Ч} = {Ч}, {Ч} \+ 1 = {Ч}\.$",
     _рамка(lambda всего, кр, лот, ов, k1, ол, k, k1b: _части_лот(всего, кр, лот, ов, k1, ол, k, k1b))),
    (rf"^лодка и прицеп стоили {Ч} {СЛ}, а лодка стоила {КРАТ_Ч} дороже прицепа; прицеп стоил {Ч} {СЛ}: {Ч} ÷ {Ч} = {Ч}, {Ч} \+ 1 = {Ч}\.$",
     _рамка(lambda всего, с1, кр, лот, с2, ов, k1, ол, k, k1b: _части_лот(всего, кр, лот, ов, k1, ол, k, k1b))),
    (rf"^a boat and a trailer cost {Ч} dollars and the boat cost {КРАТ_Ч} as much as the trailer; the boat cost {Ч} dollars: {Ч} ÷ {Ч} = {Ч}, {Ч} × {Ч} = {Ч}\.$",
     _рамка(lambda всего, кр, дом, ов, k1, ол, ол2, k, од: _части_дом(всего, кр, дом, ов, k1, ол, ол2, k, од))),
    (rf"^if a boat and a trailer cost {Ч} dollars and the boat cost {КРАТ_Ч} as much as the trailer, how much did the trailer cost\? {Ч} ÷ {Ч} = {Ч}, {Ч} \+ 1 = {Ч} dollars\.$",
     _рамка(lambda всего, кр, ов, k1, ол, k, k1b: _части_лот(всего, кр, ол, ов, k1, ол, k, k1b))),
    (rf"^if a boat and a trailer cost {Ч} dollars and the boat cost {КРАТ_Ч} as much as the trailer, how much did the boat cost\? {Ч} ÷ {Ч} = {Ч}, {Ч} × {Ч} = {Ч} dollars\.$",
     _рамка(lambda всего, кр, ов, k1, ол, ол2, k, од: _части_дом(всего, кр, од, ов, k1, ол, ол2, k, од))),
    # 22E два деятеля, одно дело
    (rf"^{ДЕЯТЕЛЬ_E} {ГЛ_E} {Ч} {ВЕЩЬ_E} and {ДЕЯТЕЛЬ_E} {ГЛ_E} {Ч} {ВЕЩЬ_E}; {ДЕЯТЕЛЬ_E} {ГЛ_E} {Ч} more {ВЕЩЬ_E} than {ДЕЯТЕЛЬ_E}: {Ч} − {Ч} = {Ч}\.$",
     _рамка(lambda d1, g1, x, v1, d2, g2, y, v2, d3, g3, d, v3, d4, ox, oy, od: d1 != d2 and (d3, d4) == (d1, d2) and g1 == g2 == g3 and v1 == v2 == v3 and d == x - y > 0 and (ox, oy, od) == (x, y, d))),
    (rf"^{ДЕЯТЕЛЬ_E} {ГЛ_E} {Ч} {ВЕЩЬ_E} and {ДЕЯТЕЛЬ_E} {ГЛ_E} {Ч} {ВЕЩЬ_E}; {ДЕЯТЕЛЬ_E} did not {ГЛ_E0} {Ч} more {ВЕЩЬ_E} than {ДЕЯТЕЛЬ_E}: {Ч} more\.$",
     _рамка(lambda d1, g1, x, v1, d2, g2, y, v2, d3, g0, ч, v3, d4, и: d1 != d2 and (d3, d4) == (d1, d2) and g1 == g2 and ОСНОВА[g1] == g0 and v1 == v2 == v3 and и == x - y > 0 and ч != и)),
    (rf"^if {ДЕЯТЕЛЬ_E} {ГЛ_E} {Ч} {ВЕЩЬ_E} and {ДЕЯТЕЛЬ_E} {ГЛ_E} {Ч} {ВЕЩЬ_E}, how many more {ВЕЩЬ_E} did {ДЕЯТЕЛЬ_E} {ГЛ_E0} than {ДЕЯТЕЛЬ_E}\? {Ч} − {Ч} = {Ч}\.$",
     _рамка(lambda d1, g1, x, v1, d2, g2, y, v2, v3, d3, g0, d4, ox, oy, d: d1 != d2 and (d3, d4) == (d1, d2) and g1 == g2 and ОСНОВА[g1] == g0 and v1 == v2 == v3 and (ox, oy) == (x, y) and d == x - y > 0)),
    (rf"^if {ДЕЯТЕЛЬ_E} {ГЛ_E} {Ч} {ВЕЩЬ_E} and {ДЕЯТЕЛЬ_E} {ГЛ_E} {Ч} {ВЕЩЬ_E}, how many fewer {ВЕЩЬ_E} did {ДЕЯТЕЛЬ_E} {ГЛ_E0} than {ДЕЯТЕЛЬ_E}\? {Ч} − {Ч} = {Ч}\.$",
     _рамка(lambda d1, g1, x, v1, d2, g2, y, v2, v3, d3, g0, d4, ox, oy, d: d1 != d2 and (d3, d4) == (d2, d1) and g1 == g2 and ОСНОВА[g1] == g0 and v1 == v2 == v3 and (ox, oy) == (x, y) and d == x - y > 0)),
    # 22П глаголы полос точками (e9 04.09: рынок глаголов историй голосует только по утверждениям)
    (rf"^{ДЕЯТЕЛЬ_П} {ГЛ_П} {Ч} {ВЕЩЬ_П}\. {ДЕЯТЕЛЬ_П} {ГЛ_П} {Ч} {ВЕЩЬ_П}\. {ДЕЯТЕЛЬ_П} {ГЛ_П} {Ч} more {ВЕЩЬ_П} than {ДЕЯТЕЛЬ_П}: {Ч} − {Ч} = {Ч}\.$",
     _рамка(lambda d1, g1, x, v1, d2, g2, y, v2, d3, g3, d, v3, d4, ox, oy, od: d1 != d2 and (d3, d4) == (d1, d2) and g1 == g2 == g3 and v1 == v2 == v3 and d == x - y > 0 and (ox, oy, od) == (x, y, d))),
    (rf"^{ДЕЯТЕЛЬ_П} {ГЛ_П} {Ч} {ВЕЩЬ_П}\. {ДЕЯТЕЛЬ_П} {ГЛ_П} {Ч} {ВЕЩЬ_П}\. {ДЕЯТЕЛЬ_П} {ГЛ_П} {Ч} fewer {ВЕЩЬ_П} than {ДЕЯТЕЛЬ_П}: {Ч} − {Ч} = {Ч}\.$",
     _рамка(lambda d1, g1, x, v1, d2, g2, y, v2, d3, g3, d, v3, d4, ox, oy, od: d1 != d2 and (d3, d4) == (d2, d1) and g1 == g2 == g3 and v1 == v2 == v3 and d == x - y > 0 and (ox, oy, od) == (x, y, d))),
    (rf"^{ДЕЯТЕЛЬ_П} {ГЛ_П} {Ч} {ВЕЩЬ_П}\. {ДЕЯТЕЛЬ_П} {ГЛ_П} {Ч} {ВЕЩЬ_П}\. together they {ГЛ_П} {Ч} {ВЕЩЬ_П}: {Ч} \+ {Ч} = {Ч}\.$",
     _рамка(lambda d1, g1, x, v1, d2, g2, y, v2, g3, s, v3, ox, oy, os: d1 != d2 and g1 == g2 == g3 and v1 == v2 == v3 and s == x + y and (ox, oy, os) == (x, y, s))),
    (rf"^{ДЕЯТЕЛЬ_П} {ГЛ_П} {Ч} {ВЕЩЬ_П}\. {ДЕЯТЕЛЬ_П} {ГЛ_П} {Ч} {ВЕЩЬ_П}\. how many more {ВЕЩЬ_П} did {ДЕЯТЕЛЬ_П} {ГЛ_П0} than {ДЕЯТЕЛЬ_П}\? {Ч} − {Ч} = {Ч}\.$",
     _рамка(lambda d1, g1, x, v1, d2, g2, y, v2, v3, d3, g0, d4, ox, oy, d: d1 != d2 and (d3, d4) == (d1, d2) and g1 == g2 and ОСНОВА[g1] == g0 and v1 == v2 == v3 and (ox, oy) == (x, y) and d == x - y > 0)),
)
# СЕМЕЙСТВО ЕСТЬ РОД, А ФОРМА — ЕГО ПОВЕРХНОСТЬ (ширина вопроса 03.09):
# прибор считал каждый образец родом и звал повествование без вопроса
# долгом, хотя вопрос у семейства есть — в его QA-форме. Образцы одного
# семейства и одного языка сливаются в ОДИН якорный образец-перечисление,
# а вердикт даёт та форма, которая совпала целиком; вердикты не меняются.
_СЕМЕЙСТВА_ОСНОВА = (
    ("сумма", ОБРАЗЦЫ[0:4]),
    ("температура", ОБРАЗЦЫ[4:8]),
    ("процент", ОБРАЗЦЫ[8:12]),
    ("фунты", ОБРАЗЦЫ[12:16]),
    ("глубина", ОБРАЗЦЫ[16:20]),
    ("вероятность", ОБРАЗЦЫ[20:24]),
    ("четверти", ОБРАЗЦЫ[24:28]),
    ("дополнение", ОБРАЗЦЫ[28:40]),
    ("население", ОБРАЗЦЫ_2[0:4]),
    ("команда", ОБРАЗЦЫ_2[4:8]),
    ("кратно", ОБРАЗЦЫ_2[8:12]),
    ("проект", ОБРАЗЦЫ_2[12:16]),
    ("окружность", ОБРАЗЦЫ_2[16:20]),
    ("верёвки", ОБРАЗЦЫ_2[20:24]),
    ("трое", ОБРАЗЦЫ_2[24:28]),
    ("ставка", ОБРАЗЦЫ_2[28:32]),
    ("листки", ОБРАЗЦЫ_2[32:36]),
    ("разница", ОБРАЗЦЫ_2[36:40]),
    ("скидка", ОБРАЗЦЫ_2[40:44]),
    ("всего", ОБРАЗЦЫ_2[44:52]),
    ("группы", ОБРАЗЦЫ_2[52:56]),
    ("остаток_деления", ОБРАЗЦЫ_2[56:58]),
    ("больше_A", ОБРАЗЦЫ_3[0:5]),
    ("больше_B", ОБРАЗЦЫ_3[5:10]),
    ("больше_C", ОБРАЗЦЫ_3[10:15]),
    ("больше_D", ОБРАЗЦЫ_3[15:19]),
    ("отбор", ОБРАЗЦЫ_3[19:24]),
    ("остаток", ОБРАЗЦЫ_3[24:29]),
    ("класс", ОБРАЗЦЫ_3[29:37]),
    ("деньги", ОБРАЗЦЫ_3[37:45]),
    ("сдача", ОБРАЗЦЫ_3[45:49]),
    ("прибыль", ОБРАЗЦЫ_3[49:53]),
    ("завышение", ОБРАЗЦЫ_3[53:57]),
    ("половина", ОБРАЗЦЫ_3[57:61]),
    ("части", ОБРАЗЦЫ_3[61:66]),
    ("больше_E", ОБРАЗЦЫ_3[66:70]),
    ("полосы", ОБРАЗЦЫ_3[70:74]),
)
# RU QA-ФОРМЫ СЕМЕЙСТВ (М-146: вопросная поверхность на каждом языке рамки).
СРОК_RU2 = r"(в понедельник|во вторник|в среду)"
ЧЕТВЕРТИ_RU = r"(четверть|две четверти|три четверти)"


def _четверти_ru(часть, слово, o_ч, k, целое):
    k_ = {4: 1, "четверть": 1, "две четверти": 2, "три четверти": 3}.get(слово)
    return k_ is not None and o_ч == часть and k == k_ and целое * k == часть * 4


РУ_ВОПРОСЫ = {
    "сумма": [(rf"^если {ИМЯ} имеет {Ч} {С}, а {ИМЯ} имеет {Ч} {С}, сколько {С} у них всего\? {Ч} \+ {Ч} = {Ч}\.$",
               _рамка(lambda n1, x, в1, n2, y, в2, в3, ox, oy, s: (ox, oy) == (x, y) and s == x + y))],
    "температура": [(rf"^если температура была {Ч} {СЛ} и (упала|поднялась) на {Ч} {СЛ}, какова температура теперь\? {Ч} ([+−]) {Ч} = {Ч}\.$",
                     _рамка(lambda t0, s1, г, d, s2, ot0, зн, od, t1: (ot0, od) == (t0, d) and зн == ("−" if г == "упала" else "+") and t1 == t0 + (-d if г == "упала" else d)))],
    "процент": [(rf"^если в саду {Ч} {СЛ}, из них {Ч} {СЛ}, какова доля груш в процентах\? {Ч} {СЛ} и {Ч} {СЛ}: {Ч} ÷ {Ч} × 100 = {Ч}\.$",
                 _рамка(lambda всего, s1, часть, s2, o_в, s3, o_ч, s4, o_ч2, o_в2, p: (o_в, o_ч, o_ч2, o_в2) == (всего, часть, часть, всего) and часть * 100 == p * всего))],
    "фунты": [(rf"^если мешок яблок весит {Ч} {СЛ}, а в фунте 16 унций, каков вес в фунтах\? {Ч} ÷ 16 = {Ч}\.$",
               _рамка(lambda у, s, o_у, ф: o_у == у and ф * 16 == у))],
    "глубина": [(rf"^если яма шириной {Ч} {СЛ} и длиной {Ч} {СЛ} вмещает {Ч} кубическ(?:ий|их) метр(?:а|ов)? песка, какой толщины слой песка в яме\? {Ч} на {Ч} при {Ч}: {Ч} ÷ \({Ч} × {Ч}\) = {Ч}\.$",
                 _рамка(lambda w, s1, l, s2, v, ow, ol, ov, ov2, ow2, ol2, h: (ow, ol, ov, ov2, ow2, ol2) == (w, l, v, v, w, l) and h * w * l == v))],
    "вероятность": [(rf"^если в банке чёрных пуговиц {Ч}, а белых {Ч}, какова вероятность взять чёрную пуговицу, записанная дробью\? {Ч} \+ {Ч} = {Ч}: {Ч}/{Ч}\.$",
                     _рамка(lambda r, b, or_, ob, n, num, den: (or_, ob) == (r, b) and n == r + b and (num, den) == (r, n)))],
    "четверти": [(rf"^если {Ч} {СЛ} — это {ЧЕТВЕРТИ_RU} книги, сколько страниц в книге\? {Ч} ÷ {Ч} × 4 = {Ч}\.$",
                  _рамка(lambda часть, сл, слово, o_ч, k, целое: _четверти_ru(часть, слово, o_ч, k, целое)))],
    "дополнение": [(rf"^если на пруду изначально было {Ч} {СЛ}, а {Ч} улетел[аи], сколько уток осталось\? {Ч} − {Ч} = {Ч}\.$",
                    _рамка(lambda б, s, у, o_б, o_у, о: (o_б, o_у) == (б, у) and о == б - у)),
                   (rf"^если мест для марок в альбоме {Ч}, а вклеен[ао] {Ч} {СЛ}, сколько марок не хватает\? {Ч} − {Ч} = {Ч}\.$",
                    _рамка(lambda б, о, s2, o_б, o_о, у: (o_б, o_о) == (б, о) and у == б - о)),
                   (rf"^если на празднике было {Ч} {СЛ}, а {Ч} (?:ушёл|ушли) домой, сколько гостей на празднике теперь\? {Ч} − {Ч} = {Ч}\.$",
                    _рамка(lambda б, s, у, o_б, o_у, о: (o_б, o_у) == (б, у) and о == б - у))],
    "население": [(rf"^если в библиотеке {Ч} {СЛ}, и {ДОЛЯ} всех книг стоит в читальном зале, сколько книг стоит в читальном зале\? {Ч} ÷ {Ч} = {Ч}\.$",
                   _рамка(lambda N, s, d, oN, od, c: (oN, od) == (N, d) and N == d * c))],
    "команда": [(rf"^если на полке {Ч} {СЛ} и {Ч} {СЛ}, сколько всего предметов на полке\? {Ч} \+ {Ч} = {Ч}\.$",
                 _рамка(lambda m, s1, d, s2, om, od, s: (om, od) == (m, d) and s == m + d))],
    "кратно": [(rf"^если трактор стоил {Ч} {СЛ}, а амбар стоил {КРАТ} дороже трактора, сколько стоил амбар\? {Ч} {СЛ}: {Ч} × {Ч} = {Ч}\.$",
                _рамка(lambda c, s, k, oc0, s2, oc, ok, h: (oc0, oc, ok) == (c, c, k) and h == c * k))],
    "проект": [(rf"^если заказ начинался с {Ч} {СЛ}, его {УДВ} и потом убавили на {Ч}, сколько коробок в итоговом заказе\? {Ч} × {Ч} − {Ч} = {Ч}\.$",
                _рамка(lambda s0, s, k, m, os0, ok, om, f: (os0, ok, om) == (s0, k, m) and f == s0 * k - m))],
    "окружность": [(rf"^если дорога вокруг озера длиной {Ч} {СЛ}, а велосипедист едет {Ч} {СЛ} в час, сколько часов занимает поездка вокруг озера\? {Ч} ÷ {Ч} = {Ч}\.$",
                    _рамка(lambda L, s1, v, s2, oL, ov, t: (oL, ov) == (L, v) and L == v * t))],
    "верёвки": [(rf"^если общая высота столбов {Ч} {СЛ}, а столбов {Ч}, какова высота среднего столба\? {Ч} ÷ {Ч} = {Ч}\.$",
                 _рамка(lambda T, s, n, oT, on, a: (oT, on) == (T, n) and T == n * a))],
    "трое": [(rf"^если {ИМЯ} имеет {Ч} {СЛ}, {ИМЯ} имеет на {Ч} {СЛ} больше, чем {ИМЯ}, а {ИМЯ} имеет {КРАТ} больше ракушек, чем {ИМЯ}, сколько ракушек у них вместе\? {Ч} \+ \({Ч} \+ {Ч}\) \+ {Ч} × {Ч} = {Ч}\.$",
              _рамка(lambda x, a, s1, y, b, s2, x2, z, k, x3, oa, oa2, ob, ok, oa3, s: x == x2 == x3 and (oa, oa2, ob, ok, oa3) == (a, a, b, k, a) and s == a + (a + b) + k * a))],
    "ставка": [(rf"^если {ИМЯ} подписывает {Ч} {СЛ} в час и работает {Ч} {СЛ}, сколько открыток подписывает {ИМЯ}\? {Ч} × {Ч} = {Ч}\.$",
                _рамка(lambda n1, r, s1, t, s2, n2, or_, ot, s: n1 == n2 and (or_, ot) == (r, t) and s == r * t))],
    "листки": [(rf"^если у {ИМЯ} было {Ч} {СЛ}, {Ч} ушли в красную вазу и {Ч} в синюю, сколько конфет осталось\? {Ч} − {Ч} − {Ч} = {Ч}\.$",
                _рамка(lambda n, b, s, r, d, ob, or_, od, k: (ob, or_, od) == (b, r, d) and k == b - r - d))],
    "разница": [(rf"^если {ИМЯ} вчера покрасила? {Ч} {СЛ}, а сегодня {Ч} {СЛ}, на сколько столбов больше вчера, чем сегодня\? {Ч} − {Ч} = {Ч}\.$",
                 _рамка(lambda n, x, s1, y, s2, ox, oy, d: (ox, oy) == (x, y) and d == x - y > 0))],
    "скидка": [(rf"^если билет стоит {Ч} {СЛ}, и ученикам на каждый билет скидка {Ч} {СЛ}, сколько ученик платит за билет\? {Ч} − {Ч} = {Ч}\.$",
                _рамка(lambda c, s1, s, s2, oc, os, p: (oc, os) == (c, s) and p == c - s))],
    "всего": [(rf"^если у {ИМЯ} было {Ч} {СЛ}, а {ИМЯ} отдала? {Ч}, сколько {СЛ} осталось\? {Ч} {СЛ}: {Ч} − {Ч} = {Ч}\.$",
               _рамка(lambda n1, x, s1, n2, y, s2, ox0, s3, ox, oy, s: _тот_же(n1, n2) and (ox0, ox, oy) == (x, x, y) and s == x - y)),
              (rf"^если у {ИМЯ} {Ч} {СЛ} в одной коробке и {Ч} {СЛ} в другой, сколько всего {СЛ} у {ИМЯ}\? {Ч} \+ {Ч} = {Ч}\.$",
               _рамка(lambda n1, x, s1, y, s2, s3, n2, ox, oy, s: n1 == n2 and (ox, oy) == (x, y) and s == x + y))],
    "группы": [(rf"^если тарелок {Ч} и их сложили стопками по {Ч}, сколько стопок\? {Ч} ÷ {Ч} = {Ч}\.$",
                _рамка(lambda T, n, oT, on, g: (oT, on) == (T, n) and T == n * g))],
    "больше_A": [(rf"^если {ИМЯ} {СЛ} {КОГДА_RU} {Ч} {СЛ}, а {КОГДА_RU} {Ч} {СЛ}, на сколько {СЛ} больше {КОГДА_RU}, чем {КОГДА_RU}\? {Ч} {СЛ} {КОГДА_RU}: {Ч} − {Ч} = {Ч}\.$",
                  _рамка(lambda n, g, w1, x, s1, w2, y, s2, s3, w3, w4, ox0, s4, w5, ox, oy, d: (w1, w2, w1) == (w3, w4, w5) and (ox0, ox, oy) == (x, x, y) and d == x - y > 0))],
    "больше_B": [(rf"^если {ИМЯ} {СЛ} {Ч} {СЛОВА} и {Ч} {СЛОВА}, на сколько {СЛОВА} больше, чем {СЛОВА}\? {Ч} − {Ч} = {Ч}\.$",
                  _рамка(lambda n, g, x, s1, y, s2, s3, s4, ox, oy, d: (ox, oy) == (x, y) and d == x - y > 0))],
    "больше_C": [(rf"^если в корзине было {Ч} {СЛ} и {Ч} {СЛ}, на сколько {СЛ} больше, чем {СЛ}\? {Ч} − {Ч} = {Ч}\.$",
                  _рамка(lambda x, a, y, b, a2, b2, ox, oy, d: (ox, oy) == (x, y) and d == x - y > 0))],
    "больше_D": [(rf"^если {ИМЯ} {СЛ} {Ч} {СЛ} {НА_RU} и {Ч} {СЛ} {НА_RU}, на сколько долларов больше потрачено {НА_RU}, чем {НА_RU}\? {Ч} − {Ч} = {Ч}\.$",
                  _рамка(lambda n, g, x, s1, на1, y, s2, на2, на3, на4, ox, oy, d: (на1, на2) == (на3, на4) and (ox, oy) == (x, y) and d == x - y > 0))],
    "отбор": [(rf"^если {ИМЯ} {СЛ} в понедельник {Ч} {СЛ}, во вторник {Ч} и в среду {Ч}, сколько {СЛ} {ИМЯ} {СЛ} {СРОК_RU2}\? {Ч} {СРОК_RU2}\.$",
               _рамка(lambda n1, g1, a, s1, b, c, s2, n2, g2, w, v, w2: n1 == n2 and g1 == g2 and w == w2 and len({a, b, c}) == 3 and v == _срок(w, a, b, c)))],
    "остаток": [(rf"^если {ИМЯ} {СЛ} {Ч} {СЛ} и {Ч} {СЛ} и {СЛ} {Ч} (ябло[а-я]*), сколько яблок осталось\? {Ч} {СЛ}; {Ч} {СЛ} не в счёт; {Ч} − {Ч} = {Ч}\.$",
                 _рамка(lambda имя, g, n, s1, m, s2, g2, k, что, on, s3, om, s4, on2, ok, r: (on, om, on2, ok) == (n, m, n, k) and r == n - k >= 0)),
                (rf"^если {ИМЯ} {СЛ} {Ч} {СЛ} и {Ч} {СЛ} и {СЛ} {Ч} (груш[а-я]*), сколько яблок осталось\? {Ч} {СЛ}: проданы груши, не яблоки\.$",
                 _рамка(lambda имя, g, n, s1, m, s2, g2, k, что, on, s3: on == n))],
    "класс": [(rf"^если на первом этаже {Ч} {СЛ}, а на втором {Ч}, сколько жителей в доме\? {Ч} \+ {Ч} = {Ч}\.$",
               _рамка(lambda g, s1, b, og, ob, s: (og, ob) == (g, b) and s == g + b)),
              (rf"^если в доме {Ч} {СЛ}, из них {Ч} живут на первом этаже, сколько жителей на втором этаже\? {Ч} − {Ч} = {Ч}\.$",
               _рамка(lambda s, s1, g, os, og, b: (os, og) == (s, g) and b == s - g > 0))],
    "деньги": [(rf"^если {ИМЯ} {СЛ} {Ч} {СЛ} по {Ч} {СЛ}, сколько денег {ИМЯ} {СЛ}\? {Ч} × {Ч} = {Ч}\.$",
                _рамка(lambda n1, g, n, s1, p, s2, n2, g2, on, op, t: n1 == n2 and (on, op) == (n, p) and t == n * p)),
               (rf"^если у {ИМЯ} было {Ч} {СЛ}, а {ИМЯ} {СЛ} {Ч} {СЛ}, сколько денег осталось\? {Ч} − {Ч} = {Ч}\.$",
                _рамка(lambda n1, a, s1, n2, g, b, s2, oa, ob, c: _тот_же(n1, n2) and (oa, ob) == (a, b) and c == a - b > 0))],
    "сдача": [(rf"^если лампа стоит {Ч} {СЛ}, а {ИМЯ} даёт {Ч} {СЛ} по {Ч} {СЛ}, какова сдача\? {Ч} × {Ч} − {Ч} = {Ч}\.$",
               _рамка(lambda p, s0, n1, n, s1, b, s2, on, ob, op, c: (on, ob, op) == (n, b, p) and c == n * b - p > 0))],
    "прибыль": [(rf"^если {ИМЯ} {СЛ} велосипед за {Ч} {СЛ} и продаёт его за {Ч}/{Ч} этой цены, какова прибыль\? {Ч} × {Ч} ÷ {Ч} − {Ч} = {Ч}\.$",
                 _рамка(lambda n1, g, p, s, a, b, op, oa, ob, op2, r: p % b == 0 and (op, oa, ob, op2) == (p, a, b, p) and r == p * a // b - p > 0))],
    "завышение": [(rf"^если {ИМЯ} {СЛ}, что гостей на празднике было {Ч}, но {СЛ} число на {Ч} {СЛ}, сколько гостей было на самом деле\? {Ч} × 100 ÷ \(100 \+ {Ч}\) = {Ч}\.$",
                   _рамка(lambda n1, g, n, s1, q, s2, on, oq, r: (on, oq) == (n, q) and r * (100 + q) == n * 100))],
    "половина": [(rf"^если в корзине было {Ч} {СЛ} и {КР_RU} груш, сколько всего яблок и груш\? {Ч} \+ {Ч} (÷|×) {Ч} = {Ч}\.$",
                  _рамка(lambda n, s, кр, on, on2, знак, k, t: _всего_насекомых(n, кр, t, on, on2, знак, k, t)))],
    "части": [(rf"^если лодка и прицеп стоили {Ч} {СЛ}, а лодка стоила {КРАТ_Ч} дороже прицепа, сколько стоил прицеп\? {Ч} {СЛ}: {Ч} ÷ {Ч} = {Ч}, {Ч} \+ 1 = {Ч}\.$",
               _рамка(lambda всего, с1, кр, лот, с2, ов, k1, ол, k, k1b: _части_лот(всего, кр, лот, ов, k1, ол, k, k1b)))],
    # РУССКИЕ ПОЛОСЫ (15.09): два деятеля, одно дело, четыре поверхности — как у английской
    # стороны, и судятся тем же пересчётом. Сверх счёта суд читает СОГЛАСОВАНИЕ ГЛАГОЛА с
    # именем: «Вера написал» не пройдёт, хотя числа сойдутся.
    "полосы": [
        (rf"^{ИМЯ} {СЛ} {Ч} {СЛ}\. {ИМЯ} {СЛ} {Ч} {СЛ}\. {ИМЯ} {СЛ} на {Ч} {СЛ} больше, чем {ИМЯ}: {Ч} − {Ч} = {Ч}\.$",
         _рамка(lambda и1, г1, x, в1, и2, г2, y, в2, и3, г3, d, в3, и4, ox, oy, od:
                _полоса_ru(и1, г1, и2, г2, и3, г3, и4, x, y, d, ox, oy, od, ждём=(и1, и2)))),
        (rf"^{ИМЯ} {СЛ} {Ч} {СЛ}\. {ИМЯ} {СЛ} {Ч} {СЛ}\. {ИМЯ} {СЛ} на {Ч} {СЛ} меньше, чем {ИМЯ}: {Ч} − {Ч} = {Ч}\.$",
         _рамка(lambda и1, г1, x, в1, и2, г2, y, в2, и3, г3, d, в3, и4, ox, oy, od:
                _полоса_ru(и1, г1, и2, г2, и3, г3, и4, x, y, d, ox, oy, od, ждём=(и2, и1)))),
        (rf"^{ИМЯ} {СЛ} {Ч} {СЛ}\. {ИМЯ} {СЛ} {Ч} {СЛ}\. вместе они {СЛ} {Ч} {СЛ}: {Ч} \+ {Ч} = {Ч}\.$",
         _рамка(lambda и1, г1, x, в1, и2, г2, y, в2, мн, s, в3, ox, oy, os:
                и1 != и2 and _тот_же_глагол(г1, и1, г2, и2)
                and мн in _множественные(г1) and мн.endswith("и")
                and (ox, oy) == (x, y) and os == s == x + y)),
        (rf"^{ИМЯ} {СЛ} {Ч} {СЛ}\. {ИМЯ} {СЛ} {Ч} {СЛ}\. на сколько {СЛ} больше {СЛ} {ИМЯ}, чем {ИМЯ}\? {Ч} − {Ч} = {Ч}\.$",
         _рамка(lambda и1, г1, x, в1, и2, г2, y, в2, в3, г3, и3, и4, ox, oy, d:
                None if (и3 not in РОД_П or и4 not in РОД_П) else  # чужое лицо — чужая рамка
                (и1 != и2 and _тот_же_глагол(г1, и1, г2, и2) and (и3, и4) == (и1, и2)
                 and _род_глагола(г3, и1) and (ox, oy) == (x, y) and d == x - y > 0))),
    ],
}
def _основа_глагола(форма):
    """Общая часть мужского и женского прошедшего: «написал»/«написала» → «написал»."""
    return форма[:-1] if форма.endswith("а") else форма


# МНОЖЕСТВЕННОЕ ПРОШЕДШЕЕ ТАМ, ГДЕ ПРАВИЛО ЛОМАЕТСЯ: «нашёл → нашли» теряет «ё» вместе с
# беглой гласной, как и женское «нашла». Суд знает обе дороги и не требует лишь одной.
_МНОЖЕСТВЕННЫЕ = {"нашёл": "нашли", "нашла": "нашли", "испёк": "испекли", "испекла": "испекли"}


def _множественные(форма):
    """Все законные множественные прошедшие для этой основы."""
    объявлено = _МНОЖЕСТВЕННЫЕ.get(форма)
    основа = _основа_глагола(форма)
    return {объявлено} if объявлено else {основа + "и"}


def _род_глагола(форма, имя):
    """Согласован ли глагол с родом имени — по объявлению дома, а не по догадке.

    ГЛАГОЛ, НЕ СОГЛАСОВАННЫЙ С ИМЕНЕМ, ЕСТЬ ЛОЖЬ О РУССКОМ ПРИ ВЕРНОЙ АРИФМЕТИКЕ. Суд
    берёт род имени из того же пакета, откуда берёт его дом, — и потому не вторит дому, а
    спрашивает объявление вместе с ним.
    """
    женское = форма.endswith("а")
    return женское == (имя in ЖЕНСКИЕ_RU_СУДА)


def _тот_же_глагол(г1, и1, г2, и2):
    """Одно ли дело у двоих: основа общая, а род у каждого свой."""
    return (_основа_глагола(г1) == _основа_глагола(г2)
            and _род_глагола(г1, и1) and _род_глагола(г2, и2))


def _полоса_ru(и1, г1, и2, г2, и3, г3, и4, x, y, d, ox, oy, od, ждём):
    """Полоса по-русски: счёт пересчитан, глаголы согласованы, порядок деятелей — ДЕЛО.

    «БОЛЬШЕ» СТАВИТ ПЕРВЫМ ТОГО, У КОГО БОЛЬШЕ, «МЕНЬШЕ» — У КОГО МЕНЬШЕ, и порядок этот
    проверяется числом, а не читается как украшение: строка «Лена написала на 6 писем
    больше, чем Вера» при 9 у Веры и 3 у Лены есть ложь, хотя вычитание в ней верно.

    ЧУЖОЕ ЛИЦО — ЧУЖАЯ РАМКА, И СУД О НЕЙ МОЛЧИТ (16.09, прибор `scripts/court_reach.py`:
    68 лжей на мире местоимений). Полоса есть сравнение ДВУХ ДЕЯТЕЛЕЙ, и её `{ИМЯ}` суть
    класс букв — а класс букв ловит и глагол. Мир местоимений пишет ОДНОГО деятеля при
    ДВУХ действиях: «Аня сделала 23 монеты. Аня продала 17 монет. Аня сделала на 6 монет
    больше, чем продала: 23 − 17 = 6.» Счёт в ней верен, форма честна и НЕ ЕСТЬ полоса —
    а суд звал её ложью, ибо на месте второго лица стоял глагол «продала».

        ИМЯ, ОПОЗНАВАЕМОЕ КАК «ЛЮБОЕ СЛОВО ИЗ БУКВ», ОПОЗНАЁТ И ГЛАГОЛ. Лицо есть
        ОБЪЯВЛЕНИЕ ПАКЕТА, а не форма буквы, и судить по букве значит судить по виду.

    Тот же закон уже назван судом речи (`courts/speech_court.py`, М-131): необъявленное
    лицо есть чужая рамка, и суд молчит. Здесь он назван вторым домом — и это не повтор
    правила, а его ПРИЗНАНИЕ ОБЩИМ: две рамки с классом букв на месте лица ошиблись
    одинаково, порознь и по одной причине.
    """
    if и4 not in РОД_П or и3 not in РОД_П:
        return None                     # на месте лица не лицо — не моя рамка
    if и1 == и2 or not _тот_же_глагол(г1, и1, г2, и2):
        return False
    if (и3, и4) != ждём or not _род_глагола(г3, и3):
        return False
    return (ox, oy, od) == (x, y, d) and d == x - y > 0


# ИМЕНА ЖЕНСКОГО РОДА ОБЪЯВЛЕНЫ ПАКЕТОМ, А НЕ ЗДЕСЬ: суд читает то же объявление, что и дом.
ЖЕНСКИЕ_RU_СУДА = frozenset(
    n.capitalize() for n, ф in json.loads(
        (pathlib.Path(__file__).resolve().parents[1] / "tools" / "langpacks" / "ru.json")
        .read_text(encoding="utf-8"))["person_forms"].items() if ф["gender"] == "f")


# ОДНО ИМЯ — ОДНО ОПРЕДЕЛЕНИЕ (суд затенения): основа семейств + RU-вопросы.
СЕМЕЙСТВА_СУДА = tuple((имя, list(формы) + РУ_ВОПРОСЫ.get(имя, [])) for имя, формы in _СЕМЕЙСТВА_ОСНОВА)
assert set(РУ_ВОПРОСЫ) <= {имя for имя, _ in СЕМЕЙСТВА_СУДА}, set(РУ_ВОПРОСЫ) - {имя for имя, _ in СЕМЕЙСТВА_СУДА}

ПРАВИЛА = families.правила(СЕМЕЙСТВА_СУДА)


# ------------------------------------------------- СОГЛАСОВАНИЕ ПО-РУССКИ
# Суд семейств — хозяин русского согласования своих строк (суд родов 03.09:
# суд согласования пропускает число под предлогом и число после счётного
# слова по своим законам, и строка оставалась без хозяина рода). Форма при
# числе сверяется домом русского счёта; под предлогом родительного — косвенная.
СЧЁТОМ = re.compile(r"(?<![\d.,×÷+−=/-])\b(\d+) ([а-яё]+)\b")
ПРЕДЛОГИ_РОДИТЕЛЬНОГО = {"с", "из", "от", "до", "у", "около", "после", "для", "без", "кроме", "против"}


def _косвенная(вещь, n):
    return rugram.форма(вещь, 2) if n % 10 == 1 and n % 100 != 11 else rugram.форма(вещь, 5)


def _согласование_ru(с):
    """Все пары «число слово» с известным словом дома счёта согласованы."""
    for м in СЧЁТОМ.finditer(с):
        n, слово = int(м.group(1)), м.group(2)
        основа = rugram.ПО_ФОРМЕ.get(слово)
        if основа is None:
            continue
        перед = с[:м.start()].rstrip().split()
        предлог = перед[-1].lower() if перед else ""
        ожид = _косвенная(основа, n) if предлог in ПРЕДЛОГИ_РОДИТЕЛЬНОГО else rugram.форма(основа, n)
        if слово != ожид:
            return False
    return True


# ОТВЕТ ПРЕДЛОЖЕНИЕМ: «… = 8. so the answer is 8.» — хвост снимается, тело
# судится своей рамкой, и названный ответ обязан быть итогом уравнения.
ХВОСТ_ОТВЕТА = re.compile(r"^(.+ = (−?\d+)\.) (?:so the answer is|значит ответ:) (−?\d+)\.$")

# ЗВЕНО НЕ ЕСТЬ ОТВЕТ (23.09). Предложение ответа сверялось с итогом ПОСЛЕДНЕГО шага, и
# десять страниц мира говорили «250 ÷ 5 = 50, 4 + 1 = 5. значит ответ: 5» при ответе 50:
# последний шаг был звеном — делителем, выведенным после. Шаг, чей итог уже стоял числом
# в прежнем шаге, есть звено; дробь («4 + 1 = 5: 4/5») — ответ, но не число. Ни того, ни
# другого предложение ответа повторять не вправе. Чтение своё, не дома: суд не ввозит того,
# кого судит.
_ЧИСЛО_ШАГА = re.compile(r"−?\d+")


def _звено_или_дробь(хвост):
    if re.search(r"\d/\d", хвост):
        return True
    шаги = [ш for ш in хвост.split(", ") if " = " in ш]
    if len(шаги) < 2:
        return False
    итог = _ЧИСЛО_ШАГА.findall(шаги[-1].rsplit(" = ", 1)[1])
    прежние = {ч for ш in шаги[:-1] for ч in _ЧИСЛО_ШАГА.findall(ш.rsplit(" = ", 1)[0])}
    return bool(итог) and итог[0] in прежние


# ОТРИЦАНИЕ НЕСЁТ ВЫКЛАДКУ (23.09, требование ядра: уравнение ответа на каждой странице):
# «…: it is 16, because 11 + 5 = 16.» Тело судится своей рамкой отрицания, выкладка — счётом:
# она верна точно, её итог есть названный телом ответ, и всякое её число стоит в теле ЦИФРОЙ
# либо СЛОВОМ, названным словарями этого же суда: доля («a fifth» — 5), кратность («twice» —
# 2), четверти («three quarters» — 3 и 4), процент — сотня. Число, не названное ни так, ни
# этак, есть число со стороны, и выкладка с ним не пересчитывает условие.
ХВОСТ_ПОТОМУ = re.compile(r"^(.+), because ([−\d][\d ()+−×÷]*?) = (−?\d+)\.$")


def _названные_словом(тело):
    """Числа, какие тело называет словом, — по словарям суда, а не списком рядом."""
    низ = тело.lower()
    вон = {str(v) for слово, v in {**СЛОВА_ДОЛЕЙ, **СЛОВА_КРАТНОСТИ}.items()
           if isinstance(v, int) and re.search(rf"\b{re.escape(слово)}\b", низ)}
    вон |= {str(v) for слово, v in СЛОВА_ЧЕТВЕРТЕЙ.items() if re.search(rf"\b{re.escape(слово)}\b", низ)}
    if "quarter" in низ or "четверт" in низ:
        вон.add("4")
    if "percent" in низ or "%" in низ or "процент" in низ:
        вон.add("100")
    return вон


def _счёт(выраж):
    """Точное значение выкладки: + − × ÷, скобки, унарный минус; None — не выкладка."""
    from fractions import Fraction
    лексемы = re.findall(r"\d+|[+−×÷()]", выраж)
    if "".join(лексемы) != re.sub(r"\s+", "", выраж):
        return None
    поз = 0

    def сумма():
        nonlocal поз
        v = произведение()
        while поз < len(лексемы) and лексемы[поз] in "+−":
            зн = лексемы[поз]
            поз += 1
            w = произведение()
            v = v + w if зн == "+" else v - w
        return v

    def произведение():
        nonlocal поз
        v = множитель()
        while поз < len(лексемы) and лексемы[поз] in "×÷":
            зн = лексемы[поз]
            поз += 1
            w = множитель()
            v = v * w if зн == "×" else v / w
        return v

    def множитель():
        nonlocal поз
        л = лексемы[поз]
        поз += 1
        if л == "−":
            return -множитель()
        if л == "(":
            v = сумма()
            if лексемы[поз] != ")":
                raise ValueError("скобка")
            поз += 1
            return v
        return Fraction(int(л))

    try:
        v = сумма()
    except (IndexError, ValueError, ZeroDivisionError):
        return None
    return v if поз == len(лексемы) else None


def _потому_верно(тело, выраж, итог):
    значение = _счёт(выраж)
    if значение is None or значение != int(итог.replace("−", "-")):
        return False
    числа_тела = re.findall(r"−?\d+", тело)
    if not числа_тела or числа_тела[-1] != итог:
        return False
    в_теле = {ч.lstrip("−") for ч in числа_тела} | _названные_словом(тело)
    return all(ч in в_теле for ч in re.findall(r"\d+", выраж))


def _судить(строка):
    """(судимо, истинно) для одной строки."""
    с = строка.strip()
    м = ХВОСТ_ОТВЕТА.match(с)
    if м and "?" in м.group(1):
        судимо, истинно = судить(м.group(1))
        if судимо:
            хвост = м.group(1).split("? ")[-1]
            return True, истинно and м.group(2) == м.group(3) and not _звено_или_дробь(хвост)
    м = ХВОСТ_ПОТОМУ.match(с)
    if м:
        тело = м.group(1) + "."
        судимо, истинно = судить(тело)
        if судимо:
            return True, истинно and _потому_верно(тело, м.group(2), м.group(3))
    for образец, проверить in ПРАВИЛА:
        м = образец.match(с)
        if м:
            try:
                ист = проверить(м)
            except (ValueError, KeyError):
                return True, False
            # ОТКАЗ РАМКИ ОТ СТРОКИ НЕ ОСТАНАВЛИВАЕТ ПЕРЕБОРА: рамка сказала «не моя»,
            # и строку может признать СЛЕДУЮЩАЯ. Прервись перебор здесь — отказ одной
            # рамки стал бы немотой всего суда.
            if ист is None:
                continue
            ист = bool(ист)
            # РУССКАЯ СТРОКА ВЕРНА ЛИШЬ ПРИ ВЕРНЫХ СЧЁТНЫХ ФОРМАХ.
            if ист and re.search(r"[а-яё]", с):
                ист = _согласование_ru(с)
            return True, ист
    return False, False


def main():
    import collections
    итог = collections.Counter()
    for путь in [pathlib.Path(п) for п in sys.argv[1:]] or [КОРЕНЬ / "datasets" / "genesis_gsmforms.txt"]:
        for с in путь.read_text(encoding="utf-8").splitlines():
            if not с.strip():
                continue
            судимо, истинно = судить(с)
            итог["несудимо" if not судимо else ("истина" if истинно else "ЛОЖЬ")] += 1
            if судимо and not истинно:
                print("  ЛОЖЬ:", с[:120])
            elif not судимо:
                итог.setdefault("_прим", []) if False else None
    ложь = итог["ЛОЖЬ"]
    print(f"ШКОЛЬНЫЕ ФОРМЫ {'PASS' if not ложь else 'FAIL'}: {ложь} ложных, "
          f"{итог['истина']} истинных, {итог['несудимо']} несудимых")
    return 0 if not ложь else 1


# МИР ЗАМКНУТ, И ЭТО ПРОВЕРЕНО ДЕЛОМ, А НЕ ОБЪЯВЛЕНО МНЕНИЕМ (06.09, перепись
# закрываемости): палата, суженная до одного этого суда, судила КАЖДУЮ строку
# мира («gsmforms» — 2511 строк) — судимы ВСЕ до одной. Значит показы суда суть весь мир, и
# молчание его о строке этого мира есть не воздержание, а форма, которой мир
# не писал. Обёртка не может сработать ни на одной сегодняшней строке — это
# доказательство, а не выборка; ловится лишь то, чего в файле НЕТ.
ЗАМКНУТЫЕ_МИРЫ = frozenset({"gsmforms"})
судить = closedworld.замкнуть(_судить, ЗАМКНУТЫЕ_МИРЫ)


if __name__ == "__main__":
    sys.exit(main())
