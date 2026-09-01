#!/usr/bin/env python3
"""[ФОРМЫ ДОКАЗАТЕЛЬСТВА] — судится не имя формы, а её ЭКЗЕМПЛЯР.

Математика делают не теоремы, а ФОРМЫ, в которых показывают истинность.
Форма без экземпляра есть слово, и потому здесь всякий показ несёт
проверяемый случай, а суд его пересчитывает:

  · ИНДУКЦИЯ — основание и шаг. Шаг не утверждается, а ПОКАЗАН на паре
    чисел, и суд проверяет обе стороны равенства «S(n) + (n+1) =
    S(n+1)»: показ, где шаг записан неверно, учит неверному ходу при
    верной теореме.
  · РАЗБОР СЛУЧАЕВ — исчерпывающее деление со свидетелем в каждом
    случае; чётность числа пересчитывается.
  · КОНТРПРИМЕР — всеобщее утверждение, убитое одним свидетелем. Суд
    проверяет самого свидетеля: «2 is prime and 2 is even» ложно, если
    двойка не проста или не чётна.
  · ПРЯМОЕ — условное с экземпляром, где ПОСЫЛКА ВЫПОЛНЕНА. Условное,
    показанное там, где посылка ложна, не учит ничему, и суд требует
    истинности обеих половин.

ЧЕГО ЗДЕСЬ НЕТ: доказательства от противного. Его экземпляры
(иррациональность корня) счётом не проверяются, а форма, чей экземпляр
непроверяем, есть ровно то, что корпус нести отказывается. Она ждёт
суда, умеющего читать вывод.
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


def просто(n):
    return n > 1 and all(n % d for d in range(2, int(n ** 0.5) + 1))


def квадрат(n):
    к = int(n ** 0.5)
    return к * к == n


# свидетели контрпримеров: каждое утверждение проверяется само
СВИДЕТЕЛИ = {
    "2 is prime and 2 is even": lambda: просто(2) and 2 % 2 == 0,
    "0 is whole and 0 is not positive": lambda: 0 <= 0,
    "9 is a square and 9 is odd": lambda: квадрат(9) and 9 % 2 == 1,
    "6 is a multiple of 3 and 6 is even": lambda: 6 % 3 == 0 and 6 % 2 == 0,
}
ЛОЖНЫЕ = {
    "all primes are odd": lambda: False,
    "all whole numbers are positive": lambda: False,
    "every square is even": lambda: False,
    "all multiples of 3 are odd": lambda: False,
}

ШАГ_EN = re.compile(
    r"^if it holds for n = (\d+) then it holds for n = (\d+): "
    r"(\d+) \+ (\d+) = (\d+)$")
ШАГ_RU = re.compile(
    r"^если верно для n = (\d+), то верно и для n = (\d+): "
    r"(\d+) \+ (\d+) = (\d+)$")
СЛУЧАЙ_EN = re.compile(
    r"^every whole number is even or odd; (\d+) is (even|odd)$")
СЛУЧАЙ_RU = re.compile(
    r"^всякое целое чётно или нечётно; (\d+) (чётно|нечётно)$")
КОНТР = re.compile(r"^(.+?) is false: (.+?)$")
ПРЯМОЕ_EN = re.compile(
    r"^if n is even then n squared is even: (\d+) is even and (\d+) "
    r"is even$")
ПРЯМОЕ_RU = re.compile(
    r"^если n чётно, то n в квадрате чётно: (\d+) чётно и (\d+) чётно$")


def судить(строка):
    с = строка.strip().rstrip(".")
    m = ШАГ_EN.match(с) or ШАГ_RU.match(с)
    if m:
        n, следом, слева, добавка, справа = (int(x) for x in m.groups())
        # ШАГ ПРОВЕРЯЕТСЯ ОБЕИМИ СТОРОНАМИ, а не только итогом
        return True, (следом == n + 1
                      and слева == n * (n + 1) // 2
                      and добавка == следом
                      and справа == следом * (следом + 1) // 2
                      and слева + добавка == справа)
    m = СЛУЧАЙ_EN.match(с)
    if m:
        x, род = int(m.group(1)), m.group(2)
        return True, (x % 2 == 0) == (род == "even")
    m = СЛУЧАЙ_RU.match(с)
    if m:
        x, род = int(m.group(1)), m.group(2)
        return True, (x % 2 == 0) == (род == "чётно")
    m = ПРЯМОЕ_EN.match(с) or ПРЯМОЕ_RU.match(с)
    if m:
        n, квадратик = (int(x) for x in m.groups())
        # ПОСЫЛКА ОБЯЗАНА БЫТЬ ВЫПОЛНЕНА, иначе показ ничему не учит
        return True, (n % 2 == 0 and квадратик == n * n
                      and квадратик % 2 == 0)
    m = КОНТР.match(с)
    if m:
        утверждение, свидетель = m.group(1).strip(), m.group(2).strip()
        если = СВИДЕТЕЛИ.get(свидетель)
        если_ложно = ЛОЖНЫЕ.get(утверждение)
        if если is None or если_ложно is None:
            return False, True
        # свидетель обязан быть ИСТИНЕН, а утверждение — ЛОЖНО
        return True, если() and not если_ложно()
    return False, True


def обход(явные):
    if явные:
        return [pathlib.Path(п) for п in явные]
    try:
        return worlds(kind="shows")
    except Unreadable as беда:
        print(f"ДОКАЗАТЕЛЬСТВО ОТКАЗ: {беда}")
        sys.exit(2)


def main():
    явные = [а for а in sys.argv[1:] if not а.startswith("-")]
    пути = [п for п in обход(явные) if п.is_file()]
    if not пути:
        print("ДОКАЗАТЕЛЬСТВО ОТКАЗ: обход пуст, судить нечего")
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
                        примеры.append(f"{путь.name}: {строка.strip()[:90]}")
        if свои:
            print(f"  {путь.name:<30} ложных {свои}")
    for п in примеры:
        print(f"    {п}")
    поза = "ЛЕНТА" if явные else (
        "PASS" if ложных <= ЛОЖНЫХ_РУБЕЖ else "FAIL")
    print(f"ДОКАЗАТЕЛЬСТВО {поза}: {ложных} ложных из {судимых} судимых "
          f"({len(пути)} файлов)")
    if явные:
        return 0
    return 0 if ложных <= ЛОЖНЫХ_РУБЕЖ else 1


if __name__ == "__main__":
    sys.exit(main())
