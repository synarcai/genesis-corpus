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
import pathlib
import re
import sys

КОРЕНЬ = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(КОРЕНЬ / "tools"))
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
    (rf"^the parcel weighs {Ч} ounces and a pound is 16 ounces\. what is the weight in pounds\? {Ч} ÷ 16 = {Ч}\.$", _фунты_qa),
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
ПРАВИЛА = tuple((re.compile(о), п) for о, п in ОБРАЗЦЫ)


def судить(строка):
    """(судимо, истинно) для одной строки."""
    с = строка.strip()
    for образец, проверить in ПРАВИЛА:
        м = образец.match(с)
        if м:
            try:
                return True, bool(проверить(м))
            except (ValueError, KeyError):
                return True, False
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
