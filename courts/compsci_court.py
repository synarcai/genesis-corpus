#!/usr/bin/env python3
"""[ОСНОВАНИЯ ИНФОРМАТИКИ] — автомат ЗАПУСКАЕТСЯ, грамматика ВЫВОДИТСЯ.

    автомат чётности: вход 1 0 1; состояние после — чётное.
    правило S → a S b, применённое 3 раза, даёт a a a b b b.
    цикл: x = 0; повторить 3 раза x = x + 2. инвариант: x чётно на
    каждом шаге. выход x = 6.

ВСЁ ИСПОЛНИМО, КРОМЕ ОДНОГО, И ЭТО ОДНО ОБЪЯВЛЕНО КАК ОБЪЯВЛЕННОЕ.
Неразрешимость останова нельзя вычислить — на то она и неразрешимость;
она стоит рядом с вычислимыми вопросами того же слоя, и суд сверяет её
с объявлением, а не с вычислением (М-103).

ИНВАРИАНТ ПРОВЕРЯЕТСЯ НА КАЖДОМ ШАГЕ, А НЕ НА ИТОГЕ: цикл, чей итог
чётен при нечётном промежуточном состоянии, инварианта не имеет, и
показ, назвавший его, лжёт — а по одному итогу этого не увидеть.

УПРАВЛЕНИЕ ТРЕБУЕТ МОДЕЛИ (Конант — Эшби): наблюдатель, не различающий
состояний системы, не может ею управлять, и «возможно» при недостатке
различения есть ложь о мире.
"""
import pathlib
import re
import sys
from fractions import Fraction

КОРЕНЬ = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(КОРЕНЬ / "tools"))
import asking  # noqa: E402
from genesis import Unreadable, worlds  # noqa: E402

# РУБЕЖ-ДОЛГА: ЛОЖНЫХ_РУБЕЖ = 0
ЛОЖНЫХ_РУБЕЖ = 0

# ПУСТОЙ-ОБХОД: no-such-corpus-file

БИТЫ = re.compile(
    r"^(?:(\d+) равновозможных исход\S* несут (\d+) \S+"
    r"|(\d+) равновозможных исход\S*: энтропия (\d+) \S+"
    r"|(\d+) equally likely outcomes carry (\d+) bits?"
    r"|(\d+) equally likely outcomes: entropy (\d+) bits?)\.$")
СЛОВО_БИТ = re.compile(
    r"^(?:слово из (\d+) \S+ алфавита в (\d+) \S+ стоит (\d+) \S+"
    r"|a word of (\d+) signs? over an alphabet of (\d+) signs? "
    r"costs (\d+) bits)\.$")
ЗНАК_БИТ = re.compile(
    r"^(?:a sign of an alphabet of (\d+) signs? costs (\d+) bits?: 2\^(\d+) = (\d+)"
    r"|знак алфавита в (\d+) \S+ стоит (\d+) \S+: 2\^(\d+) = (\d+))\.$")
АВТОМАТ = re.compile(
    r"^(?:автомат чётности: вход ([01 ]+); состояние после — "
    r"(чётное|нечётное)"
    r"|parity automaton: input ([01 ]+); the state after is "
    r"(even|odd))\.$")
ГРАММАТИКА = re.compile(
    r"^(?:правило S → a S b, применённое (\d+) \S+, даёт ([ab ]+)"
    r"|the rule S → a S b applied (\d+) times? gives ([ab ]+))\.$")
ПОРОЖДАЕТ = re.compile(
    r"^(?:формальная грамматика с правилом S → a S b порождает "
    r"строку ([ab ]+)"
    r"|the formal grammar with rule S → a S b generates the "
    r"string ([ab ]+))\.$")
РАЗРЕШИМО = re.compile(
    r"^(?:делится ли (\d+) на (\d+) — вопрос разрешимый; ответ (да|нет)"
    r"|is (\d+) divisible by (\d+) — a decidable question; "
    r"the answer is (yes|no))\.$")
НЕРАЗРЕШИМО = re.compile(
    r"^(?:остановится ли всякая программа на всяком входе — вопрос "
    r"неразрешимый: общего алгоритма нет"
    r"|whether every program halts on every input is undecidable: "
    r"there is no general algorithm)\.$")
# ОТКАЗ ЕСТЬ ТАКОЕ ЖЕ УТВЕРЖДЕНИЕ: «целого нет» истинно ровно тогда,
# когда размер алфавита и вправду не степень двойки. Суд считает сам.
ЦЕЛОСТЬ_АЛФАВИТА = re.compile(
    r"^(?:yes: (\d+) = 2\^(\d+), a sign costs (\d+) bits?"
    r"|no: (\d+) is not a power of two"
    r"|да: (\d+) = 2\^(\d+), знак стоит (\d+) бит\S*"
    r"|нет: (\d+) знак\S* — это не степень двойки)\.$")
ТИП = re.compile(
    r"^(?:тип значения (\d+) — целое; тип значения (\d+) ÷ (\d+) — "
    r"(целое|дробь)"
    r"|the type of (\d+) is whole; the type of (\d+) ÷ (\d+) is "
    r"(whole|a fraction))\.$")
ИНВАРИАНТ = re.compile(
    r"^(?:цикл: x = 0; повторить (\d+) \S+ x = x \+ (\d+)\. инвариант: "
    r"x чётно на каждом шаге\. выход x = (\d+)"
    r"|loop: x = 0; repeat (\d+) times x = x \+ (\d+)\. invariant: "
    r"x is even at every step\. exit x = (\d+))\.$")
ГОМЕОСТАЗ_ИМЯ = re.compile(
    r"^(?:гомеостаз есть удержание величины в пределах от (\d+) до "
    r"(\d+): значение (\d+) допустимо"
    r"|homeostasis is holding a value inside bounds from (\d+) to "
    r"(\d+): the value (\d+) is allowed)\.$")
ГОМЕОСТАЗ = re.compile(
    r"^(?:регулятор держит значение между (\d+) и (\d+): при возмущении "
    r"(-?\d+) он вернул (\d+)"
    r"|the regulator holds the value between (\d+) and (\d+): "
    r"given (-?\d+) it returned (\d+))\.$")
МОДЕЛЬ = re.compile(
    r"^(?:модель системы имеет (\d+) \S+; наблюдатель различает (\d+): "
    r"управление (возможно|невозможно)"
    r"|the model of the system has (\d+) states; the observer tells "
    r"apart (\d+): control is (possible|impossible))\.$")


def _г(m):
    return [x for x in m.groups() if x is not None]


import discourse  # noqa: E402
import laws  # noqa: E402
ЗАКОНЫ = laws.свод("compsci")
ЗАКОН_ЭНТРОПИИ = {"en": laws.ЗАКОНЫ["compsci"][0][2], "ru": laws.ЗАКОНЫ["compsci"][0][3]}
ВОПРОС_ЭНТРОПИИ = re.compile(
    r"^(?:what is the entropy of (\d+) equally likely outcomes|чему равна энтропия (\d+) \S+ \S+"
    r"|why is the entropy of (\d+) equally likely outcomes (\d+) bits?|почему энтропия (\d+) \S+ \S+ равна (\d+) \S+)$")
СВИД_ЭНТРОПИИ = re.compile(r"^2\^(\d+) = (\d+)$")
ВЫВОД_ЭНТРОПИИ = re.compile(r"^(?:(\d+) equally likely outcomes: entropy (\d+) bits?|(\d+) \S+ \S+: энтропия (\d+) \S+)$")


def _рассуждение(с):
    язык = "ru" if re.search(r"[а-яё]", с) else "en"
    ч_ = discourse.части(с, язык)
    if ч_ is None:
        return None
    м = ВОПРОС_ЭНТРОПИИ.match(ч_["вопрос"])
    if not м:
        return None
    if ч_["связка"] is None or ч_["вердикт"] is not None:
        return True, False
    г = [int(x) for x in м.groups() if x is not None]
    n = г[0]
    if n < 2 or n & (n - 1):
        return True, False
    k = n.bit_length() - 1
    if len(г) > 1 and г[1] != k:
        return True, False
    св = СВИД_ЭНТРОПИИ.match(ч_["свидетель"])
    выв = ВЫВОД_ЭНТРОПИИ.match(ч_["вывод"])
    return True, (bool(св) and [int(x) for x in св.groups()] == [k, n]
                  and bool(выв) and [int(x) for x in выв.groups() if x is not None] == [n, k]
                  and ч_["закон"] == ЗАКОН_ЭНТРОПИИ[язык])


def судить(строка):
    """(судимо, истинно) для одной строки."""
    if строка.strip() in ЗАКОНЫ:
        return True, True
    р = _рассуждение(строка.strip())
    if р is not None:
        return р
    # ВОПРОС СУДИТСЯ СВОИМ ОТВЕТОМ, А РОД ОПРЕДЕЛЯЕТСЯ ОТВЕТОМ.
    # Связь половин держит общий дом `tools/asking.py`: величины
    # вопроса суть начальный отрезок величин ответа, и порча любой из
    # них рвёт пару. Без этого суд читал бы вторую половину строки и
    # звал истиной вопрос, спрашивающий о другом.
    если = asking.судить_парой(строка, судить)
    if если is not None:
        return если
    с = строка.strip()
    m = БИТЫ.match(с)
    if m:
        исходов, бит = (int(x) for x in _г(m))
        return True, исходов == 2 ** бит
    m = ЗНАК_БИТ.match(с)
    if m:
        n, b, b2, n2 = (int(x) for x in _г(m))
        return True, n >= 2 and n == 2 ** b and (b2, n2) == (b, n)
    m = СЛОВО_БИТ.match(с)
    if m:
        длина, алфавит, цена = (int(x) for x in _г(m))
        if алфавит < 2 or алфавит & (алфавит - 1):
            return False, True
        return True, цена == длина * (алфавит.bit_length() - 1)
    m = АВТОМАТ.match(с)
    if m:
        г = _г(m)
        единиц = sum(1 for x in г[0].split() if x == "1")
        чётно = единиц % 2 == 0
        return True, чётно == (г[1] in ("чётное", "even"))
    m = ГРАММАТИКА.match(с)
    if m:
        г = _г(m)
        n, слово = int(г[0]), г[1].split()
        return True, слово == ["a"] * n + ["b"] * n
    m = РАЗРЕШИМО.match(с)
    if m:
        г = _г(m)
        a, b, ответ = int(г[0]), int(г[1]), г[2]
        if b == 0:
            return True, False
        return True, (a % b == 0) == (ответ in ("да", "yes"))
    if НЕРАЗРЕШИМО.match(с):
        # ОБЪЯВЛЕННОЕ ЗНАНИЕ: вычислить нельзя, на то и неразрешимость.
        return True, True
    m = ЦЕЛОСТЬ_АЛФАВИТА.match(с)
    if m:
        числа = [int(x) for x in _г(m)]
        if len(числа) == 3:
            n, b, b2 = числа
            return True, b2 == b and n == 2 ** b
        n = числа[0]
        return True, not (n >= 2 and not n & (n - 1))
    m = ТИП.match(с)
    if m:
        г = _г(m)
        a, a2, b, род = int(г[0]), int(г[1]), int(г[2]), г[3]
        if a != a2 or b == 0:
            return True, False
        целое = Fraction(a, b).denominator == 1
        return True, целое == (род in ("целое", "whole"))
    m = ИНВАРИАНТ.match(с)
    if m:
        шагов, прибавка, итог = (int(x) for x in _г(m))
        # ИНВАРИАНТ ПРОВЕРЯЕТСЯ НА КАЖДОМ ШАГЕ, А НЕ НА ИТОГЕ.
        x, держится = 0, True
        for _ in range(шагов):
            x += прибавка
            держится = держится and x % 2 == 0
        return True, держится and x == итог
    m = ПОРОЖДАЕТ.match(с)
    if m:
        слово = _г(m)[0].split()
        n = слово.count("a")
        return True, слово == ["a"] * n + ["b"] * n and n >= 1
    m = ГОМЕОСТАЗ_ИМЯ.match(с)
    if m:
        низ, верх, значение = (int(x) for x in _г(m))
        return True, низ <= значение <= верх
    m = ГОМЕОСТАЗ.match(с)
    if m:
        низ, верх, возмущение, вернул = (int(x) for x in _г(m))
        return True, низ <= верх and вернул == min(max(возмущение, низ),
                                                   верх)
    m = МОДЕЛЬ.match(с)
    if m:
        г = _г(m)
        состояний, различает, вердикт = int(г[0]), int(г[1]), г[2]
        можно = различает >= состояний
        return True, можно == (вердикт in ("возможно", "possible"))
    return False, True


def обход(явные):
    if явные:
        return [pathlib.Path(п) for п in явные]
    try:
        return worlds(kind="shows")
    except Unreadable as беда:
        print(f"ИНФОРМАТИКА ОТКАЗ: {беда}")
        sys.exit(2)


def main():
    явные = [а for а in sys.argv[1:] if not а.startswith("-")]
    пути = [п for п in обход(явные) if п.is_file()]
    if not пути:
        print("ИНФОРМАТИКА ОТКАЗ: обход пуст, судить нечего")
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
    print(f"ИНФОРМАТИКА {поза}: {ложных} ложных из {судимых} судимых "
          f"({len(пути)} файлов)")
    if явные:
        return 0
    return 0 if ложных <= ЛОЖНЫХ_РУБЕЖ else 1


if __name__ == "__main__":
    sys.exit(main())
