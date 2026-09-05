#!/usr/bin/env python3
"""[ПЕРЕКРЁСТОК COURT] — the word and the sign must name THE SAME operation.

Two things are recomputed on every line:

  · the value: «17 + 25 = 42» is counted;
  · the AGREEMENT OF THE TWO NOTATIONS: the word standing in the question and
    the sign standing in the answer must be the same operation of the same
    language.

The second is the whole reason the world exists. A line whose question says
«plus» and whose answer counts «×» would be true by arithmetic and false as a
bridge between two notations — and the bridge is what this world teaches.

The world is CLOSED.
"""
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "tools"))
import crossforms as F  # noqa: E402

import closedworld  # noqa: E402
from closedworld import Слой  # noqa: E402 — the palata hands the world's name

ЗАМКНУТЫЕ_МИРЫ = frozenset({"cross"})


def _образцы():
    """ОДИН ОБРАЗЕЦ НА ЯЗЫК, где СЛОВО и ЗНАК захвачены порознь.

    Первая проба ставила по образцу на действие, связывая слово со знаком
    жёстко, — и строка «17 плюс 25? 17 × 25 = 425» не подходила НИ К ОДНОМУ:
    к «плюс» из-за знака, к «умножить» из-за слова. Подсадка не ловилась, и
    мир, чей смысл в СОГЛАСИИ двух записей, молчал ровно там, где они
    расходятся. Слово и знак читаются отдельно, согласие проверяется потом.
    """
    вон = []
    for язык, с in F.СЛОВА.items():
        пр = с.get("пробел_перед_знаком", "")
        головы = "(?:" + "|".join(re.escape(г) for г in с["головы"]) + ")"
        слова = "|".join(re.escape(с[и]) for _, и, _ in
                         sorted(F.ДЕЙСТВИЯ, key=lambda д: len(с[д[1]]), reverse=True))
        знаки = "|".join(re.escape(з) for з, _, _ in F.ДЕЙСТВИЯ)
        # ПРОСЬБА перед вопросом — объявленная строка дома, необязательная группа:
        # «помоги, пожалуйста: сколько будет 17 плюс 25? 17 + 25 = 42.»
        просьбы = "(?:" + "|".join(re.escape(п) + " " for п in F.ПРОСЬБА[язык]) + ")?"
        # ЧИСЛО ВОПРОСА — ЦИФРОЙ ИЛИ СЛОВОМ ПАКЕТА («сколько будет семнадцать плюс
        # двадцать?»); кузница — только цифрами. Слово читается словарём пакета,
        # тем же, каким дом его писал.
        числа = r"(\d+|" + "|".join(re.escape(w) for w in sorted(F.числа_словом(язык).values(), key=len, reverse=True)) + ")"
        вон.append((язык, "слово", re.compile(
            "^" + просьбы + головы + " " + числа + " (" + слова + ") " + числа + re.escape(пр) +
            r"\? (\d+) (" + знаки + r") (\d+) = (\d+)\.$")))
        # ТРИ ЧЛЕНА ЗНАКАМИ — вопрос и кузница несут одну цепь; цепь пересчитывается
        # слева направо, и итог обязан сойтись
        вон.append((язык, "тройка", re.compile(
            "^" + головы + r" (\d+) ([+−]) (\d+) ([+−]) (\d+)" + re.escape(пр) +
            r"\? (\d+) ([+−]) (\d+) ([+−]) (\d+) = (\d+)\.$")))
        # ВОПРОС ЗНАКОМ — та же пара, знак и в вопросе, и в кузнице; голова или голова следования «а теперь»
        вон.append((язык, "знак", re.compile(
            "^(?:" + головы + "|" + re.escape(F.ТЕПЕРЬ[язык]) + r") (\d+) (" + знаки + r") (\d+)" + re.escape(пр) +
            r"\? (\d+) (" + знаки + r") (\d+) = (\d+)\.$")))
        # ЦЕПОЧКА СЛОВАМИ — второе действие названо словом языка, кузница идёт по шагам
        слова_зн = "(?:" + "|".join(re.escape(с[и]) for и in ("плюс", "минус")) + ")"
        вон.append((язык, "цепочка", re.compile(
            "^" + головы + r" (\d+) ([+−]) (\d+), " + re.escape(F.ПОТОМ[язык]) + " (" + слова_зн + r") (\d+)" + re.escape(пр) +
            r"\? (\d+) ([+−]) (\d+) = (\d+), (\d+) ([+−]) (\d+) = (\d+)\.$")))
        # СОГЛАСИЕ СО ЗНАКОМ — обе полярности; цитата в вопросе судится ответом (М-284)
        воп, да, нет = F.СОГЛАСИЕ_ЗНАКОМ[язык]
        for полярность, отв in (("да", да), ("нет", нет)):
            узор = re.escape(воп.format(a="\x01", b="\x02", w="\x03")) + " " + re.escape(отв.format(a="\x01", b="\x02", v="\x04"))
            узор = узор.replace("\x01", r"(\d+)").replace("\x02", r"(\d+)").replace("\x03", r"(\d+)").replace("\x04", r"(\d+)")
            вон.append((язык, "согласие_знаком:" + полярность, re.compile("^" + узор + "$")))
        # СТАРШИНСТВО — произведение впереди, и основание говорит это словами языка
        сн, пт = F.ПОРЯДОК_СЛОВА[язык]
        вон.append((язык, "старшинство", re.compile(
            "^" + головы + r" (\d+) ([+−]) (\d+) × (\d+)" + re.escape(пр) +
            r"\? (\d+) ([+−]) (\d+) × (\d+) = (\d+): " + re.escape(сн) + r" (\d+) × (\d+) = (\d+), " +
            re.escape(пт) + r" (\d+) ([+−]) (\d+) = (\d+)\.$")))
        # ИМЯ ДЕЙСТВИЯ — третья запись той же оси; вопрос объявлен целиком, и
        # потому образец строится из него, а не из головы со словом
        for знак, имя, _ in F.ДЕЙСТВИЯ:
            for вопрос in F.имена_вопросов(язык, имя):
                голова, _, хвост = вопрос.partition("{a}")
                середина, _, конец = хвост.partition("{b}")
                вон.append((язык, "имя:" + знак, re.compile(
                    "^" + re.escape(голова) + r"(\d+)" + re.escape(середина) + r"(\d+)" +
                    re.escape(конец) + r" (\d+) (" + знаки + r") (\d+) = (\d+)\.$")))
        # СОГЛАСИЕ НАД РАВЕНСТВОМ — четвёртая ось, и образец строится ИЗ РАМКИ
        # ЦЕЛИКОМ: рамка объявлена домом, порядок дыр в ней у всякого языка
        # свой («{a} {д} {b} равно {v}» у русского, «{a} {д} {b} {v} is» у
        # голландца), и собирать её из кусков значило бы угадывать строй.
        # Значение стоит в ВОПРОСЕ, и потому суд сверяет ТРИ числа, а не два.
        for рамка in F.СОГЛАСИЕ[язык]:
            for знак, имя, _ in F.ДЕЙСТВИЯ:
                узор = re.escape(рамка.format(a="\x01", b="\x02", v="\x03", д=с[имя]))
                узор = (узор.replace("\x01", r"(\d+)").replace("\x02", r"(\d+)")
                            .replace("\x03", r"(\d+)"))
                вон.append((язык, "согласие:" + знак, re.compile(
                    "^" + узор + " " + re.escape(F.ДА[язык]) +
                    r", (\d+) (" + знаки + r") (\d+) = (\d+)\.$")))
    return tuple(вон)


ОБРАЗЦЫ = _образцы()


def _судить(строка):
    с = строка.strip()
    if not с:
        return False, False
    for язык, вид, образец in ОБРАЗЦЫ:
        м = образец.match(с)
        if not м:
            continue
        if вид == "знак":
            a, з, b, a2, з2, b2, v = м.groups()
            if (a, з, b) != (a2, з2, b2):
                return True, False
            a, b, v = int(a), int(b), int(v)
            if з == "÷" and (b == 0 or a % b):
                return True, False
            return True, v == F.значение(з, a, b)
        if вид == "цепочка":
            a, з1, b, слово, c, a2, з1b, b2, v1, v1b, з2, c2, v = м.groups()
            if (a, з1, b) != (a2, з1b, b2) or v1 != v1b or c != c2:
                return True, False
            по_слову = {F.СЛОВА[язык][и]: F.ЗНАК_СЛОВА[и] for и in ("плюс", "минус")}
            if по_слову.get(слово) != з2:
                return True, False      # слово второго действия и его знак расходятся
            v1_, v_ = F.цепочка_значение((int(a), з1, int(b), {v: k for k, v in F.СЛОВА[язык].items() if k in ("плюс", "минус")}[слово], int(c)))
            return True, int(v1) == v1_ and int(v) == v_
        if вид.startswith("согласие_знаком:"):
            a, b, w, a2, b2, v = (int(x) for x in м.groups())
            if (a, b) != (a2, b2) or v != a + b:
                return True, False
            # «да» подтверждает верное равенство, «нет» отвергает неверное — и только так
            return True, (w == v) == (вид.endswith("да"))
        if вид == "старшинство":
            a, з, b, c, a2, з2, b2, c2, v, b3, c3, p, a4, з4, p4, v4 = м.groups()
            if (a, з, b, c) != (a2, з2, b2, c2) or (b, c) != (b3, c3) or (a, з, p) != (a4, з4, p4) or v != v4:
                return True, False      # цепь, произведение и итог обязаны быть об одном
            p_, v_ = F.старшинство_значение((int(a), з, int(b), int(c)))
            return True, int(p) == p_ and int(v) == v_
        if вид == "тройка":
            a, з1, b, з2, c, a2, з1b, b2, з2b, c2, v = м.groups()
            if (a, з1, b, з2, c) != (a2, з1b, b2, з2b, c2):
                return True, False      # вопрос и кузница о разной цепи
            return True, int(v) == F.тройка_значение((int(a), з1, int(b), з2, int(c)))
        if вид.startswith("согласие:"):
            a, b, v, a2, знак, b2, v2 = м.groups()
            a, b, v, a2, b2, v2 = int(a), int(b), int(v), int(a2), int(b2), int(v2)
            if (a, b) != (a2, b2) or v != v2:
                return True, False      # вопрос и подтверждение о разном
            if знак != вид[len("согласие:"):]:
                return True, False      # слово действия и знак называют РАЗНОЕ
            if знак == "÷" and (b == 0 or a % b):
                return True, False
            return True, v == F.значение(знак, a, b)
        if вид.startswith("имя:"):
            a, b, a2, знак, b2, v = (int(г) if г.isdigit() else г for г in м.groups())
            if (a, b) != (a2, b2):
                return True, False
            if знак != вид[4:]:
                return True, False      # имя действия и знак называют РАЗНОЕ
            if знак == "÷" and (b == 0 or a % b):
                return True, False
            return True, v == F.значение(знак, a, b)
        a, слово, b, a2, знак, b2, v = м.groups()
        по_числу = {w: n for n, w in F.числа_словом(язык).items()}
        a, b = (int(x) if x.isdigit() else по_числу[x] for x in (a, b))
        a2, b2, v = int(a2), int(b2), int(v)
        if (a, b) != (a2, b2):
            return True, False      # вопрос и ответ о разных числах
        по_слову = {F.СЛОВА[язык][и]: з for з, и, _ in F.ДЕЙСТВИЯ}
        if по_слову.get(слово) != знак:
            return True, False      # слово и знак называют РАЗНЫЕ действия
        if знак == "÷" and (b == 0 or a % b):
            return True, False
        return True, v == F.значение(знак, a, b)
    return False, False


судить = closedworld.замкнуть(_судить, ЗАМКНУТЫЕ_МИРЫ)


def main():
    import collections
    from genesis import worlds
    с = F.СЛОВА["ru"]
    # ПРЕДСТАВЛЕННОЕ «НЕТ» (М-106): неверное значение; слово и знак о РАЗНЫХ
    # действиях; числа вопроса и ответа разные.
    подсадки = (f"{с['головы'][0]} 17 {с['плюс']} 25? 17 + 25 = 43.",
                f"{с['головы'][0]} 17 {с['плюс']} 25? 17 × 25 = 425.",
                f"{с['головы'][0]} 17 {с['плюс']} 25? 18 + 25 = 43.",
                # ИМЯ ДЕЙСТВИЯ ПРОТИВ ЗНАКА: сумма, посчитанная умножением
                F.ИМЕНА["ru"]["плюс"].format(a=17, b=25) + " 17 × 25 = 425.",
                # СОГЛАСИЕ, ПОДТВЕРЖДАЮЩЕЕ НЕ ТО, О ЧЁМ СПРОШЕНО: значение в
                # вопросе одно, в ответе другое — третье число и есть новая
                # поверхность лжи, которой у прочих форм нет
                F.СОГЛАСИЕ["ru"][0].format(a=17, b=25, v=43, д=с["плюс"]) + " да, 17 + 25 = 42.",
                F.СОГЛАСИЕ["ru"][1].format(a=17, b=25, v=42, д=с["плюс"]) + " да, 17 × 25 = 425.",
                # просьба с неверным счётом
                f"{F.ПРОСЬБА['ru'][0]} {с['головы'][0]} 17 {с['плюс']} 25? 17 + 25 = 43.")
    пойманы = sum(1 for п in подсадки if _судить(п) == (True, False))
    if пойманы != len(подсадки):
        for п in подсадки:
            print(f"  ПОДСАДКА {_судить(п)}: {п[:110]}")
        print(f"ПЕРЕКРЁСТОК FAIL: подсадок поймано {пойманы} из {len(подсадки)}")
        return 1
    итог = collections.Counter(); примеры = []
    for путь in worlds(kind="shows"):
        if путь.name != "genesis_cross.txt":
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
    print(f"ПЕРЕКРЁСТОК {поза}: {итог['ложных']} ложных из {итог['судимых']} судимых, "
          f"несудимых {итог['несудимых']}; подсадок поймано {пойманы} из {len(подсадки)}")
    return 0 if поза == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
