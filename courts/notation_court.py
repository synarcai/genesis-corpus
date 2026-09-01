#!/usr/bin/env python3
"""[ЗАПИСЬ ЧИСЛА] — процент, деньги, смешанное число и знак ASCII.

Одно число носит много одежд, и каждая проверяема своим счётом:
  · ПРОЦЕНТ — доля сотой: «20% of 40 is 8» истинно ровно тогда, когда
    20 × 40 делится на 100 нацело и даёт 8; и мост «20% means 20 out of
    100» проверяется тождеством, а не принимается на веру;
  · ДЕНЬГИ — десятичная точка валюты: «$12.48 makes 1248 cents»
    проверяется как 12 × 100 + 48. Точка внутри суммы есть сосед цифры,
    а не конец фразы, и прибор режет строку так же осторожно, как её
    писал генератор;
  · СМЕШАННОЕ ЧИСЛО — «three and a half»: сумма двух таких есть 2h + 1,
    а не 2h. Первая редакция слоя писала «дважды один с половиной —
    два»: ложь, видная глазом и невидимая всякому прибору, у которого
    нет своего суда для этого рода;
  · ЗНАКИ ASCII — «-», «/», «*»: они живут в бенчмарке и не жили ни в
    одном нашем слое, так что операторный рынок не мог их купить.

ЧИСЛА СЛОВОМ читаются по объявленной таблице — той же, что пишет слой;
слово, не объявленное в ней, не судится и считается отдельно.
"""
import pathlib
import re
import sys

КОРЕНЬ = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(КОРЕНЬ / "tools"))
from genesis import Unreadable, worlds  # noqa: E402

# РУБЕЖ-ДОЛГА: ЛОЖНЫХ_РУБЕЖ = 0
ЛОЖНЫХ_РУБЕЖ = 0

# ПУСТОЙ-ОБХОД: no-such-corpus-file

СЛОВОМ = {
    "one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6,
    "seven": 7, "eight": 8, "nine": 9, "ten": 10, "eleven": 11,
    "twelve": 12, "thirteen": 13, "fourteen": 14, "fifteen": 15,
    "sixteen": 16, "seventeen": 17,
    "один": 1, "два": 2, "три": 3, "четыре": 4, "пять": 5, "шесть": 6,
    "семь": 7, "восемь": 8, "девять": 9, "десять": 10,
    "одиннадцать": 11, "двенадцать": 12, "тринадцать": 13,
    "четырнадцать": 14, "пятнадцать": 15, "шестнадцать": 16,
    "семнадцать": 17,
}

ФОРМЫ = [
    (r"^(\d+)% of (\d+) is (\d+)$",
     lambda p, w, r: int(p) * int(w) % 100 == 0
     and int(p) * int(w) // 100 == int(r)),
    (r"^(\d+)% от (\d+) — это (\d+)$",
     lambda p, w, r: int(p) * int(w) % 100 == 0
     and int(p) * int(w) // 100 == int(r)),
    (r"^what is (\d+)% of (\d+)\? it is (\d+)$",
     lambda p, w, r: int(p) * int(w) // 100 == int(r)),
    (r"^(\d+)% means (\d+) out of 100$", lambda a, b: a == b),
    (r"^(\d+)% значит (\d+) из 100$", lambda a, b: a == b),
    (r"^\$(\d+)\.(\d\d) is (\d+) dollars? and (\d+) cents? in all$",
     lambda d, c, dd, cc: int(d) == int(dd) and int(c) == int(cc)),
    (r"^\$(\d+)\.(\d\d) makes (\d+) cents in all$",
     lambda d, c, n: int(d) * 100 + int(c) == int(n)),
    (r"^(\d+) dollars? and (\d+) cents? make (\d+) cents in all$",
     lambda d, c, n: int(d) * 100 + int(c) == int(n)),
    (r"^how many cents is \$(\d+)\.(\d\d)\? it is (\d+) cents$",
     lambda d, c, n: int(d) * 100 + int(c) == int(n)),
    (r"^\$0\.(\d\d) is (\d+) cents in all$", lambda c, n: int(c) == int(n)),
    (r"^\$(\d+) is (\d+) dollars in all$", lambda d, n: int(d) == int(n)),
    (r"^\$(\d+) makes (\d+) cents in all$",
     lambda d, n: int(d) * 100 == int(n)),
    (r"^(\d+) - (\d+) = (\d+)$", lambda a, b, c: int(a) - int(b) == int(c)),
    (r"^(\d+) / (\d+) = (\d+)$",
     lambda a, b, c: int(b) and int(a) % int(b) == 0
     and int(a) // int(b) == int(c)),
    (r"^(\d+) \* (\d+) = (\d+)$", lambda a, b, c: int(a) * int(b) == int(c)),
]
СОБРАНО = [(re.compile(о), ф) for о, ф in ФОРМЫ]
ПОЛОВИНА_EN = re.compile(
    r"^(\w+) and a half plus \1 and a half is (\w+)$")
ПОЛОВИНА_RU = re.compile(
    r"^(\w+) с половиной плюс \1 с половиной — (\w+)$")
ДВАЖДЫ_EN = re.compile(r"^twice (\w+) and a half is (\w+)$")
ДВАЖДЫ_RU = re.compile(r"^дважды (\w+) с половиной — (\w+)$")


def судить(строка):
    с = строка.strip().rstrip(".")
    for образец, проверка in СОБРАНО:
        m = образец.match(с)
        if m:
            return True, bool(проверка(*m.groups()))
    for образец in (ПОЛОВИНА_EN, ПОЛОВИНА_RU, ДВАЖДЫ_EN, ДВАЖДЫ_RU):
        m = образец.match(с)
        if m:
            h = СЛОВОМ.get(m.group(1).lower())
            итог = СЛОВОМ.get(m.group(2).lower())
            if h is None or итог is None:
                return False, True
            # СУММА ДВУХ «h с половиной» ЕСТЬ 2h + 1
            return True, итог == 2 * h + 1
    return False, True


def обход(явные):
    if явные:
        return [pathlib.Path(п) for п in явные]
    try:
        return worlds(kind="shows")
    except Unreadable as беда:
        print(f"ЗАПИСЬ ОТКАЗ: {беда}")
        sys.exit(2)


def main():
    явные = [а for а in sys.argv[1:] if not а.startswith("-")]
    пути = [п for п in обход(явные) if п.is_file()]
    if not пути:
        print("ЗАПИСЬ ОТКАЗ: обход пуст, судить нечего")
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
    print(f"ЗАПИСЬ {поза}: {ложных} ложных записей из {судимых} судимых "
          f"({len(пути)} файлов)")
    if явные:
        return 0
    return 0 if ложных <= ЛОЖНЫХ_РУБЕЖ else 1


if __name__ == "__main__":
    sys.exit(main())
