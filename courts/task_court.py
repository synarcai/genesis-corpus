#!/usr/bin/env python3
"""[ЗАДАНИЕ СЛОВОМ COURT] — the word and the sign must name the same operation.

Written WITHOUT A SINGLE DECLARED PATTERN, and that is not a matter of style.
An образец declared in a court IS a genus for the question-width instrument
(М-271), and this world's lines carry no question — so every pattern here would
be a new genus without a question surface, and that debt is guarded by an
absolute number which may not grow. The check is therefore plain string work:
the head, the two numbers, the declared operation word, the sign, the value.

Equality alone would not do. «вычисли 7 минус 8. 7 + 8 = 15.» is true by
arithmetic and false by AGREEMENT OF NOTATIONS — and the arithmetic court, which
already reads every task line of the corpus, would let it through. That gap is
the whole reason this court exists.

The world is CLOSED.
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "tools"))
import taskforms as F  # noqa: E402
import crossforms as C  # noqa: E402

import closedworld  # noqa: E402
from closedworld import Слой  # noqa: E402 — the palata hands the world's name

ЗАМКНУТЫЕ_МИРЫ = frozenset({"task"})
_ЗНАКИ = {з: и for з, и, _ in C.ДЕЙСТВИЯ}


def _числа_и_знак(хвост):
    """«17 + 25 = 42» → (17, '+', 25, 42), или None."""
    части = хвост.split()
    if len(части) != 5 or части[3] != "=":
        return None
    a, знак, b, _, v = части
    if знак not in _ЗНАКИ or not (a.isdigit() and b.isdigit() and v.isdigit()):
        return None
    return int(a), знак, int(b), int(v)


def _судить(строка):
    с = строка.strip()
    if not с.endswith("."):
        return False, False
    части = с[:-1].split(". ", 1)
    if len(части) != 2:
        return False, False
    голова, остаток = части
    # ВТОРАЯ ФОРМА: задание, ВОПРОС и ответ. Вопрос кончается своим знаком, а не
    # точкой, и потому режется по нему, а не по «. » — первая проба резала точкой
    # и не узнала ни одного показа второй формы. Вопрос обязан быть ОБЪЯВЛЕННЫМ
    # вопросом дома: иначе всякая строка с любым вопросом посредине стала бы
    # подсудной этому дому (граница берётся у предмета, М-180-f2).
    хвост = остаток
    for знак_в in ("? ", "？ "):
        if знак_в in остаток:
            вопрос, хвост = остаток.split(знак_в, 1)
            if (вопрос + знак_в.strip()) not in F.ВОПРОСЫ.values():
                return False, False
            break
    разбор = _числа_и_знак(хвост)
    if разбор is None:
        return False, False
    a, знак, b, v = разбор
    # ГОЛОВА: объявленный повелительный зачин своего языка, затем два числа и
    # объявленное слово действия между ними
    # ЗАЧИН МОЖЕТ БЫТЬ ОБЩИМ У ДВУХ ЯЗЫКОВ («calcula» у испанского и
    # португальского), и потому первый совпавший язык НЕ ЕСТЬ ответ: проходятся
    # все, и лишь когда ни один не признал тела, зачин объявляется своим, а тело
    # чужим. Первая проба возвращалась на первом же языке и звала ложью шесть
    # честных португальских показов.
    наш_зачин = False
    for язык, зачины in F.ГОЛОВЫ.items():
        for зачин in зачины:
            if not голова.startswith(зачин + " "):
                continue
            наш_зачин = True
            тело = голова[len(зачин) + 1:]
            # ГОЛОВА ЗНАКОМ («compute 950 − 100.» — мир больших чисел): слова нет,
            # и согласовывать нечего, кроме самого знака и чисел; судится то же
            # согласие обозначений — голова и леджер об одном действии над теми
            # же числами. Прежде такая голова звалась «зачин наш, тело чужое» =
            # ложь, и ворота закрыли честный мир при пересборке под потолком
            # (05.09): суд, выросший головами «compute / find / найди» после
            # рождения мира, захватил его строки. Граница берётся у предмета
            # (М-180-f2): чужой знак или чужие числа в голове — ложь, свои — истина.
            части_тела = тело.split()
            if len(части_тела) == 3 and части_тела[1] in _ЗНАКИ:
                if тело != f"{a} {знак} {b}":
                    return True, False    # голова и леджер о РАЗНЫХ действиях или числах
                if знак == "÷" and (b == 0 or a % b):
                    return True, False
                return True, v == C.значение(знак, a, b)
            слова = C.СЛОВА[язык]
            for знак2, имя, _ in C.ДЕЙСТВИЯ:
                # тело есть либо «{a} слово {b}», либо ИМЯ действия в винительном
                # ЧИСЛА ЗАДАНИЯ — ЦИФРОЙ ИЛИ СЛОВОМ ПАКЕТА («calculate seventeen plus
                # twenty five.»); кузница — цифрами, и слово читается словарём пакета
                A, B = C.числом(язык, a), C.числом(язык, b)
                метки = (f"{a} {слова[имя]} {b}",
                         F.ИМЕНА_ВИН[язык][имя].format(a=a, b=b),
                         f"{A} {слова[имя]} {B}")
                if тело not in метки:
                    continue
                if знак2 != знак:
                    return True, False        # слово и знак о РАЗНЫХ действиях
                if знак == "÷" and (b == 0 or a % b):
                    return True, False
                return True, v == C.значение(знак, a, b)
    return (True, False) if наш_зачин else (False, False)


судить = closedworld.замкнуть(_судить, ЗАМКНУТЫЕ_МИРЫ)


def main():
    import collections
    from genesis import worlds
    с = C.СЛОВА["ru"]
    г = F.ГОЛОВЫ["ru"][0]
    подсадки = (f"{г} 17 {с['плюс']} 25. 17 + 25 = 43.",
                f"{г} 17 {с['минус']} 25. 17 + 25 = 42.",
                f"{г} 17 {с['плюс']} 25. 18 + 25 = 43.",
                # голова знаком: знак головы против знака леджера; числа головы против чисел леджера
                f"{г} 950 + 100. 950 − 100 = 850.",
                f"{г} 900 − 100. 950 − 100 = 850.")
    # ГОЛОВА ЗНАКОМ — ЧЕСТНАЯ СТРАНИЦА ЧУЖОГО МИРА СУДИТСЯ ИСТИНОЙ (bignum, 05.09)
    for честная in (f"{г} 950 − 100. 950 − 100 = 850.", "compute 950 − 100. 950 − 100 = 850."):
        if _судить(честная) != (True, True):
            print(f"  ЧЕСТНАЯ СТРОКА НАЗВАНА {_судить(честная)}: {честная}")
            print("ЗАДАНИЕ СЛОВОМ FAIL: голова знаком судится не истиной")
            return 1
    пойманы = sum(1 for п in подсадки if _судить(п) == (True, False))
    if пойманы != len(подсадки):
        for п in подсадки:
            print(f"  ПОДСАДКА {_судить(п)}: {п[:110]}")
        print(f"ЗАДАНИЕ СЛОВОМ FAIL: подсадок поймано {пойманы} из {len(подсадки)}")
        return 1
    итог = collections.Counter(); примеры = []
    for путь in worlds(kind="shows"):
        if путь.name != "genesis_task.txt":
            continue
        for стр in путь.read_text(encoding="utf-8").splitlines():
            if not стр.strip() or стр.startswith("\x0c"):
                continue
            судимо, истинно = судить(стр)
            итог["судимых" if судимо else "несудимых"] += 1
            if судимо and not истинно:
                итог["ложных"] += 1
                if len(примеры) < 5:
                    примеры.append(стр)
    for п in примеры:
        print(f"  ЛОЖЬ: {п[:120]}")
    поза = "PASS" if итог["ложных"] == 0 and итог["несудимых"] == 0 else "FAIL"
    print(f"ЗАДАНИЕ СЛОВОМ {поза}: {итог['ложных']} ложных из {итог['судимых']} судимых, "
          f"несудимых {итог['несудимых']}; подсадок поймано {пойманы} из {len(подсадки)}")
    return 0 if поза == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
