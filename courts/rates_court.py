#!/usr/bin/env python3
"""СУД СТАВКИ, ДЕНЕГ И ВРЕМЕНИ: отношение ПРОХОДИТСЯ, а не сверяется.

Слой ставок утверждает четыре разных вещи, и каждая проверяется своим
ходом, не сводимым к прочим:

    ЧИСЛОФОРМА — «a week has 7 days» и «7 days make a week» суть ОДНО
        отношение, сказанное с двух концов; суд проходит граф единиц
        (`units.отношение`) и требует, чтобы обе стороны дали один
        множитель. Заодно проверяется английское согласование: при
        числе один — единственное («1 dollar», не «1 dollars»), и
        артикль по ЗВУКУ («an hour», не «a hour»).
    СТАВКА — «30 dollars every day» и «in 4 days … 120 dollars»:
        произведение пересчитывается, и обе единицы обязаны быть
        объявленными в доме единиц.
    ТРАТА — вычитание с остатком; полярность проверяется отдельно от
        числа: «потратил» обязано УМЕНЬШАТЬ.
    КРУПНОЕ И МЕЛКОЕ — «1 dollar and 5 cents are 105 cents» проходится
        тем же отношением, что и «a dollar has 100 cents».

РУССКОЕ СОГЛАСОВАНИЕ ПРИ ЧИСЛЕ судится домом единиц («2 часа», «5
часов»), а предложный множественного — правилом русского дома. Слой,
сказавший «в двух час», не пройдёт: это не описка, а неверный язык.
"""

import pathlib
import re
import sys

КОРЕНЬ = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(КОРЕНЬ / "tools"))
import rugram  # noqa: E402
import units  # noqa: E402
from genesis import Unreadable, worlds  # noqa: E402

# РУБЕЖ-ДОЛГА: ЛОЖНЫХ_РУБЕЖ = 0
ЛОЖНЫХ_РУБЕЖ = 0

# ПУСТОЙ-ОБХОД: no-such-corpus-file

# ДЕЯТЕЛЬ СТАВКИ ЧИТАЕТСЯ ПО ОБЪЯВЛЕНИЮ ГЕНЕРАТОРА, А НЕ ЛЮБЫМ СЛОВОМ.
# Подсадка словом: «a driver earns 6 rubles every hour» → «a drive
# earns …» — суд читал ставку и единицы, а деятеля брал каким дали, и
# звал строку истиной. Деятели объявлены генератором мира; необъявленный
# деятель — чужая рамка, и суд о ней молчит (М-131: молчать о своём с
# искажённым словом нельзя, но и звать ложью чужое — тоже; здесь строка
# без объявленного деятеля не есть строка этого мира).
import gen_genesis_rates as _Г  # noqa: E402
ДЕЯТЕЛИ_EN = {д[0] for д in _Г.ДЕЯТЕЛИ}
_ЕД = {}
_ИМЯ = {}
for _и in units.ФОРМЫ_ВСЕХ:
    try:
        _ЕД[_и] = units.англ(_и)
        _ИМЯ[units.англ(_и)] = _и
        _ИМЯ[units.англ(_и, True)] = _и
    except (KeyError, IndexError):
        continue

_НЕМОЕ_H = ("hour", "honest", "heir")
# русское имя единицы по английскому — для падежных форм парадигмы
_РУССКОЕ_ИМЯ = {"hour": "час", "minute": "минута", "day": "день",
                "week": "неделя", "month": "месяц", "year": "год",
                "rouble": "рубль", "kopeck": "копейка",
                "kilometre": "километр"}


def артикль(слово):
    if слово[0] in "aeiou" or слово.startswith(_НЕМОЕ_H):
        return "an"
    return "a"


def _форма_верна(n, слово):
    """Английская форма при числе: один — единственное, прочее — мн."""
    имя = _ИМЯ.get(слово)
    if имя is None:
        return False
    return слово == units.англ(имя, n != 1)


def _ру_верна(n, слово, имя):
    """Русская форма при счёте — по объявленной тройке дома единиц."""
    try:
        return слово == units.рус(имя, n)
    except (KeyError, IndexError):
        return False


ИМЕЕТ = re.compile(r"^(a|an) (\w+) has (\d+) (\w+)\.$")
СОСТАВЛЯЮТ = re.compile(r"^(\d+) (\w+) make (a|an) (\w+)\.$")
СТОЛЬКО = re.compile(r"^(\d+) (\w+) are (\d+) (\w+)\.$")
МНОЖЕСТВО_И = re.compile(
    r"^the plural of (\w+) is (\w+), and 1 (\w+) is (\d+) (\w+)\.$")
СКОЛЬКО = re.compile(
    r"^how many (\w+) are in (\d+) (\w+)\? (\d+) (\w+) are (\d+) "
    r"(\w+)\.$")
СКОЛЬКО_RU = re.compile(
    r"^сколько (\S+) в (\S+) (\S+)\? (\d+) (\S+) — это (\d+) (\S+)\.$")
В_ЕДИНИЦЕ_RU = re.compile(r"^в (\S+) (\d+) (\S+)\.$")
СОСТАВЛЯЮТ_RU = re.compile(r"^(\d+) (\S+) составляют (\S+)\.$")
СТОЛЬКО_RU = re.compile(r"^(\d+) (\S+) — это (\d+) (\S+)\.$")
СТАВКА = re.compile(
    r"^(.+?) earns (\d+) (\w+) every (\w+)\.$")
СТАВКА_ЗА = re.compile(
    r"^(.+?) earns (\d+) (\w+) per (\w+); in (\d+) (\w+) (.+?) earns "
    r"(\d+) (\w+)\.$")
# THE QUESTION LINE IS WHOLE: the rate fact opens it (judged by СТАВКА on
# its own), the answer carries the product as a link the court recomputes.
СТАВКА_ВОПРОС = re.compile(
    r"^((.+?) earns (\d+) (\w+) every (\w+)\.) how much does (.+?) earn in (\d+) (\w+)\? in (\d+) (\w+) "
    r"(.+?) earns (\d+) (\w+): (\d+) × (\d+) = (\d+)\.$")
ТРАТА = re.compile(
    r"^he had (\d+) dollars and spent (\d+) dollars; he has (\d+) "
    r"dollars left\.$")
ТРАТА_ВОПРОС = re.compile(
    r"^how much does he have left after spending (\d+) dollars of "
    r"(\d+) dollars\? he has (\d+) dollars left\.$")
ТРАТА_RU = re.compile(
    r"^у него было (\d+) (\S+), он потратил (\d+) (\S+); у него "
    r"осталось (\d+) (\S+)\.$")
ДОЛЛАРЫ = re.compile(
    r"^(\d+) (dollars?) and (\d+) (cents?) are (\d+) cents\.$")
ЦЕНТЫ_ВОПРОС = re.compile(
    r"^how many cents are (\d+) (dollars?) and (\d+) (cents?)\? "
    r"(\d+) (dollars?) and (\d+) (cents?) are (\d+) cents\.$")
ЦЕНТЫ = re.compile(
    r"^(\d+) cents are (\d+) (dollars?) and (\d+) (cents?)\.$")


ЗА_ШТУКУ = re.compile(r"^each (\w+) costs (\d+) dollars\.$")
ЗА_ШТУКУ_N = re.compile(
    r"^each (\w+) costs (\d+) dollars; (\d+) (\w+)s cost (\d+) "
    r"dollars\.$")
ЗА_ШТУКУ_ВОПРОС = re.compile(
    r"^(each (\w+) costs (\d+) dollars\.) how much do (\d+) (\w+)s cost\? (\d+) (\w+)s cost (\d+) "
    r"dollars: (\d+) × (\d+) = (\d+)\.$")
ЗА_ШТУКУ_ВОПРОС_RU = re.compile(
    r"^одна (\S+) стоит (\d+) (\S+)\. сколько стоят (\d+) (\S+)\? (\d+) (\S+) стоят (\d+) "
    r"(\S+): (\d+) × (\d+) = (\d+)\.$")
ЗА_ШТУКУ_RU = re.compile(
    r"^одна (\S+) стоит (\d+) (\S+); (\d+) (\S+) стоят (\d+) "
    r"(\S+)\.$")
ВМЕСТЕ = re.compile(
    r"^the (\w+) costs (\d+) dollars and the (\w+) costs (\d+) "
    r"dollars; the (\w+) and the (\w+) cost (\d+) dollars\.$")
ВМЕСТЕ_RU = re.compile(
    r"^(\S+) стоит (\d+) (\S+), а (\S+) стоит (\d+) (\S+); вместе "
    r"они стоят (\d+) (\S+)\.$")
СТАВКА_RU = re.compile(
    r"^(\S+) зарабатывает (\d+) (\S+) в (\S+)\.$")
СТАВКА_ЗА_RU = re.compile(
    r"^(\S+) зарабатывает (\d+) (\S+) в (\S+); за (\d+) (\S+) "
    r"(\S+) зарабатывает (\d+) (\S+)\.$")
СТАВКА_ВОПРОС_RU = re.compile(
    r"^((\S+) зарабатывает (\d+) (\S+) в (\S+)\.) сколько (\S+) (\S+) зарабатывает за (\d+) (\S+)\? за (\d+) "
    r"(\S+) (\S+) зарабатывает (\d+) (\S+): (\d+) × (\d+) = (\d+)\.$")
ДОЛЛАРЫ_RU = re.compile(
    r"^(\d+) (\S+) (\d+) (\S+) — это (\d+) (\S+)\.$")

# {русская форма единицы: английское имя} — обратный ход дома единиц,
# чтобы суд узнавал единицу по ЛЮБОЙ её русской форме.
_РУ_ФОРМА = {}
for _и in units.ФОРМЫ_ВСЕХ:
    for _с in (1, 2, 5):
        try:
            _РУ_ФОРМА.setdefault(units.рус(_и, _с), _и)
        except (KeyError, IndexError):
            break


def _ру_имя(форма):
    return _РУ_ФОРМА.get(форма)


def _отношение(крупно, мелко):
    имя_к, имя_м = _ИМЯ.get(крупно), _ИМЯ.get(мелко)
    if имя_к is None or имя_м is None:
        return None
    return units.отношение(имя_к, имя_м)


def судить(строка):
    """(судимо, истинно) для одной строки."""
    с = строка.strip()
    if not с:
        return False, False
    m = ИМЕЕТ.match(с)
    if m:
        арт, крупно, k, мелко = m.group(1), m.group(2), int(m.group(3)), m.group(4)
        k0 = _отношение(крупно, мелко)
        if k0 is None:
            return False, False
        return True, (k0 == k and арт == артикль(крупно)
                      and _форма_верна(1, крупно)
                      and _форма_верна(k, мелко))
    m = СОСТАВЛЯЮТ.match(с)
    if m:
        k, мелко, арт, крупно = int(m.group(1)), m.group(2), m.group(3), m.group(4)
        k0 = _отношение(крупно, мелко)
        if k0 is None:
            return False, False
        return True, (k0 == k and арт == артикль(крупно)
                      and _форма_верна(k, мелко))
    m = МНОЖЕСТВО_И.match(с)
    if m:
        ед, мн, ед2, k, мелко = (m.group(1), m.group(2), m.group(3),
                                 int(m.group(4)), m.group(5))
        имя = _ИМЯ.get(ед)
        k0 = _отношение(ед, мелко)
        if имя is None or k0 is None:
            return False, False
        return True, (units.англ(имя, True) == мн and ед2 == ед
                      and k0 == k and _форма_верна(k, мелко))
    m = СТОЛЬКО.match(с)
    if m:
        n, крупно, m2, мелко = (int(m.group(1)), m.group(2),
                                int(m.group(3)), m.group(4))
        k0 = _отношение(крупно, мелко)
        if k0 is None:
            return False, False
        return True, (n * k0 == m2 and _форма_верна(n, крупно)
                      and _форма_верна(m2, мелко))
    m = СКОЛЬКО.match(с)
    if m:
        г = m.groups()
        if г[1] != г[3] or г[2] != г[4]:
            return True, False
        k0 = _отношение(г[2], г[0])
        if k0 is None:
            return False, False
        return True, (int(г[1]) * k0 == int(г[5]) and г[6] == г[0]
                      and _форма_верна(int(г[1]), г[2])
                      and _форма_верна(int(г[5]), г[6]))
    m = СТАВКА.match(с)
    if m:
        кто, ставка, деньги, время = (m.group(1), int(m.group(2)),
                                      m.group(3), m.group(4))
        if _ИМЯ.get(деньги) is None or _ИМЯ.get(время) is None:
            return False, False
        if кто not in ДЕЯТЕЛИ_EN:
            return False, True
        return True, (_форма_верна(ставка, деньги)
                      and _форма_верна(1, время))
    m = СТАВКА_ЗА.match(с)
    if m:
        кто, ставка, деньги, время, n, время2, кто2, итог, деньги2 = (
            m.group(1), int(m.group(2)), m.group(3), m.group(4),
            int(m.group(5)), m.group(6), m.group(7), int(m.group(8)),
            m.group(9))
        if _ИМЯ.get(деньги) is None or _ИМЯ.get(время) is None:
            return False, False
        return True, (кто == кто2 and ставка * n == итог
                      and _ИМЯ.get(время2) == _ИМЯ.get(время)
                      and _ИМЯ.get(деньги2) == _ИМЯ.get(деньги)
                      and _форма_верна(ставка, деньги)
                      and _форма_верна(n, время2)
                      and _форма_верна(итог, деньги2))
    m = СТАВКА_ВОПРОС.match(с)
    if m:
        (факт, кто0, ставка, деньги0, время0, кто, n, время, n2, время2, кто2,
         итог, деньги, л1, л2, л3) = m.groups()
        ставка, n, n2, итог, л1, л2, л3 = (int(x) for x in (ставка, n, n2, итог, л1, л2, л3))
        if _ИМЯ.get(деньги) is None or _ИМЯ.get(время) is None:
            return False, False
        судимо, верно = судить(факт)          # the rate fact by its own rule
        if not судимо:
            return False, False
        # ВОПРОС ОБЯЗАН СПРАШИВАТЬ ТО ЖЕ, ЧЕМ ОТВЕЧАЕТ, И О ТОЙ ЖЕ СТАВКЕ.
        return True, (верно and кто0 == кто == кто2 and n == n2 and время == время2
                      and _ИМЯ.get(время0) == _ИМЯ[время] and _ИМЯ.get(деньги0) == _ИМЯ[деньги]
                      and итог == ставка * n and (л1, л2, л3) == (ставка, n, итог)
                      and _форма_верна(n, время)
                      and _форма_верна(итог, деньги))
    m = ТРАТА.match(с)
    if m:
        было, ушло, осталось = (int(x) for x in m.groups())
        return True, было - ушло == осталось and ушло > 0
    m = ТРАТА_ВОПРОС.match(с)
    if m:
        ушло, было, осталось = (int(x) for x in m.groups())
        return True, было - ушло == осталось and ушло > 0
    m = ТРАТА_RU.match(с)
    if m:
        было, ф1, ушло, ф2, осталось, ф3 = m.groups()
        было, ушло, осталось = int(было), int(ушло), int(осталось)
        return True, (было - ушло == осталось and ушло > 0
                      and _ру_верна(было, ф1, "rouble")
                      and _ру_верна(ушло, ф2, "rouble")
                      and _ру_верна(осталось, ф3, "rouble"))
    m = ЗА_ШТУКУ.match(с)
    if m:
        цена = int(m.group(2))
        return True, цена > 0 and _форма_верна(цена, "dollars")
    m = ЗА_ШТУКУ_N.match(с)
    if m:
        вещь, цена, n, вещь2, итог = (m.group(1), int(m.group(2)),
                                      int(m.group(3)), m.group(4),
                                      int(m.group(5)))
        return True, вещь == вещь2 and цена * n == итог
    m = ЗА_ШТУКУ_ВОПРОС.match(с)
    if m:
        (факт, вещь0, цена, n, вещь, n2, вещь2, итог, л1, л2, л3) = m.groups()
        цена, n, n2, итог, л1, л2, л3 = (int(x) for x in (цена, n, n2, итог, л1, л2, л3))
        судимо, верно = судить(факт)          # the price per piece by its own rule
        if not судимо:
            return False, False
        return True, (верно and вещь0 == вещь == вещь2 and n == n2 and n > 0
                      and итог == цена * n and (л1, л2, л3) == (цена, n, итог))
    m = ЗА_ШТУКУ_ВОПРОС_RU.match(с)
    if m:
        (вещь, цена, ф_ц, n, ф_в, n2, ф_в2, итог, ф_и, л1, л2, л3) = m.groups()
        цена, n, n2, итог, л1, л2, л3 = (int(x) for x in (цена, n, n2, итог, л1, л2, л3))
        if rugram.ПО_ФОРМЕ.get(вещь) != вещь:
            return False, False                # the thing is not a lemma of the house of forms
        return True, (n == n2 and n > 0 and ф_в == ф_в2 == rugram.форма(вещь, n)
                      and _ру_верна(цена, ф_ц, "rouble") and _ру_верна(итог, ф_и, "rouble")
                      and итог == цена * n and (л1, л2, л3) == (цена, n, итог))
    m = ЗА_ШТУКУ_RU.match(с)
    if m:
        вещь, цена, ф1, n, вещь_n, итог, ф2 = m.groups()
        цена, n, итог = int(цена), int(n), int(итог)
        # СОГЛАСОВАНИЕ РУССКОГО ИМЕНИ ПРИ СЧЁТЕ СУДИТСЯ ОТДЕЛЬНО ОТ
        # СЧЁТА: «3 книга» неверно даже при верном произведении.
        return True, (цена * n == итог
                      and _ру_верна(цена, ф1, "rouble")
                      and _ру_верна(итог, ф2, "rouble")
                      and rugram.согласовано(n, вещь_n) is not False
                      and rugram.согласовано(1, вещь) is not False)
    m = ВМЕСТЕ.match(с)
    if m:
        а_имя, а, б_имя, б, а2, б2, всего = (
            m.group(1), int(m.group(2)), m.group(3), int(m.group(4)),
            m.group(5), m.group(6), int(m.group(7)))
        return True, (а + б == всего and а_имя == а2 and б_имя == б2)
    m = ВМЕСТЕ_RU.match(с)
    if m:
        а_имя, а, ф1, б_имя, б, ф2, всего, ф3 = m.groups()
        а, б, всего = int(а), int(б), int(всего)
        return True, (а + б == всего and а_имя != б_имя
                      and _ру_верна(а, ф1, "rouble")
                      and _ру_верна(б, ф2, "rouble")
                      and _ру_верна(всего, ф3, "rouble"))
    m = СТАВКА_RU.match(с)
    if m:
        _кто, ставка, форма, _когда = m.groups()
        имя = _ру_имя(форма)
        return True, имя is not None and _ру_верна(int(ставка), форма,
                                                   имя)
    m = СТАВКА_ЗА_RU.match(с)
    if m:
        кто, ставка, ф_д, _ед, n, ф_в, кто2, итог, ф_д2 = m.groups()
        ставка, n, итог = int(ставка), int(n), int(итог)
        имя_д, имя_в = _ру_имя(ф_д), _ру_имя(ф_в)
        if имя_д is None or имя_в is None:
            return False, False
        return True, (кто == кто2 and ставка * n == итог
                      and _ру_верна(ставка, ф_д, имя_д)
                      and _ру_верна(n, ф_в, имя_в)
                      and _ру_верна(итог, ф_д2, имя_д))
    m = СТАВКА_ВОПРОС_RU.match(с)
    if m:
        (факт, кто0, ставка, ф_д0, в_ед, _ч, кто, n, ф_в, n2, ф_в2, кто2, итог, ф_д, л1, л2, л3) = m.groups()
        ставка, n, n2, итог, л1, л2, л3 = (int(x) for x in (ставка, n, n2, итог, л1, л2, л3))
        имя_д, имя_в = _ру_имя(ф_д), _ру_имя(ф_в)
        if имя_д is None or имя_в is None:
            return False, False
        судимо, верно = судить(факт)          # the rate fact by its own rule
        if not судимо:
            return False, False
        ру_в = _РУССКОЕ_ИМЯ.get(имя_в)
        return True, (верно and кто0 == кто == кто2 and n == n2 and ф_в == ф_в2
                      and _ру_имя(ф_д0) == имя_д and _ч == units.рус(имя_д, 5)
                      and ру_в is not None and rugram.ПАРАДИГМЫ[ру_в][3] == в_ед
                      and итог == ставка * n and (л1, л2, л3) == (ставка, n, итог)
                      and _ру_верна(n, ф_в, имя_в)
                      and _ру_верна(итог, ф_д, имя_д))
    m = В_ЕДИНИЦЕ_RU.match(с)
    if m:
        предл, k, форма = m.group(1), int(m.group(2)), m.group(3)
        имя_м = _ру_имя(форма)
        if имя_м is None:
            return False, False
        for крупно in units.ФОРМЫ_ВСЕХ:
            ру = _РУССКОЕ_ИМЯ.get(крупно)
            if ру and rugram.предложный_мн(ру) is not None and (
                    rugram.ПАРАДИГМЫ[ру][5] == предл):
                k0 = units.отношение(крупно, имя_м)
                if k0 is None:
                    return False, False
                return True, k0 == k and _ру_верна(k, форма, имя_м)
        return False, False
    m = СОСТАВЛЯЮТ_RU.match(с)
    if m:
        k, форма, вин = int(m.group(1)), m.group(2), m.group(3)
        имя_м = _ру_имя(форма)
        if имя_м is None:
            return False, False
        for крупно in units.ФОРМЫ_ВСЕХ:
            ру = _РУССКОЕ_ИМЯ.get(крупно)
            if ру and rugram.ПАРАДИГМЫ.get(ру) and (
                    rugram.ПАРАДИГМЫ[ру][3] == вин):
                k0 = units.отношение(крупно, имя_м)
                return True, k0 == k and _ру_верна(k, форма, имя_м)
        return False, False
    m = СТОЛЬКО_RU.match(с)
    if m:
        n, ф_к, итог, ф_м = m.groups()
        n, итог = int(n), int(итог)
        имя_к, имя_м = _ру_имя(ф_к), _ру_имя(ф_м)
        if имя_к is None or имя_м is None:
            return False, False
        k0 = units.отношение(имя_к, имя_м)
        if k0 is None:
            return False, False
        return True, (n * k0 == итог and _ру_верна(n, ф_к, имя_к)
                      and _ру_верна(итог, ф_м, имя_м))
    m = СКОЛЬКО_RU.match(с)
    if m:
        (ф_м5, _числ, предл, n, ф_к, итог, ф_м) = m.groups()
        n, итог = int(n), int(итог)
        имя_к, имя_м = _ру_имя(ф_к), _ру_имя(ф_м)
        if имя_к is None or имя_м is None:
            return False, False
        k0 = units.отношение(имя_к, имя_м)
        ру_к = _РУССКОЕ_ИМЯ.get(имя_к)
        return True, (k0 is not None and n * k0 == итог
                      and ру_к is not None
                      and rugram.предложный_мн(ру_к) == предл
                      and _ру_верна(n, ф_к, имя_к)
                      and _ру_верна(итог, ф_м, имя_м))
    m = ДОЛЛАРЫ_RU.match(с)
    if m:
        д, ф_д, ц, ф_ц, всего, ф_в = m.groups()
        д, ц, всего = int(д), int(ц), int(всего)
        k = units.отношение("rouble", "kopeck")
        return True, (д * k + ц == всего
                      and _ру_верна(д, ф_д, "rouble")
                      and _ру_верна(ц, ф_ц, "kopeck")
                      and _ру_верна(всего, ф_в, "kopeck"))
    m = ЦЕНТЫ_ВОПРОС.match(с)
    if m:
        д, фд, ц, фц, д2, фд2, ц2, фц2, всего = m.groups()
        д, ц, д2, ц2, всего = (int(д), int(ц), int(д2), int(ц2),
                               int(всего))
        k = units.отношение("dollar", "cent")
        return True, (д == д2 and ц == ц2 and фд == фд2 and фц == фц2
                      and д * k + ц == всего
                      and _форма_верна(д, фд) and _форма_верна(ц, фц))
    m = ДОЛЛАРЫ.match(с)
    if m:
        д, фд, ц, фц, всего = (int(m.group(1)), m.group(2),
                               int(m.group(3)), m.group(4),
                               int(m.group(5)))
        k = units.отношение("dollar", "cent")
        return True, (д * k + ц == всего and _форма_верна(д, фд)
                      and _форма_верна(ц, фц))
    m = ЦЕНТЫ.match(с)
    if m:
        всего, д, фд, ц, фц = (int(m.group(1)), int(m.group(2)),
                               m.group(3), int(m.group(4)), m.group(5))
        k = units.отношение("dollar", "cent")
        return True, (д * k + ц == всего and _форма_верна(д, фд)
                      and _форма_верна(ц, фц))
    return False, False


def обход(явные):
    if явные:
        return [pathlib.Path(п) for п in явные]
    try:
        return worlds(kind="shows")
    except Unreadable as беда:
        print(f"СТАВКИ ОТКАЗ: {беда}")
        sys.exit(2)


def main():
    явные = [а for а in sys.argv[1:] if not а.startswith("-")]
    пути = [п for п in обход(явные) if п.is_file()]
    if not пути:
        print("СТАВКИ ОТКАЗ: обход пуст, судить нечего")
        return 2
    ложных = судимых = 0
    примеры = []
    for путь in пути:
        свои = 0
        with путь.open(encoding="utf-8", errors="replace") as поток:
            for строка in поток:
                судимо, истинно = судить(строка)
                if not судимо:
                    continue
                судимых += 1
                if not истинно:
                    ложных += 1
                    свои += 1
                    if len(примеры) < 4:
                        примеры.append(f"{путь.name}: {строка.strip()[:80]}")
        if свои:
            print(f"  {путь.name:<30} ложных {свои}")
    for п in примеры:
        print(f"    {п}")
    поза = "ЛЕНТА" if явные else (
        "PASS" if ложных <= ЛОЖНЫХ_РУБЕЖ else "FAIL")
    print(f"СТАВКИ {поза}: {ложных} ложных из {судимых} судимых "
          f"({len(пути)} файлов)")
    if явные:
        return 0
    return 0 if ложных <= ЛОЖНЫХ_РУБЕЖ else 1


if __name__ == "__main__":
    sys.exit(main())
