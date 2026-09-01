#!/usr/bin/env python3
"""[МАШИННОЕ ПРЕДСТАВЛЕНИЕ] — основание, бит и сдвиг пересчитываются.

Программист встречает одно число в нескольких одеждах и обязан знать,
что число одно. Основания и битовые действия суть самое точно
проверяемое знание, какое бывает, — и прибор здесь ничего не разбирает,
он ПЕРЕСЧИТЫВАЕТ: переводит основание в обе стороны, применяет
операцию, двигает биты.

  · ОСНОВАНИЯ два, восемь и шестнадцать, В ОБЕ СТОРОНЫ: перевод,
    показанный в одну сторону, учит таблице, а не переводу;
  · И, ИЛИ, ИСКЛЮЧАЮЩЕЕ ИЛИ на ОДНОЙ паре, чтобы различие
    встретилось, а не описывалось;
  · СДВИГ судится вместе со своим умножением: сдвиг, не связанный с
    умножением, есть фокус вместо факта;
  · ШИРИНА — сколько значений держит столько-то бит.

ОТРИЦАТЕЛЬНЫХ ЧИСЕЛ НЕТ НАМЕРЕННО: дополнительный код требует
объявленной ширины, и одни и те же биты значат разные числа при разной
ширине. Показанный без ширины, он не факт, а совпадение.
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

ФОРМЫ = [
    (r"^(\d+) in binary is ([01]+)$",
     lambda n, b: format(int(n), "b") == b),
    (r"^([01]+) in binary is (\d+) in decimal$",
     lambda b, n: int(b, 2) == int(n)),
    (r"^(\d+) in octal is ([0-7]+)$",
     lambda n, o: format(int(n), "o") == o),
    (r"^([0-7]+) in octal is (\d+) in decimal$",
     lambda o, n: int(o, 8) == int(n)),
    (r"^(\d+) in hex is ([0-9a-f]+)$",
     lambda n, h: format(int(n), "x") == h),
    (r"^([0-9a-f]+) in hex is (\d+) in decimal$",
     lambda h, n: int(h, 16) == int(n)),
    (r"^(\d+) в двоичной записи это ([01]+)$",
     lambda n, b: format(int(n), "b") == b),
    (r"^(\d+) в шестнадцатеричной записи это ([0-9a-f]+)$",
     lambda n, h: format(int(n), "x") == h),
    (r"^(\d+) and (\d+) is (\d+)$",
     lambda a, b, c: (int(a) & int(b)) == int(c)),
    (r"^(\d+) or (\d+) is (\d+)$",
     lambda a, b, c: (int(a) | int(b)) == int(c)),
    (r"^(\d+) xor (\d+) is (\d+)$",
     lambda a, b, c: (int(a) ^ int(b)) == int(c)),
    (r"^(\d+) и (\d+) побитово это (\d+)$",
     lambda a, b, c: (int(a) & int(b)) == int(c)),
    (r"^(\d+) или (\d+) побитово это (\d+)$",
     lambda a, b, c: (int(a) | int(b)) == int(c)),
    (r"^(\d+) shifted left by (\d+) is (\d+)$",
     lambda a, k, c: (int(a) << int(k)) == int(c)),
    (r"^(\d+) shifted right by (\d+) is (\d+)$",
     lambda a, k, c: (int(a) >> int(k)) == int(c)),
    (r"^(\d+) сдвинутое влево на (\d+) это (\d+)$",
     lambda a, k, c: (int(a) << int(k)) == int(c)),
    (r"^a (\w+) holds (\d+) bits? and (\d+) values$",
     lambda имя, б, v: 2 ** int(б) == int(v)),
    (r"^with (\d+) bits you can write (\d+) numbers?$",
     lambda б, v: 2 ** int(б) == int(v)),
    (r"^(\w+) держит (\d+) \S+ и (\d+) \S+$",
     lambda имя, б, v: 2 ** int(б) == int(v)),
]
СОБРАНО = [(re.compile(о), ф) for о, ф in ФОРМЫ]


def судить(строка):
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
        print(f"МАШИНА ОТКАЗ: {беда}")
        sys.exit(2)


def main():
    явные = [а for а in sys.argv[1:] if not а.startswith("-")]
    пути = [п for п in обход(явные) if п.is_file()]
    if not пути:
        print("МАШИНА ОТКАЗ: обход пуст, судить нечего")
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
    print(f"МАШИНА {поза}: {ложных} ложных из {судимых} судимых "
          f"({len(пути)} файлов)")
    if явные:
        return 0
    return 0 if ложных <= ЛОЖНЫХ_РУБЕЖ else 1


if __name__ == "__main__":
    sys.exit(main())
