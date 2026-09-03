#!/usr/bin/env python3
"""[АЛГОРИТМИЧЕСКАЯ ИСТИНА] — утверждение об операции проверяется её ВЫПОЛНЕНИЕМ.

Корпус, растящий инженера, не вправе нести утверждение, которого никто
не может проверить: непроверяемый показ учит ФОРМЕ знания без его
существа, и организм покупает форму.

Каждый род здесь судится не разбором, а СЧЁТОМ: сортировка
пересортировывается, наибольший общий делитель вычисляется, простота
проверяется делением, двоичная запись строится заново. Прибор не
верит корпусу и не верит породившему его генератору — он считает сам.

ДЕВЯТЬ РОДОВ, ДВЕ ПОВЕРХНОСТИ (английская и русская): порядок
(сортировка, разворот), крайние (максимум, минимум), свёртки (сумма,
длина), теория чисел (нод, нок, простота, факториал, степень),
рекурсия по индексу (Фибоначчи), СЛОЖНОСТЬ (линейный поиск против
двоичного), структуры (стек берёт последнее, очередь — первое),
позиционная запись (двоичная) и деление с частным и остатком.

ЧЕГО ПРИБОР НЕ ВИДИТ, НАЗВАНО: он судит утверждения ОБЪЯВЛЕННЫХ форм и
молчит обо всём прочем; строка, не подошедшая ни под одну, в счёт не
идёт и печатается числом, чтобы молчание не читалось как чистота.
"""
import math
import pathlib
import re
import sys

КОРЕНЬ = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(КОРЕНЬ / "tools"))
import asking  # noqa: E402
from genesis import Unreadable, worlds  # noqa: E402

# РУБЕЖ-ДОЛГА: ЛОЖНЫХ_РУБЕЖ = 0
ЛОЖНЫХ_РУБЕЖ = 0

# ПУСТОЙ-ОБХОД: no-such-corpus-file

Ч = r"(\d+(?: \d+)*)"


def числа(s):
    return [int(x) for x in s.split()]


def просто(n):
    return n > 1 and all(n % d for d in range(2, int(n ** 0.5) + 1))


def фибо(n):
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a


# (образец, проверка) — проверка получает группы и возвращает истинность
ФОРМЫ = [
    (rf"^(?:sorting|сортировка) {Ч} (?:gives|даёт) {Ч}$",
     lambda a, b: sorted(числа(a)) == числа(b)),
    (rf"^(?:reversing|разворот) {Ч} (?:gives|даёт) {Ч}$",
     lambda a, b: числа(a)[::-1] == числа(b)),
    (rf"^the maximum of {Ч} is (\d+)$",
     lambda a, b: max(числа(a)) == int(b)),
    (rf"^максимум {Ч} равен (\d+)$",
     lambda a, b: max(числа(a)) == int(b)),
    (rf"^the minimum of {Ч} is (\d+)$",
     lambda a, b: min(числа(a)) == int(b)),
    (rf"^минимум {Ч} равен (\d+)$",
     lambda a, b: min(числа(a)) == int(b)),
    (rf"^the sum of {Ч} is (\d+)$",
     lambda a, b: sum(числа(a)) == int(b)),
    (rf"^сумма {Ч} равна (\d+)$",
     lambda a, b: sum(числа(a)) == int(b)),
    (rf"^the length of {Ч} is (\d+)$",
     lambda a, b: len(числа(a)) == int(b)),
    (rf"^длина {Ч} равна (\d+)$",
     lambda a, b: len(числа(a)) == int(b)),
    (r"^the gcd of (\d+) and (\d+) is (\d+)$",
     lambda a, b, c: math.gcd(int(a), int(b)) == int(c)),
    (r"^нод (\d+) и (\d+) равен (\d+)$",
     lambda a, b, c: math.gcd(int(a), int(b)) == int(c)),
    (r"^the lcm of (\d+) and (\d+) is (\d+)$",
     lambda a, b, c: int(a) * int(b) // math.gcd(int(a), int(b)) == int(c)),
    (r"^нок (\d+) и (\d+) равен (\d+)$",
     lambda a, b, c: int(a) * int(b) // math.gcd(int(a), int(b)) == int(c)),
    (r"^(\d+) is prime$", lambda a: просто(int(a))),
    (r"^(\d+) is not prime$", lambda a: not просто(int(a))),
    (r"^(\d+) простое$", lambda a: просто(int(a))),
    (r"^(\d+) не простое$", lambda a: not просто(int(a))),
    (r"^the factorial of (\d+) is (\d+)$",
     lambda a, b: math.factorial(int(a)) == int(b)),
    (r"^факториал (\d+) равен (\d+)$",
     lambda a, b: math.factorial(int(a)) == int(b)),
    (r"^(\d+) to the power (\d+) is (\d+)$",
     lambda a, b, c: int(a) ** int(b) == int(c)),
    (r"^(\d+) в степени (\d+) равно (\d+)$",
     lambda a, b, c: int(a) ** int(b) == int(c)),
    (r"^fibonacci number (\d+) is (\d+)$",
     lambda a, b: фибо(int(a)) == int(b)),
    (r"^число фибоначчи номер (\d+) равно (\d+)$",
     lambda a, b: фибо(int(a)) == int(b)),
    (r"^linear search on (\d+) items? takes at most (\d+) steps?$",
     lambda a, b: int(a) == int(b)),
    (r"^линейный поиск по (\d+) элементам требует не более (\d+) шагов$",
     lambda a, b: int(a) == int(b)),
    (r"^binary search on (\d+) items? takes at most (\d+) steps?$",
     lambda a, b: (math.ceil(math.log2(int(a))) if int(a) > 1 else 1) == int(b)),
    (r"^двоичный поиск по (\d+) элементам требует не более (\d+) шагов$",
     lambda a, b: (math.ceil(math.log2(int(a))) if int(a) > 1 else 1) == int(b)),
    (rf"^pushing {Ч} on a stack and popping gives (\d+)$",
     lambda a, b: числа(a)[-1] == int(b)),
    (rf"^положив {Ч} в стек и сняв, получаем (\d+)$",
     lambda a, b: числа(a)[-1] == int(b)),
    (rf"^adding {Ч} to a queue and taking gives (\d+)$",
     lambda a, b: числа(a)[0] == int(b)),
    (rf"^добавив {Ч} в очередь и взяв, получаем (\d+)$",
     lambda a, b: числа(a)[0] == int(b)),
    (r"^(\d+) in binary is ([01]+)$",
     lambda a, b: format(int(a), "b") == b),
    (r"^(\d+) в двоичной записи это ([01]+)$",
     lambda a, b: format(int(a), "b") == b),
    (r"^dividing (\d+) by (\d+) gives quotient (\d+) and remainder (\d+)$",
     lambda a, b, c, d: divmod(int(a), int(b)) == (int(c), int(d))),
    (r"^деление (\d+) на (\d+) даёт частное (\d+) и остаток (\d+)$",
     lambda a, b, c, d: divmod(int(a), int(b)) == (int(c), int(d))),
    # ТА ЖЕ ИСТИНА ИНОЙ ПОВЕРХНОСТЬЮ: слой остатка пишет её короче, и
    # суд, знавший лишь одну запись, молчал о двухстах шестидесяти
    # строках.
    # …WITH ITS LEDGER (03.09): «17 divided by 5 is 3 remainder 2: 5 × 3 = 15,
    # 17 − 15 = 2» — every link is recounted; a ledger is optional in the
    # older shows, but a written ledger must be the division's own
    (r"^(\d+) divided by (\d+) is (\d+) remainder (\d+)(?:: (\d+) × (\d+) = (\d+), (\d+) − (\d+) = (\d+))?$",
     lambda a, b, c, d, *л: divmod(int(a), int(b)) == (int(c), int(d)) and _леджер_деления(a, b, c, d, л)),
    (r"^(\d+) разделить на (\d+) будет (\d+), остаток (\d+)(?:: (\d+) × (\d+) = (\d+), (\d+) − (\d+) = (\d+))?$",
     lambda a, b, c, d, *л: divmod(int(a), int(b)) == (int(c), int(d)) and _леджер_деления(a, b, c, d, л)),
    # ОТКАЗ ЕСТЬ ТАКОЕ ЖЕ УТВЕРЖДЕНИЕ: «места нет» истинно ровно
    # тогда, когда названная длина есть длина ряда И место за нею.
    # Суд считает длину сам, а не верит слову «нет».
    (r"^no item at place (\d+): the list ([\d ]+) has (\d+) items$",
     lambda м, ряд, n: len(числа(ряд)) == int(n) and int(м) > int(n)),
    (r"^на месте (\d+) нет ничего: в списке ([\d ]+) всего (\d+) "
     r"элементов$",
     lambda м, ряд, n: len(числа(ряд)) == int(n) and int(м) > int(n)),
]
def _леджер_деления(a, b, c, d, л):
    """«b × c = bc, a − bc = d» — absent, or the division's own links."""
    if not л or л[0] is None:
        return True
    b1, c1, bc, a1, bc2, d1 = (int(x) for x in л)
    return (b1, c1, a1, d1) == (int(b), int(c), int(a), int(d)) and bc == bc2 == int(b) * int(c) and int(a) - bc == d1


СОБРАНО = [(re.compile(о), ф) for о, ф in ФОРМЫ]


# СОРТИРОВКА ПЕРЕСОРТИРОВЫВАЕТСЯ, А КРАЯ БЕРУТСЯ ИЗ СПИСКА. Показ
# несёт вход, выход и оба края — и всё это ИСПОЛНИМО, а не читаемо.
СОРТИРОВКА = re.compile(
    r"^sort \[([\d ]+)\] → \[([\d ]+)\]\. min = (\d+)\. max = (\d+)\.$")


def сортировка_держится(строка):
    """Верна ли сортировка со своими краями; None — не наше."""
    m = СОРТИРОВКА.match(строка.strip())
    if not m:
        return None
    вход = [int(x) for x in m.group(1).split()]
    выход = [int(x) for x in m.group(2).split()]
    if not вход:
        return None
    return (выход == sorted(вход) and int(m.group(3)) == min(вход)
            and int(m.group(4)) == max(вход))


def судить(строка):
    # ВОПРОС СУДИТСЯ СВОИМ ОТВЕТОМ, А РОД ОПРЕДЕЛЯЕТСЯ ОТВЕТОМ.
    # Связь половин держит общий дом `tools/asking.py`: величины
    # вопроса суть начальный отрезок величин ответа, и порча любой из
    # них рвёт пару. Без этого суд читал бы вторую половину строки и
    # звал истиной вопрос, спрашивающий о другом.
    если = asking.судить_парой(строка, судить)
    if если is not None:
        return если
    сорт = сортировка_держится(строка)
    if сорт is not None:
        return True, сорт

    с = строка.strip().rstrip(".")
    for образец, проверка in СОБРАНО:
        m = образец.match(с)
        if m:
            return True, bool(проверка(*m.groups()))
    return False, True


def обход(явные):
    if явные:
        return [pathlib.Path(п) for п in явные]
    try:
        return worlds(kind="shows")
    except Unreadable as беда:
        print(f"АЛГОРИТМЫ ОТКАЗ: {беда}")
        sys.exit(2)


def main():
    явные = [а for а in sys.argv[1:] if not а.startswith("-")]
    пути = [п for п in обход(явные) if п.is_file()]
    if not пути:
        print("АЛГОРИТМЫ ОТКАЗ: обход пуст, судить нечего")
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
                        примеры.append(f"{путь.name}: {строка.strip()[:70]}")
        if свои:
            print(f"  {путь.name:<30} ложных {свои}")
    for п in примеры:
        print(f"    {п}")
    поза = "ЛЕНТА" if явные else (
        "PASS" if ложных <= ЛОЖНЫХ_РУБЕЖ else "FAIL")
    print(f"АЛГОРИТМЫ {поза}: {ложных} ложных утверждений из {судимых} "
          f"судимых ({len(пути)} файлов)")
    if явные:
        return 0
    return 0 if ложных <= ЛОЖНЫХ_РУБЕЖ else 1


if __name__ == "__main__":
    sys.exit(main())
