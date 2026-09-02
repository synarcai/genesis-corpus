#!/usr/bin/env python3
"""[СЧЁТ И СЛУЧАЙ] — середина набора, число способов и счёт исходов.

Учёного делают две привычки прежде всякой теории: считать, сколькими
способами дело может случиться, и спрашивать, где середина набора. Обе
проверяемы точно, и обе судятся здесь пересчётом, а не разбором.

  · СРЕДНЕЕ судится только там, где сумма делится на длину: среднее
    3.5 потребовало бы записи для половин, которой корпус не владеет,
    а округление учило бы округление как истину;
  · МЕДИАНА и РАЗМАХ деления не требуют вовсе и потому не лгут никогда;
  · ВЫБОР и РАССТАНОВКА — два способа, которыми множество рождает
    число, и различие между ними есть первое, чего считающий не вправе
    путать; показ «choosing is not arranging» судится обоими счётами
    сразу;
  · СЛУЧАЙ — счёт исходов, а не десятичная дробь: «благоприятных 3 из
    6» есть факт о счёте, «вероятность 0.5» — факт о записи, которой
    корпус ещё не заслужил.
"""
import math
import pathlib
import re
import sys

КОРЕНЬ = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(КОРЕНЬ / "tools"))
import asking  # noqa: E402
import discourse  # noqa: E402
from genesis import Unreadable, worlds  # noqa: E402

# РУБЕЖ-ДОЛГА: ЛОЖНЫХ_РУБЕЖ = 0
ЛОЖНЫХ_РУБЕЖ = 0

# ПУСТОЙ-ОБХОД: no-such-corpus-file

Ч = r"(\d+(?: \d+)*)"


def числа(s):
    return [int(x) for x in s.split()]


ФОРМЫ = [
    (rf"^the mean of {Ч} is (\d+)$",
     lambda a, b: sum(числа(a)) % len(числа(a)) == 0
     and sum(числа(a)) // len(числа(a)) == int(b)),
    (rf"^среднее {Ч} равно (\d+)$",
     lambda a, b: sum(числа(a)) % len(числа(a)) == 0
     and sum(числа(a)) // len(числа(a)) == int(b)),
    (rf"^the median of {Ч} is (\d+)$",
     lambda a, b: sorted(числа(a))[len(числа(a)) // 2] == int(b)),
    (rf"^медиана {Ч} равна (\d+)$",
     lambda a, b: sorted(числа(a))[len(числа(a)) // 2] == int(b)),
    (rf"^the range of {Ч} is (\d+)$",
     lambda a, b: max(числа(a)) - min(числа(a)) == int(b)),
    (rf"^размах {Ч} равен (\d+)$",
     lambda a, b: max(числа(a)) - min(числа(a)) == int(b)),
    (r"^choosing (\d+) from (\d+) gives (\d+) ways?$",
     lambda k, n, r: math.comb(int(n), int(k)) == int(r)),
    (r"^выбор (\d+) из (\d+) даёт (\d+) способ\S*$",
     lambda k, n, r: math.comb(int(n), int(k)) == int(r)),
    (r"^arranging (\d+) items gives (\d+) orders?$",
     lambda p, r: math.factorial(int(p)) == int(r)),
    (r"^расстановка (\d+) предмет\S* даёт (\d+) порядк\S*$",
     lambda p, r: math.factorial(int(p)) == int(r)),
    (r"^choosing is not arranging: (\d+) from (\d+) gives (\d+), "
     r"arranging \1 of them gives (\d+)$",
     lambda k, n, c, a: math.comb(int(n), int(k)) == int(c)
     and math.comb(int(n), int(k)) * math.factorial(int(k)) == int(a)),
    (r"^a trial has (\d+) outcomes; .+ happens in (\d+) of them$",
     lambda n, k: 0 <= int(k) <= int(n)),
    (r"^испытание имеет (\d+) исход\S*; благоприятных (\d+)$",
     lambda n, k: 0 <= int(k) <= int(n)),
    (r"^(\d+) coins give (\d+) outcomes$",
     lambda n, r: 2 ** int(n) == int(r)),
    (r"^(\d+) монет\S* дают (\d+) исход\S*$",
     lambda n, r: 2 ** int(n) == int(r)),
    # ОТКАЗ ЕСТЬ ТАКОЕ ЖЕ УТВЕРЖДЕНИЕ: «единственной середины нет»
    # истинно ровно тогда, когда названное число элементов и вправду
    # число элементов И оно чётно. Суд считает оба, а не верит слову.
    (rf"^no single middle for {Ч}: the count (\d+) is even$",
     lambda a, n: len(числа(a)) == int(n) and int(n) % 2 == 0),
    (rf"^единственной середины нет у {Ч}: элементов (\d+), "
     r"а это чётное число$",
     lambda a, n: len(числа(a)) == int(n) and int(n) % 2 == 0),
]
СОБРАНО = [(re.compile(о), ф) for о, ф in ФОРМЫ]


# ДОЛЯ РАВНОВОЗМОЖНОГО ИСХОДА ЕСТЬ ЕДИНИЦА НА ЧИСЛО ИСХОДОВ, и показ
# несёт оба числа сам: «монета: исходов 2. доля орла = 1/2».
ДОЛЯ_ИСХОДА = re.compile(
    r"^[^:]+: исходов (\d+)\. доля \S+ = (\d+)/(\d+)\.$")


def доля_сходится(строка):
    """Сходится ли доля с числом исходов; None — не наше."""
    m = ДОЛЯ_ИСХОДА.match(строка.strip())
    if not m:
        return None
    исходов, ч, зн = (int(г) for г in m.groups())
    return зн == исходов and ч == 1


# ------------------------------------------------------- РАССУЖДЕНИЕ
ЗАКОН_СРЕДНЕЕ = {"en": "the mean of a list is the sum of its numbers divided by their count.",
                 "ru": "среднее списка — это сумма его чисел, делённая на их количество."}
ЗАКОН_МЕДИАНА = {"en": "the median of a list of odd length is the middle number when the list is sorted.",
                 "ru": "медиана списка нечётной длины — это среднее по порядку число, когда список упорядочен."}
ЗАКОНЫ = set(ЗАКОН_СРЕДНЕЕ.values()) | set(ЗАКОН_МЕДИАНА.values())
ОПРЕДЕЛЕНИЯ_РАССУЖДЕНИЯ = {f"what is the mean of a list? {ЗАКОН_СРЕДНЕЕ['en']}", f"что такое среднее списка? {ЗАКОН_СРЕДНЕЕ['ru']}",
                           f"what is the median of a list? {ЗАКОН_МЕДИАНА['en']}", f"что такое медиана списка? {ЗАКОН_МЕДИАНА['ru']}"}
ВОПРОС_СРЕДНЕГО = re.compile(r"^(?:what is the mean of ([\d ]+)|чему равно среднее ([\d ]+)|why is the mean of ([\d ]+) equal to (\d+)|почему среднее ([\d ]+) равно (\d+))$")
ВОПРОС_МЕДИАНЫ = re.compile(r"^(?:what is the median of ([\d ]+)|чему равна медиана ([\d ]+)|why is the median of ([\d ]+) equal to (\d+)|почему медиана ([\d ]+) равна (\d+))$")
СВИД_СРЕДНЕГО = re.compile(r"^([\d +]+) = (\d+) (?:and|и) (\d+) ÷ (\d+) = (\d+)$")
СВИД_МЕДИАНЫ = re.compile(r"^(?:sorted it is ([\d ]+) and the middle is (\d+)|по порядку это ([\d ]+), и середина — (\d+))$")


def _рассуждение(с):
    язык = "ru" if re.search(r"[а-яё]", с) else "en"
    ч_ = discourse.части(с, язык)
    if ч_ is None:
        return None
    # РОД ОПРЕДЕЛЯЕТСЯ ВОПРОСОМ: чужое рассуждение (простота, корень) суду
    # статистики не подсудно — он молчит, а не зовёт ложью (гейт 03.09:
    # 130 честных строк дознания были названы ложью судом статистики).
    if not (ВОПРОС_СРЕДНЕГО.match(ч_["вопрос"]) or ВОПРОС_МЕДИАНЫ.match(ч_["вопрос"])):
        return None
    if ч_["связка"] is None or ч_["вердикт"] is not None:
        return True, False
    м = ВОПРОС_СРЕДНЕГО.match(ч_["вопрос"])
    if м:
        г = [x for x in м.groups() if x is not None]
        ряд = числа(г[0]); n = len(ряд); s_ = sum(ряд)
        if n == 0 or s_ % n:
            return True, False
        m = s_ // n
        if len(г) > 1 and int(г[1]) != m:
            return True, False
        мм = СВИД_СРЕДНЕГО.match(ч_["свидетель"])
        верно = (bool(мм) and [int(x) for x in мм.group(1).split(" + ")] == ряд and int(мм.group(2)) == s_
                 and int(мм.group(3)) == s_ and int(мм.group(4)) == n and int(мм.group(5)) == m)
        суд_выв = судить(ч_["вывод"] + ".")
        return True, (верно and суд_выв == (True, True) and str(m) in ч_["вывод"] and ч_["закон"] == ЗАКОН_СРЕДНЕЕ[язык])
    м = ВОПРОС_МЕДИАНЫ.match(ч_["вопрос"])
    if м:
        г = [x for x in м.groups() if x is not None]
        ряд = числа(г[0]); n = len(ряд)
        if n % 2 == 0:
            return True, False
        med = sorted(ряд)[n // 2]
        if len(г) > 1 and int(г[1]) != med:
            return True, False
        мм = СВИД_МЕДИАНЫ.match(ч_["свидетель"])
        гг = [x for x in мм.groups() if x is not None] if мм else []
        верно = bool(гг) and числа(гг[0]) == sorted(ряд) and int(гг[1]) == med
        суд_выв = судить(ч_["вывод"] + ".")
        return True, (верно and суд_выв == (True, True) and str(med) in ч_["вывод"] and ч_["закон"] == ЗАКОН_МЕДИАНА[язык])
    return None


def судить(строка):
    # ВОПРОС СУДИТСЯ СВОИМ ОТВЕТОМ, А РОД ОПРЕДЕЛЯЕТСЯ ОТВЕТОМ.
    # Связь половин держит общий дом `tools/asking.py`: величины
    # вопроса суть начальный отрезок величин ответа, и порча любой из
    # них рвёт пару. Без этого суд читал бы вторую половину строки и
    # звал истиной вопрос, спрашивающий о другом.
    # РАССУЖДЕНИЕ И ЗАКОНЫ РОДОВ — прежде дома пары: ответ-рассуждение есть
    # несколько предложений, и судится частями (дом речи).
    с0 = строка.strip()
    if с0 in ЗАКОНЫ or с0 in ОПРЕДЕЛЕНИЯ_РАССУЖДЕНИЯ:
        return True, True
    р = _рассуждение(с0)
    if р is not None:
        return р
    если = asking.судить_парой(строка, судить)
    if если is not None:
        return если
    доля = доля_сходится(строка)
    if доля is not None:
        return True, доля

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
        print(f"СТАТИСТИКА ОТКАЗ: {беда}")
        sys.exit(2)


def main():
    явные = [а for а in sys.argv[1:] if not а.startswith("-")]
    пути = [п for п in обход(явные) if п.is_file()]
    if not пути:
        print("СТАТИСТИКА ОТКАЗ: обход пуст, судить нечего")
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
    print(f"СТАТИСТИКА {поза}: {ложных} ложных из {судимых} судимых "
          f"({len(пути)} файлов)")
    if явные:
        return 0
    return 0 if ложных <= ЛОЖНЫХ_РУБЕЖ else 1


if __name__ == "__main__":
    sys.exit(main())
