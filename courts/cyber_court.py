#!/usr/bin/env python3
"""[КИБЕРНЕТИЧЕСКАЯ ИСТИНА] — управление судится счётом и ОБХОДОМ, не словом.

Кибернетика есть наука об управлении, и это ровно та область, где
корпусу удобнее всего лгать: «обратная связь исправляет систему» —
предложение, которого не проверит никакой прибор. Потому здесь судится
только то, что показано ЧИСЛОМ или ХОДОМ:

  · ОШИБКА есть вычитание, и всякий её шаг — арифметика;
  · СХОДИМОСТЬ есть счёт шагов, и счёт этот моделируется заново;
  · МАШИНА есть набор переходов, и «этот вход ведёт в то состояние» —
    ОБХОД, а не мнение: прибор идёт по переходам сам;
  · НЕОБХОДИМОЕ РАЗНООБРАЗИЕ (закон Эшби) есть отношение между числом
    состояний регулятора и числом различимых возмущений;
  · БИТЫ на n различений суть ceil(log2 n) — тот же факт, что двоичный
    поиск в слое алгоритмов: одно знание, два лица.

РАЗОМКНУТЫЙ И ЗАМКНУТЫЙ КОНТУР судятся тем, ЧТО ОНИ ДЕЛАЮТ: замкнутый
останавливается на нулевой ошибке, разомкнутый делает лишний шаг и
проскакивает ровно на шаг. Различие видно в числах — единственный
способ, которым его можно преподать.
"""
import math
import pathlib
import re
import sys

КОРЕНЬ = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(КОРЕНЬ / "tools"))
from genesis import Unreadable, worlds  # noqa: E402

# РУБЕЖ-ДОЛГА: ЛОЖНЫХ_РУБЕЖ = 0
ЛОЖНЫХ_РУБЕЖ = 0

# ПУСТОЙ-ОБХОД: no-such-corpus-file

ОШИБКА = re.compile(
    r"^(?:target|цель) (\d+), (?:value|значение) (\d+), "
    r"(?:error|ошибка) (\d+)$")
# ПОКАЗ НЕСЁТ СВОЮ ЦЕЛЬ — прибор не помнит предыдущую строку, ибо
# перестановка проходов её уносит.
ШАГ_EN = re.compile(
    r"^target (\d+), value (\d+): after a step of (\d+) the value is "
    r"(\d+) and the error is (\d+)$")
ШАГ_RU = re.compile(
    r"^цель (\d+), значение (\d+): после шага (\d+) значение равно "
    r"(\d+), а ошибка равна (\d+)$")
СХОД_EN = re.compile(
    r"^starting at (\d+) with target (\d+) and step (\d+) the value "
    r"reaches (\d+) in (\d+) steps$")
СХОД_RU = re.compile(
    r"^начав с (\d+) при цели (\d+) и шаге (\d+), значение достигает "
    r"(\d+) за (\d+) \S+$")
ЗАМКНУТ = re.compile(
    r"^target (\d+): a closed loop stops at (\d+) because the error "
    r"is 0$")
РАЗОМКНУТ = re.compile(
    r"^target (\d+): an open loop takes one step more and reaches "
    r"(\d+), overshooting by (\d+)$")
# РЕЖЕТСЯ ПО ПОСЛЕДНЕЙ ТОЧКЕ С ЗАПЯТОЙ, А НЕ ПО ПЕРВОЙ: переходов
# бывает несколько, и нежадный разбор уносил их в утверждение.
МАШИНА = re.compile(r"^machine ([A-Z ]+); (.+)$")
ПЕРЕХОД = re.compile(r"on (\S+) ([A-Z]) goes to ([A-Z])")
ВЕДЁТ = re.compile(r"^from ([A-Z]) the input ([\d ]+) leads to ([A-Z])$")
СЧЁТ = re.compile(
    r"^this machine has (\d+) states and (\d+) transitions$")
РАЗНООБРАЗИЕ = re.compile(
    r"^(?:a regulator with (\d+) states can distinguish (\d+) disturbances"
    r"|регулятор с (\d+) состояниями различает (\d+) \S+)$")
БИТЫ = re.compile(
    r"^(?:to distinguish (\d+) disturbances a regulator needs (\d+) bits"
    r"|чтобы различить (\d+) \S+, регулятору нужно (\d+) \S+)$")


def судить(строка):
    с = строка.strip().rstrip(".")
    m = ОШИБКА.match(с)
    if m:
        ц, з, о = (int(x) for x in m.groups())
        return True, ц - з == о
    m = ШАГ_EN.match(с) or ШАГ_RU.match(с)
    if m:
        ц, з, шаг, знач, ош = (int(x) for x in m.groups())
        return True, знач == з + шаг and ош == ц - знач
    m = СХОД_EN.match(с) or СХОД_RU.match(с)
    if m:
        нач, ц, шаг, дошли, шагов = (int(x) for x in m.groups())
        if шаг == 0:
            return True, False
        # СЧЁТ МОДЕЛИРУЕТСЯ, а не берётся на веру
        v, k = нач, 0
        while v < ц and k <= 1000:
            v += шаг
            k += 1
        return True, v == ц == дошли and k == шагов
    m = ЗАМКНУТ.match(с)
    if m:
        return True, int(m.group(1)) == int(m.group(2))
    m = РАЗОМКНУТ.match(с)
    if m:
        ц, достигли, перелёт = (int(x) for x in m.groups())
        return True, достигли == ц + перелёт
    m = МАШИНА.match(с)
    if m:
        состояния = m.group(1).split()
        куски = [к.strip() for к in m.group(2).split(";")]
        переходы = ПЕРЕХОД.findall("; ".join(куски[:-1]))
        хвост = куски[-1].rstrip(".")
        m2 = ВЕДЁТ.match(хвост)
        if m2:
            узел, вход, ждём = m2.group(1), m2.group(2).split(), m2.group(3)
            таблица = {(a, в): b for в, a, b in переходы}
            for знак in вход:
                узел = таблица.get((узел, знак))
                if узел is None:
                    return True, False
            return True, узел == ждём
        m2 = СЧЁТ.match(хвост)
        if m2:
            return True, (len(состояния) == int(m2.group(1))
                          and len(переходы) == int(m2.group(2)))
        return False, True
    m = РАЗНООБРАЗИЕ.match(с)
    if m:
        а, б = [x for x in m.groups() if x is not None]
        return True, int(а) == int(б)
    m = БИТЫ.match(с)
    if m:
        n, бит = [int(x) for x in m.groups() if x is not None]
        нужно = math.ceil(math.log2(n)) if n > 1 else 1
        return True, нужно == бит
    return False, True


def обход(явные):
    if явные:
        return [pathlib.Path(п) for п in явные]
    try:
        return worlds(kind="shows")
    except Unreadable as беда:
        print(f"КИБЕРНЕТИКА ОТКАЗ: {беда}")
        sys.exit(2)


def main():
    явные = [а for а in sys.argv[1:] if not а.startswith("-")]
    пути = [п for п in обход(явные) if п.is_file()]
    if not пути:
        print("КИБЕРНЕТИКА ОТКАЗ: обход пуст, судить нечего")
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
                        # СТРОКА МАШИНЫ ДЛИННА ПО ПРИРОДЕ: срез в 70
                        # знаков отрезал именно то место, где подлог и
                        # честный показ расходятся, и стенд объявил
                        # прибор слепым, хотя тот находку сделал.
                        примеры.append(
                            f"{путь.name}: {строка.strip()[:120]}")
        if свои:
            print(f"  {путь.name:<30} ложных {свои}")
    for п in примеры:
        print(f"    {п}")
    поза = "ЛЕНТА" if явные else (
        "PASS" if ложных <= ЛОЖНЫХ_РУБЕЖ else "FAIL")
    print(f"КИБЕРНЕТИКА {поза}: {ложных} ложных утверждений из {судимых} "
          f"судимых ({len(пути)} файлов)")
    if явные:
        return 0
    return 0 if ложных <= ЛОЖНЫХ_РУБЕЖ else 1


if __name__ == "__main__":
    sys.exit(main())
