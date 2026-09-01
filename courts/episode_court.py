#!/usr/bin/env python3
"""[ЭПИЗОДНАЯ АЛГЕБРА] — итог обязан следовать из частей.

Половина корпуса лежала НЕСУДИМОЙ, и худшие шесть миров стояли на нуле:
сравнение, предметы, агрегат, глаголы, конверсии, связки. Их арифметику
я проверял черновыми скриптами в блокноте — то есть не проверял вовсе,
ибо проверка, которой нет в репозитории, есть память о проверке.

Один род под одним судом: показ называет части и называет итог, и суд
пересчитывает переход. Девять поверхностей одного рода:

  · ПРИБАВЛЕНИЕ  «A got N X. A got M X more. … A holds N+M X.»
  · УБАВЛЕНИЕ    «B had N X. B gave M X away. … B keeps N−M X.»
  · ОДУШЕВЛЁННОЕ «A met N P. A missed M P. … A knows N−M P.»
  · АГРЕГАТ      «A has N X. B has M X. … A and B hold N+M X.»
  · ЦЕПЬ         тот же агрегат на трёх и более носителях;
  · СРАВНЕНИЕ    больше / меньше / во столько-то раз, любым порядком и
                 с носителем как в конце, так и в середине;
  · СТАВКА       «A walks R X every day. how much in K days? … R×K X.»
  · УПАКОВКА     «X come R to a pack. … K packs hold R×K X.»
  · КОНВЕРСИЯ    «1 hour = 60 minutes», «K hours are K×60 minutes».

ПОРЯДОК ЧАСТЕЙ НЕ ЗАКРЕПЛЁН: сравнение пишется и базой вперёд, и
отношением вперёд, и суд читает обе записи одним правилом — иначе он
судил бы поверхность, а не связь.
"""
import pathlib
import re
import sys

КОРЕНЬ = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(КОРЕНЬ / "tools"))
from genesis import Unreadable, worlds  # noqa: E402
from gsm_items import ITEMS  # noqa: E402
from plural import singular  # noqa: E402

# РУБЕЖ-ДОЛГА: ЛОЖНЫХ_РУБЕЖ = 0
ЛОЖНЫХ_РУБЕЖ = 0

# ПУСТОЙ-ОБХОД: no-such-corpus-file

С = r"[a-zа-яё]+"

ПРИБАВЛЕНИЕ = re.compile(
    rf"^({С}) {С} (\d+) ({С})\. \1 {С} (\d+) \3 more\. "
    rf"how many \3 does \1 \w+( \w+)?\? \1 \w+ (\d+) \3\.$")
УБАВЛЕНИЕ = re.compile(
    rf"^({С}) {С} (\d+) ({С})\. \1 {С} (\d+) \3( away)?\. "
    rf"how many \3 does \1 (?:keep|still know)\? \1 \w+ (\d+) \3\.$")
# ПРЕДМЕТ СОГЛАСУЕТСЯ ПО СЧЁТУ, и обратная ссылка на него ЛОЖНА:
# «felix has 1 balloon» рядом с «carla has 5 balloons» — одна и та же
# вещь в двух формах, и суд, требующий буквального совпадения, объявил
# бы показ неразобранным. Формы сводятся органом, а не переписываются.
АГРЕГАТ2 = re.compile(
    rf"^({С}) has (\d+) ({С})\. ({С}) has (\d+) ({С})\. "
    rf"how many ({С}) do (?:\1 and \4|they) [a-z ]+\? "
    rf"\1 and \4 \w+ (\d+) ({С})\.$")
АГРЕГАТ3 = re.compile(
    rf"^({С}) has (\d+) ({С})\. ({С}) has (\d+) ({С})\. "
    rf"({С}) has (\d+) ({С})\. how many ({С}) do [a-z ]+\? "
    rf"[a-z ]+ \w+ (\d+) ({С})\.$")
ПЕРФЕКТ_ПАРА = re.compile(
    rf"^({С}) has ({С}) (\d+) ({С})\. \1 \2 (\d+) ({С})\.$")
БАЗА_ПЕРФЕКТ = re.compile(rf"({С}) has {С} (\d+) ({С})\.")
БОЛЬШЕ_ПЕРФЕКТ = re.compile(
    rf"({С}) has {С} (\d+) (?:{С} )?more(?: {С})? than ({С})\.")
ЖИЗНЬ = re.compile(
    rf"^(?:the ({С}) (?:is a thing|is a person|are (?:on the table|here))"
    rf"|what (?:is|are) the ({С})\?"
    rf"|who are the ({С})\?"
    rf"|{С} likes the ({С})\."
    rf"|{С} looks at the ({С})\.)$")
ПРЕДМЕТЫ = set(ITEMS) | {singular(w) for w in ITEMS}
НЕЗНАКОМЫЕ = []


def _объявлено(имя_файла, имя_списка):
    """Список, объявленный генератором, — читается, а не копируется.

    Вместилища и периоды живут в своём генераторе; суд, носящий их
    копию, разошёлся бы с ним при первой правке любого из двух.
    """
    import ast
    ф = КОРЕНЬ / "tools" / имя_файла
    try:
        дерево = ast.parse(ф.read_text(encoding="utf-8"))
    except OSError:
        return set()
    for узел in ast.walk(дерево):
        if (isinstance(узел, ast.Assign)
                and getattr(узел.targets[0], "id", None) == имя_списка):
            вон = set()
            for пара in ast.literal_eval(узел.value):
                вон |= {str(x) for x in пара}
            return вон
    return set()


ВМЕСТИЛИЩА = _объявлено("gen_genesis_rates.py", "CONTAINERS")
ПЕРИОДЫ = {p.split()[-1] for p in
           _объявлено("gen_genesis_rates.py", "PERIODS")}
# БЕЗЧИСЛОВАЯ ЖИЗНЬ ВМЕСТИЛИЩА И ПЕРИОДА судится принадлежностью
# объявленному: слово, выпавшее из объявления, есть дрейф, и молчание о
# нём читалось бы как чистота.
ЖИЗНЬ_РОДА = re.compile(
    rf"^(?:the ({С}) is a (?:container|period)\."
    rf"|what is a ({С})\?"
    rf"|{С} waits for the ({С})\.)$")
# сравнение: база и отношение, в любом порядке
БАЗА = re.compile(rf"({С}) has (\d+) ({С})\.")
БОЛЬШЕ = re.compile(rf"({С}) has (\d+) (?:{С} )?more(?: {С})? than ({С})\.")
МЕНЬШЕ = re.compile(
    rf"({С}) has (\d+) (?:{С} )?(?:fewer|less)(?: {С})? than ({С})\.")
РАЗ_КОНЕЦ = re.compile(rf"({С}) has (\d+) times as many ({С}) as ({С})\.")
РАЗ_СЕРЕДИНА = re.compile(
    rf"({С}) has (\d+) times the (?:amount|number) of ({С}) that ({С}) has\.")
# МНОЖИТЕЛЬ БЕЗ ЧИСЛОВОГО ТОКЕНА: «twice» и «double» несут двойку в
# слове. Суд, ищущий цифру, такую связь не прочтёт вовсе — а бенчмарк
# пишет ею.
ДВАЖДЫ = re.compile(
    rf"({С}) has (?:twice as many|double the (?:amount|number) of) "
    rf"({С})(?: as | that )({С})(?: has)?\.")
# ВЛОЖЕННАЯ СВЯЗЬ: сложение НАД умножением, внешнее читается после
# внутреннего.
ВЛОЖЕННО = re.compile(
    rf"({С}) has (\d+) more than twice (?:the number of |as many )"
    rf"({С}) (?:that |as )({С})(?: has)?\.")
ИТОГ = re.compile(rf"({С}) (?:holds|owns|keeps|saves|has) (\d+) ({С})\.\s*$")
СТАВКА = re.compile(
    rf"^({С}) ({С}) (\d+) ({С}) (?:every|each|a) (?:day|night)\. "
    rf"how much in (\d+) ({С})\? \1 \2 (\d+) \4 in \5 \6\.$")
УПАКОВКА = re.compile(
    rf"^({С}) come (\d+) to a ({С})\. how many \1 in (\d+) ({С})\? "
    rf"\3 \4 hold (\d+) \1\.$")
# ВОПРОС БЕЗ СВОЕГО МОСТА: ставка объявлена отдельной строкой, и показ
# несёт лишь K и K·N. Отношение проверяется делимостью — итог обязан
# делиться на число вместилищ нацело, иначе показ учит дроби там, где
# её нет.
УПАКОВКА_ВОПРОС = re.compile(
    rf"^how many ({С}) in (\d+) ({С})\? \2 \3 hold (\d+) \1\.$")
# ДОЛЬНАЯ УБЫЛЬ: итог складывается из частей, доля УХОДИТ, остаток
# спрашивается. Три перехода в одном показе, и каждый судится: сумма,
# деление на знаменатель, разность. Доля читается обеими записями —
# косой чертой и словом.
ДОЛЯ_СЛОВОМ = {"a half": 2, "a third": 3, "a quarter": 4, "a fifth": 5,
               "половина": 2, "треть": 3, "четверть": 4,
               "пятая часть": 5}
ДВА_ШАГА = re.compile(
    rf"^({С}) counted (\d+) ({С})\. \1 counted (\d+) more \3\. "
    rf"(1/\d+|a \w+) of the \3 [\w ]+\. how many \3 [\w ]+\? "
    rf"(\d+) \3 [\w ]+\.$")
# НАЧАЛА, СКАЗАННЫЕ СЛОВАМИ, тоже принадлежат слою и тоже судятся — не
# счётом, а принадлежностью объявленному: строка вне объявления есть
# дрейф, который иначе никто не заметит.
НАЧАЛА = {
    "a part goes and a part remains.",
    "what is left is the whole minus what went.",
}
ОДИН_ШАГ = re.compile(
    rf"^({С}) had (\d+) ({С})\. (1/\d+|a \w+) of the \3 [\w ]+\. "
    rf"how many \3 (?:remain|are left|stay)\? (\d+) \3 "
    rf"(?:remain|are left|stay)\.$")
УШЕДШЕЕ = re.compile(
    rf"^({С}) had (\d+) ({С})\. (1/\d+|a \w+) of the \3 [\w ]+\. "
    rf"how many \3 went\? (\d+) \3 went\.$")
УБЫЛЬ_RU = re.compile(
    r"^у \w+ было (\d+) (\S+)\. (половина|треть|четверть|пятая часть) "
    r"(\S+) ушла\. сколько \4 осталось\? осталось (\d+) (\S+)\.$")


def знаменатель(текст):
    if текст.startswith("1/"):
        return int(текст[2:])
    return ДОЛЯ_СЛОВОМ.get(текст)


КОНВЕРСИЯ = re.compile(rf"^1 ({С}) = (\d+) ({С})\.$")
КОНВЕРСИЯ_К = re.compile(rf"^(\d+) ({С}) (?:=|are) (\d+) ({С})\.$")
ДЕРЖИТ = re.compile(rf"^a ({С}) holds (\d+) ({С})\.$")


def судить(строка):
    с = строка.strip()
    m = ПРИБАВЛЕНИЕ.match(с)
    if m:
        a, b, итог = int(m.group(2)), int(m.group(4)), int(m.group(6))
        return True, a + b == итог
    m = УБАВЛЕНИЕ.match(с)
    if m:
        a, b, итог = int(m.group(2)), int(m.group(4)), int(m.group(6))
        return True, a - b == итог
    m = АГРЕГАТ3.match(с)
    if m:
        вещи = {singular(m.group(i)) for i in (3, 6, 9, 10, 12)}
        x, y, z, итог = (int(m.group(i)) for i in (2, 5, 8, 11))
        return True, len(вещи) == 1 and x + y + z == итог
    m = АГРЕГАТ2.match(с)
    if m:
        вещи = {singular(m.group(i)) for i in (3, 6, 7, 9)}
        x, y, итог = (int(m.group(i)) for i in (2, 5, 8))
        return True, len(вещи) == 1 and x + y == итог
    m = ПЕРФЕКТ_ПАРА.match(с)
    if m:
        # «A has V-ed N X. A V-ed N X.» — перфект рядом со своим
        # прошедшим: числа обязаны совпасть, иначе пара учит разному.
        вещи = {singular(m.group(4)), singular(m.group(6))}
        return True, len(вещи) == 1 and int(m.group(3)) == int(m.group(5))
    m = ЖИЗНЬ.match(с)
    if m:
        слово = next(г for г in m.groups() if г)
        return True, слово in ПРЕДМЕТЫ
    m = ЖИЗНЬ_РОДА.match(с)
    if m:
        слово = next(г for г in m.groups() if г)
        известно = ВМЕСТИЛИЩА | ПЕРИОДЫ | {singular(w) for w in ВМЕСТИЛИЩА}
        if слово in известно:
            return True, True
        # СУД НЕ СУДИТ ТОГО, ЧЕМ НЕ ВЛАДЕЕТ. Поверхность «what is a X?»
        # общая для многих слоёв: доли спрашивают ею о трети, остаток —
        # об остатке. Объявив ложью всё, чего не знает сам, этот суд
        # обвинил бы чужие честные показы — и обвинил, пока не был
        # поправлен. Незнакомое слово уходит в СЧЁТ, а не в приговор.
        НЕЗНАКОМЫЕ.append(слово)
        return False, True
    m = СТАВКА.match(с)
    if m:
        ставка, k, итог = int(m.group(3)), int(m.group(5)), int(m.group(7))
        return True, ставка * k == итог
    m = УПАКОВКА.match(с)
    if m:
        ставка, k, итог = int(m.group(2)), int(m.group(4)), int(m.group(5))
        return True, ставка * k == итог
    if с in НАЧАЛА:
        return True, True
    m = ДВА_ШАГА.match(с)
    if m:
        a, b, зн = int(m.group(2)), int(m.group(4)), знаменатель(m.group(5))
        осталось = int(m.group(6))
        if зн is None:
            return False, True
        всего = a + b
        return True, всего % зн == 0 and всего - всего // зн == осталось
    m = ОДИН_ШАГ.match(с)
    if m:
        всего, зн = int(m.group(2)), знаменатель(m.group(4))
        осталось = int(m.group(5))
        if зн is None:
            return False, True
        return True, всего % зн == 0 and всего - всего // зн == осталось
    m = УШЕДШЕЕ.match(с)
    if m:
        всего, зн = int(m.group(2)), знаменатель(m.group(4))
        ушло = int(m.group(5))
        if зн is None:
            return False, True
        return True, всего % зн == 0 and всего // зн == ушло
    m = УБЫЛЬ_RU.match(с)
    if m:
        всего, зн = int(m.group(1)), знаменатель(m.group(3))
        осталось = int(m.group(5))
        if зн is None:
            return False, True
        return True, всего % зн == 0 and всего - всего // зн == осталось
    m = УПАКОВКА_ВОПРОС.match(с)
    if m:
        k, итог = int(m.group(2)), int(m.group(4))
        return True, k > 0 and итог % k == 0
    m = КОНВЕРСИЯ.match(с) or ДЕРЖИТ.match(с)
    if m:
        # отношение объявляется показом; судить нечего, кроме его формы
        return False, True
    m = КОНВЕРСИЯ_К.match(с)
    if m:
        k, итог = int(m.group(1)), int(m.group(3))
        return True, итог % k == 0 if k else False
    # СРАВНЕНИЕ: части в любом порядке, итог в конце
    итог_m = ИТОГ.search(с)
    if итог_m:
        база = {им: int(n) for им, n, _ in БАЗА.findall(с)}
        база.update({им: int(n) for им, n, _ in БАЗА_ПЕРФЕКТ.findall(с)})
        кто, сколько = итог_m.group(1), int(итог_m.group(2))
        # ВЛОЖЕННОЕ ЧИТАЕТСЯ ПЕРВЫМ: «3 more than twice the number of X»
        # содержит и «more than», и множитель, и суд, взявший внешнее
        # отношение отдельно, посчитал бы 2·база вместо 2·база + 3.
        m = ВЛОЖЕННО.search(с)
        if m:
            a, d, b = m.group(1), int(m.group(2)), m.group(4)
            if a == кто and b in база:
                return True, база[b] * 2 + d == сколько
        m = ДВАЖДЫ.search(с)
        if m:
            a, b = m.group(1), m.group(3)
            if a == кто and b in база:
                return True, база[b] * 2 == сколько
        for рег, действие in (
                (БОЛЬШЕ, lambda o, d: o + d),
                (БОЛЬШЕ_ПЕРФЕКТ, lambda o, d: o + d),
                (МЕНЬШЕ, lambda o, d: o - d),
                (РАЗ_КОНЕЦ, lambda o, d: o * d),
                (РАЗ_СЕРЕДИНА, lambda o, d: o * d)):
            m = рег.search(с)
            if not m:
                continue
            a, d = m.group(1), int(m.group(2))
            b = m.group(4) if рег in (РАЗ_КОНЕЦ, РАЗ_СЕРЕДИНА) else m.group(3)
            if a != кто or b not in база:
                continue
            return True, действие(база[b], d) == сколько
    return False, True


def обход(явные):
    if явные:
        return [pathlib.Path(п) for п in явные]
    try:
        return worlds(kind="shows")
    except Unreadable as беда:
        print(f"ЭПИЗОД ОТКАЗ: {беда}")
        sys.exit(2)


def main():
    явные = [а for а in sys.argv[1:] if not а.startswith("-")]
    пути = [п for п in обход(явные) if п.is_file()]
    if not пути:
        print("ЭПИЗОД ОТКАЗ: обход пуст, судить нечего")
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
                        примеры.append(f"{путь.name}: {строка.strip()[:110]}")
        if свои:
            print(f"  {путь.name:<30} ложных {свои}")
    for п in примеры:
        print(f"    {п}")
    поза = "ЛЕНТА" if явные else (
        "PASS" if ложных <= ЛОЖНЫХ_РУБЕЖ else "FAIL")
    print(f"ЭПИЗОД {поза}: {ложных} ложных из {судимых} судимых "
          f"({len(пути)} файлов)"
          + (f", вне владения {len(set(НЕЗНАКОМЫЕ))} слов: "
             f"{sorted(set(НЕЗНАКОМЫЕ))[:5]}" if НЕЗНАКОМЫЕ else ""))
    if явные:
        return 0
    return 0 if ложных <= ЛОЖНЫХ_РУБЕЖ else 1


if __name__ == "__main__":
    sys.exit(main())
