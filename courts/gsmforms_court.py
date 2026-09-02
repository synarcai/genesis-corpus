#!/usr/bin/env python3
"""[ШКОЛЬНЫЕ ФОРМЫ g1] — счёт основания пересчитывается, полярность судится итогом.

Мир gsmforms (tools/gen_genesis_gsmforms.py) показывает семейства вопросов
GSM8K, немые по прибору FORM-MUTE (e9): сумма по носителям, температура
ниже нуля, процент от доли, унции в фунты, глубина воды, вероятность
долей, доля от целого назад, дополнение. Суд не сверяет с записанным:
он считает из данных строки и сравнивает с итогом, с основанием после
двоеточия и с полярностью («is not N: it is M»); вопрос судится своим
ответом в той же строке.
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

Ч = r"(−?\d+)"
С = r"([a-zа-яё]+)"
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
    a, x, вx, b, y, вy, вещь, s, ox, oy, os = м.groups()
    x, y, s = _n(x), _n(y), _n(s)
    return a != b and x + y == s and (ox, oy, os) == (str(x), str(y), str(s))


def _сумма_не(м):
    a, x, вx, b, y, вy, вещь, чуж, ист = м.groups()
    x, y = _n(x), _n(y)
    return a != b and _n(ист) == x + y and _n(чуж) != x + y


def _сумма_ru(м):
    a, x, вx, b, y, вy, s, вs, ox, oy, os = м.groups()
    x, y, s = _n(x), _n(y), _n(s)
    return (a != b and x + y == s and (ox, oy, os) == (str(x), str(y), str(s))
            and _форма_ru(вx, x) and _форма_ru(вy, y) and _форма_ru(вs, s))


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
    всего, часть, p, oч, oв, op = (_n(x) for x in м.groups())
    return 0 < часть < всего and часть * 100 == p * всего and (oч, oв, op) == (часть, всего, p)


def _процент_не(м):
    всего, часть, чуж, ист = (_n(x) for x in м.groups())
    return часть * 100 == ист * всего and чуж != ист


# 4. фунты
def _фунты(м):
    унц, ф, oу, oф = (_n(x) for x in м.groups()[:4])
    return унц == 16 * ф and (oу, oф) == (унц, ф)


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
    r, b, num, den, or_, on = (_n(x) for x in м.groups())
    return num == r and den == r + b and (or_, on) == (r, r + b)


def _вероятность_не(м):
    r, b, чn, чd, иn, иd = (_n(x) for x in м.groups())
    return (иn, иd) == (r, r + b) and (чn, чd) != (r, r + b)


# 7. четверти
СЛОВА_ЧЕТВЕРТЕЙ = {"one quarter": 1, "two quarters": 2, "three quarters": 3,
                   "четверть": 1, "две четверти": 2, "три четверти": 3}


def _четверти(м):
    часть, слово, целое, oч, ok, o4 = м.groups()
    часть, целое, k = _n(часть), _n(целое), СЛОВА_ЧЕТВЕРТЕЙ[слово]
    return часть * 4 == целое * k and (_n(oч), _n(ok)) == (часть, k) and o4 == "4"


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
    a, x, _вx, b, y, _вy, _вещь, ox, oy, s = м.groups()
    return a != b and (_n(ox), _n(oy)) == (_n(x), _n(y)) and _n(x) + _n(y) == _n(s)


def _температура_qa(м):
    t0, глагол, d, o0, знак, od, t1 = м.groups()
    t0, d, t1 = _n(t0), _n(d), _n(t1)
    падение = глагол == "fell"
    return (_n(o0), _n(od)) == (t0, d) and знак == ("−" if падение else "+") and t1 == (t0 - d if падение else t0 + d)


def _процент_qa(м):
    всего, часть, oв, oч, oч2, oв2, p = (_n(x) for x in м.groups())
    return (oв, oч, oч2, oв2) == (всего, часть, часть, всего) and 0 < часть < всего and часть * 100 == p * всего


def _фунты_qa(м):
    унц, oу, ф = (_n(x) for x in м.groups())
    return oу == унц and унц == 16 * ф


def _глубина_qa(м):
    w, l, v, ow, ol, ov, ov2, ow2, ol2, h = (_n(x) for x in м.groups())
    return (ow, ol, ov, ov2, ow2, ol2) == (w, l, v, v, w, l) and v == w * l * h


def _вероятность_qa(м):
    r, b, or_, ob, n, num, den = (_n(x) for x in м.groups())
    return (or_, ob) == (r, b) and n == r + b and (num, den) == (r, n)


def _четверти_qa(м):
    часть, слово, oч, ok, o4, целое = м.groups()
    часть, целое, k = _n(часть), _n(целое), СЛОВА_ЧЕТВЕРТЕЙ[слово]
    return (_n(oч), _n(ok)) == (часть, k) and o4 == "4" and часть * 4 == целое * k


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
            return bool(закон(*г))
        except (TypeError, ZeroDivisionError, ValueError):
            return False
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
    (rf"^the class has {Ч} pupils and {Ч} of them are girls; the percentage of girls is {Ч} %: {Ч} ÷ {Ч} × 100 = {Ч}\.$", _процент),
    (rf"^the class has {Ч} pupils and {Ч} of them are girls\. what percentage of the class are girls\? {Ч} pupils and {Ч} girls: {Ч} ÷ {Ч} × 100 = {Ч} %\.$", _процент_qa),
    (rf"^в классе {Ч} учени(?:к|ка|ков), из них {Ч} — девоч(?:ка|ки|ек); доля девочек — {Ч} %: {Ч} ÷ {Ч} × 100 = {Ч}\.$", _процент),
    (rf"^the class has {Ч} pupils and {Ч} of them are girls; the percentage of girls is not {Ч} %: it is {Ч} %\.$", _процент_не),
    (rf"^the parcel weighs {Ч} ounces and a pound is 16 ounces; the weight in pounds is {Ч}: {Ч} ÷ 16 = {Ч}\.$", _фунты),
    (rf"^the parcel weighs {Ч} ounces and a pound is 16 ounces\. what is the weight in pounds\? {Ч} ounces: {Ч} ÷ 16 = {Ч}\.$", _рамка(lambda у, oу0, oу, ф: (oу0, oу) == (у, у) and у == 16 * ф)),
    (rf"^посылка весит {Ч} унци[йия], а в фунте 16 унций; вес в фунтах — {Ч} фунт(?:а|ов)?: {Ч} ÷ 16 = {Ч}\.$", _фунты),
    (rf"^the parcel weighs {Ч} ounces and a pound is 16 ounces; the weight in pounds is not {Ч}: it is {Ч}\.$", _фунты_не),
    (rf"^the tank is {Ч} feet wide and {Ч} feet long and holds {Ч} cubic feet of water; the tank's water depth is {Ч} f(?:ee|oo)t: {Ч} ÷ \({Ч} × {Ч}\) = {Ч}\.$", _глубина),
    (rf"^the tank is {Ч} feet wide and {Ч} feet long and holds {Ч} cubic feet of water\. what is the tank's water depth\? {Ч} by {Ч} holding {Ч}: {Ч} ÷ \({Ч} × {Ч}\) = {Ч} f(?:ee|oo)t\.$", _глубина_qa),
    (rf"^бак шириной {Ч} фут(?:а|ов)? и длиной {Ч} фут(?:а|ов)? вмещает {Ч} кубических футов воды; глубина воды в баке — {Ч} фут(?:а|ов)?: {Ч} ÷ \({Ч} × {Ч}\) = {Ч}\.$", _глубина),
    (rf"^the tank is {Ч} feet wide and {Ч} feet long and holds {Ч} cubic feet of water; the tank's water depth is not {Ч} feet: it is {Ч} f(?:ee|oo)t\.$", _глубина_не),
    (rf"^a bag holds {Ч} red marbles? and {Ч} blue marbles?; the probability of drawing a red marble, expressed as a fraction, is {Ч}/{Ч}: {Ч} red out of {Ч}\.$", _вероятность),
    (rf"^a bag holds {Ч} red marbles? and {Ч} blue marbles?\. what is the probability of drawing a red marble, expressed as a fraction\? {Ч} red and {Ч} blue make {Ч}: {Ч}/{Ч}\.$", _вероятность_qa),
    (rf"^в мешке {Ч} шар(?:а|ов)? красных и {Ч} шар(?:а|ов)? синих; вероятность вынуть красный шар, выраженная дробью, — {Ч}/{Ч}: {Ч} красных из {Ч}\.$", _вероятность),
    (rf"^a bag holds {Ч} red marbles? and {Ч} blue marbles?; the probability of drawing a red marble, expressed as a fraction, is not {Ч}/{Ч}: it is {Ч}/{Ч}\.$", _вероятность_не),
    (rf"^if {Ч} is (one quarter|two quarters|three quarters) of the class, the class has {Ч} pupils: {Ч} ÷ {Ч} × (4) = \d+\.$", _четверти),
    (rf"^if {Ч} is (one quarter|two quarters|three quarters) of the class, how many pupils does the class have\? {Ч} ÷ {Ч} × (4) = {Ч}\.$", _четверти_qa),
    (rf"^если {Ч} — это (четверть|две четверти|три четверти) класса, в классе {Ч} учени(?:к|ка|ков): {Ч} ÷ {Ч} × (4) = \d+\.$", _четверти),
    (rf"^if {Ч} is (one quarter|two quarters|three quarters) of the class, the class does not have {Ч} pupils: it has {Ч}\.$", _четверти_не),
    (rf"^there were originally {Ч} cars in the lot and {Ч} drove away; {Ч} cars? remain: {Ч} − {Ч} = {Ч}\.$", _разность),
    (rf"^if there were originally {Ч} cars in the lot and {Ч} drove away, how many cars remain\? {Ч} − {Ч} = {Ч}\.$", _разность_qa),
    (rf"^на стоянке изначально было {Ч} машин[аы]?, {Ч} уехали; осталось {Ч} машин[аы]?: {Ч} − {Ч} = {Ч}\.$", _разность),
    (rf"^there were originally {Ч} cars in the lot and {Ч} drove away; {Ч} cars do not remain: {Ч} remain\.$", _разность_не),
    (rf"^the set has {Ч} pieces and {Ч} are in the box; {Ч} pieces? (?:are|is) missing: {Ч} − {Ч} = {Ч}\.$", _разность),
    (rf"^the set has {Ч} pieces and {Ч} are in the box\. how many pieces are missing\? {Ч} − {Ч} = {Ч}\.$", _разность_qa),
    (rf"^в наборе {Ч} детал(?:ь|и|ей), в коробке {Ч} детал(?:ь|и|ей); не хватает {Ч} детал(?:ь|и|ей): {Ч} − {Ч} = {Ч}\.$", _разность),
    (rf"^the set has {Ч} pieces and {Ч} are in the box; {Ч} pieces are not missing: {Ч} (?:are|is) missing\.$", _разность_не),
    (rf"^there were {Ч} people on the bus and {Ч} got off; {Ч} people are on the bus now: {Ч} − {Ч} = {Ч}\.$", _разность),
    (rf"^if there were {Ч} people on the bus and {Ч} got off, how many people are on the bus now\? {Ч} − {Ч} = {Ч}\.$", _разность_qa),
    (rf"^в автобусе было {Ч} человек[а]?, {Ч} вышли; теперь в автобусе {Ч} человек[а]?: {Ч} − {Ч} = {Ч}\.$", _разность),
    (rf"^there were {Ч} people on the bus and {Ч} got off; the number of people on the bus now is not {Ч}: it is {Ч}\.$", _разность_не),
)
ОБРАЗЦЫ_2 = (
    # 9 население: всего, доля, часть, всего, доля, часть
    (rf"^the town has {Ч} people and {ДОЛЯ} of the whole population lives in the centre; {Ч} people live in the centre: {Ч} ÷ {Ч} = {Ч}\.$",
     _рамка(lambda N, d, c, oN, od, oc: N == d * c and (oN, od, oc) == (N, d, c))),
    (rf"^в городе {Ч} человек[а]?, и {ДОЛЯ} всего населения живёт в центре; в центре живёт {Ч} человек[а]?: {Ч} ÷ {Ч} = {Ч}\.$",
     _рамка(lambda N, d, c, oN, od, oc: N == d * c and (oN, od, oc) == (N, d, c))),
    (rf"^the town has {Ч} people and {ДОЛЯ} of the whole population lives in the centre; the number living in the centre is not {Ч}: it is {Ч}\.$",
     _рамка(lambda N, d, ч, и: N == d * и and ч != и)),
    (rf"^if the town has {Ч} people and {ДОЛЯ} of the whole population lives in the centre, how many people live in the centre\? {Ч} people: {Ч} ÷ {Ч} = {Ч}\.$",
     _рамка(lambda N, d, oN0, oN, od, c: (oN0, oN, od) == (N, N, d) and N == d * c)),
    # 10 команда
    (rf"^the number of boys on the team is {Ч} and the number of girls is {Ч}; the team has {Ч} players: {Ч} \+ {Ч} = {Ч}\.$",
     _рамка(lambda m, d, s, om, od, os: m + d == s and (om, od, os) == (m, d, s))),
    (rf"^в команде {Ч} мальчик(?:а|ов)? и {Ч} девоч(?:ка|ки|ек); всего в команде {Ч} человек[а]?: {Ч} \+ {Ч} = {Ч}\.$",
     _рамка(lambda m, d, s, om, od, os: m + d == s and (om, od, os) == (m, d, s))),
    (rf"^the number of boys on the team is {Ч} and the number of girls is {Ч}; the team does not have {Ч} players: it has {Ч}\.$",
     _рамка(lambda m, d, ч, и: m + d == и and ч != и)),
    (rf"^if the number of boys on the team is {Ч} and the number of girls is {Ч}, how many players does the team have\? {Ч} \+ {Ч} = {Ч}\.$",
     _рамка(lambda m, d, om, od, s: (om, od) == (m, d) and m + d == s)),
    # 11 кратно
    (rf"^the car cost {Ч} dollars and the house cost {КРАТ} as much as the car; the house cost {Ч} dollars: {Ч} × {Ч} = {Ч}\.$",
     _рамка(lambda c, k, h, oc, ok, oh: h == k * c and (oc, ok, oh) == (c, k, h))),
    (rf"^машина стоила {Ч} доллар(?:а|ов)?, а дом стоил {КРАТ} дороже машины; дом стоил {Ч} доллар(?:а|ов)?: {Ч} × {Ч} = {Ч}\.$",
     _рамка(lambda c, k, h, oc, ok, oh: h == k * c and (oc, ok, oh) == (c, k, h))),
    (rf"^the car cost {Ч} dollars and the house cost {КРАТ} as much as the car; the house did not cost {Ч} dollars: it cost {Ч}\.$",
     _рамка(lambda c, k, ч, и: и == k * c and ч != и)),
    (rf"^if the car cost {Ч} dollars and the house cost {КРАТ} as much as the car, how much did the house cost\? {Ч} × {Ч} = {Ч} dollars\.$",
     _рамка(lambda c, k, oc, ok, h: (oc, ok) == (c, k) and h == k * c)),
    # 12 проект
    (rf"^the design started with {Ч} panels, was {УДВ} and then reduced by {Ч}; the final design has {Ч} panels: {Ч} × {Ч} − {Ч} = {Ч}\.$",
     _рамка(lambda s0, k, m, f, os0, ok, om, of: f == s0 * k - m and (os0, ok, om, of) == (s0, k, m, f))),
    (rf"^проект начался с {Ч} панел(?:ь|и|ей), его {УДВ} и потом убавили на {Ч}; в итоговом проекте {Ч} панел(?:ь|и|ей): {Ч} × {Ч} − {Ч} = {Ч}\.$",
     _рамка(lambda s0, k, m, f, os0, ok, om, of: f == s0 * k - m and (os0, ok, om, of) == (s0, k, m, f))),
    (rf"^the design started with {Ч} panels, was {УДВ} and then reduced by {Ч}; the final design does not have {Ч} panels: it has {Ч}\.$",
     _рамка(lambda s0, k, m, ч, и: и == s0 * k - m and ч != и)),
    (rf"^if the design started with {Ч} panels, was {УДВ} and then reduced by {Ч}, how many panels does the final design have\? {Ч} × {Ч} − {Ч} = {Ч}\.$",
     _рамка(lambda s0, k, m, os0, ok, om, f: (os0, ok, om) == (s0, k, m) and f == s0 * k - m)),
    # 13 окружность
    (rf"^the circumference of the earth is taken as {Ч} miles and the plane flies {Ч} miles per hour; the flight around the earth takes {Ч} hours: {Ч} ÷ {Ч} = {Ч}\.$",
     _рамка(lambda L, v, t, oL, ov, ot: L == v * t and (oL, ov, ot) == (L, v, t))),
    (rf"^длину окружности земли берут за {Ч} мил[иья], самолёт летит {Ч} мил[иья] в час; полёт вокруг земли занимает {Ч} час(?:а|ов)?: {Ч} ÷ {Ч} = {Ч}\.$",
     _рамка(lambda L, v, t, oL, ov, ot: L == v * t and (oL, ov, ot) == (L, v, t))),
    (rf"^the circumference of the earth is taken as {Ч} miles and the plane flies {Ч} miles per hour; the flight around the earth does not take {Ч} hours: it takes {Ч}\.$",
     _рамка(lambda L, v, ч, и: L == v * и and ч != и)),
    (rf"^if the circumference of the earth is {Ч} miles and the plane flies {Ч} miles per hour, how many hours does the flight around the earth take\? {Ч} ÷ {Ч} = {Ч}\.$",
     _рамка(lambda L, v, oL, ov, t: (oL, ov) == (L, v) and L == v * t)),
    # 14 верёвки
    (rf"^the {Ч} ropes had a total length of {Ч} meters; the average rope is {Ч} meters long: {Ч} ÷ {Ч} = {Ч}\.$",
     _рамка(lambda n, T, a, oT, on, oa: T == n * a and (oT, on, oa) == (T, n, a))),
    (rf"^{Ч} верёв(?:ка|ки|ок) имели общую длину {Ч} метр(?:а|ов)?; средняя верёвка длиной {Ч} метр(?:а|ов)?: {Ч} ÷ {Ч} = {Ч}\.$",
     _рамка(lambda n, T, a, oT, on, oa: T == n * a and (oT, on, oa) == (T, n, a))),
    (rf"^the {Ч} ropes had a total length of {Ч} meters; the average rope is not {Ч} meters long: it is {Ч} meters\.$",
     _рамка(lambda n, T, ч, и: T == n * и and ч != и)),
    (rf"^if the total length of the ropes is {Ч} meters and there are {Ч} ropes, how long is the average rope\? {Ч} ÷ {Ч} = {Ч} meters\.$",
     _рамка(lambda T, n, oT, on, a: (oT, on) == (T, n) and T == n * a)),
    # 15 трое
    (rf"^{С} has {Ч} books, {С} has {Ч} more books than {С}, and {С} has {КРАТ} as many books as {С}; together {С}, {С} and {С} have {Ч} books: {Ч} \+ \({Ч} \+ {Ч}\) \+ {Ч} × {Ч} = {Ч}\.$",
     _рамка(lambda x, a, y, b, x2, z, k, x3, x4, y2, z2, s, oa, oa2, ob, ok, oa3, os: x == x2 == x3 == x4 and y == y2 and z == z2 and (oa, oa2, ob, ok, oa3) == (a, a, b, k, a) and s == os == a + (a + b) + k * a)),
    (rf"^{ИМЯ} имеет {Ч} книг[иа]?, {ИМЯ} имеет на {Ч} книг[иа]? больше, чем {ИМЯ}, а {ИМЯ} имеет {КРАТ} больше книг, чем {ИМЯ}; вместе у них {Ч} книг[иа]?: {Ч} \+ \({Ч} \+ {Ч}\) \+ {Ч} × {Ч} = {Ч}\.$",
     _рамка(lambda x, a, y, b, x2, z, k, x3, s, oa, oa2, ob, ok, oa3, os: x == x2 == x3 and (oa, oa2, ob, ok, oa3) == (a, a, b, k, a) and s == os == a + (a + b) + k * a)),
    (rf"^{С} has {Ч} books, {С} has {Ч} more books than {С}, and {С} has {КРАТ} as many books as {С}; together they do not have {Ч} books: they have {Ч}\.$",
     _рамка(lambda x, a, y, b, x2, z, k, x3, ч, и: x == x2 == x3 and и == a + (a + b) + k * a and ч != и)),
    (rf"^if {С} has {Ч} books, {С} has {Ч} more books than {С}, and {С} has {КРАТ} as many books as {С}, how many books do they have together\? {Ч} \+ \({Ч} \+ {Ч}\) \+ {Ч} × {Ч} = {Ч}\.$",
     _рамка(lambda x, a, y, b, x2, z, k, x3, oa, oa2, ob, ok, oa3, s: x == x2 == x3 and (oa, oa2, ob, ok, oa3) == (a, a, b, k, a) and s == a + (a + b) + k * a)),
    # 16 ставка
    (rf"^{С} makes {Ч} candles an hour and works {Ч} hours; {С} makes {Ч} candles: {Ч} × {Ч} = {Ч}\.$",
     _рамка(lambda n1, r, t, n2, s, or_, ot, os: n1 == n2 and s == r * t and (or_, ot, os) == (r, t, s))),
    (rf"^{ИМЯ} делает {Ч} свеч(?:а|и|ей) в час и работает {Ч} час(?:а|ов)?; {ИМЯ} делает {Ч} свеч(?:а|и|ей): {Ч} × {Ч} = {Ч}\.$",
     _рамка(lambda n1, r, t, n2, s, or_, ot, os: n1 == n2 and s == r * t and (or_, ot, os) == (r, t, s))),
    (rf"^{С} makes {Ч} candles an hour and works {Ч} hours; {С} does not make {Ч} candles: {С} makes {Ч}\.$",
     _рамка(lambda n1, r, t, n2, ч, n3, и: n1 == n2 == n3 and и == r * t and ч != и)),
    (rf"^if {С} makes {Ч} candles an hour and works {Ч} hours, how many candles does {С} make\? {Ч} × {Ч} = {Ч}\.$",
     _рамка(lambda n1, r, t, n2, or_, ot, s: n1 == n2 and (or_, ot) == (r, t) and s == r * t)),
    # 17 листки
    (rf"^{С} had {Ч} post-it notes, used {Ч} on the fridge and {Ч} on the door; {С} has {Ч} post-it notes left: {Ч} − {Ч} − {Ч} = {Ч}\.$",
     _рамка(lambda n1, b, r, d, n2, s, ob, or_, od, os: n1 == n2 and s == b - r - d and (ob, or_, od, os) == (b, r, d, s))),
    (rf"^у {ИМЯ} было {Ч} лист(?:ок|ка|ков), {Ч} ушли на холодильник и {Ч} на дверь; осталось {Ч} лист(?:ок|ка|ков): {Ч} − {Ч} − {Ч} = {Ч}\.$",
     _рамка(lambda n1, b, r, d, s, ob, or_, od, os: s == b - r - d and (ob, or_, od, os) == (b, r, d, s))),
    (rf"^{С} had {Ч} post-it notes, used {Ч} on the fridge and {Ч} on the door; {С} does not have {Ч} post-it notes left: {С} has {Ч}\.$",
     _рамка(lambda n1, b, r, d, n2, ч, n3, и: n1 == n2 == n3 and и == b - r - d and ч != и)),
    (rf"^if {С} had {Ч} post-it notes, used {Ч} on the fridge and {Ч} on the door, how many post-it notes does {С} have left\? {Ч} − {Ч} − {Ч} = {Ч}\.$",
     _рамка(lambda n1, b, r, d, n2, ob, or_, od, s: n1 == n2 and (ob, or_, od) == (b, r, d) and s == b - r - d)),
    # SVAMP разница
    (rf"^{С} planted {Ч} trees in the morning and {Ч} trees in the afternoon; {С} planted {Ч} more trees in the morning than in the afternoon: {Ч} − {Ч} = {Ч}\.$",
     _рамка(lambda n1, x, y, n2, d, ox, oy, od: n1 == n2 and d == x - y > 0 and (ox, oy, od) == (x, y, d))),
    (rf"^{ИМЯ} утром посадила? {Ч} дерев(?:о|а|ьев), а днём {Ч} дерев(?:о|а|ьев); утром на {Ч} дерев(?:о|а|ьев) больше, чем днём: {Ч} − {Ч} = {Ч}\.$",
     _рамка(lambda n1, x, y, d, ox, oy, od: d == x - y > 0 and (ox, oy, od) == (x, y, d))),
    (rf"^{С} planted {Ч} trees in the morning and {Ч} trees in the afternoon; {С} did not plant {Ч} more trees in the morning than in the afternoon: {Ч} more\.$",
     _рамка(lambda n1, x, y, n2, ч, и: n1 == n2 and и == x - y > 0 and ч != и)),
    (rf"^if {С} planted {Ч} trees in the morning and {Ч} trees in the afternoon, how many more trees did {С} plant in the morning than in the afternoon\? {Ч} − {Ч} = {Ч}\.$",
     _рамка(lambda n1, x, y, n2, ox, oy, d: n1 == n2 and (ox, oy) == (x, y) and d == x - y > 0)),
    # SVAMP скидка
    (rf"^each pack costs {Ч} dollars and there is a discount of {Ч} dollars on each pack; you have to pay {Ч} dollars for each pack: {Ч} − {Ч} = {Ч}\.$",
     _рамка(lambda c, s, p, oc, os, op: p == c - s and (oc, os, op) == (c, s, p))),
    (rf"^каждая пачка стоит {Ч} доллар(?:а|ов)?, и на каждую пачку скидка {Ч} доллар(?:а|ов)?; за каждую пачку надо заплатить {Ч} доллар(?:а|ов)?: {Ч} − {Ч} = {Ч}\.$",
     _рамка(lambda c, s, p, oc, os, op: p == c - s and (oc, os, op) == (c, s, p))),
    (rf"^each pack costs {Ч} dollars and there is a discount of {Ч} dollars on each pack; you do not have to pay {Ч} dollars for each pack: you pay {Ч}\.$",
     _рамка(lambda c, s, ч, и: и == c - s and ч != и)),
    (rf"^if each pack costs {Ч} dollars and there is a discount of {Ч} dollars on each pack, how much do you have to pay for each pack\? {Ч} dollars: {Ч} − {Ч} = {Ч} dollars\.$",
     _рамка(lambda c, s, oc0, oc, os, p: (oc0, oc, os) == (c, c, s) and p == c - s)),
    # SVAMP всего / left
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
    # SVAMP группы
    (rf"^there are {Ч} pupils and they stand in groups of {Ч}; there are {Ч} groups: {Ч} ÷ {Ч} = {Ч}\.$",
     _рамка(lambda T, n, g, oT, on, og: T == n * g and (oT, on, og) == (T, n, g))),
    (rf"^{Ч} учени(?:к|ка|ков) стоят группами по {Ч}; групп {Ч}: {Ч} ÷ {Ч} = {Ч}\.$",
     _рамка(lambda T, n, g, oT, on, og: T == n * g and (oT, on, og) == (T, n, g))),
    (rf"^there are {Ч} pupils and they stand in groups of {Ч}; there are not {Ч} groups: there are {Ч}\.$",
     _рамка(lambda T, n, ч, и: T == n * и and ч != и)),
    (rf"^if there are {Ч} pupils and they stand in groups of {Ч}, how many groups are there\? {Ч} ÷ {Ч} = {Ч}\.$",
     _рамка(lambda T, n, oT, on, g: (oT, on) == (T, n) and T == n * g)),
)
# ТРЕТИЙ СЛОЙ (03.09): роды SVAMP по массе e9 и остаток g1. Слова родов —
# замкнутые множества суда (своё чтение таблиц генератора); закон — над числами.
СЛ = r"([а-яё]+)"
СЛОВА = r"([а-яё ]+?)"
ГЛ_A, ГЛ_A0, ВЕЩЬ_A = r"(received|ate|played with)", r"(receive|eat|play with)", r"(emails|cookies|kids)"
КОГДА_EN = r"(in the morning|in the afternoon|on monday|on tuesday)"
КОГДА_RU = r"(утром|днём|в понедельник|во вторник)"
ОСНОВА = {"received": "receive", "ate": "eat", "played with": "play with", "used": "use", "made": "make",
          "read": "read", "bought": "buy", "sold": "sell", "cut": "cut", "found": "find"}
ГЛ_B, ГЛ_B0 = r"(used|made|read|bought)", r"(use|make|read|buy)"
ВЕЩЬ_B = r"(cups of flour|cups of sugar|cakes|pastries|pages of math|pages of reading|bottles of regular soda|bottles of diet soda)"
ВЕЩЬ_C, ГДЕ = r"(storks|birds|red flowers|white flowers)", r"(on the fence|in the garden)"
НА, НА_RU = r"(on the shirt|on the hat|on books|on pens)", r"(на рубашку|на шляпу|на книги|на ручки)"
ГЛ_O, ГЛ_O0, ВЕЩЬ_O = r"(received|sold|cut|found|played with)", r"(receive|sell|cut|find|play with)", r"(emails|books|roses|bottle caps|kids)"
СРОК, СРОК_RU = r"(in the morning|in the afternoon|in the evening)", r"(утром|днём|вечером)"
С_ВЕЩЬ = r"(pens|books|apples|coins|cards)"
КР, КР_RU = r"(half as many|twice as many|three times as many)", r"(вдвое меньше|вдвое больше|втрое больше)"
КР_К = {"half as many": (2, True), "twice as many": (2, False), "three times as many": (3, False),
        "вдвое меньше": (2, True), "вдвое больше": (2, False), "втрое больше": (3, False)}


def _срок(w, a, b, c):
    return {"in the morning": a, "in the afternoon": b, "in the evening": c, "утром": a, "днём": b, "вечером": c}[w]


def _остаток(n, m, k, что, r, *осн):
    if что.startswith(("cakes", "торт")):
        return tuple(осн) == (n, k, r) and r == n - k >= 0
    return not осн and r == n


def _всего_насекомых(n, кр, t, on, on2, знак, k, ot):
    k_, делить = КР_К[кр]
    if k != k_ or знак != ("÷" if делить else "×") or (делить and n % k):
        return False
    return on == on2 == n and ot == t == n + (n // k if делить else n * k)


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
    (rf"^на заборе было {Ч} {СЛ} и {Ч} {СЛ}; {СЛ} на {Ч} больше, чем {СЛ}: {Ч} − {Ч} = {Ч}\.$",
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
    (rf"^{С} {ГЛ_O} {Ч} {ВЕЩЬ_O} in the morning, {Ч} in the afternoon and {Ч} in the evening; {СРОК} {С} {ГЛ_O} {Ч} {ВЕЩЬ_O}\.$",
     _рамка(lambda n1, g1, a, t1, b, c, w, n2, g2, v, t2: n1 == n2 and g1 == g2 and t1 == t2 and len({a, b, c}) == 3 and v == _срок(w, a, b, c))),
    (rf"^{ИМЯ} {СЛ} утром {Ч} {СЛ}, днём {Ч} и вечером {Ч}; {СРОК_RU} {ИМЯ} {СЛ} {Ч} {СЛ}\.$",
     _рамка(lambda n1, g1, a, s1, b, c, w, n2, g2, v, s2: n1 == n2 and g1 == g2 and len({a, b, c}) == 3 and v == _срок(w, a, b, c))),
    (rf"^if {С} {ГЛ_O} {Ч} {ВЕЩЬ_O} in the morning, {Ч} in the afternoon and {Ч} in the evening, how many {ВЕЩЬ_O} did {С} {ГЛ_O0} in all\? {Ч} \+ {Ч} \+ {Ч} = {Ч}\.$",
     _рамка(lambda n1, g1, a, t1, b, c, t2, n2, g0, oa, ob, oc, s: n1 == n2 and ОСНОВА[g1] == g0 and t1 == t2 and (oa, ob, oc) == (a, b, c) and s == a + b + c)),
    (rf"^{С} {ГЛ_O} {Ч} {ВЕЩЬ_O} in the morning, {Ч} in the afternoon and {Ч} in the evening; {С} did not {ГЛ_O0} {Ч} {ВЕЩЬ_O} {СРОК}: {С} {ГЛ_O} {Ч}\.$",
     _рамка(lambda n1, g1, a, t1, b, c, n2, g0, ч, t2, w, n3, g2, и: n1 == n2 == n3 and ОСНОВА[g1] == g0 and g1 == g2 and t1 == t2 and len({a, b, c}) == 3 and и == _срок(w, a, b, c) and ч != и)),
    (rf"^if {С} {ГЛ_O} {Ч} {ВЕЩЬ_O} in the morning, {Ч} in the afternoon and {Ч} in the evening, how many {ВЕЩЬ_O} did {С} {ГЛ_O0} {СРОК}\? {Ч} {СРОК}\.$",
     _рамка(lambda n1, g1, a, t1, b, c, t2, n2, g0, w, v, w2: n1 == n2 and ОСНОВА[g1] == g0 and t1 == t2 and w == w2 and len({a, b, c}) == 3 and v == _срок(w, a, b, c))),
    # 24 остаток при отвлекающем
    (rf"^the baker made {Ч} cakes and {Ч} pastries and sold {Ч} (cakes|pastries); the baker still has {Ч} cakes: (?:{Ч} − {Ч} = {Ч}|the pastries sold are not cakes)\.$",
     _рамка(_остаток)),
    (rf"^пекарь {СЛ} {Ч} {СЛ} и {Ч} {СЛ} и {СЛ} {Ч} (торт[а-я]*|булоч[а-я]*); тортов осталось {Ч}: (?:{Ч} − {Ч} = {Ч}|проданы булочки, не торты)\.$",
     _рамка(lambda g, n, s1, m, s2, g2, k, что, r, *осн: _остаток(n, m, k, что, r, *осн))),
    (rf"^the baker made {Ч} cakes and {Ч} pastries and sold {Ч} (cakes|pastries); the baker does not still have {Ч} cakes: the baker has {Ч}\.$",
     _рамка(lambda n, m, k, что, ч, и: и == (n - k if что == "cakes" else n) and ч != и)),
    (rf"^if the baker made {Ч} cakes and {Ч} pastries and sold {Ч} cakes, how many cakes would the baker still have\? {Ч} cakes; the {Ч} pastries do not count; {Ч} − {Ч} = {Ч}\.$",
     _рамка(lambda n, m, k, on, om, on2, ok, r: (on, om, on2, ok) == (n, m, n, k) and r == n - k >= 0)),
    (rf"^if the baker made {Ч} cakes and {Ч} pastries and sold {Ч} pastries, how many cakes would the baker still have\? {Ч} cakes; the pastries sold are not cakes\.$",
     _рамка(lambda n, m, k, on: on == n)),
    # 25 класс
    (rf"^there are {Ч} girls and {Ч} boys in the class; the class has {Ч} pupils: {Ч} \+ {Ч} = {Ч}\.$",
     _рамка(lambda g, b, s, og, ob, os: s == g + b and (og, ob, os) == (g, b, s))),
    (rf"^в классе {Ч} {СЛ} и {Ч} {СЛ}; в классе {Ч} {СЛ}: {Ч} \+ {Ч} = {Ч}\.$",
     _рамка(lambda g, s1, b, s2, s, s3, og, ob, os: s == g + b and (og, ob, os) == (g, b, s))),
    (rf"^there are {Ч} girls and {Ч} boys in the class; the class does not have {Ч} pupils: it has {Ч}\.$",
     _рамка(lambda g, b, ч, и: и == g + b and ч != и)),
    (rf"^if there are {Ч} girls and {Ч} boys in the class, how many pupils are there in the class\? {Ч} \+ {Ч} = {Ч}\.$",
     _рамка(lambda g, b, og, ob, s: (og, ob) == (g, b) and s == g + b)),
    (rf"^there are {Ч} pupils in the class and {Ч} of them are girls; there are {Ч} boys in the class: {Ч} − {Ч} = {Ч}\.$",
     _рамка(lambda s, g, b, os, og, ob: b == s - g > 0 and (os, og, ob) == (s, g, b))),
    (rf"^в классе {Ч} {СЛ}, из них {Ч} {СЛ}; в классе {Ч} {СЛ}: {Ч} − {Ч} = {Ч}\.$",
     _рамка(lambda s, s1, g, s2, b, s3, os, og, ob: b == s - g > 0 and (os, og, ob) == (s, g, b))),
    (rf"^there are {Ч} pupils in the class and {Ч} of them are girls; there are not {Ч} boys in the class: there are {Ч}\.$",
     _рамка(lambda s, g, ч, и: и == s - g > 0 and ч != и)),
    (rf"^if there are {Ч} pupils in the class and {Ч} of them are girls, how many boys are there in the class\? {Ч} − {Ч} = {Ч}\.$",
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
    (rf"^{С} gave the craftsman {Ч} {Ч}-dollar bills for a hat worth {Ч} dollars; the change is {Ч} dollars: {Ч} × {Ч} − {Ч} = {Ч}\.$",
     _рамка(lambda n1, n, b, p, c, on, ob, op, oc: c == n * b - p > 0 and (on, ob, op, oc) == (n, b, p, c))),
    (rf"^{ИМЯ} {СЛ} мастеру {Ч} {СЛ} по {Ч} {СЛ} за шляпу ценой {Ч} {СЛ}; сдача {Ч} {СЛ}: {Ч} × {Ч} − {Ч} = {Ч}\.$",
     _рамка(lambda n1, g, n, s1, b, s2, p, s3, c, s4, on, ob, op, oc: c == n * b - p > 0 and (on, ob, op, oc) == (n, b, p, c))),
    (rf"^{С} gave the craftsman {Ч} {Ч}-dollar bills for a hat worth {Ч} dollars; the change is not {Ч} dollars: it is {Ч}\.$",
     _рамка(lambda n1, n, b, p, ч, и: и == n * b - p > 0 and ч != и)),
    (rf"^if {С} gave the craftsman {Ч} {Ч}-dollar bills for a hat worth {Ч} dollars, how much change did {С} get\? {Ч} × {Ч} − {Ч} = {Ч} dollars\.$",
     _рамка(lambda n1, n, b, p, n2, on, ob, op, c: n1 == n2 and (on, ob, op) == (n, b, p) and c == n * b - p > 0)),
    # 28 прибыль
    (rf"^{С} bought the magazines at {Ч} dollars and sells them at {Ч}/{Ч} of the price; the profit is {Ч} dollars: {Ч} × {Ч} ÷ {Ч} − {Ч} = {Ч}\.$",
     _рамка(lambda n1, p, a, b, r, op, oa, ob, op2, or_: p % b == 0 and r == p * a // b - p > 0 and (op, oa, ob, op2, or_) == (p, a, b, p, r))),
    (rf"^{ИМЯ} {СЛ} журналы за {Ч} {СЛ} и продаёт их за {Ч}/{Ч} цены; прибыль {Ч} {СЛ}: {Ч} × {Ч} ÷ {Ч} − {Ч} = {Ч}\.$",
     _рамка(lambda n1, g, p, s1, a, b, r, s2, op, oa, ob, op2, or_: p % b == 0 and r == p * a // b - p > 0 and (op, oa, ob, op2, or_) == (p, a, b, p, r))),
    (rf"^{С} bought the magazines at {Ч} dollars and sells them at {Ч}/{Ч} of the price; the profit is not {Ч} dollars: it is {Ч}\.$",
     _рамка(lambda n1, p, a, b, ч, и: p % b == 0 and и == p * a // b - p > 0 and ч != и)),
    (rf"^if {С} bought the magazines at {Ч} dollars and sells them at {Ч}/{Ч} of the price, what is the profit\? {Ч} × {Ч} ÷ {Ч} − {Ч} = {Ч} dollars\.$",
     _рамка(lambda n1, p, a, b, op, oa, ob, op2, r: p % b == 0 and (op, oa, ob, op2) == (p, a, b, p) and r == p * a // b - p > 0)),
    # 29 завышение
    (rf"^{С} reported {Ч} people at the concert, overstating the number by {Ч} percent; {Ч} people really attended: {Ч} × 100 ÷ \(100 \+ {Ч}\) = {Ч}\.$",
     _рамка(lambda n1, n, q, r, on, oq, or_: r * (100 + q) == n * 100 and (on, oq, or_) == (n, q, r))),
    (rf"^{ИМЯ} {СЛ}, что на концерте было {Ч} {СЛ}, завысив число на {Ч} {СЛ}; на самом деле было {Ч} {СЛ}: {Ч} × 100 ÷ \(100 \+ {Ч}\) = {Ч}\.$",
     _рамка(lambda n1, g, n, s1, q, s2, r, s3, on, oq, or_: r * (100 + q) == n * 100 and (on, oq, or_) == (n, q, r))),
    (rf"^{С} reported {Ч} people at the concert, overstating the number by {Ч} percent; the real number is not {Ч}: it is {Ч}\.$",
     _рамка(lambda n1, n, q, ч, и: и * (100 + q) == n * 100 and ч != и)),
    (rf"^if {С} reported {Ч} people at the concert, overstating the number by {Ч} percent, how many people really attended\? {Ч} × 100 ÷ \(100 \+ {Ч}\) = {Ч}\.$",
     _рамка(lambda n1, n, q, on, oq, r: (on, oq) == (n, q) and r * (100 + q) == n * 100)),
    # 30 половина / кратно и всего
    (rf"^there were {Ч} ants and {КР} bugs as ants in the garden; there were {Ч} insects in all: {Ч} \+ {Ч} (÷|×) {Ч} = {Ч}\.$",
     _рамка(_всего_насекомых)),
    (rf"^в саду было {Ч} {СЛ} и {КР_RU} жуков; всего муравьёв и жуков {Ч}: {Ч} \+ {Ч} (÷|×) {Ч} = {Ч}\.$",
     _рамка(lambda n, s, кр, t, on, on2, знак, k, ot: _всего_насекомых(n, кр, t, on, on2, знак, k, ot))),
    (rf"^there were {Ч} ants and {КР} bugs as ants in the garden; there were not {Ч} insects in all: there were {Ч}\.$",
     _рамка(lambda n, кр, ч, и: и == n + (n // КР_К[кр][0] if КР_К[кр][1] else n * КР_К[кр][0]) and (not КР_К[кр][1] or n % КР_К[кр][0] == 0) and ч != и)),
    (rf"^if there were {Ч} ants and {КР} bugs as ants in the garden, how many insects were there in all\? {Ч} \+ {Ч} (÷|×) {Ч} = {Ч}\.$",
     _рамка(lambda n, кр, on, on2, знак, k, t: _всего_насекомых(n, кр, t, on, on2, знак, k, t))),
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
)
# RU QA-ФОРМЫ СЕМЕЙСТВ (М-146: вопросная поверхность на каждом языке рамки).
СРОК_RU2 = r"(утром|днём|вечером)"
ЧЕТВЕРТИ_RU = r"(четверть|две четверти|три четверти)"


def _четверти_ru(часть, слово, oч, k, целое):
    k_ = {4: 1, "четверть": 1, "две четверти": 2, "три четверти": 3}.get(слово)
    return k_ is not None and oч == часть and k == k_ and целое * k == часть * 4


РУ_ВОПРОСЫ = {
    "сумма": [(rf"^если {ИМЯ} имеет {Ч} {С}, а {ИМЯ} имеет {Ч} {С}, сколько {С} у них всего\? {Ч} \+ {Ч} = {Ч}\.$",
               _рамка(lambda n1, x, в1, n2, y, в2, в3, ox, oy, s: (ox, oy) == (x, y) and s == x + y))],
    "температура": [(rf"^если температура была {Ч} {СЛ} и (упала|поднялась) на {Ч} {СЛ}, какова температура теперь\? {Ч} ([+−]) {Ч} = {Ч}\.$",
                     _рамка(lambda t0, s1, г, d, s2, ot0, зн, od, t1: (ot0, od) == (t0, d) and зн == ("−" if г == "упала" else "+") and t1 == t0 + (-d if г == "упала" else d)))],
    "процент": [(rf"^если в классе {Ч} {СЛ}, из них {Ч} — {СЛ}, какова доля девочек в процентах\? {Ч} {СЛ} и {Ч} {СЛ}: {Ч} ÷ {Ч} × 100 = {Ч}\.$",
                 _рамка(lambda всего, s1, часть, s2, oв, s3, oч, s4, oч2, oв2, p: (oв, oч, oч2, oв2) == (всего, часть, часть, всего) and часть * 100 == p * всего))],
    "фунты": [(rf"^если посылка весит {Ч} {СЛ}, а в фунте 16 унций, каков вес в фунтах\? {Ч} ÷ 16 = {Ч}\.$",
               _рамка(lambda у, s, oу, ф: oу == у and ф * 16 == у))],
    "глубина": [(rf"^если бак шириной {Ч} {СЛ} и длиной {Ч} {СЛ} вмещает {Ч} кубических футов воды, какова глубина воды в баке\? {Ч} на {Ч} при {Ч}: {Ч} ÷ \({Ч} × {Ч}\) = {Ч}\.$",
                 _рамка(lambda w, s1, l, s2, v, ow, ol, ov, ov2, ow2, ol2, h: (ow, ol, ov, ov2, ow2, ol2) == (w, l, v, v, w, l) and h * w * l == v))],
    "вероятность": [(rf"^если в мешке {Ч} {СЛ} красных и {Ч} {СЛ} синих, какова вероятность вынуть красный шар, выраженная дробью\? {Ч} красных и {Ч} синих: {Ч}/{Ч}\.$",
                     _рамка(lambda r, s1, b, s2, or_, ob, r2, n: (or_, ob, r2) == (r, b, r) and n == r + b))],
    "четверти": [(rf"^если {Ч} — это {ЧЕТВЕРТИ_RU} класса, сколько учеников в классе\? {Ч} ÷ {Ч} × 4 = {Ч}\.$", _рамка(_четверти_ru))],
    "дополнение": [(rf"^если на стоянке изначально было {Ч} {СЛ}, а {Ч} уехали, сколько машин осталось\? {Ч} − {Ч} = {Ч}\.$",
                    _рамка(lambda б, s, у, oб, oу, о: (oб, oу) == (б, у) and о == б - у)),
                   (rf"^если в наборе {Ч} {СЛ}, а в коробке {Ч} {СЛ}, сколько деталей не хватает\? {Ч} − {Ч} = {Ч}\.$",
                    _рамка(lambda б, s1, о, s2, oб, oо, у: (oб, oо) == (б, о) and у == б - о)),
                   (rf"^если в автобусе было {Ч} {СЛ}, а {Ч} вышли, сколько человек в автобусе теперь\? {Ч} − {Ч} = {Ч}\.$",
                    _рамка(lambda б, s, у, oб, oу, о: (oб, oу) == (б, у) and о == б - у))],
    "население": [(rf"^если в городе {Ч} {СЛ}, и {ДОЛЯ} всего населения живёт в центре, сколько человек живёт в центре\? {Ч} ÷ {Ч} = {Ч}\.$",
                   _рамка(lambda N, s, d, oN, od, c: (oN, od) == (N, d) and N == d * c))],
    "команда": [(rf"^если в команде {Ч} {СЛ} и {Ч} {СЛ}, сколько человек в команде\? {Ч} \+ {Ч} = {Ч}\.$",
                 _рамка(lambda m, s1, d, s2, om, od, s: (om, od) == (m, d) and s == m + d))],
    "кратно": [(rf"^если машина стоила {Ч} {СЛ}, а дом стоил {КРАТ} дороже машины, сколько стоил дом\? {Ч} {СЛ}: {Ч} × {Ч} = {Ч}\.$",
                _рамка(lambda c, s, k, oc0, s2, oc, ok, h: (oc0, oc, ok) == (c, c, k) and h == c * k))],
    "проект": [(rf"^если проект начался с {Ч} {СЛ}, его {УДВ} и потом убавили на {Ч}, сколько панелей в итоговом проекте\? {Ч} × {Ч} − {Ч} = {Ч}\.$",
                _рамка(lambda s0, s, k, m, os0, ok, om, f: (os0, ok, om) == (s0, k, m) and f == s0 * k - m))],
    "окружность": [(rf"^если длину окружности земли берут за {Ч} {СЛ}, а самолёт летит {Ч} {СЛ} в час, сколько часов занимает полёт вокруг земли\? {Ч} ÷ {Ч} = {Ч}\.$",
                    _рамка(lambda L, s1, v, s2, oL, ov, t: (oL, ov) == (L, v) and L == v * t))],
    "верёвки": [(rf"^если общая длина верёвок {Ч} {СЛ}, а верёвок {Ч}, какова длина средней верёвки\? {Ч} ÷ {Ч} = {Ч}\.$",
                 _рамка(lambda T, s, n, oT, on, a: (oT, on) == (T, n) and T == n * a))],
    "трое": [(rf"^если {ИМЯ} имеет {Ч} {СЛ}, {ИМЯ} имеет на {Ч} {СЛ} больше, чем {ИМЯ}, а {ИМЯ} имеет {КРАТ} больше книг, чем {ИМЯ}, сколько книг у них вместе\? {Ч} \+ \({Ч} \+ {Ч}\) \+ {Ч} × {Ч} = {Ч}\.$",
              _рамка(lambda x, a, s1, y, b, s2, x2, z, k, x3, oa, oa2, ob, ok, oa3, s: x == x2 == x3 and (oa, oa2, ob, ok, oa3) == (a, a, b, k, a) and s == a + (a + b) + k * a))],
    "ставка": [(rf"^если {ИМЯ} делает {Ч} {СЛ} в час и работает {Ч} {СЛ}, сколько свечей делает {ИМЯ}\? {Ч} × {Ч} = {Ч}\.$",
                _рамка(lambda n1, r, s1, t, s2, n2, or_, ot, s: n1 == n2 and (or_, ot) == (r, t) and s == r * t))],
    "листки": [(rf"^если у {ИМЯ} было {Ч} {СЛ}, {Ч} ушли на холодильник и {Ч} на дверь, сколько листков осталось\? {Ч} − {Ч} − {Ч} = {Ч}\.$",
                _рамка(lambda n, b, s, r, d, ob, or_, od, k: (ob, or_, od) == (b, r, d) and k == b - r - d))],
    "разница": [(rf"^если {ИМЯ} утром посадила? {Ч} {СЛ}, а днём {Ч} {СЛ}, на сколько деревьев больше утром, чем днём\? {Ч} − {Ч} = {Ч}\.$",
                 _рамка(lambda n, x, s1, y, s2, ox, oy, d: (ox, oy) == (x, y) and d == x - y > 0))],
    "скидка": [(rf"^если каждая пачка стоит {Ч} {СЛ}, и на каждую пачку скидка {Ч} {СЛ}, сколько надо заплатить за каждую пачку\? {Ч} − {Ч} = {Ч}\.$",
                _рамка(lambda c, s1, s, s2, oc, os, p: (oc, os) == (c, s) and p == c - s))],
    "всего": [(rf"^если у {ИМЯ} было {Ч} {СЛ}, а {ИМЯ} отдала? {Ч}, сколько {СЛ} осталось\? {Ч} {СЛ}: {Ч} − {Ч} = {Ч}\.$",
               _рамка(lambda n1, x, s1, n2, y, s2, ox0, s3, ox, oy, s: _тот_же(n1, n2) and (ox0, ox, oy) == (x, x, y) and s == x - y)),
              (rf"^если у {ИМЯ} {Ч} {СЛ} в одной коробке и {Ч} {СЛ} в другой, сколько всего {СЛ} у {ИМЯ}\? {Ч} \+ {Ч} = {Ч}\.$",
               _рамка(lambda n1, x, s1, y, s2, s3, n2, ox, oy, s: n1 == n2 and (ox, oy) == (x, y) and s == x + y))],
    "группы": [(rf"^если {Ч} {СЛ} стоят группами по {Ч}, сколько групп\? {Ч} ÷ {Ч} = {Ч}\.$",
                _рамка(lambda T, s, n, oT, on, g: (oT, on) == (T, n) and T == n * g))],
    "больше_A": [(rf"^если {ИМЯ} {СЛ} {КОГДА_RU} {Ч} {СЛ}, а {КОГДА_RU} {Ч} {СЛ}, на сколько {СЛ} больше {КОГДА_RU}, чем {КОГДА_RU}\? {Ч} {СЛ} {КОГДА_RU}: {Ч} − {Ч} = {Ч}\.$",
                  _рамка(lambda n, g, w1, x, s1, w2, y, s2, s3, w3, w4, ox0, s4, w5, ox, oy, d: (w1, w2, w1) == (w3, w4, w5) and (ox0, ox, oy) == (x, x, y) and d == x - y > 0))],
    "больше_B": [(rf"^если {ИМЯ} {СЛ} {Ч} {СЛОВА} и {Ч} {СЛОВА}, на сколько {СЛОВА} больше, чем {СЛОВА}\? {Ч} − {Ч} = {Ч}\.$",
                  _рамка(lambda n, g, x, s1, y, s2, s3, s4, ox, oy, d: (ox, oy) == (x, y) and d == x - y > 0))],
    "больше_C": [(rf"^если на заборе было {Ч} {СЛ} и {Ч} {СЛ}, на сколько {СЛ} больше, чем {СЛ}\? {Ч} − {Ч} = {Ч}\.$",
                  _рамка(lambda x, a, y, b, a2, b2, ox, oy, d: (ox, oy) == (x, y) and d == x - y > 0))],
    "больше_D": [(rf"^если {ИМЯ} {СЛ} {Ч} {СЛ} {НА_RU} и {Ч} {СЛ} {НА_RU}, на сколько долларов больше потрачено {НА_RU}, чем {НА_RU}\? {Ч} − {Ч} = {Ч}\.$",
                  _рамка(lambda n, g, x, s1, на1, y, s2, на2, на3, на4, ox, oy, d: (на1, на2) == (на3, на4) and (ox, oy) == (x, y) and d == x - y > 0))],
    "отбор": [(rf"^если {ИМЯ} {СЛ} утром {Ч} {СЛ}, днём {Ч} и вечером {Ч}, сколько {СЛ} {ИМЯ} {СЛ} {СРОК_RU2}\? {Ч} {СРОК_RU2}\.$",
               _рамка(lambda n1, g1, a, s1, b, c, s2, n2, g2, w, v, w2: n1 == n2 and g1 == g2 and w == w2 and len({a, b, c}) == 3 and v == _срок(w, a, b, c)))],
    "остаток": [(rf"^если пекарь испёк {Ч} {СЛ} и {Ч} {СЛ} и продал {Ч} (торт[а-я]*), сколько тортов осталось\? {Ч} {СЛ}; {Ч} {СЛ} не в счёт; {Ч} − {Ч} = {Ч}\.$",
                 _рамка(lambda n, s1, m, s2, k, что, on, s3, om, s4, on2, ok, r: (on, om, on2, ok) == (n, m, n, k) and r == n - k >= 0)),
                (rf"^если пекарь испёк {Ч} {СЛ} и {Ч} {СЛ} и продал {Ч} (булоч[а-я]*), сколько тортов осталось\? {Ч} {СЛ}: проданы булочки, не торты\.$",
                 _рамка(lambda n, s1, m, s2, k, что, on, s3: on == n))],
    "класс": [(rf"^если в классе {Ч} {СЛ} и {Ч} {СЛ}, сколько учеников в классе\? {Ч} \+ {Ч} = {Ч}\.$",
               _рамка(lambda g, s1, b, s2, og, ob, s: (og, ob) == (g, b) and s == g + b)),
              (rf"^если в классе {Ч} {СЛ}, из них {Ч} {СЛ}, сколько мальчиков в классе\? {Ч} − {Ч} = {Ч}\.$",
               _рамка(lambda s, s1, g, s2, os, og, b: (os, og) == (s, g) and b == s - g > 0))],
    "деньги": [(rf"^если {ИМЯ} {СЛ} {Ч} {СЛ} по {Ч} {СЛ}, сколько денег {ИМЯ} {СЛ}\? {Ч} × {Ч} = {Ч}\.$",
                _рамка(lambda n1, g, n, s1, p, s2, n2, g2, on, op, t: n1 == n2 and (on, op) == (n, p) and t == n * p)),
               (rf"^если у {ИМЯ} было {Ч} {СЛ}, а {ИМЯ} {СЛ} {Ч} {СЛ}, сколько денег осталось\? {Ч} − {Ч} = {Ч}\.$",
                _рамка(lambda n1, a, s1, n2, g, b, s2, oa, ob, c: _тот_же(n1, n2) and (oa, ob) == (a, b) and c == a - b > 0))],
    "сдача": [(rf"^если {ИМЯ} {СЛ} мастеру {Ч} {СЛ} по {Ч} {СЛ} за шляпу ценой {Ч} {СЛ}, какова сдача\? {Ч} × {Ч} − {Ч} = {Ч}\.$",
               _рамка(lambda n1, g, n, s1, b, s2, p, s3, on, ob, op, c: (on, ob, op) == (n, b, p) and c == n * b - p > 0))],
    "прибыль": [(rf"^если {ИМЯ} {СЛ} журналы за {Ч} {СЛ} и продаёт их за {Ч}/{Ч} цены, какова прибыль\? {Ч} × {Ч} ÷ {Ч} − {Ч} = {Ч}\.$",
                 _рамка(lambda n1, g, p, s, a, b, op, oa, ob, op2, r: p % b == 0 and (op, oa, ob, op2) == (p, a, b, p) and r == p * a // b - p > 0))],
    "завышение": [(rf"^если {ИМЯ} {СЛ}, что на концерте было {Ч} {СЛ}, завысив число на {Ч} {СЛ}, сколько человек было на самом деле\? {Ч} × 100 ÷ \(100 \+ {Ч}\) = {Ч}\.$",
                   _рамка(lambda n1, g, n, s1, q, s2, on, oq, r: (on, oq) == (n, q) and r * (100 + q) == n * 100))],
    "половина": [(rf"^если в саду было {Ч} {СЛ} и {КР_RU} жуков, сколько всего муравьёв и жуков\? {Ч} \+ {Ч} (÷|×) {Ч} = {Ч}\.$",
                  _рамка(lambda n, s, кр, on, on2, знак, k, t: _всего_насекомых(n, кр, t, on, on2, знак, k, t)))],
}
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


def судить(строка):
    """(судимо, истинно) для одной строки."""
    с = строка.strip()
    м = ХВОСТ_ОТВЕТА.match(с)
    if м and "?" in м.group(1):
        судимо, истинно = судить(м.group(1))
        if судимо:
            return True, истинно and м.group(2) == м.group(3)
    for образец, проверить in ПРАВИЛА:
        м = образец.match(с)
        if м:
            try:
                ист = bool(проверить(м))
            except (ValueError, KeyError):
                return True, False
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


if __name__ == "__main__":
    sys.exit(main())
